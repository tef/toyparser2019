import os
import os.path

from .errors import *

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
                elif name not in fn_args:
                    fn_args[name] = self.parse_argument(kind, value)
                else:
                    raise Error("Unexpected argument: {}".format(value))

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
            if value == '.':
                out.extend(["./", "../"])
            if value == '..':
                out.extend(["../"])
            def format(p, dir=None):
                if dir:
                    p = os.path.join(dir, p) 
                if os.path.isdir(p):
                    return f"{p}/"
                else:
                    return f"{p} "
            def filter(p, path):
                if path: return p.startswith(path)
                return not (p.endswith(("~", ".swp")))
            if value:
                if value.endswith('/'):
                    out.extend(format(p, value) for p in os.listdir(value) if filter(p, None))
                else:
                    dir, path = os.path.split(value)
                    if dir == '':
                        out.extend(format(p) for p in os.listdir() if filter(p, value))
                    else:
                        out.extend(format(p, dir) for p in os.listdir(dir) if filter(p, path))
            else:
                dir = os.getcwd()
                out.extend(format(p) for p in os.listdir() if filter(p, None))
        elif kind in ('bool', 'boolean'):
            vals = ('true ','false ')
            if value:
                out.extend(p for p in vals if p.startswith(value))
            else:
                out.extend(vals)
        return out

