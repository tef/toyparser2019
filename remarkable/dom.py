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
        if other is None: return
        if isinstance(other, str): return
        if self.name != other.name: return
        text = self.text
        for x, y in self.args:
            if x == "text": text = y
            elif y != other.get_arg(x): return

        other_text = other.get_arg('text') or other.text

        if len(text) != len(other_text): return
        return all(x == y for x,y in zip(text, other_text))

    def get_arg(self, key):
        if key is None:
            return [v for k,v in self.args if k is None]
        for k,v in self.args:
            if k == key: return v

    def walk(self, builder):
        raise Exception(f'no builder for {self.__class__}')

    def select(self, name):
        if name == self.name:
            yield self
        for o in self.text:
            if isinstance(o, str): continue
            yield from o.select(name)


class Node(Element):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    @property
    def text(self):
        x = self.get_arg('text')
        return x or ()

    def walk(self, builder):
        builder.add_node(self)

class DocumentSet(Node):
    name = "DocumentSet"
    def __init__(self, args, text=None):
        self.args = args

    @property
    def text(self):
        x = self.get_arg('text')
        return x or ()

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

    def walk(self, builder):
        with builder.build_directive(self.get_arg('name'), self.args) as b:
            b.walk_text(self.text)

@elements.add()
class NamedBlockDirective(Block):
    name = "BlockDirective"

    def walk(self, builder):
        with builder.build_directive(self.get_arg('name'), self.args) as b:
            b.walk_text(self.text)

class DirectiveNode(Element):
    def __init__(self, name, args, text):
        self.name = name
        self.args = args
        self.text = text

    def walk(self, builder):
        raise Exception('bad')

@elements.add()
class DefinitionList(Block):
    name = "DefinitionList"

@elements.add()
class DefinitionBlock(Block):
    name = "DefinitionBlock"

@elements.add()
class DefinitionLabel(Inline):
    name = "DefinitionLabel"

@elements.add()
class ItemLabel(Inline):
    name = "ItemLabel"

@elements.add()
class Metadata(Block):
    name = "Metadata"

    def walk(self, builder):
        pass

@elements.add()
class RawBlock(Block):
    name = "RawBlock"

    def walk(self, builder):
        builder.add_raw(self.text)

@elements.add()
class Document(Block):
    name = "Document"

    def walk(self, builder):
        if hasattr(builder, 'build_fragment'):
            with builder.build_document() as b:
                b.walk_text(self.text)
        else:
            builder.lines.append('waaa')

@elements.add()
class Fragment(Block):
    name = "Fragment"

    def walk(self, builder):
        if hasattr(builder, 'build_fragment'):
            with builder.build_fragment() as b:
                b.walk_text(self.text)
        else:
            builder.lines.append('waaa')

@elements.add()
class InlineFragment(Inline):
    name = "InlineFragment"

    def walk(self, builder):
        with builder.build_inline_fragment() as b:
            b.walk_text(self.text)

@elements.add()
class Paragraph(Block):
    name = "Paragraph"

    def walk(self, builder):
        with builder.build_para() as b:
            for o in self.text:
                b.walk(o)

@elements.add()
class Prose(Block):
    name = "Prose"

    def walk(self, builder):
        with builder.build_prose() as b:
            for o in self.text:
                b.walk(o)

@elements.add()
class HorizontalRule(Block):
    name = "HorizontalRule"

    def walk(self, builder):
        builder.add_hr()

@elements.add()
class Section(Block):
    name = "Section"

    def walk(self, builder):
        with builder.build_section() as b:
            b.walk_text(self.text)

@elements.add()
class Division(Block):
    name = "Division"

    def walk(self, builder):
        with builder.build_division() as b:
            for o in self.text:
                b.walk(o)


@elements.add()
class Heading(Block):
    name = "Heading"

    def walk(self, builder):
        with builder.build_heading(self.get_arg('level')) as b:
            for o in self.text:
                b.walk(o)


