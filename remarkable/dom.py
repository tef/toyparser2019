from .rson import Codec

class Registry:
    def __init__(self):
        self.classes = {}
        self.names = {}

    def add(self):
        def _wrapper(cls):
            self.register(cls.name, cls)
            return cls
        return _wrapper

    def __contains__(self, name):
        return name in self.classes

    def make(self, name, args, text):
        return self.classes[name](args, text)
    
    def register(self, name, cls):
        if name in self.classes or cls in self.names:
            raise Exception('no')
        self.classes[name] = cls
        self.names[cls] = name


elements = Registry()

class Element:
    def get_arg(self, key):
        if key is None:
            return [v for k,v in self.args if k is None]
        for k,v in self.args:
            if k == key: return v

class Node(Element):
    def __init__(self, name, args, text):
        self.name = name
        self.args = args
        self.text = text

class Block(Element):
    def __init__(self, args, text):
        self.args = args
        self.text = text

class Inline(Element):
    def __init__(self, args, text):
        self.args = args
        self.text = text

@elements.add()
class NamedInlineDirective(Inline):
    name = "InlineDirective"
    def __init__(self, name, args, text):
        args = args + [('name', name)]
        Inline.__init__(self, args, text)

@elements.add()
class NamedBlockDirective(Block):
    name = "BlockDirective"
    def __init__(self, name, args, text):
        args = args + [('name', name)]
        Block.__init__(self, args, text)

@elements.add()
class RawBlock(Block):
    name = "RawBlock"

@elements.add()
class Document(Block):
    name = "Document"

@elements.add()
class Paragraph(Block):
    name = "Paragraph"

@elements.add()
class Prose(Block):
    name = "Prose"
    def __init__(self, args, text):
        Block.__init__(self, "prose", args, text)

@elements.add()
class HorizontalRule(Block):
    name = "HorizontalRule"

@elements.add()
class Section(Block):
    name = "Section"

@elements.add()
class Division(Block):
    name = "Division"

@elements.add()
class Heading(Block):
    name = "Heading"

@elements.add()
class CodeBlock(Block):
    name = "CodeBlock"

@elements.add()
class ListBlock(Block):
    name = "ListBlock"

@elements.add()
class Blockquote(Block):
    name = "Blockquote"

@elements.add()
class ItemBlock(Block):
    name = "ItemBlock"

@elements.add()
class Table(Block):
    name = "TableBlock"

@elements.add()
class Row(Inline):
    name = "TableRow"

@elements.add()
class TableHeader(Inline):
    name = "TableHeader"

@elements.add()
class TableRule(Inline):
    name = "TableRule"

@elements.add()
class CellBlock(Block):
    name = "TableCellBlock"

@elements.add()
class CellSpan(Inline):
    name = "TableCellSpan"

@elements.add()
class Span(Inline):
    name = "Span"

@elements.add()
class RawSpan(Inline):
    name = "RawSpan"

@elements.add()
class ItemSpan(Inline):
    name = "ItemSpan"

@elements.add()
class CodeSpan(Inline):
    name = "CodeSpan"

@elements.add()
class Strong(Inline):
    name = "Strong"

@elements.add()
class Emphasis(Inline):
    name = "Emphasis"

@elements.add()
class Strikethrough(Inline):
    name = "Strikethrough"

@elements.add()
class Hardbreak(Inline):
    name ="HardBreak"


@elements.add()
class Newline(Inline):
    name = "Newline"

@elements.add()
class Softbreak(Inline):
    name = "Softbreak"

@elements.add()
class Nbsp(Inline):
    name = "Nbsp"

@elements.add()
class Emoji(Inline):
    name = "Emoji"

@elements.add()
class Whitespace(Inline):
    name = "Whitespace"


block_directives = { # \foo::begin
        "hr": HorizontalRule,
        "list": ListBlock,
        "blockquote": Blockquote,
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
        "heading": Heading,
        "list": ListBlock,
        "code": CodeBlock,
        "raw": RawBlock,
        "table": Table,
        "row": Row,
        "cell": CellSpan,
        "span": Span,
}

