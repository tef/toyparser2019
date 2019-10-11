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
        new_width = (self.width - amount*2, self.min_width)
        new_amount = (self.width - new_width)/2
        return RenderBox(self.indent+new_amount, self.width-new_amount, self._height)

class BlockBuilder:
    def __init__(self, box):
        self.lines = []
        self.box = box

    def build(self):
        return [(" "* self.box.indent)+line for line in self.lines]

    def add_hr(self):
        width = int(self.box.width*0.3)*2
        pad = (self.box.width - width)//2
        
        line = (" "*pad) + ("-"*width) + (" "*pad)
        self.lines.append(line)
        self.lines.append("")

    @contextmanager
    def build_para(self):
        box = RenderBox(0, self.box.width, self.box.height)
        builder = ParaBuilder(box)
        yield builder
        self.lines.extend(builder.build())
        self.lines.append("")

class ParaBuilder:
    def __init__(self, box):
        self.lines = []
        self.box = box
        self.current_line = []
        self.current_width = 0
        self.whitespace = True

    def build(self):
        self.add_break()
        return [(" "* self.box.indent)+line for line in self.lines]
        
    def add_text(self, text):
        l = len(text)
        if l + self.current_width > self.box.width:
            self.add_break()
        self.current_line.append(text)
        self.current_width += l
        self.whitespace = False

    def add_space(self):
        if not self.whitespace:
            if self.current_width + 1 >= self.box.width:
                self.add_break()
            else:
                self.current_line.append(" ")
                self.current_width += 1
                self.whitespace = True

    def add_break(self):
        self.lines.append("".join(self.current_line))
        self.current_line[:] = []
        self.current_width = 0
        self.whitespace = True


def render(obj, indent, width, height):
    if isinstance(obj, (list, tuple)):
        return obj
    if isinstance(obj, dom.Document):
        return to_ansi(obj, indent, width, height)
    if isinstance(obj, dom.Plaintext):
        return obj.lines.splitlines()
    if isinstance(obj, str):
        return obj
    return obj.render(width=width, height=height)



def to_ansi(obj, indent, width, height):
    def walk(obj, builder):
        if obj is None: 
            pass
        if obj.name == "document":
            for o in obj.text:
                walk(o, builder)
        elif obj.name == "hr":
            builder.add_hr()
        elif obj.name == "paragraph":
            with builder.build_para() as p:
                p.add_space()
                for word in obj.text:
                    walk_inline(word, p)

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
        else:
            builder.add_word(f"{obj.name}{{")
            for o in obj.text:
                walk_inline(o, builder)
            builder.add_word("}")

    if width > 80:
        indent = (width-80)//2
        width = 80
    box = RenderBox(indent, width, height)
    builder = BlockBuilder(box)
    walk(obj, builder)
    return builder.build()
