/*
 * This file was auto-generated by speedy-antlr-tool v1.4.1
 *  https://github.com/amykyta3/speedy-antlr-tool
 */

#include "speedy_antlr.h"
#include <any>

using namespace speedy_antlr;

Translator::Translator(PyObject *parser_cls, PyObject *input_stream) {
    this->parser_cls = parser_cls;
    this->input_stream = input_stream;

    // Cache some things for convenience
    PyObject *py_token_module = NULL;
    PyObject *py_tree_module = NULL;
    try {
        py_tree_module = PyImport_ImportModule("antlr4.tree.Tree");
        if(!py_tree_module) throw PythonException();

        TerminalNodeImpl_cls = PyObject_GetAttrString(py_tree_module, "TerminalNodeImpl");
        if(!TerminalNodeImpl_cls) throw PythonException();

        py_token_module = PyImport_ImportModule("antlr4.Token");
        if(!py_token_module) throw PythonException();

        CommonToken_cls = PyObject_GetAttrString(py_token_module, "CommonToken");
        if(!CommonToken_cls) throw PythonException();

        source_tuple = Py_BuildValue("(OO)", Py_None, input_stream);

    } catch(PythonException &e) {
        Py_XDECREF(py_token_module);
        Py_XDECREF(py_tree_module);
        Py_XDECREF(TerminalNodeImpl_cls);
        Py_XDECREF(CommonToken_cls);
        Py_XDECREF(source_tuple);
        throw;
    }
    Py_XDECREF(py_token_module);
    Py_XDECREF(py_tree_module);
}


Translator::~Translator() {
    Py_XDECREF(TerminalNodeImpl_cls);
    Py_XDECREF(CommonToken_cls);
    Py_XDECREF(source_tuple);
}


PyObject* Translator::new_cls(PyObject *cls){
    PyObject* inst = PyObject_CallMethod(
        cls, "__new__", "O", cls
    );
    if(!inst) throw PythonException();
    return inst;
}


PyObject* Translator::convert_common_token(antlr4::Token *token){
    PyObject *tmp;

    PyObject *py_token = new_cls(CommonToken_cls);

    // Assign attributes
    PyObject_SetAttrString(py_token, "source", source_tuple);

    tmp = PyLong_FromSsize_t(token->getType());
    PyObject_SetAttrString(py_token, "type", tmp);
    Py_DECREF(tmp);

    tmp = PyLong_FromSsize_t(0);
    PyObject_SetAttrString(py_token, "channel", tmp);
    Py_DECREF(tmp);

    tmp = PyLong_FromSsize_t(token->getStartIndex());
    PyObject_SetAttrString(py_token, "start", tmp);
    Py_DECREF(tmp);

    tmp = PyLong_FromSsize_t(token->getStopIndex());
    PyObject_SetAttrString(py_token, "stop", tmp);
    Py_DECREF(tmp);

    tmp = PyLong_FromSsize_t(token->getTokenIndex());
    PyObject_SetAttrString(py_token, "tokenIndex", tmp);
    Py_DECREF(tmp);

    tmp = PyLong_FromSsize_t(token->getLine());
    PyObject_SetAttrString(py_token, "line", tmp);
    Py_DECREF(tmp);

    tmp = PyLong_FromSsize_t(token->getCharPositionInLine());
    PyObject_SetAttrString(py_token, "column", tmp);
    Py_DECREF(tmp);

    tmp = PyUnicode_FromString(token->getText().c_str());
    PyObject_SetAttrString(py_token, "_text", tmp);
    Py_DECREF(tmp);

    return py_token;
}


PyObject* Translator::tnode_from_token(PyObject *py_token, PyObject *py_parent_ctx){
    // Wrap token in TerminalNodeImpl
    PyObject *py_tnode = new_cls(TerminalNodeImpl_cls);

    // Assign attributes
    PyObject_SetAttrString(py_tnode, "symbol", py_token);
    PyObject_SetAttrString(py_tnode, "parentCtx", py_parent_ctx);
    return py_tnode;
}

