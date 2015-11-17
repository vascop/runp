#!/usr/bin/env python
import os
import sys
import argparse
import inspect
import pydoc


def filter_vars(imported_vars):
    functions = {}
    for tup in imported_vars:
        name, obj = tup
        if callable(obj) and not name.startswith('_'):
            if inspect.isclass(obj):
                methods = inspect.getmembers(obj(), predicate=inspect.ismethod)
                for name, method in methods:
                    if not name.startswith('_'):
                        functions[obj.__name__ + "." + name] = method
            else:
                functions[obj.__name__] = obj
    return functions


def load_runfile(runfile):
    importer = __import__
    directory, runfile = os.path.split(runfile)

    added_to_path = False
    index = None

    if directory not in sys.path:
        sys.path.insert(0, directory)
        added_to_path = True
    else:
        i = sys.path.index(directory)
        if i != 0:
            index = i
            sys.path.insert(0, directory)
            del sys.path[i + 1]

    imported = importer(os.path.splitext(runfile)[0])

    if added_to_path:
        del sys.path[0]

    if index is not None:
        sys.path.insert(index + 1, directory)
        del sys.path[0]

    imported_vars = vars(imported).items()
    return imported_vars


def _escape_split(sep, argstr):
    escaped_sep = r'\%s' % sep

    if escaped_sep not in argstr:
        return argstr.split(sep)

    before, _, after = argstr.partition(escaped_sep)
    startlist = before.split(sep)
    unfinished = startlist[-1]
    startlist = startlist[:-1]
    endlist = _escape_split(sep, after)
    unfinished += sep + endlist[0]
    return startlist + [unfinished] + endlist[1:]


def parse_args(cmd):
    args = []
    kwargs = {}
    if ':' in cmd:
        cmd, argstr = cmd.split(':', 1)
        for pair in _escape_split(',', argstr):
            result = _escape_split('=', pair)
            if len(result) > 1:
                k, v = result
                kwargs[k] = v
            else:
                args.append(result[0])
    return cmd, args, kwargs


def get_docstring(function, abbrv=False):
    try:
        doc = inspect.getdoc(function)
        if abbrv:
            doc = doc.splitlines()[0].strip()
    except:
        doc = ""
    return doc


def get_function(functions, function_name):
    try:
        return functions[function_name]
    except KeyError:
        print "No function named '{}' found!".format(function_name)
        return None


def print_functions(functions):
    print "Available functions:"
    for fname, function in functions.iteritems():
        doc = get_docstring(function, abbrv=True)
        print fname + "\t" + doc


def print_function(functions, function):
    func = get_function(functions, function)
    if func:
        print pydoc.plain(pydoc.render_doc(
            func,
            "Displaying docstring for %s")
        )


def run_function(functions, cmd):
    function, args, kwargs = parse_args(cmd)
    try:
        func = get_function(functions, function)
        if func:
            func(*args, **kwargs)
    except TypeError as e:
        print e.message


def main():
    parser = argparse.ArgumentParser(description='Run functions in a file.')
    parser.add_argument('runfile', help='file containing the functions')
    parser.add_argument('function', nargs='?', help='function to run')
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='list available functions in file'
    )
    parser.add_argument(
        '-d', '--detail',
        help='print function docstring'
    )
    args = parser.parse_args()
    runfile = os.path.abspath(args.runfile)

    if not os.path.isfile(runfile):
        print "No such file '{}'".format(args.runfile)
        sys.exit(1)

    imported_vars = load_runfile(runfile)
    functions = filter_vars(imported_vars)

    if args.list:
        print_functions(functions)
        sys.exit(0)

    if args.detail:
        print_function(functions, args.detail)
        sys.exit(0)

    if args.function is None:
        print "No function was selected!"
        sys.exit(1)
    run_function(functions, args.function)
