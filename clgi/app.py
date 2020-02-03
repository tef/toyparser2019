#!/usr/bin/env python3

import os
import sys
import shlex
import shutil
import tempfile
import subprocess
import contextlib
import traceback
import os.path
import json
import io

from .errors import Bug, Error
from .argparser import ArgumentParser
from .tty import pager
from remarkable import dom

from remarkable.render_ansi import to_ansi, RenderBox

def to_response(response):
    if isinstance(response, dom.Node):
        response = Document(response)
    if not isinstance(response, Response):
        response = Plaintext(response)
    return response

class Response:
    pass

in_complete = 'COMP_LINE' in os.environ and 'COMP_POINT' in os.environ
class Multiple(Response):
    def __init__(self, original, extra):
        self.original = original
        self.extra = extra

    def render(self, width, height):
        mapping1, lines1 = self.original.render(width, height)
        mapping2, lines2 = self.extra.render(width, height)
        return {}, lines1 + [""] + lines2

class Plaintext(Response):
    def __init__(self, lines):
        self.lines = lines
    def render(self, width, height):
        if isinstance(self.lines, str):
            return [], self.lines.splitlines()
        return [], self.lines

class Document(Response):
    def __init__(self, obj, args):
        self.obj = obj
        self.args = args
    def render(self, width, height):
        settings = {'width': width, 'height': height}
        settings.update(self.args)
        if 'width' in self.args:
            indent = max(width-settings['width'],0)//2
            box = RenderBox(indent, settings['width'], settings['height'])
        else:
            box = RenderBox.max_width(0, width, height, 90)
        return to_ansi(self.obj, box, settings)

# Errors

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

class App:
    PREFIX = set((
        'help', 'profile', 'time',
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

    def main(self, name, base_ctx=None):
        if name != '__main__':
            return

        self.name = sys.argv[0]

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
            request = self.parse(argv, environ, base_ctx)
        except Error as e:
            if any(a.startswith('--debug=') or a == '--debug' for a in argv):
                raise
            ctx = dict()
            ctx.update(base_ctx)
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

        response = to_response(response)
        if response:
            pager(response, use_tty=(code == 0 and 'debug' not in request.ctx and request.mode not in ('debug', 'error')))
        sys.exit(code) 

    def parse(self, argv, environ, base_ctx=None):
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
        _ctx = dict()
        _ctx.update(base_ctx)
        _ctx['app'] = self
        _ctx['argv'] = argv
        _ctx['name'] = self.name
        ctx = self.parser.parse(app_args, named_args=True, defaults=False) 
        if 'help' in ctx:
            mode = 'usage'
        if 'debug' in ctx:
            mode = ctx['debug']
        if 'version' in ctx:
            mode = 'version'
        ctx.update(_ctx)
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
            out = to_response(out)
            extra = Plaintext([f"{end-start}"])
            out = Multiple(out, extra)

            return code, out

        elif debug == 'profile' or mode == 'profile':
            import cProfile, pstats

            pr = cProfile.Profile()
            pr.enable()
            out = self.command(request, _code)
            pr.disable()
            s = io.StringIO()
            pstats.Stats(pr, stream=s).strip_dirs().sort_stats(-1).print_stats()
            out = to_response(out)
            extra = Plaintext(s.getvalue())
            out = Multiple(out, extra)

            return code, out

        else:
            out = self.command(request, _code)
            return code, out

class Router:
    def __init__(self):
        self.routes = {}
        self.error_routes = {}

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

    def on_error(self, *paths):
        """ Add a function to handle a path,
            @route("a:b", "a:c")
            def handler(request, code):
                code(0)
                return response
        """
        def _decorator(fn):
            for path in paths:
                self.error_routes[path] = fn
            return fn
        return _decorator

    
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
                _code(-1)
                return out
            else:
                raise Error('unknown command: {} {}'.format(ctx['name'], request.path))


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
            code(0)
            return [doc]
        if mode == 'error':
            code(-1)
            return ["error: {}".format(args['args'])]
        args = self.parser.parse(args)
        request = Request(ctx, mode, path, args)
        code(0)
        return self.fn(ctx, **args)


def command(args=None):
    def _decorator(fn):
        expected_args = set(fn.__code__.co_varnames[:fn.__code__.co_argcount])
        if 'ctx' in expected_args:
            expected_args.remove('ctx')
        return Command(args, fn, expected_args) 
    return _decorator


