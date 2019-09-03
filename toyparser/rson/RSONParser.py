import unicodedata, re

class Node:
    def __init__(self, name, start, end, start_column, end_column, children, value):
        self.name = name
        self.start = start
        self.end = end
        self.start_column = start_column
        self.end_column = end_column
        self.children = children if children is not None else ()
        self.value = value
    def __str__(self):
        return '{}[{}:{}]'.format(self.name, self.start, self.end)
    def build(self, buf, builder):
        children = [child.build(buf, builder) for child in self.children]
        if callable(builder): return builder(buf, self, children)
        if self.name == "value": return self.value
        return builder[self.name](buf, self, children)

regex_0 = re.compile(r'(?:[^\n])*')
regex_1 = re.compile(r'[a-zA-Z]')
regex_2 = re.compile(r'(?:[0-9a-zA-Z_])*')
regex_3 = re.compile(r'[^\x00-\x1f\\\"\ud800-\udfff]')
regex_4 = re.compile(r'[0-1]')
regex_5 = re.compile(r'[0-9a-fA-F]')
regex_6 = re.compile(r'(?:D|d)')
regex_7 = re.compile(r'[8-9A-F]')
regex_8 = re.compile(r'(?:\\)[\"\\\/bfnrt\'\n]')
regex_9 = re.compile(r'[^\x00-\x1f\\\'\ud800-\udfff]')
regex_10 = re.compile(r'(?:(?:(?:[\-\+])?(?:0x)[0-9A-Fa-f](?:[0-9A-Fa-f_])*)|(?:(?:[\-\+])?(?:0o)[0-8](?:[0-8_])*)|(?:(?:[\-\+])?(?:0b)[0-1](?:[0-1_])*)|(?:(?:[\-\+])?(?:(?:(?:0))|(?:[1-9](?:[0-9])*))(?:(?:\.)(?:[0-9])*)?(?:(?:e|E)(?:(?:\+|\-)(?:[0-9])*)?)?))')

