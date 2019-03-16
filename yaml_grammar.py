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
    'pair': (lambda buf, children: children),
    'document': (lambda buf, children: children[0]),
    'identifier': (lambda buf, children: str(buf)),
    'bool': (lambda buf, children: bool(buf)),
    'null': (lambda buf, children: None),
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

for name, value in JSON.rules.items():
    print(name, '<--', value,'.')

print()
parser = JSON.parser({})
buf = '[1, 2, 3, "fooo"]'
node = parser.parse(buf)

walk(node, "")
print()

print(node.build(buf, builder))
print()

parser = JSON.parser(builder)
print(parser.parse("[1, 2, 3]"))
print()

class YAML(Grammar, start="document", whitespace=[" ", "\t"], newline=["\n"]):
    literal = rule( 
        list_literal | object_literal |
        string_literal | number_literal |
        true_literal | false_literal | 
        null_literal
    )

    true_literal = rule(accept("true"), capture="bool")
    false_literal = rule(accept("false"), capture="bool")
    null_literal = rule(accept("null"), capture="null")

    @rule()
    def identifier(self):
        with self.choice():
            with self.case(), self.capture('identifier'), self.repeat(min=1):
                self.range("a-z","A-Z","_")
            with self.case():
                self.string_literal()

    @rule()
    def number_literal(self):
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
    def string_literal(self):
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
    def list_literal(self):
        self.accept("[")
        self.whitespace()
        with self.capture("list"), self.repeat(max=1):
            self.literal()
            with self.repeat(min=0):
                self.whitespace()
                self.accept(",")
                self.whitespace()
                self.literal()
        self.accept("]")

    @rule()
    def object_literal(self):
        self.accept("{")
        self.whitespace()
        with self.capture("object"), self.optional():
            self.string_literal()
            self.whitespace()
            self.accept(":")
            self.whitespace()
            self.literal()
            self.whitespace()
            with self.repeat(min=0):
                self.accept(",")
                self.whitespace()
                self.string_literal()
                self.whitespace()
                self.accept(":")
                self.whitespace()
                self.literal()
                self.whitespace()
        self.accept("}")

    @rule()
    def end_of_line(self):
        with self.repeat(), self.choice():
            with self.case():
                self.whitespace()
                self.accept('#')
                with self.repeat():
                    self.range("\n", invert=True)
                self.newline()
            with self.case():
                self.whitespace()
                self.newline()

    
    @rule()
    def indented_list(self):
        with self.indented(), self.capture('list'):
            self.accept("-")
            with self.choice():
                with self.case():
                    self.whitespace()
                    self.indented_value()
                with self.case():
                    self.end_of_line()
                    self.indent()
                    self.accept(' ')
                    self.whitespace()
                    self.indented_value()

            with self.repeat():
                self.end_of_line()
                self.indent()
                self.accept("-")
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.indented_value()
                    with self.case():
                        self.end_of_line()
                        self.indent()
                        self.whitespace()
                        self.indented_value()

    @rule()
    def indented_object(self):
        with self.indented(), self.capture('object'):
            with self.capture("pair"):
                self.identifier()
                self.whitespace()
                self.accept(":")
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.indented_value()
                    with self.case():
                        self.end_of_line()
                        self.indent()
                        self.accept(' ')
                        self.whitespace()
                        self.indented_value()

            with self.repeat(), self.capture("pair"):
                self.end_of_line()
                self.indent()
                self.identifier()
                self.whitespace()
                self.accept(":")
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.indented_value()
                    with self.case():
                        self.end_of_line()
                        self.indent()
                        self.whitespace()
                        self.indented_value()

    @rule()
    def indented_value(self):
        with self.choice():
            with self.case():
                self.indented_object()
            with self.case():
                self.indented_list()
            with self.case():
                self.literal()

    @rule()
    def document(self):
        with self.optional():
            self.whitespace()
            self.end_of_line()
        with self.capture("document"), self.choice():
            with self.case():
                self.indented_object()
            with self.case():
                self.indented_list()
            with self.case():
                self.list_literal()
            with self.case():
                self.object_literal()



for name, value in YAML.rules.items():
    print(name, '<--', value,'.')

def yaml(buf):
    parser = YAML.parser({})
    node = parser.parse(buf)
    walk(node)
    print(node.build(buf, builder))

yaml("""\
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
-
 13
""")

yaml("""\
name: 1
example: 2
""")

yaml("""\
title: "SafeYAML Example"

database:
  server: "192.168.1.1"

  ports:
    - 8000
    - 8001
    - 8002

  enabled: true

servers:
  # JSON-style objects
  alpha: {
    "ip": "10.0.0.1",
    "names": [
      "alpha",
      "alpha.server",
    ],
  }
  beta: {
    "ip": "10.0.0.2",
    "names": ["beta"],
  }
""")