inline_directives = {
        "strong": Strong,
        "b": Strong,
        "br": Hardbreak,
        "n": Newline,
        "em": Emphasis,
        "emph": Emphasis,
        "emphasis": Emphasis,
        "strike": Strikethrough,
        "code": CodeSpan,
        "item": ItemSpan,
        "raw": RawSpan,
        "span": Span,
        "cell": CellSpan,
        "nbsp": Nbsp,
}
def walk(obj, builder):
    if obj is None: 
        pass
    if obj.name == Document.name:
        for o in obj.text:
            walk(o, builder)
    elif obj.name == HorizontalRule.name:
        builder.add_hr()
    elif obj.name == CodeBlock.name:
        text = "".join(obj.text)
        builder.add_code_block(text)
    elif obj.name == Blockquote.name:
        with builder.build_blockquote() as b:
            for o in obj.text:
                walk(o, b)
    elif obj.name == Paragraph.name:
        with builder.build_para() as p:
            for word in obj.text:
                walk_inline(word, p)
    elif obj.name == Prose.name:
        with builder.build_para(prose=True) as p:
            for word in obj.text:
                walk_inline(word, p)
    elif obj.name == Heading.name:
        with builder.build_heading(obj.get_arg('level')) as p:
            for word in obj.text:
                walk_inline(word, p)
    elif obj.name == Section.name:
        with builder.build_section() as b:
            for o in obj.text:
                walk(o, b)

    elif obj.name ==  Table.name:
        cols = len(obj.text[0].text)
        align = dict(enumerate(obj.get_arg('column_align') or ()))
        with builder.build_table(cols, align) as t:
            for row in obj.text:
                with t.add_row(heading=(row.name==TableHeader.name)) as b:
                    for cell in row.text:
                        if cell.name == CellBlock.name:
                            with b.add_block_column() as c:
                                for x in cell.text:
                                    walk(x, c)
                        else:
                            with b.add_column() as c:
                                for x in cell.text:
                                    walk_inline(x, c)

    elif obj.name == ListBlock.name:
        with builder.build_list(obj.get_arg('start'), obj.get_arg('bullet'), len(obj.text)) as l:
            for item in obj.text:
                if item.name == ItemSpan.name:
                    with l.build_item_span() as p:
                        for word in item.text:   
                            walk_inline(word, p)
                if item.name == ItemBlock.name:
                    with l.build_block_item() as p:
                        for word in item.text:   
                            walk(word, p)
    elif isinstance(obj, Block):
        builder.lines.append(obj.name)
        for o in obj.text:
            builder.lines.append(getattr(o,'name',''))


def walk_inline(obj, builder, filter=None):
    if obj is None: return
    if obj == " ":
        builder.add_space()
    elif isinstance(obj, str):
        if obj:
            if filter: obj = filter(obj)
            builder.add_text(obj)
    elif obj.name == Hardbreak.name:
        builder.add_break()
    elif obj.name == Nbsp.name:
        builder.add_text(" ")
    elif obj.name == Softbreak.name:
        builder.add_space()
    elif obj.name == CodeSpan.name:
        def walk_code(obj):
            if isinstance(obj, str): return obj
            return ""
        text = "".join(walk_code(c) for c in obj.text).strip()
        builder.add_code_text(text)
    elif obj.name == Emphasis.name:
        for o in obj.text:
            walk_inline(o, builder, filter)
    elif obj.name == Strong.name:
        with builder.effect('strong') as b:
            for o in obj.text:
                walk_inline(o, builder, filter)
    elif obj.name == Strikethrough.name:
        for o in obj.text:
            walk_inline(o, builder, filter)
    elif obj.name == Emoji.name:
        builder.add_text(":")
        for o in obj.text:
            walk_inline(o, builder, filter)
        builder.add_text(":")
    else:
        raise Exception(obj.name)
        builder.add_text(f"{obj.name}{{")
        if obj.text:
            for o in obj.text:
                walk_inline(o, builder, filter)
        builder.add_text("}")

def object_to_tagged(obj):
    args = {}
    args.update(obj.args)
    if obj.text:
        args['text'] = obj.text
    return obj.name, args

def tagged_to_object(name, value):
    if 'text' in value:
        text = value['text']
    else:
        text = []
    value = list(value.items())
    if name in elements:
        return elements.make(name, value, text)
    else:
        return Node(name, value, text)

codec = Codec(object_to_tagged, tagged_to_object)

dump = codec.dump
parse = codec.parse