class Parser:
    def __init__(self, tabstop=None, allow_mixed_indent=False):
         self.tabstop = tabstop or 8
         self.cache = None
         self.allow_mixed_indent = allow_mixed_indent

    def parse(self, buf, offset=0, end=None, err=None, builder=None):
        self.cache = dict()
        end = len(buf) if end is None else end
        start, eof = offset, end
        column, indent_column = 0, [0]
        prefix, children = [], []
        new_offset, column, partial_tab_offset, partial_tab_width = self.parse_document(buf, start, end, offset, column, indent_column, prefix, children, 0, 0)
        if children and new_offset == end:
             if builder is None: return Node('document', offset, new_offset, 0, column, children, None)
             return children[-1].build(buf, builder)
        print('no', offset, new_offset, end, buf[new_offset:])
        if err is not None: raise err(buf, new_offset, 'no')

    def parse_document(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof:
                codepoint = buf[offset_0]
                if codepoint in ' \t\r\n\ufeff':
                    if codepoint == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break

            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    if buf[offset_1:offset_1+1] == '#':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    _match = regex_0.match(buf, offset_1)
                    if _match:
                        _end = _match.end()
                        column_1 += (_end - offset_1)
                        offset_1 = _end
                    else:
                        offset_1 = -1
                        break

                    count_1 = 0
                    while offset_1 < buf_eof:
                        codepoint = buf[offset_1]
                        if codepoint in ' \t\r\n\ufeff':
                            if codepoint == '\t':
                                if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                    width = partial_tab_width_1
                                else:
                                    width  = (self.tabstop-(column_1%self.tabstop))
                                count_1 += width
                                column_1 += width
                                offset_1 += 1
                            else:
                                count_1 += 1
                                column_1 += 1
                                offset_1 += 1
                        else:
                            break

                    break
                if offset_1 == -1:
                    break
                if offset_0 == offset_1: break
                if children_1 is not None and children_1 is not None:
                    children_0.extend(children_1)
                offset_0 = offset_1
                column_0 = column_1
                indent_column_0 = indent_column_1
                partial_tab_offset_0 = partial_tab_offset_1
                partial_tab_width_0 = partial_tab_width_1
                count_0 += 1
            if offset_0 == -1:
                break

            count_0 = 0
            while offset_0 < buf_eof:
                codepoint = buf[offset_0]
                if codepoint in ' \t\r\n\ufeff':
                    if codepoint == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break


            offset_0, column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_rson_value(buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0)
            if offset_0 == -1: break


            count_0 = 0
            while offset_0 < buf_eof:
                codepoint = buf[offset_0]
                if codepoint in ' \t\r\n\ufeff':
                    if codepoint == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break

            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    if buf[offset_1:offset_1+1] == '#':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    _match = regex_0.match(buf, offset_1)
                    if _match:
                        _end = _match.end()
                        column_1 += (_end - offset_1)
                        offset_1 = _end
                    else:
                        offset_1 = -1
                        break

                    count_1 = 0
                    while offset_1 < buf_eof:
                        codepoint = buf[offset_1]
                        if codepoint in ' \t\r\n\ufeff':
                            if codepoint == '\t':
                                if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                    width = partial_tab_width_1
                                else:
                                    width  = (self.tabstop-(column_1%self.tabstop))
                                count_1 += width
                                column_1 += width
                                offset_1 += 1
                            else:
                                count_1 += 1
                                column_1 += 1
                                offset_1 += 1
                        else:
                            break

                    break
                if offset_1 == -1:
                    break
                if offset_0 == offset_1: break
                if children_1 is not None and children_1 is not None:
                    children_0.extend(children_1)
                offset_0 = offset_1
                column_0 = column_1
                indent_column_0 = indent_column_1
                partial_tab_offset_0 = partial_tab_offset_1
                partial_tab_width_0 = partial_tab_width_1
                count_0 += 1
            if offset_0 == -1:
                break

            count_0 = 0
            while offset_0 < buf_eof:
                codepoint = buf[offset_0]
                if codepoint in ' \t\r\n\ufeff':
                    if codepoint == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break



            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_rson_value(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    column_2 = column_1
                    children_2 = []
                    value_0 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        if buf[offset_2:offset_2+1] == '@':
                            offset_2 += 1
                            column_2 += 1
                        else:
                            offset_2 = -1
                            break

                        offset_3 = offset_2
                        column_3 = column_2
                        children_3 = None
                        value_1 = Node(None, offset_2, offset_2, column_2, column_2, children_3, None)
                        while True: # start capture
                            _match = regex_1.match(buf, offset_3)
                            if _match:
                                _end = _match.end()
                                column_3 += (_end - offset_3)
                                offset_3 = _end
                            else:
                                offset_3 = -1
                                break

                            _match = regex_2.match(buf, offset_3)
                            if _match:
                                _end = _match.end()
                                column_3 += (_end - offset_3)
                                offset_3 = _end
                            else:
                                offset_3 = -1
                                break

                            break
                        if offset_3 == -1:
                            offset_2 = -1
                            break
                        value_1.name = 'identifier'
                        value_1.end = offset_3
                        value_1.end_column = column_3
                        value_1.value = None
                        children_2.append(value_1)
                        offset_2 = offset_3
                        column_2 = column_3

                        if buf[offset_2:offset_2+1] == ' ':
                            offset_2 += 1
                            column_2 += 1
                        else:
                            offset_2 = -1
                            break

                        offset_2, column_2, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_literal(buf, buf_start, buf_eof, offset_2, column_2, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                        if offset_2 == -1: break


                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_0.name = 'tagged'
                    value_0.end = offset_2
                    value_0.end_column = column_2
                    value_0.value = None
                    children_1.append(value_0)
                    offset_1 = offset_2
                    column_1 = column_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    column_0 = column_1
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
                    if offset_1 == -1: break



                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    column_0 = column_1
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_0 = -1 # no more choices
                break # end choice
            if offset_0 == -1:
                break

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_rson_literal(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_list(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
                    if offset_1 == -1: break



                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    column_0 = column_1
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_object(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
                    if offset_1 == -1: break



                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    column_0 = column_1
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    while True: # start choice
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = list(indent_column_1)
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            if buf[offset_2:offset_2+1] == '"':
                                offset_2 += 1
                                column_2 += 1
                            else:
                                offset_2 = -1
                                break

                            offset_3 = offset_2
                            column_3 = column_2
                            children_3 = None
                            value_0 = Node(None, offset_2, offset_2, column_2, column_2, children_3, None)
                            while True: # start capture
                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        while True: # start choice
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                _match = regex_3.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if buf[offset_5:offset_5+2] == '\\x':
                                                    offset_5 += 2
                                                    column_5 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_6 = column_5
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    _match = regex_4.match(buf, offset_6)
                                                    if _match:
                                                        _end = _match.end()
                                                        column_6 += (_end - offset_6)
                                                        offset_6 = _end
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if buf[offset_5:offset_5+2] == '\\u':
                                                    offset_5 += 2
                                                    column_5 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_6 = column_5
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if buf[offset_6:offset_6+3] == '000':
                                                        offset_6 += 3
                                                        column_6 += 3
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    _match = regex_4.match(buf, offset_6)
                                                    if _match:
                                                        _end = _match.end()
                                                        column_6 += (_end - offset_6)
                                                        offset_6 = _end
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_6 = column_5
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    _match = regex_6.match(buf, offset_6)
                                                    if _match:
                                                        _end = _match.end()
                                                        column_6 += (_end - offset_6)
                                                        offset_6 = _end
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    _match = regex_7.match(buf, offset_6)
                                                    if _match:
                                                        _end = _match.end()
                                                        column_6 += (_end - offset_6)
                                                        offset_6 = _end
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if buf[offset_5:offset_5+2] == '\\U':
                                                    offset_5 += 2
                                                    column_5 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_6 = column_5
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if buf[offset_6:offset_6+7] == '0000000':
                                                        offset_6 += 7
                                                        column_6 += 7
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    _match = regex_4.match(buf, offset_6)
                                                    if _match:
                                                        _end = _match.end()
                                                        column_6 += (_end - offset_6)
                                                        offset_6 = _end
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_6 = column_5
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if buf[offset_6:offset_6+4] == '0000':
                                                        offset_6 += 4
                                                        column_6 += 4
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    _match = regex_6.match(buf, offset_6)
                                                    if _match:
                                                        _end = _match.end()
                                                        column_6 += (_end - offset_6)
                                                        offset_6 = _end
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    _match = regex_7.match(buf, offset_6)
                                                    if _match:
                                                        _end = _match.end()
                                                        column_6 += (_end - offset_6)
                                                        offset_6 = _end
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                _match = regex_8.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_4 = -1 # no more choices
                                            break # end choice
                                        if offset_4 == -1:
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_3 = column_4
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_0 += 1
                                if offset_3 == -1:
                                    break

                                break
                            if offset_3 == -1:
                                offset_2 = -1
                                break
                            value_0.name = 'string'
                            value_0.end = offset_3
                            value_0.end_column = column_3
                            value_0.value = None
                            children_2.append(value_0)
                            offset_2 = offset_3
                            column_2 = column_3

                            if buf[offset_2:offset_2+1] == '"':
                                offset_2 += 1
                                column_2 += 1
                            else:
                                offset_2 = -1
                                break


                            break
                        if offset_2 != -1:
                            offset_1 = offset_2
                            column_1 = column_2
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            if children_2 is not None and children_2 is not None:
                                children_1.extend(children_2)
                            break
                        # end case
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = list(indent_column_1)
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            if buf[offset_2:offset_2+1] == "'":
                                offset_2 += 1
                                column_2 += 1
                            else:
                                offset_2 = -1
                                break

                            offset_3 = offset_2
                            column_3 = column_2
                            children_3 = None
                            value_1 = Node(None, offset_2, offset_2, column_2, column_2, children_3, None)
                            while True: # start capture
                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        while True: # start choice
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                _match = regex_9.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if buf[offset_5:offset_5+2] == '\\x':
                                                    offset_5 += 2
                                                    column_5 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_6 = column_5
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    _match = regex_4.match(buf, offset_6)
                                                    if _match:
                                                        _end = _match.end()
                                                        column_6 += (_end - offset_6)
                                                        offset_6 = _end
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if buf[offset_5:offset_5+2] == '\\u':
                                                    offset_5 += 2
                                                    column_5 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_6 = column_5
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if buf[offset_6:offset_6+2] == '00':
                                                        offset_6 += 2
                                                        column_6 += 2
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    _match = regex_4.match(buf, offset_6)
                                                    if _match:
                                                        _end = _match.end()
                                                        column_6 += (_end - offset_6)
                                                        offset_6 = _end
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_6 = column_5
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    _match = regex_6.match(buf, offset_6)
                                                    if _match:
                                                        _end = _match.end()
                                                        column_6 += (_end - offset_6)
                                                        offset_6 = _end
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    _match = regex_7.match(buf, offset_6)
                                                    if _match:
                                                        _end = _match.end()
                                                        column_6 += (_end - offset_6)
                                                        offset_6 = _end
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if buf[offset_5:offset_5+2] == '\\U':
                                                    offset_5 += 2
                                                    column_5 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_6 = column_5
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if buf[offset_6:offset_6+6] == '000000':
                                                        offset_6 += 6
                                                        column_6 += 6
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    _match = regex_4.match(buf, offset_6)
                                                    if _match:
                                                        _end = _match.end()
                                                        column_6 += (_end - offset_6)
                                                        offset_6 = _end
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_6 = column_5
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if buf[offset_6:offset_6+4] == '0000':
                                                        offset_6 += 4
                                                        column_6 += 4
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    _match = regex_6.match(buf, offset_6)
                                                    if _match:
                                                        _end = _match.end()
                                                        column_6 += (_end - offset_6)
                                                        offset_6 = _end
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    _match = regex_7.match(buf, offset_6)
                                                    if _match:
                                                        _end = _match.end()
                                                        column_6 += (_end - offset_6)
                                                        offset_6 = _end
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                _match = regex_5.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                _match = regex_8.match(buf, offset_5)
                                                if _match:
                                                    _end = _match.end()
                                                    column_5 += (_end - offset_5)
                                                    offset_5 = _end
                                                else:
                                                    offset_5 = -1
                                                    break

                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_4 = -1 # no more choices
                                            break # end choice
                                        if offset_4 == -1:
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_3 = column_4
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_0 += 1
                                if offset_3 == -1:
                                    break

                                break
                            if offset_3 == -1:
                                offset_2 = -1
                                break
                            value_1.name = 'string'
                            value_1.end = offset_3
                            value_1.end_column = column_3
                            value_1.value = None
                            children_2.append(value_1)
                            offset_2 = offset_3
                            column_2 = column_3

                            if buf[offset_2:offset_2+1] == "'":
                                offset_2 += 1
                                column_2 += 1
                            else:
                                offset_2 = -1
                                break


                            break
                        if offset_2 != -1:
                            offset_1 = offset_2
                            column_1 = column_2
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            if children_2 is not None and children_2 is not None:
                                children_1.extend(children_2)
                            break
                        # end case
                        offset_1 = -1 # no more choices
                        break # end choice
                    if offset_1 == -1:
                        break


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    column_0 = column_1
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    column_2 = column_1
                    children_2 = None
                    value_2 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        _match = regex_10.match(buf, offset_2)
                        if _match:
                            _end = _match.end()
                            column_2 += (_end - offset_2)
                            offset_2 = _end
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_2.name = 'number'
                    value_2.end = offset_2
                    value_2.end_column = column_2
                    value_2.value = None
                    children_1.append(value_2)
                    offset_1 = offset_2
                    column_1 = column_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    column_0 = column_1
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    column_2 = column_1
                    children_2 = []
                    value_3 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        if buf[offset_2:offset_2+4] == 'true':
                            offset_2 += 4
                            column_2 += 4
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_3.name = 'bool'
                    value_3.end = offset_2
                    value_3.end_column = column_2
                    value_3.value = None
                    children_1.append(value_3)
                    offset_1 = offset_2
                    column_1 = column_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    column_0 = column_1
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    column_2 = column_1
                    children_2 = []
                    value_4 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        if buf[offset_2:offset_2+5] == 'false':
                            offset_2 += 5
                            column_2 += 5
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_4.name = 'bool'
                    value_4.end = offset_2
                    value_4.end_column = column_2
                    value_4.value = None
                    children_1.append(value_4)
                    offset_1 = offset_2
                    column_1 = column_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    column_0 = column_1
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    column_2 = column_1
                    children_2 = []
                    value_5 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        if buf[offset_2:offset_2+4] == 'null':
                            offset_2 += 4
                            column_2 += 4
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_5.name = 'null'
                    value_5.end = offset_2
                    value_5.end_column = column_2
                    value_5.value = None
                    children_1.append(value_5)
                    offset_1 = offset_2
                    column_1 = column_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    column_0 = column_1
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_0 = -1 # no more choices
                break # end choice
            if offset_0 == -1:
                break

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_rson_string(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    if buf[offset_1:offset_1+1] == '"':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    offset_2 = offset_1
                    column_2 = column_1
                    children_2 = None
                    value_0 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                while True: # start choice
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        _match = regex_3.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_3 = column_4
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if buf[offset_4:offset_4+2] == '\\x':
                                            offset_4 += 2
                                            column_4 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            _match = regex_4.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_3 = column_4
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if buf[offset_4:offset_4+2] == '\\u':
                                            offset_4 += 2
                                            column_4 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if buf[offset_5:offset_5+3] == '000':
                                                offset_5 += 3
                                                column_5 += 3
                                            else:
                                                offset_5 = -1
                                                break

                                            _match = regex_4.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            _match = regex_6.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            _match = regex_7.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_3 = column_4
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if buf[offset_4:offset_4+2] == '\\U':
                                            offset_4 += 2
                                            column_4 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if buf[offset_5:offset_5+7] == '0000000':
                                                offset_5 += 7
                                                column_5 += 7
                                            else:
                                                offset_5 = -1
                                                break

                                            _match = regex_4.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if buf[offset_5:offset_5+4] == '0000':
                                                offset_5 += 4
                                                column_5 += 4
                                            else:
                                                offset_5 = -1
                                                break

                                            _match = regex_6.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            _match = regex_7.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_3 = column_4
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        _match = regex_8.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_3 = column_4
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_3 = -1 # no more choices
                                    break # end choice
                                if offset_3 == -1:
                                    break

                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            column_2 = column_3
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            count_0 += 1
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_0.name = 'string'
                    value_0.end = offset_2
                    value_0.end_column = column_2
                    value_0.value = None
                    children_1.append(value_0)
                    offset_1 = offset_2
                    column_1 = column_2

                    if buf[offset_1:offset_1+1] == '"':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    column_0 = column_1
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    if buf[offset_1:offset_1+1] == "'":
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    offset_2 = offset_1
                    column_2 = column_1
                    children_2 = None
                    value_1 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                while True: # start choice
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        _match = regex_9.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_3 = column_4
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if buf[offset_4:offset_4+2] == '\\x':
                                            offset_4 += 2
                                            column_4 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            _match = regex_4.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_3 = column_4
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if buf[offset_4:offset_4+2] == '\\u':
                                            offset_4 += 2
                                            column_4 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if buf[offset_5:offset_5+2] == '00':
                                                offset_5 += 2
                                                column_5 += 2
                                            else:
                                                offset_5 = -1
                                                break

                                            _match = regex_4.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            _match = regex_6.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            _match = regex_7.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_3 = column_4
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if buf[offset_4:offset_4+2] == '\\U':
                                            offset_4 += 2
                                            column_4 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if buf[offset_5:offset_5+6] == '000000':
                                                offset_5 += 6
                                                column_5 += 6
                                            else:
                                                offset_5 = -1
                                                break

                                            _match = regex_4.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_5 = column_4
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if buf[offset_5:offset_5+4] == '0000':
                                                offset_5 += 4
                                                column_5 += 4
                                            else:
                                                offset_5 = -1
                                                break

                                            _match = regex_6.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            _match = regex_7.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_5.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_3 = column_4
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        _match = regex_8.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_3 = column_4
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_3 = -1 # no more choices
                                    break # end choice
                                if offset_3 == -1:
                                    break

                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            column_2 = column_3
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            count_0 += 1
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_1.name = 'string'
                    value_1.end = offset_2
                    value_1.end_column = column_2
                    value_1.value = None
                    children_1.append(value_1)
                    offset_1 = offset_2
                    column_1 = column_2

                    if buf[offset_1:offset_1+1] == "'":
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    column_0 = column_1
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_0 = -1 # no more choices
                break # end choice
            if offset_0 == -1:
                break

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_rson_list(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            if buf[offset_0:offset_0+1] == '[':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break

            count_0 = 0
            while offset_0 < buf_eof:
                codepoint = buf[offset_0]
                if codepoint in ' \t\r\n\ufeff':
                    if codepoint == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break

            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    if buf[offset_1:offset_1+1] == '#':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    _match = regex_0.match(buf, offset_1)
                    if _match:
                        _end = _match.end()
                        column_1 += (_end - offset_1)
                        offset_1 = _end
                    else:
                        offset_1 = -1
                        break

                    count_1 = 0
                    while offset_1 < buf_eof:
                        codepoint = buf[offset_1]
                        if codepoint in ' \t\r\n\ufeff':
                            if codepoint == '\t':
                                if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                    width = partial_tab_width_1
                                else:
                                    width  = (self.tabstop-(column_1%self.tabstop))
                                count_1 += width
                                column_1 += width
                                offset_1 += 1
                            else:
                                count_1 += 1
                                column_1 += 1
                                offset_1 += 1
                        else:
                            break

                    break
                if offset_1 == -1:
                    break
                if offset_0 == offset_1: break
                if children_1 is not None and children_1 is not None:
                    children_0.extend(children_1)
                offset_0 = offset_1
                column_0 = column_1
                indent_column_0 = indent_column_1
                partial_tab_offset_0 = partial_tab_offset_1
                partial_tab_width_0 = partial_tab_width_1
                count_0 += 1
            if offset_0 == -1:
                break

            count_0 = 0
            while offset_0 < buf_eof:
                codepoint = buf[offset_0]
                if codepoint in ' \t\r\n\ufeff':
                    if codepoint == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break


            offset_1 = offset_0
            column_1 = column_0
            children_1 = []
            value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
            while True: # start capture
                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    column_2 = column_1
                    indent_column_1 = list(indent_column_0)
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        offset_2, column_2, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_value(buf, buf_start, buf_eof, offset_2, column_2, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                        if offset_2 == -1: break


                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_2 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if buf[offset_4:offset_4+1] == '#':
                                            offset_4 += 1
                                            column_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_0.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t\r\n\ufeff':
                                                if codepoint == '\t':
                                                    if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                        width = partial_tab_width_3
                                                    else:
                                                        width  = (self.tabstop-(column_4%self.tabstop))
                                                    count_3 += width
                                                    column_4 += width
                                                    offset_4 += 1
                                                else:
                                                    count_3 += 1
                                                    column_4 += 1
                                                    offset_4 += 1
                                            else:
                                                break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_3 = column_4
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_2 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break


                                if buf[offset_3:offset_3+1] == ',':
                                    offset_3 += 1
                                    column_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_2 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if buf[offset_4:offset_4+1] == '#':
                                            offset_4 += 1
                                            column_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_0.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t\r\n\ufeff':
                                                if codepoint == '\t':
                                                    if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                        width = partial_tab_width_3
                                                    else:
                                                        width  = (self.tabstop-(column_4%self.tabstop))
                                                    count_3 += width
                                                    column_4 += width
                                                    offset_4 += 1
                                                else:
                                                    count_3 += 1
                                                    column_4 += 1
                                                    offset_4 += 1
                                            else:
                                                break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_3 = column_4
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_2 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break


                                offset_3, column_3, partial_tab_offset_2, partial_tab_width_2 = self.parse_rson_value(buf, buf_start, buf_eof, offset_3, column_3, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
                                if offset_3 == -1: break


                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            column_2 = column_3
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            count_1 += 1
                        if offset_2 == -1:
                            break

                        count_1 = 0
                        while offset_2 < buf_eof:
                            codepoint = buf[offset_2]
                            if codepoint in ' \t\r\n\ufeff':
                                if codepoint == '\t':
                                    if offset_2 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                        width = partial_tab_width_1
                                    else:
                                        width  = (self.tabstop-(column_2%self.tabstop))
                                    count_1 += width
                                    column_2 += width
                                    offset_2 += 1
                                else:
                                    count_1 += 1
                                    column_2 += 1
                                    offset_2 += 1
                            else:
                                break

                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if buf[offset_3:offset_3+1] == '#':
                                    offset_3 += 1
                                    column_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                _match = regex_0.match(buf, offset_3)
                                if _match:
                                    _end = _match.end()
                                    column_3 += (_end - offset_3)
                                    offset_3 = _end
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_2 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            column_2 = column_3
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            count_1 += 1
                        if offset_2 == -1:
                            break

                        count_1 = 0
                        while offset_2 < buf_eof:
                            codepoint = buf[offset_2]
                            if codepoint in ' \t\r\n\ufeff':
                                if codepoint == '\t':
                                    if offset_2 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                        width = partial_tab_width_1
                                    else:
                                        width  = (self.tabstop-(column_2%self.tabstop))
                                    count_1 += width
                                    column_2 += width
                                    offset_2 += 1
                                else:
                                    count_1 += 1
                                    column_2 += 1
                                    offset_2 += 1
                            else:
                                break


                        count_1 = 0
                        while count_1 < 1:
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if buf[offset_3:offset_3+1] == ',':
                                    offset_3 += 1
                                    column_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_2 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if buf[offset_4:offset_4+1] == '#':
                                            offset_4 += 1
                                            column_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_0.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t\r\n\ufeff':
                                                if codepoint == '\t':
                                                    if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                        width = partial_tab_width_3
                                                    else:
                                                        width  = (self.tabstop-(column_4%self.tabstop))
                                                    count_3 += width
                                                    column_4 += width
                                                    offset_4 += 1
                                                else:
                                                    count_3 += 1
                                                    column_4 += 1
                                                    offset_4 += 1
                                            else:
                                                break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_3 = column_4
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_2 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break


                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            column_2 = column_3
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            count_1 += 1
                            break
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        break
                    if offset_1 == offset_2: break
                    if children_2 is not None and children_2 is not None:
                        children_1.extend(children_2)
                    offset_1 = offset_2
                    column_1 = column_2
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    count_0 += 1
                    break
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            value_0.name = 'list'
            value_0.end = offset_1
            value_0.end_column = column_1
            value_0.value = None
            children_0.append(value_0)
            offset_0 = offset_1
            column_0 = column_1

            if buf[offset_0:offset_0+1] == ']':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_rson_object(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            if buf[offset_0:offset_0+1] == '{':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break

            count_0 = 0
            while offset_0 < buf_eof:
                codepoint = buf[offset_0]
                if codepoint in ' \t\r\n\ufeff':
                    if codepoint == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break

            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    if buf[offset_1:offset_1+1] == '#':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    _match = regex_0.match(buf, offset_1)
                    if _match:
                        _end = _match.end()
                        column_1 += (_end - offset_1)
                        offset_1 = _end
                    else:
                        offset_1 = -1
                        break

                    count_1 = 0
                    while offset_1 < buf_eof:
                        codepoint = buf[offset_1]
                        if codepoint in ' \t\r\n\ufeff':
                            if codepoint == '\t':
                                if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                    width = partial_tab_width_1
                                else:
                                    width  = (self.tabstop-(column_1%self.tabstop))
                                count_1 += width
                                column_1 += width
                                offset_1 += 1
                            else:
                                count_1 += 1
                                column_1 += 1
                                offset_1 += 1
                        else:
                            break

                    break
                if offset_1 == -1:
                    break
                if offset_0 == offset_1: break
                if children_1 is not None and children_1 is not None:
                    children_0.extend(children_1)
                offset_0 = offset_1
                column_0 = column_1
                indent_column_0 = indent_column_1
                partial_tab_offset_0 = partial_tab_offset_1
                partial_tab_width_0 = partial_tab_width_1
                count_0 += 1
            if offset_0 == -1:
                break

            count_0 = 0
            while offset_0 < buf_eof:
                codepoint = buf[offset_0]
                if codepoint in ' \t\r\n\ufeff':
                    if codepoint == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break


            offset_1 = offset_0
            column_1 = column_0
            children_1 = []
            value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
            while True: # start capture
                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    column_2 = column_1
                    indent_column_1 = list(indent_column_0)
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        offset_3 = offset_2
                        column_3 = column_2
                        children_3 = []
                        value_1 = Node(None, offset_2, offset_2, column_2, column_2, children_3, None)
                        while True: # start capture
                            offset_3, column_3, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_string(buf, buf_start, buf_eof, offset_3, column_3, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                            if offset_3 == -1: break


                            count_1 = 0
                            while offset_3 < buf_eof:
                                codepoint = buf[offset_3]
                                if codepoint in ' \t\r\n\ufeff':
                                    if codepoint == '\t':
                                        if offset_3 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-(column_3%self.tabstop))
                                        count_1 += width
                                        column_3 += width
                                        offset_3 += 1
                                    else:
                                        count_1 += 1
                                        column_3 += 1
                                        offset_3 += 1
                                else:
                                    break

                            count_1 = 0
                            while True:
                                offset_4 = offset_3
                                column_4 = column_3
                                indent_column_2 = list(indent_column_1)
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_4 = [] if children_3 is not None else None
                                while True:
                                    if buf[offset_4:offset_4+1] == '#':
                                        offset_4 += 1
                                        column_4 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    _match = regex_0.match(buf, offset_4)
                                    if _match:
                                        _end = _match.end()
                                        column_4 += (_end - offset_4)
                                        offset_4 = _end
                                    else:
                                        offset_4 = -1
                                        break

                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        codepoint = buf[offset_4]
                                        if codepoint in ' \t\r\n\ufeff':
                                            if codepoint == '\t':
                                                if offset_4 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                    width = partial_tab_width_2
                                                else:
                                                    width  = (self.tabstop-(column_4%self.tabstop))
                                                count_2 += width
                                                column_4 += width
                                                offset_4 += 1
                                            else:
                                                count_2 += 1
                                                column_4 += 1
                                                offset_4 += 1
                                        else:
                                            break

                                    break
                                if offset_4 == -1:
                                    break
                                if offset_3 == offset_4: break
                                if children_4 is not None and children_4 is not None:
                                    children_3.extend(children_4)
                                offset_3 = offset_4
                                column_3 = column_4
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                count_1 += 1
                            if offset_3 == -1:
                                break

                            count_1 = 0
                            while offset_3 < buf_eof:
                                codepoint = buf[offset_3]
                                if codepoint in ' \t\r\n\ufeff':
                                    if codepoint == '\t':
                                        if offset_3 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-(column_3%self.tabstop))
                                        count_1 += width
                                        column_3 += width
                                        offset_3 += 1
                                    else:
                                        count_1 += 1
                                        column_3 += 1
                                        offset_3 += 1
                                else:
                                    break


                            if buf[offset_3:offset_3+1] == ':':
                                offset_3 += 1
                                column_3 += 1
                            else:
                                offset_3 = -1
                                break

                            count_1 = 0
                            while offset_3 < buf_eof:
                                codepoint = buf[offset_3]
                                if codepoint in ' \t\r\n\ufeff':
                                    if codepoint == '\t':
                                        if offset_3 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-(column_3%self.tabstop))
                                        count_1 += width
                                        column_3 += width
                                        offset_3 += 1
                                    else:
                                        count_1 += 1
                                        column_3 += 1
                                        offset_3 += 1
                                else:
                                    break

                            count_1 = 0
                            while True:
                                offset_4 = offset_3
                                column_4 = column_3
                                indent_column_2 = list(indent_column_1)
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_4 = [] if children_3 is not None else None
                                while True:
                                    if buf[offset_4:offset_4+1] == '#':
                                        offset_4 += 1
                                        column_4 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    _match = regex_0.match(buf, offset_4)
                                    if _match:
                                        _end = _match.end()
                                        column_4 += (_end - offset_4)
                                        offset_4 = _end
                                    else:
                                        offset_4 = -1
                                        break

                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        codepoint = buf[offset_4]
                                        if codepoint in ' \t\r\n\ufeff':
                                            if codepoint == '\t':
                                                if offset_4 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                    width = partial_tab_width_2
                                                else:
                                                    width  = (self.tabstop-(column_4%self.tabstop))
                                                count_2 += width
                                                column_4 += width
                                                offset_4 += 1
                                            else:
                                                count_2 += 1
                                                column_4 += 1
                                                offset_4 += 1
                                        else:
                                            break

                                    break
                                if offset_4 == -1:
                                    break
                                if offset_3 == offset_4: break
                                if children_4 is not None and children_4 is not None:
                                    children_3.extend(children_4)
                                offset_3 = offset_4
                                column_3 = column_4
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                count_1 += 1
                            if offset_3 == -1:
                                break

                            count_1 = 0
                            while offset_3 < buf_eof:
                                codepoint = buf[offset_3]
                                if codepoint in ' \t\r\n\ufeff':
                                    if codepoint == '\t':
                                        if offset_3 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-(column_3%self.tabstop))
                                        count_1 += width
                                        column_3 += width
                                        offset_3 += 1
                                    else:
                                        count_1 += 1
                                        column_3 += 1
                                        offset_3 += 1
                                else:
                                    break


                            offset_3, column_3, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_value(buf, buf_start, buf_eof, offset_3, column_3, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                            if offset_3 == -1: break


                            break
                        if offset_3 == -1:
                            offset_2 = -1
                            break
                        value_1.name = 'pair'
                        value_1.end = offset_3
                        value_1.end_column = column_3
                        value_1.value = None
                        children_2.append(value_1)
                        offset_2 = offset_3
                        column_2 = column_3

                        count_1 = 0
                        while offset_2 < buf_eof:
                            codepoint = buf[offset_2]
                            if codepoint in ' \t\r\n\ufeff':
                                if codepoint == '\t':
                                    if offset_2 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                        width = partial_tab_width_1
                                    else:
                                        width  = (self.tabstop-(column_2%self.tabstop))
                                    count_1 += width
                                    column_2 += width
                                    offset_2 += 1
                                else:
                                    count_1 += 1
                                    column_2 += 1
                                    offset_2 += 1
                            else:
                                break

                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if buf[offset_3:offset_3+1] == '#':
                                    offset_3 += 1
                                    column_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                _match = regex_0.match(buf, offset_3)
                                if _match:
                                    _end = _match.end()
                                    column_3 += (_end - offset_3)
                                    offset_3 = _end
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_2 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            column_2 = column_3
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            count_1 += 1
                        if offset_2 == -1:
                            break

                        count_1 = 0
                        while offset_2 < buf_eof:
                            codepoint = buf[offset_2]
                            if codepoint in ' \t\r\n\ufeff':
                                if codepoint == '\t':
                                    if offset_2 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                        width = partial_tab_width_1
                                    else:
                                        width  = (self.tabstop-(column_2%self.tabstop))
                                    count_1 += width
                                    column_2 += width
                                    offset_2 += 1
                                else:
                                    count_1 += 1
                                    column_2 += 1
                                    offset_2 += 1
                            else:
                                break


                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if buf[offset_3:offset_3+1] == ',':
                                    offset_3 += 1
                                    column_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_2 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if buf[offset_4:offset_4+1] == '#':
                                            offset_4 += 1
                                            column_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_0.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t\r\n\ufeff':
                                                if codepoint == '\t':
                                                    if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                        width = partial_tab_width_3
                                                    else:
                                                        width  = (self.tabstop-(column_4%self.tabstop))
                                                    count_3 += width
                                                    column_4 += width
                                                    offset_4 += 1
                                                else:
                                                    count_3 += 1
                                                    column_4 += 1
                                                    offset_4 += 1
                                            else:
                                                break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_3 = column_4
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_2 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break


                                offset_4 = offset_3
                                column_4 = column_3
                                children_4 = []
                                value_2 = Node(None, offset_3, offset_3, column_3, column_3, children_4, None)
                                while True: # start capture
                                    offset_4, column_4, partial_tab_offset_2, partial_tab_width_2 = self.parse_rson_string(buf, buf_start, buf_eof, offset_4, column_4, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                    if offset_4 == -1: break


                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        codepoint = buf[offset_4]
                                        if codepoint in ' \t\r\n\ufeff':
                                            if codepoint == '\t':
                                                if offset_4 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                    width = partial_tab_width_2
                                                else:
                                                    width  = (self.tabstop-(column_4%self.tabstop))
                                                count_2 += width
                                                column_4 += width
                                                offset_4 += 1
                                            else:
                                                count_2 += 1
                                                column_4 += 1
                                                offset_4 += 1
                                        else:
                                            break

                                    count_2 = 0
                                    while True:
                                        offset_5 = offset_4
                                        column_5 = column_4
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            if buf[offset_5:offset_5+1] == '#':
                                                offset_5 += 1
                                                column_5 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            _match = regex_0.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            count_3 = 0
                                            while offset_5 < buf_eof:
                                                codepoint = buf[offset_5]
                                                if codepoint in ' \t\r\n\ufeff':
                                                    if codepoint == '\t':
                                                        if offset_5 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                            width = partial_tab_width_3
                                                        else:
                                                            width  = (self.tabstop-(column_5%self.tabstop))
                                                        count_3 += width
                                                        column_5 += width
                                                        offset_5 += 1
                                                    else:
                                                        count_3 += 1
                                                        column_5 += 1
                                                        offset_5 += 1
                                                else:
                                                    break

                                            break
                                        if offset_5 == -1:
                                            break
                                        if offset_4 == offset_5: break
                                        if children_5 is not None and children_5 is not None:
                                            children_4.extend(children_5)
                                        offset_4 = offset_5
                                        column_4 = column_5
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        count_2 += 1
                                    if offset_4 == -1:
                                        break

                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        codepoint = buf[offset_4]
                                        if codepoint in ' \t\r\n\ufeff':
                                            if codepoint == '\t':
                                                if offset_4 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                    width = partial_tab_width_2
                                                else:
                                                    width  = (self.tabstop-(column_4%self.tabstop))
                                                count_2 += width
                                                column_4 += width
                                                offset_4 += 1
                                            else:
                                                count_2 += 1
                                                column_4 += 1
                                                offset_4 += 1
                                        else:
                                            break


                                    if buf[offset_4:offset_4+1] == ':':
                                        offset_4 += 1
                                        column_4 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        codepoint = buf[offset_4]
                                        if codepoint in ' \t\r\n\ufeff':
                                            if codepoint == '\t':
                                                if offset_4 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                    width = partial_tab_width_2
                                                else:
                                                    width  = (self.tabstop-(column_4%self.tabstop))
                                                count_2 += width
                                                column_4 += width
                                                offset_4 += 1
                                            else:
                                                count_2 += 1
                                                column_4 += 1
                                                offset_4 += 1
                                        else:
                                            break

                                    count_2 = 0
                                    while True:
                                        offset_5 = offset_4
                                        column_5 = column_4
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            if buf[offset_5:offset_5+1] == '#':
                                                offset_5 += 1
                                                column_5 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            _match = regex_0.match(buf, offset_5)
                                            if _match:
                                                _end = _match.end()
                                                column_5 += (_end - offset_5)
                                                offset_5 = _end
                                            else:
                                                offset_5 = -1
                                                break

                                            count_3 = 0
                                            while offset_5 < buf_eof:
                                                codepoint = buf[offset_5]
                                                if codepoint in ' \t\r\n\ufeff':
                                                    if codepoint == '\t':
                                                        if offset_5 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                            width = partial_tab_width_3
                                                        else:
                                                            width  = (self.tabstop-(column_5%self.tabstop))
                                                        count_3 += width
                                                        column_5 += width
                                                        offset_5 += 1
                                                    else:
                                                        count_3 += 1
                                                        column_5 += 1
                                                        offset_5 += 1
                                                else:
                                                    break

                                            break
                                        if offset_5 == -1:
                                            break
                                        if offset_4 == offset_5: break
                                        if children_5 is not None and children_5 is not None:
                                            children_4.extend(children_5)
                                        offset_4 = offset_5
                                        column_4 = column_5
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        count_2 += 1
                                    if offset_4 == -1:
                                        break

                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        codepoint = buf[offset_4]
                                        if codepoint in ' \t\r\n\ufeff':
                                            if codepoint == '\t':
                                                if offset_4 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                    width = partial_tab_width_2
                                                else:
                                                    width  = (self.tabstop-(column_4%self.tabstop))
                                                count_2 += width
                                                column_4 += width
                                                offset_4 += 1
                                            else:
                                                count_2 += 1
                                                column_4 += 1
                                                offset_4 += 1
                                        else:
                                            break


                                    offset_4, column_4, partial_tab_offset_2, partial_tab_width_2 = self.parse_rson_value(buf, buf_start, buf_eof, offset_4, column_4, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                    if offset_4 == -1: break


                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                value_2.name = 'pair'
                                value_2.end = offset_4
                                value_2.end_column = column_4
                                value_2.value = None
                                children_3.append(value_2)
                                offset_3 = offset_4
                                column_3 = column_4

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_2 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if buf[offset_4:offset_4+1] == '#':
                                            offset_4 += 1
                                            column_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_0.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t\r\n\ufeff':
                                                if codepoint == '\t':
                                                    if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                        width = partial_tab_width_3
                                                    else:
                                                        width  = (self.tabstop-(column_4%self.tabstop))
                                                    count_3 += width
                                                    column_4 += width
                                                    offset_4 += 1
                                                else:
                                                    count_3 += 1
                                                    column_4 += 1
                                                    offset_4 += 1
                                            else:
                                                break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_3 = column_4
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_2 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break


                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            column_2 = column_3
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            count_1 += 1
                        if offset_2 == -1:
                            break

                        count_1 = 0
                        while count_1 < 1:
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if buf[offset_3:offset_3+1] == ',':
                                    offset_3 += 1
                                    column_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_2 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if buf[offset_4:offset_4+1] == '#':
                                            offset_4 += 1
                                            column_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        _match = regex_0.match(buf, offset_4)
                                        if _match:
                                            _end = _match.end()
                                            column_4 += (_end - offset_4)
                                            offset_4 = _end
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t\r\n\ufeff':
                                                if codepoint == '\t':
                                                    if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                        width = partial_tab_width_3
                                                    else:
                                                        width  = (self.tabstop-(column_4%self.tabstop))
                                                    count_3 += width
                                                    column_4 += width
                                                    offset_4 += 1
                                                else:
                                                    count_3 += 1
                                                    column_4 += 1
                                                    offset_4 += 1
                                            else:
                                                break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_3 = column_4
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_2 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break


                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            column_2 = column_3
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            count_1 += 1
                            break
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        break
                    if offset_1 == offset_2: break
                    if children_2 is not None and children_2 is not None:
                        children_1.extend(children_2)
                    offset_1 = offset_2
                    column_1 = column_2
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    count_0 += 1
                    break
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            value_0.name = 'object'
            value_0.end = offset_1
            value_0.end_column = column_1
            value_0.value = None
            children_0.append(value_0)
            offset_0 = offset_1
            column_0 = column_1

            if buf[offset_0:offset_0+1] == '}':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0
