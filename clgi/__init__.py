#!/usr/bin/env python3

import os
import sys
import shutil
import hashlib
import sqlite3
import traceback
import subprocess
import unicodedata
import contextlib
import functools
import tempfile
import os.path
import shlex
import json
import io

from datetime import datetime, timezone
from uuid import uuid4


# Errors

class Bug(SyntaxError): pass # Bad Code
class Error(Exception): pass # Bad Input

# Wrappers for shell programs: less, $EDITOR, and git

@contextlib.contextmanager
def PAGER(use_less=True):
    if use_less and sys.stdout.isatty() and sys.stderr.isatty():
        env = {}
        env.update(os.environ)
        env["LESS"] = "FRX"
        env["LV"] = "-c"
        p = subprocess.Popen(
            'less',
            env=env, 
            stdin=subprocess.PIPE,
            encoding='utf8'
        )
        width, height = shutil.get_terminal_size((None, None))
        try:
            yield p.stdin, width
        finally:
            p.stdin.close()
            while p.poll() is None:
                try:
                    p.wait()
                except KeyboardInterrupt:
                    pass
    else:
        yield sys.stdout, None

def EDITOR(buffer):
    editor = os.environ.get('EDITOR')
    if not editor:
        editor = os.environ.get('VISUAL')
    if not editor:
        raise Error('No EDITOR environment variable set')

    fd, file = tempfile.mkstemp()
    with os.fdopen(fd, 'r+') as fh:
        fh.write(buffer)

    p = subprocess.Popen([editor, file])
    if p.wait() == 0:
        with open(file) as fh:
            return fh.read()
    return None

def RENDER(line, width):
    if width is None:
        return line
    # if template type, do special behavior

    return line

# Request/App/Parser/Command libraries for CLI

class Request:
    def __init__(self, ctx, mode, path, args):
        self.ctx = ctx
        self.mode = mode
        self.path = path
        self.args = args

class Redirect(Exception):
    def __init__(self, request):
        self.request = request
        Exception.__init__(self)

class Routes:
    def __init__(self):
        self.routes = {}

    def on(self, *paths):
        """ Add a function to handle a path,
            @route("a:b", "a:c")
            def handler(request, code):
                code(0)
                return response
        """
        def _decorator(fn):
            for path in paths:
                self.routes[path] = fn
            return fn
        return _decorator

