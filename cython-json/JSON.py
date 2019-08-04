from grammar import Grammar, compile_python
import codecs

def walk(node, indent="- "):
    print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")

def unescape(string):
    return codecs.decode(string, 'unicode_escape')

builder = {
    'number': (lambda buf, start, end, children: float(buf[start:end])),
    'string': (lambda buf, start, end, children: unescape(buf[start:end])),
    'list': (lambda buf, start, end, children: children),
    'object': (lambda buf, start, end, children: dict(children)),
    'pair': (lambda buf, start, end, children: children),
    'document': (lambda buf, start, end, children: children[0]),
    'bool': (lambda buf, start, end, children: bool(buf[start:end])),
    'null': (lambda buf, start, end, children: None),
}

class JSON(Grammar, start="document", whitespace=[" ", "\t", "\r", "\n"]):
    document = rule(whitespace, rule(json_list | json_object, capture="document"))

    @rule()
    def json_value(self):
        with self.choice():
            with self.case(), self.capture("bool"): self.accept("true")
            with self.case(), self.capture("bool"): self.accept("false")
            with self.case(), self.capture("bool"): self.accept("null")
            with self.case(): self.json_number()
            with self.case(): self.json_string()
            with self.case(): self.json_list()
            with self.case(): self.json_object()

    @rule()
    def json_number(self):
        with self.capture("number"):
            with self.optional():
                self.accept("-")
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
    def json_string(self):
        self.accept("\"")
        with self.capture("string"), self.repeat(), self.choice():
            with self.case():
                self.accept("\\u")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
            with self.case():
                self.accept("\\")
                self.range(
                    "\"", "\\", "/", "b", 
                    "f", "n", "r", "t",
                )
            with self.case():
                self.range("\\", "\"", invert=True)
        self.accept("\"")

    @rule()
    def json_list(self):
        self.accept("[")
        self.whitespace()
        with self.capture("list"), self.repeat(max=1):
            self.json_value()
            with self.repeat(min=0):
                self.whitespace()
                self.accept(",")
                self.whitespace()
                self.json_value()
        self.accept("]")

    @rule()
    def json_object(self):
        self.accept("{")
        self.whitespace()
        with self.capture("object"), self.optional():
            with self.capture("pair"):
                self.json_string()
                self.whitespace()
                self.accept(":")
                self.whitespace()
                self.json_value()
            self.whitespace()
            with self.repeat(min=0):
                self.accept(",")
                self.whitespace()
                with self.capture("pair"):
                    self.json_string()
                    self.whitespace()
                    self.accept(":")
                    self.whitespace()
                    self.json_value()
                self.whitespace()
        self.accept("}")


if __name__ == "__main__":
    import subprocess, sys
    if not sys.argv[1:] or sys.argv[1] != "--skip":
        code = compile_python(JSON, builder, cython=True)
        with open("JSONParser.pyx", "w") as fh:
            fh.write(code)

        subprocess.run(["python3", "setup.py", "build_ext", "--inplace"])

    from JSONParser import Parser as JSONParser
    print()

    parser = JSON.parser(builder)
    old_python_parser = JSON.compile_old(builder)
    python_parser = JSON.compile(builder)
    cython_parser = JSONParser(builder)

    import time, json

    n= 50_000
    s = json.dumps(list(range(n))+list(str(x) for x in range(n)))
    print('file is', len(s)/1024, 'k')

    def timeit(name,parser, buf):
        t = time.time()
        o = parser(buf)
        t = time.time() - t
        print(name, t, len(o))
        return t

    json_t = timeit("json", json.loads, s)
    python_t = timeit("python-compiled", python_parser.parse, s)
    cython_t = timeit("cython", cython_parser.parse, s)
    print("cython is",cython_t/json_t, "times slower than handrolled C",  python_t/cython_t, "times faster than python")

#    t2 = timeit("python-compiled-old", old_python_parser.parse, s)
#    t3 = timeit("python-interpreted", parser.parse, s)
#    print("cython is",t2/cython_t, "times faster than cheap codegen", t3/cython_t, "times faster than interpreter")

