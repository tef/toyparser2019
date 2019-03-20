from grammar import Grammar

import codecs

def walk(node, indent="- "):
    print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")

def unescape(string):
    return codecs.decode(string, 'unicode_escape')

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

class Expr(Grammar, start="expr", whitespace=[" ", "\t"], newline=["\n"]):
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

    expr = rule(literal)
    expr = rule( accept("("), expr, accept(")") )

    expr = recursive(
           [mul, div],
           [add, sub],
    )

    mul = left(expr, accept("*"), expr, capture="mul")
    div = left(expr, accept("/"), expr, capture="div")
    add = left(expr, accept("+"), expr, capture="add")
    sub = left(expr, accept("-"), expr, capture="sub")



for name, value in Expr.rules.items():
    print(name, '<--', value,'.')

def parse(buf):
    parser = Expr.parser({})
    node = parser.parse(buf)
    walk(node)
    print(node.build(buf, builder))

# parse("1+2")

