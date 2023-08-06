#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "structmember.h"

// Helper C types

enum parser_state {
    STATE_AFTER_ROW,
    STATE_AFTER_DELIM,
    STATE_IN_CELL,
    STATE_ESCAPE,
    STATE_IN_CELL_QUOTED,
    STATE_ESCAPE_QUOTED,
    STATE_QUOTE_IN_QUOTED,
    STATE_EAT_NEWLINE,
};

enum parser_quoting { QUOTING_NONE, QUOTING_NONNUMERIC, QUOTING_OTHER };

// Helper functions

PyObject* return_self(PyObject* o) {
    Py_XINCREF(o);
    return o;
}

// Dialect handling

typedef struct {
    Py_UCS4 delimiter;
    Py_UCS4 quote_char;
    Py_UCS4 escape_char;
    uint8_t quoting;
    bool skip_initial_space;
    bool double_quote;
    bool strict;
} dialect_t;

int dialect_from_python_object(PyObject* p, dialect_t* d) {
    PyObject* attr = NULL;

    // delimiter
    attr = PyObject_GetAttrString(p, "delimiter");
    if (!attr) {
        PyErr_SetString(PyExc_AttributeError, "dialect: missing delimiter");
        return 1;
    }
    d->delimiter = PyUnicode_ReadChar(attr, 0);
    Py_DECREF(attr);
    if (!d->delimiter) return 1;

    // quote_char
    attr = PyObject_GetAttrString(p, "quotechar");
    if (attr) {
        d->quote_char = PyUnicode_ReadChar(attr, 0);
        PyErr_Clear();
        Py_DECREF(attr);
    } else {
        d->quote_char = 0;
    }

    // escape_char
    attr = PyObject_GetAttrString(p, "escapechar");
    if (attr) {
        d->escape_char = PyUnicode_ReadChar(attr, 0);
        PyErr_Clear();
        Py_DECREF(attr);
    } else {
        d->escape_char = 0;
    }

    // quoting
    attr = PyObject_GetAttrString(p, "quoting");
    if (attr) {
        // retrieve the value as an integer
        long quoting_value = PyLong_AsLong(attr);
        if (quoting_value == -1) {
            Py_DECREF(attr);
            return 1;
        }

        // convert csv enum values to internal values
        // FIXME: Import csv and get the values that way?
        if (quoting_value == 2) {
            d->quoting = QUOTING_NONNUMERIC;
        } else if (quoting_value == 3) {
            d->quoting = QUOTING_NONE;
        } else {
            d->quoting = QUOTING_OTHER;
        }
        PyErr_Clear();
        Py_DECREF(attr);
    } else {
        d->quoting = QUOTING_OTHER;
    }

    // skip_initial_space
    attr = PyObject_GetAttrString(p, "skipinitialspace");
    if (attr) {
        int truthy = PyObject_IsTrue(attr);
        if (truthy < 0) {
            Py_DECREF(attr);
            return 1;
        } else if (truthy == 0) {
            d->skip_initial_space = false;
        } else {
            d->skip_initial_space = true;
        }
        PyErr_Clear();
        Py_DECREF(attr);
    } else {
        d->skip_initial_space = false;
    }

    // double_quote
    attr = PyObject_GetAttrString(p, "doublequote");
    if (attr) {
        int truthy = PyObject_IsTrue(attr);
        if (truthy < 0) {
            Py_DECREF(attr);
            return 1;
        } else if (truthy == 0) {
            d->double_quote = false;
        } else {
            d->double_quote = true;
        }
        PyErr_Clear();
        Py_DECREF(attr);
    } else {
        d->double_quote = false;
    }

    // strict
    attr = PyObject_GetAttrString(p, "strict");
    if (attr) {
        int truthy = PyObject_IsTrue(attr);
        if (truthy < 0) {
            Py_DECREF(attr);
            return 1;
        } else if (truthy == 0) {
            d->strict = false;
        } else {
            d->strict = true;
        }
        PyErr_Clear();
        Py_DECREF(attr);
    } else {
        d->strict = false;
    }

    return 0;
}

// Parser class definition

typedef struct {
    PyObject_HEAD;
    PyObject* reader;
    dialect_t dialect;
    long state;
} parser_t;

typedef struct {
    PyObject_HEAD;
    parser_t* parser;

    PyObject* awaited_coroutine_iter;
} parser_anext_coro_t;

// parser methods

static PyObject* parser_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    (void)args;
    (void)kwds;
    parser_t* o = (parser_t*)type->tp_alloc(type, 0);
    if (o) {
        o->reader = NULL;
        memset(&o->dialect, 0, sizeof(dialect_t));
    }
    return (PyObject*)o;
}

