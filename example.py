from textexpressions import Grammar

def walk(node, indent):
    print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")

class JSON(Grammar, start="document"):
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

    whitespace = rule(repeat(range(" ", "\t", "\r", "\n")), capture=None)

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

import codecs

builder = {
    'number': (lambda buf, children: int(buf)),
    'string': (lambda buf, children: codecs.decode(buf, 'unicode_escape')),
    'list': (lambda buf, children: children),
    'object': (lambda buf, children: dict(children)),
    'document': (lambda buf, children: children[0]),
}

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


class Expression(Grammar, start="number"):
    #expr[50] = rule(expr < 50, accept("+"), expr <= 50, capture="+")
    # expr[0] = number
    @rule()
    def number(self):
        with self.capture("number"):
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

for name, value in Expression.rules.items():
    print(name, '<--', value,'.')

print()
parser = Expression.parser({})
node = parser.parse("1")

walk(node, "")
print()
