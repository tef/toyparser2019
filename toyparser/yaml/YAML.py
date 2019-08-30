from ..grammar import Grammar, compile_python, sibling

import codecs

def unescape(string):
    return codecs.decode(string, 'unicode_escape')

builder = {
    'number': (lambda buf, node, children: int(buf[node.start:node.end])),
    'string': (lambda buf, node, children: unescape(buf[node.start:node.end])),
    'list': (lambda buf, node, children: children),
    'object': (lambda buf, node, children: dict(children)),
    'pair': (lambda buf, node, children: children),
    'document': (lambda buf, node, children: children[0]),
    'identifier': (lambda buf, node, children: str(buf[node.start:node.end])),
    'bool': (lambda buf, node, children: bool(buf)),
    'null': (lambda buf, node, children: None),
}

class YAML(Grammar, start="document", whitespace=[" ", "\t"], newline=["\n", "\r", "\r\n"]):
    yaml_literal = rule( 
        list_literal | object_literal |
        string_literal | number_literal |
        true_literal | false_literal | 
        null_literal
    )

    true_literal = rule(literal("true"), capture="bool")
    false_literal = rule(literal("false"), capture="bool")
    null_literal = rule(literal("null"), capture="null")

    @rule()
    def identifier(self):
        with self.choice():
            with self.case(), self.capture_node('identifier'), self.repeat(min=1):
                self.range("a-z","A-Z","_")
            with self.case():
                self.string_literal()

    @rule()
    def number_literal(self):
        with self.capture_node("number"):
            with self.optional():
                self.range("-", "+")
            with self.repeat(min=1):
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
    def string_literal(self):
        self.literal("\"")
        with self.capture_node("string"), self.repeat(), self.choice():
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
    def list_literal(self):
        self.literal("[")
        self.whitespace(newline=True)
        with self.capture_node("list"), self.repeat(max=1):
            self.yaml_literal()
            with self.repeat(min=0):
                self.whitespace(newline=True)
                self.literal(",")
                self.whitespace(newline=True)
                self.yaml_literal()
            self.whitespace(newline=True)
            with self.optional():
                self.literal(",")
                self.whitespace(newline=True)
        self.literal("]")

    @rule()
    def object_literal(self):
        self.literal("{")
        self.whitespace(newline=True)
        with self.capture_node("object"), self.optional():
            self.string_literal()
            self.whitespace() # must be on same line as :
            self.literal(":")
            self.whitespace(newline=True)
            self.yaml_literal()
            with self.repeat(min=0):
                self.whitespace(newline=True)
                self.literal(",")
                self.whitespace(newline=True)
                self.string_literal()
                self.whitespace() # must be on same line as #
                self.literal(":")
                self.whitespace(newline=True)
                self.yaml_literal()
            self.whitespace(newline=True)
            with self.optional():
                self.literal(",")
                self.whitespace(newline=True)
        self.literal("}")

    @rule()
    def yaml_eol(self):
        with self.repeat(), self.choice():
            with self.case():
                self.whitespace()
                self.newline()
            with self.case():
                self.whitespace()
                self.literal('#')
                with self.repeat():
                    self.range("\n", invert=True)
                self.newline()

    
    @rule()
    def indented_list(self):
        with self.indented(), self.capture_node('list'):
            self.literal("-")
            with self.choice():
                with self.case():
                    self.whitespace()
                    self.indented_value()
                with self.case():
                    self.yaml_eol()
                    self.indent()
                    self.whitespace(min=1)
                    self.indented_value()

            with self.repeat():
                self.yaml_eol()
                self.indent()
                self.literal("-")
                self.whitespace(min=1)
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.indented_value()
                    with self.case():
                        self.yaml_eol()
                        self.indent()
                        self.whitespace()
                        self.indented_value()

    @rule()
    def indented_object(self):
        with self.indented(), self.capture_node('object'):
            with self.capture_node("pair"):
                self.identifier()
                self.whitespace()
                self.literal(":")
                with self.choice():
                    with self.case():
                        self.yaml_eol()
                        self.indent()
                        self.whitespace(min=1)
                        self.indented_value()
                    with self.case():
                        self.whitespace()
                        self.indented_value()

            with self.repeat(), self.capture_node("pair"):
                self.yaml_eol()
                self.indent()
                self.identifier()
                self.whitespace()
                self.literal(":")
                self.capture_value("a")
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.indented_value()
                    with self.case():
                        self.yaml_eol()
                        self.indent()
                        self.whitespace(min=1)
                        self.indented_value()

    @rule()
    def indented_value(self):
        with self.choice():
            with self.case():
                self.indented_object()
            with self.case():
                self.indented_list()
            with self.case():
                self.yaml_literal()

    @rule()
    def document(self):
        with self.repeat():
            self.whitespace()
            self.yaml_eol()
        with self.choice():
            with self.case():
                self.indented_object()
            with self.case():
                self.indented_list()
            with self.case():
                self.list_literal()
            with self.case():
                self.object_literal()
        self.whitespace()
        with self.repeat():
            self.yaml_eol()
            self.whitespace()
        with self.repeat():
            self.end_of_line()
            self.whitespace()


if __name__ == "__main__":
    import subprocess
    import os.path


    filename = sibling(__file__, "YAMLParser.py")
    code = compile_python(YAML, cython=False)

    with open(filename, "w") as fh:
        fh.write(code)

    filename = sibling(__file__, "YAMLParser.pyx")
    code = compile_python(YAML, cython=True)

    with open(filename, "w") as fh:
        fh.write(code)

    subprocess.run(f"python3 `which cythonize` -i {filename}", shell=True).check_returncode()
