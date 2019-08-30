from ..grammar import Grammar, compile_python, sibling
import codecs

def unescape(string):
    return codecs.decode(string.replace('\\/', '/'), 'unicode_escape')

builder = {
    'number': (lambda buf, node, children: int(buf[node.start:node.end])),
    'string': (lambda buf, node, children: unescape(buf[node.start:node.end])),
    'list': (lambda buf, node, children: children),
    'object': (lambda buf, node, children: dict(children)),
    'pair': (lambda buf, node, children: children),
    'document': (lambda buf, node, children: children[0]),
    'bool': (lambda buf, node, children: bool(buf[node.start:node.end])),
    'null': (lambda buf, node, children: None),
}

class JSON(Grammar, start="document", whitespace=[" ", "\t", "\r", "\n"]):
    @rule()
    def document(self):
        self.whitespace()
        with self.lookahead():
            self.literal('[', '{')
        with self.choice():
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
    import subprocess
    import os.path


    filename = sibling(__file__, "JSONParser.py")
    code = compile_python(JSON, cython=False)

    with open(filename, "w") as fh:
        fh.write(code)

    filename = sibling(__file__, "JSONParser.pyx")
    code = compile_python(JSON, cython=True)

    with open(filename, "w") as fh:
        fh.write(code)

    subprocess.run(f"python3 `which cythonize` -i {filename}", shell=True).check_returncode()

