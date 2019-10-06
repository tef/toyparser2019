"""
"""

import base64, codecs
from datetime import datetime, timedelta, timezone

from ..grammar import Grammar, compile_python, sibling


import html

def to_html(obj, inside=None):
    if isinstance(obj, str): return html.escape(obj)
    return obj.to_html(inside=inside)

html_tags = {
       "document": "<html>\n{text}</html>",
       "code": "<pre><code>{text}</code></pre>\n",
       "code_span": "<code>{text}</code>",
       "thead": "<thead><tr>{text}</tr></thead>\n",
       "para": "<p>{text}</p>\n",
       "br": "<br/>\n",
       "nbsp": "&nbsp;",
       "strike": "<del>{text}</del>",
       "strong": "<strong>{text}</strong>",
       "emph": "<em>{text}</em>",
}


class Directive:
    def __init__(self, name, args, text):
        self.name = name
        self.args = args
        self.text = text

    def to_text(self):
        return to_text(self)
    def to_html(self, inside=None):
        args = " ".join(f"{key}={repr(value)}" for key, value in self.args)
        args = f" {args}" if args else ""
        text = "".join(to_html(x) for x in self.text) if self.text else ""


class Block(Directive):
    def to_html(self, inside=None):
        args = dict(self.args)
        name = self.name

        if name == "heading":
            name = f"h{args.get('level',1)}"
            if 'level' in args: args.pop('level')
        if name =="group" or name =="para_group":
            if args['marker'] == '-':
                if 'start' in args:
                    name = "ol"
                else:
                    name = "ul"
                args.pop('marker')
            elif args['marker'] == '>':
                name = "blockquote"
                args.pop('marker')

        if name =="list":
            if 'start' in args:
                name = "ol"
            else:
                name = "ul"
            args.pop('marker')

        if name == "table":
            # pull out alignment
            pass
        if name == "division":
            return ""
        if name == "row":
            name = "tr"


        text = "".join(to_html(x, inside=name) for x in self.text if x is not None) if self.text else ""
        args = " ".join(f"{key}={repr(value)}" for key, value in args.items())

        if name =="item":
            if inside == "blockquote":
                return text
            else:
                name ="li"

        if name in html_tags:
            return html_tags[name].format(name=name, args=args, text=text)
        if text:
            args = f" {args}" if args else ""
            return f"<{name}{args}>{text}</{name}>\n"
        else:
            args = f" {args} " if args else ""
            return f"<{name}{args}/>\n"


class Inline(Directive):
    def to_html(self, inside=None):
        args = dict(self.args)
        name = self.name

        if name == "cell":
            name = "td"
        if name == "emoij":
            name = "span"
            args['class'] = "emoji"
            args['style'] = "border: 1px dotted red"

        if name =="item_span":
            if inside == "blockquote":
                name = "p"
            else:
                name ="li"
        if name == "nbsp":
            return "&nbsp;"

        text = "".join(to_html(x, inside=name) for x in self.text if x is not None) if self.text else ""
        args = " ".join(f"{key}={repr(value)}" for key, value in args.items())

        if name in html_tags:
            return html_tags[name].format(name=name, args=args, text=text)
        if text:
            args = f" {args}" if args else ""
            return f"<{name}{args}>{text}</{name}>"
        else:
            args = f" {args} " if args else ""
            return f"<{name}{args}/>"


class Raw(Directive):
    pass

def to_text(obj):
    if isinstance(obj, str): return obj

    end = "\n" if isinstance(obj, Block) else ""
    args = ", ".join(f"{key}: {repr(value)}" for key, value in obj.args)
    args = f"[{args}]" if args else ""
    text = "".join(to_text(x) for x in obj.text) if obj.text else ""
    text = "{" f"{text}" "}" if text else ";"
    return f"\\{obj.name}{args}{text}"

def unescape(string):
    return codecs.decode(string.replace('\\/', '/'), 'unicode_escape')

def parse_datetime(v):
    if v[-1] == 'Z':
        if '.' in v:
            return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        else:
            return datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    else:
        raise NotImplementedError()

bools = {'false': False, 'true':True}

