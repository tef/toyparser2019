import base64, codecs
from datetime import datetime, timedelta, timezone

from ..grammar import Grammar, compile_python
from .RemarkableParser import Parser as RemarkableParser
from .Remarkable import Remarkable, builder

def walk(node, indent="- "):
    print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")

if __name__ == "__main__":
    cython_parser = RemarkableParser()
    python_parser = Remarkable.parser()

    import time

    def timeit(name, parser, buf):
        t = time.time()
        o = parser(buf)
        t = time.time() - t
        print(name, t)
        return o, t

    tests = [
        "\n".join([
            "@Tag [1,2,3]",
            ""
        ]),
        "\n".join([
            "# header",
            "para1",
            "",
            "para2",
        ]),
    ]

    for testcase in tests:
        for line in testcase.splitlines():
            print("> ", line)

        o1, python_t = timeit("python-compiled", (lambda b: python_parser.parse(b)), testcase)
        #o2, cython_t = timeit("cython", (lambda b: cython_parser.parse(b)), testcase)

        # if not o1 or not o2 or o1.end != o2.end: raise Exception(o1,o2)

        walk(o1)
        print()




