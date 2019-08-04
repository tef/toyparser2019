from grammar import Grammar, compile_python

import codecs

def walk(node, indent="- "):
    print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")

def unescape(string):
    return codecs.decode(string, 'unicode_escape')

builder = {
    'number': (lambda buf, start, end, children: eval(buf[start:end])),
    'string': (lambda buf, start, end, children: unescape(buf[start:end])),
    'list': (lambda buf, start, end, children: children),
    'object': (lambda buf, start, end, children: dict(children)),
    'pair': (lambda buf, start, end, children: children),
    'document': (lambda buf, start, end, children: children[0]),
    'bool': (lambda buf, start, end, children: bool(buf[start:end])),
    'null': (lambda buf, start, end, children: None),
}

class RSON(Grammar, start="document", whitespace=[" ", "\t", "\r", "\n", "\uFEFF"]):
    @rule()
    def document(self):
        self.comment()
        with self.capture('document'):
            self.rson_value()
        self.comment()

    @rule()
    def comment(self):
        self.whitespace()
        with self.repeat(min=0):
            self.accept("#")
            with self.repeat(min=0):
                self.range("\n", invert=True)
            self.whitespace()
        self.whitespace()

    rson_value = rule( 
        rson_list | rson_object |
        rson_string | rson_number |
        rson_true | rson_false | 
        rson_null
    )
    
    rson_true = rule(accept("true"), capture="bool")
    rson_false = rule(accept("false"), capture="bool")
    rson_null = rule(accept("null"), capture="null")


    @rule()
    def rson_number(self):
        with self.capture("number"), self.choice():
            with self.case():
                with self.optional():
                    self.range("-", "+")
                self.accept("0x")
                self.range("0-9", "A-F", "a-f")
                with self.repeat():
                    self.range("0-9","A-F","a-f","_")
            with self.case():
                with self.optional():
                    self.range("-", "+")
                self.accept("0o")
                self.range("0-8",)
                with self.repeat():
                    self.range("0-8","_")
            with self.case():
                with self.optional():
                    self.range("-", "+")
                self.accept("0b")
                self.range("0-1",)
                with self.repeat():
                    self.range("0-1","_")
            with self.case():
                with self.optional():
                    self.range("-", "+")
                with self.choice():
                    with self.case():
                        self.accept("0")
                    with self.case():
                        self.range("1-9")
                        with self.repeat():
                            self.range("0-9")
                with self.optional():
                    self.accept(".")
                    with self.repeat():
                        self.range("0-9")
                with self.optional():
                    self.accept("e", "E")
                    with self.optional():
                        self.accept("+", "-")
                        with self.repeat():
                            self.range("0-9")

    @rule()
    def rson_string(self):
        self.accept("\"")
        with self.capture("string"), self.repeat(), self.choice():
            with self.case():
                self.accept("\\x")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
            with self.case():
                self.accept("\\u")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
            with self.case():
                self.accept("\\U")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
            with self.case():
                self.accept("\\")
                self.range(
                    "\"", "\\", "/", "b", 
                    "f", "n", "r", "t", "'", "\n",
                )
            with self.case():
                self.range("\\", "\"", invert=True)
        self.accept("\"")

    @rule()
    def rson_list(self):
        self.accept("[")
        self.comment()
        with self.capture("list"), self.repeat(max=1):
            self.rson_value()
            with self.repeat(min=0):
                self.comment()
                self.accept(",")
                self.comment()
                self.rson_value()
        self.accept("]")

    @rule()
    def rson_object(self):
        self.accept("{")
        self.comment()
        with self.capture("object"), self.optional():
            with self.capture("pair"):
                self.rson_string()
                self.comment()
                self.accept(":")
                self.comment()
                self.rson_value()
            self.comment()
            with self.repeat(min=0):
                self.accept(",")
                self.comment()
                with self.capture("pair"):
                    self.rson_string()
                    self.comment()
                    self.accept(":")
                    self.comment()
                    self.rson_value()
                self.comment()
        self.accept("}")

if __name__ == "__main__":
    import subprocess, sys
    if not sys.argv[1:] or sys.argv[1] != "--skip":
        code = compile_python(RSON, builder, cython=True)
        with open("RSONParser.pyx", "w") as fh:
            fh.write(code)

        subprocess.run(["python3", "setup.py", "build_ext", "--inplace"])

    import rsonlib
    from RSONParser import Parser as RSONParser
    print()

    parser = RSON.parser(builder)
    old_python_parser = RSON.compile_old(builder)
    python_parser = RSON.compile(builder)
    cython_parser = RSONParser(builder)

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
    cython_t = timeit("cython", cython_parser.parse, s)
    python_t = timeit("python-compiled", python_parser.parse, s)
    print("rson is",rson_t/cython_t, "times faster than handrolled python",  python_t/cython_t, "times faster than python")

#    t2 = timeit("python-compiled-old", old_python_parser.parse, s)
#    t3 = timeit("python-interpreted", parser.parse, s)
#    print("cython is",t2/cython_t, "times sloweer  than cheap codegen", t3/cython_t, "times faster than interpreter")

    rsonlib.run_tests(cython_parser.parse, rsonlib.dump)



