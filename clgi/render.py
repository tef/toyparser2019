from contextlib import contextmanager

from . import dom

class TextBuilder:
    pass

class LineBuilder:
    pass

class RenderBox:
    min_width = 40

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
        return self.mapper, [(" "* self.box.indent)+line for line in self.lines]

    def add_code_block(self, text):
        self.add_index()
        lines = text.splitlines()
        indent = 4
        self.lines.extend((" "* indent)+line for line in lines)
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
        if l + self.current_width > self.box.width:
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
        if obj == " ":
            builder.add_space()
        elif isinstance(obj, str):
            if obj:
                builder.add_text(obj)
        elif obj.name == "hardbreak" or obj.name == "n":
            builder.add_break()
        elif obj.name == "softbreak":
            builder.add_space()
        elif obj.name == 'code_span':
            text = " ".join(obj.text).strip()
            builder.add_code_text(text)
        else:
            builder.add_text(f"{obj.name}{{")
            for o in obj.text:
                walk_inline(o, builder)
            builder.add_text("}")
    

    if width > 80:
        indent = (width-80)//2
        width = 80
    box = RenderBox(indent, width, height)
    builder = BlockBuilder(box)
    builder.add_index()
    walk(obj, builder)
    builder.add_index()
    return builder.build()
