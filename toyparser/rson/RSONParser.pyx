#cython: language_level=3, bounds_check=False
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
        start, eof = offset, end
        column, indent_column = 0, [0]
        prefix, children = [], []
        new_offset, column, partial_tab_offset, partial_tab_width = self.parse_document(buf, start, end, offset, column, indent_column, prefix, children, 0, 0)
        if new_offset == end:
             if builder is None: return Node('document', offset, new_offset, 0, column, children, None)
             return children[-1].build(buf, builder)
        # print('no', children, offset, new_offset, end)
        if err is not None: raise err(buf, new_offset, 'no')

    cdef (int, int, int, int) parse_document(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2
        cdef int column_1, column_2

        cdef list children_1, children_2
        cdef int count_1, count_2
        cdef list indent_column_1, indent_column_2
        cdef int partial_tab_offset_1, partial_tab_offset_2
        cdef int partial_tab_width_1, partial_tab_width_2
        while True: # note: return at end of loop
            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    #print('entry rep rule', offset_0, offset_1)
                    if offset_1 == buf_eof:
                        offset_1 = -1
                        break

                    codepoint = (buf[offset_1])

                    if codepoint == 32:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 9:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 13:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 10:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 65279:
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    #print('safe exit rep rule', offset_0, offset_1)
                    break
                #print('exit rep rule', offset_0, offset_1)
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
            value_0 = count_0

            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    #print('entry rep rule', offset_0, offset_1)
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
                        indent_column_2 = list(indent_column_1)
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            #print('entry rep rule', offset_1, offset_2)
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

                            #print('safe exit rep rule', offset_1, offset_2)
                            break
                        #print('exit rep rule', offset_1, offset_2)
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
                    value_2 = count_1

                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = list(indent_column_1)
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            #print('entry rep rule', offset_1, offset_2)
                            if offset_2 == buf_eof:
                                offset_2 = -1
                                break

                            codepoint = (buf[offset_2])

                            if codepoint == 32:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 9:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 13:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 10:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 65279:
                                offset_2 += 1
                                column_2 += 1
                            else:
                                offset_2 = -1
                                break

                            #print('safe exit rep rule', offset_1, offset_2)
                            break
                        #print('exit rep rule', offset_1, offset_2)
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
                    value_3 = count_1

                    #print('safe exit rep rule', offset_0, offset_1)
                    break
                #print('exit rep rule', offset_0, offset_1)
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
            value_1 = count_0

            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    #print('entry rep rule', offset_0, offset_1)
                    if offset_1 == buf_eof:
                        offset_1 = -1
                        break

                    codepoint = (buf[offset_1])

                    if codepoint == 32:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 9:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 13:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 10:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 65279:
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    #print('safe exit rep rule', offset_0, offset_1)
                    break
                #print('exit rep rule', offset_0, offset_1)
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
            value_4 = count_0



            offset_0, column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_rson_value(buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0)
            if offset_0 == -1: break


            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    #print('entry rep rule', offset_0, offset_1)
                    if offset_1 == buf_eof:
                        offset_1 = -1
                        break

                    codepoint = (buf[offset_1])

                    if codepoint == 32:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 9:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 13:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 10:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 65279:
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    #print('safe exit rep rule', offset_0, offset_1)
                    break
                #print('exit rep rule', offset_0, offset_1)
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
            value_5 = count_0

            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    #print('entry rep rule', offset_0, offset_1)
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
                        indent_column_2 = list(indent_column_1)
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            #print('entry rep rule', offset_1, offset_2)
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

                            #print('safe exit rep rule', offset_1, offset_2)
                            break
                        #print('exit rep rule', offset_1, offset_2)
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
                    value_7 = count_1

                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = list(indent_column_1)
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            #print('entry rep rule', offset_1, offset_2)
                            if offset_2 == buf_eof:
                                offset_2 = -1
                                break

                            codepoint = (buf[offset_2])

                            if codepoint == 32:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 9:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 13:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 10:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 65279:
                                offset_2 += 1
                                column_2 += 1
                            else:
                                offset_2 = -1
                                break

                            #print('safe exit rep rule', offset_1, offset_2)
                            break
                        #print('exit rep rule', offset_1, offset_2)
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
                    value_8 = count_1

                    #print('safe exit rep rule', offset_0, offset_1)
                    break
                #print('exit rep rule', offset_0, offset_1)
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
            value_6 = count_0

            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    #print('entry rep rule', offset_0, offset_1)
                    if offset_1 == buf_eof:
                        offset_1 = -1
                        break

                    codepoint = (buf[offset_1])

                    if codepoint == 32:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 9:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 13:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 10:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 65279:
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    #print('safe exit rep rule', offset_0, offset_1)
                    break
                #print('exit rep rule', offset_0, offset_1)
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
            value_9 = count_0




            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    cdef (int, int, int, int) parse_rson_value(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2
        cdef int column_1, column_2

        cdef list children_1, children_2, children_3, children_4
        cdef int count_1
        cdef list indent_column_1, indent_column_2
        cdef int partial_tab_offset_1, partial_tab_offset_2
        cdef int partial_tab_width_1, partial_tab_width_2
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
                        if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '@':
                            offset_1 += 1
                            column_1 += 1
                        else:
                            offset_1 = -1
                            break

                        children_3 = None
                        value_1 = Node(None, offset_1, offset_1, column_1, column_1, children_3, None)
                        while True: # start capture
                            if offset_1 == buf_eof:
                                offset_1 = -1
                                break

                            codepoint = (buf[offset_1])

                            if 97 <= codepoint <= 122:
                                offset_1 += 1
                                column_1 += 1
                            elif 65 <= codepoint <= 90:
                                offset_1 += 1
                                column_1 += 1
                            else:
                                offset_1 = -1
                                break


                            count_0 = 0
                            while True:
                                offset_2 = offset_1
                                column_2 = column_1
                                indent_column_2 = list(indent_column_1)
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_4 = [] if children_3 is not None else None
                                while True:
                                    #print('entry rep rule', offset_1, offset_2)
                                    if offset_2 == buf_eof:
                                        offset_2 = -1
                                        break

                                    codepoint = (buf[offset_2])

                                    if 48 <= codepoint <= 57:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif 97 <= codepoint <= 122:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif 65 <= codepoint <= 90:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 95:
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    #print('safe exit rep rule', offset_1, offset_2)
                                    break
                                #print('exit rep rule', offset_1, offset_2)
                                if offset_2 == -1:
                                    break
                                if offset_1 == offset_2: break
                                if children_4 is not None and children_4 is not None:
                                    children_3.extend(children_4)
                                offset_1 = offset_2
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                count_0 += 1
                            if offset_1 == -1:
                                break
                            value_2 = count_0


                            break
                        if offset_1 == -1:
                            break
                        value_1.name = 'identifier'
                        value_1.end = offset_1
                        value_1.end_column = column_1
                        value_1.value = None
                        children_2.append(value_1)

                        if offset_1 + 1 <= buf_eof and buf[offset_1+0] == ' ':
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

    cdef (int, int, int, int) parse_rson_literal(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2, offset_3, offset_4, offset_5
        cdef int column_1, column_2, column_3, column_4, column_5

        cdef list children_1, children_2, children_3, children_4, children_5, children_6
        cdef int count_1, count_2, count_3
        cdef list indent_column_1, indent_column_2, indent_column_3, indent_column_4, indent_column_5
        cdef int partial_tab_offset_1, partial_tab_offset_2, partial_tab_offset_3, partial_tab_offset_4, partial_tab_offset_5
        cdef int partial_tab_width_1, partial_tab_width_2, partial_tab_width_3, partial_tab_width_4, partial_tab_width_5
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
                            if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '"':
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
                                                    column_4 += 1



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
                                                if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'x':
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
                                                    if offset_5 == buf_eof:
                                                        offset_5 = -1
                                                        break

                                                    codepoint = (buf[offset_5])

                                                    if 48 <= codepoint <= 49:
                                                        offset_5 += 1
                                                        column_5 += 1
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
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
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
                                                if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'u':
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
                                                    if offset_5 + 3 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0':
                                                        offset_5 += 3
                                                        column_5 += 3
                                                    else:
                                                        offset_5 = -1
                                                        break

                                                    if offset_5 == buf_eof:
                                                        offset_5 = -1
                                                        break

                                                    codepoint = (buf[offset_5])

                                                    if 48 <= codepoint <= 49:
                                                        offset_5 += 1
                                                        column_5 += 1
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
                                                    if offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'D':
                                                        offset_5 += 1
                                                        column_5 += 1
                                                    elif offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'd':
                                                        offset_5 += 1
                                                        column_5 += 1
                                                    else:
                                                        offset_5 = -1
                                                        break


                                                    if offset_5 == buf_eof:
                                                        offset_5 = -1
                                                        break

                                                    codepoint = (buf[offset_5])

                                                    if 56 <= codepoint <= 57:
                                                        offset_5 += 1
                                                        column_5 += 1
                                                    elif 65 <= codepoint <= 70:
                                                        offset_5 += 1
                                                        column_5 += 1
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
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
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
                                                if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'U':
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
                                                    if offset_5 + 7 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0' and buf[offset_5+3] == '0' and buf[offset_5+4] == '0' and buf[offset_5+5] == '0' and buf[offset_5+6] == '0':
                                                        offset_5 += 7
                                                        column_5 += 7
                                                    else:
                                                        offset_5 = -1
                                                        break

                                                    if offset_5 == buf_eof:
                                                        offset_5 = -1
                                                        break

                                                    codepoint = (buf[offset_5])

                                                    if 48 <= codepoint <= 49:
                                                        offset_5 += 1
                                                        column_5 += 1
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
                                                    if offset_5 + 4 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0' and buf[offset_5+3] == '0':
                                                        offset_5 += 4
                                                        column_5 += 4
                                                    else:
                                                        offset_5 = -1
                                                        break

                                                    if offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'D':
                                                        offset_5 += 1
                                                        column_5 += 1
                                                    elif offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'd':
                                                        offset_5 += 1
                                                        column_5 += 1
                                                    else:
                                                        offset_5 = -1
                                                        break


                                                    if offset_5 == buf_eof:
                                                        offset_5 = -1
                                                        break

                                                    codepoint = (buf[offset_5])

                                                    if 56 <= codepoint <= 57:
                                                        offset_5 += 1
                                                        column_5 += 1
                                                    elif 65 <= codepoint <= 70:
                                                        offset_5 += 1
                                                        column_5 += 1
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
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
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
                                                if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '\\':
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break

                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if codepoint == 34:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 92:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 47:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 98:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 110:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 114:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 116:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 39:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 10:
                                                    offset_4 += 1
                                                    column_4 += 1
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
                        indent_column_2 = list(indent_column_1)
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
                                                    column_4 += 1



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
                                                if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'x':
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
                                                    if offset_5 == buf_eof:
                                                        offset_5 = -1
                                                        break

                                                    codepoint = (buf[offset_5])

                                                    if 48 <= codepoint <= 49:
                                                        offset_5 += 1
                                                        column_5 += 1
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
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
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
                                                if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'u':
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
                                                    if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0':
                                                        offset_5 += 2
                                                        column_5 += 2
                                                    else:
                                                        offset_5 = -1
                                                        break

                                                    if offset_5 == buf_eof:
                                                        offset_5 = -1
                                                        break

                                                    codepoint = (buf[offset_5])

                                                    if 48 <= codepoint <= 49:
                                                        offset_5 += 1
                                                        column_5 += 1
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
                                                    if offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'D':
                                                        offset_5 += 1
                                                        column_5 += 1
                                                    elif offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'd':
                                                        offset_5 += 1
                                                        column_5 += 1
                                                    else:
                                                        offset_5 = -1
                                                        break


                                                    if offset_5 == buf_eof:
                                                        offset_5 = -1
                                                        break

                                                    codepoint = (buf[offset_5])

                                                    if 56 <= codepoint <= 57:
                                                        offset_5 += 1
                                                        column_5 += 1
                                                    elif 65 <= codepoint <= 70:
                                                        offset_5 += 1
                                                        column_5 += 1
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
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
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
                                                if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'U':
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
                                                    if offset_5 + 6 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0' and buf[offset_5+3] == '0' and buf[offset_5+4] == '0' and buf[offset_5+5] == '0':
                                                        offset_5 += 6
                                                        column_5 += 6
                                                    else:
                                                        offset_5 = -1
                                                        break

                                                    if offset_5 == buf_eof:
                                                        offset_5 = -1
                                                        break

                                                    codepoint = (buf[offset_5])

                                                    if 48 <= codepoint <= 49:
                                                        offset_5 += 1
                                                        column_5 += 1
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
                                                    if offset_5 + 4 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0' and buf[offset_5+3] == '0':
                                                        offset_5 += 4
                                                        column_5 += 4
                                                    else:
                                                        offset_5 = -1
                                                        break

                                                    if offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'D':
                                                        offset_5 += 1
                                                        column_5 += 1
                                                    elif offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'd':
                                                        offset_5 += 1
                                                        column_5 += 1
                                                    else:
                                                        offset_5 = -1
                                                        break


                                                    if offset_5 == buf_eof:
                                                        offset_5 = -1
                                                        break

                                                    codepoint = (buf[offset_5])

                                                    if 56 <= codepoint <= 57:
                                                        offset_5 += 1
                                                        column_5 += 1
                                                    elif 65 <= codepoint <= 70:
                                                        offset_5 += 1
                                                        column_5 += 1
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
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break


                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_4 += 1
                                                    column_4 += 1
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
                                                if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '\\':
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break

                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if codepoint == 34:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 92:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 47:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 98:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 102:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 110:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 114:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 116:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 39:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 10:
                                                    offset_4 += 1
                                                    column_4 += 1
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
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    children_2 = None
                    value_4 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        while True: # start choice
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                count_0 = 0
                                while count_0 < 1:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 45:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 43:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    break
                                if offset_2 == -1:
                                    break
                                value_5 = count_0

                                if offset_2 + 2 <= buf_eof and buf[offset_2+0] == '0' and buf[offset_2+1] == 'x':
                                    offset_2 += 2
                                    column_2 += 2
                                else:
                                    offset_2 = -1
                                    break

                                if offset_2 == buf_eof:
                                    offset_2 = -1
                                    break

                                codepoint = (buf[offset_2])

                                if 48 <= codepoint <= 57:
                                    offset_2 += 1
                                    column_2 += 1
                                elif 65 <= codepoint <= 70:
                                    offset_2 += 1
                                    column_2 += 1
                                elif 97 <= codepoint <= 102:
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

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
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if 48 <= codepoint <= 57:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 95:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                value_6 = count_0


                                break
                            if offset_2 != -1:
                                offset_1 = offset_2
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                count_0 = 0
                                while count_0 < 1:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 45:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 43:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    break
                                if offset_2 == -1:
                                    break
                                value_7 = count_0

                                if offset_2 + 2 <= buf_eof and buf[offset_2+0] == '0' and buf[offset_2+1] == 'o':
                                    offset_2 += 2
                                    column_2 += 2
                                else:
                                    offset_2 = -1
                                    break

                                if offset_2 == buf_eof:
                                    offset_2 = -1
                                    break

                                codepoint = (buf[offset_2])

                                if 48 <= codepoint <= 56:
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

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
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if 48 <= codepoint <= 56:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 95:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                value_8 = count_0


                                break
                            if offset_2 != -1:
                                offset_1 = offset_2
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                count_0 = 0
                                while count_0 < 1:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 45:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 43:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    break
                                if offset_2 == -1:
                                    break
                                value_9 = count_0

                                if offset_2 + 2 <= buf_eof and buf[offset_2+0] == '0' and buf[offset_2+1] == 'b':
                                    offset_2 += 2
                                    column_2 += 2
                                else:
                                    offset_2 = -1
                                    break

                                if offset_2 == buf_eof:
                                    offset_2 = -1
                                    break

                                codepoint = (buf[offset_2])

                                if 48 <= codepoint <= 49:
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

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
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if 48 <= codepoint <= 49:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 95:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                value_10 = count_0


                                break
                            if offset_2 != -1:
                                offset_1 = offset_2
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                count_0 = 0
                                while count_0 < 1:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 45:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 43:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    break
                                if offset_2 == -1:
                                    break
                                value_11 = count_0

                                while True: # start choice
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '0':
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
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if 49 <= codepoint <= 57:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
                                            break

                                        count_0 = 0
                                        while True:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_0 += 1
                                        if offset_3 == -1:
                                            break
                                        value_12 = count_0


                                        break
                                    if offset_3 != -1:
                                        offset_2 = offset_3
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_2 = -1 # no more choices
                                    break # end choice
                                if offset_2 == -1:
                                    break

                                count_0 = 0
                                while count_0 < 1:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '.':
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
                                            break

                                        count_1 = 0
                                        while True:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if 48 <= codepoint <= 57:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_1 += 1
                                        if offset_3 == -1:
                                            break
                                        value_14 = count_1

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
                                    break
                                if offset_2 == -1:
                                    break
                                value_13 = count_0

                                count_0 = 0
                                while count_0 < 1:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 + 1 <= buf_eof and buf[offset_3+0] == 'e':
                                            offset_3 += 1
                                            column_3 += 1
                                        elif offset_3 + 1 <= buf_eof and buf[offset_3+0] == 'E':
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
                                            break

                                        count_1 = 0
                                        while count_1 < 1:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '+':
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif offset_4 + 1 <= buf_eof and buf[offset_4+0] == '-':
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break

                                                count_2 = 0
                                                while True:
                                                    offset_5 = offset_4
                                                    column_5 = column_4
                                                    indent_column_5 = list(indent_column_4)
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    children_6 = [] if children_5 is not None else None
                                                    while True:
                                                        #print('entry rep rule', offset_4, offset_5)
                                                        if offset_5 == buf_eof:
                                                            offset_5 = -1
                                                            break

                                                        codepoint = (buf[offset_5])

                                                        if 48 <= codepoint <= 57:
                                                            offset_5 += 1
                                                            column_5 += 1
                                                        else:
                                                            offset_5 = -1
                                                            break

                                                        #print('safe exit rep rule', offset_4, offset_5)
                                                        break
                                                    #print('exit rep rule', offset_4, offset_5)
                                                    if offset_5 == -1:
                                                        break
                                                    if offset_4 == offset_5: break
                                                    if children_6 is not None and children_6 is not None:
                                                        children_5.extend(children_6)
                                                    offset_4 = offset_5
                                                    column_4 = column_5
                                                    indent_column_4 = indent_column_5
                                                    partial_tab_offset_4 = partial_tab_offset_5
                                                    partial_tab_width_4 = partial_tab_width_5
                                                    count_2 += 1
                                                if offset_4 == -1:
                                                    break
                                                value_17 = count_2

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_1 += 1
                                            break
                                        if offset_3 == -1:
                                            break
                                        value_16 = count_1

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
                                    break
                                if offset_2 == -1:
                                    break
                                value_15 = count_0


                                break
                            if offset_2 != -1:
                                offset_1 = offset_2
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_1 = -1 # no more choices
                            break # end choice
                        if offset_1 == -1:
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
                    value_18 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        if offset_1 + 4 <= buf_eof and buf[offset_1+0] == 't' and buf[offset_1+1] == 'r' and buf[offset_1+2] == 'u' and buf[offset_1+3] == 'e':
                            offset_1 += 4
                            column_1 += 4
                        else:
                            offset_1 = -1
                            break

                        break
                    if offset_1 == -1:
                        break
                    value_18.name = 'bool'
                    value_18.end = offset_1
                    value_18.end_column = column_1
                    value_18.value = None
                    children_1.append(value_18)


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
                    value_19 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        if offset_1 + 5 <= buf_eof and buf[offset_1+0] == 'f' and buf[offset_1+1] == 'a' and buf[offset_1+2] == 'l' and buf[offset_1+3] == 's' and buf[offset_1+4] == 'e':
                            offset_1 += 5
                            column_1 += 5
                        else:
                            offset_1 = -1
                            break

                        break
                    if offset_1 == -1:
                        break
                    value_19.name = 'bool'
                    value_19.end = offset_1
                    value_19.end_column = column_1
                    value_19.value = None
                    children_1.append(value_19)


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
                    value_20 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        if offset_1 + 4 <= buf_eof and buf[offset_1+0] == 'n' and buf[offset_1+1] == 'u' and buf[offset_1+2] == 'l' and buf[offset_1+3] == 'l':
                            offset_1 += 4
                            column_1 += 4
                        else:
                            offset_1 = -1
                            break

                        break
                    if offset_1 == -1:
                        break
                    value_20.name = 'null'
                    value_20.end = offset_1
                    value_20.end_column = column_1
                    value_20.value = None
                    children_1.append(value_20)


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

    cdef (int, int, int, int) parse_rson_list(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2, offset_3, offset_4
        cdef int column_1, column_2, column_3, column_4

        cdef list children_1, children_2, children_3, children_4, children_5
        cdef int count_1, count_2, count_3, count_4
        cdef list indent_column_1, indent_column_2, indent_column_3, indent_column_4
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
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    #print('entry rep rule', offset_0, offset_1)
                    if offset_1 == buf_eof:
                        offset_1 = -1
                        break

                    codepoint = (buf[offset_1])

                    if codepoint == 32:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 9:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 13:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 10:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 65279:
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    #print('safe exit rep rule', offset_0, offset_1)
                    break
                #print('exit rep rule', offset_0, offset_1)
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
            value_0 = count_0

            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    #print('entry rep rule', offset_0, offset_1)
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
                        indent_column_2 = list(indent_column_1)
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            #print('entry rep rule', offset_1, offset_2)
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

                            #print('safe exit rep rule', offset_1, offset_2)
                            break
                        #print('exit rep rule', offset_1, offset_2)
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
                    value_2 = count_1

                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = list(indent_column_1)
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            #print('entry rep rule', offset_1, offset_2)
                            if offset_2 == buf_eof:
                                offset_2 = -1
                                break

                            codepoint = (buf[offset_2])

                            if codepoint == 32:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 9:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 13:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 10:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 65279:
                                offset_2 += 1
                                column_2 += 1
                            else:
                                offset_2 = -1
                                break

                            #print('safe exit rep rule', offset_1, offset_2)
                            break
                        #print('exit rep rule', offset_1, offset_2)
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
                    value_3 = count_1

                    #print('safe exit rep rule', offset_0, offset_1)
                    break
                #print('exit rep rule', offset_0, offset_1)
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
            value_1 = count_0

            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    #print('entry rep rule', offset_0, offset_1)
                    if offset_1 == buf_eof:
                        offset_1 = -1
                        break

                    codepoint = (buf[offset_1])

                    if codepoint == 32:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 9:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 13:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 10:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 65279:
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    #print('safe exit rep rule', offset_0, offset_1)
                    break
                #print('exit rep rule', offset_0, offset_1)
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
            value_4 = count_0



            children_1 = []
            value_5 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
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
                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 32:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 9:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 13:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 65279:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_8 = count_2

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '#':
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if codepoint == 10:
                                                    offset_4 = -1
                                                    break
                                                else:
                                                    offset_4 += 1
                                                    column_4 += 1

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_3 == -1:
                                            break
                                        value_10 = count_3

                                        count_3 = 0
                                        while True:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if codepoint == 32:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 9:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 13:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 10:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 65279:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_3 == -1:
                                            break
                                        value_11 = count_3

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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_9 = count_2

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 32:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 9:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 13:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 65279:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_12 = count_2



                                if offset_2 + 1 <= buf_eof and buf[offset_2+0] == ',':
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 32:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 9:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 13:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 65279:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_13 = count_2

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '#':
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if codepoint == 10:
                                                    offset_4 = -1
                                                    break
                                                else:
                                                    offset_4 += 1
                                                    column_4 += 1

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_3 == -1:
                                            break
                                        value_15 = count_3

                                        count_3 = 0
                                        while True:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if codepoint == 32:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 9:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 13:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 10:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 65279:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_3 == -1:
                                            break
                                        value_16 = count_3

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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_14 = count_2

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 32:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 9:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 13:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 65279:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_17 = count_2



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
                        value_7 = count_1

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
                                if offset_2 == buf_eof:
                                    offset_2 = -1
                                    break

                                codepoint = (buf[offset_2])

                                if codepoint == 32:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 9:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 13:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 10:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 65279:
                                    offset_2 += 1
                                    column_2 += 1
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
                        value_18 = count_1

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
                                if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '#':
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 10:
                                            offset_3 = -1
                                            break
                                        else:
                                            offset_3 += 1
                                            column_3 += 1

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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_20 = count_2

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 32:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 9:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 13:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 65279:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_21 = count_2

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
                        value_19 = count_1

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
                                if offset_2 == buf_eof:
                                    offset_2 = -1
                                    break

                                codepoint = (buf[offset_2])

                                if codepoint == 32:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 9:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 13:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 10:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 65279:
                                    offset_2 += 1
                                    column_2 += 1
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
                        value_22 = count_1



                        count_1 = 0
                        while count_1 < 1:
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                #print('entry rep rule', offset_1, offset_2)
                                if offset_2 + 1 <= buf_eof and buf[offset_2+0] == ',':
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 32:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 9:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 13:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 65279:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_24 = count_2

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '#':
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if codepoint == 10:
                                                    offset_4 = -1
                                                    break
                                                else:
                                                    offset_4 += 1
                                                    column_4 += 1

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_3 == -1:
                                            break
                                        value_26 = count_3

                                        count_3 = 0
                                        while True:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if codepoint == 32:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 9:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 13:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 10:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 65279:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_3 == -1:
                                            break
                                        value_27 = count_3

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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_25 = count_2

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 32:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 9:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 13:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 65279:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_28 = count_2


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
                            break
                        if offset_1 == -1:
                            break
                        value_23 = count_1


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
                value_6 = count_0

                break
            if offset_0 == -1:
                break
            value_5.name = 'list'
            value_5.end = offset_0
            value_5.end_column = column_0
            value_5.value = None
            children_0.append(value_5)

            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == ']':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    cdef (int, int, int, int) parse_rson_object(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2, offset_3, offset_4, offset_5, offset_6
        cdef int column_1, column_2, column_3, column_4, column_5, column_6

        cdef list children_1, children_2, children_3, children_4, children_5, children_6, children_7, children_8, children_9
        cdef int count_1, count_2, count_3, count_4
        cdef list indent_column_1, indent_column_2, indent_column_3, indent_column_4, indent_column_5, indent_column_6
        cdef int partial_tab_offset_1, partial_tab_offset_2, partial_tab_offset_3, partial_tab_offset_4, partial_tab_offset_5, partial_tab_offset_6
        cdef int partial_tab_width_1, partial_tab_width_2, partial_tab_width_3, partial_tab_width_4, partial_tab_width_5, partial_tab_width_6
        while True: # note: return at end of loop
            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '{':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
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
                    #print('entry rep rule', offset_0, offset_1)
                    if offset_1 == buf_eof:
                        offset_1 = -1
                        break

                    codepoint = (buf[offset_1])

                    if codepoint == 32:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 9:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 13:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 10:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 65279:
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    #print('safe exit rep rule', offset_0, offset_1)
                    break
                #print('exit rep rule', offset_0, offset_1)
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
            value_0 = count_0

            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    #print('entry rep rule', offset_0, offset_1)
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
                        indent_column_2 = list(indent_column_1)
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            #print('entry rep rule', offset_1, offset_2)
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

                            #print('safe exit rep rule', offset_1, offset_2)
                            break
                        #print('exit rep rule', offset_1, offset_2)
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
                    value_2 = count_1

                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = list(indent_column_1)
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            #print('entry rep rule', offset_1, offset_2)
                            if offset_2 == buf_eof:
                                offset_2 = -1
                                break

                            codepoint = (buf[offset_2])

                            if codepoint == 32:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 9:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 13:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 10:
                                offset_2 += 1
                                column_2 += 1
                            elif codepoint == 65279:
                                offset_2 += 1
                                column_2 += 1
                            else:
                                offset_2 = -1
                                break

                            #print('safe exit rep rule', offset_1, offset_2)
                            break
                        #print('exit rep rule', offset_1, offset_2)
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
                    value_3 = count_1

                    #print('safe exit rep rule', offset_0, offset_1)
                    break
                #print('exit rep rule', offset_0, offset_1)
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
            value_1 = count_0

            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    #print('entry rep rule', offset_0, offset_1)
                    if offset_1 == buf_eof:
                        offset_1 = -1
                        break

                    codepoint = (buf[offset_1])

                    if codepoint == 32:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 9:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 13:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 10:
                        offset_1 += 1
                        column_1 += 1
                    elif codepoint == 65279:
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    #print('safe exit rep rule', offset_0, offset_1)
                    break
                #print('exit rep rule', offset_0, offset_1)
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
            value_4 = count_0



            children_1 = []
            value_5 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
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
                        value_7 = Node(None, offset_1, offset_1, column_1, column_1, children_3, None)
                        while True: # start capture
                            while True: # start choice
                                offset_2 = offset_1
                                column_2 = column_1
                                indent_column_2 = list(indent_column_1)
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_4 = [] if children_3 is not None else None
                                while True: # case
                                    if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '"':
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    children_5 = None
                                    value_8 = Node(None, offset_2, offset_2, column_2, column_2, children_5, None)
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
                                                            column_4 += 1



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
                                                        if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'x':
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
                                                            if offset_5 == buf_eof:
                                                                offset_5 = -1
                                                                break

                                                            codepoint = (buf[offset_5])

                                                            if 48 <= codepoint <= 49:
                                                                offset_5 += 1
                                                                column_5 += 1
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
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
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
                                                        if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'u':
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
                                                            if offset_5 + 3 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0':
                                                                offset_5 += 3
                                                                column_5 += 3
                                                            else:
                                                                offset_5 = -1
                                                                break

                                                            if offset_5 == buf_eof:
                                                                offset_5 = -1
                                                                break

                                                            codepoint = (buf[offset_5])

                                                            if 48 <= codepoint <= 49:
                                                                offset_5 += 1
                                                                column_5 += 1
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
                                                            if offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'D':
                                                                offset_5 += 1
                                                                column_5 += 1
                                                            elif offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'd':
                                                                offset_5 += 1
                                                                column_5 += 1
                                                            else:
                                                                offset_5 = -1
                                                                break


                                                            if offset_5 == buf_eof:
                                                                offset_5 = -1
                                                                break

                                                            codepoint = (buf[offset_5])

                                                            if 56 <= codepoint <= 57:
                                                                offset_5 += 1
                                                                column_5 += 1
                                                            elif 65 <= codepoint <= 70:
                                                                offset_5 += 1
                                                                column_5 += 1
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
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
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
                                                        if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'U':
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
                                                            if offset_5 + 7 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0' and buf[offset_5+3] == '0' and buf[offset_5+4] == '0' and buf[offset_5+5] == '0' and buf[offset_5+6] == '0':
                                                                offset_5 += 7
                                                                column_5 += 7
                                                            else:
                                                                offset_5 = -1
                                                                break

                                                            if offset_5 == buf_eof:
                                                                offset_5 = -1
                                                                break

                                                            codepoint = (buf[offset_5])

                                                            if 48 <= codepoint <= 49:
                                                                offset_5 += 1
                                                                column_5 += 1
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
                                                            if offset_5 + 4 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0' and buf[offset_5+3] == '0':
                                                                offset_5 += 4
                                                                column_5 += 4
                                                            else:
                                                                offset_5 = -1
                                                                break

                                                            if offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'D':
                                                                offset_5 += 1
                                                                column_5 += 1
                                                            elif offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'd':
                                                                offset_5 += 1
                                                                column_5 += 1
                                                            else:
                                                                offset_5 = -1
                                                                break


                                                            if offset_5 == buf_eof:
                                                                offset_5 = -1
                                                                break

                                                            codepoint = (buf[offset_5])

                                                            if 56 <= codepoint <= 57:
                                                                offset_5 += 1
                                                                column_5 += 1
                                                            elif 65 <= codepoint <= 70:
                                                                offset_5 += 1
                                                                column_5 += 1
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
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
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
                                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '\\':
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break

                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if codepoint == 34:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 92:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 47:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 98:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 110:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 114:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 116:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 39:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 10:
                                                            offset_4 += 1
                                                            column_4 += 1
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
                                        value_9 = count_1

                                        break
                                    if offset_2 == -1:
                                        break
                                    value_8.name = 'string'
                                    value_8.end = offset_2
                                    value_8.end_column = column_2
                                    value_8.value = None
                                    children_4.append(value_8)

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
                                    if offset_2 + 1 <= buf_eof and buf[offset_2+0] == "'":
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    children_5 = None
                                    value_10 = Node(None, offset_2, offset_2, column_2, column_2, children_5, None)
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
                                                            column_4 += 1



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
                                                        if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'x':
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
                                                            if offset_5 == buf_eof:
                                                                offset_5 = -1
                                                                break

                                                            codepoint = (buf[offset_5])

                                                            if 48 <= codepoint <= 49:
                                                                offset_5 += 1
                                                                column_5 += 1
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
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
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
                                                        if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'u':
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
                                                            if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0':
                                                                offset_5 += 2
                                                                column_5 += 2
                                                            else:
                                                                offset_5 = -1
                                                                break

                                                            if offset_5 == buf_eof:
                                                                offset_5 = -1
                                                                break

                                                            codepoint = (buf[offset_5])

                                                            if 48 <= codepoint <= 49:
                                                                offset_5 += 1
                                                                column_5 += 1
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
                                                            if offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'D':
                                                                offset_5 += 1
                                                                column_5 += 1
                                                            elif offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'd':
                                                                offset_5 += 1
                                                                column_5 += 1
                                                            else:
                                                                offset_5 = -1
                                                                break


                                                            if offset_5 == buf_eof:
                                                                offset_5 = -1
                                                                break

                                                            codepoint = (buf[offset_5])

                                                            if 56 <= codepoint <= 57:
                                                                offset_5 += 1
                                                                column_5 += 1
                                                            elif 65 <= codepoint <= 70:
                                                                offset_5 += 1
                                                                column_5 += 1
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
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
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
                                                        if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'U':
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
                                                            if offset_5 + 6 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0' and buf[offset_5+3] == '0' and buf[offset_5+4] == '0' and buf[offset_5+5] == '0':
                                                                offset_5 += 6
                                                                column_5 += 6
                                                            else:
                                                                offset_5 = -1
                                                                break

                                                            if offset_5 == buf_eof:
                                                                offset_5 = -1
                                                                break

                                                            codepoint = (buf[offset_5])

                                                            if 48 <= codepoint <= 49:
                                                                offset_5 += 1
                                                                column_5 += 1
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
                                                            if offset_5 + 4 <= buf_eof and buf[offset_5+0] == '0' and buf[offset_5+1] == '0' and buf[offset_5+2] == '0' and buf[offset_5+3] == '0':
                                                                offset_5 += 4
                                                                column_5 += 4
                                                            else:
                                                                offset_5 = -1
                                                                break

                                                            if offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'D':
                                                                offset_5 += 1
                                                                column_5 += 1
                                                            elif offset_5 + 1 <= buf_eof and buf[offset_5+0] == 'd':
                                                                offset_5 += 1
                                                                column_5 += 1
                                                            else:
                                                                offset_5 = -1
                                                                break


                                                            if offset_5 == buf_eof:
                                                                offset_5 = -1
                                                                break

                                                            codepoint = (buf[offset_5])

                                                            if 56 <= codepoint <= 57:
                                                                offset_5 += 1
                                                                column_5 += 1
                                                            elif 65 <= codepoint <= 70:
                                                                offset_5 += 1
                                                                column_5 += 1
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
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break


                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if 48 <= codepoint <= 57:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 97 <= codepoint <= 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif 65 <= codepoint <= 70:
                                                            offset_4 += 1
                                                            column_4 += 1
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
                                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '\\':
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_4 = -1
                                                            break

                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if codepoint == 34:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 92:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 47:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 98:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 102:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 110:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 114:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 116:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 39:
                                                            offset_4 += 1
                                                            column_4 += 1
                                                        elif codepoint == 10:
                                                            offset_4 += 1
                                                            column_4 += 1
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
                                        value_11 = count_1

                                        break
                                    if offset_2 == -1:
                                        break
                                    value_10.name = 'string'
                                    value_10.end = offset_2
                                    value_10.end_column = column_2
                                    value_10.value = None
                                    children_4.append(value_10)

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
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    break
                                # end case
                                offset_1 = -1 # no more choices
                                break # end choice
                            if offset_1 == -1:
                                break

                            count_1 = 0
                            while True:
                                offset_2 = offset_1
                                column_2 = column_1
                                indent_column_2 = list(indent_column_1)
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_4 = [] if children_3 is not None else None
                                while True:
                                    #print('entry rep rule', offset_1, offset_2)
                                    if offset_2 == buf_eof:
                                        offset_2 = -1
                                        break

                                    codepoint = (buf[offset_2])

                                    if codepoint == 32:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 9:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 13:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 10:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 65279:
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    #print('safe exit rep rule', offset_1, offset_2)
                                    break
                                #print('exit rep rule', offset_1, offset_2)
                                if offset_2 == -1:
                                    break
                                if offset_1 == offset_2: break
                                if children_4 is not None and children_4 is not None:
                                    children_3.extend(children_4)
                                offset_1 = offset_2
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                count_1 += 1
                            if offset_1 == -1:
                                break
                            value_12 = count_1

                            count_1 = 0
                            while True:
                                offset_2 = offset_1
                                column_2 = column_1
                                indent_column_2 = list(indent_column_1)
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_4 = [] if children_3 is not None else None
                                while True:
                                    #print('entry rep rule', offset_1, offset_2)
                                    if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '#':
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    count_2 = 0
                                    while True:
                                        offset_3 = offset_2
                                        column_3 = column_2
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            #print('entry rep rule', offset_2, offset_3)
                                            if offset_3 == buf_eof:
                                                offset_3 = -1
                                                break

                                            codepoint = (buf[offset_3])

                                            if codepoint == 10:
                                                offset_3 = -1
                                                break
                                            else:
                                                offset_3 += 1
                                                column_3 += 1

                                            #print('safe exit rep rule', offset_2, offset_3)
                                            break
                                        #print('exit rep rule', offset_2, offset_3)
                                        if offset_3 == -1:
                                            break
                                        if offset_2 == offset_3: break
                                        if children_5 is not None and children_5 is not None:
                                            children_4.extend(children_5)
                                        offset_2 = offset_3
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        count_2 += 1
                                    if offset_2 == -1:
                                        break
                                    value_14 = count_2

                                    count_2 = 0
                                    while True:
                                        offset_3 = offset_2
                                        column_3 = column_2
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            #print('entry rep rule', offset_2, offset_3)
                                            if offset_3 == buf_eof:
                                                offset_3 = -1
                                                break

                                            codepoint = (buf[offset_3])

                                            if codepoint == 32:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 9:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 13:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 10:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 65279:
                                                offset_3 += 1
                                                column_3 += 1
                                            else:
                                                offset_3 = -1
                                                break

                                            #print('safe exit rep rule', offset_2, offset_3)
                                            break
                                        #print('exit rep rule', offset_2, offset_3)
                                        if offset_3 == -1:
                                            break
                                        if offset_2 == offset_3: break
                                        if children_5 is not None and children_5 is not None:
                                            children_4.extend(children_5)
                                        offset_2 = offset_3
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        count_2 += 1
                                    if offset_2 == -1:
                                        break
                                    value_15 = count_2

                                    #print('safe exit rep rule', offset_1, offset_2)
                                    break
                                #print('exit rep rule', offset_1, offset_2)
                                if offset_2 == -1:
                                    break
                                if offset_1 == offset_2: break
                                if children_4 is not None and children_4 is not None:
                                    children_3.extend(children_4)
                                offset_1 = offset_2
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                count_1 += 1
                            if offset_1 == -1:
                                break
                            value_13 = count_1

                            count_1 = 0
                            while True:
                                offset_2 = offset_1
                                column_2 = column_1
                                indent_column_2 = list(indent_column_1)
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_4 = [] if children_3 is not None else None
                                while True:
                                    #print('entry rep rule', offset_1, offset_2)
                                    if offset_2 == buf_eof:
                                        offset_2 = -1
                                        break

                                    codepoint = (buf[offset_2])

                                    if codepoint == 32:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 9:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 13:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 10:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 65279:
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    #print('safe exit rep rule', offset_1, offset_2)
                                    break
                                #print('exit rep rule', offset_1, offset_2)
                                if offset_2 == -1:
                                    break
                                if offset_1 == offset_2: break
                                if children_4 is not None and children_4 is not None:
                                    children_3.extend(children_4)
                                offset_1 = offset_2
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                count_1 += 1
                            if offset_1 == -1:
                                break
                            value_16 = count_1



                            if offset_1 + 1 <= buf_eof and buf[offset_1+0] == ':':
                                offset_1 += 1
                                column_1 += 1
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
                                children_4 = [] if children_3 is not None else None
                                while True:
                                    #print('entry rep rule', offset_1, offset_2)
                                    if offset_2 == buf_eof:
                                        offset_2 = -1
                                        break

                                    codepoint = (buf[offset_2])

                                    if codepoint == 32:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 9:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 13:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 10:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 65279:
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    #print('safe exit rep rule', offset_1, offset_2)
                                    break
                                #print('exit rep rule', offset_1, offset_2)
                                if offset_2 == -1:
                                    break
                                if offset_1 == offset_2: break
                                if children_4 is not None and children_4 is not None:
                                    children_3.extend(children_4)
                                offset_1 = offset_2
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                count_1 += 1
                            if offset_1 == -1:
                                break
                            value_17 = count_1

                            count_1 = 0
                            while True:
                                offset_2 = offset_1
                                column_2 = column_1
                                indent_column_2 = list(indent_column_1)
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_4 = [] if children_3 is not None else None
                                while True:
                                    #print('entry rep rule', offset_1, offset_2)
                                    if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '#':
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    count_2 = 0
                                    while True:
                                        offset_3 = offset_2
                                        column_3 = column_2
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            #print('entry rep rule', offset_2, offset_3)
                                            if offset_3 == buf_eof:
                                                offset_3 = -1
                                                break

                                            codepoint = (buf[offset_3])

                                            if codepoint == 10:
                                                offset_3 = -1
                                                break
                                            else:
                                                offset_3 += 1
                                                column_3 += 1

                                            #print('safe exit rep rule', offset_2, offset_3)
                                            break
                                        #print('exit rep rule', offset_2, offset_3)
                                        if offset_3 == -1:
                                            break
                                        if offset_2 == offset_3: break
                                        if children_5 is not None and children_5 is not None:
                                            children_4.extend(children_5)
                                        offset_2 = offset_3
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        count_2 += 1
                                    if offset_2 == -1:
                                        break
                                    value_19 = count_2

                                    count_2 = 0
                                    while True:
                                        offset_3 = offset_2
                                        column_3 = column_2
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            #print('entry rep rule', offset_2, offset_3)
                                            if offset_3 == buf_eof:
                                                offset_3 = -1
                                                break

                                            codepoint = (buf[offset_3])

                                            if codepoint == 32:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 9:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 13:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 10:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 65279:
                                                offset_3 += 1
                                                column_3 += 1
                                            else:
                                                offset_3 = -1
                                                break

                                            #print('safe exit rep rule', offset_2, offset_3)
                                            break
                                        #print('exit rep rule', offset_2, offset_3)
                                        if offset_3 == -1:
                                            break
                                        if offset_2 == offset_3: break
                                        if children_5 is not None and children_5 is not None:
                                            children_4.extend(children_5)
                                        offset_2 = offset_3
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        count_2 += 1
                                    if offset_2 == -1:
                                        break
                                    value_20 = count_2

                                    #print('safe exit rep rule', offset_1, offset_2)
                                    break
                                #print('exit rep rule', offset_1, offset_2)
                                if offset_2 == -1:
                                    break
                                if offset_1 == offset_2: break
                                if children_4 is not None and children_4 is not None:
                                    children_3.extend(children_4)
                                offset_1 = offset_2
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                count_1 += 1
                            if offset_1 == -1:
                                break
                            value_18 = count_1

                            count_1 = 0
                            while True:
                                offset_2 = offset_1
                                column_2 = column_1
                                indent_column_2 = list(indent_column_1)
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_4 = [] if children_3 is not None else None
                                while True:
                                    #print('entry rep rule', offset_1, offset_2)
                                    if offset_2 == buf_eof:
                                        offset_2 = -1
                                        break

                                    codepoint = (buf[offset_2])

                                    if codepoint == 32:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 9:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 13:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 10:
                                        offset_2 += 1
                                        column_2 += 1
                                    elif codepoint == 65279:
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    #print('safe exit rep rule', offset_1, offset_2)
                                    break
                                #print('exit rep rule', offset_1, offset_2)
                                if offset_2 == -1:
                                    break
                                if offset_1 == offset_2: break
                                if children_4 is not None and children_4 is not None:
                                    children_3.extend(children_4)
                                offset_1 = offset_2
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                count_1 += 1
                            if offset_1 == -1:
                                break
                            value_21 = count_1



                            offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_rson_value(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                            if offset_1 == -1: break


                            break
                        if offset_1 == -1:
                            break
                        value_7.name = 'pair'
                        value_7.end = offset_1
                        value_7.end_column = column_1
                        value_7.value = None
                        children_2.append(value_7)

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
                                if offset_2 == buf_eof:
                                    offset_2 = -1
                                    break

                                codepoint = (buf[offset_2])

                                if codepoint == 32:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 9:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 13:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 10:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 65279:
                                    offset_2 += 1
                                    column_2 += 1
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
                        value_22 = count_1

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
                                if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '#':
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 10:
                                            offset_3 = -1
                                            break
                                        else:
                                            offset_3 += 1
                                            column_3 += 1

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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_24 = count_2

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 32:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 9:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 13:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 65279:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_25 = count_2

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
                        value_23 = count_1

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
                                if offset_2 == buf_eof:
                                    offset_2 = -1
                                    break

                                codepoint = (buf[offset_2])

                                if codepoint == 32:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 9:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 13:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 10:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 65279:
                                    offset_2 += 1
                                    column_2 += 1
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
                        value_26 = count_1



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
                                if offset_2 + 1 <= buf_eof and buf[offset_2+0] == ',':
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 32:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 9:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 13:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 65279:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_28 = count_2

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '#':
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if codepoint == 10:
                                                    offset_4 = -1
                                                    break
                                                else:
                                                    offset_4 += 1
                                                    column_4 += 1

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_3 == -1:
                                            break
                                        value_30 = count_3

                                        count_3 = 0
                                        while True:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if codepoint == 32:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 9:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 13:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 10:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 65279:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_3 == -1:
                                            break
                                        value_31 = count_3

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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_29 = count_2

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 32:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 9:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 13:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 65279:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_32 = count_2



                                children_4 = []
                                value_33 = Node(None, offset_2, offset_2, column_2, column_2, children_4, None)
                                while True: # start capture
                                    while True: # start choice
                                        offset_3 = offset_2
                                        column_3 = column_2
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True: # case
                                            if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '"':
                                                offset_3 += 1
                                                column_3 += 1
                                            else:
                                                offset_3 = -1
                                                break

                                            children_6 = None
                                            value_34 = Node(None, offset_3, offset_3, column_3, column_3, children_6, None)
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
                                                                    column_5 += 1



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
                                                                if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '\\' and buf[offset_5+1] == 'x':
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
                                                                    if offset_6 == buf_eof:
                                                                        offset_6 = -1
                                                                        break

                                                                    codepoint = (buf[offset_6])

                                                                    if 48 <= codepoint <= 49:
                                                                        offset_6 += 1
                                                                        column_6 += 1
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
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
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
                                                                if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '\\' and buf[offset_5+1] == 'u':
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
                                                                    if offset_6 + 3 <= buf_eof and buf[offset_6+0] == '0' and buf[offset_6+1] == '0' and buf[offset_6+2] == '0':
                                                                        offset_6 += 3
                                                                        column_6 += 3
                                                                    else:
                                                                        offset_6 = -1
                                                                        break

                                                                    if offset_6 == buf_eof:
                                                                        offset_6 = -1
                                                                        break

                                                                    codepoint = (buf[offset_6])

                                                                    if 48 <= codepoint <= 49:
                                                                        offset_6 += 1
                                                                        column_6 += 1
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
                                                                    if offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'D':
                                                                        offset_6 += 1
                                                                        column_6 += 1
                                                                    elif offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'd':
                                                                        offset_6 += 1
                                                                        column_6 += 1
                                                                    else:
                                                                        offset_6 = -1
                                                                        break


                                                                    if offset_6 == buf_eof:
                                                                        offset_6 = -1
                                                                        break

                                                                    codepoint = (buf[offset_6])

                                                                    if 56 <= codepoint <= 57:
                                                                        offset_6 += 1
                                                                        column_6 += 1
                                                                    elif 65 <= codepoint <= 70:
                                                                        offset_6 += 1
                                                                        column_6 += 1
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
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
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
                                                                if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '\\' and buf[offset_5+1] == 'U':
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
                                                                    if offset_6 + 7 <= buf_eof and buf[offset_6+0] == '0' and buf[offset_6+1] == '0' and buf[offset_6+2] == '0' and buf[offset_6+3] == '0' and buf[offset_6+4] == '0' and buf[offset_6+5] == '0' and buf[offset_6+6] == '0':
                                                                        offset_6 += 7
                                                                        column_6 += 7
                                                                    else:
                                                                        offset_6 = -1
                                                                        break

                                                                    if offset_6 == buf_eof:
                                                                        offset_6 = -1
                                                                        break

                                                                    codepoint = (buf[offset_6])

                                                                    if 48 <= codepoint <= 49:
                                                                        offset_6 += 1
                                                                        column_6 += 1
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
                                                                    if offset_6 + 4 <= buf_eof and buf[offset_6+0] == '0' and buf[offset_6+1] == '0' and buf[offset_6+2] == '0' and buf[offset_6+3] == '0':
                                                                        offset_6 += 4
                                                                        column_6 += 4
                                                                    else:
                                                                        offset_6 = -1
                                                                        break

                                                                    if offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'D':
                                                                        offset_6 += 1
                                                                        column_6 += 1
                                                                    elif offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'd':
                                                                        offset_6 += 1
                                                                        column_6 += 1
                                                                    else:
                                                                        offset_6 = -1
                                                                        break


                                                                    if offset_6 == buf_eof:
                                                                        offset_6 = -1
                                                                        break

                                                                    codepoint = (buf[offset_6])

                                                                    if 56 <= codepoint <= 57:
                                                                        offset_6 += 1
                                                                        column_6 += 1
                                                                    elif 65 <= codepoint <= 70:
                                                                        offset_6 += 1
                                                                        column_6 += 1
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
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
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
                                                                if offset_5 + 1 <= buf_eof and buf[offset_5+0] == '\\':
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break

                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if codepoint == 34:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 92:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 47:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 98:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 110:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 114:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 116:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 39:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 10:
                                                                    offset_5 += 1
                                                                    column_5 += 1
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
                                                value_35 = count_2

                                                break
                                            if offset_3 == -1:
                                                break
                                            value_34.name = 'string'
                                            value_34.end = offset_3
                                            value_34.end_column = column_3
                                            value_34.value = None
                                            children_5.append(value_34)

                                            if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '"':
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
                                            if offset_3 + 1 <= buf_eof and buf[offset_3+0] == "'":
                                                offset_3 += 1
                                                column_3 += 1
                                            else:
                                                offset_3 = -1
                                                break

                                            children_6 = None
                                            value_36 = Node(None, offset_3, offset_3, column_3, column_3, children_6, None)
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
                                                                    column_5 += 1



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
                                                                if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '\\' and buf[offset_5+1] == 'x':
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
                                                                    if offset_6 == buf_eof:
                                                                        offset_6 = -1
                                                                        break

                                                                    codepoint = (buf[offset_6])

                                                                    if 48 <= codepoint <= 49:
                                                                        offset_6 += 1
                                                                        column_6 += 1
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
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
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
                                                                if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '\\' and buf[offset_5+1] == 'u':
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
                                                                    if offset_6 + 2 <= buf_eof and buf[offset_6+0] == '0' and buf[offset_6+1] == '0':
                                                                        offset_6 += 2
                                                                        column_6 += 2
                                                                    else:
                                                                        offset_6 = -1
                                                                        break

                                                                    if offset_6 == buf_eof:
                                                                        offset_6 = -1
                                                                        break

                                                                    codepoint = (buf[offset_6])

                                                                    if 48 <= codepoint <= 49:
                                                                        offset_6 += 1
                                                                        column_6 += 1
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
                                                                    if offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'D':
                                                                        offset_6 += 1
                                                                        column_6 += 1
                                                                    elif offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'd':
                                                                        offset_6 += 1
                                                                        column_6 += 1
                                                                    else:
                                                                        offset_6 = -1
                                                                        break


                                                                    if offset_6 == buf_eof:
                                                                        offset_6 = -1
                                                                        break

                                                                    codepoint = (buf[offset_6])

                                                                    if 56 <= codepoint <= 57:
                                                                        offset_6 += 1
                                                                        column_6 += 1
                                                                    elif 65 <= codepoint <= 70:
                                                                        offset_6 += 1
                                                                        column_6 += 1
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
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
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
                                                                if offset_5 + 2 <= buf_eof and buf[offset_5+0] == '\\' and buf[offset_5+1] == 'U':
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
                                                                    if offset_6 + 6 <= buf_eof and buf[offset_6+0] == '0' and buf[offset_6+1] == '0' and buf[offset_6+2] == '0' and buf[offset_6+3] == '0' and buf[offset_6+4] == '0' and buf[offset_6+5] == '0':
                                                                        offset_6 += 6
                                                                        column_6 += 6
                                                                    else:
                                                                        offset_6 = -1
                                                                        break

                                                                    if offset_6 == buf_eof:
                                                                        offset_6 = -1
                                                                        break

                                                                    codepoint = (buf[offset_6])

                                                                    if 48 <= codepoint <= 49:
                                                                        offset_6 += 1
                                                                        column_6 += 1
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
                                                                    if offset_6 + 4 <= buf_eof and buf[offset_6+0] == '0' and buf[offset_6+1] == '0' and buf[offset_6+2] == '0' and buf[offset_6+3] == '0':
                                                                        offset_6 += 4
                                                                        column_6 += 4
                                                                    else:
                                                                        offset_6 = -1
                                                                        break

                                                                    if offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'D':
                                                                        offset_6 += 1
                                                                        column_6 += 1
                                                                    elif offset_6 + 1 <= buf_eof and buf[offset_6+0] == 'd':
                                                                        offset_6 += 1
                                                                        column_6 += 1
                                                                    else:
                                                                        offset_6 = -1
                                                                        break


                                                                    if offset_6 == buf_eof:
                                                                        offset_6 = -1
                                                                        break

                                                                    codepoint = (buf[offset_6])

                                                                    if 56 <= codepoint <= 57:
                                                                        offset_6 += 1
                                                                        column_6 += 1
                                                                    elif 65 <= codepoint <= 70:
                                                                        offset_6 += 1
                                                                        column_6 += 1
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
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break


                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if 48 <= codepoint <= 57:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 97 <= codepoint <= 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif 65 <= codepoint <= 70:
                                                                    offset_5 += 1
                                                                    column_5 += 1
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
                                                                if offset_5 + 1 <= buf_eof and buf[offset_5+0] == '\\':
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                else:
                                                                    offset_5 = -1
                                                                    break

                                                                if offset_5 == buf_eof:
                                                                    offset_5 = -1
                                                                    break

                                                                codepoint = (buf[offset_5])

                                                                if codepoint == 34:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 92:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 47:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 98:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 102:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 110:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 114:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 116:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 39:
                                                                    offset_5 += 1
                                                                    column_5 += 1
                                                                elif codepoint == 10:
                                                                    offset_5 += 1
                                                                    column_5 += 1
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
                                                value_37 = count_2

                                                break
                                            if offset_3 == -1:
                                                break
                                            value_36.name = 'string'
                                            value_36.end = offset_3
                                            value_36.end_column = column_3
                                            value_36.value = None
                                            children_5.append(value_36)

                                            if offset_3 + 1 <= buf_eof and buf[offset_3+0] == "'":
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

                                    count_2 = 0
                                    while True:
                                        offset_3 = offset_2
                                        column_3 = column_2
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            #print('entry rep rule', offset_2, offset_3)
                                            if offset_3 == buf_eof:
                                                offset_3 = -1
                                                break

                                            codepoint = (buf[offset_3])

                                            if codepoint == 32:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 9:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 13:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 10:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 65279:
                                                offset_3 += 1
                                                column_3 += 1
                                            else:
                                                offset_3 = -1
                                                break

                                            #print('safe exit rep rule', offset_2, offset_3)
                                            break
                                        #print('exit rep rule', offset_2, offset_3)
                                        if offset_3 == -1:
                                            break
                                        if offset_2 == offset_3: break
                                        if children_5 is not None and children_5 is not None:
                                            children_4.extend(children_5)
                                        offset_2 = offset_3
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        count_2 += 1
                                    if offset_2 == -1:
                                        break
                                    value_38 = count_2

                                    count_2 = 0
                                    while True:
                                        offset_3 = offset_2
                                        column_3 = column_2
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            #print('entry rep rule', offset_2, offset_3)
                                            if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '#':
                                                offset_3 += 1
                                                column_3 += 1
                                            else:
                                                offset_3 = -1
                                                break

                                            count_3 = 0
                                            while True:
                                                offset_4 = offset_3
                                                column_4 = column_3
                                                indent_column_4 = list(indent_column_3)
                                                partial_tab_offset_4 = partial_tab_offset_3
                                                partial_tab_width_4 = partial_tab_width_3
                                                children_6 = [] if children_5 is not None else None
                                                while True:
                                                    #print('entry rep rule', offset_3, offset_4)
                                                    if offset_4 == buf_eof:
                                                        offset_4 = -1
                                                        break

                                                    codepoint = (buf[offset_4])

                                                    if codepoint == 10:
                                                        offset_4 = -1
                                                        break
                                                    else:
                                                        offset_4 += 1
                                                        column_4 += 1

                                                    #print('safe exit rep rule', offset_3, offset_4)
                                                    break
                                                #print('exit rep rule', offset_3, offset_4)
                                                if offset_4 == -1:
                                                    break
                                                if offset_3 == offset_4: break
                                                if children_6 is not None and children_6 is not None:
                                                    children_5.extend(children_6)
                                                offset_3 = offset_4
                                                column_3 = column_4
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                count_3 += 1
                                            if offset_3 == -1:
                                                break
                                            value_40 = count_3

                                            count_3 = 0
                                            while True:
                                                offset_4 = offset_3
                                                column_4 = column_3
                                                indent_column_4 = list(indent_column_3)
                                                partial_tab_offset_4 = partial_tab_offset_3
                                                partial_tab_width_4 = partial_tab_width_3
                                                children_6 = [] if children_5 is not None else None
                                                while True:
                                                    #print('entry rep rule', offset_3, offset_4)
                                                    if offset_4 == buf_eof:
                                                        offset_4 = -1
                                                        break

                                                    codepoint = (buf[offset_4])

                                                    if codepoint == 32:
                                                        offset_4 += 1
                                                        column_4 += 1
                                                    elif codepoint == 9:
                                                        offset_4 += 1
                                                        column_4 += 1
                                                    elif codepoint == 13:
                                                        offset_4 += 1
                                                        column_4 += 1
                                                    elif codepoint == 10:
                                                        offset_4 += 1
                                                        column_4 += 1
                                                    elif codepoint == 65279:
                                                        offset_4 += 1
                                                        column_4 += 1
                                                    else:
                                                        offset_4 = -1
                                                        break

                                                    #print('safe exit rep rule', offset_3, offset_4)
                                                    break
                                                #print('exit rep rule', offset_3, offset_4)
                                                if offset_4 == -1:
                                                    break
                                                if offset_3 == offset_4: break
                                                if children_6 is not None and children_6 is not None:
                                                    children_5.extend(children_6)
                                                offset_3 = offset_4
                                                column_3 = column_4
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                count_3 += 1
                                            if offset_3 == -1:
                                                break
                                            value_41 = count_3

                                            #print('safe exit rep rule', offset_2, offset_3)
                                            break
                                        #print('exit rep rule', offset_2, offset_3)
                                        if offset_3 == -1:
                                            break
                                        if offset_2 == offset_3: break
                                        if children_5 is not None and children_5 is not None:
                                            children_4.extend(children_5)
                                        offset_2 = offset_3
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        count_2 += 1
                                    if offset_2 == -1:
                                        break
                                    value_39 = count_2

                                    count_2 = 0
                                    while True:
                                        offset_3 = offset_2
                                        column_3 = column_2
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            #print('entry rep rule', offset_2, offset_3)
                                            if offset_3 == buf_eof:
                                                offset_3 = -1
                                                break

                                            codepoint = (buf[offset_3])

                                            if codepoint == 32:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 9:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 13:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 10:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 65279:
                                                offset_3 += 1
                                                column_3 += 1
                                            else:
                                                offset_3 = -1
                                                break

                                            #print('safe exit rep rule', offset_2, offset_3)
                                            break
                                        #print('exit rep rule', offset_2, offset_3)
                                        if offset_3 == -1:
                                            break
                                        if offset_2 == offset_3: break
                                        if children_5 is not None and children_5 is not None:
                                            children_4.extend(children_5)
                                        offset_2 = offset_3
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        count_2 += 1
                                    if offset_2 == -1:
                                        break
                                    value_42 = count_2



                                    if offset_2 + 1 <= buf_eof and buf[offset_2+0] == ':':
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    count_2 = 0
                                    while True:
                                        offset_3 = offset_2
                                        column_3 = column_2
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            #print('entry rep rule', offset_2, offset_3)
                                            if offset_3 == buf_eof:
                                                offset_3 = -1
                                                break

                                            codepoint = (buf[offset_3])

                                            if codepoint == 32:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 9:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 13:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 10:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 65279:
                                                offset_3 += 1
                                                column_3 += 1
                                            else:
                                                offset_3 = -1
                                                break

                                            #print('safe exit rep rule', offset_2, offset_3)
                                            break
                                        #print('exit rep rule', offset_2, offset_3)
                                        if offset_3 == -1:
                                            break
                                        if offset_2 == offset_3: break
                                        if children_5 is not None and children_5 is not None:
                                            children_4.extend(children_5)
                                        offset_2 = offset_3
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        count_2 += 1
                                    if offset_2 == -1:
                                        break
                                    value_43 = count_2

                                    count_2 = 0
                                    while True:
                                        offset_3 = offset_2
                                        column_3 = column_2
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            #print('entry rep rule', offset_2, offset_3)
                                            if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '#':
                                                offset_3 += 1
                                                column_3 += 1
                                            else:
                                                offset_3 = -1
                                                break

                                            count_3 = 0
                                            while True:
                                                offset_4 = offset_3
                                                column_4 = column_3
                                                indent_column_4 = list(indent_column_3)
                                                partial_tab_offset_4 = partial_tab_offset_3
                                                partial_tab_width_4 = partial_tab_width_3
                                                children_6 = [] if children_5 is not None else None
                                                while True:
                                                    #print('entry rep rule', offset_3, offset_4)
                                                    if offset_4 == buf_eof:
                                                        offset_4 = -1
                                                        break

                                                    codepoint = (buf[offset_4])

                                                    if codepoint == 10:
                                                        offset_4 = -1
                                                        break
                                                    else:
                                                        offset_4 += 1
                                                        column_4 += 1

                                                    #print('safe exit rep rule', offset_3, offset_4)
                                                    break
                                                #print('exit rep rule', offset_3, offset_4)
                                                if offset_4 == -1:
                                                    break
                                                if offset_3 == offset_4: break
                                                if children_6 is not None and children_6 is not None:
                                                    children_5.extend(children_6)
                                                offset_3 = offset_4
                                                column_3 = column_4
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                count_3 += 1
                                            if offset_3 == -1:
                                                break
                                            value_45 = count_3

                                            count_3 = 0
                                            while True:
                                                offset_4 = offset_3
                                                column_4 = column_3
                                                indent_column_4 = list(indent_column_3)
                                                partial_tab_offset_4 = partial_tab_offset_3
                                                partial_tab_width_4 = partial_tab_width_3
                                                children_6 = [] if children_5 is not None else None
                                                while True:
                                                    #print('entry rep rule', offset_3, offset_4)
                                                    if offset_4 == buf_eof:
                                                        offset_4 = -1
                                                        break

                                                    codepoint = (buf[offset_4])

                                                    if codepoint == 32:
                                                        offset_4 += 1
                                                        column_4 += 1
                                                    elif codepoint == 9:
                                                        offset_4 += 1
                                                        column_4 += 1
                                                    elif codepoint == 13:
                                                        offset_4 += 1
                                                        column_4 += 1
                                                    elif codepoint == 10:
                                                        offset_4 += 1
                                                        column_4 += 1
                                                    elif codepoint == 65279:
                                                        offset_4 += 1
                                                        column_4 += 1
                                                    else:
                                                        offset_4 = -1
                                                        break

                                                    #print('safe exit rep rule', offset_3, offset_4)
                                                    break
                                                #print('exit rep rule', offset_3, offset_4)
                                                if offset_4 == -1:
                                                    break
                                                if offset_3 == offset_4: break
                                                if children_6 is not None and children_6 is not None:
                                                    children_5.extend(children_6)
                                                offset_3 = offset_4
                                                column_3 = column_4
                                                indent_column_3 = indent_column_4
                                                partial_tab_offset_3 = partial_tab_offset_4
                                                partial_tab_width_3 = partial_tab_width_4
                                                count_3 += 1
                                            if offset_3 == -1:
                                                break
                                            value_46 = count_3

                                            #print('safe exit rep rule', offset_2, offset_3)
                                            break
                                        #print('exit rep rule', offset_2, offset_3)
                                        if offset_3 == -1:
                                            break
                                        if offset_2 == offset_3: break
                                        if children_5 is not None and children_5 is not None:
                                            children_4.extend(children_5)
                                        offset_2 = offset_3
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        count_2 += 1
                                    if offset_2 == -1:
                                        break
                                    value_44 = count_2

                                    count_2 = 0
                                    while True:
                                        offset_3 = offset_2
                                        column_3 = column_2
                                        indent_column_3 = list(indent_column_2)
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            #print('entry rep rule', offset_2, offset_3)
                                            if offset_3 == buf_eof:
                                                offset_3 = -1
                                                break

                                            codepoint = (buf[offset_3])

                                            if codepoint == 32:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 9:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 13:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 10:
                                                offset_3 += 1
                                                column_3 += 1
                                            elif codepoint == 65279:
                                                offset_3 += 1
                                                column_3 += 1
                                            else:
                                                offset_3 = -1
                                                break

                                            #print('safe exit rep rule', offset_2, offset_3)
                                            break
                                        #print('exit rep rule', offset_2, offset_3)
                                        if offset_3 == -1:
                                            break
                                        if offset_2 == offset_3: break
                                        if children_5 is not None and children_5 is not None:
                                            children_4.extend(children_5)
                                        offset_2 = offset_3
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        count_2 += 1
                                    if offset_2 == -1:
                                        break
                                    value_47 = count_2



                                    offset_2, column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_rson_value(buf, buf_start, buf_eof, offset_2, column_2, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                    if offset_2 == -1: break


                                    break
                                if offset_2 == -1:
                                    break
                                value_33.name = 'pair'
                                value_33.end = offset_2
                                value_33.end_column = column_2
                                value_33.value = None
                                children_3.append(value_33)

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 32:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 9:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 13:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 65279:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_48 = count_2

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '#':
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if codepoint == 10:
                                                    offset_4 = -1
                                                    break
                                                else:
                                                    offset_4 += 1
                                                    column_4 += 1

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_3 == -1:
                                            break
                                        value_50 = count_3

                                        count_3 = 0
                                        while True:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if codepoint == 32:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 9:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 13:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 10:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 65279:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_3 == -1:
                                            break
                                        value_51 = count_3

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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_49 = count_2

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 32:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 9:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 13:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 65279:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_52 = count_2



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
                        value_27 = count_1

                        count_1 = 0
                        while count_1 < 1:
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                #print('entry rep rule', offset_1, offset_2)
                                if offset_2 + 1 <= buf_eof and buf[offset_2+0] == ',':
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 32:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 9:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 13:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 65279:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_54 = count_2

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '#':
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if codepoint == 10:
                                                    offset_4 = -1
                                                    break
                                                else:
                                                    offset_4 += 1
                                                    column_4 += 1

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_3 == -1:
                                            break
                                        value_56 = count_3

                                        count_3 = 0
                                        while True:
                                            offset_4 = offset_3
                                            column_4 = column_3
                                            indent_column_4 = list(indent_column_3)
                                            partial_tab_offset_4 = partial_tab_offset_3
                                            partial_tab_width_4 = partial_tab_width_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                #print('entry rep rule', offset_3, offset_4)
                                                if offset_4 == buf_eof:
                                                    offset_4 = -1
                                                    break

                                                codepoint = (buf[offset_4])

                                                if codepoint == 32:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 9:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 13:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 10:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                elif codepoint == 65279:
                                                    offset_4 += 1
                                                    column_4 += 1
                                                else:
                                                    offset_4 = -1
                                                    break

                                                #print('safe exit rep rule', offset_3, offset_4)
                                                break
                                            #print('exit rep rule', offset_3, offset_4)
                                            if offset_4 == -1:
                                                break
                                            if offset_3 == offset_4: break
                                            if children_5 is not None and children_5 is not None:
                                                children_4.extend(children_5)
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            count_3 += 1
                                        if offset_3 == -1:
                                            break
                                        value_57 = count_3

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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_55 = count_2

                                count_2 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 32:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 9:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 13:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 10:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 65279:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_58 = count_2


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
                            break
                        if offset_1 == -1:
                            break
                        value_53 = count_1


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
                value_6 = count_0

                break
            if offset_0 == -1:
                break
            value_5.name = 'object'
            value_5.end = offset_0
            value_5.end_column = column_0
            value_5.value = None
            children_0.append(value_5)

            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '}':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0