def builder(buf, node, children):
    kind = node.name
    if kind == "value":
        return node.value

    if kind == "document":
        return Block("document", [], [c for c in children if c is not None])

    if kind == 'identifier':
        return buf[node.start:node.end]
    if kind == "text":
        return buf[node.start:node.end]
    if kind == "nbsp":
        return Inline("nbsp", [],[])
    if kind == "whitespace":
        if node.end == node.start:
            return None
        return " "

    if kind == "softbreak":
        return " "
    if kind == "hardbreak":
        return Inline("br", [], [])

    if kind in ('empty', 'empty_line'):
        return None

    if kind == "emoji":
        return Inline("emoij", [],[c for c in children if c is not None])


    if kind == 'horizontal_rule':
        return Block("hr", children[0], [])
    if kind == 'atx_heading':
        args = children[0]
        return Block("heading", [("level", node.value)] + args, [c for c in children[1:] if c is not None])

    if kind == "para":
        return Block("para", [], [c for c in children if c is not None])
    if kind == "span":
        args = children[-1]
        return Inline("span", [("marker", node.value)] +args,[c for c in children[:-1] if c is not None])
    if kind == 'code_span':
        args = children[-1]
        return Inline("code_span",args, [c for c in children[:-1] if c is not None])

    if kind == 'code_block':
        arg = children[0] if children[0] is not None else []
        return Block("code", arg, [c for c in children[1:] if c is not None])
    if kind == "code_string":
        return [("language", children)]

    if kind == 'group':
        marker = children[0]
        spacing = children[1]
        if spacing == "tight":
            if all(c and c.name == "item_span" for c in children[2:]):
                return Block("para_group", [("marker", marker)], [c for c in children[2:] if c is not None])
        new_children = []
        for c in children[2:]:
            if c is None: continue
            if c.name == 'item_span':
                text = [Block("para", [], c.text)] if c.text else []
                c = Block("item", c.args, text)
            new_children.append(c)
        return Block("group", [("marker", marker)], new_children)
    if kind == 'group_marker':
        return buf[node.start:node.end]
    if kind == 'group_spacing':
        return node.value
    if kind == 'item':
        spacing = children[1]
        if spacing == "tight":
            if not children[2:]:
                return Inline("item_span", children[0], [])
            elif len(children) == 3 and children[2].name == "para" and not children[2].args:
                return Inline("item_span", children[0], children[2].text)
            else:
                return Block("item", children[0], [c for c in children[2:] if c is not None])

        return Block("item", children[0], [c for c in children[2:] if c is not None])
    if kind == 'item_spacing':
        return node.value

    if kind == "block_directive":
        args = children[1]
        text = [children[2]] if children[2] is not None else []
        name = children[0]
        if text and text[0].name in ('directive_group', 'directive_para', 'directive_table', 'directive_block'):
            if name in ('list', 'blockquote') and text[0].name == "directive_group":
                args = args + text[0].args # pull up spacing
            if name == 'table' and text[0].name == "directive_group":
                new_text = []
                def transform_row(r):
                    if r.name in ('item', 'item_span'):
                        name, text = transform_cols(r.name, r.text)
                        return Block(name, [], text)
                    else:
                        return d

                def transform_cols(name, d):
                    if len(d) == 1 and d[0].name in ('para_group', 'group'):
                        return "row", [Inline('cell', [], t.text) for t in d[0].text]
                    elif all(getattr(t,'name', '') == 'heading' for t in d):
                        return "thead", [Inline('cell', [], t.text) for t in d]

                    return name, d
                    
                text = [transform_row(r) for r in text[0].text]
            else:
                text = text[0].text
        return Block(children[0], args, text)
    if kind == "inline_directive":
        args = children[1]
        text = [children[2]] if children[2:] and children[2] is not None else []
        if text and text[0].name == 'directive_span':
            text = text[0].text
        return Inline(children[0], args, text)
    if kind == "arg":
        return children
    if kind == "directive_args":
        return children
    if kind == "directive_name":
        return buf[node.start:node.end]

    if kind == "directive_span":
        return Inline('directive_span',[],[c for c in children if c is not None])

    if kind == "directive_para":
        return Block('directive_para',[],[c for c in children if c is not None])
    if kind == "directive_table":
        return Block('directive_table',[],[c for c in children if c is not None])
    if kind == "directive_block":
        return Block('directive_block',[],[c for c in children if c is not None])
    if kind == "directive_group":
        marker = children[0]
        spacing = children[1]
        return Block("directive_group", [("marker", marker), ("spacing", spacing)], [c for c in children[2:] if c is not None])

    if kind == "table":
        return Block('table',[],[c for c in children if c is not None])
        
    if kind == "table_cell":
        return Inline('cell', [], children)
    if kind == "cell_align":
        left = buf[node.start] == ":"
        right = buf[node.end-1] == ":"
        if left and right: return "\\center;"
        if left: return "\\left;"
        if right: return "\\right;"
        return "\\default;"
    if kind == "table_row":
        return Block('row', [], children)
    if kind == "table_heading":
        return Block('thead', [], children)
    if kind == "table_division":
        return Block('division',[], children)

    if kind == 'block_rson':
        text = []
        args = children[1]
        if isinstance(args, dict) and 'text' in args:
            text = args.pop('text')
        args = list(args.items())
        return Raw(children[0], args, text)

    if kind == 'rson_number': 
        return eval(buf[node.start:node.end])
    if kind == 'rson_string': 
        return unescape(buf[node.start:node.end])
    if kind == 'rson_list': 
        return children
    if kind == 'rson_object': 
        return dict(children)
    if kind == 'rson_pair':
        return children
    if kind =='rson_bool': 
        return bools[buf[node.start:node.end]]
    if kind == 'rson_null': 
        return None
    if kind == "rson_tagged":
        identifier, literal = children
        if identifier == "object":
           return literal
        if identifier == "record" or identifier == "dict":
            if not isinstance(literal, dict): raise Exception('bad')
            return literal
        elif identifier == "list":
            if not isinstance(literal, list): raise Exception('bad')
            return literal
        elif identifier == "string":
            if not isinstance(literal, str): raise Exception('bad')
            return literal
        elif identifier == "bool":
            if not isinstance(literal, bool): raise Exception('bad')
            return literal
        elif identifier == "int":
            if not isinstance(literal, int): raise Exception('bad')
            return literal
        elif identifier == "float":
            if isinstance(literal, float): return literal
            if not isinstance(literal, str): raise Exception('bad')
            return float.fromhex(literal)
        elif identifier == "set":
            if not isinstance(literal, list): raise Exception('bad')
            return set(literal)
        elif identifier == "complex":
            if not isinstance(literal, list): raise Exception('bad')
            return complex(*literal)
        elif identifier == "bytestring":
            if not isinstance(literal, str): raise Exception('bad')
            return literal.encode('ascii')
        elif identifier == "base64":
            if not isinstance(literal, str): raise Exception('bad')
            return base64.standard_b64decode(literal)
        elif identifier == "datetime":
            if not isinstance(literal, str): raise Exception('bad')
            return parse_datetime(literal)
        elif identifier == "duration":
            if not isinstance(literal, (int, float)): raise Exception('bad')
            return timedelta(seconds=literal)
        elif identifier == "unknown":
            raise Exception('bad')
        return {identifier: literal}
    raise Exception(node.name)
    return {node.name: children}


