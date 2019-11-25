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
    def __eq__(self, other):
        return (
            self.name == other.name and
            all(x == y for x,y in zip(self.args, other.args)) and
            all(x == y for x,y in zip(self.text, other.text))
        )
    def get_arg(self, key):
        if key is None:
            return [v for k,v in self.args if k is None]
        for k,v in self.args:
            if k == key: return v
    def walk(self, builder):
        pass

    def select(self, name):
        if name == self.name:
            yield self
        for o in self.text:
            if isinstance(o, str): continue
            yield from o.select(name)

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
class Aside(Block):
    name = "AsideBlock"

@elements.add()
class Warning(Block):
    name = "WarningBlock"

@elements.add()
class NoteBlock(Block):
    name = "NoteBlock"

@elements.add()
class Figure(Block):
    name = "Figure"

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
class MathBlock(Block):
    name = "MathBlock"

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
class Wordbreak(Inline):
    name ="WordBreak"

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
class NoteSpan(Inline):
    name = "NoteSpan"

@elements.add()
class Footnote(Inline):
    name = "Footnote"

@elements.add()
class Sidenote(Inline):
    name = "Sidenote"

@elements.add()
class Insertion(Inline):
    name = "Insertion"

@elements.add()
class Deletion(Inline):
    name = "Deletion"

@elements.add()
class Image(Inline):
    name = "Image"

@elements.add()
class Link(Inline):
    name = "Link"

@elements.add()
class Data(Inline):
    name = "Data"

@elements.add()
class Quote(Inline):
    name = "Quote"

@elements.add()
class MathSpan(Inline):
    name = "MathSpan"

@elements.add()
class Whitespace(Inline):
    name = "Whitespace"

@elements.add()
class CommentSpan(Element):
    name = "CommentSpan"

@elements.add()
class CommentBlock(Element):
    name = "CommentBlock"

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
        "aside": Aside,
        "warning": Warning,
        "note": NoteBlock,
        "comment": CommentBlock,
        "math": MathBlock,
        "figure": Figure,
}
para_directives = { # \foo: ...
        "para": Paragraph,
        "p": Paragraph,
        "prose": Prose,
        "h": Heading,
        "heading": Heading,
        "list": ListBlock,
        "code": CodeBlock,
        "raw": RawBlock,
        "table": Table,
        "row": Row,
        "cell": CellSpan,
        "span": Span,
        "comment": CommentSpan,
        "math": MathSpan,
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
        "wbr": Wordbreak,
        "note": NoteSpan,
        "footnote": Footnote,
        "sidenote": Sidenote,
        "ins": Insertion,
        "insertion": Insertion,
        "del": Deletion,
        "deletion": Deletion,
        "q": Quote,
        "quote": Quote,
        "img": Image,
        "a": Link,
        "link": Link,
        "data": Data,
        "comment": CommentSpan,
        "math": MathSpan,
}
def walk(obj, builder):
    if obj is None: 
        pass
    if obj.name == Document.name:
        for o in obj.text:
            walk(o, builder)
    elif obj.name == RawBlock:
        builder.add_raw(obj.text)
    elif obj.name == HorizontalRule.name:
        builder.add_hr()
    elif obj.name == CodeBlock.name:
        with builder.build_codeblock() as p:
            for word in obj.text:
                walk_inline(word, p)
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
    elif obj.name == Division.name:
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
    elif obj.name == NamedBlockDirective:
        with builder.build_directive(obj.get_arg('name'), obj.args) as b:
            for t in obj.text:
                walk(t, b)
    else:
        with builder.build_node(obj.name, obj.args) as b:
            for t in obj.text:
                walk(t, b)

def walk_inline(obj, builder, filter=None):
    if obj is None: return
    if obj == " ":
        builder.add_space(" ")
    elif isinstance(obj, str):
        if obj:
            if filter: obj = filter(obj)
            builder.add_text(obj)
    elif obj.name == RawSpan:
        builder.add_raw(obj.text)
    elif obj.name == Wordbreak.name:
        builder.add_wordbreak()
    elif obj.name == Whitespace.name:
        builder.add_space(obj.text[0]) 
    elif obj.name == Hardbreak.name or obj.name == Newline.name:
        builder.add_break()
    elif obj.name == Nbsp.name:
        builder.add_text(" ")
    elif obj.name == Softbreak.name:
        builder.add_softbreak()
    elif obj.name == Span.name:
        with builder.build_codespan() as b:
            for o in obj.text:
                walk_inline(o, b, filter)
    elif obj.name == CodeSpan.name:
        with builder.build_codespan() as b:
            for o in obj.text:
                walk_inline(o, b, filter)
    elif obj.name == Emphasis.name:
        with builder.effect('emphasis') as b:
            for o in obj.text:
                walk_inline(o, b, filter)
    elif obj.name == Strong.name:
        with builder.effect('strong') as b:
            for o in obj.text:
                walk_inline(o, b, filter)
    elif obj.name == Strikethrough.name:
        with builder.effect('strikethrough') as b:
            for o in obj.text:
                walk_inline(o, builder, filter)
    elif obj.name == Emoji.name:
        builder.add_emoji(obj.get_arg('name'))
    elif obj.name == NamedInlineDirective:
        with builder.build_directive(obj.get_args('name'), obj.args) as b:
            for o in obj.text:
                walk_inline(o, builder, filter)
    else:
        with builder.build_node(obj.name, obj.args) as b:
            for o in obj.text:
                walk_inline(o, builder, filter)

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




