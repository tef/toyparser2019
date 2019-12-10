from ..grammar import Grammar, compile_python, sibling

class Remarkable(Grammar, start="remark_document", whitespace=[" ", "\t"], newline=["\r", "\n", "\r\n"], tabstop=8):
    @rule(inline=True) # 2.1 line ends by newline or end_of_file
    def line_end(self):
        self.whitespace()
        self.end_of_line()

    # block
    @rule(start="remark_document")
    def remark_document(self):
        with self.optional():
            self.literal("\uFEFF")
        with self.choice():
            with self.case():
                self.end_of_file()
            # with self.case():
            #    self.whitespace(newline=True)
            #    self.inline_directive()
            #    self.whitespace(newline=True)
            #    self.end_of_file()
            with self.case():
                with self.repeat(min=0) as n:
                    self.indent()
                    with self.choice():
                        with self.case(): self.block_element()
                        with self.case(): self.para()
                        with self.case(): self.empty_lines()
                        with self.case(): self.end_of_file()
                self.whitespace(newline=True)
                self.end_of_file()

    @rule(inline=True)
    def empty_lines(self):
        self.whitespace()
        self.newline()
        with self.repeat():
            self.indent()
            self.whitespace()
            self.newline()
        with self.capture_node("remark_empty_line"):
            pass

    # blocks
    @rule()
    def block_element(self):
        with self.choice():
            with self.case():
                self.block_rson()
            with self.case():
                self.code_block()
            with self.case():
                self.atx_heading()
            with self.case():
                self.horizontal_rule()
            with self.case():
                self.begin_end_directive()
            with self.case():
                self.block_directive()
            with self.case():
                self.list_block()
            with self.case():
                self.blockquote()
            with self.case():
                self.table()
            with self.case():
                self.prose_para()

    @rule()
    def paragraph_breaks(self):
        with self.choice():
            with self.case(): self.horizontal_rule()
            with self.case(): self.atx_heading()
            with self.case(): self.start_code_block()
            with self.case(): self.start_list_block()
            with self.case(): self.start_blockquote()
            with self.case(): self.start_table()


    @rule(inline=True)
    def linebreak(self):
        with self.choice():
            with self.case():
                self.whitespace()
                self.literal("\\")
                with self.capture_node("remark_hardbreak"):
                    self.newline()
            with self.case():
                self.whitespace()
                with self.capture_node("remark_softbreak"):
                    self.newline()

        self.indent(partial=True)
        # allow missing indents if no interrupts
        with self.reject():
            self.paragraph_breaks()
        self.whitespace()
        with self.reject(): 
            self.newline()

    @rule()
    def inner_para(self):
        with self.capture_node("remark_whitespace"):
            self.whitespace()
        self.inline_element()

        with self.repeat():
            with self.choice():
                with self.case():
                    self.linebreak()
                with self.case():
                    with self.capture_node("remark_whitespace"):
                        self.whitespace()

            self.inline_element()

        with self.capture_node("remark_whitespace"):
            self.whitespace()
        with self.optional():
            self.literal("\\")
            self.capture_value("\\")



    @rule()
    def para(self):
        with self.capture_node("remark_paragraph"):
            self.inner_para()
        self.end_of_line()

    @rule()
    def rson_identifier(self):
        with self.capture_node('rson_identifier', nested=False):
            self.range("a-z", "A-Z")
            with self.repeat():
                self.range("0-9", "a-z","A-Z","_")

    @rule(inline=True)
    def raw_identifier(self):
        self.range("a-z", "A-Z")
        with self.repeat():
            self.range("0-9", "a-z","A-Z","_")
    @rule()
    def directive_args(self):
        self.whitespace(newline=True)
        with self.optional():
            self.directive_arg()
            self.whitespace()
            with self.repeat(min=0):
                self.literal(",")
                self.whitespace(newline=True)
                self.directive_arg()
                self.whitespace()
            with self.optional():
                self.literal(",")
            self.whitespace(newline=True)

    @rule(inline=True)
    def directive_arg(self):
        with self.capture_node("arg"), self.choice():
            with self.case():
                self.rson_identifier()
                with self.optional():
                    self.whitespace()
                    self.literal(":")
                    self.whitespace(newline=True)
                    self.rson_value()
            with self.case():
                self.rson_string()
                self.whitespace()
                self.literal(":")
                self.whitespace(newline=True)
                self.rson_value()
            with self.case():
                self.rson_value()
    @rule()
    def begin_end_directive(self):
        marker = ["\\", "&"]
        self.whitespace(max=8)
        self.literal(*marker)
        self.literal("begin::")
        with self.capture_node("block_directive"):
            with self.capture_node("directive_name"), self.backref() as name:
                self.rson_identifier()
            with self.variable("fake name") as fence:
                with self.choice():
                    with self.case():
                        self.whitespace()
                        with self.backref() as b:
                            self.raw_identifier()
                        self.set_variable(fence, b)
                        self.whitespace()
                        with self.capture_node("directive_args"), self.optional():
                            self.literal("[", "&[",)
                            self.directive_args()
                            self.literal("]")
                    with self.case():
                        self.whitespace()
                        with self.capture_node("directive_args"), self.optional():
                            self.literal("[", "&[",)
                            self.directive_args()
                            self.literal("]")
                        with self.optional():
                            with self.backref() as b:
                                self.raw_identifier()
                            self.set_variable(fence, b)
                self.whitespace()
                self.line_end()
                with self.capture_node("directive_block"):
                    with self.repeat(min=0) as n:
                        self.indent()
                        with self.reject():
                            self.whitespace(max=8)
                            self.literal(*marker)
                            self.literal("end")
                            with self.optional():
                                self.literal("::")
                                self.literal(name)
                                with self.optional():
                                    self.whitespace()
                                    self.literal(fence)
                            self.line_end()
                        with self.choice():

                            with self.case(): self.block_element()
                            with self.case(): self.para()
                            with self.case(): self.empty_lines()
                with self.choice():
                    # someone else's marker
                    # my marker, diff name
                    with self.case(), self.lookahead():
                        self.whitespace(newline=True)
                        self.end_of_file()
                    with self.case(), self.lookahead():
                        self.indent()
                        self.whitespace(max=8)
                        self.literal(*marker)
                        self.literal("end")
                        self.literal("::")
                        with self.reject():
                            self.literal(name)
                        self.raw_identifier()
                        with self.optional():
                            self.whitespace()
                            self.literal(fence)
                        self.line_end()
                    with self.case(), self.lookahead():
                        self.indent()
                        self.whitespace(max=8)
                        self.literal(*marker)
                        self.literal("end")
                        self.literal("::")
                        self.literal(name)
                        self.whitespace()
                        with self.reject():
                            self.literal(fence)
                        self.raw_identifier()
                        self.line_end()
                    with self.case():
                        self.indent()
                        self.whitespace(max=8)
                        self.literal(*marker)
                        self.literal("end")
                        with self.optional():
                            self.literal("::")
                            self.literal(name)
                            with self.optional():
                                self.whitespace()
                                self.literal(fence)
                        self.line_end()

    @rule()
    def block_directive(self):
        self.whitespace(max=8)
        self.literal("\\", "&")
        with self.reject():
            self.literal("begin", "end")
        with self.capture_node("block_directive"):
            with self.capture_node("directive_name"), self.backref() as name:
                self.raw_identifier()
            with self.capture_node("directive_args"), self.optional():
                self.literal("[")
                self.directive_args()
                self.literal("]")
            with self.choice():
                with self.case():
                    self.literal(";")
                    self.capture_value(None)
                    self.newline()
                with self.case():
                    with self.capture_node('directive_code'): 
                        self.inner_code_block()
                with self.case():
                    with self.count(columns=True) as n, self.repeat(min=3):
                        self.literal("{")
                    self.line_end()
                    with self.capture_node("directive_block"):
                        with self.repeat(min=0):
                            self.indent()
                            with self.reject():
                                self.whitespace(max=8)
                                with self.repeat(max=n, min=n):
                                    self.literal("}")
                                self.line_end()
                            with self.choice():

                                with self.case(): self.block_element()
                                with self.case(): self.para()
                                with self.case(): self.empty_lines()
                    self.indent()
                    self.whitespace(max=8)
                    with self.repeat(max=n, min=n):
                        self.literal("}")
                    self.line_end()
                with self.case():
                    self.literal(":")
                    with self.reject():
                        self.literal(":")
                    with self.choice():
                        with self.case():
                            with self.reject():
                                self.whitespace()
                                self.newline()
                            self.whitespace(min=1)
                            with self.capture_node("directive_para"):
                                self.inner_para()
                            self.end_of_line()
                        with self.case():
                            self.whitespace()
                            self.newline()
                            self.indent()
                            with self.choice():
                                with self.case():
                                    with self.capture_node("directive_list"):
                                        self.inner_list()
                                with self.case():
                                    with self.capture_node("directive_quote"):
                                        self.inner_blockquote()
                                with self.case():
                                    with self.capture_node("directive_prose"):
                                        self.inner_prose_para()
                                with self.case():
                                    with self.capture_node("directive_table"):
                                        self.inner_table()
                                with self.case():
                                    with self.count(columns=True) as c:
                                        self.whitespace(min=1)
                                    with self.indented(count=c), self.capture_node("directive_block"):
                                        with self.choice():
                                            with self.case(): self.block_element()
                                            with self.case(): self.para()
                                            with self.case(): self.empty_lines()
                                        with self.repeat(min=0) as n:
                                            self.indent()
                                            with self.choice():
                                                with self.case(): self.block_element()
                                                with self.case(): self.para()
                                                with self.case(): self.empty_lines()
                        with self.case():
                            self.whitespace()
                            self.newline()
                            with self.capture_node("directive_para"):
                                pass
                with self.case():
                    self.line_end()
                    self.capture_value(None)

    # inlines/paras
            
    @rule(inline=True)
    def inline_directive(self):
        self.literal("\\", "&")
        with self.reject():
            self.literal("begin", "end")
        with self.capture_node("inline_directive"):
            with self.capture_node("directive_name"):
                self.rson_identifier()
            with self.capture_node("directive_args"), self.optional():
                self.literal("[")
                self.directive_args()
                self.literal("]")
            with self.reject():
                self.literal(":")
            with self.optional(), self.choice():
                with self.case():
                    self.literal(";")
                    self.capture_value(None)
                #with self.case():
                #    with self.count(columns=True) as n, self.repeat(min=3):
                #        self.literal("{")
                #    with self.capture_node("directive_span"):
                #        with self.repeat():
                #            self.whitespace(newline=True)
                #            self.inline_directive()
                #            self.whitespace(newline=True)
                #    self.whitespace(newline=True)
                #    with self.repeat(min=n, max=n):
                #        self.literal("}")
                with self.case():
                    with self.count(columns=True) as n, self.repeat(min=1):
                        self.literal("{")

                    with self.capture_node("directive_span"):
                        with self.optional():
                            with self.reject():
                                with self.repeat(min=n, max=n):
                                    self.literal("}")
                            self.inline_element()

                            with self.repeat(min=0):
                                with self.choice():
                                    with self.case():
                                        self.linebreak()
                                    with self.case():
                                        with self.capture_node("remark_whitespace"):
                                            self.whitespace()

                                with self.reject():
                                    with self.repeat(min=n, max=n):
                                        self.literal("}")
                                self.inline_element()
                        with self.repeat(), self.choice():
                            with self.case():
                                self.linebreak()
                            with self.case():
                                with self.capture_node("remark_whitespace"):
                                    self.whitespace()

                    with self.repeat(min=n, max=n):
                        self.literal("}")
                with self.case():
                    with self.capture_node('directive_code_span') as span: 
                        self.inner_code_span()
    @rule() 
    def horizontal_rule(self):
        self.whitespace(max=8)
        with self.capture_node('remark_horizontal_rule'):
            with self.repeat(min=3):
                self.literal("-")
            with self.capture_node("directive_args"), self.optional():
                self.whitespace(min=1)
                self.literal("&[", "[")
                self.directive_args()
                self.literal("]")
        self.line_end()

    @rule()
    def atx_heading_indent(self):
        self.whitespace(max=8)
        with self.repeat(min=1, max=9):
            self.literal("#")

        with self.choice():
            with self.case(): self.whitespace(max=1, min=1)
            with self.case(), self.lookahead(): self.newline()


    @rule()
    def atx_heading(self):
        self.whitespace(max=8)
        with self.variable(0) as num, self.capture_node("remark_heading", value=num):
            with self.count(char='#') as level:
                with self.repeat(min=1, max=9):
                    self.literal("#")
            self.set_variable(num, level)
            with self.capture_node("directive_args"):
                with self.optional():
                    self.whitespace(min=1)
                    self.literal("&[")
                    self.directive_args()
                    self.literal("]")
            with self.choice():
                with self.case():
                    self.line_end()
                with self.case():
                    self.whitespace(min=1)
                    with self.indented(indent=self.atx_heading_indent):
                        self.inner_para()
                    self.end_of_line()
    @rule()
    def start_prose_para(self):
        self.whitespace(max=8)
        self.literal("|")
        with self.choice():
            with self.case(): self.whitespace(max=1, min=1)
            with self.case(), self.lookahead(): 
                self.line_end()

    @rule()
    def prose_para(self):
        with self.capture_node("remark_prose_paragraph"):
            self.inner_prose_para()

    @rule()
    def inner_prose_para(self):
        self.start_prose_para()
        with self.capture_node("directive_args"):
            with self.optional():
                self.whitespace()
                self.literal("&[")
                self.directive_args()
                self.literal("]")
                self.line_end()
                self.start_prose_para()

        with self.indented(count=-1):
            self.inner_para()
        with self.repeat():
            with self.capture_node("remark_prose_hardbreak"):
                self.newline()
            self.indent()
            self.start_prose_para()
            with self.indented(count=-1):
                self.inner_para()
        self.end_of_line()

    @rule()
    def start_code_block(self):
        self.whitespace(max=8)
        self.literal("```")

    @rule()
    def code_block(self):
        with self.count(columns=True) as w:
            self.whitespace(max=8)
        with self.indented(count=w), self.capture_node('remark_code_block'):
            fence = "`"
            with self.count(char=fence) as c, self.repeat(min=3):
                self.literal(fence)
            with self.choice():
                with self.case(), self.capture_node("directive_args"):
                    self.whitespace(min=1)
                    self.literal("&[", "[")
                    self.directive_args()
                    self.literal("]")
                with self.case(), self.capture_node("code_string"):
                    self.whitespace()
                    self.rson_identifier()
                with self.case():
                    self.capture_value(None)

            self.line_end()
            with self.repeat():
                self.indent()
                with self.reject():
                    with self.repeat(min=c):
                        self.literal(fence)
                    self.line_end()
                with self.capture_node('code_text'):
                    with self.repeat(min=0):
                        self.range("\n", invert=True)
                with self.capture_node('code_text'):
                    self.line_end()
            self.indent()
            with self.repeat(min=c):
                self.literal(fence)
            self.whitespace()
            self.line_end()

    @rule()
    def inner_code_block(self):
        with self.indented():
            fence = "`"
            with self.count(char=fence) as c, self.repeat(min=3):
                self.literal(fence)
            self.line_end()
            with self.repeat():
                self.indent()
                with self.reject():
                    with self.repeat(min=c):
                        self.literal(fence)
                    self.line_end()
                with self.capture_node('code_text'):
                    with self.repeat(min=0):
                        self.range("\n", invert=True)
                with self.capture_node('code_text'):
                    self.line_end()
            self.indent()
            with self.repeat(min=c):
                self.literal(fence)
            self.whitespace()
            self.line_end()

    @rule()
    def start_blockquote(self):
        self.whitespace(max=8)
        self.literal('>')
        with self.choice():
            with self.case(): self.whitespace(max=1, min=1)
            with self.case(), self.lookahead():
                self.newline()
    @rule()
    def blockquote(self):
        with self.capture_node("remark_blockquote"):
            self.inner_blockquote()

    @rule()
    def inner_blockquote(self):
        self.start_blockquote()
        with self.capture_node("directive_args"):
            with self.optional():
                self.literal("&[")
                self.directive_args()
                self.literal("] ")
        with self.choice():
            with self.case():
                self.whitespace()
                self.end_of_line()
            with self.case():
                with self.indented(indent=self.start_blockquote, dedent=None): # self.paragraph_breaks):
                    with self.choice():
                        with self.case(): self.block_element()
                        with self.case(): self.para()
        with self.repeat():
            self.indent()
            self.start_blockquote()
            with self.choice():
                with self.case():
                    self.whitespace()
                    self.end_of_line()
                with self.case():
                    with self.indented(indent=self.start_blockquote, dedent=None): # self.paragraph_breaks):
                        with self.choice():
                            with self.case(): self.block_element()
                            with self.case(): self.para()
                        

    @rule()
    def start_list_block(self):
        self.whitespace(max=8)
        self.literal("*", "-")
        with self.choice():
            with self.case(), self.lookahead():
                self.whitespace()
                self.end_of_line()
            with self.case():
                self.whitespace(min=1, max=1, newline=True)


    @rule()
    def group_item(self):
        with self.variable('tight') as spacing:
            with self.capture_node('item_spacing', value=spacing):
                pass

            with self.choice():
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
                    self.set_variable(spacing, 'loose')

            with self.choice():
                with self.case():
                    self.block_element()
                    self.set_variable(spacing, 'loose')
                with self.case(): self.para()


            with self.repeat():
                self.indent()
                with self.optional():
                    with self.repeat(min=1):
                        self.whitespace()
                        self.newline()
                        self.indent()
                    with self.lookahead():
                        self.whitespace()
                        self.range("\n", invert=True)
                with self.choice():
                    with self.case(): self.block_element()
                    with self.case(): self.para()
                self.set_variable(spacing, 'loose')

    @rule()
    def inner_list(self):
        with self.variable('tight') as spacing:
            with self.count(columns=True) as w:
                with self.count(columns=True) as i:
                    self.whitespace(max=8)
                with self.capture_node('item_marker'), self.backref() as marker:
                    self.literal("--", "-")
            with self.capture_node('list_spacing', value=spacing):
                pass


            with self.choice():
                with self.case(), self.lookahead():
                    self.whitespace()
                    self.end_of_line()
                with self.case():
                    self.whitespace(min=1, max=1, newline=True)

            with self.capture_node("remark_item"):
                with self.capture_node("directive_args"):
                    with self.optional():
                        self.literal("&[")
                        self.directive_args()
                        self.literal("] ")
                with self.choice():
                    with self.case():
                        with self.indented(count=1, dedent=self.paragraph_breaks), self.indented(count=w, dedent=self.paragraph_breaks):
                            self.group_item()
                    with self.case():
                        self.whitespace()
                        self.end_of_line()
                        with self.capture_node('item_spacing', value='tight'):
                            pass

            with self.repeat():
                self.indent()
                with self.optional():
                    self.whitespace()
                    self.newline()
                    self.indent()
                    with self.lookahead():
                        self.whitespace(min=i, max=i)
                        self.literal(marker)
                    self.set_variable(spacing, 'loose')

                self.whitespace(min=i, max=i)
                self.literal(marker)
                with self.choice():
                    with self.case(), self.lookahead():
                        self.whitespace()
                        self.end_of_line()
                    with self.case():
                        self.whitespace(min=1, max=1, newline=True)

                with self.capture_node("remark_item"):
                    with self.capture_node("directive_args"):
                        with self.optional():
                            self.literal("&[")
                            self.directive_args()
                            self.literal("] ")
                    with self.choice():
                        with self.case():
                            with self.indented(count=1, dedent=self.paragraph_breaks):
                                with self.indented(count=w, dedent=self.paragraph_breaks):
                                    self.group_item()
                        with self.case():
                            self.whitespace()
                            self.end_of_line()
                            with self.capture_node('item_spacing', value='tight'):
                                pass

    @rule()
    def list_block(self):
        with self.capture_node('remark_list'):
            self.inner_list()


    @rule()
    def start_table(self):
        self.whitespace(max=8)
        self.literal("|")


    @rule()
    def table_cell(self):
        with self.capture_node("table_cell"):
            with self.choice():
                with self.case(), self.lookahead():
                    self.literal("|")
                with self.case():
                    with self.reject():
                        self.literal("|")
                    with self.indented(count=-1):
                        self.inline_element()
                        with self.repeat():
                            with self.capture_node("remark_whitespace"):
                                self.whitespace()
                            with self.reject():
                                self.literal("|")
                            self.inline_element()

    @rule()
    def table(self):
        with self.capture_node('table'):
            self.inner_table()


    @rule()
    def inner_table(self):
        with self.count(columns=True) as c:
            self.whitespace(max=8)
        with self.indented(count=c):
            with self.variable(0) as rows:
                with self.capture_node('table_header'):
                    with self.repeat(min=1) as c:
                        self.literal("|")
                        self.whitespace()
                        self.table_cell()
                        self.whitespace()
                    with self.optional():
                        self.literal("|")
                        self.whitespace()
                    self.newline()
                
                self.indent()

                with self.capture_node('table_header_rule'):
                    with self.repeat(min=c, max=c):
                        self.literal("|")
                        self.whitespace()
                        with self.capture_node("column_align"):
                            with self.optional(): self.literal(":")
                            with self.repeat(min=1): self.literal("-")
                            with self.optional(): self.literal(":")
                        self.whitespace()
                    with self.optional():
                        self.literal("|")
                        self.whitespace()
                    self.newline()
            with self.repeat():
                self.indent()
                with self.capture_node("table_row"):
                    with self.repeat(min=1,max=c):
                        self.literal("|")
                        self.whitespace()
                        self.table_cell()
                        self.whitespace()
                    with self.optional():
                        self.literal("|")
                        self.whitespace()
                    self.newline()
            
    @rule()
    def inline_element(self):
        with self.choice():
            with self.case():
                self.literal("\\")
                with self.capture_node("remark_nbsp"):
                    self.whitespace(min=1)
            with self.case():
                self.literal("\\")
                with self.capture_node("remark_text"):
                    self.range("*", "_","!-/",":-@","[-`","{-~")
                    # self.range(" ", "\t", "\n", invert=True)
            with self.case():
                self.literal(":")
                with self.capture_node("remark_emoji"):
                    self.rson_identifier()
                self.literal(":")
            with self.case():
                self.literal("&")
                with self.optional(): self.literal("#")
                self.literal('0x', "x")
                with self.capture_node("remark_hex_codepoint"):
                    with self.repeat(min=1):
                        self.range("0-9")
                with self.choice():
                    with self.case():
                        self.literal(";")
                    with self.case(), self.reject():
                        self.raw_identifier()
            with self.case():
                self.literal("&")
                with self.optional():
                    self.literal('#')
                with self.reject():
                    self.literal('0x','x')
                with self.capture_node("remark_codepoint"):
                    with self.repeat(min=1):
                        self.range("0-9")
                with self.choice():
                    with self.case():
                        self.literal(";")
                    with self.case(), self.reject():
                        self.raw_identifier()
            with self.case():
                self.inline_directive()
            with self.case():
                self.inline_span()
            with self.case():
                self.code_span()
            with self.case():
                self.word.inline()

    @rule()
    def word(self):
        with self.capture_node('remark_text'):
            self.range(" ", "\n", "\\", "&", invert=True)
            with self.repeat(min=0):
                with self.choice():
                    with self.case():
                        self.range(" ", "\n", "`", "_", "*", "~", "\\", "}",invert=True)
                    with self.case():
                        with self.repeat(min=1): 
                            self.literal("_") 
                        with self.reject():
                            self.whitespace(newline=True)

    @rule()
    def inline_span(self):
        with self.variable('') as fence, self.capture_node('remark_paragraph_span', value=fence):
            with self.count(columns=True) as n:
                with self.backref() as chr:
                    self.range("_", "*", "~")
                with self.repeat(min=0):
                    self.literal(chr)
                with self.reject():
                    self.whitespace(newline=True, min=1)
                self.set_variable(fence, chr)

            self.inline_element()

            with self.repeat(min=0):
                with self.choice():
                    with self.case():
                        self.linebreak()
                    with self.case():
                        with self.capture_node("remark_whitespace"):
                            self.whitespace()

                with self.reject():
                    with self.repeat(min=n, max=n):
                        self.literal(fence)
                self.inline_element()

            with self.choice():
                with self.case():
                    self.linebreak()
                with self.case():
                    with self.capture_node("remark_whitespace"):
                        self.whitespace()
            with self.repeat(min=n, max=n):
                self.literal(fence)
            with self.capture_node("directive_args"), self.optional():
                self.literal("&[", "[")
                self.directive_args()
                self.literal("]")
    @rule()
    def inner_code_span(self):
        with self.count(char="`") as c, self.repeat(min=1):
            self.literal("`")
        with self.reject():
            self.whitespace()
            self.newline()
        with self.repeat(min=1), self.choice():
            with self.case():
                with self.capture_node('remark_text'):
                    self.range("\n", "`", invert=True)
                    with self.repeat(min=0):
                        self.range("\n", "`", invert=True)
            with self.case():
                self.newline()
                self.indent(partial=True)
            with self.case():
                with self.reject():
                    with self.repeat(min=c, max=c):
                        self.literal("`")
                    with self.choice():
                        with self.case(): self.range('`', invert=True)
                        with self.case(): self.end_of_file()
                with self.capture_node("remark_text"), self.repeat():
                    self.literal("`")
        with self.repeat(min=c, max=c):
            self.literal("`")
        with self.reject():
            self.literal("`")
    @rule()
    def code_span(self):
        with self.capture_node('remark_code_span') as span: 
            self.inner_code_span()
            with self.capture_node("directive_args"), self.optional():
                self.literal("&[", "[")
                self.directive_args()
                self.literal("]")

    @rule()
    def block_rson(self):
        with self.capture_node('block_rson'):
            self.literal('@')
            self.rson_identifier()
            self.literal(' ')
            self.rson_literal()
            self.line_end()

    # rson

    @rule()
    def rson_value(self):
        with self.choice():
            with self.case():
                with self.capture_node('rson_tagged'):
                    self.literal('@')
                    self.rson_identifier()
                    self.literal(' ')
                    self.rson_literal()
            with self.case():
                self.rson_literal.inline()

    @rule()
    def rson_literal(self):
        with self.choice():
            with self.case(): self.rson_list.inline()
            with self.case(): self.rson_object.inline()
            with self.case(): self.rson_string.inline()
            with self.case(): self.rson_number.inline()
            with self.case(): self.rson_true.inline()
            with self.case(): self.rson_false.inline()
            with self.case(): self.rson_null.inline()
            with self.case(): self.inline_directive()

    @rule(inline=True)
    def rson_comment(self):
        with self.repeat(min=0):
            self.whitespace()
            self.literal("#")
            with self.repeat(min=0):
                self.range("\n", invert=True)
            self.newline()
        self.whitespace(newline=True)

    @rule()
    def rson_list(self):
        self.literal("[")
        self.rson_comment.inline()
        with self.capture_node("rson_list"), self.repeat(max=1):
            self.rson_value()
            with self.repeat(min=0):
                self.rson_comment.inline()
                self.literal(",")
                self.rson_comment.inline()
                self.rson_value()
            self.rson_comment.inline()
            with self.optional():
                self.literal(",")
                self.rson_comment.inline()
        self.literal("]")

    @rule()
    def rson_key(self):
        with self.choice():
            with self.case(): self.rson_string()
            with self.case(): self.rson_identifier()
    @rule()
    def rson_pair(self):
        with self.capture_node("rson_pair"):
            self.rson_key()
            self.rson_comment.inline()
            self.literal(":")
            self.rson_comment.inline()
            self.rson_value()

    @rule()
    def rson_object(self):
        self.literal("{")
        self.rson_comment.inline()
        with self.capture_node("rson_object"), self.optional():
            self.rson_pair()
            self.rson_comment.inline()
            with self.repeat(min=0):
                self.literal(",")
                self.rson_comment.inline()
                self.rson_pair()
                self.rson_comment.inline()
            with self.optional():
                self.literal(",")
                self.rson_comment.inline()
        self.literal("}")

    rson_true = rule(literal("true"), capture="rson_bool")
    rson_false = rule(literal("false"), capture="rson_bool")
    rson_null = rule(literal("null"), capture="rson_null")

    @rule()
    def rson_number(self):
        with self.capture_node("rson_number", nested=False), self.choice():
            with self.case():
                with self.optional():
                    self.range("-", "+")
                self.literal("0x")
                self.range("0-9", "A-F", "a-f")
                with self.repeat():
                    self.range("0-9","A-F","a-f","_")
                # hexfloat?
            with self.case():
                with self.optional():
                    self.range("-", "+")
                self.literal("0o")
                self.range("0-8",)
                with self.repeat():
                    self.range("0-8","_")
            with self.case():
                with self.optional():
                    self.range("-", "+")
                self.literal("0b")
                self.range("0-1",)
                with self.repeat():
                    self.range("0-1","_")
            with self.case():
                with self.optional():
                    self.range("-", "+")
                with self.choice():
                    with self.case():
                        self.literal("0")
                    with self.case():
                        self.range("1-9")
                        with self.repeat():
                            self.range("0-9")
                with self.optional():
                    self.literal(".")
                    with self.repeat():
                        self.range("0-9")
                with self.optional():
                    self.literal("e", "E")
                    with self.optional():
                        self.literal("+", "-")
                        with self.repeat():
                            self.range("0-9")

    @rule()
    def rson_string(self):
        with self.choice():
            with self.case():
                self.literal("\"")
                with self.capture_node("rson_string", nested=False), self.repeat(), self.choice():
                    with self.case():
                        self.range("\x00-\x1f", "\\", "\"", "\uD800-\uDFFF", invert=True)
                    with self.case():
                        self.literal("\\x")
                        with self.reject():
                            self.range('0-1')
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                    with self.case():
                        self.literal("\\u")
                        with self.reject():
                            self.literal("000")
                            self.range('0-1')
                        with self.reject():
                            self.literal("D", "d")
                            self.range("8-9", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                    with self.case():
                        self.literal("\\U")
                        with self.reject():
                            self.literal("0000000")
                            self.range('0-1')
                        with self.reject():
                            self.literal("0000")
                            self.literal("D", "d")
                            self.range("8-9", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                    with self.case():
                        self.literal("\\")
                        self.range(
                            "\"", "\\", "/", "b", 
                            "f", "n", "r", "t", "'", "\n",
                        )
                self.literal("\"")
            with self.case():
                self.literal("\'")
                with self.capture_node("rson_string", nested=False), self.repeat(), self.choice():
                    with self.case():
                        self.range("\x00-\x1f", "\\", "\'", "\uD800-\uDFFF", invert=True)
                    with self.case():
                        self.literal("\\x")
                        with self.reject():
                            self.range('0-1')
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                    with self.case():
                        self.literal("\\u")
                        with self.reject():
                            self.literal("00")
                            self.range('0-1')
                        with self.reject():
                            self.literal("D", "d")
                            self.range("8-9", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                    with self.case():
                        self.literal("\\U")
                        with self.reject():
                            self.literal("000000")
                            self.range('0-1')
                        with self.reject():
                            self.literal("0000")
                            self.literal("D", "d")
                            self.range("8-9", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                    with self.case():
                        self.literal("\\")
                        self.range(
                            "\"", "\\", "/", "b", 
                            "f", "n", "r", "t", "'", "\n",
                        )
                self.literal("\'")

if __name__ == "__main__":
    import subprocess
    import os.path


    filename = sibling(__file__, "RemarkableParser.py")
    code = compile_python(Remarkable, cython=False)

    with open(filename, "w") as fh:
        fh.write(code)

    filename = sibling(__file__, "RemarkableParser.pyx")
    code = compile_python(Remarkable, cython=True)

    with open(filename, "w") as fh:
        fh.write(code)

    subprocess.run(f"python3 `which cythonize` -i {filename}", shell=True).check_returncode()
