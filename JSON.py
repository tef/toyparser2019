from grammar import Grammar, ParserState

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


parser1 = JSON.compile_old(builder)
parser2 = JSON.compile(builder)

import time, json

s = json.dumps(list(range(25000)))
print('file is', len(s)/1024, 'k')

def timeit(name,parser, buf):
    t = time.time()
    o = parser(buf)
    t = time.time() - t
    print(name, t)


timeit("json", json.loads, s)
timeit("inew", parser2.parse, s)
timeit("comp", parser1.parse, s)
timeit("inter", parser.parse, s)


