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

regex_0 = re.compile(r'''(?:[ \t\r\n\ufeff])*(?:(?:\#)(?:[^\n])*(?:[ \t\r\n\ufeff])*)*(?:[ \t\r\n\ufeff])*''')
regex_1 = re.compile(r'''[a-zA-Z]''')
regex_2 = re.compile(r'''(?:[0-9a-zA-Z_])*''')
regex_3 = re.compile(r'''[^\x00-\x1f\\"\ud800-\udfff]''')
regex_4 = re.compile(r'''[0-1]''')
regex_5 = re.compile(r'''[0-9a-fA-F]''')
regex_6 = re.compile(r'''(?:D|d)''')
regex_7 = re.compile(r'''[8-9A-F]''')
regex_8 = re.compile(r'''(?:\\)["\\/bfnrt'\n]''')
regex_9 = re.compile(r'''[^\x00-\x1f\\'\ud800-\udfff]''')
regex_10 = re.compile(r'''(?:(?:(?:[\-\+])?(?:0x)[0-9A-Fa-f](?:[0-9A-Fa-f_])*)|(?:(?:[\-\+])?(?:0o)[0-8](?:[0-8_])*)|(?:(?:[\-\+])?(?:0b)[0-1](?:[0-1_])*)|(?:(?:[\-\+])?(?:(?:(?:0))|(?:[1-9](?:[0-9])*))(?:(?:\.)(?:[0-9])*)?(?:(?:e|E)(?:(?:\+|\-)(?:[0-9])*)?)?))''')
regex_11 = re.compile(r'''(?:(?:,)(?:[ \t\r\n\ufeff])*(?:(?:\#)(?:[^\n])*(?:[ \t\r\n\ufeff])*)*(?:[ \t\r\n\ufeff])*)?''')

