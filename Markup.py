from toyparser.grammar import Grammar

import codecs

def walk(node, indent="- "):
    print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")

def unescape(string):
    return codecs.decode(string, 'unicode_escape')

builder = {
    'document': (lambda buf, node, children: children),
    'para': (lambda buf, node, children: {"para":children}),
    'header': (lambda buf, node, children: {"header":children}),
    'text': (lambda buf, node, children: buf[node.start:node.end]),
}

class Markup(Grammar, start="document", whitespace=[" ", "\t"], newline=["\n"]):
    @rule()
    def document(self):
        with self.repeat(min=0):
            self.element()
        self.whitespace()
        self.end_of_file()

    element = rule(
        blockquote | header | para | hr | empty_lines
    )

    inline_element = rule(word)

    @rule()
    def header(self):
        with self.capture_node("header"):
            with self.count('#') as c, self.repeat(min=1):
                self.literal("#")
            self.capture_value(c)
            with self.optional():
                self.whitespace()
            with self.capture_node('text'):
                self.inline_element()
                with self.repeat():
                    self.whitespace()
                    self.inline_element()
            self.whitespace()
            with self.choice():
                with self.case(): self.end_of_file()
                with self.case(): self.newline()

    @rule()
    def para(self):
        self.whitespace()
        with self.capture_node("para"):
            with self.capture_node('text'):
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
                with self.capture_node('text'):
                    self.inline_element()

            self.whitespace()
            with self.choice():
                with self.case():
                    self.end_of_file()
                with self.case():
                    self.newline()
                    self.whitespace()
            with self.choice():
                with self.case(): self.end_of_file()
                with self.case(): self.newline()
            
    @rule()
    def hr(self):
        self.whitespace()
        self.literal("---")
        self.whitespace()
        with self.choice():
            with self.case(): self.end_of_file()
            with self.case(): self.newline()
    @rule()
    def empty_lines(self):
        with self.repeat(min=1):
            self.whitespace()
            self.newline()

    @rule()
    def word(self):
        with self.capture_node('text'), self.repeat(min=1):
            self.range(" ", "\n", invert=True)

    @rule()
    def start_blockquote(self):
        self.whitespace()
        self.literal('>')
        
    @rule()
    def blockquote(self):
        self.start_blockquote()
        with self.indented(indent=self.start_blockquote):
            self.para()
for name, value in Markup.rules.items():
    print(name, '<--', value,'.')

def markup(buf):
    parser = Markup.parser()
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
