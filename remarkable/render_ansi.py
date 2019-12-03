from contextlib import contextmanager

from . import dom

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

    def zero(self):
        return RenderBox(0, self.width, self.height)

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
        before_c, after_c, percent, old = pos
        before_l = None
        after_l = None
        for count, line in self.mapping:
            if count <= before_c:
                before_l = line
            elif count >= after_c:
                after_l = line
                break
        if after_l and before_l:
            return before_l + int((after_l-before_l)*percent)

        return old

    def index_of(self, lineno):
        before_c, before_l = self.mapping[0]
        after_c, after_l = self.mapping[-1]
        for count, line in self.mapping:
            if line <= lineno:
                before_c, before_l = count, line
            elif line > lineno:
                after_c, after_l = count, line
                break
        percent = max(0, lineno-before_l) / max(1, after_l-before_l)
        return (before_c, after_c, percent, lineno)

to_monospace = dict()
to_monospace.update(zip(range(ord('a'), ord('z')+1),range(0x1d68a, 0x1d6a4+1)))
to_monospace.update(zip(range(ord('A'), ord('Z')+1),range(0x1d670, 0x1d689+1)))

to_sans_bold = dict()
to_sans_bold.update(zip(range(ord('a'), ord('z')+1),range(0x1d5ee, 0x1d607+1)))
to_sans_bold.update(zip(range(ord('A'), ord('Z')+1),range(0x1d5d4, 0x1d5ed+1)))

to_sans_italic = dict()
to_sans_italic.update(zip(range(ord('a'), ord('z')+1),range(0x1d622, 0x1d63b+1)))
to_sans_italic.update(zip(range(ord('A'), ord('Z')+1),range(0x1d608, 0x1d621+1)))

class Box:
    top_left  = "\u250c"
    top_right = "\u2510"
    bot_left  = "\u2514"
    bot_right = "\u2518"
    horizontal= "\u2500"
    vertical  = "\u2502"
    cross     = "\u253c"
    top_mid   = "\u252c"
    bot_mid   = "\u2534"
    left_mid  = "\u251c"
    right_mid = "\u2524"

    top_left_bold = "\u250F"
    top_mid_bold = "\u2533"
    top_mid_left_bold = "\u2531"
    top_right_bold = "\u2513"
    left_mid_top_bold = "\u2521"
    cross_top_bold = "\u2547"
    right_mid_top_bold = "\u2529"
    horizontal_bold = "\u2501"
    vertical_bold = "\u2503"
    left_mid_bold = "\u2523"
    cross_bold = "\u254b"
    cross_bold_left = "\u2549"
    bot_left_bold = "\u2517"
    bot_mid_left_bold = "\u2539"
    bot_mid_left_bold = "\u2539"

    @classmethod
    def top_line(cls, col_widths, pad):
        out = []
        for n, col in enumerate(col_widths):
            out.append(cls.top_left if n == 0 else cls.top_mid)
            out.append(cls.horizontal* (col+pad))
        out.append(cls.top_right)
        return "".join(out)

    @classmethod
    def mid_line(cls, col_widths, pad):
        out = []
        for n, col in enumerate(col_widths):
            out.append(cls.left_mid if n == 0 else cls.cross)
            out.append(cls.horizontal* (col+pad))
        out.append(cls.right_mid)
        return "".join(out)

    @classmethod
    def bot_line(cls, col_widths, pad):
        out = []
        for n, col in enumerate(col_widths):
            out.append(cls.bot_left if n == 0 else cls.bot_mid)
            out.append(cls.horizontal* (col+pad))
        out.append(cls.bot_right)
        return "".join(out)
    @classmethod
    def sideways_top_line(cls, col_widths, pad):
        out = []
        for n, col in enumerate(col_widths[:-1]):
            out.append(cls.top_left_bold if n == 0 else cls.top_mid_bold)
            out.append(cls.horizontal_bold* (col+pad))
        out.append(cls.top_mid_left_bold)
        out.append(cls.horizontal* (col_widths[-1]+pad))
        out.append(cls.top_right)
        return "".join(out)

    @classmethod
    def sideways_mid_line(cls, col_widths, pad):
        out = []
        for n, col in enumerate(col_widths[:-1]):
            out.append(cls.left_mid_bold if n == 0 else cls.cross_bold)
            out.append(cls.horizontal_bold* (col+pad))
        out.append(cls.cross_bold_left)
        out.append(cls.horizontal* (pad+col_widths[-1]))
        out.append(cls.right_mid)
        return "".join(out)

    @classmethod
    def sideways_bot_line(cls, col_widths, pad):
        out = []
        for n, col in enumerate(col_widths[:-1]):
            out.append(cls.bot_left_bold if n == 0 else cls.bot_mid_bold)
            out.append(cls.horizontal_bold* (col+pad))
        out.append(cls.bot_mid_left_bold)
        out.append(cls.horizontal* (col_widths[-1]+pad))
        out.append(cls.bot_right)
        return "".join(out)

    @classmethod
    def head_top_line(cls, col_widths, pad):
        out = []
        for n, col in enumerate(col_widths):
            out.append(cls.top_left_bold if n == 0 else cls.top_mid_bold)
            out.append(cls.horizontal_bold* (col+pad))
        out.append(cls.top_right_bold)
        return "".join(out)

    @classmethod
    def head_mid_line(cls, col_widths, pad):
        out = []
        for n, col in enumerate(col_widths):
            out.append(cls.left_mid if n == 0 else cls.cross)
            out.append(cls.horizontal* (col+pad))
        out.append(cls.right_mid)
        return "".join(out)
    @classmethod
    def head_bot_line(cls, col_widths, pad):
        out = []
        for n, col in enumerate(col_widths):
            out.append(cls.left_mid_top_bold if n == 0 else cls.cross_top_bold)
            out.append(cls.horizontal_bold* (col+pad))
        out.append(cls.right_mid_top_bold)
        return "".join(out)
