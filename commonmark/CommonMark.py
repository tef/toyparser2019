from grammar import Grammar, compile_python

import codecs

def walk(node, indent="- "):
    if (node.name == "value"):
        print(indent, node, node.value)
    else:
        print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")

def unescape(string):
    return codecs.decode(string, 'unicode_escape')

class CommonMark(Grammar, capture="document", whitespace=[" ", "\t"], newline=["\n"], tabstop=4):
    version = 0.29
    @rule(start="document")
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
        html_block |
        indented_code_block | 
        tilde_code_block |
        backtick_code_block |
        blockquote | 
        atx_heading |  
            # 4.1 Ex 29. Headers take precidence over thematic breaks
        thematic_break |  
            # 4.1 Ex 30. Thematic Breaks take precidence over lists
        # Link reference_definiton
        ordered_list |
        unordered_list |
        link_definition | 
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
        with self.variable(0) as num, self.capture_node("atx_heading", value=num):
            with self.count(char='#') as level:
                with self.repeat(min=1, max=6):
                    self.literal("#")
            self.set_variable(num, level)
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

            with self.capture_node('partial_indent'): self.partial_tab()

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
                        with self.capture_node('partial_indent'): self.partial_tab()

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
                with self.capture_node('text'), self.repeat(min=0):
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
                with self.capture_node('text'), self.repeat(min=0):
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
            with self.case(): self.start_html_block()

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
            with self.case(): self.start_html_block()
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



    ## lnk def
            
    @rule(inline=True)
    def link_url_spaces(self):
        with self.choice():
            with self.case():
                self.literal("<")
                with self.capture_node("link_url"):
                    with self.repeat(), self.choice():
                        with self.case():
                            self.literal("\\>", "\\>")
                        with self.case(): self.range(">", "<", "\n", invert=True)
                self.literal(">")
                self.whitespace()
            with self.case():
                with self.capture_node("link_url"):
                    with self.reject(): self.literal("<",)
                    self.balanced_list_url_spaces()

    @rule(inline=True)
    def balanced_list_url_spaces(self):
        with self.repeat():
            with self.repeat():
                with self.choice():
                    with self.case():
                        self.literal("\\(", "\\)")
                    with self.case():
                        self.range(")", "(", "\n",  " ", invert=True)
                    with self.case():
                        self.whitespace()
                        with self.reject():
                            self.end_of_line()
            with self.repeat():
                self.literal("(")
                self.balanced_list_url_spaces()
                self.literal(")")

    @rule()
    def link_definition(self):
        with self.capture_node("link_def"):
            self.whitespace(max=3)
            self.literal("[")
            with self.reject():
                self.whitespace()
                self.literal("]")
            with self.capture_node("link_name"):
                with self.repeat(min=1), self.choice():
                    with self.case():
                        self.literal("\\[", "\\]")
                    with self.case():
                        self.range("[", "]", invert=True)
            self.literal("]")
            self.literal(":")
            with self.choice():
                with self.case():
                    self.whitespace()
                    self.newline()
                    self.indent(partial=True)
                    self.whitespace()
                    with self.reject(): self.newline()
                    self.link_url_spaces()
                with self.case():
                    self.whitespace()
                    with self.reject(): self.newline()
                    self.link_url()
            with self.optional():
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.newline()
                        self.indent(partial=True)
                        self.whitespace()
                        with self.reject(): self.newline()
                    with self.case(): self.whitespace(min=1)
                self.link_title()
                with self.lookahead():
                    self.whitespace()
                    self.newline()
                with self.repeat():
                    self.whitespace()
                    self.newline()
                    self.indent(partial=True)
                    self.whitespace()
                    with self.reject(): self.newline()
                    self.link_title()
                    with self.lookahead():
                        self.whitespace()
                        self.newline()
        self.whitespace()
        self.newline()

    ## html

    html_block = rule(
            html_block_type_1 |
            html_block_type_2 |
            html_block_type_3 |
            html_block_type_4 |
            html_block_type_5 |
            html_block_type_6 |
            html_block_type_7 
    )

    @rule()
    def start_html_block(self):
        self.whitespace(max=3)
        with self.choice():
            with self.case():
                self.literal("<script", "<pre", "<style", transform="lower")
            with self.case():
                self.literal("<?", "<![CDATA[")
            with self.case():
                self.literal("<!")
                self.range("A-Z")
            with self.case():
                self.literal("</", "<")
                self.literal(*"address,article,aside,base,basefont,blockquote,body,caption,center,col,colgroup,dd,details,dialog,dir,div,dl,dt,fieldset,figcaption,figure,footer,form,frame,frameset,h1,h2,h3,h4,h5,h6,head,header,hr,html,iframe,legend,li,link,main,menu,menuitem,nav,noframes,ol,optgroup,option,p,param,section,source,summary,table,tbody,td,tfoot,th,thead,title,tr,track,ul".split(","), transform="lower")
                with self.lookahead(), self.choice():
                    with self.case(): self.whitespace(min=1)
                    with self.case(): self.literal(">")
                    with self.case(): self.end_of_line()


    @rule()
    def html_block_type_1(self):
        with self.capture_node('html_block'):
            with self.capture_node('raw'):
                self.whitespace(max=3)
                self.literal("<script", "<pre", "<style", transform="lower")
                with self.lookahead(), self.choice():
                    with self.case(): self.whitespace(min=1)
                    with self.case(): self.literal(">")
                    with self.case(): self.end_of_line()
                with self.repeat():
                    with self.reject(): self.literal("</script>", "</pre>", "</style>", transform="lower")
                    self.range("\n", invert=True)

            with self.repeat():
                with self.capture_node('raw'): self.newline()
                self.indent(partial=False)
                with self.reject():
                    self.whitespace()
                    self.end_of_file()
                with self.capture_node('raw'):
                    with self.repeat():
                        with self.reject(): self.literal("</script>", "</pre>", "</style>", transform="lower")
                        self.range("\n", invert=True)

            with self.choice():
                with self.case():
                    with self.capture_node('raw'):
                        self.literal("</script>", "</pre>", "</style>", transform="lower")
                        with self.repeat(): self.range("\n", invert=True)
                    self.newline()
                with self.case():
                    with self.capture_node('raw'):
                        with self.repeat():
                            with self.reject(): self.literal("</script>", "</pre>", "</style>", transform="lower")
                            self.range("\n", invert=True)
                    self.end_of_line()
    @rule()
    def html_block_type_2(self):
        with self.capture_node('html_block'):
            with self.capture_node('raw'):
                self.whitespace(max=3)
                self.literal("<!--")
                with self.repeat():
                    with self.reject(): self.literal("-->")
                    self.range("\n", invert=True)

            with self.repeat():
                with self.capture_node('raw'): self.newline()
                self.indent(partial=False)
                with self.reject():
                    self.whitespace()
                    self.end_of_file()
                with self.capture_node('raw'):
                    with self.repeat():
                        with self.reject(): self.literal("-->")
                        self.range("\n", invert=True)

            with self.choice():
                with self.case():
                    with self.capture_node('raw'):
                        self.literal("-->")
                        with self.repeat(): self.range("\n", invert=True)
                    self.newline()
                with self.case():
                    with self.capture_node('raw'):
                        with self.repeat():
                            with self.reject(): self.literal("-->")
                            self.range("\n", invert=True)
                    self.end_of_line()
    @rule()
    def html_block_type_3(self):
        with self.capture_node('html_block'):
            with self.capture_node('raw'):
                self.whitespace(max=3)
                self.literal("<?")
                with self.repeat():
                    with self.reject(): self.literal("?>")
                    self.range("\n", invert=True)

            with self.repeat():
                with self.capture_node('raw'): self.newline()
                self.indent(partial=False)
                with self.reject():
                    self.whitespace()
                    self.end_of_file()
                with self.capture_node('raw'):
                    with self.repeat():
                        with self.reject(): self.literal("?>")
                        self.range("\n", invert=True)

            with self.choice():
                with self.case():
                    with self.capture_node('raw'):
                        self.literal("?>")
                        with self.repeat(): self.range("\n", invert=True)
                    self.newline()
                with self.case():
                    with self.capture_node('raw'):
                        with self.repeat():
                            with self.reject(): self.literal("?>")
                            self.range("\n", invert=True)
                    self.end_of_line()
    @rule()
    def html_block_type_4(self):
        with self.capture_node('html_block'):
            with self.capture_node('raw'):
                self.whitespace(max=3)
                self.literal("<!")
                self.range("A-Z")
                with self.repeat():
                    with self.reject(): self.literal(">")
                    self.range("\n", invert=True)

            with self.repeat():
                with self.capture_node('raw'): self.newline()
                self.indent(partial=False)
                with self.reject():
                    self.whitespace()
                    self.end_of_file()
                with self.capture_node('raw'):
                    with self.repeat():
                        with self.reject(): self.literal(">")
                        self.range("\n", invert=True)

            with self.choice():
                with self.case():
                    with self.capture_node('raw'):
                        self.literal(">")
                        with self.repeat(): self.range("\n", invert=True)
                    self.newline()
                with self.case():
                    with self.capture_node('raw'):
                        with self.repeat():
                            with self.reject(): self.literal(">")
                            self.range("\n", invert=True)
                    self.end_of_line()
    @rule()
    def html_block_type_5(self):
        with self.capture_node('html_block'):
            with self.capture_node('raw'):
                self.whitespace(max=3)
                self.literal("<![CDATA[")
                with self.repeat():
                    with self.reject(): self.literal("]]>")
                    self.range("\n", invert=True)

            with self.repeat():
                with self.capture_node('raw'): self.newline()
                self.indent(partial=False)
                with self.reject():
                    self.whitespace()
                    self.end_of_file()
                with self.capture_node('raw'):
                    with self.repeat():
                        with self.reject(): self.literal("]]>")
                        self.range("\n", invert=True)

            with self.choice():
                with self.case():
                    with self.capture_node('raw'):
                        self.literal("]]>")
                        with self.repeat(): self.range("\n", invert=True)
                    self.newline()
                with self.case():
                    with self.capture_node('raw'):
                        with self.repeat():
                            with self.reject(): self.literal("]]>")
                            self.range("\n", invert=True)
                    self.end_of_line()
    @rule()
    def html_block_type_6(self):
        with self.capture_node('html_block'):
            with self.capture_node('raw'):
                self.whitespace(max=3)
                self.literal("</", "<")
                self.literal(*"address,article,aside,base,basefont,blockquote,body,caption,center,col,colgroup,dd,details,dialog,dir,div,dl,dt,fieldset,figcaption,figure,footer,form,frame,frameset,h1,h2,h3,h4,h5,h6,head,header,hr,html,iframe,legend,li,link,main,menu,menuitem,nav,noframes,ol,optgroup,option,p,param,section,source,summary,table,tbody,td,tfoot,th,thead,title,tr,track,ul".split(","), transform="lower")
                with self.lookahead(), self.choice():
                    with self.case(): self.whitespace(min=1)
                    with self.case(): self.literal(">")
                    with self.case(): self.end_of_line()
                with self.repeat():
                    self.range("\n", invert=True)

            with self.repeat():
                with self.capture_node('raw'): self.newline()
                self.indent(partial=False)
                with self.reject():
                    self.whitespace()
                    self.end_of_line()
                with self.capture_node('raw'):
                    with self.repeat():
                        self.range("\n", invert=True)

            with self.choice():
                with self.case():
                    self.newline()
                    self.indent(partial=False)
                    self.whitespace()
                    self.end_of_line()
                with self.case():
                    self.end_of_line()
                    with self.reject():
                        self.indent(partial=False)
                with self.case():
                    self.end_of_line()
                    self.end_of_file()
    @rule()
    def html_block_type_7(self):
        with self.capture_node('html_block'):
            with self.capture_node('raw'):
                self.whitespace(max=3)
                self.literal("<")
                with self.reject():
                    self.literal("pre", "script", "style", transform="lower")
                with self.choice():
                    with self.case():
                        self.literal("/")
                        self.range("a-z", "A-Z")
                        with self.repeat():
                            self.range("a-z", "A-Z", "-", "0-9")
                        self.whitespace()
                        self.literal(">")
                        self.whitespace()
                    with self.case():
                        self.range("a-z", "A-Z")
                        with self.repeat():
                            self.range("a-z", "A-Z", "-", "0-9")
                        with self.repeat():
                            self.whitespace(min=1)
                            self.range("a-z", "A-Z", ":", "_")
                            with self.repeat(min=1):
                                self.range("a-z", "A-Z", ":", "_", "0-9", "-")
                            with self.optional():
                                self.whitespace()
                                self.literal("=")
                                self.whitespace()
                                with self.choice():
                                    with self.case():
                                        with self.repeat(min=1):
                                            self.range("\"", "'", "=", "<", ">", "`", "\t", " ", "\n", "\r", invert=True)
                                    with self.case():
                                        self.literal("\"")
                                        with self.repeat(): self.range('"',"\n",  invert=True)
                                        self.literal("\"")
                                    with self.case():
                                        self.literal('\'')
                                        with self.repeat(): self.range("'","\n", invert=True)
                                        self.literal('\'')
                        self.whitespace()
                        self.literal(">", "/>")
                        self.whitespace()
                

            with self.repeat():
                with self.capture_node('raw'): self.newline()
                self.indent(partial=False)
                with self.reject():
                    self.whitespace()
                    self.end_of_line()
                with self.capture_node('raw'):
                    with self.repeat():
                        self.range("\n", invert=True)

            with self.choice():
                with self.case():
                    self.newline()
                    self.indent(partial=False)
                    self.whitespace()
                    self.newline()
                with self.case():
                    self.end_of_line()
                    with self.reject():
                        self.indent(partial=False)
                with self.case():
                    self.end_of_line()
                    self.end_of_file()


    @rule()
    def para_interrupt(self):
        with self.choice():
            with self.case(): self.thematic_break()
            with self.case(): self.atx_heading()
            with self.case(): self.start_fenced_block()
            with self.case(): self.start_blockquote()
            with self.case(): self.start_html_block()
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
            with self.case():
                with self.repeat(min=1):
                    self.literal('-')
        self.line_end()

    @rule()
    def no_setext_heading_line(self):
        with self.reject():
            self.setext_heading_line()

    @rule()
    def para(self):
        self.whitespace(max=3)
        with self.variable("para") as kind, self.variable(0) as level, self.capture_node(kind, value=level):
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

                    self.whitespace(max=3)
                    with self.choice():
                        with self.case():
                            with self.repeat(min=1):
                                self.literal('=')
                            self.set_variable(level, 1)
                        with self.case():
                            with self.repeat(min=1):
                                self.literal('-')
                            self.set_variable(level, 2)
                    self.line_end()
                    self.set_variable(kind, 'setext')
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

    @rule()
    def inline_element(self):
        with self.choice():
            with self.case():
                self.link_operator()
            with self.case():
                self.inline_html()
            with self.case():
                self.literal("<")
                with self.capture_node('auto_link'):
                    self.range("a-z","A-Z")
                    with self.repeat(min=1):
                        self.range("a-z","A-Z", "0-9","+",".","-")
                    self.literal(":")
                    with self.repeat():
                        self.range("\x00- ", ">", "<", invert=True)
                self.literal(">")
            with self.case():
                self.literal("<")
                with self.capture_node("mailto_auto_link"):
                    with self.repeat(min=1):
                        self.range(
                            "a-z", "A-Z", "0-9", ".","!",
                            "#", "$", "%", "&", "'", 
                            "*", "+", "/", "=", "?", 
                            "^", "_", "`", "{", "|", "}",
                            "~", "-",
                        )
                    self.literal("@")
                    self.range("a-z", "A-Z", "0-9")
                    with self.optional():
                        with self.repeat(max=62):
                            with self.choice():
                                with self.case(): self.range("a-z", "A-Z", "0-9")
                                with self.case(): 
                                    with self.repeat(min=1): self.literal("-")
                                    self.range("a-z", "A-Z", "0-9")
                    with self.repeat():
                        self.literal(".")
                        self.range("a-z", "A-Z", "0-9")
                        with self.optional():
                            with self.repeat(max=61):
                                with self.choice():
                                    with self.case(): self.range("a-z", "A-Z", "0-9")
                                    with self.case(): 
                                        with self.repeat(min=1): self.literal("-")
                                        self.range("a-z", "A-Z", "0-9")
                self.literal(">")
            with self.case():
                self.code_span()

            with self.case():
                self.dual_flank()
            with self.case():
                # with self.reject(): self.left_flank()
                self.right_flank()
            with self.case():
                # with self.reject(): self.right_flank()
                self.left_flank()
            with self.case():
                self.html_entity()
            with self.case():
                self.escaped_text()
            with self.case():
                with self.capture_node('text'):
                    with self.repeat(min=1): 
                        self.literal("_") 
            with self.case():
                with self.capture_node('text'):
                    with self.repeat(min=1): 
                        self.literal("*") 

            with self.case():
                with self.capture_node('text'):
                    self.range(" ", "\n", "\\", invert=True)
                    with self.repeat(min=0):
                        with self.choice():
                            with self.case():
                                self.range(" ", "\n", "\\", "<", "`", "&", "*", "_", "[", "]", invert=True)
                            with self.case():
                                with self.reject(offset=-1):
                                    self.range(unicode_punctuation=True)
                                with self.reject():
                                    with self.reject():
                                        self.left_flank()
                                    self.right_flank()
                                with self.repeat(min=1): 
                                    self.literal("_") 

    @rule()
    def link_operator(self):
            with self.variable('link') as kind, self.capture_node(kind) as cap:
                with self.optional():
                    self.literal("!")
                    self.set_variable(kind, "image")
                self.literal("[")
                with self.capture_node('link_para'), self.backref() as raw:
                    with self.optional():

                        with self.reject():
                            self.whitespace()
                            self.literal("]")
                        self.inline_element()

                        with self.repeat():
                            with self.choice():
                                with self.case():
                                    self.linebreak.inline()
                                with self.case():
                                    with self.capture_node("whitespace"):
                                        self.whitespace()

                            with self.reject():
                                self.literal("]")
                            self.inline_element()

                    with self.capture_node("whitespace"):
                        self.whitespace()
                self.literal("]")

                with self.choice():
                    with self.case():
                        self.literal("[")
                        self.whitespace()
                        with self.capture_node("link_label"):
                            with self.repeat(min=1), self.choice():
                                with self.case():
                                    self.literal("\\[", "\\]")
                                with self.case():
                                    self.range("[", "]", "\n", invert=True)
                        self.literal("]")
                        with self.reject(): self.literal("[")

                    with self.case():
                        self.literal("(")
                        self.whitespace()
                        self.link_url()

                        with self.optional():
                            self.whitespace()
                            self.link_title()
                        self.whitespace()
                        self.literal(")")
                    with self.case():
                        self.literal('[]')
                        self.capture_value(name="link_label", value=raw)
                    with self.case():
                        with self.reject():
                            self.literal('{', '(', ":")
                        self.capture_value(name="link_label", value=raw)

            
    @rule(inline=True)
    def link_url(self):
        with self.choice():
            with self.case():
                self.literal("<")
                with self.capture_node("link_url"):
                    with self.repeat(), self.choice():
                        with self.case():
                            self.literal("\\>", "\\>")
                        with self.case(): self.range(">", "<", "\n", invert=True)
                self.literal(">")
                self.whitespace()
            with self.case():
                with self.capture_node("link_url"):
                    with self.reject(): self.literal("<", " ")
                    self.balanced_list_url()

    @rule(inline=True)
    def balanced_list_url(self):
        with self.repeat():
            with self.repeat():
                with self.choice():
                    with self.case():
                        self.literal("\\(", "\\)")
                    with self.case():
                        self.range(")", "(", "\n", " ", invert=True)
            with self.repeat():
                self.literal("(")
                self.balanced_list_url()
                self.literal(")")
            

    @rule()
    def link_title(self):
        with self.choice():
            with self.case():
                self.literal('"')
                with self.capture_node("link_title"), self.repeat():
                    with self.choice():
                        with self.case():
                            self.range("\"", "\n", invert=True)
                        with self.case():
                            self.newline()
                            self.indent(partial=True)
                            self.whitespace()
                            with self.reject(): self.newline()

                self.literal('"')
            with self.case():
                self.literal("'")
                with self.capture_node("link_title"), self.repeat():
                    with self.choice():
                        with self.case():
                            self.range("\'", "\n", invert=True)
                        with self.case():
                            self.newline()
                            self.indent(partial=True)
                            self.whitespace()
                            with self.reject(): self.newline()
                self.literal('\'')
            with self.case():
                self.literal("(")
                with self.capture_node("link_title"):
                    self.balanced_list_title()
                self.literal(")")

    @rule()
    def balanced_list_title(self):
        with self.repeat():
            with self.repeat():
                with self.choice():
                    with self.case():
                        self.literal("\\(", "\\)")
                    with self.case():
                        self.range(")", "(", "\n", invert=True)
            with self.repeat():
                self.literal("(")
                self.balanced_list_title()
                self.literal(")")
            


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
                with self.capture_node("html_entity", value="decimal"), self.repeat(min=1, max=7):
                    self.range("0-9")
                self.literal(";")
            with self.case():
                self.literal("#")
                self.range("x","X")
                with self.capture_node("html_entity", value="hex"):
                    self.range("0-9", "a-f","A-F")
                    with self.repeat(min=0, max=6):
                        self.range("0-9", "a-f","A-F")
                self.literal(";")
            with self.case():
                with self.capture_node("html_entity", value="named"):
                    self.range("a-z","A-Z")
                    with self.repeat(min=1):
                        self.range("0-9","a-z","A-Z")
                self.literal(";")

    @rule()
    def left_flank(self):
        with self.capture_node("left_flank"), self.choice():
            with self.case():
                with self.lookahead(offset=-1):
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range("_", "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                with self.reject():
                    self.range(unicode_whitespace=True, unicode_newline=True)
                self.capture_value("left")
                self.capture_value(chr)
                self.capture_value(n)

            with self.case():
                with self.reject(offset=-1):
                    self.range(unicode_punctuation=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range("_", "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                with self.reject():
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                self.capture_value('left')
                self.capture_value(chr)
                self.capture_value(n)
                    
    @rule()
    def right_flank(self):
        with self.capture_node("right_flank"), self.choice():
            with self.case():
                with self.reject(offset=-1):
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range("_", "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                self.capture_value("right")
                self.capture_value(chr)
                self.capture_value(n)

            with self.case():
                with self.reject(offset=-1):
                    self.range(unicode_whitespace=True, unicode_newline=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range("_", "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                with self.lookahead():
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                self.capture_value("right")
                self.capture_value(chr)
                self.capture_value(n)
                
    @rule()
    def dual_flank(self):
        with self.capture_node("dual_flank"), self.choice():
            with self.case():
                with self.lookahead(offset=-1):
                    self.range(unicode_punctuation=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range("_", "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                with self.lookahead():
                    self.range(unicode_punctuation=True)
                self.capture_value("dual")
                self.capture_value(chr)
                self.capture_value(n)

            with self.case():
                with self.reject(offset=-1):
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range( "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                with self.reject():
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                self.capture_value('dual')
                self.capture_value(chr)
                self.capture_value(n)
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

    @rule()
    def inline_html(self):
        with self.choice():
            with self.case():
                with self.capture_node('raw'):
                    self.literal("<?")
                    with self.repeat():
                        with self.reject():
                            self.literal("?>")
                        self.range("\n", invert=True)
                with self.repeat():
                    with self.capture_node('raw'):self.newline()
                    self.indent(partial=True)
                    with self.capture_node('raw'), self.repeat():
                        with self.reject():
                            self.literal("?>")
                        self.range("\n", invert=True)
                with self.capture_node('raw'): self.literal("?>")
            with self.case():
                with self.capture_node('raw'):
                    self.literal("<!--")
                    with self.repeat():
                        with self.reject():
                            self.literal("--", "->", ">", "---")
                        self.range("\n", invert=True)
                with self.repeat():
                    with self.capture_node('raw'):
                        self.newline()
                    self.indent(partial=True)
                    with self.capture_node('raw'):
                        with self.repeat():
                            with self.reject():
                                self.literal("--", "->", ">", "---")
                            self.range("\n", invert=True)
                with self.capture_node('raw'):
                    self.literal("-->")
            with self.case():
                with self.capture_node('raw'):
                    self.literal("<!")
                    self.range("A-Z")
                    with self.repeat():
                        self.range(">", "\n", invert=True)
                with self.repeat():
                    with self.capture_node('raw'):
                        self.newline()
                    self.indent(partial=True)
                    with self.capture_node('raw'):
                        with self.repeat():
                            self.range(">", "\n", invert=True)
                with self.capture_node('raw'):
                    self.literal(">")
            with self.case():
                with self.capture_node('raw'):
                    self.literal("<![CDATA[")
                    with self.repeat():
                        with self.reject():
                            self.literal("]]>")
                        self.range("\n", invert=True)
                with self.repeat():
                    with self.capture_node('raw'):
                        self.newline()
                    self.indent(partial=True)
                    with self.capture_node('raw'):
                        with self.repeat():
                            with self.reject():
                                self.literal("]]>")
                            self.range("\n", invert=True)
                with self.capture_node('raw'):
                    self.literal("]]>")
            with self.case():
                with self.capture_node('raw'):
                    self.literal("<")
                    self.range("a-z", "A-Z")
                    with self.repeat():
                        self.range("a-z", "A-Z", "-", "0-9")
                with self.repeat():
                    with self.choice():
                        with self.case(), self.capture_node('raw'):
                            self.whitespace(min=1)  # allow newline
                        with self.case(), self.repeat(min=1):
                            with self.capture_node('raw'): 
                                self.whitespace()
                                self.newline()
                            self.indent(partial=True)
                            with self.capture_node('raw'): self.whitespace()

                    with self.capture_node('raw'):
                        self.range("a-z", "A-Z", ":", "_")
                        with self.repeat(min=1):
                            self.range("a-z", "A-Z", ":", "_", "0-9", "-")
                    with self.optional():
                        with self.capture_node('raw'):
                            self.whitespace()
                            self.literal("=")
                        with self.choice():
                            with self.case(), self.capture_node('raw'):
                                self.whitespace() # allow newline
                            with self.case(), self.repeat(min=0):
                                with self.capture_node('raw'):
                                    self.whitespace()
                                    self.newline()
                                self.indent(partial=True)
                                with self.capture_node('raw'): self.whitespace()

                        with self.choice():
                            with self.case():
                                with self.capture_node('raw'):
                                    with self.repeat(min=1):
                                        self.range("\"", "'", "=", "<", ">", "`", "\t", " ", "\n", "\r", invert=True)
                            with self.case():
                                with self.capture_node('raw'):
                                    self.literal("\"")
                                    with self.repeat(): 
                                        self.range('"', "\n", invert=True)
                                with self.repeat():
                                    with self.capture_node('raw'):
                                        self.newline()
                                    self.indent(partial=True)
                                    with self.capture_node('raw'), self.repeat(): 
                                        self.range('"', "\n", invert=True)

                                with self.capture_node('raw'): 
                                    self.literal("\"")
                            with self.case():
                                with self.capture_node('raw'):
                                    self.literal('\'')
                                    with self.repeat(): 
                                        self.range("'", "\n",invert=True)
                                with self.repeat():
                                    with self.capture_node('raw'):
                                        self.newline()
                                    self.indent(partial=True)
                                    with self.capture_node('raw'), self.repeat(): 
                                        self.range('\'', "\n", invert=True)
                                with self.capture_node('raw'):
                                    self.literal('\'')
                with self.choice():
                    with self.case():
                        with self.capture_node('raw'):
                            self.whitespace()
                            self.literal("/>", ">")
                    with self.case():
                        with self.choice():
                            with self.case(), self.capture_node('raw'):
                                self.whitespace() # allow newline
                            with self.case(), self.repeat():
                                with self.capture_node('raw'):
                                    self.whitespace()
                                    self.newline()
                                self.indent(partial=True)
                                with self.capture_node('raw'): self.whitespace()
                        with self.capture_node('raw'):
                            self.literal("/>")
            with self.case():
                with self.capture_node('raw'):
                    self.literal("</")
                    self.range("a-z", "A-Z")
                    with self.repeat():
                        self.range("a-z", "A-Z", "-", "0-9")
                    self.whitespace()
                    self.literal(">")


## HTML Builder

import html
import html.entities
import urllib.parse 

def link_encode(text):
    text = urllib.parse.quote(text, safe="/:?=&+*;@,.()#")
    return text

def html_escape(text):
    return text.replace("&", "&amp;").replace("\"", "&quot;").replace(">", "&gt;").replace("<","&lt;").replace("\x00", "\uFFFD")

def make_para(children):
    return process_emphasis(children)

def process_emphasis(children):
    operators =[(idx, o[0], o[1], o[2], o[2]) for idx, o in enumerate(children) if isinstance(o, tuple)]
    active = {k:True for k in range(len(operators))}

    left_replacement = {}
    right_replacement = {}
    op_idx = 0

    while op_idx < len(operators):
        idx, kind, chr, N, n = operators[op_idx]
        if kind == "right" or kind == "dual":
            left_op = op_idx -1
            while n >0 and left_op >=0:
                found = False
                while left_op >= 0:
                    if active[left_op]:
                        left_idx, left_kind, left_chr, left_N, left_n = operators[left_op]
                        if left_chr == chr and left_n > 0 and (kind != "dual" or  left_N%3 == 0 or N%3 == 0 or (left_N + N)%3 != 0):
                            if left_kind == "left" or (left_kind == "dual" and( left_N%3 == 0 or N%3 == 0 or (left_N + N)%3 != 0)):
                                found = True
                                break
                    left_op -=1
                if found:
                    if left_n  <= n:
                        operators[left_op] = (left_idx, left_kind, left_chr, left_N, 0)
                        n = n - left_n
                    else:
                        operators[left_op] = (left_idx, left_kind, left_chr, left_N, left_n -n)
                        left_n = n
                        n = 0
                        
                    if left_idx not in left_replacement:
                        left_replacement[left_idx] = []
                    if idx not in right_replacement:
                        right_replacement[idx] = []
                    
                    left_replacement[left_idx].insert(0, left_n)
                    right_replacement[idx].append(left_n)

                    for i in range(left_op+1, op_idx):
                        active[i] = False

                left_op -= 1
            operators[op_idx] = (idx, kind, chr, N, n)
        op_idx +=1

    for idx, kind, chr, N, count in operators:
        if kind == "left": # replacements in left to right order
            out = []
            for _ in range(count):
                out.append(chr)
            if idx in left_replacement:
                for c in left_replacement[idx]:
                    if c%4: out.append(["<strong><strong>", "<em>", "<strong>", "<em><strong>"][c%4])
                    for _ in range(c//4):
                        out.append("<strong><strong>")
            children[idx] = "".join(out)
        elif kind == "right":
            out = []
            if idx in right_replacement:
                for c in right_replacement[idx]: 
                    for _ in range(c//4):
                        out.append("</strong></strong>")
                    if c%4: out.append(["</strong></strong>", "</em>", "</strong>", "</strong></em>"][c%4])
            for _ in range(count):
                out.append(chr)
            children[idx] = "".join(out)
        elif kind == "dual":
            out = []
            if idx in right_replacement:
                for c in reversed(right_replacement[idx]): 
                    for _ in range(c//4):
                        out.append("</strong></strong>")
                    if c%4: out.append(["</strong></strong>", "</em>", "</strong>", "</strong></em>"][c%4])
            for _ in range(count):
                out.append(chr)
            if idx in left_replacement:
                for c in left_replacement[idx]:
                    if c%4: out.append(["<strong><strong>", "<em>", "<strong>", "<em><strong>"][c%4])
                    for _ in range(c//4):
                        out.append("<strong><strong>")
            children[idx] = "".join(out)


    return "".join(children)

def join_blocks(children):
    def wrap(c):
        if isinstance(c, tuple):
            return f"<p>{c[0]}</p>"
        return c
    return '\n'.join(wrap(c) for c in children if c)

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

builder = {}
_builder = lambda fn:builder.__setitem__(fn.__name__,fn)

@_builder
def document(buf, node, children):
    o=join_blocks(children)
    return o+"\n" if o else ""

@_builder
def thematic_break(buf, node, children):
    return "<hr />"

@_builder
def atx_heading(buf, node, children):
    return f"<h{node.value}>{make_para(children)}</h{node.value}>"

@_builder
def setext(buf, node, children):
    return f"<h{node.value}>{make_para(children)}</h{node.value}>"

@_builder
def para(buf, node,  children):
    return (make_para(children),)

@_builder
def indented_code(buf, node, children):
    text = html_escape("".join(children))
    return f"<pre><code>{text}</code></pre>"

@_builder
def partial_indent(buf, node, children):
    return " "*(node.end_column-node.start_column)

@_builder
def indented_code_line(buf, node, children):
    return buf[node.start:node.end]+"\n"

@_builder
def fenced_code(buf, node, children):
    info = children[0]
    language = ""
    if info:
        language = f' class="language-{info}"'
    text = "\n".join(children[1:])
    if text: text = text+"\n"
    return f"<pre><code{language}>{text}</code></pre>"

@_builder
def info(buf, node, children):
    text = "".join(children)
    text = text.lstrip().split(' ',1)
    if text: return text[0]

@_builder
def blockquote(buf, node, children):
    text = join_blocks(children)
    end = '\n' if text != '\n' else ''
    start = '\n' if text and text != '\n' else ''
    return f"<blockquote>{start}{text}{end}</blockquote>"

@_builder
def unordered_list(buf, node, list_items):
    out = ["<ul>\n"]

    if loose(list_items) or any(loose(c) for c in list_items if c):
        wrap_loose(list_items, out)
    else:
        wrap_tight(list_items, out)

    out.extend("</ul>")
    return "".join(out)

@_builder
def ordered_list(buf, node, list_items):
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
def list_item(buf, node, children):
    return children

@_builder
def ordered_list_start(buf, node, children):
    return int(buf[node.start:node.end])

@_builder
def html_block(buf, node, children):
    return "".join(children)

@_builder
def link_def(buf, node, children):
    return ""

@_builder
def link_name(buf, node, children):
    return buf[node.start:node.end]

@_builder
def image(buf, node, children):
    if len(children) == 3 and children[2]:
        return f'<img src="{link_encode(children[1])}" alt="{children[0]}" title="{html_escape(children[2])}" />'

    if len(children) >= 2 and children[1] is not None:
        return f'<img src="{link_encode(children[1])}" alt="{children[0]}" />'

    return f"![{children[0]}]"

@_builder
def link(buf, node, children):
    if len(children) == 3 and children[2]:
        return f'<a href="{link_encode(children[1])}" title="{html_escape(children[2])}">{children[0]}</a>'

    if len(children) >= 2 and children[1] is not None:
        return f'<a href="{link_encode(children[1])}">{children[0]}</a>'

    return f"[{children[0]}]"

@_builder
def link_label(buf, node, children):
    return None
    
@_builder
def link_para(buf, node, children):
    return make_para(children)

@_builder
def link_url(buf, node, children):
    return buf[node.start:node.end]

@_builder
def link_title(buf, node, children):
    return buf[node.start:node.end]

@_builder
def raw_entity(buf, node, children):
    kind = node.value
    if kind == "named":
        text = buf[node.start:node.end+1] # + ;
        if text in html.entities.html5:
            out = (html.entities.html5[text])
        else:
            out = f"&{text}"
    elif kind == "hex":
        text = buf[node.start:node.end]
        out =(chr(int(text,16)))
    elif kind == "decimal":
        text = buf[node.start:node.end]
        out = (chr(int(text)))
    else:
        raise Exception('no')
    return out

@_builder
def html_entity(buf, node, children):
    kind = node.value
    if kind == "named":
        text = buf[node.start:node.end+1] # + ;
        if text in html.entities.html5:
            out = (html.entities.html5[text])
        else:
            out = f"&{(text)}"
    elif kind == "hex":
        text = buf[node.start:node.end]
        out =(chr(int(text,16)))
    elif kind == "decimal":
        text = buf[node.start:node.end]
        out = (chr(int(text)))
    else:
        raise Exception('no')
    return html_escape(out)
@_builder
def code_span(buf, node, children):
    text = "".join(children)
    text = text.replace('\n', ' ')
    if len(text) > 2 and text[0] == text[-1] == " ":
        text = text[1:-1]
    return f"<code>{text}</code>"

@_builder
def left_flank(buf, node, children):
    return tuple(children)

@_builder
def right_flank(buf, node, children):
    return tuple(children)

@_builder
def dual_flank(buf, node, children):
    return tuple(children)

@_builder
def auto_link(buf, node, children): 
    text = buf[node.start:node.end]
    return f'<a href="{link_encode(text)}">{html_escape(text)}</a>'

@_builder
def mailto_auto_link(buf, node, children): 
    text = buf[node.start:node.end]
    return f'<a href="mailto:{link_encode(text)}">{html_escape(text)}</a>'


@_builder
def softbreak(buf, node, children):
    return "\n"

@_builder
def hardbreak(buf,  node, children):
    return f"<br />\n"

@_builder
def whitespace(buf, node,  children):
    return buf[node.start:node.end]

@_builder
def text(buf, node, children):
    return html_escape(buf[node.start: node.end])

@_builder
def raw(buf, node, children):
    return buf[node.start:node.end]

@_builder
def empty(buf, node, children):
    return None

@_builder
def empty_line(buf, node, children):
    return None


### 


def markup(buf):
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

if __name__ == "__main__":
    with open('CommonMarkParser.py', 'w') as fh:
        fh.write(compile_python(CommonMark))
            
    #for name, value in CommonMark.rules.items():
    #    print(name, '<--', value,'.')

    print(CommonMark.version)
    #with open("../README.md") as readme:
    #    markup(readme.read())


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
        backrefs = {}
        def visit_backrefs(buf, node, children):
            if node.name == "link_def":
                name_node = children[0]
                name = buf[name_node.start:name_node.end]
                name = " ".join(name.strip().casefold().split())
                if name not in backrefs:
                    backrefs[name] = children[1:]
            return node

        out1.build(markd, visit_backrefs)

        def fill_backrefs(buf, node, children):
            if node.name == "link_label":
                name = node.value or buf[node.start:node.end]
                name = " ".join(name.strip().casefold().split())
                if name in backrefs:
                    node.value = backrefs[name]
                else:
                    node.value = None
            if node.name == "link" or node.name == "image":
                if len(children) > 1 and children[1].name == "link_label" and children[1].value is not None:
                    node.children = children[:1] + children[1].value
            return node

        out1 = out1.build(markd, fill_backrefs)

        out = out1.build(markd, builder)
        count +=1
        if out == t['html']: 
            worked +=1
            #print(repr(markd))
            #print(repr(out))
        else:
            failed +=1
            # if '<' in markd: continue
            # if '[' in markd: continue
            print(t['example'])
            print(repr(markd))
            print('=', repr(t['html']))
            print('X', repr(out))
            print()
            walk(out1)
            print()
    print(count, worked, failed)


