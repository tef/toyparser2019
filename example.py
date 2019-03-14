from textexpressions import Grammar

class JSON(Grammar, start="document"):
    document = json_list 
    document = json_object

    json_value = rule( 
        json_list | json_object |
        json_string | json_number |
        json_true | json_false | 
        json_null
    )
    
    json_true = capture("bool", accept("true"))
    json_false = capture("bool", accept("false"))
    json_null = capture("null", accept("null"))

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
        with self.capture("list"), self.repeat(max=1):
            self.json_value()
            with self.repeat(min=0):
                self.accept(",")
                self.json_value()
        self.accept("]")

    @rule()
    def json_object(self):
        self.accept("{")
        with self.capture("object"), self.optional():
            self.json_string()
            self.accept(":")
            self.json_value()
            with self.repeat(min=0):
                self.accept(",")
                self.json_string()
                self.accept(":")
                self.json_value()
        self.accept("}")

for name, value in JSON.rules.items():
    print(name, '<--', value,'.')
    print()

parser = JSON.parser({})
node = parser.parse("[1,2,3]")

def walk(node, indent):
    print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")

walk(node, "")
print()

import codecs

builder = {
    'number': (lambda buf, stack: int(buf)),
    'string': (lambda buf, stack: codecs.decode(buf, 'unicode_escape')),
    'list': (lambda buf, stack: stack),
    'object': (lambda buf, stack: dict(stack)),
    'document': (lambda buf, stack: stack[0]),
}

parser = JSON.parser(builder)
print(parser.parse("[1,2,3]"))
print()
