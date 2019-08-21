from grammar import Grammar, compile_python

import codecs

def walk(node, indent="- "):
    print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")

def unescape(string):
    return codecs.decode(string, 'unicode_escape')

class CommonMark(Grammar, start="document", capture="document", whitespace=[" ", "\t"], newline=["\n"], tabstop=4):
    version = 0.29
    @rule()
    def document(self):
        with self.repeat(min=0):
            self.indent()
            with self.choice():
                with self.case(): self.block_element()
                with self.case(): self.empty_lines()
        self.whitespace()
        self.end_of_file()

    @rule()
    def empty_lines(self):
        self.whitespace()
        self.newline()
        with self.repeat():
            self.indent()
            self.whitespace()
            self.newline()
        with self.capture_node("empty_line"):
            pass

    @rule() # 2.1 line ends by newline or end_of_file
    def line_end(self):
        self.whitespace()
        self.end_of_line()

    # 3. Block and Inline Elemnts

    block_element = rule(
        indented_code_block | 
        tilde_code_block |
        backtick_code_block |
        blockquote | 
        atx_heading |  
            # 4.1 Ex 29. Headers take precidence over thematic breaks
        thematic_break |  
            # 4.1 Ex 30. Thematic Breaks take precidence over lists
        # HTML Block
        # Link reference_definiton
        ordered_list |
        unordered_list |
        para 
    )

    @rule() # 4.1
    def thematic_break(self):
        self.whitespace(min=0, max=3)
        with self.capture_node('thematic_break'), self.choice():
            with self.case(), self.repeat(min=3):
                self.literal("-")
                self.whitespace()
            with self.case(), self.repeat(min=3):
                self.literal("*")
                self.whitespace()
            with self.case(), self.repeat(min=3):
                self.literal("_")
                self.whitespace()
        self.line_end()

    @rule()
    def atx_heading(self):
        self.whitespace(max=3)
        with self.capture_node("atx_heading"):
            with self.count(char='#') as level:
                with self.repeat(min=1, max=6):
                    self.literal("#")
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
                        self.literal("\\")
                        self.capture_value("\\")
                    self.atx_heading_end()

    @rule()
    def atx_heading_end(self):
        with self.optional():
            self.whitespace(min=1)
            with self.repeat():
                self.literal("#")
        self.whitespace()
        self.end_of_line()


    @rule()
    def indented_code_block(self):
        self.whitespace(min=4, max=4)
        with self.capture_node('indented_code'), self.indented():

            with self.count(columns=True) as w: self.partial_tab()
            with self.capture_node('partial_indent'): self.capture_value(w)

            with self.capture_node('indented_code_line'):
                self.whitespace()
                with self.repeat(min=1): self.range("\n", invert=True)
            self.end_of_line()

            with self.repeat():
                with self.choice():
                    with self.case():
                        with self.repeat(min=1):
                            self.indent()
                            with self.capture_node('indented_code_line'):
                                self.whitespace()
                            self.newline()
                        with self.lookahead():
                            self.indent()
                            self.whitespace()
                            self.range("\n", invert=True)

                    with self.case():
                        self.indent()
                        with self.count(columns=True) as w: self.partial_tab()
                        with self.capture_node('partial_indent'): self.capture_value(w)

                        with self.capture_node('indented_code_line'):
                            self.whitespace()
                            with self.repeat(min=1): self.range("\n", invert=True)
                        self.end_of_line()

    @rule()
    def start_fenced_block(self):
        self.whitespace(max=3)
        with self.choice():
            with self.case(): self.literal("```")
            with self.case(): self.literal("~~~")

    @rule()
    def backtick_code_block(self):
        with self.count(columns=True) as w: 
            self.whitespace(max=3)
        with self.capture_node('fenced_code'):
            fence = "`"
            with self.count(char=fence) as c, self.repeat(min=3):
                self.literal(fence)
            with self.capture_node('info'), self.repeat(min=0):
                with self.reject(): # Example 115
                    self.literal(fence)
                with self.choice():
                    with self.case(): self.escaped_text()
                    with self.case(): self.html_entity()
                    with self.case():
                        with self.capture_node('text'):
                            self.range("\n", invert=True)
                            with self.repeat(min=0):
                                self.range("\n", "\\", "&", "`", invert=True)
            self.line_end()
            with self.repeat():
                self.indent()
                with self.reject():
                    self.whitespace(max=3)
                    with self.repeat(min=c):
                        self.literal(fence)
                        self.whitespace()
                    self.end_of_line()
                self.whitespace(max=w)
                with self.capture_node('text'), self.repeat(min=0), self.choice():
                    with self.case():
                        with self.capture_node('text'):
                            self.range("\n", invert=True)
                            with self.repeat(min=0):
                                self.range("\n", invert=True)
                self.line_end()
            with self.choice():
                with self.case():
                    with self.reject():
                        self.indent()
                with self.case(): 
                    self.whitespace()
                    self.end_of_file()
                with self.case():
                    self.indent()
                    self.whitespace(max=3)
                    with self.repeat(min=c):
                        self.whitespace()
                        self.literal(fence)
                    self.whitespace()
                    self.line_end()


    @rule()
    def tilde_code_block(self):
        with self.count(columns=True) as w: 
            self.whitespace(max=3)
        with self.capture_node('fenced_code'):
            fence = "~"
            with self.count(char=fence) as c, self.repeat(min=3):
                self.literal(fence)
            with self.capture_node('info'), self.repeat(min=0):
                with self.choice():
                    with self.case(): self.escaped_text()
                    with self.case(): self.html_entity()
                    with self.case():
                        with self.capture_node('text'):
                            self.range("\n", invert=True)
                            with self.repeat(min=0):
                                self.range("\n", "\\", "&", invert=True)
            self.line_end()
            with self.repeat():
                self.indent()
                with self.reject():
                    self.whitespace(max=3)
                    with self.repeat(min=c):
                        self.literal(fence)
                        self.whitespace()
                self.whitespace(max=w)
                with self.capture_node('text'), self.repeat(min=0), self.choice():
                    with self.case():
                        with self.capture_node('text'):
                            self.range("\n", invert=True)
                            with self.repeat(min=0):
                               self.range("\n", "\\", invert=True)
                self.line_end()
            with self.choice():
                with self.case():
                    with self.reject():
                        self.indent()
                with self.case(): 
                    self.whitespace()
                    self.end_of_file()
                with self.case():
                    self.indent()
                    self.whitespace(max=3)
                    with self.repeat(min=c):
                        self.whitespace()
                        self.literal(fence)
                    self.whitespace()
                    self.line_end()

    @rule()
    def start_blockquote(self):
        self.whitespace(max=3)
        self.literal('>')
        with self.choice():
            with self.case(), self.lookahead():
                self.whitespace()
                self.end_of_line()
            with self.case():
                self.whitespace(min=0, max=1)
                with self.lookahead():
                    self.range("\n", invert=True)

    @rule()
    def blockquote_interrupt(self):
        with self.choice():
            with self.case(): 
                self.whitespace()
                self.newline()
            with self.case(): self.thematic_break()
            with self.case(): self.atx_heading()
            with self.case(): self.start_fenced_block()
            with self.case(): self.start_list()

    @rule()
    def blockquote(self):
        with self.capture_node("blockquote"):
            self.start_blockquote()
            with self.choice():
                with self.case():
                    self.whitespace()
                    self.end_of_line()
                with self.case():
                    with self.indented(indent=self.start_blockquote, dedent=self.blockquote_interrupt):
                        self.block_element()
            with self.repeat():
                self.indent()
                self.start_blockquote()
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.end_of_line()
                    with self.case():
                        with self.indented(indent=self.start_blockquote, dedent=self.blockquote_interrupt):
                            self.block_element()
                        

    @rule()
    def start_list(self):
        self.whitespace(max=3)
        with self.choice():
            with self.case():
                self.range('-', '*', '+') 
            with self.case():
                with self.repeat(min=1, max=9): self.range("0-9")
                self.range(".", ")")

        with self.choice():
            with self.case(), self.lookahead():
                self.whitespace()
                self.end_of_line()
            with self.case():
                self.whitespace(min=1, max=1, newline=True)

    @rule()
    def list_interrupts(self):
        with self.choice():
            with self.case(): self.thematic_break()
            with self.case(): self.atx_heading()
            with self.case(): self.start_fenced_block()
            with self.case(): self.start_blockquote()
            with self.case():
                self.start_list()


    @rule()
    def list_item(self):
        with self.choice():
            with self.case():
                with self.lookahead():
                    self.whitespace(min=4, max=4)
                    with self.reject():
                        self.line_end()
            with self.case():
                with self.lookahead():
                    self.start_fenced_block()
            
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
                    self.indent()
                self.whitespace(min=1, max=1)

        c = self.column(from_prefix=True)
        with self.list_interrupts.as_dedent(count=c):
            self.block_element()
        with self.repeat():
            with self.list_interrupts.as_dedent(count=c):
                self.indent(partial=True)
                print('??')
                with self.optional():
                    with self.repeat():
                        self.whitespace()
                        with self.capture_node("empty"):
                            self.newline()
                        self.indent()
                    with self.lookahead():
                        self.whitespace()
                        self.range("\n", invert=True)
            with self.list_interrupts.as_dedent(count=c):
                self.block_element()

    @rule()
    def unordered_list(self):
        with self.reject():
            self.thematic_break()
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
                self.indent()
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.newline()
                        with self.capture_node('empty'), self.repeat():
                            self.indent()
                            self.whitespace()
                            self.newline()
                        with self.lookahead():
                            self.indent()
                            self.whitespace(max=3)
                            self.literal(delimiter)
                    with self.case():
                        with self.reject():
                            self.thematic_break()
                        self.whitespace(max=3)

                        self.literal(delimiter)

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
    def ordered_list(self):
        with self.capture_node("ordered_list"):
            self.whitespace(max=3)
            with self.capture_node('ordered_list_start'):
                with self.repeat(min=1, max=9):
                    self.range('0-9')
            with self.backref() as delimiter:
                self.range('.',')')

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
                self.indent()
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.newline()
                        with self.capture_node('empty'), self.repeat():
                            self.indent()
                            self.whitespace()
                            self.newline()
                        with self.lookahead():
                            self.indent()
                            self.whitespace(max=3)
                            with self.repeat(min=1, max=9):
                                self.range('0-9')
                            self.literal(delimiter)
                    with self.case():
                        self.whitespace(max=3)

                        with self.repeat(min=1, max=9):
                            self.range('0-9')

                        self.literal(delimiter)

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

    # para 

    @rule()
    def para_interrupt(self):
        with self.choice():
            with self.case(): self.thematic_break()
            with self.case(): self.atx_heading()
            with self.case(): self.start_fenced_block()
            with self.case(): self.start_blockquote()
            with self.case():
                self.whitespace(max=3)
                with self.choice():
                    with self.case():
                        self.range('-', '*', '+') 
                    with self.case():
                        self.literal("1")
                        self.range(".", ")")
                self.whitespace(min=1)
                with self.reject():
                    self.whitespace()
                    self.end_of_line()
            
    @rule()
    def linebreak(self):
        with self.choice():
            with self.case():
                with self.choice():
                    with self.case(): self.whitespace(min=2)
                    with self.case(): self.literal("\\")
                with self.capture_node("hardbreak"):
                    self.newline()
            with self.case():
                self.whitespace()
                with self.capture_node("softbreak"):
                    self.newline()

        self.indent(partial=True)
        with self.reject(): 
            self.para_interrupt.inline()
        self.whitespace()
        with self.reject(): 
            self.newline()
    # setext

    @rule()
    def setext_heading_line(self):
        self.whitespace(max=3)
        with self.choice():
            with self.case():
                with self.repeat(min=1):
                    self.literal('=')
                self.capture_value(1)
            with self.case():
                with self.repeat(min=1):
                    self.literal('-')
                self.capture_value(2)
        self.line_end()

    @rule()
    def no_setext_heading_line(self):
        with self.reject():
            self.setext_heading_line()

    @rule()
    def para(self):
        self.whitespace(max=3)
        with self.capture_node("para"):
            with self.no_setext_heading_line.as_indent():
                self.inline_element()

                with self.repeat():
                    with self.choice():
                        with self.case():
                            self.linebreak.inline()
                        with self.case():
                            with self.capture_node("whitespace"):
                                self.whitespace()

                    self.inline_element()
            with self.choice():
                with self.case():
                    with self.optional():
                        self.literal("\\")
                        self.capture_value("\\")

                    self.whitespace()
                    self.newline()
                    self.indent(partial=False)
                    self.setext_heading_line()
                    self.capture_value('setext')
                with self.case():
                    with self.repeat():
                        with self.choice():
                            with self.case():
                                self.linebreak.inline()
                            with self.case():
                                with self.capture_node("whitespace"):
                                    self.whitespace()

                        # 4.1 Ex 27, 28. Thematic Breaks can interrupt a paragraph
                        self.inline_element()

                    self.whitespace()
                    with self.optional():
                        self.literal("\\")
                        self.capture_value("\\")
                    self.end_of_line()
                    self.capture_value('para')

    @rule()
    def inline_element(self):
        with self.choice():
            with self.case():
                self.code_span()

            with self.case():
                self.left_flank()
            with self.case():
                self.right_flank()
            with self.case():
                self.html_entity()
            with self.case():
                self.escaped_text()
            with self.case():
                with self.capture_node('text'):
                    self.range(" ", "\n", "\\", invert=True)
                    with self.repeat(min=0):
                        self.range(" ", "\n", "\\", "<", "`", "*", "_", "&", "[", invert=True)

    @rule()
    def escaped_text(self):
        self.literal("\\")
        with self.reject(): # hardbreaks
            self.newline()
            self.whitespace()
            self.range('\n', invert=True)

        with self.choice():
            with self.case(), self.capture_node("text"):
                self.range("!-/",":-@","[-`","{-~")
            with self.case():
                self.capture_value("\\")

    @rule()
    def html_entity(self):
        self.literal("&");
        with self.choice():
            with self.case():
                self.literal("#")
                with self.capture_node("dec_entity"), self.repeat(min=1, max=7):
                    self.range("0-9")
                self.literal(";")
            with self.case():
                self.literal("#")
                self.range("x","X")
                with self.capture_node("hex_entity"):
                    self.range("0-9", "a-f","A-F")
                    with self.repeat(min=0, max=6):
                        self.range("0-9", "a-f","A-F")
                self.literal(";")
            with self.case():
                with self.capture_node("named_entity"):
                    self.range("a-z","A-Z")
                    with self.repeat(min=1):
                        self.range("0-9","a-z","A-Z")
                self.literal(";")

    @rule()
    def left_flank(self):
        with self.capture_node("left_flank"), self.choice():
            with self.case():
                with self.lookahead(-1):
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range("_", "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                with self.reject():
                    self.range(unicode_whitespace=True)
                self.capture_value(chr)
                self.capture_value(n)

            with self.case():
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range("_", "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                with self.reject():
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                    
    @rule()
    def right_flank(self):
        with self.capture_node("right_flank"), self.choice():
            with self.case():
                with self.reject(-1):
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range("_", "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                self.capture_value(chr)
                self.capture_value(n)

            with self.case():
                with self.reject(-1):
                    self.range(unicode_whitespace=True, unicode_newline=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range("_", "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                with self.lookahead():
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                
    @rule()
    def code_span(self):
        with self.choice():
            with self.case():
                with self.count(char="`") as c, self.repeat(min=1):
                    self.literal("`")
                with self.capture_node('code_span') as span, self.repeat(min=1), self.choice():
                    with self.case():
                        with self.capture_node('text'):
                            self.range("\n", "`", invert=True)
                            with self.repeat(min=0):
                                self.range("\n", "`", invert=True)
                    with self.case():
                        with self.capture_node("text"):
                            self.newline()
                        self.indent(partial=True)
                    with self.case():
                        with self.reject():
                            with self.repeat(min=c, max=c):
                                self.literal("`")
                            with self.choice():
                                with self.case(): self.range('`', invert=True)
                                with self.case(): self.end_of_file()
                        with self.capture_node("text"), self.repeat():
                            self.literal("`")
                with self.repeat(min=c, max=c):
                    self.literal("`")
                with self.reject():
                    self.literal("`")
            with self.case():
                with self.capture_node('text'), self.repeat(min=1):
                    self.literal("`")



## HTML Builder

import html
import html.entities

def html_escape(text):
    return text.replace("&", "&amp;").replace("\"", "&quot;").replace(">", "&gt;").replace("<","&lt;").replace("\x00", "\uFFFD")

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
def indented_code(buf, pos,end, children):
    text = html_escape("".join(children))
    return f"<pre><code>{text}</code></pre>"

@_builder
def partial_indent(buf, pos, end, children):
    width = children[0]
    return " "*width

@_builder
def indented_code_line(buf, pos, end, children):
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
    text = "".join(children)
    text = text.lstrip().split(' ',1)
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

def wrap_loose(list_items, out):
    def wrap(c):
        if not c: return None
        if isinstance(c, tuple):
            return f"<p>{c[0]}</p>"
        return c
    for item in list_items:
        if item == None: continue
        wrapped = [ wrap(line) for line in item]
        _out = []
        for line in item:
            line = wrap(line)
            if line is None:
                if not _out[-1].endswith('\n'):
                    _out.append('\n')
            else:
                _out.append(line)
                if not line[-1].endswith('\n'):
                    _out.append('\n')
        if _out:
            if not _out[0].startswith('\n'): 
                _out.insert(0, '\n') 

            if not _out[-1].endswith('\n'): 
                _out.append('\n') 
        
        out.append(f"<li>{''.join(_out)}</li>\n")
    return out

def wrap_tight(list_items, out):
    def wrap(c):
        if not c: return None
        if isinstance(c, tuple):
            return f"{c[0]}"
        return c if c.endswith('\n') else c+"\n"
    for item in list_items:
        out2=[]
        a_block=False
        for c in item:
            if isinstance(c, tuple):
                out2.append(f"{c[0]}")
                a_block=False
            elif c:
                if not a_block: out2.append('\n')
                out2.append(c)
                out2.append("\n")
                a_block=True
        out.append(f"<li>{''.join(out2)}</li>\n")
    return out

@_builder
def unordered_list(buf, pos,end, list_items):
    out = ["<ul>\n"]

    if loose(list_items) or any(loose(c) for c in list_items if c):
        wrap_loose(list_items, out)
    else:
        wrap_tight(list_items, out)

    out.extend("</ul>")
    return "".join(out)

@_builder
def ordered_list(buf, pos,end, list_items):
    start = list_items.pop(0)
    if start != 1:
        start = f' start="{start}"'
    else:
        start = ''
    out = [f'<ol{start}>\n']

    if loose(list_items) or any(loose(c) for c in list_items if c):
        wrap_loose(list_items, out)
    else:
        wrap_tight(list_items, out)
    out.extend("</ol>")
    return "".join(out)

@_builder
def list_item(buf, pos,end, children):
    return children

@_builder
def ordered_list_start(buf, pos,end, children):
    return int(buf[pos:end])

@_builder
def empty(buf, pos, end, children):
    return None

@_builder
def empty_line(buf, pos, end, children):
    return None

@_builder
def left_flank(buf, pos, end, children):
    return buf[pos:end]

@_builder
def right_flank(buf, pos, end, children):
    return buf[pos:end]


@_builder
def para(buf, pos,end, children):
    kind = children.pop()
    if kind == "setext":
        return f"<h{children[-1]}>{make_para(children[:-1])}</h{children[-1]}>"
    else:
        return (make_para(children),)

@_builder
def code_span(buf, pos, end, children):
    text = "".join(children)
    text = text.replace('\n', ' ')
    if len(text) > 2 and text[0] == text[-1] == " ":
        text = text[1:-1]
    return f"<code>{text}</code>"

@_builder
def text(buf, pos,end, children):
    return html_escape(buf[pos:end])

@_builder
def named_entity(buf, pos,end, children):
    text = buf[pos:end+1] # + ;
    if text in html.entities.html5:
        return html_escape(html.entities.html5[text])
    else:
        return f"&amp;{html_escape(text)}"

@_builder
def hex_entity(buf, pos,end, children):
    text = buf[pos:end]
    return html_escape(chr(int(text,16)))

@_builder
def dec_entity(buf, pos,end, children):
    text = buf[pos:end]
    return html_escape(chr(int(text)))

@_builder
def softbreak(buf, pos,end, children):
    return "\n"

@_builder
def hardbreak(buf, pos,end, children):
    return f"<br />\n"

@_builder
def whitespace(buf, pos, end, children):
    return buf[pos:end]

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
        if '[' in markd: continue
        if '_' in markd: continue
        #if out.replace('\n','') == t['html'].replace('\n',''): continue
        print(t['example'])
        print(repr(markd))
        print('=', repr(t['html']))
        print('X', repr(out))
        print()
        walk(out1)
        print()
print(count, worked, failed)

markup("""
\\
""")