@elements.add()
class CodeBlock(Block):
    name = "CodeBlock"

    def walk(self, builder):
        with builder.build_codeblock() as p:
            for word in self.text:
                p.walk(word)

@elements.add()
class AsideBlock(Block):
    name = "AsideBlock"

@elements.add()
class WarningBlock(Block):
    name = "WarningBlock"


@elements.add()
class NoteBlock(Block):
    name = "NoteBlock"

    def walk(self, builder):
        with builder.build_noteblock() as b:
            b.walk_text(self.text)


@elements.add()
class LinkDef(Block):
    name = "LinkDef"

    def walk(self, builder):
        pass

@elements.add()
class Figure(Block):
    name = "Figure"

    def walk(self, builder):
        with builder.build_figure() as b:
            b.walk_text(self.text)


@elements.add()
class BulletList(Block):
    name = "BulletList"

    def walk(self, builder):
        with builder.build_bullet_list(self.get_arg('bullet'), len(self.text)) as l:
            for item in self.text:
                if item.name == ItemSpan.name:
                    with l.build_item_span() as p:
                        p.walk_text(item.text)
                if item.name == ItemBlock.name:
                    with l.build_block_item() as p:
                        p.walk_text(item.text)
@elements.add()
class NumberedList(Block):
    name = "NumberedList"

    def walk(self, builder):
        with builder.build_numbered_list(self.get_arg('start'), len(self.text)) as l:
            for item in self.text:
                if item.name == ItemSpan.name:
                    with l.build_item_span() as p:
                        p.walk_text(item.text)
                if item.name == ItemBlock.name:
                    with l.build_block_item() as p:
                        p.walk_text(item.text)

@elements.add()
class TodoList(Block):
    name = "TodoList"

    def walk(self, builder):
        with builder.build_bullet_list(self.get_arg('bullet'), len(self.text)) as l:
            for item in self.text:
                checked = item.get_arg('done')
                if item.name == ItemSpan.name:
                    with l.build_item_span() as p:
                        if checked:
                            p.walk_text(["[x]", " "])
                        else:
                            p.walk_text(["[ ]", " "])
                        p.walk_text(item.text)
                if item.name == ItemBlock.name:
                    with l.build_block_item() as p:
                        if checked:
                            p.walk_text(["[x]", " "])
                        else:
                            p.walk_text(["[ ]", " "])
                        p.walk_text(item.text)
@elements.add()
class Blockquote(Block):
    name = "Blockquote"

    def walk(self, builder):
        with builder.build_blockquote() as b:
            b.walk_text(self.text)


@elements.add()
class ItemBlock(Block):
    name = "ItemBlock"

    def walk(self, builder):
        raise Exception('no')

@elements.add()
class MathBlock(Block):
    name = "MathBlock"

    def walk(self, builder):
        with builder.build_math() as b:
            b.walk_text(self.text)


@elements.add()
class Table(Block):
    name = "TableBlock"

    def walk(self, builder):
        cols = len(self.text[0].text)
        align = dict(enumerate(self.get_arg('column_align') or ()))
        with builder.build_table(cols, align) as t:
            t.walk_text(self.text)




@elements.add()
class Row(Inline):
    name = "TableRow"

    def walk(self, builder):
        with builder.build_row() as b:
            b.walk_text(self.text)

@elements.add()
class TableHeader(Inline):
    name = "TableHeader"
    def walk(self, builder):
        with builder.build_table_header() as b:
            b.walk_text(self.text)

class TableRule(Inline):
    name = "TableRule"

@elements.add()
class CellBlock(Block):
    name = "TableCellBlock"

    def walk(self, builder):
        with builder.build_block_column() as c:
            c.walk_text(self.text)


@elements.add()
class CellSpan(Inline):
    name = "TableCellSpan"

    def walk(self, builder):
        with builder.build_column() as c:
            c.walk_text(self.text)


@elements.add()
class Span(Inline):
    name = "Span"

    def walk(self, builder):
        with builder.build_span() as b:
            b.walk_text(self.text)


