"""
"""

import base64, codecs, html
from datetime import datetime, timedelta, timezone

from ..grammar import Grammar, compile_python, sibling

class Directive:
    def __init__(self, name, args, text):
        self.name = name
        self.args = args
        self.text = text

    def to_text(self):
        return to_text(self)
    def to_html(self, inside=None):
        return to_html(self, inside)
    def to_ansi(self, width=None, height=None, inside=None):
        return to_ansi(self, 0, width, height, inside).splitlines()
class Data(Directive):
    pass

class Block(Directive):
    pass

class Document(Block):
    def __init__(self, args, text):
        Block.__init__(self, "document", args, text)

class Paragraph(Block):
    def __init__(self, args, text):
        Block.__init__(self, "paragraph", args, text)

class HorizontalRule(Block):
    def __init__(self, args, text=None):
        if text: raise Exception('bad')
        Block.__init__(self, "hr", args, [])

class Heading(Block):
    def __init__(self, args, text):
        Block.__init__(self, "heading", args, text)

class CodeBlock(Block):
    def __init__(self, args, text):
        Block.__init__(self, "code_block", args, text)

class GroupBlock(Block):
    def __init__(self, args, text):
        Block.__init__(self, "group", args, text)
class ListBlock(Block):
    def __init__(self, args, text):
        Block.__init__(self, "list", args, text)

class QuoteBlock(Block):
    def __init__(self, args, text):
        Block.__init__(self, "blockquote", args, text)

class BlockItem(Block):
    def __init__(self, args, text):
        Block.__init__(self, "block_item", args, text)
class Table(Block):
    def __init__(self, args, text):
        Block.__init__(self, "table", args, text)
class Row(Block):
    def __init__(self, args, text):
        Block.__init__(self, "row", args, text)

class HeaderRow(Block):
    def __init__(self, args, text):
        Block.__init__(self, "thead", args, text)

class BlockDirective(Block):
    def __init__(self, args, text):
        Block.__init__(self, "directive", args, text)

class Inline(Directive):
    pass

class Cell(Inline):
    def __init__(self, args, text):
        Inline.__init__(self, "cell", args, text)

class Span(Inline):
    def __init__(self, args, text):
        Inline.__init__(self, "span", args, text)

class ItemSpan(Inline):
    def __init__(self, args, text):
        Inline.__init__(self, "item_span", args, text)

class CodeSpan(Inline):
    def __init__(self, args, text):
        Inline.__init__(self, "code_span", args, text)

class Strong(Inline):
    def __init__(self, args, text):
        Inline.__init__(self, "strong", args, text)

class Emphasis(Inline):
    def __init__(self, args, text):
        Inline.__init__(self, "emph", args, text)

class Strike(Inline):
    def __init__(self, args, text):
        Inline.__init__(self, "strike", args, text)

class Hardbreak(Inline):
    def __init__(self, args=None, text=None):
        if args or text: raise Exception('bad')
        Inline.__init__(self, "hardbreak", [],[])

class Softbreak(Inline):
    def __init__(self, args=None, text=None):
        if args or text: raise Exception('bad')
        Inline.__init__(self, "softbreak", [],[])

class Nbsp(Inline):
    def __init__(self, args=None, text=None):
        if args or text: raise Exception('bad')
        Inline.__init__(self, "nbsp", [],[])

class Emoji(Inline):
    def __init__(self, args=None, text=None):
        if args: raise Exception('bad')
        Inline.__init__(self, "emoji", [], text)

class InlineDirective(Inline):
    def __init__(self, args, text):
        Inline.__init__(self, "directive", args, text)

block_directives = {
        "para": Paragraph,
        "p": Paragraph,
        "hr": HorizontalRule,
        "h": Heading,
        "heading": Heading,
        "code": CodeBlock,
        "list": ListBlock,
        "blockquote": QuoteBlock,
        "item": BlockItem,
}