class Parser:
    def __init__(self, tabstop=None, allow_mixed_indent=True):
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
        if new_offset == end:
             if builder is None: return Node('document', offset, new_offset, 0, column, children, None)
             return children[-1].build(buf, builder)
        # print('no', children, offset, new_offset, end)
        if err is not None: raise err(buf, new_offset, 'no')

    def parse_document(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            _match = regex_0.match(buf, offset_0)
            if _match:
                _end = _match.end()
                column_0 += (_end - offset_0)
                offset_0 = _end
            else:
                offset_0 = -1
                break

            offset_0, column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_rson_value(buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0)
            if offset_0 == -1: break


            _match = regex_0.match(buf, offset_0)
            if _match:
                _end = _match.end()
                column_0 += (_end - offset_0)
                offset_0 = _end
            else:
                offset_0 = -1
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
                    children_2 = []
                    value_0 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        if buf[offset_1:offset_1+1] == '@':
                            offset_1 += 1
                            column_1 += 1
                        else:
                            offset_1 = -1
                            break

                        children_3 = None
                        value_1 = Node(None, offset_1, offset_1, column_1, column_1, children_3, None)
                        while True: # start capture
                            _match = regex_1.match(buf, offset_1)
                            if _match:
                                _end = _match.end()
                                column_1 += (_end - offset_1)
                                offset_1 = _end
                            else:
                                offset_1 = -1
                                break

                            _match = regex_2.match(buf, offset_1)
                            if _match:
                                _end = _match.end()
                                column_1 += (_end - offset_1)
                                offset_1 = _end
                            else:
                                offset_1 = -1
                                break

                            break
                        if offset_1 == -1:
                            break
                        value_1.name = 'identifier'
                        value_1.end = offset_1
                        value_1.end_column = column_1
                        value_1.value = None
                        children_2.append(value_1)

                        if buf[offset_1:offset_1+1] == ' ':
                            offset_1 += 1
                            column_1 += 1
                        else:
                            offset_1 = -1
                            break

                        offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                        if offset_1 == -1: break


                        break
                    if offset_1 == -1:
                        break
                    value_0.name = 'tagged'
                    value_0.end = offset_1
                    value_0.end_column = column_1
                    value_0.value = None
                    children_1.append(value_0)


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

                            children_3 = None
                            value_0 = Node(None, offset_2, offset_2, column_2, column_2, children_3, None)
                            while True: # start capture
                                count_0 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        while True: # start choice
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
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
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if buf[offset_4:offset_4+2] == '\\x':
                                                    offset_4 += 2
                                                    column_4 += 2
                                                else:
                                                    offset_4 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_5 = offset_4 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
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
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if buf[offset_4:offset_4+2] == '\\u':
                                                    offset_4 += 2
                                                    column_4 += 2
                                                else:
                                                    offset_4 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_5 = offset_4 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
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
                                                    children_6 = []
                                                    offset_5 = offset_4 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
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
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if buf[offset_4:offset_4+2] == '\\U':
                                                    offset_4 += 2
                                                    column_4 += 2
                                                else:
                                                    offset_4 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_5 = offset_4 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
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
                                                    children_6 = []
                                                    offset_5 = offset_4 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
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
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
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
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_3 = -1 # no more choices
                                            break # end choice
                                        if offset_3 == -1:
                                            break

                                        #print('safe exit rep rule', offset_2, offset_3)
                                        break
                                    #print('exit rep rule', offset_2, offset_3)
                                    if offset_3 == -1:
                                        break
                                    if offset_2 == offset_3: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_2 = offset_3
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_0 += 1
                                if offset_2 == -1:
                                    break
                                value_1 = count_0

                                break
                            if offset_2 == -1:
                                break
                            value_0.name = 'string'
                            value_0.end = offset_2
                            value_0.end_column = column_2
                            value_0.value = None
                            children_2.append(value_0)

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

                            children_3 = None
                            value_2 = Node(None, offset_2, offset_2, column_2, column_2, children_3, None)
                            while True: # start capture
                                count_0 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        while True: # start choice
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
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
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if buf[offset_4:offset_4+2] == '\\x':
                                                    offset_4 += 2
                                                    column_4 += 2
                                                else:
                                                    offset_4 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_5 = offset_4 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
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
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if buf[offset_4:offset_4+2] == '\\u':
                                                    offset_4 += 2
                                                    column_4 += 2
                                                else:
                                                    offset_4 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_5 = offset_4 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
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
                                                    children_6 = []
                                                    offset_5 = offset_4 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
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
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if buf[offset_4:offset_4+2] == '\\U':
                                                    offset_4 += 2
                                                    column_4 += 2
                                                else:
                                                    offset_4 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_5 = offset_4 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
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
                                                    children_6 = []
                                                    offset_5 = offset_4 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
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
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
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
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_3 = -1 # no more choices
                                            break # end choice
                                        if offset_3 == -1:
                                            break

                                        #print('safe exit rep rule', offset_2, offset_3)
                                        break
                                    #print('exit rep rule', offset_2, offset_3)
                                    if offset_3 == -1:
                                        break
                                    if offset_2 == offset_3: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_2 = offset_3
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_0 += 1
                                if offset_2 == -1:
                                    break
                                value_3 = count_0

                                break
                            if offset_2 == -1:
                                break
                            value_2.name = 'string'
                            value_2.end = offset_2
                            value_2.end_column = column_2
                            value_2.value = None
                            children_2.append(value_2)

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
                    children_2 = None
                    value_4 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        _match = regex_10.match(buf, offset_1)
                        if _match:
                            _end = _match.end()
                            column_1 += (_end - offset_1)
                            offset_1 = _end
                        else:
                            offset_1 = -1
                            break

                        break
                    if offset_1 == -1:
                        break
                    value_4.name = 'number'
                    value_4.end = offset_1
                    value_4.end_column = column_1
                    value_4.value = None
                    children_1.append(value_4)


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
                    children_2 = []
                    value_5 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        if buf[offset_1:offset_1+4] == 'true':
                            offset_1 += 4
                            column_1 += 4
                        else:
                            offset_1 = -1
                            break

                        break
                    if offset_1 == -1:
                        break
                    value_5.name = 'bool'
                    value_5.end = offset_1
                    value_5.end_column = column_1
                    value_5.value = None
                    children_1.append(value_5)


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
                    children_2 = []
                    value_6 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        if buf[offset_1:offset_1+5] == 'false':
                            offset_1 += 5
                            column_1 += 5
                        else:
                            offset_1 = -1
                            break

                        break
                    if offset_1 == -1:
                        break
                    value_6.name = 'bool'
                    value_6.end = offset_1
                    value_6.end_column = column_1
                    value_6.value = None
                    children_1.append(value_6)


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
                    children_2 = []
                    value_7 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        if buf[offset_1:offset_1+4] == 'null':
                            offset_1 += 4
                            column_1 += 4
                        else:
                            offset_1 = -1
                            break

                        break
                    if offset_1 == -1:
                        break
                    value_7.name = 'null'
                    value_7.end = offset_1
                    value_7.end_column = column_1
                    value_7.value = None
                    children_1.append(value_7)


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

            _match = regex_0.match(buf, offset_0)
            if _match:
                _end = _match.end()
                column_0 += (_end - offset_0)
                offset_0 = _end
            else:
                offset_0 = -1
                break

            children_1 = []
            value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
            while True: # start capture
                count_0 = 0
                while count_0 < 1:
                    offset_1 = offset_0
                    column_1 = column_0
                    indent_column_1 = list(indent_column_0)
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        #print('entry rep rule', offset_0, offset_1)
                        offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_value(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                        if offset_1 == -1: break


                        count_1 = 0
                        while True:
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                #print('entry rep rule', offset_1, offset_2)
                                _match = regex_0.match(buf, offset_2)
                                if _match:
                                    _end = _match.end()
                                    column_2 += (_end - offset_2)
                                    offset_2 = _end
                                else:
                                    offset_2 = -1
                                    break

                                if buf[offset_2:offset_2+1] == ',':
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

                                _match = regex_0.match(buf, offset_2)
                                if _match:
                                    _end = _match.end()
                                    column_2 += (_end - offset_2)
                                    offset_2 = _end
                                else:
                                    offset_2 = -1
                                    break

                                offset_2, column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_rson_value(buf, buf_start, buf_eof, offset_2, column_2, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
                                if offset_2 == -1: break


                                #print('safe exit rep rule', offset_1, offset_2)
                                break
                            #print('exit rep rule', offset_1, offset_2)
                            if offset_2 == -1:
                                break
                            if offset_1 == offset_2: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_1 = offset_2
                            column_1 = column_2
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            count_1 += 1
                        if offset_1 == -1:
                            break
                        value_2 = count_1

                        _match = regex_0.match(buf, offset_1)
                        if _match:
                            _end = _match.end()
                            column_1 += (_end - offset_1)
                            offset_1 = _end
                        else:
                            offset_1 = -1
                            break

                        _match = regex_11.match(buf, offset_1)
                        if _match:
                            _end = _match.end()
                            column_1 += (_end - offset_1)
                            offset_1 = _end
                        else:
                            offset_1 = -1
                            break

                        #print('safe exit rep rule', offset_0, offset_1)
                        break
                    #print('exit rep rule', offset_0, offset_1)
                    if offset_1 == -1:
                        break
                    if offset_0 == offset_1: break
                    if children_2 is not None and children_2 is not None:
                        children_1.extend(children_2)
                    offset_0 = offset_1
                    column_0 = column_1
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    count_0 += 1
                    break
                if offset_0 == -1:
                    break
                value_1 = count_0

                break
            if offset_0 == -1:
                break
            value_0.name = 'list'
            value_0.end = offset_0
            value_0.end_column = column_0
            value_0.value = None
            children_0.append(value_0)

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

            _match = regex_0.match(buf, offset_0)
            if _match:
                _end = _match.end()
                column_0 += (_end - offset_0)
                offset_0 = _end
            else:
                offset_0 = -1
                break

            children_1 = []
            value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
            while True: # start capture
                count_0 = 0
                while count_0 < 1:
                    offset_1 = offset_0
                    column_1 = column_0
                    indent_column_1 = list(indent_column_0)
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        #print('entry rep rule', offset_0, offset_1)
                        children_3 = []
                        value_2 = Node(None, offset_1, offset_1, column_1, column_1, children_3, None)
                        while True: # start capture
                            while True: # start choice
                                offset_2 = offset_1
                                column_2 = column_1
                                indent_column_2 = list(indent_column_1)
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_4 = [] if children_3 is not None else None
                                while True: # case
                                    if buf[offset_2:offset_2+1] == '"':
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    children_5 = None
                                    value_3 = Node(None, offset_2, offset_2, column_2, column_2, children_5, None)
                                    while True: # start capture
                                        count_1 = 0
                                        while True:
                                            offset_3 = offset_2
                                            column_3 = column_2
                                            indent_column_3 = list(indent_column_2)
                                            partial_tab_offset_3 = partial_tab_offset_2
                                            partial_tab_width_3 = partial_tab_width_2
                                            children_6 = [] if children_5 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_2, offset_3)
                                                while True: # start choice
                                                    offset_4 = offset_3
                                                    column_4 = column_3
                                                    indent_column_4 = list(indent_column_3)
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_7 = [] if children_6 is not None else None
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
                                                        indent_column_3 = indent_column_4
                                                        partial_tab_offset_3 = partial_tab_offset_4
                                                        partial_tab_width_3 = partial_tab_width_4
                                                        if children_7 is not None and children_7 is not None:
                                                            children_6.extend(children_7)
                                                        break
                                                    # end case
                                                    offset_4 = offset_3
                                                    column_4 = column_3
                                                    indent_column_4 = list(indent_column_3)
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_7 = [] if children_6 is not None else None
                                                    while True: # case
                                                        if buf[offset_4:offset_4+2] == '\\x':
                                                            offset_4 += 2
                                                            column_4 += 2
                                                        else:
                                                            offset_4 = -1
                                                            break

                                                        while True: # start reject
                                                            children_8 = []
                                                            offset_5 = offset_4 + 0
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
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
                                                        indent_column_3 = indent_column_4
                                                        partial_tab_offset_3 = partial_tab_offset_4
                                                        partial_tab_width_3 = partial_tab_width_4
                                                        if children_7 is not None and children_7 is not None:
                                                            children_6.extend(children_7)
                                                        break
                                                    # end case
                                                    offset_4 = offset_3
                                                    column_4 = column_3
                                                    indent_column_4 = list(indent_column_3)
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_7 = [] if children_6 is not None else None
                                                    while True: # case
                                                        if buf[offset_4:offset_4+2] == '\\u':
                                                            offset_4 += 2
                                                            column_4 += 2
                                                        else:
                                                            offset_4 = -1
                                                            break

                                                        while True: # start reject
                                                            children_8 = []
                                                            offset_5 = offset_4 + 0
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
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
                                                            children_8 = []
                                                            offset_5 = offset_4 + 0
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
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
                                                        indent_column_3 = indent_column_4
                                                        partial_tab_offset_3 = partial_tab_offset_4
                                                        partial_tab_width_3 = partial_tab_width_4
                                                        if children_7 is not None and children_7 is not None:
                                                            children_6.extend(children_7)
                                                        break
                                                    # end case
                                                    offset_4 = offset_3
                                                    column_4 = column_3
                                                    indent_column_4 = list(indent_column_3)
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_7 = [] if children_6 is not None else None
                                                    while True: # case
                                                        if buf[offset_4:offset_4+2] == '\\U':
                                                            offset_4 += 2
                                                            column_4 += 2
                                                        else:
                                                            offset_4 = -1
                                                            break

                                                        while True: # start reject
                                                            children_8 = []
                                                            offset_5 = offset_4 + 0
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
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
                                                            children_8 = []
                                                            offset_5 = offset_4 + 0
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
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
                                                        indent_column_3 = indent_column_4
                                                        partial_tab_offset_3 = partial_tab_offset_4
                                                        partial_tab_width_3 = partial_tab_width_4
                                                        if children_7 is not None and children_7 is not None:
                                                            children_6.extend(children_7)
                                                        break
                                                    # end case
                                                    offset_4 = offset_3
                                                    column_4 = column_3
                                                    indent_column_4 = list(indent_column_3)
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_7 = [] if children_6 is not None else None
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
                                                        indent_column_3 = indent_column_4
                                                        partial_tab_offset_3 = partial_tab_offset_4
                                                        partial_tab_width_3 = partial_tab_width_4
                                                        if children_7 is not None and children_7 is not None:
                                                            children_6.extend(children_7)
                                                        break
                                                    # end case
                                                    offset_3 = -1 # no more choices
                                                    break # end choice
                                                if offset_3 == -1:
                                                    break

                                                #print('safe exit rep rule', offset_2, offset_3)
                                                break
                                            #print('exit rep rule', offset_2, offset_3)
                                            if offset_3 == -1:
                                                break
                                            if offset_2 == offset_3: break
                                            if children_6 is not None and children_6 is not None:
                                                children_5.extend(children_6)
                                            offset_2 = offset_3
                                            column_2 = column_3
                                            indent_column_2 = indent_column_3
                                            partial_tab_offset_2 = partial_tab_offset_3
                                            partial_tab_width_2 = partial_tab_width_3
                                            count_1 += 1
                                        if offset_2 == -1:
                                            break
                                        value_4 = count_1

                                        break
                                    if offset_2 == -1:
                                        break
                                    value_3.name = 'string'
                                    value_3.end = offset_2
                                    value_3.end_column = column_2
                                    value_3.value = None
                                    children_4.append(value_3)

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
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    break
                                # end case
                                offset_2 = offset_1
                                column_2 = column_1
                                indent_column_2 = list(indent_column_1)
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_4 = [] if children_3 is not None else None
                                while True: # case
                                    if buf[offset_2:offset_2+1] == "'":
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    children_5 = None
                                    value_5 = Node(None, offset_2, offset_2, column_2, column_2, children_5, None)
                                    while True: # start capture
                                        count_1 = 0
                                        while True:
                                            offset_3 = offset_2
                                            column_3 = column_2
                                            indent_column_3 = list(indent_column_2)
                                            partial_tab_offset_3 = partial_tab_offset_2
                                            partial_tab_width_3 = partial_tab_width_2
                                            children_6 = [] if children_5 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_2, offset_3)
                                                while True: # start choice
                                                    offset_4 = offset_3
                                                    column_4 = column_3
                                                    indent_column_4 = list(indent_column_3)
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_7 = [] if children_6 is not None else None
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
                                                        indent_column_3 = indent_column_4
                                                        partial_tab_offset_3 = partial_tab_offset_4
                                                        partial_tab_width_3 = partial_tab_width_4
                                                        if children_7 is not None and children_7 is not None:
                                                            children_6.extend(children_7)
                                                        break
                                                    # end case
                                                    offset_4 = offset_3
                                                    column_4 = column_3
                                                    indent_column_4 = list(indent_column_3)
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_7 = [] if children_6 is not None else None
                                                    while True: # case
                                                        if buf[offset_4:offset_4+2] == '\\x':
                                                            offset_4 += 2
                                                            column_4 += 2
                                                        else:
                                                            offset_4 = -1
                                                            break

                                                        while True: # start reject
                                                            children_8 = []
                                                            offset_5 = offset_4 + 0
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
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
                                                        indent_column_3 = indent_column_4
                                                        partial_tab_offset_3 = partial_tab_offset_4
                                                        partial_tab_width_3 = partial_tab_width_4
                                                        if children_7 is not None and children_7 is not None:
                                                            children_6.extend(children_7)
                                                        break
                                                    # end case
                                                    offset_4 = offset_3
                                                    column_4 = column_3
                                                    indent_column_4 = list(indent_column_3)
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_7 = [] if children_6 is not None else None
                                                    while True: # case
                                                        if buf[offset_4:offset_4+2] == '\\u':
                                                            offset_4 += 2
                                                            column_4 += 2
                                                        else:
                                                            offset_4 = -1
                                                            break

                                                        while True: # start reject
                                                            children_8 = []
                                                            offset_5 = offset_4 + 0
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
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
                                                            children_8 = []
                                                            offset_5 = offset_4 + 0
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
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
                                                        indent_column_3 = indent_column_4
                                                        partial_tab_offset_3 = partial_tab_offset_4
                                                        partial_tab_width_3 = partial_tab_width_4
                                                        if children_7 is not None and children_7 is not None:
                                                            children_6.extend(children_7)
                                                        break
                                                    # end case
                                                    offset_4 = offset_3
                                                    column_4 = column_3
                                                    indent_column_4 = list(indent_column_3)
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_7 = [] if children_6 is not None else None
                                                    while True: # case
                                                        if buf[offset_4:offset_4+2] == '\\U':
                                                            offset_4 += 2
                                                            column_4 += 2
                                                        else:
                                                            offset_4 = -1
                                                            break

                                                        while True: # start reject
                                                            children_8 = []
                                                            offset_5 = offset_4 + 0
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
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
                                                            children_8 = []
                                                            offset_5 = offset_4 + 0
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
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
                                                        indent_column_3 = indent_column_4
                                                        partial_tab_offset_3 = partial_tab_offset_4
                                                        partial_tab_width_3 = partial_tab_width_4
                                                        if children_7 is not None and children_7 is not None:
                                                            children_6.extend(children_7)
                                                        break
                                                    # end case
                                                    offset_4 = offset_3
                                                    column_4 = column_3
                                                    indent_column_4 = list(indent_column_3)
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_7 = [] if children_6 is not None else None
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
                                                        indent_column_3 = indent_column_4
                                                        partial_tab_offset_3 = partial_tab_offset_4
                                                        partial_tab_width_3 = partial_tab_width_4
                                                        if children_7 is not None and children_7 is not None:
                                                            children_6.extend(children_7)
                                                        break
                                                    # end case
                                                    offset_3 = -1 # no more choices
                                                    break # end choice
                                                if offset_3 == -1:
                                                    break

                                                #print('safe exit rep rule', offset_2, offset_3)
                                                break
                                            #print('exit rep rule', offset_2, offset_3)
                                            if offset_3 == -1:
                                                break
                                            if offset_2 == offset_3: break
                                            if children_6 is not None and children_6 is not None:
                                                children_5.extend(children_6)
                                            offset_2 = offset_3
                                            column_2 = column_3
                                            indent_column_2 = indent_column_3
                                            partial_tab_offset_2 = partial_tab_offset_3
                                            partial_tab_width_2 = partial_tab_width_3
                                            count_1 += 1
                                        if offset_2 == -1:
                                            break
                                        value_6 = count_1

                                        break
                                    if offset_2 == -1:
                                        break
                                    value_5.name = 'string'
                                    value_5.end = offset_2
                                    value_5.end_column = column_2
                                    value_5.value = None
                                    children_4.append(value_5)

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
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    break
                                # end case
                                offset_1 = -1 # no more choices
                                break # end choice
                            if offset_1 == -1:
                                break

                            _match = regex_0.match(buf, offset_1)
                            if _match:
                                _end = _match.end()
                                column_1 += (_end - offset_1)
                                offset_1 = _end
                            else:
                                offset_1 = -1
                                break

                            if buf[offset_1:offset_1+1] == ':':
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

                            offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_value(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                            if offset_1 == -1: break


                            break
                        if offset_1 == -1:
                            break
                        value_2.name = 'pair'
                        value_2.end = offset_1
                        value_2.end_column = column_1
                        value_2.value = None
                        children_2.append(value_2)

                        _match = regex_0.match(buf, offset_1)
                        if _match:
                            _end = _match.end()
                            column_1 += (_end - offset_1)
                            offset_1 = _end
                        else:
                            offset_1 = -1
                            break

                        count_1 = 0
                        while True:
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                #print('entry rep rule', offset_1, offset_2)
                                if buf[offset_2:offset_2+1] == ',':
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

                                _match = regex_0.match(buf, offset_2)
                                if _match:
                                    _end = _match.end()
                                    column_2 += (_end - offset_2)
                                    offset_2 = _end
                                else:
                                    offset_2 = -1
                                    break

                                children_4 = []
                                value_8 = Node(None, offset_2, offset_2, column_2, column_2, children_4, None)
                                while True: # start capture
                                    while True: # start choice
                                        offset_3 = offset_2
                                        column_3 = column_2
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True: # case
                                            if buf[offset_3:offset_3+1] == '"':
                                                offset_3 += 1
                                                column_3 += 1
                                            else:
                                                offset_3 = -1
                                                break

                                            children_6 = None
                                            value_9 = Node(None, offset_3, offset_3, column_3, column_3, children_6, None)
                                            while True: # start capture
                                                count_2 = 0
                                                while True:
                                                    offset_4 = offset_3
                                                    column_4 = column_3
                                                    indent_column_4 = list(indent_column_3)
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_7 = [] if children_6 is not None else None
                                                    while True:
                                                        #print('entry rep rule', offset_3, offset_4)
                                                        while True: # start choice
                                                            offset_5 = offset_4
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
                                                            children_8 = [] if children_7 is not None else None
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
                                                                indent_column_4 = indent_column_5
                                                                partial_tab_offset_4 = partial_tab_offset_5
                                                                partial_tab_width_4 = partial_tab_width_5
                                                                if children_8 is not None and children_8 is not None:
                                                                    children_7.extend(children_8)
                                                                break
                                                            # end case
                                                            offset_5 = offset_4
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
                                                            children_8 = [] if children_7 is not None else None
                                                            while True: # case
                                                                if buf[offset_5:offset_5+2] == '\\x':
                                                                    offset_5 += 2
                                                                    column_5 += 2
                                                                else:
                                                                    offset_5 = -1
                                                                    break

                                                                while True: # start reject
                                                                    children_9 = []
                                                                    offset_6 = offset_5 + 0
                                                                    column_6 = column_5
                                                                    indent_column_6 = list(indent_column_5)
                                                                    partial_tab_offset_6 = partial_tab_offset_5
                                                                    partial_tab_width_6 = partial_tab_width_5
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
                                                                indent_column_4 = indent_column_5
                                                                partial_tab_offset_4 = partial_tab_offset_5
                                                                partial_tab_width_4 = partial_tab_width_5
                                                                if children_8 is not None and children_8 is not None:
                                                                    children_7.extend(children_8)
                                                                break
                                                            # end case
                                                            offset_5 = offset_4
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
                                                            children_8 = [] if children_7 is not None else None
                                                            while True: # case
                                                                if buf[offset_5:offset_5+2] == '\\u':
                                                                    offset_5 += 2
                                                                    column_5 += 2
                                                                else:
                                                                    offset_5 = -1
                                                                    break

                                                                while True: # start reject
                                                                    children_9 = []
                                                                    offset_6 = offset_5 + 0
                                                                    column_6 = column_5
                                                                    indent_column_6 = list(indent_column_5)
                                                                    partial_tab_offset_6 = partial_tab_offset_5
                                                                    partial_tab_width_6 = partial_tab_width_5
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
                                                                    children_9 = []
                                                                    offset_6 = offset_5 + 0
                                                                    column_6 = column_5
                                                                    indent_column_6 = list(indent_column_5)
                                                                    partial_tab_offset_6 = partial_tab_offset_5
                                                                    partial_tab_width_6 = partial_tab_width_5
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
                                                                indent_column_4 = indent_column_5
                                                                partial_tab_offset_4 = partial_tab_offset_5
                                                                partial_tab_width_4 = partial_tab_width_5
                                                                if children_8 is not None and children_8 is not None:
                                                                    children_7.extend(children_8)
                                                                break
                                                            # end case
                                                            offset_5 = offset_4
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
                                                            children_8 = [] if children_7 is not None else None
                                                            while True: # case
                                                                if buf[offset_5:offset_5+2] == '\\U':
                                                                    offset_5 += 2
                                                                    column_5 += 2
                                                                else:
                                                                    offset_5 = -1
                                                                    break

                                                                while True: # start reject
                                                                    children_9 = []
                                                                    offset_6 = offset_5 + 0
                                                                    column_6 = column_5
                                                                    indent_column_6 = list(indent_column_5)
                                                                    partial_tab_offset_6 = partial_tab_offset_5
                                                                    partial_tab_width_6 = partial_tab_width_5
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
                                                                    children_9 = []
                                                                    offset_6 = offset_5 + 0
                                                                    column_6 = column_5
                                                                    indent_column_6 = list(indent_column_5)
                                                                    partial_tab_offset_6 = partial_tab_offset_5
                                                                    partial_tab_width_6 = partial_tab_width_5
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
                                                                indent_column_4 = indent_column_5
                                                                partial_tab_offset_4 = partial_tab_offset_5
                                                                partial_tab_width_4 = partial_tab_width_5
                                                                if children_8 is not None and children_8 is not None:
                                                                    children_7.extend(children_8)
                                                                break
                                                            # end case
                                                            offset_5 = offset_4
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
                                                            children_8 = [] if children_7 is not None else None
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
                                                                indent_column_4 = indent_column_5
                                                                partial_tab_offset_4 = partial_tab_offset_5
                                                                partial_tab_width_4 = partial_tab_width_5
                                                                if children_8 is not None and children_8 is not None:
                                                                    children_7.extend(children_8)
                                                                break
                                                            # end case
                                                            offset_4 = -1 # no more choices
                                                            break # end choice
                                                        if offset_4 == -1:
                                                            break

                                                        #print('safe exit rep rule', offset_3, offset_4)
                                                        break
                                                    #print('exit rep rule', offset_3, offset_4)
                                                    if offset_4 == -1:
                                                        break
                                                    if offset_3 == offset_4: break
                                                    if children_7 is not None and children_7 is not None:
                                                        children_6.extend(children_7)
                                                    offset_3 = offset_4
                                                    column_3 = column_4
                                                    indent_column_3 = indent_column_4
                                                    partial_tab_offset_3 = partial_tab_offset_4
                                                    partial_tab_width_3 = partial_tab_width_4
                                                    count_2 += 1
                                                if offset_3 == -1:
                                                    break
                                                value_10 = count_2

                                                break
                                            if offset_3 == -1:
                                                break
                                            value_9.name = 'string'
                                            value_9.end = offset_3
                                            value_9.end_column = column_3
                                            value_9.value = None
                                            children_5.append(value_9)

                                            if buf[offset_3:offset_3+1] == '"':
                                                offset_3 += 1
                                                column_3 += 1
                                            else:
                                                offset_3 = -1
                                                break


                                            break
                                        if offset_3 != -1:
                                            offset_2 = offset_3
                                            column_2 = column_3
                                            indent_column_2 = indent_column_3
                                            partial_tab_offset_2 = partial_tab_offset_3
                                            partial_tab_width_2 = partial_tab_width_3
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            break
                                        # end case
                                        offset_3 = offset_2
                                        column_3 = column_2
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True: # case
                                            if buf[offset_3:offset_3+1] == "'":
                                                offset_3 += 1
                                                column_3 += 1
                                            else:
                                                offset_3 = -1
                                                break

                                            children_6 = None
                                            value_11 = Node(None, offset_3, offset_3, column_3, column_3, children_6, None)
                                            while True: # start capture
                                                count_2 = 0
                                                while True:
                                                    offset_4 = offset_3
                                                    column_4 = column_3
                                                    indent_column_4 = list(indent_column_3)
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_7 = [] if children_6 is not None else None
                                                    while True:
                                                        #print('entry rep rule', offset_3, offset_4)
                                                        while True: # start choice
                                                            offset_5 = offset_4
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
                                                            children_8 = [] if children_7 is not None else None
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
                                                                indent_column_4 = indent_column_5
                                                                partial_tab_offset_4 = partial_tab_offset_5
                                                                partial_tab_width_4 = partial_tab_width_5
                                                                if children_8 is not None and children_8 is not None:
                                                                    children_7.extend(children_8)
                                                                break
                                                            # end case
                                                            offset_5 = offset_4
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
                                                            children_8 = [] if children_7 is not None else None
                                                            while True: # case
                                                                if buf[offset_5:offset_5+2] == '\\x':
                                                                    offset_5 += 2
                                                                    column_5 += 2
                                                                else:
                                                                    offset_5 = -1
                                                                    break

                                                                while True: # start reject
                                                                    children_9 = []
                                                                    offset_6 = offset_5 + 0
                                                                    column_6 = column_5
                                                                    indent_column_6 = list(indent_column_5)
                                                                    partial_tab_offset_6 = partial_tab_offset_5
                                                                    partial_tab_width_6 = partial_tab_width_5
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
                                                                indent_column_4 = indent_column_5
                                                                partial_tab_offset_4 = partial_tab_offset_5
                                                                partial_tab_width_4 = partial_tab_width_5
                                                                if children_8 is not None and children_8 is not None:
                                                                    children_7.extend(children_8)
                                                                break
                                                            # end case
                                                            offset_5 = offset_4
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
                                                            children_8 = [] if children_7 is not None else None
                                                            while True: # case
                                                                if buf[offset_5:offset_5+2] == '\\u':
                                                                    offset_5 += 2
                                                                    column_5 += 2
                                                                else:
                                                                    offset_5 = -1
                                                                    break

                                                                while True: # start reject
                                                                    children_9 = []
                                                                    offset_6 = offset_5 + 0
                                                                    column_6 = column_5
                                                                    indent_column_6 = list(indent_column_5)
                                                                    partial_tab_offset_6 = partial_tab_offset_5
                                                                    partial_tab_width_6 = partial_tab_width_5
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
                                                                    children_9 = []
                                                                    offset_6 = offset_5 + 0
                                                                    column_6 = column_5
                                                                    indent_column_6 = list(indent_column_5)
                                                                    partial_tab_offset_6 = partial_tab_offset_5
                                                                    partial_tab_width_6 = partial_tab_width_5
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
                                                                indent_column_4 = indent_column_5
                                                                partial_tab_offset_4 = partial_tab_offset_5
                                                                partial_tab_width_4 = partial_tab_width_5
                                                                if children_8 is not None and children_8 is not None:
                                                                    children_7.extend(children_8)
                                                                break
                                                            # end case
                                                            offset_5 = offset_4
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
                                                            children_8 = [] if children_7 is not None else None
                                                            while True: # case
                                                                if buf[offset_5:offset_5+2] == '\\U':
                                                                    offset_5 += 2
                                                                    column_5 += 2
                                                                else:
                                                                    offset_5 = -1
                                                                    break

                                                                while True: # start reject
                                                                    children_9 = []
                                                                    offset_6 = offset_5 + 0
                                                                    column_6 = column_5
                                                                    indent_column_6 = list(indent_column_5)
                                                                    partial_tab_offset_6 = partial_tab_offset_5
                                                                    partial_tab_width_6 = partial_tab_width_5
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
                                                                    children_9 = []
                                                                    offset_6 = offset_5 + 0
                                                                    column_6 = column_5
                                                                    indent_column_6 = list(indent_column_5)
                                                                    partial_tab_offset_6 = partial_tab_offset_5
                                                                    partial_tab_width_6 = partial_tab_width_5
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
                                                                indent_column_4 = indent_column_5
                                                                partial_tab_offset_4 = partial_tab_offset_5
                                                                partial_tab_width_4 = partial_tab_width_5
                                                                if children_8 is not None and children_8 is not None:
                                                                    children_7.extend(children_8)
                                                                break
                                                            # end case
                                                            offset_5 = offset_4
                                                            column_5 = column_4
                                                            indent_column_5 = list(indent_column_4)
                                                            partial_tab_offset_5 = partial_tab_offset_4
                                                            partial_tab_width_5 = partial_tab_width_4
                                                            children_8 = [] if children_7 is not None else None
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
                                                                indent_column_4 = indent_column_5
                                                                partial_tab_offset_4 = partial_tab_offset_5
                                                                partial_tab_width_4 = partial_tab_width_5
                                                                if children_8 is not None and children_8 is not None:
                                                                    children_7.extend(children_8)
                                                                break
                                                            # end case
                                                            offset_4 = -1 # no more choices
                                                            break # end choice
                                                        if offset_4 == -1:
                                                            break

                                                        #print('safe exit rep rule', offset_3, offset_4)
                                                        break
                                                    #print('exit rep rule', offset_3, offset_4)
                                                    if offset_4 == -1:
                                                        break
                                                    if offset_3 == offset_4: break
                                                    if children_7 is not None and children_7 is not None:
                                                        children_6.extend(children_7)
                                                    offset_3 = offset_4
                                                    column_3 = column_4
                                                    indent_column_3 = indent_column_4
                                                    partial_tab_offset_3 = partial_tab_offset_4
                                                    partial_tab_width_3 = partial_tab_width_4
                                                    count_2 += 1
                                                if offset_3 == -1:
                                                    break
                                                value_12 = count_2

                                                break
                                            if offset_3 == -1:
                                                break
                                            value_11.name = 'string'
                                            value_11.end = offset_3
                                            value_11.end_column = column_3
                                            value_11.value = None
                                            children_5.append(value_11)

                                            if buf[offset_3:offset_3+1] == "'":
                                                offset_3 += 1
                                                column_3 += 1
                                            else:
                                                offset_3 = -1
                                                break


                                            break
                                        if offset_3 != -1:
                                            offset_2 = offset_3
                                            column_2 = column_3
                                            indent_column_2 = indent_column_3
                                            partial_tab_offset_2 = partial_tab_offset_3
                                            partial_tab_width_2 = partial_tab_width_3
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            break
                                        # end case
                                        offset_2 = -1 # no more choices
                                        break # end choice
                                    if offset_2 == -1:
                                        break

                                    _match = regex_0.match(buf, offset_2)
                                    if _match:
                                        _end = _match.end()
                                        column_2 += (_end - offset_2)
                                        offset_2 = _end
                                    else:
                                        offset_2 = -1
                                        break

                                    if buf[offset_2:offset_2+1] == ':':
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    _match = regex_0.match(buf, offset_2)
                                    if _match:
                                        _end = _match.end()
                                        column_2 += (_end - offset_2)
                                        offset_2 = _end
                                    else:
                                        offset_2 = -1
                                        break

                                    offset_2, column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_rson_value(buf, buf_start, buf_eof, offset_2, column_2, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                    if offset_2 == -1: break


                                    break
                                if offset_2 == -1:
                                    break
                                value_8.name = 'pair'
                                value_8.end = offset_2
                                value_8.end_column = column_2
                                value_8.value = None
                                children_3.append(value_8)

                                _match = regex_0.match(buf, offset_2)
                                if _match:
                                    _end = _match.end()
                                    column_2 += (_end - offset_2)
                                    offset_2 = _end
                                else:
                                    offset_2 = -1
                                    break

                                #print('safe exit rep rule', offset_1, offset_2)
                                break
                            #print('exit rep rule', offset_1, offset_2)
                            if offset_2 == -1:
                                break
                            if offset_1 == offset_2: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_1 = offset_2
                            column_1 = column_2
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            count_1 += 1
                        if offset_1 == -1:
                            break
                        value_7 = count_1

                        _match = regex_11.match(buf, offset_1)
                        if _match:
                            _end = _match.end()
                            column_1 += (_end - offset_1)
                            offset_1 = _end
                        else:
                            offset_1 = -1
                            break

                        #print('safe exit rep rule', offset_0, offset_1)
                        break
                    #print('exit rep rule', offset_0, offset_1)
                    if offset_1 == -1:
                        break
                    if offset_0 == offset_1: break
                    if children_2 is not None and children_2 is not None:
                        children_1.extend(children_2)
                    offset_0 = offset_1
                    column_0 = column_1
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    count_0 += 1
                    break
                if offset_0 == -1:
                    break
                value_1 = count_0

                break
            if offset_0 == -1:
                break
            value_0.name = 'object'
            value_0.end = offset_0
            value_0.end_column = column_0
            value_0.value = None
            children_0.append(value_0)

            if buf[offset_0:offset_0+1] == '}':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0
