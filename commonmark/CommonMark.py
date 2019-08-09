from grammar import Grammar, compile_python

import codecs

def walk(node, indent="- "):
    print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")

def unescape(string):
    return codecs.decode(string, 'unicode_escape')

ast_builder = {
    'document': (lambda buf, pos, end, children: children),
    'thematic_break': (lambda buf, pos, end, children: {'hr': buf[pos:end]}),
    'atx_heading': (lambda buf, pos, end, children: {"heading":children}),
    'setext_heading': (lambda buf, pos, end, children: {"heading":[children[-1]]+children[:-1]}),
    'indented_code': (lambda buf, pos, end, children: {"indented_code":children}),
    'fenced_code': (lambda buf, pos, end, children: {"fenced_code":children}),
    'info': (lambda buf, pos, end, children: {"info":buf[pos:end]}),
    'blockquote': (lambda buf, pos, end, children: {"blockquote":children}),
    'block_list': (lambda buf, pos, end, children: {"list":children}),
    'list_item': (lambda buf, pos, end, children: {"item":children}),
    'para': (lambda buf, pos, end, children: {"para":children}),
    'text': (lambda buf, pos, end, children: buf[pos:end]),
}

builder = {}

_builder = lambda fn:builder.__setitem__(fn.__name__,fn)

@_builder
def document(buf, pos,end, children):
    def wrap(c):
        if isinstance(c, tuple):
            return f"<p>{c[0]}</p>"
        return c
    text = '\n'.join(wrap(c) for c in children if c)
    return text

@_builder
def thematic_break(buf, pos,end, children):
    return "<hr/>\n"

@_builder
def atx_heading(buf, pos,end, children):
    return f"<h{children[0]}>{' '.join(children[1:])}</h{children[0]}>"

@_builder
def setext_heading(buf, pos,end, children):
    return f"<h{children[-1]}>{' '.join(children[:-1])}</h{children[-1]}>"

@_builder
def indented_code(buf, pos,end, children):
    text = "\n".join(children)
    return f"<pre><code>{text}\n</code></pre>"

@_builder
def fenced_code(buf, pos,end, children):
    info = children[0]
    language = ""
    if info:
        language = f' class="language-{info}"'
    text = "\n".join(children[1:])
    return f"<pre><code{language}>{text}</code></pre>"

@_builder
def info(buf, pos,end, children):
    text = buf[pos:end].lstrip().split(' ',1)
    if text: return text[0]

@_builder
def blockquote(buf, pos, end, children):
    def wrap(c):
        if isinstance(c, tuple):
            return f"<p>{c[0]}</p>"
        return c
    text = '\n'.join(wrap(c) for c in children if c)
    return f"<blockquote>\n{text}\n</blockquote>"

@_builder
def block_list(buf, pos,end, children):
    out = ["<ul>\n"]
    print(children)
    if None in children or any(None in c for c in children):
        def wrap(c):
            if isinstance(c, tuple):
                return f"<p>{c[0]}</p>"
            return c
        for item in children:
            if not item: continue
            item = "\n".join(wrap(line) for line in item if line)
            out.append(f"<li>\n{item}\n</li>\n")
    else:
        def wrap(c):
            if isinstance(c, tuple):
                return f"{c[0]}"
            return c
        for item in children:
            item = "\n".join(wrap(line) for line in item) 
            out.append(f"<li>{item}</li>\n")
    out.extend("</ul>")
    return "".join(out)

@_builder
def list_item(buf, pos,end, children):
    return children

@_builder
def para(buf, pos,end, children):
    text= " ".join(c for c in children if c)
    return (text,)

@_builder
def text(buf, pos,end, children):
    return buf[pos:end]

@_builder
def empty(buf, pos, end, children):
    return None