inline_directives = {
        "strong": Strong,
        "b": Strong,
        "em": Emphasis,
        "emph": Emphasis,
        "emphasis": Emphasis,
        "strike": Strike,
        "code": CodeSpan,
        "item": ItemSpan,
}

        
# --- Parse Tree Builder
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
        text = []
        metadata = None
        for c in children:
            if c is None: continue
            if metadata is None and getattr(c, "name", "") == "metadata":
                metadata = c.args
                continue
            text.append(c)

        metadata = metadata or [('title', '')]

        if len(text) == 1 and getattr(text[0], "name", "") == "document":
            return text[0]
        return Document(metadata, text)

    if kind == 'identifier':
        return buf[node.start:node.end]
    if kind == "text":
        return buf[node.start:node.end]
    if kind == "nbsp":
        return Nbsp()
    if kind == "whitespace":
        if node.end == node.start:
            return None
        return " "

    if kind == "softbreak":
        return Softbreak()
    if kind == "hardbreak":
        return Hardbreak()

    if kind in ('empty', 'empty_line'):
        return None

    if kind == "emoji":
        return Emoji((), [c for c in children if c is not None])


    if kind == 'horizontal_rule':
        return HorizonralRule(children[0], ())
    if kind == 'atx_heading':
        args = [('level', node.value)] + children[0]
        return Heading(args, [c for c in children[1:] if c is not None])

    if kind == "paragraph":
        return Paragraph([], [c for c in children if c is not None])
    if kind == "span":
        args = children[-1]
        marker = node.value
        if marker == "*":
            return Strong(args,[c for c in children[:-1] if c is not None])
        if marker == "_":
            return Emphasis(args,[c for c in children[:-1] if c is not None])
        if marker == "~":
            return Strike(args,[c for c in children[:-1] if c is not None])
        if marker:
            return Span([("marker", node.value)] +args,[c for c in children[:-1] if c is not None])
        return Span(args,[c for c in children[:-1] if c is not None])
    if kind == 'code_span':
        args = children[-1]
        return CodeSpan(args, [c for c in children[:-1] if c is not None])

    if kind == 'code_block':
        arg = children[0] if children[0] is not None else []
        return CodeBlock(arg, [c for c in children[1:] if c is not None])
    if kind == "code_string":
        return [("language", children)]

    if kind == 'group':
        marker = children[0]
        spacing = children[1]
        name = 'group'
        args = [("marker", marker)]

        block = GroupBlock

        if marker == '>':
            name = "blockquote"
            block = QuoteBlock
            new_children = []
            for c in children[2:]:
                if c is None:
                    continue
                elif c.name == 'item_span':
                    new_children.append(Paragraph(c.args, c.text))
                elif c.name == "block_item":
                    new_children.extend(c.text)
                else:
                    new_children.append(c)
            return QuoteBlock([], new_children)


        elif marker == '-':
            name = "list"

            if spacing == "tight":
                if all(c and c.name == "item_span" for c in children[2:]):
                    return ListBlock([], [c for c in children[2:] if c is not None])

            new_children = []
            for c in children[2:]:
                if c is None: continue
                if c.name == 'item_span':
                    text = [Paragraph([], c.text)] if c.text else []
                    c = BlockItem(c.args, text)
                new_children.append(c)
            return ListBlock([], new_children)

        return GroupBlock(args, new_children)
    if kind == 'group_marker':
        return buf[node.start:node.end]
    if kind == 'group_spacing':
        return node.value
    if kind == 'item':
        spacing = children[1]
        if spacing == "tight":
            if not children[2:]:
                return ItemSpan(children[0], [])
            elif len(children) == 3 and children[2].name == "para" and not children[2].args:
                return ItemSpan(children[0], children[2].text)
            else:
                return BlockItem(children[0], [c for c in children[2:] if c is not None])

        return BlockItem(children[0], [c for c in children[2:] if c is not None])
    if kind == 'item_spacing':
        return node.value

    if kind == "block_directive":
        args = children[1]
        text = [children[2]] if children[2] is not None else []
        name = children[0]
        if text and text[0].name in ('directive_group', 'directive_para', 'directive_table', 'directive_block', 'directive_code', 'directive_code_span'):
            if name == 'list' and text[0].name == "directive_group":
                args = args + text[0].args # pull up spacing
                return BlockList([], args, text)
            if name == 'blockquote' and text[0].name == "directive_group":
                args = args + text[0].args # pull up spacing
                return BlockQuote([], args, text)
            if name == 'table' and text[0].name == "directive_group":
                new_text = []
                def transform_row(r):
                    if r.name == 'item_span':
                        return transform_cols(r, r.text)
                    if r.name == 'block_item':
                        return transform_cols(r, r.text)
                    else:
                        return r

                def transform_cols(name, d):
                    if len(d) == 1 and d[0].name in ('para_group', 'group', 'list', 'blockquote'):
                        if all( len(e.text) == 1 and getattr(e.text[0],'name', '') == 'heading' for e in d[0].text):
                            return HeaderRow([], [Cell([], t.text[0].text) for t in d[0].text])

                        return Row([], [Cell([], t.text) for t in d[0].text])
                    elif all(getattr(t,'name', '') == 'heading' for t in d):
                        return HeaderRow([], [Cell([], t.text) for t in d])

                    return name
                    
                text = [transform_row(r) for r in text[0].text]
                return Table(args, text)
            else:
                text = text[0].text
        if name in block_directives:
            return block_directives[name](args, text)
        else:
            return BlockDirective('directive', [('name', name)] + args, text)

    if kind == "inline_directive":
        name = children[0]
        if name == 'code':
            name == 'code_span'
        args = children[1]
        text = [children[2]] if children[2:] and children[2] is not None else []
        if text and text[0].name == 'directive_span':
            text = text[0].text
        if name in inline_directives:
            return inline_directives[name](args, text)
        return InlineDirective([('name', name)]+ args, text)
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
    if kind == "directive_code":
        return Block('directive_code',[],[c for c in children if c is not None])
    if kind == "directive_code_span":
        return Block('directive_code',[],[c for c in children if c is not None])
    if kind == "directive_table":
        return Block('directive_table',[],[c for c in children if c is not None])
    if kind == "directive_block":
        return Block('directive_block',[],[c for c in children if c is not None])
    if kind == "directive_group":
        marker = children[0]
        spacing = children[1]
        return Block("directive_group", [("marker", marker), ("spacing", spacing)], [c for c in children[2:] if c is not None])

    if kind == "table":
        text = []
        args = []
        for c in children:
            if c is None: continue
            if getattr(c, 'name', '') == "division":
                args.append(('column_align', c.text))
            else:
                text.append(c)
        return Block('table',args,text)
        
    if kind == "table_cell":
        return Inline('cell', [], children)
    if kind == "column_align":
        left = buf[node.start] == ":"
        right = buf[node.end-1] == ":"
        if left and right: return "center"
        if left: return "left"
        if right: return "right"
        return "default"
    if kind == "table_row":
        return Block('row', [], children)
    if kind == "table_heading":
        return Block('thead', [], children)
    if kind == "table_division":
        return Block('division',[], children)

    if kind == 'block_rson':
        text = []
        args = children[1]
        args = list(args.items())
        return Data(children[0], args, text)

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