class App:
    PREFIX = set((
        'help',
    ))
    MODES = set((
        'call', 'help', 'error', 'usage', 'complete', 'version', 'debug', 'time', 'profile',
    ))
    def __init__(self, *, name, version, args, command):
        self.name = name
        self.version = version
        self.command = command
        args = dict(args)
        args['help'] = '--bool*'
        args['version'] = '--bool?'
        args['debug'] = '--str?'

        self.parser = ArgumentParser(args)
        if self.parser.positional:
            raise Bug('No Positional arguments for app option parser')

    def main(self, name):
        if name != '__main__':
            return

        argv, environ = sys.argv[1:], os.environ
        if 'COMP_LINE' in environ and 'COMP_POINT' in environ:
            # Bash Line Completion.
            line, offset =  environ['COMP_LINE'], int(environ['COMP_POINT'])
            try:
                prefix = shlex.split(line[:offset])
                # if there's mismatched ''s bail
            except ValueError:
                sys.exit(0)

            # Best effort parsing
            prefix = line[:offset].split(' ')
            for o in self.complete(prefix):
                print(o)
            sys.exit(0)

        try:
            request = None
            request = self.parse(argv, environ)
        except Error as e:
            if any(a.startswith('--debug=') or a == '--debug' for a in argv):
                raise
            ctx = dict()
            ctx['app'] = self
            ctx['argv'] = argv
            ctx['name'] = self.name
            request = Request(ctx, 'error', e.__class__, {'args':e.args[0], 'request': None })
        while True:
            try:
                code, response = self.run(request)
                break
            except Error as e:
                ctx = request.ctx if request else {}
                if 'debug' in ctx:
                    raise
                else:
                    request = Request(ctx, "error", e.__class__, {'args':e.args[0], 'request': request})
            except Redirect as r:
                ctx = request[0] if request else {}
                if 'debug' in ctx:
                    code, response = -1, r.redirect
                else:
                    request = r.redirect
            # except Exception as e:
            #    code, response = -1, ["".join(traceback.format_exception(*sys.exc_info()))]
            #    break

        if response:
            with PAGER() as (stdout, width):
                for line in response:
                    if line is not None:
                        line = RENDER(line, width)
                        print(line, file=stdout)
        sys.exit(code) 

    def parse(self, argv, environ):
        """ turn 
            a b c --d=e -- --raw
            into list of name, value pairs
            None, a 
            None, b
            None, c
            d, e
            None --raw
        """
        mode = "call"
        if argv and argv[0] in self.PREFIX:
            mode = argv.pop(0)

        path = ""
        app_args = []
        args = []
        
        #if argv and not argv[0].startswith('--'):
        #    path = argv.pop(0)

        flags = True
        for arg in argv:
            name, value = None, None
            if flags and arg == '--':
                flags = False
                continue
            if flags and arg.startswith('--'):
                if '=' in arg:
                    name, value = arg[2:].split('=', 1)
                else:
                    name, value = arg[2:], None
            else:
                name, value = None, arg
            if name in self.parser.argspec:
                app_args.append((name, value))
            else:
                args.append((name, value))
        base_ctx = dict()
        base_ctx['app'] = self
        base_ctx['argv'] = argv
        base_ctx['name'] = self.name
        ctx = self.parser.parse(app_args, named_args=True, defaults=False) 
        if 'help' in ctx:
            mode = 'usage'
        if 'debug' in ctx:
            mode = ctx['debug']
        if 'version' in ctx:
            mode = 'version'
        ctx.update(base_ctx)
        return Request(ctx, mode, "", args)

    def complete(self, prefix):
        out = []
        if len(prefix) < 2:
            return out

        if prefix[1]:
            if prefix[1] in self.PREFIX:
                prefix.pop(1)
            elif len(prefix) == 2:
                for m in self.PREFIX:
                    if m.startswith(prefix[1]):
                        out.append('{} '.format(m))
        if len(prefix) > 1:
            base_ctx = dict()
            base_ctx['app'] = self
            base_ctx['name'] = self.name
            request = Request(base_ctx, "complete", "", prefix[1:])
            out.extend(self.command(request, lambda code: 0))
        out.sort()
        return out

    def run(self, request):
        ctx, mode, path, args = request.ctx, request.mode, request.path, request.args

        if request.ctx.get('version') or mode == 'version':
            return 0, [str(self.version)]

        code = 0
        def _code(c):
            nonlocal code
            code = c

        debug = request.ctx.get('debug')
        if debug == 'time' or mode == 'time':
            import time

            start = time.monotonic()
            out = self.command(request, _code)
            end = time.monotonic()
            out.extend(("", str(end-start)))

            return code, out

        elif debug == 'profile' or mode == 'profile':
            import cProfile, pstats

            pr = cProfile.Profile()
            pr.enable()
            out = self.command(request, _code)
            pr.disable()
            s = io.StringIO()
            pstats.Stats(pr, stream=s).strip_dirs().sort_stats(-1).print_stats()
            out.extend(("", s.getvalue()))

            return code, out

        else:
            out = self.command(request, _code)
            return code, out

class Router:
    def __init__(self, routes, errors):
        self.routes = routes.routes
        self.error_routes = errors.routes
    
    def __call__(self, request, _code):
        ctx, mode, path, args = request.ctx, request.mode, request.path, request.args
        if mode == "complete":
            return self.complete(args, ctx)

        if request.path == "" and request.args and request.args[0][0] is None:
            route = request.args.pop(0)
            request.path = request.path + route[1]

        if request.mode == 'error':
            fn = self.error_routes.get(request.path)
            if fn:
                return fn(request, _code)
            else:
                _code(-1)
                return ["error: {}".format(args['args'])]

        if request.path not in self.routes:
            if request.path == '':
                out = []
                for r in self.routes:
                    out.append("{} {}".format(ctx['name'], r))
                _code(0)
                return out
            else:
                raise Error('unknown command: {} {}'.format(app.name, path))


        return self.routes[request.path](request, _code)


    def complete(self, prefix, ctx):
        out = []

        if len(prefix) == 1:
            p = prefix[0]
            mask = 0 
            if not p:
                out.append('help ')
            # if word to complete is 'foo:b' and
            # matches 'foo:bar', we must print 'bar '
            # because bash

            if ':' in p:
                mask = len(p.rsplit(':', 1)[0])+1

            for r in self.routes:
                if isinstance(r, str) and r.startswith(p):
                    out.append("{} ".format(r[mask:]))

        elif len(prefix) > 1:
            path = prefix[0]
            if path in self.routes:
                request = Request(ctx, "complete", "", prefix[1:])
                out.extend(self.routes[path](request, None))
        return out