@elements.add()
class RawSpan(Inline):
    name = "RawSpan"

    def walk(self, builder):
        builder.add_raw(self.text)

@elements.add()
class ItemSpan(Inline):
    name = "ItemSpan"

    def walk(self, builder):
        raise Exception('no')


@elements.add()
class CodeSpan(Inline):
    name = "CodeSpan"

    def walk(self, builder):
        with builder.build_codespan() as b:
            b.walk_text(self.text)

class Effect(Inline):
    def walk(self, builder):
        with builder.effect(self.name) as b:
            b.walk_text(self.text)

@elements.add()
class SmallCaps(Effect):
    name = "SmallCaps"

@elements.add()
class Superscript(Effect):
    name = "Superscript"

@elements.add()
class Subscript(Effect):
    name = "Subscript"

@elements.add()
class Strong(Effect):
    name = "Strong"

@elements.add()
class Emphasis(Effect):
    name = "Emphasis"

@elements.add()
class Strikethrough(Effect):
    name = "Strikethrough"



@elements.add()
class Emoji(Inline):
    name = "Emoji"

    def walk(self, builder):
        builder.add_emoji(self.get_arg('name'))


@elements.add()
class Cite(Inline):
    name = "Cite"

    def walk(self, builder):
        with builder.build_cite(self.get_arg('name')) as b:
            b.walk_text(self.text)

@elements.add()
class NoteSpan(Inline):
    name = "NoteSpan"

    def walk(self, builder):
        with builder.build_note() as b:
            b.walk_text(self.text)


@elements.add()
class Footnote(Inline):
    name = "Footnote"

    def walk(self, builder):
        with builder.build_footnote() as b:
            b.walk_text(self.text)


@elements.add()
class Sidenote(Inline):
    name = "Sidenote"

    def walk(self, builder):
        with builder.build_sidenote() as b:
            b.walk_text(self.text)


@elements.add()
class Insertion(Inline):
    name = "Insertion"

    def walk(self, builder):
        with builder.build_insertion() as b:
            b.walk_text(self.text)


@elements.add()
class Deletion(Inline):
    name = "Deletion"

    def walk(self, builder):
        with builder.build_deletion() as b:
            b.walk_text(self.text)


@elements.add()
class Image(Inline):
    name = "Image"

    def walk(self, builder):
        with builder.build_image() as b:
            b.walk_text(self.text)


@elements.add()
class Link(Inline):
    name = "Link"

    def walk(self, builder):
        with builder.build_link() as b:
            b.walk_text(self.text)


@elements.add()
class Data(Inline):
    name = "Data"

    def walk(self, builder):
        with builder.build_data(self.get_arg('value')) as b:
            b.walk_text(self.text)


@elements.add()
class Quote(Inline):
    name = "Quote"

    def walk(self, builder):
        with builder.build_quote() as b:
            b.walk_text(self.text)


@elements.add()
class MathSpan(Inline):
    name = "MathSpan"

    def walk(self, builder):
        with builder.build_section() as b:
            for o in self.text:
                b.walk(o)
        for o in self.text:
            o.walk(builder)

@elements.add()
class NamedEntity(Inline):
    name = "NamedEntity"

    def walk(self, builder):
        builder.add_named_entity(self.text[0])

@elements.add()
class Codepoint(Inline):
    name = "Codepoint"

    def walk(self, builder):
        builder.add_text(chr(self.get_arg('n')))


@elements.add()
class Whitespace(Inline):
    name = "Whitespace"

    def walk(self, builder):
        builder.add_space(self.text[0]) 

@elements.add()
class Nbsp(Inline):
    name = "Nbsp"

    def walk(self, builder):
        builder.add_text(" ")


@elements.add()
class Hardbreak(Inline):
    name ="Hardbreak"

    def walk(self, builder):
        builder.add_break()

@elements.add()
class Wordbreak(Inline):
    name ="Wordbreak"

    def walk(self, builder):
        builder.add_wordbreak()

