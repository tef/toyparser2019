class Response:
    pass

class Plaintext(Response):
    def __init__(self, lines):
        self.lines = lines
    def render(self, width, height):
        return self.lines

class Document(Response):
    def __init__(self, obj):
        self.obj = obj

class Directive:
    def __init__(self, name, args, text):
        self.name = name
        self.args = args
        self.text = text

class Data(Directive):
    pass

class Block(Directive):
    pass

class Document(Block, Response):
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

class NamedBlockDirective(Block):
    def __init__(self, args, text):
        Block.__init__(self, "directive", args, text)

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
        "item": BlockItem,
        "table": Table,
        "row": Row,
}
para_directives = { # \foo: ...
        "para": Paragraph,
        "p": Paragraph,
        "h": Heading,
        "heading": Heading,
        "code": CodeBlock,
        "raw": RawBlock,
        "row": Row,
        "cell": Cell,
}

inline_directives = {
        "strong": Strong,
        "b": Strong,
        "em": Emphasis,
        "emph": Emphasis,
        "emphasis": Emphasis,
        "strike": Strike,
        "code": CodeSpan,
        "code_span": CodeSpan,
        "item": ItemSpan,
        "raw": RawSpan,
        "cell": Cell,
}

