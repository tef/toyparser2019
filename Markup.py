from grammar import Grammar

import codecs

def walk(node, indent="- "):
    print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")

def unescape(string):
    return codecs.decode(string, 'unicode_escape')

builder = {
    'document': (lambda buf, children: children),
    'para': (lambda buf, children: {"para":children}),
    'header': (lambda buf, children: {"header":children}),
    'level': (lambda buf, children: len(buf)),
    'text': (lambda buf, children: buf),
}

class Markup(Grammar, start="document", whitespace=[" ", "\t"], newline=["\n"]):
    @rule()
    def document(self):
        with self.capture("document"), self.repeat(min=0):
            self.element()
        self.whitespace()
        self.eof()

    element = rule(
        header | para | empty_lines
    )

    inline_element = rule(word)

    @rule()
    def header(self):
        with self.capture("header"):
            with self.capture('level'), self.repeat(min=1):
                self.accept("#")
            with self.optional():
                self.whitespace()
            with self.capture('text'):
                self.inline_element()
                with self.repeat():
                    self.whitespace()
                    self.inline_element()
            self.whitespace()
            with self.choice():
                with self.case(): self.eof()
                with self.case(): self.newline()

    @rule()
    def para(self):
        self.whitespace()
        with self.capture("para"):
            with self.capture('text'):
                self.inline_element()
            with self.repeat():
                with self.reject():
                    self.newline()
                    self.whitespace()
                    self.newline()
                    self.whitespace()
                with self.choice():
                    with self.case(): 
                        self.whitespace()
                        self.newline()
                        self.whitespace()
                    with self.case():
                        self.whitespace()
                with self.capture('text'):
                    self.inline_element()

            self.whitespace()
            with self.choice():
                with self.case():
                    self.eof()
                with self.case():
                    self.newline()
                    self.whitespace()
            with self.choice():
                with self.case(): self.eof()
                with self.case(): self.newline()
            
    @rule()
    def empty_lines(self):
        with self.repeat(min=1):
            self.whitespace()
            self.newline()

    @rule()
    def word(self):
        with self.capture('text'), self.repeat(min=1):
            self.range(" ", "\n", invert=True)

        
for name, value in Markup.rules.items():
    print(name, '<--', value,'.')

def markup(buf):
    parser = Markup.parser({})
    node = parser.parse(buf)
    if node:
        walk(node)
        print(node.build(buf, builder))

markup("# butt")
markup("""a b c\n\n""")
markup("""a b c\n""")
markup("""a b c""")
markup("""
d e f

g h i
j l k

b r b
"""
)