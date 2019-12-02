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
            other is not None and 
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
        raise Exception('no')

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
class RawBlock(Block):
    name = "RawBlock"

    def walk(self, builder):
        builder.add_raw(self.text)

@elements.add()
class Document(Block):
    name = "Document"

    def walk(self, builder):
        with builder.build_document() as b:
            b.walk_text(self.text)

@elements.add()
class Fragment(Block):
    name = "Fragment"

    def walk(self, builder):
        with builder.build_fragment() as b:
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
class Aside(Block):
    name = "AsideBlock"

@elements.add()
class Warning(Block):
    name = "WarningBlock"


@elements.add()
class NoteBlock(Block):
    name = "NoteBlock"

    def walk(self, builder):
        with builder.build_noteblock() as b:
            b.walk_text(self.text)


@elements.add()
class Figure(Block):
    name = "Figure"

    def walk(self, builder):
        with builder.build_figure() as b:
            b.walk_text(self.text)


@elements.add()
class ListBlock(Block):
    name = "ListBlock"

    def walk(self, builder):
        with builder.build_list(self.get_arg('start'), self.get_arg('bullet'), len(self.text)) as l:
            for item in self.text:
                if item.name == ItemSpan.name:
                    with l.build_item_span() as p:
                        p.walk_text(item.text)
                if item.name == ItemBlock.name:
                    with l.build_block_item() as p:
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
        with builder.add_row() as b:
            b.walk_text(self.text)

@elements.add()
class TableHeader(Inline):
    name = "TableHeader"
    def walk(self, builder):
        with builder.add_table_header() as b:
            b.walk_text(self.text)

class TableRule(Inline):
    name = "TableRule"

@elements.add()
class CellBlock(Block):
    name = "TableCellBlock"

    def walk(self, builder):
        with builder.add_block_column() as c:
            c.walk_text(self.text)


@elements.add()
class CellSpan(Inline):
    name = "TableCellSpan"

    def walk(self, builder):
        with builder.add_column() as c:
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


@elements.add()
class Strong(Inline):
    name = "Strong"

    def walk(self, builder):
        with builder.effect('strong') as b:
            b.walk_text(self.text)


@elements.add()
class Emphasis(Inline):
    name = "Emphasis"

    def walk(self, builder):
        with builder.effect('emphasis') as b:
            b.walk_text(self.text)


@elements.add()
class Strikethrough(Inline):
    name = "Strikethrough"

    def walk(self, builder):
        with builder.effect('strikethrough') as b:
            b.walk_text(self.text)

@elements.add()
class Hardbreak(Inline):
    name ="HardBreak"

    def walk(self, builder):
        builder.add_break()


@elements.add()
class Wordbreak(Inline):
    name ="WordBreak"

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
class Nbsp(Inline):
    name = "Nbsp"

    def walk(self, builder):
        builder.add_text(" ")


@elements.add()
class Emoji(Inline):
    name = "Emoji"

    def walk(self, builder):
        builder.add_emoji(self.get_arg('name'))


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
            b.walk_text(self)


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
class Whitespace(Inline):
    name = "Whitespace"

    def walk(self, builder):
        builder.add_space(self.text[0]) 


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
        with builder.build_table(3, {0: "left"}) as t:
            with t.add_row() as r:
                with r.add_column() as c, c.effect('strong') as s:
                    s.add_text('Test')
                    s.add_space()
                    s.add_text('report:')
                with r.add_column() as c:
                    number = self.get_arg('working') or 0
                    if number is not None:
                        c.add_text('Working')
                        c.add_space()
                        c.add_text(str(number))
                with r.add_column() as c:
                    number = self.get_arg('total') or 0
                    if number is not None:
                        c.add_text('Total')
                        c.add_space()
                        c.add_text(str(number))
@elements.add()
class TestCase(Element):
    name = "TestCase"

    def __init__(self, args, text):
        self.args = args
        self.text = text

    def walk(self, builder):
        with builder.build_table(4, {0: "left"}) as t:
            with t.add_row() as r:
                with r.add_column() as c, c.effect('strong') as s:
                    s.add_text('Testcase')
                    number = self.get_arg('number')
                    if number is not None:
                        s.add_space()
                        s.add_text(str(number))
                with r.add_column() as c:
                    c.add_code_text(self.get_arg('input_text'))
                with r.add_column() as c:
                    c.add_code_text(dump(self.get_arg('output_dom')))
                with r.add_column() as c:
                    result = self.get_arg('state')
                    if result:
                        c.add_text(result)


def run_tests(doc, parse):
    tests = list(doc.select(TestCase.name))
    results = []
    success = []
    total = 0
    working = 0
    for n, test_case in enumerate(tests):
        total += 1
        raw_text = test_case.get_arg('input_text')
        output_dom = test_case.get_arg('output_dom')
        result_dom = parse(raw_text)

        if result_dom == output_dom:
            test_case.args.append( ('state', 'working'))
            working+=1
        else:
            test_case.args.append( ('state', 'failed'))
        test_case.args.append(('number', n))
    for r in list(doc.select(TestReport.name)):
        r.args.append(('total', total))
        r.args.append(('working', working))

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
        "paragraph": Paragraph,
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

def object_to_tagged(obj):
    args = {}
    args.update(obj.args)
    if obj.text:
        args['text'] = obj.text
    return obj.name, args

def tagged_to_object(name, value):
    if name in elements:
        if 'text' in value:
            text = value['text']
        else:
            text = []
        value = list(value.items())
        return elements.make(name, value, text)
    else:
        value = list(value.items())
        return Node(name, value)

codec = Codec(object_to_tagged, tagged_to_object)

dump = codec.dump
parse = codec.parse