class Command:
    def __init__(self, args, fn, expected_args=None):
        if args is None: args = {}
        self.parser = ArgumentParser(args)
        self.fn = fn
        if expected_args and expected_args != self.parser.argspec.keys():
            raise Bug("missing args in command: {}".format(expected_args-self.parser.argspec.keys()))

    def __call__(self, request, code):
        ctx, mode, path, args = request.ctx, request.mode, request.path, request.args
        if mode == "complete":
            return self.parser.complete(args, None)
        if mode == "help" or mode == "usage":
            doc = self.fn.__doc__ or ""
            return 0, [doc]
        args = self.parser.parse(args)
        request = Request(ctx, mode, path, args)
        code(0)
        return self.fn(ctx, **args)


class ArgumentParser:
    """
        p = ArgumentParser({ first="--str?", second="--str*", third="str+", })

        running:
            p.parse("--first=a --second=b --second=b 1 2 3 4")

        gives
            {
                "first": "a", 
                "second": ["b", "c"],
                "third": ["1", "2", "3", "4"]
            }

        arguments can be named, '--kind', or positional 'kind'
        only one argument can be positional

        kinds are:

            string, str
            int, integer
            float, num, number
            path, file, dir

        kinds can be annotated:

                --kind   exactly 1 of named arg
                           no default
                --kind?  0 or 1 of named arg
                           default None
                --kind*  0 or more of named arg
                           default ()
                --kind+  1 or more of named arg
                           no default

                kind       1 of, positional
                           no default
                kind?     0 or 1 of, positional
                           default None
                kind*  0 or more of tail
                           default ()
                kind+    1 or more of tail
                           no default
    """
        
    KINDS = set((
        'str', 'string', 'scalar',
        'bool', 'boolean', 
        'int', 'integer',
        'num', 'number', 'float',
        'path', 'file', 'dir',
    ))

    def __init__(self, expected):
        """
            expected is a dict of name:kind
            kind is str, int, bool, etc
        """
        argspec = {}
        positional = None
        flags = False
        for name, value in expected.items():
            if positional:
                raise Bug("Commands can only take one type of positional arg")
            elif value.startswith("--"):
                flags = True
                if value.endswith("?"):
                    argspec[name] = ("named?", value[2:-1])  
                elif value.endswith("*"):
                    argspec[name] = ("named*", value[2:-1])  
                elif value.endswith("+"):
                    argspec[name] = ("named+", value[2:-1])  
                else:
                    argspec[name] = ("named", value[2:])  
            elif value.endswith('?'):
                positional = name
                argspec[name] = ("positional?", value[:-1])  
            elif value.endswith('*'):
                positional = name
                argspec[name] = ("positional*", value[:-1])  
            elif value.endswith('+'):
                positional = name
                argspec[name] = ("positional+", value[:-1])  
            else:
                positional = name
                argspec[name] = ("positional", value) 
        for key, value in argspec.items():
            rule, kind = value
            if kind not in self.KINDS:
                raise Bug('bad kind: {!r}'.format(kind))
            elif kind == "bool" and rule.startswith('positional'):
                raise Bug('why a positional bool? no')
        self.argspec = argspec
        self.positional = positional
        self.flags = flags

    def parse(self, args, named_args=False, defaults=True):
        """ args is a list of (name, value) pairs """
        argspec, flags, positional = self.argspec, self.flags, self.positional
        fn_args = {}
        for name, value in args:
            if name is None:
                if named_args:
                    raise Error("Can't mix positional argument and also pass it as a named argument")
                name = positional
                if name is None:
                    raise Error("Unexpected argument: {}".format(value))
                rule, kind = argspec[name]
                if rule in ('positional+', 'positional*'):
                    if name not in fn_args: fn_args[name] = []
                    fn_args[name].append(self.parse_argument(kind, value))
                else:
                    fn_args[name] = self.parse_argument(kind, value)
            elif name not in argspec:
                raise Error('unknown arg: --{}'.format(name))
            else:
                rule, kind = argspec[name]
                if kind == 'bool' and value is None:
                    value = True
                else:
                    value = self.parse_argument(kind, value)
                if rule in ('named+', 'named*', 'positional*', 'positional+'):
                    if name not in fn_args: fn_args[name] = []
                    fn_args[name].append(value)
                elif name in fn_args:
                    raise Error('duplicate argument --{}'.format(name))
                else:
                    fn_args[name] = value
                if rule.startswith("positional"):
                    named_args = True
        missing = []
        for name, value in argspec.items():
            rule, kind = value
            if name in fn_args:
                continue
            if rule in ('named?', 'positional?'):
                if defaults: fn_args[name] = None
            elif rule in ('named*', 'positional*'):
                if defaults: fn_args[name] = ()
            else:
                missing.append((name, rule, kind))

        if missing:
            out = []
            for name, rule, kind in missing:
                if rule.startswith('named'):
                    out.append('--{}=<{}>'.format(name, kind))
                elif rule.startswith('positional'):
                    out.append('<{}>'.format(kind))
            raise Error("missing arguments: {}".format(" ".join(out)))
        return fn_args

    def parse_argument(self, kind, value):
        if kind in (None, "str", "string"):
            return value
        elif kind in ("path", "file", "dir"):
            return os.path.normpath(os.path.join(os.getcwd(), value))
        elif kind in ("int","integer"):
            try:
                return int(value)
            except ValueError:
                raise Error('got {} expecting integer'.format(value))
        elif kind in ("float","num", "number"):
            try:
                return float(value)
            except ValueError:
                raise Error('got {} expecting float'.format(value))
        elif kind in ("bool", "boolean"):
            try:
                return {'true':True, 'false':False, None: True}[value]
            except KeyError:
                raise Error('expecting true/false, got {}'.format(value))
        elif kind == "scalar":
            try: return int(value)
            except: pass
            try: return float(arg)
            except: pass
            return value
        return value

    def complete_named(self, args):
        arg = args[-1]

        if arg.startswith('--') and '=' in arg:
            name, value = arg[2:].split('=',1)
            if name in self.argspec:
                rule, kind = self.argspec[name]
                return self.complete_kind(kind, value)
            else:
                return ()
        out = []
        if arg.startswith('--') and '--' not in args[:-1]:
            argname = arg[2:]
            for name, value in self.argspec.items():
                rule, kind = value
                if name.startswith(argname):
                    if not argname and name in ('version','debug', 'help',):
                        continue # HACK
                    if rule.startswith('named') and kind == 'bool':
                        out.append('--{} '.format(name))
                    else:
                        out.append('--{}='.format(name))


        return out

    def complete(self, args, app_parser):
        arg = args[-1]

        if arg.startswith('--') and '=' in arg:
            name, value = arg[2:].split('=',1)
            if name in self.argspec:
                rule, kind = self.argspec[name]
                return self.complete_kind(kind, value)
            elif app_parser:
                return app_parser.complete_named(args)
            else:
                return ()

        out = []
        if app_parser:
            out.extend(app_parser.complete_named(args))
        if (not arg or arg.startswith('-')) and '--' not in args[:-1]:
            if not arg:
                out.append('')
            if arg in ('', '-', '--'):
                out.append('-- ')
            argname = arg[2:]
            for name, value in self.argspec.items():
                rule, kind = value
                if name.startswith(argname):
                    if rule.startswith('named') and kind == 'bool':
                        out.append('--{} '.format(name))
                    else:
                        out.append('--{}='.format(name))

        if (not arg) or (not arg.startswith('-') or '--' in args[:-1]):
            if self.positional:
                rule, kind = self.argspec[self.positional]
                out.extend(self.complete_kind(kind, arg))

        return out

    def complete_kind(self, kind, value):
        out = []
        if kind in ('path', 'dir', 'file'):
            if value:
                out.extend("{} ".format(p) for p in os.listdir() if p.startswith(value))
            else:
                out.extend("{} ".format(p) for p in os.listdir() if not p.startswith('.'))
        elif kind in ('bool', 'boolean'):
            vals = ('true ','false ')
            if value:
                out.extend(p for p in vals if p.startswith(value))
            else:
                out.extend(vals)
        return out

def command(args=None):
    def _decorator(fn):
        expected_args = set(fn.__code__.co_varnames[:fn.__code__.co_argcount])
        if 'ctx' in expected_args:
            expected_args.remove('ctx')
        return Command(args, fn, expected_args) 
    return _decorator