BULLETS = ["\u2022", "\u25e6"]

def line_len(text):
    return len(text)-4*(text.count("\x1b[0m")+text.count("\x1b[1m"))

class DocumentBuilder:
    def __init__(self, settings, box):
        self.settings = settings
        self.box = box
        self.lines = []
        self.mapper = Mapper()

    @contextmanager
    def build_fragment(self):
        self.add_index()
        builder = BlockBuilder(self.settings, self.box.zero())
        yield builder
        mapper, lines = builder.build()
        self.add_mapper(mapper)
        self.lines.extend(lines)
        self.lines.append("")

    @contextmanager
    def build_document(self):
        self.add_index()
        builder = BlockBuilder(self.settings, self.box.zero())
        yield builder
        mapper, lines = builder.build(indent=False)
        self.add_mapper(mapper)
        self.lines.extend(lines)
        self.lines.append("")
        
    def build(self, indent=True):
        if indent:
            def _indent(line):
                w = self.box.indent
                if line_len(line) > self.box.width:
                    w = w - max(line_len(line) - self.box.width, 0)//2
                if '\x1b#' in line:
                    w = w//2
                return (" "*w) + line
            return self.mapper, [_indent(line) for line in self.lines]
        return self.mapper, self.lines

    @contextmanager
    def build_fragment(self):
        self.add_index()
        builder = BlockBuilder(self.settings, self.box.zero())
        yield builder
        mapper, lines = builder.build(indent=False)
        self.add_mapper(mapper)
        self.lines.extend(lines)
        self.lines.append("")

    def add_index(self):
        self.mapper.add_index(len(self.lines))
    def add_mapper(self, mapper):
        self.mapper.add_mapper(len(self.lines), mapper)