template = """\
<html>
<head>
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
<style type="text/css">
* {{
    -webkit-box-sizing: border-box; 
    -moz-box-sizing: border-box;  
    box-sizing: border-box;   
}}

body, td {{
    background: white;
    font-family: "Lucida Sans Unicode", "Lucida Grande", Verdana, Arial, Helvetica, sans-serif;
    /*color: #000000;*/
    font-size: 0.9rem;
}}
i, em {{
    font-family: Georgia, serif;
}}

h1.title {{font-weight: normal; margin-top: 0; font-size: 1.8rem;}}
h1 {{font-weight: normal; margin-top: 0; font-size: 1.3rem;}}
h2 {{font-weight: normal; margin-top: 0; font-size: 1.1rem; }}

section {{
    margin-bottom: 2em;
}}

blockquote {{
    font-style: italic;
}}

blockquote em {{
    font-style: normal; 
}}

a {{ color: #0000ff; text-decoration: none; }} 
a:hover {{ color: #ff0000; text-decoration: underline; }}
a img {{ outline: 0; border: none; }}

hr {{
    height: 0;
    border: solid 1px;
    color: #cccccc;
    width: 100%;
    max-width: 36rem;
}}

footer {{
    text-align: center;

}}
footer ul {{
    padding-left: 0;
}}
footer li {{
    display: inline-block;
    list-style-type: none;
}}
footer li:after {{
    content: "&mdash;";
}}
footer li:last-child:after {{
    content: "";
}}


@media all and (max-width: 600px)  {{
  article {{
      padding-top: 1rem;
    }}
    nav {{
        border-top: solid 1px;
        width: 100%;
    }}
    body {{
        padding-left:3px;
        padding-right:3px;
    }}
    blockquote, pre, ul, ol {{
        padding-left:1rem;
        margin-left: 0;
        padding-right: 0;
        margin-right: 0;
    }}

}}

@media all and (min-width: 600px)  {{
    pre {{ 
        margin-left: 0rem; 
        padding-left: 1rem; 
        margin-top: 0; 
    }}
    blockquote {{
        margin-left: 0rem; 
        padding-left: 1rem; 
        margin-top: 0; 
        border-left: dotted 1px ;
    }}
    blockquote blockquote {{ 
        margin-left: 0; 
    }}

    blockquote ul, blockquote ol {{
        padding-left: 1rem;
    }}

    ul, ol {{
        padding-left: 1rem;
    }}
    
    body {{
        padding-left:5rem;
        max-width:37rem;
    }}
}}


h1,h2,h3 {{  padding-top:1rem;}}

p {{padding-bottom: 0.2rem;}}

p {{ -webkit-hyphens: none; -moz-hyphens: none; hyphens: none; }}

table {{
    border-spacing: 0;
    border-collapse: collapse;
}}
td {{

          border: 1px solid black;
          padding: 6px 13px;
}}

code {{
        white-space: pre;
}}
.emoji {{
    border: 1px dotted red
}}

</style>
</head>
<body>
{text}
</html>"""


