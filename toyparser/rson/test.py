import base64, codecs
from datetime import datetime, timedelta, timezone

from ..grammar import Grammar, compile_python
from ..old_grammar import compile, Parser
from . import rsonlib
from .RSONParser import Parser as RSONParser
from .RSON import RSON, builder

def walk(node, indent="- "):
    print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")

if __name__ == "__main__":
    parser = Parser(RSON)
    cython_parser = RSONParser()
    python_parser = RSON.parser()
    old_python_parser = compile(RSON)

    def p(buf):
        return cython_parser.parse(buf, err=rsonlib.ParserErr, builder=builder)

    rsonlib.run_tests(p, rsonlib.dump)

    import time, json

    s = json.dumps(list(range(50_000))+list(str(x) for x in range(0,50_000)))
    print('file is', len(s)/1024, 'k')

    def timeit(name,parser, buf):
        t = time.time()
        o = parser(buf)
        t = time.time() - t
        print(name, t, len(o))
        return t

    rson_t = timeit("rson", rsonlib.parse, s)
    cython_t = timeit("cython", (lambda b: cython_parser.parse(b, builder=builder)), s)
    python_t = timeit("python-compiled", (lambda b: python_parser.parse(b, builder=builder)), s)
    print("rson is",rson_t/cython_t, "times faster than handrolled python",  python_t/cython_t, "times faster than python")

#    t2 = timeit("python-compiled-old", old_python_parser.parse, s)
#    t3 = timeit("python-interpreted", parser.parse, s)
#    print("cython is",t2/cython_t, "times sloweer  than cheap codegen", t3/cython_t, "times faster than interpreter")




