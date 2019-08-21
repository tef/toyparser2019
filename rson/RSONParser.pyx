# cython: language_level=3, bounds_check=False
import unicodedata
class Node:
    def __init__(self, name, start, end, children, value):
        self.name = name
        self.start = start
        self.end = end
        self.children = children if children is not None else ()
        self.value = value
    def __str__(self):
        return '{}[{}:{}]'.format(self.name, self.start, self.end)
    def build(self, buf, builder):
        children = [child.build(buf, builder) for child in self.children]
        if self.name == "value": return self.value
        return builder[self.name](buf, self.start, self.end, children)


cdef class Parser:
    cdef dict cache
    cdef int tabstop
    cdef int allow_mixed_indent

    def __init__(self, tabstop=None, allow_mixed_indent=True):
         self.tabstop = tabstop or 8
         self.cache = None
         self.allow_mixed_indent = allow_mixed_indent

    def parse(self, buf, offset=0, end=None, err=None, builder=None):
        self.cache = dict()
        end = len(buf) if end is None else end
        column, indent_column, eof = 0, (0, None), end
        prefix, children = [], []
        new_offset, column, indent_column, partial_tab_offset, partial_tab_width = self.parse_document(buf, offset, eof, column, indent_column, prefix, children, 0, 0)
        if children and new_offset == end:
             if builder is None: return Node('document', offset, new_offset, children, None)
             return children[-1].build(buf, builder)
        print('no', offset, new_offset, end, buf[new_offset:])
        if err is not None: raise err(buf, new_offset, 'no')

    cdef parse_document(self, str buf, int offset_0, int buf_eof, int column_0, tuple indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2
        cdef int column_1, column_2

        cdef list children_1, children_2
        cdef int count_1, count_2
        cdef tuple indent_column_1, indent_column_2
        cdef int partial_tab_offset_1, partial_tab_offset_2
        cdef int partial_tab_width_1, partial_tab_width_2
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
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '#':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            if offset_2 == buf_eof:
                                offset_2 = -1
                                break

                            codepoint = (buf[offset_2])

                            if codepoint == 10:
                                offset_2 = -1
                                break
                            else:
                                offset_2 += 1
                                column_2 += 1

                            break
                        if offset_2 == -1:
                            break
                        if offset_1 == offset_2: break
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        offset_1 = offset_2
                        column_1 = column_2
                        indent_column_1 = indent_column_2
                        partial_tab_offset_1 = partial_tab_offset_2
                        partial_tab_width_1 = partial_tab_width_2
                        count_1 += 1
                    if offset_1 == -1:
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


            offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_rson_value(buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0)
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
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '#':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            if offset_2 == buf_eof:
                                offset_2 = -1
                                break

                            codepoint = (buf[offset_2])

                            if codepoint == 10:
                                offset_2 = -1
                                break
                            else:
                                offset_2 += 1
                                column_2 += 1

                            break
                        if offset_2 == -1:
                            break
                        if offset_1 == offset_2: break
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        offset_1 = offset_2
                        column_1 = column_2
                        indent_column_1 = indent_column_2
                        partial_tab_offset_1 = partial_tab_offset_2
                        partial_tab_width_1 = partial_tab_width_2
                        count_1 += 1
                    if offset_1 == -1:
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
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    cdef parse_rson_value(self, str buf, int offset_0, int buf_eof, int column_0, tuple indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2, offset_3, offset_4
        cdef int column_1, column_2

        cdef list children_1, children_2, children_3, children_4
        cdef int count_1
        cdef tuple indent_column_1, indent_column_2
        cdef int partial_tab_offset_1, partial_tab_offset_2
        cdef int partial_tab_width_1, partial_tab_width_2
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '@':
                            offset_2 += 1
                            column_1 += 1
                        else:
                            offset_2 = -1
                            break

                        offset_3 = offset_2
                        children_3 = None
                        while True: # start capture
                            if offset_3 == buf_eof:
                                offset_3 = -1
                                break

                            codepoint = (buf[offset_3])

                            if 97 <= codepoint <= 122:
                                offset_3 += 1
                                column_1 += 1
                            elif 97 <= codepoint <= 90:
                                offset_3 += 1
                                column_1 += 1
                            else:
                                offset_3 = -1
                                break

                            count_0 = 0
                            while True:
                                offset_4 = offset_3
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_4 = [] if children_3 is not None else None
                                while True:
                                    if offset_4 == buf_eof:
                                        offset_4 = -1
                                        break

                                    codepoint = (buf[offset_4])

                                    if 48 <= codepoint <= 57:
                                        offset_4 += 1
                                        column_2 += 1
                                    elif 97 <= codepoint <= 122:
                                        offset_4 += 1
                                        column_2 += 1
                                    elif 65 <= codepoint <= 90:
                                        offset_4 += 1
                                        column_2 += 1
                                    elif codepoint == 95:
                                        offset_4 += 1
                                        column_2 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    break
                                if offset_4 == -1:
                                    break
                                if offset_3 == offset_4: break
                                if children_4 is not None and children_4 is not None:
                                    children_3.extend(children_4)
                                offset_3 = offset_4
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                count_0 += 1
                            if offset_3 == -1:
                                break

                            break
                        if offset_3 == -1:
                            offset_2 = -1
                            break
                        value_0 = Node('identifier', offset_2, offset_3, children_3, None)
                        children_2.append(value_0)
                        offset_2 = offset_3

                        if offset_2 + 1 <= buf_eof and buf[offset_2+0] == ' ':
                            offset_2 += 1
                            column_1 += 1
                        else:
                            offset_2 = -1
                            break

                        offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_literal(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                        if offset_2 == -1: break


                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_1 = Node('tagged', offset_1, offset_2, children_2, None)
                    children_1.append(value_1)
                    offset_1 = offset_2


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
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_literal(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    cdef parse_rson_literal(self, str buf, int offset_0, int buf_eof, int column_0, tuple indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2, offset_3, offset_4, offset_5, offset_6
        cdef int column_1, column_2, column_3, column_4, column_5

        cdef list children_1, children_2, children_3, children_4, children_5, children_6
        cdef int count_1, count_2, count_3
        cdef tuple indent_column_1, indent_column_2, indent_column_3, indent_column_4, indent_column_5
        cdef int partial_tab_offset_1, partial_tab_offset_2, partial_tab_offset_3, partial_tab_offset_4, partial_tab_offset_5
        cdef int partial_tab_width_1, partial_tab_width_2, partial_tab_width_3, partial_tab_width_4, partial_tab_width_5
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_list(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_object(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    while True: # start choice
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '"':
                                offset_2 += 1
                                column_2 += 1
                            else:
                                offset_2 = -1
                                break

                            offset_3 = offset_2
                            children_3 = None
                            while True: # start capture
                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        while True: # start choice
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if codepoint <= 31:
                                                    offset_5 = -1
                                                    break
                                                elif codepoint == 92:
                                                    offset_5 = -1
                                                    break
                                                elif codepoint == 34:
                                                    offset_5 = -1
                                                    break
                                                elif 55296 <= codepoint <= 57343:
                                                    offset_5 = -1
                                                    break
                                                else:
                                                    offset_5 += 1
                                                    column_4 += 1


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_3 = column_4
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '\\' and buf[offset_5+1] == 'x':
                                                    offset_5 += 2
                                                    column_4 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    codepoint = (buf[offset_6])

                                                    if 48 <= codepoint <= 49:
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_3 = column_4
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '\\' and buf[offset_5+1] == 'u':
                                                    offset_5 += 2
                                                    column_4 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if offset_6 + 3 <= buf_eof and buf[offset_6+0] == '0' and buf[offset_6+1] == '0' and buf[offset_6+2] == '0':
                                                        offset_6 += 3
                                                        column_5 += 3
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    codepoint = (buf[offset_6])

                                                    if 48 <= codepoint <= 49:
                                                        offset_6 += 1
                                                        column_5 += 1
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
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'D':
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    elif offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'd':
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    codepoint = (buf[offset_6])

                                                    if 56 <= codepoint <= 57:
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    elif 65 <= codepoint <= 70:
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_3 = column_4
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '\\' and buf[offset_5+1] == 'U':
                                                    offset_5 += 2
                                                    column_4 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if offset_6 + 7 <= buf_eof and buf[offset_6+0] == '0' and buf[offset_6+1] == '0' and buf[offset_6+2] == '0' and buf[offset_6+3] == '0' and buf[offset_6+4] == '0' and buf[offset_6+5] == '0' and buf[offset_6+6] == '0':
                                                        offset_6 += 7
                                                        column_5 += 7
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    codepoint = (buf[offset_6])

                                                    if 48 <= codepoint <= 49:
                                                        offset_6 += 1
                                                        column_5 += 1
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
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if offset_6 + 4 <= buf_eof and buf[offset_6+0] == '0' and buf[offset_6+1] == '0' and buf[offset_6+2] == '0' and buf[offset_6+3] == '0':
                                                        offset_6 += 4
                                                        column_5 += 4
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'D':
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    elif offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'd':
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    codepoint = (buf[offset_6])

                                                    if 56 <= codepoint <= 57:
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    elif 65 <= codepoint <= 70:
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_3 = column_4
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if offset_5 + 1 <= buf_eof and buf[offset_5+0] == '\\':
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if codepoint == 34:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 92:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 47:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 98:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 110:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 114:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 116:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 39:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 10:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_3 = column_4
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
                                    column_2 = column_3
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
                            value_0 = Node('string', offset_2, offset_3, children_3, None)
                            children_2.append(value_0)
                            offset_2 = offset_3

                            if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '"':
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
                        indent_column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            if offset_2 + 1 <= buf_eof and buf[offset_2+0] == "'":
                                offset_2 += 1
                                column_2 += 1
                            else:
                                offset_2 = -1
                                break

                            offset_3 = offset_2
                            children_3 = None
                            while True: # start capture
                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        while True: # start choice
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if codepoint <= 31:
                                                    offset_5 = -1
                                                    break
                                                elif codepoint == 92:
                                                    offset_5 = -1
                                                    break
                                                elif codepoint == 39:
                                                    offset_5 = -1
                                                    break
                                                elif 55296 <= codepoint <= 57343:
                                                    offset_5 = -1
                                                    break
                                                else:
                                                    offset_5 += 1
                                                    column_4 += 1


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_3 = column_4
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '\\' and buf[offset_5+1] == 'x':
                                                    offset_5 += 2
                                                    column_4 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    codepoint = (buf[offset_6])

                                                    if 48 <= codepoint <= 49:
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_3 = column_4
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '\\' and buf[offset_5+1] == 'u':
                                                    offset_5 += 2
                                                    column_4 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if offset_6 + 2 <= buf_eof and buf[offset_6+0] == '0' and buf[offset_6+1] == '0':
                                                        offset_6 += 2
                                                        column_5 += 2
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    codepoint = (buf[offset_6])

                                                    if 48 <= codepoint <= 49:
                                                        offset_6 += 1
                                                        column_5 += 1
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
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'D':
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    elif offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'd':
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    codepoint = (buf[offset_6])

                                                    if 56 <= codepoint <= 57:
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    elif 65 <= codepoint <= 70:
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_3 = column_4
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '\\' and buf[offset_5+1] == 'U':
                                                    offset_5 += 2
                                                    column_4 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5 + 0
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if offset_6 + 6 <= buf_eof and buf[offset_6+0] == '0' and buf[offset_6+1] == '0' and buf[offset_6+2] == '0' and buf[offset_6+3] == '0' and buf[offset_6+4] == '0' and buf[offset_6+5] == '0':
                                                        offset_6 += 6
                                                        column_5 += 6
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    codepoint = (buf[offset_6])

                                                    if 48 <= codepoint <= 49:
                                                        offset_6 += 1
                                                        column_5 += 1
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
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    if offset_6 + 4 <= buf_eof and buf[offset_6+0] == '0' and buf[offset_6+1] == '0' and buf[offset_6+2] == '0' and buf[offset_6+3] == '0':
                                                        offset_6 += 4
                                                        column_5 += 4
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'D':
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    elif offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'd':
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    codepoint = (buf[offset_6])

                                                    if 56 <= codepoint <= 57:
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    elif 65 <= codepoint <= 70:
                                                        offset_6 += 1
                                                        column_5 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_3 = column_4
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if offset_5 + 1 <= buf_eof and buf[offset_5+0] == '\\':
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if codepoint == 34:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 92:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 47:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 98:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 102:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 110:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 114:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 116:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 39:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif codepoint == 10:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_3 = column_4
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
                                    column_2 = column_3
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
                            value_1 = Node('string', offset_2, offset_3, children_3, None)
                            children_2.append(value_1)
                            offset_2 = offset_3

                            if offset_2 + 1 <= buf_eof and buf[offset_2+0] == "'":
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
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    children_2 = None
                    while True: # start capture
                        while True: # start choice
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                count_0 = 0
                                while count_0 < 1:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if codepoint == 45:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 43:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_0 += 1
                                    break
                                if offset_3 == -1:
                                    break

                                if offset_3 + 2 <= buf_eof and buf[offset_3+0] == '0' and buf[offset_3+1] == 'x':
                                    offset_3 += 2
                                    column_2 += 2
                                else:
                                    offset_3 = -1
                                    break

                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = (buf[offset_3])

                                if 48 <= codepoint <= 57:
                                    offset_3 += 1
                                    column_2 += 1
                                elif 65 <= codepoint <= 70:
                                    offset_3 += 1
                                    column_2 += 1
                                elif 97 <= codepoint <= 102:
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 95:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_0 += 1
                                if offset_3 == -1:
                                    break


                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                count_0 = 0
                                while count_0 < 1:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if codepoint == 45:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 43:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_0 += 1
                                    break
                                if offset_3 == -1:
                                    break

                                if offset_3 + 2 <= buf_eof and buf[offset_3+0] == '0' and buf[offset_3+1] == 'o':
                                    offset_3 += 2
                                    column_2 += 2
                                else:
                                    offset_3 = -1
                                    break

                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = (buf[offset_3])

                                if 48 <= codepoint <= 56:
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 56:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 95:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_0 += 1
                                if offset_3 == -1:
                                    break


                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                count_0 = 0
                                while count_0 < 1:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if codepoint == 45:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 43:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_0 += 1
                                    break
                                if offset_3 == -1:
                                    break

                                if offset_3 + 2 <= buf_eof and buf[offset_3+0] == '0' and buf[offset_3+1] == 'b':
                                    offset_3 += 2
                                    column_2 += 2
                                else:
                                    offset_3 = -1
                                    break

                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = (buf[offset_3])

                                if 48 <= codepoint <= 49:
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 49:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 95:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_0 += 1
                                if offset_3 == -1:
                                    break


                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                count_0 = 0
                                while count_0 < 1:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if codepoint == 45:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 43:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_0 += 1
                                    break
                                if offset_3 == -1:
                                    break

                                while True: # start choice
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '0':
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 49 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_0 = 0
                                        while True:
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_4 = offset_5
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_0 += 1
                                        if offset_4 == -1:
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_2 = column_3
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

                                count_0 = 0
                                while count_0 < 1:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '.':
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_1 = 0
                                        while True:
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if 48 <= codepoint <= 57:
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_4 = offset_5
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_1 += 1
                                        if offset_4 == -1:
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_0 += 1
                                    break
                                if offset_3 == -1:
                                    break

                                count_0 = 0
                                while count_0 < 1:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == 'e':
                                            offset_4 += 1
                                            column_3 += 1
                                        elif offset_4 + 1 <= buf_eof and buf[offset_4+0] == 'E':
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_1 = 0
                                        while count_1 < 1:
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                if offset_5 + 1 <= buf_eof and buf[offset_5+0] == '+':
                                                    offset_5 += 1
                                                    column_4 += 1
                                                elif offset_5 + 1 <= buf_eof and buf[offset_5+0] == '-':
                                                    offset_5 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                count_2 = 0
                                                while True:
                                                    offset_6 = offset_5
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    children_6 = [] if children_5 is not None else None
                                                    while True:
                                                        if offset_6 == buf_eof:
                                                            offset_6 = -1
                                                            break

                                                        codepoint = (buf[offset_6])

                                                        if 48 <= codepoint <= 57:
                                                            offset_6 += 1
                                                            column_5 += 1
                                                        else:
                                                            offset_6 = -1
                                                            break

                                                        break
                                                    if offset_6 == -1:
                                                        break
                                                    if offset_5 == offset_6: break
                                                    if children_6 is not None and children_6 is not None:
                                                        children_5.extend(children_6)
                                                    offset_5 = offset_6
                                                    column_4 = column_5
                                                    indent_column_4 = indent_column_5
                                                    partial_tab_offset_4 = partial_tab_offset_5
                                                    partial_tab_width_4 = partial_tab_width_5
                                                    count_2 += 1
                                                if offset_5 == -1:
                                                    break

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_4 = offset_5
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_1 += 1
                                            break
                                        if offset_4 == -1:
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_0 += 1
                                    break
                                if offset_3 == -1:
                                    break


                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_2 = -1 # no more choices
                            break # end choice
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_2 = Node('number', offset_1, offset_2, children_2, None)
                    children_1.append(value_2)
                    offset_1 = offset_2


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
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        if offset_2 + 4 <= buf_eof and buf[offset_2+0] == 't' and buf[offset_2+1] == 'r' and buf[offset_2+2] == 'u' and buf[offset_2+3] == 'e':
                            offset_2 += 4
                            column_1 += 4
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_3 = Node('bool', offset_1, offset_2, children_2, None)
                    children_1.append(value_3)
                    offset_1 = offset_2


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
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        if offset_2 + 5 <= buf_eof and buf[offset_2+0] == 'f' and buf[offset_2+1] == 'a' and buf[offset_2+2] == 'l' and buf[offset_2+3] == 's' and buf[offset_2+4] == 'e':
                            offset_2 += 5
                            column_1 += 5
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_4 = Node('bool', offset_1, offset_2, children_2, None)
                    children_1.append(value_4)
                    offset_1 = offset_2


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
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        if offset_2 + 4 <= buf_eof and buf[offset_2+0] == 'n' and buf[offset_2+1] == 'u' and buf[offset_2+2] == 'l' and buf[offset_2+3] == 'l':
                            offset_2 += 4
                            column_1 += 4
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_5 = Node('null', offset_1, offset_2, children_2, None)
                    children_1.append(value_5)
                    offset_1 = offset_2


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
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    cdef parse_rson_string(self, str buf, int offset_0, int buf_eof, int column_0, tuple indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2, offset_3, offset_4, offset_5
        cdef int column_1, column_2, column_3, column_4

        cdef list children_1, children_2, children_3, children_4, children_5
        cdef int count_1
        cdef tuple indent_column_1, indent_column_2, indent_column_3, indent_column_4
        cdef int partial_tab_offset_1, partial_tab_offset_2, partial_tab_offset_3, partial_tab_offset_4
        cdef int partial_tab_width_1, partial_tab_width_2, partial_tab_width_3, partial_tab_width_4
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '"':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    offset_2 = offset_1
                    children_2 = None
                    while True: # start capture
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                while True: # start choice
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if codepoint <= 31:
                                            offset_4 = -1
                                            break
                                        elif codepoint == 92:
                                            offset_4 = -1
                                            break
                                        elif codepoint == 34:
                                            offset_4 = -1
                                            break
                                        elif 55296 <= codepoint <= 57343:
                                            offset_4 = -1
                                            break
                                        else:
                                            offset_4 += 1
                                            column_3 += 1


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'x':
                                            offset_4 += 2
                                            column_3 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            codepoint = (buf[offset_5])

                                            if 48 <= codepoint <= 49:
                                                offset_5 += 1
                                                column_4 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'u':
                                            offset_4 += 2
                                            column_3 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if offset_5 + 3 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0':
                                                offset_5 += 3
                                                column_4 += 3
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            codepoint = (buf[offset_5])

                                            if 48 <= codepoint <= 49:
                                                offset_5 += 1
                                                column_4 += 1
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
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'D':
                                                offset_5 += 1
                                                column_4 += 1
                                            elif offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'd':
                                                offset_5 += 1
                                                column_4 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            codepoint = (buf[offset_5])

                                            if 56 <= codepoint <= 57:
                                                offset_5 += 1
                                                column_4 += 1
                                            elif 65 <= codepoint <= 70:
                                                offset_5 += 1
                                                column_4 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'U':
                                            offset_4 += 2
                                            column_3 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if offset_5 + 7 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0' and buf[offset_5+3] == '0' and buf[offset_5+4] == '0' and buf[offset_5+5] == '0' and buf[offset_5+6] == '0':
                                                offset_5 += 7
                                                column_4 += 7
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            codepoint = (buf[offset_5])

                                            if 48 <= codepoint <= 49:
                                                offset_5 += 1
                                                column_4 += 1
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
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if offset_5 + 4 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0' and buf[offset_5+3] == '0':
                                                offset_5 += 4
                                                column_4 += 4
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'D':
                                                offset_5 += 1
                                                column_4 += 1
                                            elif offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'd':
                                                offset_5 += 1
                                                column_4 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            codepoint = (buf[offset_5])

                                            if 56 <= codepoint <= 57:
                                                offset_5 += 1
                                                column_4 += 1
                                            elif 65 <= codepoint <= 70:
                                                offset_5 += 1
                                                column_4 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '\\':
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if codepoint == 34:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 92:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 47:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 98:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 110:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 114:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 116:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 39:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_2 = column_3
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
                            column_1 = column_2
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
                    value_0 = Node('string', offset_1, offset_2, children_2, None)
                    children_1.append(value_0)
                    offset_1 = offset_2

                    if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '"':
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
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    if offset_1 + 1 <= buf_eof and buf[offset_1+0] == "'":
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    offset_2 = offset_1
                    children_2 = None
                    while True: # start capture
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                while True: # start choice
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if codepoint <= 31:
                                            offset_4 = -1
                                            break
                                        elif codepoint == 92:
                                            offset_4 = -1
                                            break
                                        elif codepoint == 39:
                                            offset_4 = -1
                                            break
                                        elif 55296 <= codepoint <= 57343:
                                            offset_4 = -1
                                            break
                                        else:
                                            offset_4 += 1
                                            column_3 += 1


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'x':
                                            offset_4 += 2
                                            column_3 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            codepoint = (buf[offset_5])

                                            if 48 <= codepoint <= 49:
                                                offset_5 += 1
                                                column_4 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'u':
                                            offset_4 += 2
                                            column_3 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0':
                                                offset_5 += 2
                                                column_4 += 2
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            codepoint = (buf[offset_5])

                                            if 48 <= codepoint <= 49:
                                                offset_5 += 1
                                                column_4 += 1
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
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'D':
                                                offset_5 += 1
                                                column_4 += 1
                                            elif offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'd':
                                                offset_5 += 1
                                                column_4 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            codepoint = (buf[offset_5])

                                            if 56 <= codepoint <= 57:
                                                offset_5 += 1
                                                column_4 += 1
                                            elif 65 <= codepoint <= 70:
                                                offset_5 += 1
                                                column_4 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'U':
                                            offset_4 += 2
                                            column_3 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5 = offset_4 + 0
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if offset_5 + 6 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0' and buf[offset_5+3] == '0' and buf[offset_5+4] == '0' and buf[offset_5+5] == '0':
                                                offset_5 += 6
                                                column_4 += 6
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            codepoint = (buf[offset_5])

                                            if 48 <= codepoint <= 49:
                                                offset_5 += 1
                                                column_4 += 1
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
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            if offset_5 + 4 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0' and buf[offset_5+3] == '0':
                                                offset_5 += 4
                                                column_4 += 4
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'D':
                                                offset_5 += 1
                                                column_4 += 1
                                            elif offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'd':
                                                offset_5 += 1
                                                column_4 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            codepoint = (buf[offset_5])

                                            if 56 <= codepoint <= 57:
                                                offset_5 += 1
                                                column_4 += 1
                                            elif 65 <= codepoint <= 70:
                                                offset_5 += 1
                                                column_4 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '\\':
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if codepoint == 34:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 92:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 47:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 98:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 102:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 110:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 114:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 116:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 39:
                                            offset_4 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_2 = column_3
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
                            column_1 = column_2
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
                    value_1 = Node('string', offset_1, offset_2, children_2, None)
                    children_1.append(value_1)
                    offset_1 = offset_2

                    if offset_1 + 1 <= buf_eof and buf[offset_1+0] == "'":
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
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    cdef parse_rson_list(self, str buf, int offset_0, int buf_eof, int column_0, tuple indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2, offset_3, offset_4, offset_5
        cdef int column_1, column_2, column_3, column_4

        cdef list children_1, children_2, children_3, children_4, children_5
        cdef int count_1, count_2, count_3, count_4
        cdef tuple indent_column_1, indent_column_2, indent_column_3, indent_column_4
        cdef int partial_tab_offset_1, partial_tab_offset_2, partial_tab_offset_3, partial_tab_offset_4
        cdef int partial_tab_width_1, partial_tab_width_2, partial_tab_width_3, partial_tab_width_4
        while True: # note: return at end of loop
            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '[':
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
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '#':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            if offset_2 == buf_eof:
                                offset_2 = -1
                                break

                            codepoint = (buf[offset_2])

                            if codepoint == 10:
                                offset_2 = -1
                                break
                            else:
                                offset_2 += 1
                                column_2 += 1

                            break
                        if offset_2 == -1:
                            break
                        if offset_1 == offset_2: break
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        offset_1 = offset_2
                        column_1 = column_2
                        indent_column_1 = indent_column_2
                        partial_tab_offset_1 = partial_tab_offset_2
                        partial_tab_width_1 = partial_tab_width_2
                        count_1 += 1
                    if offset_1 == -1:
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
            children_1 = []
            while True: # start capture
                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_value(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                        if offset_2 == -1: break


                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
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
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_2 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '#':
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if codepoint == 10:
                                                    offset_5 = -1
                                                    break
                                                else:
                                                    offset_5 += 1
                                                    column_4 += 1

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_4 = offset_5
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_4 == -1:
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t\r\n\ufeff':
                                                if codepoint == '\t':
                                                    if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                        width = partial_tab_width_3
                                                    else:
                                                        width  = (self.tabstop-(column_3%self.tabstop))
                                                    count_3 += width
                                                    column_3 += width
                                                    offset_4 += 1
                                                else:
                                                    count_3 += 1
                                                    column_3 += 1
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
                                    column_2 = column_3
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
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_2 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break


                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == ',':
                                    offset_3 += 1
                                    column_2 += 1
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
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_2 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '#':
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if codepoint == 10:
                                                    offset_5 = -1
                                                    break
                                                else:
                                                    offset_5 += 1
                                                    column_4 += 1

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_4 = offset_5
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_4 == -1:
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t\r\n\ufeff':
                                                if codepoint == '\t':
                                                    if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                        width = partial_tab_width_3
                                                    else:
                                                        width  = (self.tabstop-(column_3%self.tabstop))
                                                    count_3 += width
                                                    column_3 += width
                                                    offset_4 += 1
                                                else:
                                                    count_3 += 1
                                                    column_3 += 1
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
                                    column_2 = column_3
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
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_2 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break


                                offset_3, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_rson_value(buf, offset_3, buf_eof, column_2, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
                                if offset_3 == -1: break


                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            column_1 = column_2
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
                                        width  = (self.tabstop-(column_1%self.tabstop))
                                    count_1 += width
                                    column_1 += width
                                    offset_2 += 1
                                else:
                                    count_1 += 1
                                    column_1 += 1
                                    offset_2 += 1
                            else:
                                break

                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '#':
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if codepoint == 10:
                                            offset_4 = -1
                                            break
                                        else:
                                            offset_4 += 1
                                            column_3 += 1

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_2 = column_3
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
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_2 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
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
                            column_1 = column_2
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
                                        width  = (self.tabstop-(column_1%self.tabstop))
                                    count_1 += width
                                    column_1 += width
                                    offset_2 += 1
                                else:
                                    count_1 += 1
                                    column_1 += 1
                                    offset_2 += 1
                            else:
                                break


                        count_1 = 0
                        while count_1 < 1:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == ',':
                                    offset_3 += 1
                                    column_2 += 1
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
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_2 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '#':
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if codepoint == 10:
                                                    offset_5 = -1
                                                    break
                                                else:
                                                    offset_5 += 1
                                                    column_4 += 1

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_4 = offset_5
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_4 == -1:
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t\r\n\ufeff':
                                                if codepoint == '\t':
                                                    if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                        width = partial_tab_width_3
                                                    else:
                                                        width  = (self.tabstop-(column_3%self.tabstop))
                                                    count_3 += width
                                                    column_3 += width
                                                    offset_4 += 1
                                                else:
                                                    count_3 += 1
                                                    column_3 += 1
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
                                    column_2 = column_3
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
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_2 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
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
                            column_1 = column_2
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
                    column_0 = column_1
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
            value_0 = Node('list', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == ']':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    cdef parse_rson_object(self, str buf, int offset_0, int buf_eof, int column_0, tuple indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2, offset_3, offset_4, offset_5, offset_6
        cdef int column_1, column_2, column_3, column_4

        cdef list children_1, children_2, children_3, children_4, children_5, children_6
        cdef int count_1, count_2, count_3, count_4
        cdef tuple indent_column_1, indent_column_2, indent_column_3, indent_column_4
        cdef int partial_tab_offset_1, partial_tab_offset_2, partial_tab_offset_3, partial_tab_offset_4
        cdef int partial_tab_width_1, partial_tab_width_2, partial_tab_width_3, partial_tab_width_4
        while True: # note: return at end of loop
            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '{':
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
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '#':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            if offset_2 == buf_eof:
                                offset_2 = -1
                                break

                            codepoint = (buf[offset_2])

                            if codepoint == 10:
                                offset_2 = -1
                                break
                            else:
                                offset_2 += 1
                                column_2 += 1

                            break
                        if offset_2 == -1:
                            break
                        if offset_1 == offset_2: break
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        offset_1 = offset_2
                        column_1 = column_2
                        indent_column_1 = indent_column_2
                        partial_tab_offset_1 = partial_tab_offset_2
                        partial_tab_width_1 = partial_tab_width_2
                        count_1 += 1
                    if offset_1 == -1:
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
            children_1 = []
            while True: # start capture
                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        offset_3 = offset_2
                        children_3 = []
                        while True: # start capture
                            offset_3, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_string(buf, offset_3, buf_eof, column_1, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                            if offset_3 == -1: break


                            count_1 = 0
                            while offset_3 < buf_eof:
                                codepoint = buf[offset_3]
                                if codepoint in ' \t\r\n\ufeff':
                                    if codepoint == '\t':
                                        if offset_3 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-(column_1%self.tabstop))
                                        count_1 += width
                                        column_1 += width
                                        offset_3 += 1
                                    else:
                                        count_1 += 1
                                        column_1 += 1
                                        offset_3 += 1
                                else:
                                    break

                            count_1 = 0
                            while True:
                                offset_4 = offset_3
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_4 = [] if children_3 is not None else None
                                while True:
                                    if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '#':
                                        offset_4 += 1
                                        column_2 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    count_2 = 0
                                    while True:
                                        offset_5 = offset_4
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            codepoint = (buf[offset_5])

                                            if codepoint == 10:
                                                offset_5 = -1
                                                break
                                            else:
                                                offset_5 += 1
                                                column_3 += 1

                                            break
                                        if offset_5 == -1:
                                            break
                                        if offset_4 == offset_5: break
                                        if children_5 is not None and children_5 is not None:
                                            children_4.extend(children_5)
                                        offset_4 = offset_5
                                        column_2 = column_3
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
                                                    width  = (self.tabstop-(column_2%self.tabstop))
                                                count_2 += width
                                                column_2 += width
                                                offset_4 += 1
                                            else:
                                                count_2 += 1
                                                column_2 += 1
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
                                column_1 = column_2
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
                                            width  = (self.tabstop-(column_1%self.tabstop))
                                        count_1 += width
                                        column_1 += width
                                        offset_3 += 1
                                    else:
                                        count_1 += 1
                                        column_1 += 1
                                        offset_3 += 1
                                else:
                                    break


                            if offset_3 + 1 <= buf_eof and buf[offset_3+0] == ':':
                                offset_3 += 1
                                column_1 += 1
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
                                            width  = (self.tabstop-(column_1%self.tabstop))
                                        count_1 += width
                                        column_1 += width
                                        offset_3 += 1
                                    else:
                                        count_1 += 1
                                        column_1 += 1
                                        offset_3 += 1
                                else:
                                    break

                            count_1 = 0
                            while True:
                                offset_4 = offset_3
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_4 = [] if children_3 is not None else None
                                while True:
                                    if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '#':
                                        offset_4 += 1
                                        column_2 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    count_2 = 0
                                    while True:
                                        offset_5 = offset_4
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            codepoint = (buf[offset_5])

                                            if codepoint == 10:
                                                offset_5 = -1
                                                break
                                            else:
                                                offset_5 += 1
                                                column_3 += 1

                                            break
                                        if offset_5 == -1:
                                            break
                                        if offset_4 == offset_5: break
                                        if children_5 is not None and children_5 is not None:
                                            children_4.extend(children_5)
                                        offset_4 = offset_5
                                        column_2 = column_3
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
                                                    width  = (self.tabstop-(column_2%self.tabstop))
                                                count_2 += width
                                                column_2 += width
                                                offset_4 += 1
                                            else:
                                                count_2 += 1
                                                column_2 += 1
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
                                column_1 = column_2
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
                                            width  = (self.tabstop-(column_1%self.tabstop))
                                        count_1 += width
                                        column_1 += width
                                        offset_3 += 1
                                    else:
                                        count_1 += 1
                                        column_1 += 1
                                        offset_3 += 1
                                else:
                                    break


                            offset_3, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_value(buf, offset_3, buf_eof, column_1, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                            if offset_3 == -1: break


                            break
                        if offset_3 == -1:
                            offset_2 = -1
                            break
                        value_0 = Node('pair', offset_2, offset_3, children_3, None)
                        children_2.append(value_0)
                        offset_2 = offset_3

                        count_1 = 0
                        while offset_2 < buf_eof:
                            codepoint = buf[offset_2]
                            if codepoint in ' \t\r\n\ufeff':
                                if codepoint == '\t':
                                    if offset_2 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                        width = partial_tab_width_1
                                    else:
                                        width  = (self.tabstop-(column_1%self.tabstop))
                                    count_1 += width
                                    column_1 += width
                                    offset_2 += 1
                                else:
                                    count_1 += 1
                                    column_1 += 1
                                    offset_2 += 1
                            else:
                                break

                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '#':
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = (buf[offset_4])

                                        if codepoint == 10:
                                            offset_4 = -1
                                            break
                                        else:
                                            offset_4 += 1
                                            column_3 += 1

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    column_2 = column_3
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
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_2 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
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
                            column_1 = column_2
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
                                        width  = (self.tabstop-(column_1%self.tabstop))
                                    count_1 += width
                                    column_1 += width
                                    offset_2 += 1
                                else:
                                    count_1 += 1
                                    column_1 += 1
                                    offset_2 += 1
                            else:
                                break


                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == ',':
                                    offset_3 += 1
                                    column_2 += 1
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
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_2 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '#':
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if codepoint == 10:
                                                    offset_5 = -1
                                                    break
                                                else:
                                                    offset_5 += 1
                                                    column_4 += 1

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_4 = offset_5
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_4 == -1:
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t\r\n\ufeff':
                                                if codepoint == '\t':
                                                    if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                        width = partial_tab_width_3
                                                    else:
                                                        width  = (self.tabstop-(column_3%self.tabstop))
                                                    count_3 += width
                                                    column_3 += width
                                                    offset_4 += 1
                                                else:
                                                    count_3 += 1
                                                    column_3 += 1
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
                                    column_2 = column_3
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
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_2 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break


                                offset_4 = offset_3
                                children_4 = []
                                while True: # start capture
                                    offset_4, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_rson_string(buf, offset_4, buf_eof, column_2, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                    if offset_4 == -1: break


                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        codepoint = buf[offset_4]
                                        if codepoint in ' \t\r\n\ufeff':
                                            if codepoint == '\t':
                                                if offset_4 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                    width = partial_tab_width_2
                                                else:
                                                    width  = (self.tabstop-(column_2%self.tabstop))
                                                count_2 += width
                                                column_2 += width
                                                offset_4 += 1
                                            else:
                                                count_2 += 1
                                                column_2 += 1
                                                offset_4 += 1
                                        else:
                                            break

                                    count_2 = 0
                                    while True:
                                        offset_5 = offset_4
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            if offset_5 + 1 <= buf_eof and buf[offset_5+0] == '#':
                                                offset_5 += 1
                                                column_3 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            count_3 = 0
                                            while True:
                                                offset_6 = offset_5
                                                column_4 = column_3
                                                indent_column_4 = indent_column_3
                                                partial_tab_offset_4 = partial_tab_offset_3
                                                partial_tab_width_4 = partial_tab_width_3
                                                children_6 = [] if children_5 is not None else None
                                                while True:
                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    codepoint = (buf[offset_6])

                                                    if codepoint == 10:
                                                        offset_6 = -1
                                                        break
                                                    else:
                                                        offset_6 += 1
                                                        column_4 += 1

                                                    break
                                                if offset_6 == -1:
                                                    break
                                                if offset_5 == offset_6: break
                                                if children_6 is not None and children_6 is not None:
                                                    children_5.extend(children_6)
                                                offset_5 = offset_6
                                                column_3 = column_4
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                count_3 += 1
                                            if offset_5 == -1:
                                                break

                                            count_3 = 0
                                            while offset_5 < buf_eof:
                                                codepoint = buf[offset_5]
                                                if codepoint in ' \t\r\n\ufeff':
                                                    if codepoint == '\t':
                                                        if offset_5 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                            width = partial_tab_width_3
                                                        else:
                                                            width  = (self.tabstop-(column_3%self.tabstop))
                                                        count_3 += width
                                                        column_3 += width
                                                        offset_5 += 1
                                                    else:
                                                        count_3 += 1
                                                        column_3 += 1
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
                                        column_2 = column_3
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
                                                    width  = (self.tabstop-(column_2%self.tabstop))
                                                count_2 += width
                                                column_2 += width
                                                offset_4 += 1
                                            else:
                                                count_2 += 1
                                                column_2 += 1
                                                offset_4 += 1
                                        else:
                                            break


                                    if offset_4 + 1 <= buf_eof and buf[offset_4+0] == ':':
                                        offset_4 += 1
                                        column_2 += 1
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
                                                    width  = (self.tabstop-(column_2%self.tabstop))
                                                count_2 += width
                                                column_2 += width
                                                offset_4 += 1
                                            else:
                                                count_2 += 1
                                                column_2 += 1
                                                offset_4 += 1
                                        else:
                                            break

                                    count_2 = 0
                                    while True:
                                        offset_5 = offset_4
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            if offset_5 + 1 <= buf_eof and buf[offset_5+0] == '#':
                                                offset_5 += 1
                                                column_3 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            count_3 = 0
                                            while True:
                                                offset_6 = offset_5
                                                column_4 = column_3
                                                indent_column_4 = indent_column_3
                                                partial_tab_offset_4 = partial_tab_offset_3
                                                partial_tab_width_4 = partial_tab_width_3
                                                children_6 = [] if children_5 is not None else None
                                                while True:
                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    codepoint = (buf[offset_6])

                                                    if codepoint == 10:
                                                        offset_6 = -1
                                                        break
                                                    else:
                                                        offset_6 += 1
                                                        column_4 += 1

                                                    break
                                                if offset_6 == -1:
                                                    break
                                                if offset_5 == offset_6: break
                                                if children_6 is not None and children_6 is not None:
                                                    children_5.extend(children_6)
                                                offset_5 = offset_6
                                                column_3 = column_4
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                count_3 += 1
                                            if offset_5 == -1:
                                                break

                                            count_3 = 0
                                            while offset_5 < buf_eof:
                                                codepoint = buf[offset_5]
                                                if codepoint in ' \t\r\n\ufeff':
                                                    if codepoint == '\t':
                                                        if offset_5 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                            width = partial_tab_width_3
                                                        else:
                                                            width  = (self.tabstop-(column_3%self.tabstop))
                                                        count_3 += width
                                                        column_3 += width
                                                        offset_5 += 1
                                                    else:
                                                        count_3 += 1
                                                        column_3 += 1
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
                                        column_2 = column_3
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
                                                    width  = (self.tabstop-(column_2%self.tabstop))
                                                count_2 += width
                                                column_2 += width
                                                offset_4 += 1
                                            else:
                                                count_2 += 1
                                                column_2 += 1
                                                offset_4 += 1
                                        else:
                                            break


                                    offset_4, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_rson_value(buf, offset_4, buf_eof, column_2, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                    if offset_4 == -1: break


                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                value_1 = Node('pair', offset_3, offset_4, children_4, None)
                                children_3.append(value_1)
                                offset_3 = offset_4

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t\r\n\ufeff':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_2 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '#':
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if codepoint == 10:
                                                    offset_5 = -1
                                                    break
                                                else:
                                                    offset_5 += 1
                                                    column_4 += 1

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_4 = offset_5
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_4 == -1:
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t\r\n\ufeff':
                                                if codepoint == '\t':
                                                    if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                        width = partial_tab_width_3
                                                    else:
                                                        width  = (self.tabstop-(column_3%self.tabstop))
                                                    count_3 += width
                                                    column_3 += width
                                                    offset_4 += 1
                                                else:
                                                    count_3 += 1
                                                    column_3 += 1
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
                                    column_2 = column_3
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
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_2 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
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
                            column_1 = column_2
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            count_1 += 1
                        if offset_2 == -1:
                            break

                        count_1 = 0
                        while count_1 < 1:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == ',':
                                    offset_3 += 1
                                    column_2 += 1
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
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_2 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '#':
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_5 = offset_4
                                            column_4 = column_3
                                            indent_column_4 = indent_column_3
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = (buf[offset_5])

                                                if codepoint == 10:
                                                    offset_5 = -1
                                                    break
                                                else:
                                                    offset_5 += 1
                                                    column_4 += 1

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_4 = offset_5
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_4 == -1:
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t\r\n\ufeff':
                                                if codepoint == '\t':
                                                    if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                        width = partial_tab_width_3
                                                    else:
                                                        width  = (self.tabstop-(column_3%self.tabstop))
                                                    count_3 += width
                                                    column_3 += width
                                                    offset_4 += 1
                                                else:
                                                    count_3 += 1
                                                    column_3 += 1
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
                                    column_2 = column_3
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
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_2 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
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
                            column_1 = column_2
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
                    column_0 = column_1
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
            value_2 = Node('object', offset_0, offset_1, children_1, None)
            children_0.append(value_2)
            offset_0 = offset_1

            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '}':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0
