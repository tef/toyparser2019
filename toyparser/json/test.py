from ..grammar import Grammar, compile_python
from ..old_grammar import compile as old_compile, Parser as InterpreterParser
from .JSON import JSON, builder
from .JSONParser import Parser as JSONParser

def walk(node, indent="- "):
    if (node.value is not None):
        print(indent, node, node.value)
    else:
        print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")


if __name__ == "__main__":
    parser = JSON.parser()
    buf = '[1, 2, 3, "fooo"]'
    node = parser.parse(buf)

    walk(node, "")
    print()

    print(node.build(buf, builder))
    print()

    print(parser.parse("[1, 2, 3]"))
    print()


    import time, json

    inter_parser = InterpreterParser(JSON)
    python_parser = JSON.parser()
    old_python_parser = old_compile(JSON)
    cython_parser = JSONParser()

    n= 80_000
    import random
    l = list(range(n))+list(str(x) for x in range(n))
    random.shuffle(l)
    s = json.dumps(l)
    print()
    print('file is', len(s)/1024, 'k')

    def timeit(name,parser, buf):
        t = time.time()
        o = parser(buf)
        t = time.time() - t
        print(name, t, len(o))
        return t

    json_t = timeit("json", json.loads, s)
    cython_t = timeit("cython compiled", (lambda b: cython_parser.parse(b, builder=builder)), s)
    python_t = timeit("python", (lambda b: python_parser.parse(b, builder=builder)), s)
    print("cython is",cython_t/json_t, "times slower than handrolled C",  python_t/cython_t, "times faster than python")

#    t2 = timeit("python-compiled-old", old_python_parser.parse, s)
#    t3 = timeit("python-interpreted", inter_parser.parse, s)
#    print("cython is",t2/cython_t, "times faster than cheap codegen", t3/cython_t, "times faster than interpreter")