class BlockBuilder:
    def __init__(self, settings, box):
        self.settings = settings
        self.lines = []
        self.mapper = Mapper()
        self.box = box
        self.count = -1
        self.mapping = {}

    def add_index(self):
        self.mapper.add_index(len(self.lines))
    def add_mapper(self, mapper):
        self.mapper.add_mapper(len(self.lines), mapper)

    def walk(self, text):
        text.walk(self)

    def walk_text(self, text):
        for x in text:
            self.walk(x)

        
    def build(self, indent=True):
        if indent:
            def _indent(line):
                w = self.box.indent
                if line_len(line) > self.box.width:
                    w = w - max(line_len(line) - self.box.width, 0)//2
                if '\x1b#' in line:
                    w = w//2
                return (" "*w) + line
            return self.mapper, [_indent(line) for line in self.lines]
        return self.mapper, self.lines

    def add_hr(self):
        self.add_index()
        width = int(self.box.width*0.3)*2
        pad = (self.box.width - width)//2
        
        line = (" "*pad) + ("-"*width) + (" "*pad)
        self.lines.append(line)
        self.lines.append("")

    def add_raw(self, text):
        self.lines.extend(text.splitlines())

    @contextmanager
    def build_division(self):
        self.add_index()
        builder = BlockBuilder(self.settings, self.box)
        yield builder
        mapper, lines = builder.build(indent=False)
        self.add_mapper(mapper)
        self.lines.extend(lines)
        self.lines.append("")

    @contextmanager
    def build_section(self):
        self.add_index()
        builder = BlockBuilder(self.settings, self.box)
        yield builder
        mapper, lines = builder.build(indent=False)
        self.add_mapper(mapper)
        self.lines.extend(lines)
        self.lines.append("")

    def add_node(self, obj):
        self.add_index()
        self.lines.append(dom.dump(obj))
        self.lines.append("")

    @contextmanager
    def build_directive(self, name, args):
        self.add_index()
        builder = BlockBuilder(self.settings, self.box.indent())
        self.lines.append("\\{name}:")
        yield builder
        mapper, lines = builder.build(indent=False)
        self.add_mapper(mapper)
        self.lines.extend(lines)
        self.lines.append("")

    @contextmanager
    def build_blockquote(self):
        self.add_index()
        box = self.box.shrink(0.8)
        box.indent = (self.box.width-box.width)//2
        builder = BlockBuilder(self.settings, box)
        yield builder
        width = max(line_len(l) for l in builder.lines)
        mapper, lines = builder.build()
        pad = (box.width - width)
        mark_line = (" "*(pad//2+box.indent)) + ("-"*width) + (" "*(pad-pad//2))
        self.lines.append(mark_line)
        self.lines.append("")
        self.add_mapper(mapper)
        for line in lines:
            pad = (box.width - line_len(line))
            self.lines.append((" "*(pad//2)) + line + (" "*(pad-pad//2)))
        self.lines.append(mark_line)
        self.lines.append("")

    @contextmanager
    def build_table(self, cols, align):
        self.add_index()
        builder = TableBuilder(self.settings, self.box, cols, align)
        yield builder
        mapper, lines = builder.build()
        self.add_mapper(mapper)
        for line in lines:
            pad = max(0, self.box.width-line_len(line)) //2
            self.lines.append((" "*pad)+line)

        self.lines.append("")

    @contextmanager
    def build_codeblock(self):
        self.add_index()
        box = RenderBox(2, self.box.width-2, self.box.height)
        builder = ParaBuilder(self.settings, box, prose=True)
        yield builder
        mapper, lines= builder.build()
        self.add_mapper(mapper)
        max_width = len(max(lines, key=len))
        lines = [line + (" "*(max_width-len(line))) for line in lines]
        self.lines.extend(lines)
        self.lines.append("")

    def build_prose(self, prose=True):
        return self.build_para(prose=prose)

    @contextmanager
    def build_para(self, prose=False):
        self.add_index()
        box = RenderBox(0, self.box.width, self.box.height)
        builder = ParaBuilder(self.settings, box, prose=prose)
        yield builder
        mapper, lines= builder.build()
        self.add_mapper(mapper)
        self.lines.extend(lines)
        self.lines.append("")

    @contextmanager
    def build_heading(self, level):
        self.add_index()
        amount = [0.5, 0.6, 0.7, 0.8, 0.9, 0.9]
        if self.settings.get("double") and self.box.width >40:
            # wings = "*" *(6-level)
            box = self.box.shrink(amount[level])
            box.width = box.width //2
            # box.width = a2*line_len(wings)+2
            builder = ParaBuilder(self.settings, box)
            yield builder
            mapper, lines = builder.build()
            self.add_mapper(mapper)
            for line in lines:
                pad = max(0, self.box.width-(line_len(line)*2))//2 # -2*line_len(wings)-2) 
                line = ((" "*(pad//2)) + line + (" " * (pad-pad//2)) )
                # line = wings +" " + line + " "+wings
                self.lines.append("\x1b#3"+ line)
                self.lines.append("\x1b#4"+ line)
        else:
            wings = "*" *(6-level)
            box = self.box.shrink(amount[level])
            box.width -= 2*line_len(wings)+2
            builder = ParaBuilder(self.settings, box)
            yield builder
            mapper, lines = builder.build()
            self.add_mapper(mapper)
            for line in lines:
                pad = max(0, self.box.width-line_len(line) -2*line_len(wings)-2) 
                line = ((" "*(pad//2)) + line + (" " * (pad-pad//2)) )
                line = wings +" " + line + " "+wings
                self.lines.append(line)

        self.lines.append("")

    @contextmanager
    def build_list(self, start, bullet, num):
        self.add_index()
        box = RenderBox(0, self.box.width, self.box.height)
        builder = ListBuilder(self.settings, box, start, bullet, num)
        yield builder
        mapper, lines = builder.build()
        self.lines.extend(lines)
        self.add_mapper(mapper)
        self.lines.append("")
    

class TableBuilder:
    def __init__(self, settings, box, cols, align):
        self.settings = settings
        self.box = box
        self.mapper = Mapper()
        self.cols = cols
        self.rows = []
        self.headings = []
        self.align = align

    def add_index(self, lines):
        self.mapper.add_index(len(lines))

    def walk(self, text):
        text.walk(self)

    def walk_text(self, text):
        for x in text:
            self.walk(x)

    def build(self):
        max_widths = list(0 for _ in range(self.cols))
        for r, row in enumerate(self.headings + self.rows):
            for c, col in enumerate(row):
                for line in col:
                    max_widths[c] = max(max_widths[c], line_len(line))
        total_width = sum(max_widths)+3*len(max_widths)+1

        sideways = False
        headings = len(self.headings)
        if total_width  > self.settings['width']:
            headers_width = [max(max(line_len(l) for l in c) for c in r) for r in self.headings]
            max_width_rows = max(max(max(line_len(l) for l in c) for c in r) for r in self.rows)
            max_width_header = max(headers_width) if headers_width else 0
            if max_width_header + max_width_rows + 7 < total_width:
                new_rows = []
                for r in self.rows:
                    x = self.headings +[r] 
                    new_rows.extend(zip(*x))
                    new_rows.append(None)
                if new_rows[-1] is None: new_rows.pop()
                self.cols = len(self.headings) + 1
                self.rows = new_rows
                self.headings = []
                max_widths = headers_width + [max_width_rows]
                sideways = True
                if headings:
                    self.align = dict(enumerate((["left"] * headings) + ["right"], 0))
                else:
                    self.align = dict(enumerate(["left"], 0))


        lines = []
        if sideways and headings:
            top_line = Box.sideways_top_line(max_widths, 2)
            mid_line = Box.sideways_mid_line(max_widths, 2)
            bot_line = Box.sideways_bot_line(max_widths, 2)
        else:
            head_top_line = Box.head_top_line(max_widths, 2)
            head_mid_line = Box.head_mid_line(max_widths, 2)
            head_bot_line = Box.head_bot_line(max_widths, 2)
            top_line = Box.top_line(max_widths, 2)
            mid_line = Box.mid_line(max_widths, 2)
            bot_line = Box.bot_line(max_widths, 2)


        last_null = False
        for r, row in enumerate(self.headings + self.rows):
            if sideways:
                if row is None:
                    if r > 0: lines.append(bot_line)
                    last_null = True
                    continue
                if r == 0:
                    self.add_index(lines)
                    lines.append(top_line)
                elif last_null:
                    self.add_index(lines)
                    lines.append(top_line)
                else:
                    lines.append(mid_line)
                last_null = False
            elif self.headings:
                if r == 0:
                    self.add_index(lines)
                    lines.append(head_top_line)
                elif r < len(self.headings):
                    lines.append(head_mid_line)
                elif r == len(self.headings):
                    lines.append(head_bot_line)
                else:
                    self.add_index(lines)
                    lines.append(mid_line)
            else:
                if r == 0:
                    lines.append(top_line)
                else:
                    lines.append(mid_line)

            for l in range(max(len(c) for c in row)):
                line = []
                for x, col in enumerate(row):
                    if (sideways or r < len(self.headings)) and headings >0:
                        line.append(Box.vertical_bold+" ")
                    else:
                        line.append(Box.vertical+" ")
                    if l < len(col):
                        cur = col[l]
                        pad = max_widths[x]- line_len(cur) 
                        align = self.align.get(x, "default")
                        if align == "left":
                            line.append(cur)
                            line.append(" "*pad)
                        elif align == "right":
                            line.append(" "*pad)
                            line.append(cur)
                        else:
                            line.append(" "*(pad//2))
                            line.append(cur)
                            line.append(" "*(pad-pad//2))
                    else:
                        pad = max_widths[x]
                        line.append(" "*pad)


                    line.append(" ")
                if r < len(self.headings):
                    line.append(Box.vertical_bold)
                else:
                    line.append(Box.vertical)
                lines.append("".join(line))
        lines.append(bot_line)

        return self.mapper, lines

    def build_table_header(self,heading = True):
        return self.build_row(heading=heading)

    @contextmanager
    def build_row(self,heading = False):
        builder = RowBuilder(self.settings, self.box, self.cols)
        yield builder
        cols = builder.build()
        if heading:
            cols = [[f"\x1b[1m{line}\x1b[0m" for line in lines] for lines in cols]
            self.headings.append(cols)
        else:
            self.rows.append(cols)


class RowBuilder:
    def __init__(self, settings, box, cols):
        self.settings = settings
        self.lines = []
        self.box = box
        self.width = max(1, (box.width-2) // cols)
        self.columns = []

    def build(self):
        return self.columns

    def walk(self, text):
        text.walk(self)

    def walk_text(self, text):
        for x in text:
            self.walk(x)

    @contextmanager
    def build_column(self):
        box = RenderBox(0, self.width-4, self.box.height)
        builder = ParaBuilder(self.settings, box)
        yield builder
        mapper, lines = builder.build()
        self.columns.append(lines)

    @contextmanager
    def build_block_column(self):
        box = RenderBox(0, self.width-2, self.box.height)
        builder = BlockBuilder(self.settings, box)
        yield builder
        mapper, lines = builder.build()
        while lines and lines[-1] == "":
            lines.pop()
        self.columns.append(lines)


class ListBuilder:
    def __init__(self, settings, box, start, bullet, num):
        self.settings = settings
        self.lines = []
        self.box = box
        self.mapper = Mapper()
        self.numbered = start is not None and bullet is None
        self.count = start if start is not None else 1
        self.bullet = bullet or BULLETS[self.settings.get('list_depth',0)%len(BULLETS)]
        self.width = len(str(num))+2 if self.numbered else 7-len(self.bullet)

    def add_index(self):
        self.mapper.add_index(len(self.lines))

    def add_mapper(self, mapper):
        self.mapper.add_mapper(len(self.lines), mapper)

    def incr(self):
        self.count +=1
        if self.numbered:
            n = str(self.count)+". "
        else:
            n = f"{self.bullet} "
        pad= max(0, self.width - line_len(n))
        return (" "*pad) + n

    def build(self):
        return self.mapper, [(" "* self.box.indent)+line for line in self.lines]

    @contextmanager
    def build_block_item(self):
        self.add_index()
        box = RenderBox(0, self.box.width-self.width, self.box.height)
        builder = BlockBuilder(self.settings, box)
        self.settings['list_depth'] = self.settings.get('list_depth',0) +1
        yield builder
        self.settings['list_depth'] = self.settings['list_depth'] -1
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
        builder = ParaBuilder(self.settings, box)
        yield builder
        mapper, lines = builder.build()
        self.add_mapper(mapper)
        for i, line in enumerate(lines):
            if i == 0:
                self.lines.append(self.incr() + line)
            else:
                self.lines.append((" "*self.width) + line)
        if len(lines) == 0:
            self.lines.append(self.incr())

class ParaBuilder:
    def __init__(self, settings, box, prose=False):
        self.settings = settings
        self.lines = []
        self.box = box
        self.mapper = Mapper()
        self.current_line = []
        self.current_word = []
        self.current_width = 0
        self.effects = []
        self.start_code = { 'strong': '\x1b[1m', 'emphasis': '', 'strikethrough':''}
        self.end_code = { 'strong': '\x1b[0m', 'emphasis':'', 'strikethrough':''}
        self.count = 0
        self.prose = prose
        self.whitespace = False

    def add_index(self):
        self.mapper.add_index(len(self.lines))

    def walk_text(self, text):
        for x in text:
            self.walk(x)

    def walk(self, text):
        if not text: 
            return

        if isinstance(text, str):
            if text == " ":
                self.add_space()
            else:
                self.add_text(text)
        else:
            text.walk(self)
        
    def build(self):
        self.add_current_word()
        self.add_current_line()

        if self.prose:
            lines = [(" "* self.box.indent)+line for line in self.lines]
            max_width = len(max(lines, key=len))
            max_width = max(max_width, self.box.width)
            return self.mapper, [line + (" "*(max_width-len(line))) for line in lines]
        else:
            return self.mapper, [(" "* self.box.indent)+line for line in self.lines]

    def add_current_word(self):
        if not self.current_word:
            return

        text = "".join(self.current_word)
        self.current_word[:] = []

        l = line_len(text)
        l = l +1 if self.current_width else l
        if l + self.current_width >= self.box.width and self.current_width > 0:
            self.add_current_line()
        if self.whitespace:
            self.current_line.append(" ")
        self.current_line.append(text)
        self.current_width += l
        self.whitespace = False

    def add_current_line(self):
        for name in self.effects[::-1]:
            self.current_line.append(self.end_code[name])
        self.lines.append("".join(self.current_line))
        self.current_line[:] = []
        self.current_width = 0
        for name in self.effects[::-1]:
            self.current_line.append(self.start_code[name])
        self.whitespace = False

    def add_space(self, text=" "):
        if self.prose:
            self.current_word.append(text)
        else:
            self.add_current_word()
            self.whitespace = True

    def add_code_text(self, text):
        self.add_wordbreak()
        self.add_text("`")
        for line in text.splitlines(keepends=True):
            if '\n' == line[-1]:
                self.add_text(line[:-1])
                self.add_break()
            else:
                self.add_text(line)
        self.add_text("`")
        self.add_wordbreak()

    def add_softbreak(self):
        if self.prose:
            self.add_break()
        else:
            self.add_space()

    def add_wordbreak(self):
        if self.whitespace:
            self.add_text(' ')
        self.add_current_word()
        self.whitespace = False

    def add_break(self):
        self.add_current_word()
        self.add_current_line()
        self.add_index()
        self.whitespace = False

    def add_text(self, text):
        for line in text.splitlines(keepends=True):
            if '\n' == line[-1]:
                self.current_word.append(line[:-1])
                self.add_break()
            else:
                self.current_word.append(line)

    def add_node(self, obj):
        self.add_wordbreak()
        self.add_text(dom.dump(obj))
        self.add_wordbreak()

    @contextmanager
    def build_directive(self, name, args):
        self.add_text(f"\\{name}{{")
        yield self
        self.add_text("}")


    def add_emoji(self, name):
        self.add_wordbreak()
        self.current_word.extend([':', name, ':'])
        self.add_wordbreak()


    @contextmanager
    def effect(self, name):
        self.add_wordbreak()
        self.current_word.append(self.start_code[name])
        self.effects.append(name)
        yield self
        self.current_word.append(self.end_code[name])
        self.add_current_word()
        self.effects.pop()

    @contextmanager
    def build_codespan(self):
        self.add_wordbreak()
        old_prose, self.prose = self.prose, True
        self.current_word.append('`')
        yield self
        self.current_word.append('`')
        self.add_current_word()
        self.prose = old_prose


def to_ansi(obj, box, settings):
    builder = DocumentBuilder(settings, box)
    builder.add_index()
    obj.walk(builder)
    builder.add_index()
    return builder.build()
