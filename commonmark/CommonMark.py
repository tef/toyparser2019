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
    'unordered_list': (lambda buf, pos, end, children: {"list":children}),
    'list_item': (lambda buf, pos, end, children: {"item":children}),
    'para': (lambda buf, pos, end, children: {"para":children}),
    'text': (lambda buf, pos, end, children: buf[pos:end]),
}

import html

builder = {}

_builder = lambda fn:builder.__setitem__(fn.__name__,fn)


def make_para(children):
    return "".join(children)

def join_blocks(children):
    def wrap(c):
        if isinstance(c, tuple):
            return f"<p>{c[0]}</p>"
        return c
    return '\n'.join(wrap(c) for c in children if c)

@_builder
def document(buf, pos,end, children):
    o=join_blocks(children)
    return o+"\n"

@_builder
def thematic_break(buf, pos,end, children):
    return "<hr />"

@_builder
def atx_heading(buf, pos,end, children):
    return f"<h{children[0]}>{make_para(children[1:])}</h{children[0]}>"

@_builder
def setext_heading(buf, pos,end, children):
    return f"<h{children[-1]}>{make_para(children[:-1])}</h{children[-1]}>"

@_builder
def indented_code(buf, pos,end, children):
    text = html.escape("".join(children))
    return f"<pre><code>{text}</code></pre>"

@_builder
def partial_indent(buf, pos, end, children):
    width = children[0]
    return " "*width

@_builder
def code_line(buf, pos, end, children):
    return buf[pos:end]+"\n"

@_builder
def fenced_code(buf, pos,end, children):
    info = children[0]
    language = ""
    if info:
        language = f' class="language-{info}"'
    text = "\n".join(children[1:])
    if text: text = text+"\n"
    return f"<pre><code{language}>{text}</code></pre>"

@_builder
def info(buf, pos,end, children):
    text = buf[pos:end].lstrip().split(' ',1)
    if text: return text[0]

@_builder
def blockquote(buf, pos, end, children):
    text = join_blocks(children)
    end = '\n' if text != '\n' else ''
    start = '\n' if text and text != '\n' else ''
    return f"<blockquote>{start}{text}{end}</blockquote>"

def loose(list_items):
    idx = 0
    while idx < len(list_items) and list_items[idx] is None: idx+=1
    while idx < len(list_items) and list_items[idx] is not None: idx+=1
    while idx < len(list_items) and list_items[idx] is None: idx+=1
    return idx != len(list_items)

@_builder
def unordered_list(buf, pos,end, list_items):
    out = ["<ul>\n"]

    if loose(list_items) or any(loose(c) for c in list_items if c):
        def wrap(c):
            if isinstance(c, tuple):
                return f"<p>{c[0]}</p>"
            return c
        for item in list_items:
            if item == None: continue
            item = "\n".join(wrap(line) for line in item if line)
            out.append(f"<li>\n{item}\n</li>\n")
        out.extend("</ul>")
    else:
        def wrap(c):
            if not c: return ""
            if isinstance(c, tuple):
                return f"{c[0]}"
            return c+"\n"
        for item in list_items:
            text = "\n".join(wrap(line) for line in item) 
            if item and text and not isinstance(item[0], tuple): text=f"\n{text}"
            out.append(f"<li>{text}</li>\n")
        out.extend("</ul>")
    return "".join(out)

@_builder
def list_item(buf, pos,end, children):
    return children

@_builder
def empty(buf, pos, end, children):
    return None

@_builder
def empty_line(buf, pos, end, children):
    return None

@_builder
def para(buf, pos,end, children):
    return (make_para(children),)

@_builder
def code_span(buf, pos, end, children):
    text = " ".join(buf[pos:end].splitlines())
    if text and text[0] == text[-1] == " ":
        text = text[1:-1]
    return f"<code>{text}</code>"

@_builder
def text(buf, pos,end, children):
    return html.escape(buf[pos:end])

@_builder
def softbreak(buf, pos,end, children):
    return "\n"