html_tags = {
       "document": template,
       "code_block": "<pre><code>{text}</code></pre>\n",
       "code_span": "<code>{text}</code>",
       "thead": "<thead><tr>{text}</tr></thead>\n",
       "para": "<p>{text}</p>\n",
       "paragraph": "<p>{text}</p>\n",
       "hardbreak": "<br/>\n",
       "softbreak": "\n",
       "emoji":"<span class='emoji'>{text}</span>",
       "n": "\n",
       "table": "<table>\n{text}</table>\n",
       "row": "<tr>{text}</tr>\n",
       "division": "",
       "cell": "<td>{text}</td>",
       "nbsp": "&nbsp;",
       "strike": "<del>{text}</del>",
       "strong": "<strong>{text}</strong>",
       "emph": "<em>{text}</em>",
}

def to_html(obj, inside=None):
    if isinstance(obj, str): return html.escape(obj)

    args = dict(obj.args)
    name = obj.name
    text = "".join(to_html(x, inside=name) for x in obj.text if x is not None) if obj.text else ""

    if name == "heading":
        name = f"h{args.get('level',1)}"
        if 'level' in args: args.pop('level')

    if name =="list":
        if 'start' in args:
            name = "ol"
        else:
            name = "ul"
        if 'marker' in args: args.pop('marker')


    if name == "block_item":
        if inside in ('list','ul', 'ol'):
            name = "li"
        elif inside == "blockquote":
            name == "div"

    if name == "item_span":
        if inside in ('list','ul', 'ol'):
            name = "li"
        elif inside == "blockquote":
            name = "p"

    if name in html_tags:
        return html_tags[name].format(name=name, text=text, **args)
        args = " ".join(f"{key}={repr(value)}" for key, value in args.items())
    end = "" if isinstance(obj, Inline) else "\n"
    if text:
        args = f" {args}" if args else ""
        return f"<{name}{args}>{text}</{name}>{end}"
    else:
        args = f" {args}" if args else ""
        return f"<{name}{args}/>{end}"