@elements.add()
class Newline(Inline):
    name = "Newline"

    def walk(self, builder):
        builder.add_break()

@elements.add()
class Softbreak(Inline):
    name = "Softbreak"

    def walk(self, builder):
        builder.add_softbreak()


@elements.add()
class CommentSpan(Element):
    name = "CommentSpan"

    def walk(self, builder):
        with builder.build_comment() as b:
            b.walk_text(self.text)


@elements.add()
class CommentBlock(Element):
    name = "CommentBlock"

    def walk(self, builder):
        with builder.build_comment() as b:
            b.walk_text(self.text)

@elements.add()
class TestReport(Element):
    name = "TestReport"

    def __init__(self, args, text):
        self.args = args
        self.text = text

    def walk(self, builder):
        builder.walk_text(self.text)

@elements.add()
class TestCase(Element):
    name = "TestCase"

    def __init__(self, args, text):
        self.args = args
        self.text = text

    def walk(self, builder):
        builder.walk_text(self.text)

# ---

def list_directive(args, text):
    if any('start' == x[0] for x in args):
        return NumberedList(args, text)
    return BulletList(args, text)

block_directives = { # \foo::begin
        "hr": HorizontalRule,
        "list": list_directive,
        "ol": NumberedList,
        "ul": BulletList,
        "blockquote": Blockquote,
        "item": ItemBlock,
        "table": Table,
        "row": Row,
        "cell": CellBlock,
        "code": CodeBlock,
        "section": Section,
        "division": Division,
        "aside": AsideBlock,
        "warning": WarningBlock,
        "note": NoteBlock,
        "comment": CommentBlock,
        "math": MathBlock,
        "figure": Figure,
        "TestCase": TestCase,
        "TestReport": TestReport,
        "metadata": Metadata,
        "document": Document,
        "documentset": DocumentSet,
        "fragment": Fragment,
        "todo": TodoList,
        "linkdef": LinkDef,
}
para_directives = { # \foo: ...
        "paragraph": Paragraph,
        "para": Paragraph,
        "p": Paragraph,
        "prose": Prose,
        "h": Heading,
        "heading": Heading,
        "list": list_directive,
        "ul": BulletList,
        "ol": NumberedList,
        "code": CodeBlock,
        "raw": RawBlock,
        "table": Table,
        "row": Row,
        "cell": CellSpan,
        "span": Span,
        "comment": CommentBlock,
        "math": MathBlock,
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
entities = {}

def named_entity(name):
    return NamedEntity([('name', name)], [entities[name]])

def named_block_directive(name, args, text):
    if name in para_directives:
        return para_directives[name](args, text)
    elif name in block_directives:
        return block_directives[name](args, text)
    elif name in entities:
        return named_entity(name)
    else:
        return NamedBlockDirective([('name', name)] + args, text)

def named_inline_directive(name, args, text):
    if name in inline_directives:
        return inline_directives[name](args, text)
    return NamedInlineDirective([('name', name)]+ args, text)
def _parse_args(args):
    if isinstance(args, dict):
        text = args.pop('text') if 'text' in args else []
        return list(args.items()), text
    elif isinstance(args, str):
        return [], [args]
    else:
        raise Exception("What")


def named_rson_block(name, args):
    if name in elements:
        args, text = _parse_args(args)
        return elements.make(name, args, text)
    else:
        args, text = _parse_args(args)
        return Node(name, args)

def object_to_tagged(obj):
    try:
        args = {}
        if obj.text:
            args['text'] = obj.text
        args.update(obj.args)
        return obj.name, args
    except:
        print(obj, obj.name, obj.args, obj.text)
        raise

def tagged_to_object(name, value):
    if name in elements:
        value, text = _parse_args(value)
        return elements.make(name, value, text)
    else:
        value = list(value.items())
        return Node(name, value)

codec = Codec(object_to_tagged, tagged_to_object)

dump = codec.dump
parse = codec.parse




