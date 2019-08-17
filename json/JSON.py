from grammar import Grammar, compile_python
import codecs

def walk(node, indent="- "):
    print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")

def unescape(string):
    return codecs.decode(string, 'unicode_escape')

builder = {
    'number': (lambda buf, start, end, children: int(buf[start:end])),
    'string': (lambda buf, start, end, children: unescape(buf[start:end])),
    'list': (lambda buf, start, end, children: children),
    'object': (lambda buf, start, end, children: dict(children)),
    'pair': (lambda buf, start, end, children: children),
    'document': (lambda buf, start, end, children: children[0]),
    'bool': (lambda buf, start, end, children: bool(buf[start:end])),
    'null': (lambda buf, start, end, children: None),
}

class JSON(Grammar, start="document", whitespace=[" ", "\t", "\r", "\n"]):
    @rule()
    def document(self):
        self.whitespace()
        with self.lookahead():
            self.literal('[', '{')
        with self.capture_node("document"), self.choice():
            with self.case(): self.json_list.inline()
            with self.case(): self.json_object.inline()

    @rule()
    def json_value(self):
        with self.choice():
            with self.case(): self.json_list.inline()
            with self.case(): self.json_object.inline()
            with self.case(): self.json_string.inline()
            with self.case(): self.json_number.inline()
            with self.case(): self.json_true.inline()
            with self.case(): self.json_false.inline()
            with self.case(): self.json_null.inline()
    
    @rule()
    def json_true(self):
        with self.capture_node("bool", nested=False):
            self.literal("true")
    @rule()
    def json_false(self):
        with self.capture_node("bool", nested=False):
            self.literal("false")
    @rule()
    def json_null(self):
        with self.capture_node("bool", nested=False):
            self.literal("null")

    @rule()
    def json_number(self):
        with self.capture_node("number", nested=False):
            with self.optional():
                self.literal("-")
            with self.choice():
                with self.case():
                    self.literal("0")
                with self.case():
                    self.range("1-9")
                    with self.repeat():
                        self.range("0-9")
            with self.optional():
                self.literal(".")
                with self.repeat():
                    self.range("0-9")
            with self.optional():
                self.literal("e", "E")
                with self.optional():
                    self.literal("+", "-")
                    with self.repeat():
                        self.range("0-9")

    @rule()
    def json_string(self):
        self.literal("\"")
        with self.capture_node("string", nested=False), self.repeat(), self.choice():
            with self.case():
                self.literal("\\u")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
            with self.case():
                self.literal("\\")
                self.range(
                    "\"", "\\", "/", "b", 
                    "f", "n", "r", "t",
                )
            with self.case():
                self.range("\\", "\"", invert=True)
        self.literal("\"")

    @rule()
    def json_list(self):
        self.literal("[")
        self.whitespace()
        with self.capture_node("list"), self.repeat(max=1):
            self.json_value()
            with self.repeat(min=0):
                self.whitespace()
                self.literal(",")
                self.whitespace()
                self.json_value()
        self.literal("]")

    @rule()
    def json_object(self):
        self.literal("{")
        self.whitespace()
        with self.capture_node("object"), self.optional():
            with self.capture_node("pair"):
                self.json_string.inline()
                self.whitespace()
                self.literal(":")
                self.whitespace()
                self.json_value()
            self.whitespace()
            with self.repeat(min=0):
                self.literal(",")
                self.whitespace()
                with self.capture_node("pair"):
                    self.json_string()
                    self.whitespace()
                    self.literal(":")
                    self.whitespace()
                    self.json_value()
                self.whitespace()
        self.literal("}")


if __name__ == "__main__":
    import subprocess, sys
    if not sys.argv[1:] or sys.argv[1] != "--skip":
        code = compile_python(JSON, builder, cython=False)
        with open("JSONParser.py", "w") as fh:
            fh.write(code)
        code = compile_python(JSON, builder, cython=True)
        with open("JSONParser.pyx", "w") as fh:
            fh.write(code)

        subprocess.run(["python3", "setup.py", "build_ext", "--inplace"]).check_returncode()

    from JSONParser import Parser as JSONParser
    from old_grammar import compile, Parser
    print()

    print()
    parser = JSON.parser(None)
    buf = '[1, 2, 3, "fooo"]'
    node = parser.parse(buf)

    walk(node, "")
    print()

    print(node.build(buf, builder))
    print()

    print(parser.parse("[1, 2, 3]"))
    print()


    import time, json

    inter_parser = Parser(JSON, builder)
    python_parser = JSON.parser(builder)
    old_python_parser = compile(JSON, builder)
    cython_parser = JSONParser(builder)

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
    cython_t = timeit("cython compiled", cython_parser.parse, s)
    python_t = timeit("python", python_parser.parse, s)
    print("cython is",cython_t/json_t, "times slower than handrolled C",  python_t/cython_t, "times faster than python")

#    t2 = timeit("python-compiled-old", old_python_parser.parse, s)
#    t3 = timeit("python-interpreted", inter_parser.parse, s)
#    print("cython is",t2/cython_t, "times faster than cheap codegen", t3/cython_t, "times faster than interpreter")