def to_text(obj):
    if obj is None: return ""
    if isinstance(obj, str): 
        escape = "~_*\\-#`{}[]|@<>"
        return "".join(('\\'+t if t in escape else t) for t in obj).replace("\n", "\\n;")
    if isinstance(obj, Data):
        args = ", ".join(f"{key}: {repr(value)}" for key, value in obj.args)
        return f"@{obj.name}" "{" f"{args}" "}\n"


    end = "\n" if isinstance(obj, Block) else ""
    args = ", ".join(f"{key}: {repr(value)}" for key, value in obj.args) if obj.args else "NONE"
    #if obj.name in ('code', 'code_span') and obj.text:
    #    text = repr("".join(obj.text))
    #    args = f"text: {text}, {args}"
    #    text = ""
    #else:
    text = "".join(to_text(x) for x in obj.text) if obj.text else ""

    args = f"[{args}]" if args else ""
    text = "{" f"{text}" "}" if text else ";"
    return f"\\{obj.name}{args}{text}{end}"


def to_ansi(obj, indent, width, height, inside):
    if isinstance(obj, str): 
        escape = "~_*\\-#`{}[]|@<>"
        return "".join(('\\'+t if t in escape else t) for t in obj).replace("\n", "\\n;")
    if isinstance(obj, Data):
        args = ", ".join(f"{key}: {repr(value)}" for key, value in obj.args)
        return f"@{obj.name}" "{" f"{args}" "}\n"


    end = "\n" if isinstance(obj, Block) else ""
    args = ", ".join(f"{key}: {repr(value)}" for key, value in obj.args) if obj.args else ""
    text = "".join(to_ansi(x, indent, width, height, obj.name) for x in obj.text if x is not None) if obj.text else ""

    args = f"[{args}]" if args else ""
    text = "{" f"{text}" "}" if text else ";"
    return f"\\{obj.name}{args}{text}{end}"

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
                self.whitespace(newline=True)
                self.inline_directive()
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
        with self.capture_node("paragraph"):
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
                    with self.capture_node('directive_code'): 
                        self.inner_code_block()
                with self.case():
                    with self.count(columns=True) as n, self.repeat(min=3):
                        self.literal("{")
                        self.line_end()
                        with self.capture_node("directive_block"):
                            with self.repeat(min=0) as n:
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
                                        self.whitespace(max=8)
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
                            self.whitespace(max=8)
                            self.literal("\\")
                            self.literal(name)
                            self.literal("::end")
                            self.whitespace()
                            self.literal(fence)
                            self.line_end()

                        with self.case():
                            with self.reject():
                                self.literal(":")
                            with self.reject():
                                self.whitespace()
                                self.newline()
                            self.whitespace(min=1)
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
        self.literal("\\")
        with self.capture_node("inline_directive"):
            with self.capture_node("directive_name"):
                self.identifier()
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
                                        with self.capture_node("whitespace"):
                                            self.whitespace()

                                with self.reject():
                                    with self.repeat(min=n, max=n):
                                        self.literal("}")
                                self.inline_element()
                        with self.repeat(), self.choice():
                            with self.case():
                                self.linebreak()
                            with self.case():
                                with self.capture_node("whitespace"):
                                    self.whitespace()

                    with self.repeat(min=n, max=n):
                        self.literal("}")
                with self.case():
                    with self.capture_node('directive_code_span') as span: 
                        self.inner_code_span()
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
    def inner_code_block(self):
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
                        with self.capture_node("column_align"):
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
    def inner_code_span(self):
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
    @rule()
    def code_span(self):
        with self.capture_node('code_span') as span: 
            self.inner_code_span()
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