class Remarkable(Grammar, start="document", whitespace=[" ", "\t"], newline=["\r", "\n", "\r\n"], tabstop=8):
    @rule(inline=True) # 2.1 line ends by newline or end_of_file
    def line_end(self):
        self.whitespace()
        self.end_of_line()

    # block
    @rule(start="document")
    def document(self):
        with self.choice():
            with self.case():
                self.literal("\\document{")
                with self.repeat():
                    self.whitespace()
                    self.inline_directive()
                    self.whitespace()
                self.literal("}")
                self.whitespace(newline=True)
                self.end_of_file()
            with self.case():
                with self.repeat(min=0) as n:
                    self.indent()
                    with self.choice():
                        with self.case(): self.block_element()
                        with self.case(): self.para()
                        with self.case(): self.empty_lines()
                        with self.case(): self.end_of_file()
                self.whitespace()
                self.end_of_file()

    @rule(inline=True)
    def empty_lines(self):
        self.whitespace()
        self.newline()
        with self.repeat():
            self.indent()
            self.whitespace()
            self.newline()
        with self.capture_node("empty_line"):
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
                self.block_directive()
            with self.case():
                self.block_group()
            with self.case():
                self.table()

    @rule()
    def paragraph_breaks(self):
        with self.choice():
            with self.case(): self.horizontal_rule()
            with self.case(): self.atx_heading()
            with self.case(): self.start_code_block()
            with self.case(): self.start_group()
            with self.case(): self.start_table()


    @rule(inline=True)
    def linebreak(self):
        with self.choice():
            with self.case():
                self.whitespace()
                self.literal("\\")
                with self.capture_node("hardbreak"):
                    self.newline()
            with self.case():
                self.whitespace()
                with self.capture_node("softbreak"):
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
        self.whitespace()
        self.inline_element()

        with self.repeat():
            with self.choice():
                with self.case():
                    self.linebreak()
                with self.case():
                    with self.capture_node("whitespace"):
                        self.whitespace()

            self.inline_element()

        self.whitespace()
        with self.optional():
            self.literal("\\")
            self.capture_value("\\")
        self.end_of_line()



    @rule()
    def para(self):
        with self.capture_node("para"):
            self.inner_para()

    @rule()
    def identifier(self):
        with self.capture_node('identifier', nested=False):
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
                self.identifier()
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
    def block_directive(self):
        self.whitespace(max=8)
        self.literal("\\")
        with self.capture_node("block_directive"):
            with self.capture_node("directive_name"), self.backref() as name:
                self.identifier()
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
                    self.code_block()
                with self.case():
                    self.literal(":")
                    with self.choice():
                        with self.case(), self.variable("") as fence:
                            self.literal(":begin")
                            with self.optional():
                                self.whitespace()
                                with self.backref() as b:
                                    self.identifier()
                                self.set_variable(fence, b)
                            self.line_end()
                            with self.capture_node("directive_block"):
                                with self.repeat(min=0) as n:
                                    self.indent()
                                    with self.reject():
                                        self.literal("\\")
                                        self.literal(name)
                                        self.literal("::end")
                                        self.whitespace()
                                        self.literal(fence)
                                        self.line_end()
                                    with self.choice():

                                        with self.case(): self.block_element()
                                        with self.case(): self.para()
                                        with self.case(): self.empty_lines()
                            self.indent()
                            self.literal("\\")
                            self.literal(name)
                            self.literal("::end")
                            self.whitespace()
                            self.literal(fence)
                            self.line_end()


                        with self.case():
                            with self.reject():
                                self.whitespace()
                                self.newline()
                            with self.capture_node("directive_para"):
                                self.inner_para()
                        with self.case():
                            self.whitespace()
                            self.newline()
                            self.indent()
                            with self.choice():
                                with self.case():
                                    with self.capture_node("directive_group"):
                                        self.inner_group()
                                with self.case():
                                    with self.capture_node("directive_table"):
                                        self.inner_table()
                                with self.case():
                                    with self.capture_node("directive_para"):
                                        self.inner_para()
                        with self.case():
                            self.empty_lines()
                with self.case():
                    self.line_end()
                    self.capture_value(None)

    # inlines/paras
            
    @rule(inline=True)
    def inline_directive(self):
        self.literal("\\")
        with self.capture_node("inline_directive"):
            with self.capture_node("directive_name"):
                self.identifier()
            with self.capture_node("directive_args"), self.optional():
                self.literal("[")
                self.directive_args()
                self.literal("]")
            with self.optional(), self.choice():
                with self.case():
                    self.literal(";")
                    self.capture_value(None)
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
                                        with self.capture_node("whitespace"):
                                            self.whitespace()

                                with self.reject():
                                    with self.repeat(min=n, max=n):
                                        self.literal("}")
                                self.inline_element()
                        with self.choice():
                            with self.case():
                                self.linebreak()
                            with self.case():
                                with self.capture_node("whitespace"):
                                    self.whitespace()

                    with self.repeat(min=n, max=n):
                        self.literal("}")
                with self.case():
                    self.code_span()
    @rule() 
    def horizontal_rule(self):
        self.whitespace(max=8)
        with self.capture_node('horizontal_rule'):
            with self.repeat(min=3):
                self.literal("-")
            with self.capture_node("directive_args"), self.optional():
                self.whitespace(min=1)
                self.literal("[")
                self.directive_args()
                self.literal("]")
        self.line_end()

    @rule()
    def atx_heading(self):
        self.whitespace(max=8)
        with self.variable(0) as num, self.capture_node("atx_heading", value=num):
            with self.count(char='#') as level:
                with self.repeat(min=1, max=9):
                    self.literal("#")
            self.set_variable(num, level)
            with self.capture_node("directive_args"):
                with self.optional():
                    self.whitespace(min=1)
                    self.literal("[")
                    self.directive_args()
                    self.literal("]")
            with self.choice():
                with self.case():
                    self.line_end()
                with self.case():
                    self.whitespace(min=1)
                    self.inner_para()

    @rule()
    def start_code_block(self):
        self.whitespace(max=8)
        self.literal("```")

    @rule()
    def code_block(self):
        self.whitespace(max=8)
        with self.capture_node('code_block'):
            fence = "`"
            with self.count(char=fence) as c, self.repeat(min=3):
                self.literal(fence)
            with self.choice():
                with self.case(), self.capture_node("directive_args"):
                    self.whitespace(min=1)
                    self.literal("[")
                    self.directive_args()
                    self.literal("]")
                with self.case(), self.capture_node("code_string"):
                    self.whitespace()
                    self.identifier()
                with self.case():
                    self.capture_value(None)

            self.line_end()
            with self.repeat():
                self.indent()
                with self.reject():
                    with self.repeat(min=c):
                        self.literal(fence)
                    self.line_end()
                with self.capture_node('text'):
                    with self.repeat(min=0):
                        self.range("\n", invert=True)
                    self.line_end()
            self.indent()
            with self.repeat(min=c):
                self.literal(fence)
            self.whitespace()
            self.line_end()

    @rule()
    def start_group(self):
        self.whitespace(max=8)
        self.literal("-", ">")
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
                        with self.capture_node("empty"):
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
    def inner_group(self):
        with self.variable('tight') as spacing:
            with self.count(columns=True) as w:
                with self.count(columns=True) as i:
                    self.whitespace(max=8)
                with self.capture_node('group_marker'), self.backref() as marker:
                    self.range("-", ">")
            with self.capture_node('group_spacing', value=spacing):
                pass


            with self.choice():
                with self.case(), self.lookahead():
                    self.whitespace()
                    self.end_of_line()
                with self.case():
                    self.whitespace(min=1, max=1, newline=True)

            with self.capture_node("item"):
                with self.capture_node("directive_args"):
                    with self.optional():
                        self.literal("[")
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
                    with self.capture_node('empty'):
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

                with self.capture_node("item"):
                    with self.capture_node("directive_args"):
                        with self.optional():
                            self.literal("[")
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
    def block_group(self):
        with self.capture_node('group'):
            self.inner_group()


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
                    self.inline_element()
                    with self.repeat():
                        with self.capture_node("whitespace"):
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
                with self.capture_node('table_heading'):
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

                with self.capture_node('table_division'):
                    with self.repeat(min=c, max=c):
                        self.literal("|")
                        self.whitespace()
                        with self.capture_node("cell_align"):
                            self.whitespace()
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
                    with self.repeat(max=c):
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
                with self.capture_node("text"):
                    self.range("*", "_","!-/",":-@","[-`","{-~")
            with self.case():
                self.literal("\\")
                with self.capture_node("nbsp"):
                    self.whitespace(min=1)
            with self.case():
                self.literal(":")
                with self.capture_node("emoji"):
                    self.identifier()
                self.literal(":")
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
        with self.capture_node('text'):
            self.range(" ", "\n", "\\", invert=True)
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
        with self.variable('') as fence, self.capture_node('span', value=fence):
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
                        with self.capture_node("whitespace"):
                            self.whitespace()

                with self.reject():
                    with self.repeat(min=n, max=n):
                        self.literal(fence)
                self.inline_element()

            with self.choice():
                with self.case():
                    self.linebreak()
                with self.case():
                    with self.capture_node("whitespace"):
                        self.whitespace()
            with self.repeat(min=n, max=n):
                self.literal(fence)
            with self.capture_node("directive_args"), self.optional():
                self.literal("[")
                self.directive_args()
                self.literal("]")
                
    @rule()
    def code_span(self):
        with self.capture_node('code_span') as span: 
            with self.count(char="`") as c, self.repeat(min=1):
                self.literal("`")
            with self.repeat(min=1), self.choice():
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
            with self.capture_node("directive_args"), self.optional():
                self.literal("[")
                self.directive_args()
                self.literal("]")

    @rule()
    def block_rson(self):
        with self.capture_node('block_rson'):
            self.literal('@')
            self.identifier()
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
                    self.identifier()
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
            with self.case(): self.identifier()
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

parser = Remarkable().parser()
def parse(buf):
    # remove metadata block
    # lift into document block
    # use metadata block to set up default transforms
    node = parser.parse(buf)
    def lift(buf, node, children):
        name = node.name
        if name =="group" or name =="para_group":
            if args['marker'] == '-':
                node.name = "list" 
                node.args.pop('marker')
            elif args['marker'] == '>':
                node.name = "blockquote"
                node.args.pop('marker')

        if name =="span":
            if args['marker'] == '*':
                node.name = "strong"
                args.pop('marker')
            elif args['marker'] == '~':
                node.name = "strike"
                args.pop('marker')
            elif args['marker'] == '_':
                name = "emph"
                args.pop('marker')

        return node
    if node:
        tree = node.build(buf, builder)
        return tree

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
