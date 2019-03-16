from textexpressions import Grammar

import codecs

def walk(node, indent="- "):
    print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")

def unescape(string):
    return codecs.decode(buf, 'unicode_escape')

builder = {
    'number': (lambda buf, children: int(buf)),
    'string': (lambda buf, children: unescape(buf)),
    'list': (lambda buf, children: children),
    'object': (lambda buf, children: dict(children)),
    'document': (lambda buf, children: children[0]),
}

class JSON(Grammar, start="document", whitespace=[" ", "\t", "\r", "\n"]):
    document = rule(whitespace, rule(json_list | json_object, capture="document"))

    json_value = rule( 
        json_list | json_object |
        json_string | json_number |
        json_true | json_false | 
        json_null
    )
    
    json_true = rule(accept("true"), capture="bool")
    json_false = rule(accept("false"), capture="bool")
    json_null = rule(accept("null"), capture="null")

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
            self.json_string()
            self.whitespace()
            self.accept(":")
            self.whitespace()
            self.json_value()
            self.whitespace()
            with self.repeat(min=0):
                self.accept(",")
                self.whitespace()
                self.json_string()
                self.whitespace()
                self.accept(":")
                self.whitespace()
                self.json_value()
                self.whitespace()
        self.accept("}")

for name, value in JSON.rules.items():
    print(name, '<--', value,'.')

print()
parser = JSON.parser({})
buf = "[1, 2, 3]"
node = parser.parse(buf)

walk(node, "")
print()

print(node.build(buf, builder))
print()

parser = JSON.parser(builder)
print(parser.parse("[1, 2, 3]"))
print()


class YAML(Grammar, start="document", whitespace=[" ", "\t"], newline=["\n"]):
    @rule()
    def document(self):
        self.whitespace()
        with self.capture("document"), self.choice():
            with self.case():
                self.list_flow_rule()
            with self.case():
                self.list_rule()
            with self.case():
                self.object_rule()

    @rule()
    def list_flow_rule(self):
        with self.indented(), self.capture('list'):
            self.accept("-")
            with self.choice():
                with self.case():
                    self.whitespace()
                    self.value_flow_rule()
                with self.case():
                    self.whitespace()
                    self.newline()
                    self.indent()
                    self.accept(' ')
                    self.whitespace()
                    self.value_flow_rule()

            with self.repeat():
                self.whitespace()
                self.newline()
                self.indent()
                self.accept("-")
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.value_flow_rule()
                    with self.case():
                        self.whitespace()
                        self.newline()
                        self.indent()
                        self.whitespace()
                        self.value_flow_rule()

    @rule()
    def value_flow_rule(self):
        with self.choice():
            with self.case():
                self.number_rule()
            with self.case():
                self.list_flow_rule()

    value_rule = rule( 
        list_rule | object_rule |
        string_rule | number_rule |
        true_rule | false_rule | 
        null_rule
    )
    
    true_rule = rule(accept("true"), capture="bool")
    false_rule = rule(accept("false"), capture="bool")
    null_rule = rule(accept("null"), capture="null")

    @rule()
    def number_rule(self):
        with self.capture("number"):
            with self.optional():
                self.range("-", "+")
            with self.repeat(min=1):
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
    def string_rule(self):
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
    def list_rule(self):
        self.accept("[")
        self.whitespace()
        with self.capture("list"), self.repeat(max=1):
            self.value_rule()
            with self.repeat(min=0):
                self.whitespace()
                self.accept(",")
                self.whitespace()
                self.value_rule()
        self.accept("]")

    @rule()
    def object_rule(self):
        self.accept("{")
        self.whitespace()
        with self.capture("object"), self.optional():
            self.string_rule()
            self.whitespace()
            self.accept(":")
            self.whitespace()
            self.value_rule()
            self.whitespace()
            with self.repeat(min=0):
                self.accept(",")
                self.whitespace()
                self.string_rule()
                self.whitespace()
                self.accept(":")
                self.whitespace()
                self.value_rule()
                self.whitespace()
        self.accept("}")

for name, value in YAML.rules.items():
    print(name, '<--', value,'.')

parser = YAML.parser({})
buf = """\
- 1
- 2
- 
  - 3
  - 4
- 5
- 6
- - 7
  - 8
  - - 9
  - 
    - 10
    - 11
- 12
"""
node = parser.parse(buf)
walk(node)
print(node.build(buf, builder))
