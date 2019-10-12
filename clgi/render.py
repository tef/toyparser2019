from contextlib import contextmanager

from . import dom

class TextBuilder:
    pass

class LineBuilder:
    pass

class RenderBox:
    min_width = 40

    @classmethod
    def max_width(self, indent, width, height, max_w):
        if width > max_w:
            indent = (width-max_w)//2
            width = max_w
        return self(indent, width, height)

    def __init__(self, indent, width, height):
        self.indent = indent
        self.width = width
        self.height = height

    def margin(self, amount):
        new_width = max(self.width - amount*2) if self.width >= self.min_width else self.width
        new_amount = (self.width - new_width)/2
        return RenderBox(new_amount, self.width-new_amount, self.height)

    def shrink(self, scale=0.5, indent=False):
        new_width = int(max(self.width * scale, self.min_width)) if self.width >= self.min_width else self.width
        indent = (self.width - new_width)//2 if indent else 0
        return RenderBox(indent, new_width, self.height)

class Mapper:
    def __init__(self, *, mapping=(), count=-1, offset=0):
        self.mapping = mapping if mapping else []
        self.count = count
        self.offset = offset

    def add_index(self, lineno):
        lineno = lineno + self.offset
        self.mapping.append((self.count, lineno))
        self.count -=1

    def add_mapper(self, lineno, mapper):
        for i,x in mapper.mapping:
            self.add_index(x+lineno)

    def line_of(self, pos):
        count, offset, old = pos
        if count == 0: return old
        for c, line in self.mapping:
            if c == count:
                return line-offset
        return old

    def index_of(self, lineno):
        for count, line in self.mapping:
            if line >= lineno:
                return (count, line-lineno, lineno)
        return (0, 0, lineno)

class BlockBuilder:
    def __init__(self, box):
        self.lines = []
        self.mapper = Mapper()
        self.box = box
        self.count = -1
        self.mapping = {}

    def add_index(self):
        self.mapper.add_index(len(self.lines))
    def add_mapper(self, mapper):
        self.mapper.add_mapper(len(self.lines), mapper)

    def build(self):
        def indent(line):
            if len(line) <= self.box.width:
                return (" "*self.box.indent) + line
            else:
                w = self.box.indent - max(len(line) - self.box.width, 0)//2
                return (" "*w) + line
        return self.mapper, [indent(line) for line in self.lines]

    def add_code_block(self, text):
        self.add_index()
        lines = text.splitlines()
        indent = 2
        self.lines.extend((" "* indent)+line+(" "*indent) for line in lines)
        self.lines.append("")

    def add_hr(self):
        self.add_index()
        width = int(self.box.width*0.3)*2
        pad = (self.box.width - width)//2
        
        line = (" "*pad) + ("-"*width) + (" "*pad)
        self.lines.append(line)
        self.lines.append("")

    @contextmanager
    def build_blockquote(self):
        self.add_index()
        box = self.box.shrink(0.8, indent=True)
        builder = BlockBuilder(box)
        yield builder
        mapper, lines = builder.build()
        self.add_mapper(mapper)
        self.lines.extend(lines)
        self.lines.append("")

    @contextmanager
    def build_table(self, cols):
        self.add_index()
        builder = TableBuilder(self.box, cols)
        yield builder
        lines = builder.build()
        for line in lines:
            pad = max(0, self.box.width-len(line)) //2
            self.lines.append((" "*pad)+line)

        self.lines.append("")

    @contextmanager
    def build_para(self):
        self.add_index()
        box = RenderBox(0, self.box.width, self.box.height)
        builder = ParaBuilder(box)
        builder.add_space()
        yield builder
        mapper, lines= builder.build()
        self.add_mapper(mapper)
        self.lines.extend(lines)
        self.lines.append("")

    @contextmanager
    def build_heading(self, level):
        self.add_index()
        amount = [0.5, 0.6, 0.7, 0.8, 0.9, 0.9]
        box = self.box.shrink(amount[level])
        builder = ParaBuilder(box)
        yield builder
        mapper, lines = builder.build()
        self.add_mapper(mapper)
        for line in lines:
            pad = max(0, self.box.width-len(line)) //2
            self.lines.append((" "*pad)+line)
        self.lines.append("")
        self.lines.append("")

    @contextmanager
    def build_list(self, start, num):
        self.add_index()
        box = RenderBox(0, self.box.width, self.box.height)
        builder = ListBuilder(box, start, num)
        yield builder
        mapper, lines = builder.build()
        self.lines.extend(lines)
        self.add_mapper(mapper)
        self.lines.append("")

