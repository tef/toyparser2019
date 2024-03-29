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
        cdef int offset_1
        cdef int column_1

        cdef list children_1

        cdef list indent_column_1
        cdef int partial_tab_offset_1
        cdef int partial_tab_width_1
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof:
                codepoint = buf[offset_0]
                if codepoint in ' \t\r\n':
                    if codepoint == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-((column_0)%self.tabstop));
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break

            while True: # start lookahed
                children_1 = []
                offset_1 = offset_0 + 0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '[':
                    offset_1 += 1
                    column_1 += 1
                elif offset_1 + 1 <= buf_eof and buf[offset_1+0] == '{':
                    offset_1 += 1
                    column_1 += 1
                else:
                    offset_1 = -1
                    break


                break
            if offset_1 == -1:
                offset_0 = -1
                break

            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_json_list(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_json_object(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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

    cdef (int, int, int, int) parse_json_value(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2, offset_3, offset_4
        cdef int column_1, column_2, column_3, column_4

        cdef list children_1, children_2, children_3, children_4, children_5
        cdef int count_1, count_2, count_3
        cdef list indent_column_1, indent_column_2, indent_column_3, indent_column_4
        cdef int partial_tab_offset_1, partial_tab_offset_2, partial_tab_offset_3, partial_tab_offset_4
        cdef int partial_tab_width_1, partial_tab_width_2, partial_tab_width_3, partial_tab_width_4
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_json_list(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_json_object(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '"':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    children_2 = None
                    value_0 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        count_0 = 0
                        while True:
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                #print('entry rep rule', offset_1, offset_2)
                                while True: # start choice
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_3 + 2 <= buf_eof and buf[offset_3+0] == '\\' and buf[offset_3+1] == 'u':
                                            offset_3 += 2
                                            column_3 += 2
                                        else:
                                            offset_3 = -1
                                            break

                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if 48 <= codepoint <= 57:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
                                            break

                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if 48 <= codepoint <= 57:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
                                            break

                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if 48 <= codepoint <= 57:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
                                            break

                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if 48 <= codepoint <= 57:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif 97 <= codepoint <= 102:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif 65 <= codepoint <= 70:
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
                                        if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '\\':
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
                                            break

                                        if offset_3 == buf_eof:
                                            offset_3 = -1
                                            break

                                        codepoint = (buf[offset_3])

                                        if codepoint == 34:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 92:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 47:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 98:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 102:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 110:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 114:
                                            offset_3 += 1
                                            column_3 += 1
                                        elif codepoint == 116:
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

                                        if codepoint == 92:
                                            offset_3 = -1
                                            break
                                        elif codepoint == 34:
                                            offset_3 = -1
                                            break
                                        else:
                                            offset_3 += 1
                                            column_3 += 1


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
                            count_0 += 1
                        if offset_1 == -1:
                            break
                        value_1 = count_0



                        break
                    if offset_1 == -1:
                        break
                    value_0.name = 'string'
                    value_0.end = offset_1
                    value_0.end_column = column_1
                    value_0.value = None
                    children_1.append(value_0)

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
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    children_2 = None
                    value_2 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        count_0 = 0
                        while count_0 < 1:
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                #print('entry rep rule', offset_1, offset_2)
                                if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '-':
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
                            count_0 += 1
                            break
                        if offset_1 == -1:
                            break
                        value_3 = count_0


                        while True: # start choice
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '0':
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
                                if offset_2 == buf_eof:
                                    offset_2 = -1
                                    break

                                codepoint = (buf[offset_2])

                                if 49 <= codepoint <= 57:
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
                                value_4 = count_0


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


                        count_0 = 0
                        while count_0 < 1:
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                #print('entry rep rule', offset_1, offset_2)
                                if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '.':
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

                                count_1 = 0
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
                                    count_1 += 1
                                if offset_2 == -1:
                                    break
                                value_6 = count_1

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
                            count_0 += 1
                            break
                        if offset_1 == -1:
                            break
                        value_5 = count_0


                        count_0 = 0
                        while count_0 < 1:
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                #print('entry rep rule', offset_1, offset_2)
                                if offset_2 + 1 <= buf_eof and buf[offset_2+0] == 'e':
                                    offset_2 += 1
                                    column_2 += 1
                                elif offset_2 + 1 <= buf_eof and buf[offset_2+0] == 'E':
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

                                count_1 = 0
                                while count_1 < 1:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = list(indent_column_2)
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_2, offset_3)
                                        if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '+':
                                            offset_3 += 1
                                            column_3 += 1
                                        elif offset_3 + 1 <= buf_eof and buf[offset_3+0] == '-':
                                            offset_3 += 1
                                            column_3 += 1
                                        else:
                                            offset_3 = -1
                                            break

                                        count_2 = 0
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
                                            count_2 += 1
                                        if offset_3 == -1:
                                            break
                                        value_9 = count_2

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
                                    count_1 += 1
                                    break
                                if offset_2 == -1:
                                    break
                                value_8 = count_1

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
                            count_0 += 1
                            break
                        if offset_1 == -1:
                            break
                        value_7 = count_0


                        break
                    if offset_1 == -1:
                        break
                    value_2.name = 'number'
                    value_2.end = offset_1
                    value_2.end_column = column_1
                    value_2.value = None
                    children_1.append(value_2)


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
                    value_10 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
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
                    value_10.name = 'bool'
                    value_10.end = offset_1
                    value_10.end_column = column_1
                    value_10.value = None
                    children_1.append(value_10)


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
                    value_11 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
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
                    value_11.name = 'bool'
                    value_11.end = offset_1
                    value_11.end_column = column_1
                    value_11.value = None
                    children_1.append(value_11)


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
                    value_12 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
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
                    value_12.name = 'bool'
                    value_12.end = offset_1
                    value_12.end_column = column_1
                    value_12.value = None
                    children_1.append(value_12)


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

    cdef (int, int, int, int) parse_json_list(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2
        cdef int column_1, column_2

        cdef list children_1, children_2, children_3
        cdef int count_1, count_2
        cdef list indent_column_1, indent_column_2
        cdef int partial_tab_offset_1, partial_tab_offset_2
        cdef int partial_tab_width_1, partial_tab_width_2
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
                if codepoint in ' \t\r\n':
                    if codepoint == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-((column_0)%self.tabstop));
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
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
                        offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_json_value(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
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
                                while offset_2 < buf_eof:
                                    codepoint = buf[offset_2]
                                    if codepoint in ' \t\r\n':
                                        if codepoint == '\t':
                                            if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-((column_2)%self.tabstop));
                                            count_2 += width
                                            column_2 += width
                                            offset_2 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
                                            offset_2 += 1
                                    else:
                                        break

                                if offset_2 + 1 <= buf_eof and buf[offset_2+0] == ',':
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

                                count_2 = 0
                                while offset_2 < buf_eof:
                                    codepoint = buf[offset_2]
                                    if codepoint in ' \t\r\n':
                                        if codepoint == '\t':
                                            if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-((column_2)%self.tabstop));
                                            count_2 += width
                                            column_2 += width
                                            offset_2 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
                                            offset_2 += 1
                                    else:
                                        break

                                offset_2, column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_json_value(buf, buf_start, buf_eof, offset_2, column_2, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
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

            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == ']':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    cdef (int, int, int, int) parse_json_object(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2, offset_3, offset_4
        cdef int column_1, column_2, column_3, column_4

        cdef list children_1, children_2, children_3, children_4, children_5, children_6, children_7
        cdef int count_1, count_2, count_3
        cdef list indent_column_1, indent_column_2, indent_column_3, indent_column_4
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
                if codepoint in ' \t\r\n':
                    if codepoint == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-((column_0)%self.tabstop));
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
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
                            if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '"':
                                offset_1 += 1
                                column_1 += 1
                            else:
                                offset_1 = -1
                                break

                            children_4 = None
                            value_3 = Node(None, offset_1, offset_1, column_1, column_1, children_4, None)
                            while True: # start capture
                                count_1 = 0
                                while True:
                                    offset_2 = offset_1
                                    column_2 = column_1
                                    indent_column_2 = list(indent_column_1)
                                    partial_tab_offset_2 = partial_tab_offset_1
                                    partial_tab_width_2 = partial_tab_width_1
                                    children_5 = [] if children_4 is not None else None
                                    while True:
                                        #print('entry rep rule', offset_1, offset_2)
                                        while True: # start choice
                                            offset_3 = offset_2
                                            column_3 = column_2
                                            indent_column_3 = list(indent_column_2)
                                            partial_tab_offset_3 = partial_tab_offset_2
                                            partial_tab_width_3 = partial_tab_width_2
                                            children_6 = [] if children_5 is not None else None
                                            while True: # case
                                                if offset_3 + 2 <= buf_eof and buf[offset_3+0] == '\\' and buf[offset_3+1] == 'u':
                                                    offset_3 += 2
                                                    column_3 += 2
                                                else:
                                                    offset_3 = -1
                                                    break

                                                if offset_3 == buf_eof:
                                                    offset_3 = -1
                                                    break

                                                codepoint = (buf[offset_3])

                                                if 48 <= codepoint <= 57:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                else:
                                                    offset_3 = -1
                                                    break

                                                if offset_3 == buf_eof:
                                                    offset_3 = -1
                                                    break

                                                codepoint = (buf[offset_3])

                                                if 48 <= codepoint <= 57:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                else:
                                                    offset_3 = -1
                                                    break

                                                if offset_3 == buf_eof:
                                                    offset_3 = -1
                                                    break

                                                codepoint = (buf[offset_3])

                                                if 48 <= codepoint <= 57:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif 65 <= codepoint <= 70:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                else:
                                                    offset_3 = -1
                                                    break

                                                if offset_3 == buf_eof:
                                                    offset_3 = -1
                                                    break

                                                codepoint = (buf[offset_3])

                                                if 48 <= codepoint <= 57:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif 97 <= codepoint <= 102:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif 65 <= codepoint <= 70:
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
                                                if children_6 is not None and children_6 is not None:
                                                    children_5.extend(children_6)
                                                break
                                            # end case
                                            offset_3 = offset_2
                                            column_3 = column_2
                                            indent_column_3 = list(indent_column_2)
                                            partial_tab_offset_3 = partial_tab_offset_2
                                            partial_tab_width_3 = partial_tab_width_2
                                            children_6 = [] if children_5 is not None else None
                                            while True: # case
                                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '\\':
                                                    offset_3 += 1
                                                    column_3 += 1
                                                else:
                                                    offset_3 = -1
                                                    break

                                                if offset_3 == buf_eof:
                                                    offset_3 = -1
                                                    break

                                                codepoint = (buf[offset_3])

                                                if codepoint == 34:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif codepoint == 92:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif codepoint == 47:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif codepoint == 98:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif codepoint == 102:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif codepoint == 110:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif codepoint == 114:
                                                    offset_3 += 1
                                                    column_3 += 1
                                                elif codepoint == 116:
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
                                                if children_6 is not None and children_6 is not None:
                                                    children_5.extend(children_6)
                                                break
                                            # end case
                                            offset_3 = offset_2
                                            column_3 = column_2
                                            indent_column_3 = list(indent_column_2)
                                            partial_tab_offset_3 = partial_tab_offset_2
                                            partial_tab_width_3 = partial_tab_width_2
                                            children_6 = [] if children_5 is not None else None
                                            while True: # case
                                                if offset_3 == buf_eof:
                                                    offset_3 = -1
                                                    break

                                                codepoint = (buf[offset_3])

                                                if codepoint == 92:
                                                    offset_3 = -1
                                                    break
                                                elif codepoint == 34:
                                                    offset_3 = -1
                                                    break
                                                else:
                                                    offset_3 += 1
                                                    column_3 += 1


                                                break
                                            if offset_3 != -1:
                                                offset_2 = offset_3
                                                column_2 = column_3
                                                indent_column_2 = indent_column_3
                                                partial_tab_offset_2 = partial_tab_offset_3
                                                partial_tab_width_2 = partial_tab_width_3
                                                if children_6 is not None and children_6 is not None:
                                                    children_5.extend(children_6)
                                                break
                                            # end case
                                            offset_2 = -1 # no more choices
                                            break # end choice
                                        if offset_2 == -1:
                                            break

                                        #print('safe exit rep rule', offset_1, offset_2)
                                        break
                                    #print('exit rep rule', offset_1, offset_2)
                                    if offset_2 == -1:
                                        break
                                    if offset_1 == offset_2: break
                                    if children_5 is not None and children_5 is not None:
                                        children_4.extend(children_5)
                                    offset_1 = offset_2
                                    column_1 = column_2
                                    indent_column_1 = indent_column_2
                                    partial_tab_offset_1 = partial_tab_offset_2
                                    partial_tab_width_1 = partial_tab_width_2
                                    count_1 += 1
                                if offset_1 == -1:
                                    break
                                value_4 = count_1



                                break
                            if offset_1 == -1:
                                break
                            value_3.name = 'string'
                            value_3.end = offset_1
                            value_3.end_column = column_1
                            value_3.value = None
                            children_3.append(value_3)

                            if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '"':
                                offset_1 += 1
                                column_1 += 1
                            else:
                                offset_1 = -1
                                break


                            count_1 = 0
                            while offset_1 < buf_eof:
                                codepoint = buf[offset_1]
                                if codepoint in ' \t\r\n':
                                    if codepoint == '\t':
                                        if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-((column_1)%self.tabstop));
                                        count_1 += width
                                        column_1 += width
                                        offset_1 += 1
                                    else:
                                        count_1 += 1
                                        column_1 += 1
                                        offset_1 += 1
                                else:
                                    break

                            if offset_1 + 1 <= buf_eof and buf[offset_1+0] == ':':
                                offset_1 += 1
                                column_1 += 1
                            else:
                                offset_1 = -1
                                break

                            count_1 = 0
                            while offset_1 < buf_eof:
                                codepoint = buf[offset_1]
                                if codepoint in ' \t\r\n':
                                    if codepoint == '\t':
                                        if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-((column_1)%self.tabstop));
                                        count_1 += width
                                        column_1 += width
                                        offset_1 += 1
                                    else:
                                        count_1 += 1
                                        column_1 += 1
                                        offset_1 += 1
                                else:
                                    break

                            offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_json_value(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                            if offset_1 == -1: break


                            break
                        if offset_1 == -1:
                            break
                        value_2.name = 'pair'
                        value_2.end = offset_1
                        value_2.end_column = column_1
                        value_2.value = None
                        children_2.append(value_2)

                        count_1 = 0
                        while offset_1 < buf_eof:
                            codepoint = buf[offset_1]
                            if codepoint in ' \t\r\n':
                                if codepoint == '\t':
                                    if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                        width = partial_tab_width_1
                                    else:
                                        width  = (self.tabstop-((column_1)%self.tabstop));
                                    count_1 += width
                                    column_1 += width
                                    offset_1 += 1
                                else:
                                    count_1 += 1
                                    column_1 += 1
                                    offset_1 += 1
                            else:
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
                                if offset_2 + 1 <= buf_eof and buf[offset_2+0] == ',':
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

                                count_2 = 0
                                while offset_2 < buf_eof:
                                    codepoint = buf[offset_2]
                                    if codepoint in ' \t\r\n':
                                        if codepoint == '\t':
                                            if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-((column_2)%self.tabstop));
                                            count_2 += width
                                            column_2 += width
                                            offset_2 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
                                            offset_2 += 1
                                    else:
                                        break

                                children_4 = []
                                value_6 = Node(None, offset_2, offset_2, column_2, column_2, children_4, None)
                                while True: # start capture
                                    if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '"':
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    children_5 = None
                                    value_7 = Node(None, offset_2, offset_2, column_2, column_2, children_5, None)
                                    while True: # start capture
                                        count_2 = 0
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
                                                        if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'u':
                                                            offset_4 += 2
                                                            column_4 += 2
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
                                                        if offset_4 == buf_eof:
                                                            offset_4 = -1
                                                            break

                                                        codepoint = (buf[offset_4])

                                                        if codepoint == 92:
                                                            offset_4 = -1
                                                            break
                                                        elif codepoint == 34:
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
                                            count_2 += 1
                                        if offset_2 == -1:
                                            break
                                        value_8 = count_2



                                        break
                                    if offset_2 == -1:
                                        break
                                    value_7.name = 'string'
                                    value_7.end = offset_2
                                    value_7.end_column = column_2
                                    value_7.value = None
                                    children_4.append(value_7)

                                    if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '"':
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break


                                    count_2 = 0
                                    while offset_2 < buf_eof:
                                        codepoint = buf[offset_2]
                                        if codepoint in ' \t\r\n':
                                            if codepoint == '\t':
                                                if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                    width = partial_tab_width_2
                                                else:
                                                    width  = (self.tabstop-((column_2)%self.tabstop));
                                                count_2 += width
                                                column_2 += width
                                                offset_2 += 1
                                            else:
                                                count_2 += 1
                                                column_2 += 1
                                                offset_2 += 1
                                        else:
                                            break

                                    if offset_2 + 1 <= buf_eof and buf[offset_2+0] == ':':
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    count_2 = 0
                                    while offset_2 < buf_eof:
                                        codepoint = buf[offset_2]
                                        if codepoint in ' \t\r\n':
                                            if codepoint == '\t':
                                                if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                    width = partial_tab_width_2
                                                else:
                                                    width  = (self.tabstop-((column_2)%self.tabstop));
                                                count_2 += width
                                                column_2 += width
                                                offset_2 += 1
                                            else:
                                                count_2 += 1
                                                column_2 += 1
                                                offset_2 += 1
                                        else:
                                            break

                                    offset_2, column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_json_value(buf, buf_start, buf_eof, offset_2, column_2, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                    if offset_2 == -1: break


                                    break
                                if offset_2 == -1:
                                    break
                                value_6.name = 'pair'
                                value_6.end = offset_2
                                value_6.end_column = column_2
                                value_6.value = None
                                children_3.append(value_6)

                                count_2 = 0
                                while offset_2 < buf_eof:
                                    codepoint = buf[offset_2]
                                    if codepoint in ' \t\r\n':
                                        if codepoint == '\t':
                                            if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-((column_2)%self.tabstop));
                                            count_2 += width
                                            column_2 += width
                                            offset_2 += 1
                                        else:
                                            count_2 += 1
                                            column_2 += 1
                                            offset_2 += 1
                                    else:
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
                        value_5 = count_1

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

            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '}':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0