static int parser_init(parser_t* self, PyObject* args, PyObject* kwds) {
    // Parse the arguments
    static char* kw_list[] = {"reader", "dialect", NULL};
    PyObject* reader_obj = NULL;
    PyObject* dialect_obj = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO", kw_list, &reader_obj, &dialect_obj)) {
        return -1;
    }

    // Ensure we got a reader
    assert(reader_obj);
    Py_INCREF(reader_obj);
    self->reader = reader_obj;

    // Parse the dialect object
    if (dialect_from_python_object(dialect_obj, &self->dialect)) {
        Py_DECREF(dialect_obj);
        return -1;
    }

    Py_DECREF(dialect_obj);
    self->state = 0;
    return 0;
}

static void parser_dealloc(parser_t* self) {
    Py_XDECREF(self->reader);
    Py_TYPE(self)->tp_free(self);
}

// Forward declarations for parser_anext
static PyTypeObject parser_anext_coro_python_type;

PyObject* parser_anext(parser_t* self) {
    // See: https://stackoverflow.com/a/51115745
    //
    // Must return an awaitable object; that is an object with:
    // 1. tp_iter: PyIter_Self (or return_self)
    // 2. tp_iternext: which in turn
    //      - returns without an exception on execution suspension (aka on await)
    //      - returns with StopIteration(value=...) (aka on yield)
    //      - returns with StopAsyncIteration (aka on return) /or maybe that's for the anext?/

    // Create new coroutine
    parser_anext_coro_t* coro = PyObject_New(parser_anext_coro_t, &parser_anext_coro_python_type);
    if (!coro) {
        return NULL;
    }

    // Initialize it
    PyObject* args = PyTuple_Pack(1, self);
    if (!args) {
        Py_DECREF(coro);
        return NULL;
    }

    if (parser_anext_coro_python_type.tp_init((PyObject*)coro, args, NULL)) {
        Py_DECREF(coro);
        Py_DECREF(args);
        return NULL;
    }

    Py_DECREF(args);
    return (PyObject*)coro;
}

// Python type definition for the parser

static PyAsyncMethods parser_python_async_methods = {
    .am_aiter = (unaryfunc)return_self,
    .am_anext = (unaryfunc)parser_anext,
};

static PyTypeObject parser_python_type = {
    PyVarObject_HEAD_INIT(NULL, 0)  //
        .tp_name = "_nparser.parser",
    .tp_basicsize = sizeof(parser_t),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = (newfunc)parser_new,
    .tp_init = (initproc)parser_init,
    .tp_dealloc = (destructor)parser_dealloc,
    .tp_as_async = &parser_python_async_methods,
};

// anext-coro methods

static PyObject* parser_anext_coro_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    fprintf(stderr, "\x1B[36m" "_parser_async_coro.__new__" "\x1B[0m\n");

    (void)args;
    (void)kwds;
    parser_anext_coro_t* o = (parser_anext_coro_t*)type->tp_alloc(type, 0);
    if (o) {
        o->parser = NULL;
    }
    return (PyObject*)o;
}

static int parser_anext_coro_init(parser_anext_coro_t* self, PyObject* args, PyObject* kwds) {
    // Parser arguments
    static char* kw_list[] = {"parser", NULL};
    parser_t* parser = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O", kw_list, &parser)) {
        return -1;
    }

    // Verify the type of parser
    if (!Py_IS_TYPE(parser, &parser_python_type)) {
        PyErr_SetString(PyExc_TypeError, "_nparser.parser expected");
        return -1;
    }

    Py_INCREF(parser);
    self->parser = parser;
    self->awaited_coroutine_iter = NULL;
    return 0;
}

static void parser_anext_coro_dealloc(parser_anext_coro_t* self) {
    Py_XDECREF(self->parser);
    Py_TYPE(self)->tp_free(self);
}

// Coroutine state machine