class TableBuilder:
    def __init__(self, box, cols):
        self.box = box
        self.mapper = Mapper()
        self.cols = cols
        self.rows = []


    def build(self):
        max_widths = list(0 for _ in range(self.cols))
        for r, row in enumerate(self.rows):
            for c, col in enumerate(row):
                for line in col:
                    max_widths[c] = max(max_widths[c], len(line))
        lines = []
        line = []
        line.append("+")
        for x in range(self.cols):
            pad = max_widths[x]+2
            line.append("-"*pad)
            line.append("+")
        division = "".join(line)
        lines.append(division)

        for r, row in enumerate(self.rows):
            for l in range(max(len(c) for c in row)):
                line = []
                for x, col in enumerate(row):
                    line.append("| ")
                    if l < len(col):
                        cur = col[l]
                        pad = max_widths[x]- len(cur) 
                        line.append(" "*(pad//2))
                        line.append(cur)
                        line.append(" "*(pad-pad//2))
                    else:
                        pad = max_widths[x]
                        line.append(" "*pad)


                    line.append(" ")
                line.append("|")
                lines.append("".join(line))
            lines.append(division)

        return lines

    @contextmanager
    def add_row(self):
        builder = RowBuilder(self.box, self.cols)
        yield builder
        cols = builder.build()
        self.rows.append(cols)


class RowBuilder:
    def __init__(self, box, cols):
        self.lines = []
        self.box = box
        self.width = max(10, (box.width-2) // cols)
        self.columns = []

    def build(self):
        return self.columns

    @contextmanager
    def add_column(self):
        box = RenderBox(0, self.width-2, self.box.height)
        builder = ParaBuilder(box)
        yield builder
        mapper, lines = builder.build()
        self.columns.append(lines)

    @contextmanager
    def add_block_column(self):
        box = RenderBox(0, self.width-2, self.box.height)
        builder = BlockBuilder(box)
        yield builder
        mapper, lines = builder.build()
        self.columns.append(lines)


class ListBuilder:
    def __init__(self, box, start, num):
        self.lines = []
        self.box = box
        self.mapper = Mapper()
        self.numbered = start is not None
        self.count = start if start is not None else 1
        self.width = len(str(num))+2 if self.numbered else 6

    def add_index(self):
        self.mapper.add_index(len(self.lines))

    def add_mapper(self, mapper):
        self.mapper.add_mapper(len(self.lines), mapper)

    def incr(self):
        self.count +=1
        if self.numbered:
            n = str(self.count)+". "
        else:
            n = "\u2022 "
        pad= max(0, self.width - len(n))
        return (" "*pad) + n

    def build(self):
        return self.mapper, [(" "* self.box.indent)+line for line in self.lines]

    @contextmanager
    def build_block_item(self):
        self.add_index()
        box = RenderBox(0, self.box.width-self.width, self.box.height)
        builder = BlockBuilder(box)
        yield builder
        mapper, lines = builder.build()
        self.add_mapper(mapper)
        for i, line in enumerate(lines):
            if i == 0:
                self.lines.append(self.incr() + line)
            else:
                self.lines.append((" "*self.width) + line)

    @contextmanager
    def build_item_span(self):
        self.add_index()
        box = RenderBox(0, self.box.width-self.width, self.box.height)
        builder = ParaBuilder(box)
        yield builder
        mapper, lines = builder.build()
        self.add_mapper(mapper)
        for i, line in enumerate(lines):
            if i == 0:
                self.lines.append(self.incr() + line)
            else:
                self.lines.append((" "*self.width) + line)

class ParaBuilder:
    def __init__(self, box):
        self.lines = []
        self.box = box
        self.mapper = Mapper()
        self.current_line = []
        self.current_word = []
        self.current_width = 0
        self.count = 0

    def add_index(self):
        self.mapper.add_index(len(self.lines))

    def build(self):
        self.add_break()
        return self.mapper, [(" "* self.box.indent)+line for line in self.lines]
        
    def _add_text(self, text):
        l = len(text)
        l = l +1 if self.current_line else l
        if l + self.current_width > self.box.width and self.current_width > 0:
            self._add_break()
        if self.current_line:
            self.current_line.append(" ")
        self.current_line.append(text)
        self.current_width += l

    def _add_break(self):
        self.lines.append("".join(self.current_line))
        self.current_line[:] = []
        self.current_width = 0

    def add_space(self):
        if self.current_word:
            word = "".join(self.current_word)
            self.current_word[:] = []
            self._add_text(word)
        self.whitespace = True

    def add_code_text(self, text):
        self.add_text("`")
        self.add_text(text)
        self.add_text("`")


    def add_break(self):
        self.add_space()
        self._add_break()
        self.add_index()
        self.whitespace = False

    def add_text(self, text):
        self.current_word.append(text)



def to_ansi(obj, indent, width, height):
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
            with builder.build_table(cols) as t:
                for row in obj.text:
                    with t.add_row() as b:
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
            with builder.build_list(obj.get_arg('start'), len(obj.text)) as l:
                for item in obj.text:
                    if item.name == 'item_span':
                        with l.build_item_span() as p:
                            for word in item.text:   
                                walk_inline(word, p)
                    if item.name == 'block_item':
                        with l.build_block_item() as p:
                            for word in item.text:   
                                walk(word, p)


    def walk_inline(obj, builder):
        if obj is None: return
        if obj == " ":
            builder.add_space()
        elif isinstance(obj, str):
            if obj:
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
            text = " ".join(walk_code(c) for c in obj.text).strip()
            builder.add_code_text(text)
        else:
            builder.add_text(f"{obj.name}{{")
            if obj.text:
                for o in obj.text:
                    walk_inline(o, builder)
            builder.add_text("}")
    

    box = RenderBox.max_width(indent, width, height, 90)
    builder = BlockBuilder(box)
    builder.add_index()
    walk(obj, builder)
    builder.add_index()
    return builder.build()