class CommonMark(Grammar, start="document", whitespace=[" ", "\t"], newline=["\n"], tabstop=4):
    version = 0.29
    @rule()
    def document(self):
        with self.capture("document"), self.repeat(min=0):
            self.start_of_line()
            self.block_element()
        self.whitespace()
        self.eof()

    # 3. Block and Inline Elemnts

    block_element = rule(
        empty_lines |
        indented_code_block | 
        fenced_code_block |
        blockquote | 
        atx_heading |  
            # 4.1 Ex 29. Headers take precidence over thematic breaks
        thematic_break |  
            # 4.1 Ex 30. Thematic Breaks take precidence over lists
        # HTML Block
        # Link reference_definiton
        block_list |
        setext_heading |     
        para 
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
        self.line_end()

    @rule()
    def atx_heading(self):
        self.whitespace(max=3)
        with self.capture("atx_heading"):
            with self.count('#') as level:
                with self.repeat(min=1, max=6):
                    self.accept("#")
            self.capture(value=level)
            with self.choice():
                with self.case():
                    self.line_end()
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
        self.end_of_line()

    @rule()
    def setext_heading(self):
        # 4.3 they cannot be interpretable as a code fence, 
        # ATX heading, block quote, thematic break, list item, or HTML block.
        self.whitespace(max=3)
        with self.capture('setext_heading'):
            self.inline_para()
            self.whitespace()
            self.newline()
            self.start_of_line()
            self.setext_heading_line()

    @rule()
    def setext_heading_line(self):
        self.whitespace(max=3)
        with self.choice():
            with self.case():
                with self.repeat(min=1):
                    self.accept('-')
                self.capture(value=2)
            with self.case():
                with self.repeat(min=1):
                    self.accept('=')
                self.capture(value=2)
        self.line_end()

    @rule()
    def indented_code_block(self):
        self.whitespace(min=4, max=4)
        with self.indented(), self.capture('indented_code'):
            with self.capture('text'), self.repeat(min=1):
                self.range("\n", invert=True)
            self.end_of_line()
            with self.repeat():
                self.start_of_line()
                with self.choice():
                    with self.case():
                        self.whitespace()
                        with self.capture('text'), self.repeat(min=1):
                            self.range("\n", invert=True)
                        self.end_of_line()
                    with self.case():
                        with self.capture('text'):
                            self.whitespace()
                        self.newline()
                        with self.repeat():
                            self.start_of_line()
                            with self.capture('text'):
                                self.whitespace()
                            self.newline()
                            self.end_of_line()
                        with self.lookahead():
                            self.start_of_line()


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
        with self.capture('info'), self.repeat(min=0):
            with self.reject(): # Example 115
                self.accept(fence)
            self.range("\n", invert=True)
        self.line_end()
        with self.repeat():
            self.start_of_line()
            with self.reject():
                self.whitespace(max=3)
                self.accept(fence)
            with self.capture('text'), self.repeat(min=0):
                self.range("\n", invert=True)
            self.line_end()
        self.start_of_line()
        self.whitespace(max=3)
        self.accept(fence)
        self.line_end()


    @rule()
    def tilde_code_block(self):
        fence = "~~~"
        self.accept(fence)
        with self.capture('info'), self.repeat(min=0):
            self.range("\n", invert=True)
        self.line_end()
        with self.repeat():
            self.start_of_line()
            with self.reject():
                self.whitespace(max=3)
                self.accept(fence)
            with self.capture('text'), self.repeat(min=0):
                self.range("\n", invert=True)
            self.line_end()
        self.start_of_line()
        self.whitespace(max=3)
        self.accept(fence)
        self.line_end()

    @rule()
    def blockquote_prefix(self):
        with self.choice():
            with self.case():
                self.start_blockquote()
            with self.case():
                with self.reject(), self.choice():
                    with self.case(): 
                        self.whitespace()
                        self.newline()
                    with self.case(): self.thematic_break()
                    with self.case(): self.setext_heading_line()
                    with self.case(): self.start_fenced_block()
                    with self.case(): self.start_list()

    @rule()
    def start_blockquote(self):
        self.whitespace(max=3)
        self.accept('>')
        self.whitespace(max=1, newline=True)

    @rule()
    def blockquote(self):
        with self.capture("blockquote"):
            self.start_blockquote()
            with self.blockquote_prefix.as_line_prefix():
                self.block_element()
                with self.repeat():
                    self.start_of_line()
                    with self.choice():
                        with self.case():
                            self.block_element()
                        with self.case():
                            self.whitespace()
                            self.newline()

    @rule()
    def start_list(self):
        self.whitespace(max=3)
        self.accept('-')
        self.whitespace(min=1)

    @rule()
    def block_list(self):
        with self.capture("block_list"):
            self.start_list()
            with self.capture("list_item"):
                self.list_item()
            with self.repeat():
                self.start_of_line()
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.newline()
                        with self.repeat():
                            self.start_of_line()
                            self.whitespace()
                            self.newline()
                        with self.lookahead():
                            self.start_of_line()
                            self.whitespace(max=3)
                            self.accept('-')
                        with self.capture('empty'):
                            pass
                    with self.case():
                        self.whitespace(max=3)
                        self.accept('-')
                        self.whitespace(min=1)
                        with self.capture("list_item"):
                            self.list_item()

    @rule()
    def list_item(self):
        with self.indented():
            self.block_element()
            with self.repeat():
                self.start_of_line()
                with self.choice():
                    with self.case():
                        self.block_element()
                    with self.case():
                        with self.repeat():
                            self.start_of_line()
                            self.whitespace()
                            self.newline()
                        with self.lookahead():
                            self.start_of_line()

    @rule()
    def para(self):
        self.whitespace(max=3)
        with self.memoize(),self.capture("para"):
            self.inline_para.inline()
            self.whitespace()
            self.end_of_line()
            

    @rule()
    def inline_para(self):
        with self.capture('text'):
            self.inline_element()
        with self.repeat():
            with self.reject():
                self.newline()
                self.whitespace()
                self.newline()
            with self.reject():
                self.newline()
                self.start_of_line()
                self.whitespace()
                self.newline()
            with self.choice():
                with self.case(): 
                    self.whitespace(max=1)
                    self.newline()
                    self.start_of_line()
                    with self.reject():
                        self.para_interrupt.inline()
                    self.whitespace()
                with self.case():
                    self.whitespace(min=2)
                    self.newline()
                    self.start_of_line()
                    with self.reject():
                        self.para_interrupt.inline()
                    with self.capture('empty'):
                        pass
                with self.case():
                    self.whitespace()
            # 4.1 Ex 27, 28. Thematic Breaks can interrupt a paragraph
            with self.capture('text'):
                self.inline_element()

    @rule()
    def para_interrupt(self):
        with self.choice():
            with self.case(): self.thematic_break()
            with self.case(): self.setext_heading_line()
            with self.case(): self.start_fenced_block()
            with self.case(): self.start_list()
            with self.case(): self.start_blockquote()

    @rule()
    def empty_lines(self):
        with self.repeat(min=1):
            self.whitespace()
            self.newline()
            self.start_of_line()
        with self.capture("empty"):
            pass

    @rule() # 2.1 line ends by newline or eof
    def line_end(self):
        self.whitespace()
        self.end_of_line()

    @rule()
    def word(self):
        with self.capture('text'), self.repeat(min=1):
            self.range(" ", "\n", invert=True)

if __name__ == "__main__":
    with open('CommonMarkParser.py', 'w') as fh:
        fh.write(compile_python(CommonMark))
            
    for name, value in CommonMark.rules.items():
        print(name, '<--', value,'.')

    print(CommonMark.version)

def _markup(buf):
    parser = CommonMark.parser(builder)
    node = parser.parse(buf)
    if node:
        print("test")
        for b in buf.splitlines():
            print(b)
        print()
        print(node)
        print()
        # print(node.build(buf, builder))

markup = _markup # lambda x:x
if name != '__main__': markup = lambda x:x
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
markup("# butt\n")
markup("   ##### butt #####\n")
markup("   ##### butt ##### a\n")
_markup("""
ab
c

> a
b c d

a b c
""")
markup("""
ab
c

>> a
>b c d

a b c
""")
markup("---")
markup("   ---   \n")
markup("""
d1 e2 f3
----

g h i
j l k

----

b r b
"""
)
_markup("""\
> a 
> > b

ddff
""")
markup("""\
- 1
- 2
- 3

four

- a

- c

  - d 

  - e

- f

""")
markup("""\

    a

    v

>     t
>      
>     u

    b
     
    t
""")

with open("../README.md") as readme:
    markup(readme.read())