// FIXME: I dont think i'm handling exception cleanup properly!
PyObject* Translator::convert_ctx(
    antlr4::tree::AbstractParseTreeVisitor *visitor,
    antlr4::ParserRuleContext *ctx,
    PyObject *ctx_cls,
    LabelMap labels[], size_t n_labels
){
    // Create py context class
    PyObject *py_ctx = new_cls(ctx_cls);

    PyObject *start = NULL;
    PyObject *stop = NULL;

    // Keep track of which labels were filled already
    std::vector<bool> label_used(n_labels, false);

    // Convert all children
    PyObject *py_children = PyList_New(ctx->children.size());
    for (size_t i=0; i < ctx->children.size(); i++) {
        PyObject *py_child = NULL;
        PyObject *py_label_candidate = NULL;
        void *child_ref = NULL;
        if (antlrcpp::is<antlr4::tree::TerminalNode *>(ctx->children[i])) {
            // Child is a token
            antlr4::tree::TerminalNode *tnode = dynamic_cast<antlr4::tree::TerminalNode *>(ctx->children[i]);

            // Convert the token
            antlr4::Token *token = tnode->getSymbol();
            PyObject *py_token = NULL;
            try {
                py_token = convert_common_token(token);
                py_child = tnode_from_token(py_token, py_ctx);
            } catch(PythonException &e) {
                Py_XDECREF(py_token);
                Py_XDECREF(py_ctx);
                Py_XDECREF(py_children);
                throw;
            }
            child_ref = static_cast<void*>(token);
            py_label_candidate = py_token;
            Py_INCREF(py_label_candidate);

            // Get start/stop
            if(!start || start==Py_None){
                start = py_token;
                Py_INCREF(start);
            }
            if(token->getType() != antlr4::IntStream::EOF) {
                // Always set stop to current token
                stop = py_token;
                Py_INCREF(stop);
            }
            Py_DECREF(py_token);
        } else if (antlrcpp::is<antlr4::ParserRuleContext *>(ctx->children[i])) {
            child_ref = static_cast<void*>(ctx->children[i]);
            try {
                py_child = std::any_cast<PyObject *>(visitor->visit(ctx->children[i]));
            } catch(PythonException &e) {
                Py_XDECREF(py_ctx);
                Py_XDECREF(py_children);
                throw;
            }
            PyObject_SetAttrString(py_child, "parentCtx", py_ctx);
            py_label_candidate = py_child;
            Py_INCREF(py_label_candidate);

            // Get start/stop
            if(!start || start==Py_None) {
                start = PyObject_GetAttrString(py_child, "start");
            }
            PyObject *tmp_stop = PyObject_GetAttrString(py_child, "stop");
            if (tmp_stop && tmp_stop!=Py_None) stop = tmp_stop;
        } else {
            PyErr_SetString(PyExc_RuntimeError, "Unknown child type");
            throw PythonException();
        }

        // Check if child matches one of the labels
        for(size_t j=0; j<n_labels; j++) {
            if(child_ref == labels[j].ref){
                PyObject_SetAttrString(py_ctx, labels[j].name, py_label_candidate);
                label_used[j] = true;
            }
        }
        Py_DECREF(py_label_candidate);

        // Steals reference to py_child
        PyList_SetItem(py_children, i, py_child);

    }

    // Assign any remaining labels to None
    for(size_t j=0; j<n_labels; j++) {
        if(!label_used[j]) {
            PyObject_SetAttrString(py_ctx, labels[j].name, Py_None);
        }
    }

    // Assign remaining ctx class attributes
    PyObject_SetAttrString(py_ctx, "parser", Py_None); // (Set to None since this is not translated)
    PyObject_SetAttrString(py_ctx, "exception", Py_None);
    if(!ctx->parent){
        // This is the topmost context. No parent to set this, so set to None
        PyObject_SetAttrString(py_ctx, "parentCtx", Py_None);
    }

    PyObject *tmp = PyLong_FromSsize_t(ctx->invokingState);
    PyObject_SetAttrString(py_ctx, "invokingState", tmp);
    Py_DECREF(tmp);

    if(start) {
        PyObject_SetAttrString(py_ctx, "start", start);
        Py_DECREF(start);
    } else {
        PyObject_SetAttrString(py_ctx, "start", Py_None);
    }

    if(stop) {
        PyObject_SetAttrString(py_ctx, "stop", stop);
        Py_DECREF(stop);
    } else {
        PyObject_SetAttrString(py_ctx, "stop", Py_None);
    }

    // Assign child list to context
    PyObject_SetAttrString(py_ctx, "children", py_children);
    Py_DECREF(py_children);

    return py_ctx;
}





ErrorTranslatorListener::ErrorTranslatorListener(Translator *translator, PyObject *sa_err_listener) {
    this->translator = translator;
    this->sa_err_listener = sa_err_listener;
}

void ErrorTranslatorListener::syntaxError(
    antlr4::Recognizer *recognizer, antlr4::Token *offendingSymbol, size_t line,
    size_t charPositionInLine, const std::string &msg, std::exception_ptr e
) {
    // Get input stream from recognizer
    antlr4::IntStream *input_stream;
    if (antlrcpp::is<antlr4::Lexer *>(recognizer)) {
        antlr4::Lexer *lexer = dynamic_cast<antlr4::Lexer *>(recognizer);
        input_stream = lexer->getInputStream();
    } else if (antlrcpp::is<antlr4::Parser *>(recognizer)) {
        antlr4::Parser *parser = dynamic_cast<antlr4::Parser *>(recognizer);
        input_stream = parser->getInputStream();
    } else {
        PyErr_SetString(PyExc_RuntimeError, "Unknown recognizer type");
        throw PythonException();
    }

    size_t char_index = input_stream->index();

    PyObject *py_token;
    if(offendingSymbol){
        py_token = translator->convert_common_token(offendingSymbol);
    } else {
        py_token = Py_None;
        Py_INCREF(py_token);
    }

    PyObject *ret = PyObject_CallMethod(
        sa_err_listener, "syntaxError",
        "OOnnns",
        translator->input_stream, // input_stream
        py_token, // offendingSymbol
        char_index, // char_index
        line, // line
        charPositionInLine, // column
        msg.c_str()// msg
    );
    Py_DECREF(py_token);
    if(!ret) throw PythonException();
    Py_DECREF(ret);
}