static PyObject* parser_anext_coro_initial_call(parser_anext_coro_t* self) {
    // See: https://stackoverflow.com/a/51115745
    //
    // The awaitable's __next__ method must:
    // - raise StopAsyncIteration to stop iteration over parser altogether
    // - raise StopIteration(value) to resolve the await with specific value
    // - ??? to await for something

    // Prepare to call parser.read(1)
    // TODO: Statically allocate read_str and one?
    PyObject* read_str = PyUnicode_FromString("read");
    if (!read_str) {
        return NULL;
    }

    PyObject* one = PyLong_FromLong(1);
    if (!one) {
        Py_DECREF(read_str);
        return NULL;
    }

    // Do call parser.read
    PyObject* read_awaitable = PyObject_CallMethodObjArgs(self->parser->reader, read_str, one, NULL);
    Py_DECREF(read_str);
    Py_DECREF(one);
    if (!read_awaitable) {
        return NULL;
    }

    // Ensure the result is awaitable
    PyTypeObject* read_awaitable_type = Py_TYPE(read_awaitable);
    if (!read_awaitable_type) {
        Py_DECREF(read_awaitable);
        return NULL;
    } else if (!read_awaitable_type->tp_as_async || !read_awaitable_type->tp_as_async->am_await) {
        Py_DECREF(read_awaitable);
        Py_DECREF(read_awaitable_type);
        PyErr_Format(PyExc_TypeError, "Expected read() to return an awaitable, got %s", read_awaitable_type->tp_name);
        return NULL;
    }

    // await on the read call
    PyObject* read_await_iter = read_awaitable_type->tp_as_async->am_await(read_awaitable);
    self->awaited_coroutine_iter = read_await_iter;
    return read_await_iter;
}


// Async interface
// See: https://stackoverflow.com/a/51115745
//
// The awaitable's __next__ method must:
// - raise StopAsyncIteration to stop iteration over parser altogether
// - raise StopIteration(value) to resolve the await with specific value
// - ??? to await for something

PySendResult parser_anext_coro_am_send(parser_anext_coro_t* self, PyObject* sent_value, PyObject** result) {
    if (Py_IsNone(sent_value)) {
        *result = parser_anext_coro_initial_call(self);

        return PYGEN_NEXT;
    } else {
        fprintf(stderr, "\x1B[36m" "anext_coro_am_send: received ");
        PyObject_Print(sent_value, stderr, Py_PRINT_RAW);
        fprintf(stderr, "\x1B[0m\n");
        abort();
    }
}

static PyObject* parser_anext_coro_next(parser_anext_coro_t* self) {
    PyObject* result = NULL;
    switch (parser_anext_coro_am_send(self, Py_None, &result)) {
        case PYGEN_RETURN:
            (void)_PyGen_SetStopIterationValue(result);
            Py_DECREF(result);
            return NULL;

        case PYGEN_NEXT:
            fprintf(stderr, "\x1B[36m" "parser_anext_coro_next: next with ");
            PyObject_Print(result, stderr, Py_PRINT_RAW);
            fprintf(stderr, "\x1B[0m\n");
            return result;

        case PYGEN_ERROR:
            return NULL;

        default:
            Py_UNREACHABLE();
    }
}

// Python type definition for the anext coroutine (return type of parser.__anext__())

static PyAsyncMethods parser_anext_coro_python_async_methods = {
    .am_await = (unaryfunc)return_self,
    .am_send = (sendfunc)parser_anext_coro_am_send,
};

static PyTypeObject parser_anext_coro_python_type = {
    PyVarObject_HEAD_INIT(NULL, 1)  //
        .tp_name = "_nparser._parser_anext_coro",
    .tp_basicsize = sizeof(parser_anext_coro_t),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = (newfunc)parser_anext_coro_new,
    .tp_init = (initproc)parser_anext_coro_init,
    .tp_dealloc = (destructor)parser_anext_coro_dealloc,
    .tp_iter = (getiterfunc)return_self,
    .tp_iternext = (iternextfunc)parser_anext_coro_next,
    .tp_as_async = &parser_anext_coro_python_async_methods,
};

// Module definition

static struct PyModuleDef parser_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "_nparser",
    .m_doc = "aiocsv internal parser, written in C",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit__nparser(void) {
    // Check if the parser type is ready
    if (PyType_Ready(&parser_python_type) < 0 || PyType_Ready(&parser_anext_coro_python_type) < 0) {
        return NULL;
    }

    // Create the module object
    PyObject* module = PyModule_Create(&parser_module);
    if (!module) {
        return NULL;
    }

    // Try to add the parser type to the module
    Py_INCREF(&parser_python_type);
    if (PyModule_AddObject(module, "parser", (PyObject*)&parser_python_type) < 0) {
        Py_DECREF(&parser_python_type);
        Py_DECREF(module);
        return NULL;
    }

    // Try to add the async_coro type to the module

    Py_INCREF(&parser_anext_coro_python_type);
    if (PyModule_AddObject(module, "_parser_anext_coro", (PyObject*)&parser_anext_coro_python_type) < 0) {
        Py_DECREF(&parser_python_type);
        Py_DECREF(&parser_anext_coro_python_type);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}