@_builder
def hardbreak(buf, pos,end, children):
    return f"<br />\n"

@_builder
def whitespace(buf, pos, end, children):
    return buf[pos:end]

class CommonMark(Grammar, start="document", whitespace=[" ", "\t"], newline=["\n"], tabstop=4):
    version = 0.29
    @rule()
    def document(self):
        with self.capture_node("document"), self.repeat(min=0):
            self.start_of_line()
            with self.choice():
                with self.case(): self.block_element()
                with self.case(): self.empty_lines()
        self.whitespace()
        self.eof()

    # 3. Block and Inline Elemnts

    block_element = rule(
        indented_code_block | 
        fenced_code_block |
        blockquote | 
        atx_heading |  
            # 4.1 Ex 29. Headers take precidence over thematic breaks
        thematic_break |  
            # 4.1 Ex 30. Thematic Breaks take precidence over lists
        # HTML Block
        # Link reference_definiton
        unordered_list |
        setext_heading |     
        para 
    )

    @rule() # 4.1
    def thematic_break(self):
        self.whitespace(min=0, max=3)
        with self.capture_node('thematic_break'), self.choice():
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
        with self.capture_node("atx_heading"):
            with self.count(char='#') as level:
                with self.repeat(min=1, max=6):
                    self.accept("#")
            self.capture_value(level)
            with self.choice():
                with self.case():
                    self.atx_heading_end()
                with self.case():
                    self.whitespace(min=1)
                    self.inline_element()
                    with self.repeat():
                        with self.reject():
                            self.atx_heading_end()
                        with self.capture_node("whitespace"):
                            self.whitespace()
                        self.inline_element()
                    with self.optional():
                        self.accept("\\")
                        self.capture_value("\\")
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
        with self.capture_node('setext_heading'):
            with self.no_setext_heading_line.as_line_prefix():
                self.setext_para()
                self.whitespace()
                self.newline()
            self.start_of_line()
            self.setext_heading_line()

    @rule()
    def no_setext_heading_line(self):
        with self.reject():
            self.accept('=','-')

    @rule()
    def setext_heading_line(self):
        self.whitespace(max=3)
        with self.choice():
            with self.case():
                with self.repeat(min=1):
                    self.accept('=')
                self.capture_value(1)
            with self.case():
                with self.repeat(min=1):
                    self.accept('-')
                self.capture_value(2)
        self.line_end()

    @rule()
    def indented_code_block(self):
        self.whitespace(min=4, max=4)
        with self.capture_node('indented_code'), self.indented():

            with self.count(columns=True) as w: self.partial_tab()
            with self.capture_node('partial_indent'): self.capture_value(w)

            with self.capture_node('code_line'):
                self.whitespace()
                with self.repeat(min=1): self.range("\n", invert=True)
            self.end_of_line()

            with self.repeat():
                with self.choice():
                    with self.case():
                        with self.repeat(min=1):
                            self.start_of_line()
                            with self.capture_node('code_line'):
                                self.whitespace()
                            self.newline()
                        with self.lookahead():
                            self.start_of_line()
                            self.whitespace()
                            self.range("\n", invert=True)

                    with self.case():
                        self.start_of_line()
                        with self.count(columns=True) as w: self.partial_tab()
                        with self.capture_node('partial_indent'): self.capture_value(w)

                        with self.capture_node('code_line'):
                            self.whitespace()
                            with self.repeat(min=1): self.range("\n", invert=True)
                        self.end_of_line()


    @rule()
    def fenced_code_block(self):
        self.whitespace(max=3)
        with self.capture_node('fenced_code'):
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
        fence = "`"
        with self.count(char=fence) as c, self.repeat(min=3):
            self.accept(fence)
        with self.capture_node('info'), self.repeat(min=0):
            with self.reject(): # Example 115
                self.accept(fence)
            self.range("\n", invert=True)
        self.line_end()
        with self.repeat():
            self.start_of_line()
            with self.reject():
                self.whitespace(max=3)
                with self.repeat(min=c):
                    self.accept(fence)
                    self.whitespace()
            with self.capture_node('text'), self.repeat(min=0):
                self.range("\n", invert=True)
            self.line_end()
        with self.choice():
            with self.case(): self.eof()
            with self.case():
                self.start_of_line()
                self.whitespace(max=3)
                with self.repeat(min=c):
                    self.whitespace()
                    self.accept(fence)
                self.whitespace()
                self.line_end()


    @rule()
    def tilde_code_block(self):
        fence = "~"
        with self.count(char=fence) as c, self.repeat(min=3):
            self.accept(fence)
        with self.capture_node('info'), self.repeat(min=0):
            self.range("\n", invert=True)
        self.line_end()
        with self.repeat():
            self.start_of_line()
            with self.reject():
                self.whitespace(max=3)
                with self.repeat(min=c):
                    self.accept(fence)
                    self.whitespace()
            with self.capture_node('text'), self.repeat(min=0):
                self.range("\n", invert=True)
            self.line_end()
        with self.choice():
            with self.case(): self.eof()
            with self.case():
                self.start_of_line()
                self.whitespace(max=3)
                with self.repeat(min=c):
                    self.whitespace()
                    self.accept(fence)
                self.whitespace()
                self.line_end()

    @rule()
    def blockquote_prefix(self):
        with self.choice():
            with self.case():
                self.start_blockquote()
                with self.reject():
                    self.whitespace()
                    self.newline()
            with self.case():
                with self.reject(), self.choice():
                    with self.case(): 
                        self.whitespace()
                        self.newline()
                    with self.case():
                        self.whitespace(min=4, max=4)
                        self.range(" ", "\t", "\n", invert=True)
                    with self.case(): self.thematic_break()
                    with self.case(): self.atx_heading()
                    with self.case(): self.start_fenced_block()
                    with self.case(): self.start_list()
                    with self.case(): self.setext_heading_line()
                    with self.case(): self.start_blockquote()

    @rule()
    def start_blockquote(self):
        self.whitespace(max=3)
        self.accept('>')
        with self.choice():
            with self.case(), self.lookahead():
                self.whitespace()
                self.end_of_line()
            with self.case():
                self.whitespace(min=0, max=1)
                with self.lookahead():
                    self.range("\n", invert=True)

    @rule()
    def blockquote(self):
        with self.capture_node("blockquote"):
            self.start_blockquote()
            with self.choice():
                with self.case():
                    self.whitespace()
                    self.end_of_line()
                with self.case():
                    with self.blockquote_prefix.as_line_prefix():
                        with self.reject():
                            self.empty_lines()
                        self.block_element()
            with self.repeat():
                self.start_of_line()
                self.start_blockquote()
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.end_of_line()
                    with self.case():
                        with self.blockquote_prefix.as_line_prefix():
                            with self.reject():
                                self.empty_lines()
                            self.block_element()
                        

    @rule()
    def start_list(self):
        self.whitespace(max=3)
        self.range('-', '*', '+') 
        with self.choice():
            with self.case(), self.lookahead():
                self.whitespace()
                self.end_of_line()
            with self.case():
                self.whitespace(min=1, max=1, newline=True)

    @rule()
    def unordered_list(self):
        with self.capture_node("unordered_list"):
            self.whitespace(max=3)
            with self.backref() as delimiter:
                self.range('-', '*', '+') 

            with self.choice():
                with self.case(), self.lookahead():
                    self.whitespace()
                    self.end_of_line()
                with self.case():
                    self.whitespace(min=1, max=1, newline=True)

            with self.choice():
                with self.case():
                    with self.capture_node("list_item"):
                        self.list_item()
                with self.case():
                    with self.capture_node("list_item"):
                        self.whitespace()
                    self.end_of_line()

            with self.repeat():
                self.start_of_line()
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.newline()
                        with self.capture_node('empty'), self.repeat():
                            self.start_of_line()
                            self.whitespace()
                            self.newline()
                        with self.lookahead():
                            self.start_of_line()
                            self.whitespace(max=3)
                            self.accept(delimiter)
                    with self.case():
                        self.whitespace(max=3)

                        self.accept(delimiter)

                        with self.choice():
                            with self.case(), self.lookahead():
                                self.whitespace()
                                self.end_of_line()
                            with self.case():
                                self.whitespace(min=1, max=1, newline=True)

                        with self.choice():
                            with self.case():
                                with self.capture_node("list_item"):
                                    self.list_item()
                            with self.case():
                                with self.capture_node("list_item"):
                                    self.whitespace()
                                self.end_of_line()

    @rule()
    def list_item(self):
        with self.choice():
            with self.case():
                with self.lookahead():
                    self.whitespace(min=4, max=4)
                    with self.reject():
                        self.line_end()
            with self.case():
                self.whitespace()
                with self.reject(): 
                    self.newline()
            with self.case():
                with self.lookahead():
                    self.whitespace()
                    self.newline()
                with self.indented():
                    self.whitespace()
                    self.newline()
                    self.start_of_line()
                    self.whitespace(min=1, max=1)

        with self.indented():
            self.block_element()
            with self.repeat():
                self.start_of_line()
                with self.optional():
                    with self.repeat():
                        self.whitespace()
                        with self.capture_node("empty"):
                            self.newline()
                        self.start_of_line()
                    with self.lookahead():
                        self.whitespace()
                        self.range("\n", invert=True)
                self.block_element()

    @rule()
    def para(self):
        self.whitespace(max=3)
        with self.memoize(),self.capture_node("para"):
            self.inline_para.inline()
            self.whitespace()
            with self.optional():
                self.accept("\\")
                self.capture_value("\\")
            self.end_of_line()
            
    @rule()
    def setext_para(self):
        self.inline_element()
        with self.repeat():
            with self.choice():
                with self.case():
                    # newline ?
                    with self.choice():
                        with self.case():
                            with self.choice():
                                with self.case(): self.whitespace(min=2)
                                with self.case(): self.accept("\\")
                            with self.capture_node("hardbreak"):
                                self.newline()
                        with self.case():
                            self.whitespace()
                            with self.capture_node("softbreak"):
                                self.newline()

                    with self.choice():
                        with self.case():
                            self.start_of_line()
                            with self.reject():
                                self.para_interrupt.inline()
                            with self.reject():
                                self.setext_heading_line()
                            self.whitespace()
                            with self.reject():
                                self.newline()
                        with self.case():
                            # lazy continuation
                            with self.reject():
                                self.start_of_line()
                            with self.reject():
                                self.para_interrupt.inline()
                            with self.reject():
                                self.setext_heading_line()
                            self.whitespace()
                            with self.reject():
                                self.newline()
                with self.case():
                    with self.capture_node("whitespace"):
                        self.whitespace()
                    with self.optional():
                        with self.capture_node('text'):
                            self.accept("\\")
                        with self.lookahead():
                            self.newline()

            # 4.1 Ex 27, 28. Thematic Breaks can interrupt a paragraph
            self.inline_element()
        self.whitespace()
        with self.optional():
            self.accept("\\")
            self.capture_value("\\")

    @rule()
    def inline_para(self):
        self.inline_element()
        with self.repeat():
            with self.choice():
                with self.case():
                    # newline ?
                    with self.choice():
                        with self.case():
                            with self.choice():
                                with self.case(): self.whitespace(min=2)
                                with self.case(): self.accept("\\")
                            with self.capture_node("hardbreak"):
                                self.newline()
                        with self.case():
                            self.whitespace()
                            with self.capture_node("softbreak"):
                                self.newline()

                    with self.choice():
                        with self.case():
                            self.start_of_line()
                            with self.reject(): self.para_interrupt.inline()
                            self.whitespace()
                            with self.reject(): self.newline()
                        with self.case():
                            # lazy continuation
                            with self.reject():
                                self.start_of_line()
                            with self.reject():
                                self.para_interrupt.inline()
                            self.whitespace()
                            with self.reject():
                                self.newline()
                with self.case():
                    with self.capture_node("whitespace"):
                        self.whitespace()
                    with self.optional():
                        with self.capture_node('text'):
                            self.accept("\\")
                        with self.lookahead():
                            self.newline()

            # 4.1 Ex 27, 28. Thematic Breaks can interrupt a paragraph
            self.inline_element()

    @rule()
    def para_interrupt(self):
        with self.choice():
            with self.case(): self.thematic_break()
            with self.case(): self.atx_heading()
            with self.case(): self.start_fenced_block()
            with self.case(): self.start_list()
            with self.case(): self.start_blockquote()

    @rule()
    def empty_lines(self):
        self.whitespace()
        self.newline()
        with self.repeat():
            self.start_of_line()
            self.whitespace()
            self.newline()
        with self.capture_node("empty_line"):
            pass

    @rule() # 2.1 line ends by newline or eof
    def line_end(self):
        self.whitespace()
        self.end_of_line()


    inline_element = rule(code_span | escaped | word )
    # \ escapes
    # entity
    # code spans
    # emph
    # links
    # images
    # autolinks
    # html
    @rule()
    def code_span(self):
        with self.count(char="`") as c, self.repeat(min=1):
            self.accept("`")
        with self.capture_node('code_span'), self.repeat(min=1), self.choice():
            with self.case():
                self.range("`", invert=True)
            with self.case():
                with self.reject(), self.repeat(min=c, max=c):
                    self.accept("`")
                self.accept("`")
        with self.repeat(min=c, max=c):
            self.accept("`")

    @rule()
    def escaped(self):
        self.accept("\\")
        with self.reject():
            self.newline()
        with self.choice():
            with self.case(), self.capture_node("text"):
                self.range("!-/",":-@","[-`","{-~")
            with self.case():
                self.capture_value("\\")


    @rule()
    def word(self):
        with self.capture_node('text'):
            with self.repeat(min=1):
                self.range(" ", "\n", "\\", invert=True)

