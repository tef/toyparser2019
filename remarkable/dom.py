class Directive:
    def __init__(self, name, args, text):
        self.name = name
        self.args = args
        self.text = text

    def build(self, builder):
        pass

    def get_arg(self, key):
        if key is None:
            return [v for k,v in self.args if k is None]
        for k,v in self.args:
            if k == key: return v

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

class Section(Block):
    def __init__(self, args, text):
        Block.__init__(self, "section", args, text)

class Division(Block):
    def __init__(self, args, text):
        Block.__init__(self, "division", args, text)

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

class ItemBlock(Block):
    def __init__(self, args, text):
        Block.__init__(self, "block_item", args, text)

class Table(Block):
    def __init__(self, args, text):
        Block.__init__(self, "table", args, text)

class Row(Block):
    def __init__(self, args, text):
        Block.__init__(self, "row", args, text)

class CellBlock(Block):
    def __init__(self, args, text):
        Block.__init__(self, "cell_block", args, text)

class HeaderRow(Block):
    def __init__(self, args, text):
        Block.__init__(self, "thead", args, text)

class NamedBlockDirective(Block):
    def __init__(self, args, text):
        Block.__init__(self, "directive_block", args, text)

class RawBlock(Block):
    def __init__(self, args, text):
        Block.__init__(self, "block_raw", args, text)

class Inline(Directive):
    pass

class Cell(Inline):
    def __init__(self, args, text):
        Inline.__init__(self, "cell", args, text)

class Span(Inline):
    def __init__(self, args, text):
        Inline.__init__(self, "span", args, text)

class RawSpan(Inline):
    def __init__(self, args, text):
        Inline.__init__(self, "raw_span", args, text)

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

class Newline(Inline):
    def __init__(self, args=None, text=None):
        if args or text: raise Exception('bad')
        Inline.__init__(self, "n", [],[])

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

class NamedInlineDirective(Inline):
    def __init__(self, args, text):
        Inline.__init__(self, "directive", args, text)

block_directives = { # \foo::begin
        "hr": HorizontalRule,
        "list": ListBlock,
        "blockquote": QuoteBlock,
        "item": ItemBlock,
        "table": Table,
        "row": Row,
        "cell": CellBlock,
        "code": CodeBlock,
        "section": Section,
        "division": Division,
}
para_directives = { # \foo: ...
        "para": Paragraph,
        "p": Paragraph,
        "h": Heading,
        "list": ListBlock,
        "heading": Heading,
        "code": CodeBlock,
        "raw": RawBlock,
        "row": Row,
        "cell": Cell,
        "div": Division,
}

inline_directives = {
        "strong": Strong,
        "b": Strong,
        "br": Hardbreak,
        "n": Newline,
        "em": Emphasis,
        "emph": Emphasis,
        "emphasis": Emphasis,
        "strike": Strike,
        "code": CodeSpan,
        "code_span": CodeSpan,
        "item": ItemSpan,
        "raw": RawSpan,
        "span": Span,
        "cell": Cell,
        "nbsp": Nbsp,
}
def walk(obj, builder):
    if obj is None: 
        pass
    if obj.name == "document":
        for o in obj.text:
            walk(o, builder)
    elif obj.name == "hr":
        builder.add_hr()
    elif obj.name == "code_block":
        text = "".join(obj.text)
        builder.add_code_block(text)
    elif obj.name == "blockquote":
        with builder.build_blockquote() as b:
            for o in obj.text:
                walk(o, b)
    elif obj.name == "paragraph":
        with builder.build_para() as p:
            for word in obj.text:
                walk_inline(word, p)
    elif obj.name == "heading":
        with builder.build_heading(obj.get_arg('level')) as p:
            for word in obj.text:
                walk_inline(word, p)
    elif obj.name == "table":
        cols = len(obj.text[0].text)
        align = dict(enumerate(obj.get_arg('column_align') or ()))
        with builder.build_table(cols, align) as t:
            for row in obj.text:
                with t.add_row(heading=row.name=='thead') as b:
                    for cell in row.text:
                        if cell.name == 'cell_block':
                            with b.add_block_column() as c:
                                for x in cell.text:
                                    walk(x, c)
                        else:
                            with b.add_column() as c:
                                for x in cell.text:
                                    walk_inline(x, c)

    elif obj.name == "list":
        with builder.build_list(obj.get_arg('start'), obj.get_arg('bullet'), len(obj.text)) as l:
            for item in obj.text:
                if item.name == 'item_span':
                    with l.build_item_span() as p:
                        for word in item.text:   
                            walk_inline(word, p)
                if item.name == 'block_item':
                    with l.build_block_item() as p:
                        for word in item.text:   
                            walk(word, p)
    elif isinstance(obj, Block):
        builder.lines.append(obj.name)
        for o in obj.text:
            builder.lines.append(getattr(obj,'name',''))


def walk_inline(obj, builder, filter=None):
    if obj is None: return
    if obj == " ":
        builder.add_space()
    elif isinstance(obj, str):
        if obj:
            if filter: obj = filter(obj)
            builder.add_text(obj)
    elif obj.name == "hardbreak" or obj.name == "n":
        builder.add_break()
    elif obj.name == "nbsp":
        builder.add_text(" ")
    elif obj.name == "softbreak":
        builder.add_space()
    elif obj.name == 'code_span':
        def walk_code(obj):
            if isinstance(obj, str): return obj
            return ""
        text = "".join(walk_code(c) for c in obj.text).strip()
        builder.add_code_text(text)
    elif obj.name == 'emph':
        for o in obj.text:
            walk_inline(o, builder, filter)
    elif obj.name == 'strong':
        with builder.effect('strong') as builder:
            for o in obj.text:
                walk_inline(o, builder, filter)
    elif obj.name == 'strike':
        for o in obj.text:
            walk_inline(o, builder, filter)
    else:
        builder.add_text(f"{obj.name}{{")
        if obj.text:
            for o in obj.text:
                walk_inline(o, builder, filter)
        builder.add_text("}")



