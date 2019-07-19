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
    'thematic_break': (lambda buf, children: {"hr": buf}),
    'atx_heading': (lambda buf, children: {"heading":children}),
    'atx_level': (lambda buf, children: len(buf)),
    'setext_heading': (lambda buf, children: {"heading":children[::-1]}),
    'indented_code': (lambda buf, children: {"indented_code":children}),
    'fenced_code': (lambda buf, children: {"fenced_code":children}),
    'para': (lambda buf, children: {"para":children}),
    'text': (lambda buf, children: buf),
    'info': (lambda buf, children: {"info":buf}),
}

class CommonMark(Grammar, start="document", whitespace=[" ", "\t"], newline=["\n"]):
    version = 0.29
    @rule()
    def document(self):
        with self.capture("document"), self.repeat(min=0):
            self.block_element()
        self.whitespace()
        self.eof()

    # 3. Block and Inline Elemnts

    block_element = rule(
        indented_code_block | 
        fenced_code_block |
        # blockquote
        atx_heading |  
            # 4.1 Ex 29. Headers take precidence over thematic breaks
        thematic_break |  
            # 4.1 Ex 30. Thematic Breaks take precidence over lists
        # list items
        # HTML Block
        # Link reference_definiton
        setext_heading |     
        para | 
        empty_lines
    )

    inline_element = rule(word)
    # \ escapes
    # entity
    # code spans
    # emph
    # links
    # images
    # autolinks
    # html

    @rule() # 4.1
    def thematic_break(self):
        self.whitespace(min=0, max=3)
        with self.capture('thematic_break'), self.choice():
            with self.case(), self.repeat(min=3):
                self.accept("-")
                self.whitespace()
            with self.case(), self.repeat(min=3):
                self.accept("*")
                self.whitespace()
            with self.case(), self.repeat(min=3):
                self.accept("_")
                self.whitespace()
        self.end_of_line()

    @rule()
    def atx_heading(self):
        self.whitespace(max=3)
        with self.capture("atx_heading"):
            with self.count('#') as level:
                with self.capture('atx_level'), self.repeat(min=1, max=6):
                    self.accept("#")
            with self.choice():
                with self.case():
                    self.end_of_line()
                with self.case():
                    self.whitespace(min=1)
            with self.capture('text'):
                self.inline_element()
                with self.repeat():
                    with self.reject():
                        self.atx_heading_end()
                    self.whitespace()
                    self.inline_element()
        self.atx_heading_end()

    @rule()
    def atx_heading_end(self):
        with self.optional():
            self.whitespace(min=1)
            with self.repeat():
                self.accept("#")
        self.whitespace()
        with self.choice():
            with self.case(): self.eof()
            with self.case(): self.newline()

    @rule()
    def setext_heading(self):
        # 4.3 they cannot be interpretable as a code fence, 
        # ATX heading, block quote, thematic break, list item, or HTML block.
        self.whitespace(max=3)
        with self.capture('setext_heading'):
            self.inline_para()
            self.whitespace()
            self.newline()
            self.setext_heading_line()

    @rule()
    def setext_heading_line(self):
        self.whitespace(max=3)
        with self.choice():
            with self.case():
                with self.repeat(min=1):
                    self.accept('-')
                self.capture_value(2)
            with self.case():
                with self.repeat(min=1):
                    self.accept('=')
                self.capture_value(2)
        self.end_of_line()

    @rule()
    def indented_code_block(self):
        self.whitespace(min=4, max=4)
        with self.indented(), self.capture('indented_code'):
            self.whitespace()
            self.indented_code_line()
            with self.repeat(), self.choice():
                with self.case():
                    self.indent()
                    self.indented_code_line()
                with self.case():
                    self.whitespace()
                    self.newline()
                    self.capture_value("")

    @rule()
    def indented_code_line(self):
        with self.capture('text'), self.repeat(min=1):
            with self.reject():
                self.end_of_line()
            self.range("\n", invert=True)
        with self.choice():
            with self.case(): self.eof()
            with self.case(): self.newline()

    @rule()
    def fenced_code_block(self):
        self.whitespace(max=3)
        with self.capture('fenced_code'):
            with self.choice():
                with self.case():
                    self.tilde_code_block()
                with self.case():
                    self.backtick_code_block()

    @rule()
    def start_fenced_block(self):
        self.whitespace(max=3)
        with self.choice():
            with self.case(): self.accept("```")
            with self.case(): self.accept("~~~")

    @rule()
    def backtick_code_block(self):
        fence = "```"
        self.accept(fence)
        with self.capture('info'), self.repeat(min=1):
            with self.reject(): # Example 115
                self.accept(fence)
            self.range("\n", invert=True)
        self.end_of_line()
        with self.repeat():
            with self.reject():
                self.whitespace(max=3)
                self.accept(fence)
            with self.capture('text'), self.repeat(min=1):
                self.range("\n", invert=True)
            self.end_of_line()
        self.whitespace(max=3)
        self.accept(fence)
        self.end_of_line()


    @rule()
    def tilde_code_block(self):
        fence = "~~~"
        self.accept(fence)
        with self.capture('info'), self.repeat(min=1):
            self.range("\n", invert=True)
        self.end_of_line()
        with self.repeat():
            with self.reject():
                self.whitespace(max=3)
                self.accept(fence)
            with self.capture('text'), self.repeat(min=1):
                self.range("\n", invert=True)
            self.end_of_line()
        self.whitespace(max=3)
        self.accept(fence)
        self.end_of_line()

    @rule()
    def blockquote(self):
        self.whitespace(max=3)


    @rule()
    def para(self):
        self.whitespace(max=3)
        with self.capture("para"):
            self.inline_para()
            self.whitespace()
            with self.choice():
                with self.case():
                    self.eof()
                with self.case():
                    self.newline()
                    self.whitespace()
            with self.choice():
                # 4.1 Ex 27, 28. Thematic Breaks can interrupt a paragraph
                with self.case(), self.lookahead():
                    self.para_interrupt()
                with self.case(): self.eof()
                with self.case(): self.newline()
            

    @rule()
    def inline_para(self):
        with self.capture('text'):
            self.inline_element()
        with self.repeat():
            with self.reject():
                self.newline()
                self.whitespace()
                self.newline()
            with self.choice():
                with self.case(): 
                    self.whitespace(max=1)
                    self.newline()
                    self.whitespace()
                with self.case():
                    self.whitespace(min=2)
                    self.newline()
                    self.capture_value("\n")
                with self.case():
                    self.whitespace()
            # 4.1 Ex 27, 28. Thematic Breaks can interrupt a paragraph
            with self.reject():
                self.para_interrupt()
            with self.capture('text'):
                self.inline_element()

    @rule()
    def para_interrupt(self):
        with self.choice():
            with self.case(): self.thematic_break()
            with self.case(): self.setext_heading_line()
            with self.case(): self.start_fenced_block()
    @rule()
    def empty_lines(self):
        with self.repeat(min=1):
            self.whitespace()
            self.newline()

    @rule() # 2.1 line ends by newline or eof
    def end_of_line(self):
        self.whitespace()
        with self.choice():
            with self.case(): self.eof()
            with self.case(): self.newline()

    @rule()
    def word(self):
        with self.capture('text'), self.repeat(min=1):
            self.range(" ", "\n", invert=True)

        
for name, value in CommonMark.rules.items():
    print(name, '<--', value,'.')

print(CommonMark.version)

def markup(buf):
    parser = CommonMark.parser({})
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
markup("---\n")
markup("---")
markup("   ---   \n")
markup("""
d e f
---
g h i
j l k
---
b r b
"""
)
markup("# butt\n")
markup("   ##### butt #####\n")
markup("   ##### butt ##### a\n")
markup("""
aaaa
====

1 2 3 4

bbbb
cccc
dddd
----

1 2 3 4

""")


markup("""\
    buttt
    ubtt

    uttt


    buttt

butt

    butt
    butt

    butt
""")
markup("""\
```
    buttt
    ubtt

    uttt
```

    buttt

butt

~~~ nice
    butt
    butt
~~~

butt
""")
markup("""
aaa bbb  
ddd eee
fff

ggg

```
butt
""")