if __name__ == "__main__":
    with open('CommonMarkParser.py', 'w') as fh:
        fh.write(compile_python(CommonMark))
            
    #for name, value in CommonMark.rules.items():
    #    print(name, '<--', value,'.')

    print(CommonMark.version)

def _markup(buf):
    parser = CommonMark.parser()
    node = parser.parse(buf)
    if node:
        print("test")
        for b in buf.splitlines():
            print(b)
        print()
        walk(node)
        print()
        print(node.build(buf, builder))

if __name__ != '__main__': markup = lambda x:x
markup = lambda x:x
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
markup("""
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
markup("""\
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


markup("""\
- a  
  b
- c

def

- c
  ```
  d
  ```
- foo

def

- c
 
  d
- e

butt
""")

_markup("""\
> a
> b
> ===
""")
_markup("""\
- a
  b
  ===
""")
_markup("""\
> a
b
===
""")
_markup("""\
- a
b
===
""")
print('spec')
import json
with open("commonmark_0_29.json") as fh:
    tests = json.load(fh)
failed = 0
worked = 0
count =0

parser = CommonMark.parser()
for t in tests:
    markd = t['markdown']
    out1 = parser.parse(markd)
    out = out1.build(markd, builder)
    count +=1
    if out == t['html']: 
        worked +=1
        #print(repr(markd))
        #print(repr(out))
    else:
        failed +=1
        if '<' in markd: continue
        if '*' in markd: continue
        if '1.' in markd: continue
        if '`' in markd: continue
        if '[' in markd: continue
        if '&' in markd: continue
        #if out.replace('\n','') == t['html'].replace('\n',''): continue
        print(t['example'])
        print(repr(markd))
        print('=', repr(t['html']))
        print('X', repr(out))
        print()
        walk(out1)
        print()
print(count, worked, failed)

