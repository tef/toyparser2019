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

    cdef (int, int, int, int) parse_yaml_literal(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1
        cdef int column_1

        cdef list children_1

        cdef list indent_column_1
        cdef int partial_tab_offset_1
        cdef int partial_tab_width_1
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_list_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_object_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_string_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_number_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_true_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_false_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_null_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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

    cdef (int, int, int, int) parse_true_literal(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint



        cdef list children_1




        while True: # note: return at end of loop
            children_1 = []
            value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
            while True: # start capture
                if offset_0 + 4 <= buf_eof and buf[offset_0+0] == 't' and buf[offset_0+1] == 'r' and buf[offset_0+2] == 'u' and buf[offset_0+3] == 'e':
                    offset_0 += 4
                    column_0 += 4
                else:
                    offset_0 = -1
                    break

                break
            if offset_0 == -1:
                break
            value_0.name = 'bool'
            value_0.end = offset_0
            value_0.end_column = column_0
            value_0.value = None
            children_0.append(value_0)

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    cdef (int, int, int, int) parse_false_literal(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint



        cdef list children_1




        while True: # note: return at end of loop
            children_1 = []
            value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
            while True: # start capture
                if offset_0 + 5 <= buf_eof and buf[offset_0+0] == 'f' and buf[offset_0+1] == 'a' and buf[offset_0+2] == 'l' and buf[offset_0+3] == 's' and buf[offset_0+4] == 'e':
                    offset_0 += 5
                    column_0 += 5
                else:
                    offset_0 = -1
                    break

                break
            if offset_0 == -1:
                break
            value_0.name = 'bool'
            value_0.end = offset_0
            value_0.end_column = column_0
            value_0.value = None
            children_0.append(value_0)

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    cdef (int, int, int, int) parse_null_literal(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint



        cdef list children_1




        while True: # note: return at end of loop
            children_1 = []
            value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
            while True: # start capture
                if offset_0 + 4 <= buf_eof and buf[offset_0+0] == 'n' and buf[offset_0+1] == 'u' and buf[offset_0+2] == 'l' and buf[offset_0+3] == 'l':
                    offset_0 += 4
                    column_0 += 4
                else:
                    offset_0 = -1
                    break

                break
            if offset_0 == -1:
                break
            value_0.name = 'null'
            value_0.end = offset_0
            value_0.end_column = column_0
            value_0.value = None
            children_0.append(value_0)

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    cdef (int, int, int, int) parse_identifier(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2
        cdef int column_1, column_2

        cdef list children_1, children_2, children_3
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
                                if offset_2 == buf_eof:
                                    offset_2 = -1
                                    break

                                codepoint = (buf[offset_2])

                                if 97 <= codepoint <= 122:
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
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_1 = offset_2
                            column_1 = column_2
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            count_0 += 1
                        if count_0 < 1:
                        #    print('min exit', offset_1)
                            offset_1 = -1
                            break
                        if offset_1 == -1:
                            break
                        value_1 = count_0


                        break
                    if offset_1 == -1:
                        break
                    value_0.name = 'identifier'
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_string_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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

    cdef (int, int, int, int) parse_number_literal(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2, offset_3
        cdef int column_1, column_2, column_3

        cdef list children_1, children_2, children_3, children_4
        cdef int count_1, count_2, count_3
        cdef list indent_column_1, indent_column_2, indent_column_3
        cdef int partial_tab_offset_1, partial_tab_offset_2, partial_tab_offset_3
        cdef int partial_tab_width_1, partial_tab_width_2, partial_tab_width_3
        while True: # note: return at end of loop
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
                        if offset_1 == buf_eof:
                            offset_1 = -1
                            break

                        codepoint = (buf[offset_1])

                        if codepoint == 45:
                            offset_1 += 1
                            column_1 += 1
                        elif codepoint == 43:
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


                count_0 = 0
                while True:
                    offset_1 = offset_0
                    column_1 = column_0
                    indent_column_1 = list(indent_column_0)
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        #print('entry rep rule', offset_0, offset_1)
                        if offset_1 == buf_eof:
                            offset_1 = -1
                            break

                        codepoint = (buf[offset_1])

                        if 48 <= codepoint <= 57:
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
                    if children_2 is not None and children_2 is not None:
                        children_1.extend(children_2)
                    offset_0 = offset_1
                    column_0 = column_1
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    count_0 += 1
                if count_0 < 1:
                #    print('min exit', offset_0)
                    offset_0 = -1
                    break
                if offset_0 == -1:
                    break
                value_2 = count_0


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
                        if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '.':
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
                            children_3 = [] if children_2 is not None else None
                            while True:
                                #print('entry rep rule', offset_1, offset_2)
                                if offset_2 == buf_eof:
                                    offset_2 = -1
                                    break

                                codepoint = (buf[offset_2])

                                if 48 <= codepoint <= 57:
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
                        value_4 = count_1

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
                value_3 = count_0


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
                        if offset_1 + 1 <= buf_eof and buf[offset_1+0] == 'e':
                            offset_1 += 1
                            column_1 += 1
                        elif offset_1 + 1 <= buf_eof and buf[offset_1+0] == 'E':
                            offset_1 += 1
                            column_1 += 1
                        else:
                            offset_1 = -1
                            break

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
                                if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '+':
                                    offset_2 += 1
                                    column_2 += 1
                                elif offset_2 + 1 <= buf_eof and buf[offset_2+0] == '-':
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
                                    count_2 += 1
                                if offset_2 == -1:
                                    break
                                value_7 = count_2

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
                        value_6 = count_1

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
                value_5 = count_0


                break
            if offset_0 == -1:
                break
            value_0.name = 'number'
            value_0.end = offset_0
            value_0.end_column = column_0
            value_0.value = None
            children_0.append(value_0)

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    cdef (int, int, int, int) parse_string_literal(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2
        cdef int column_1, column_2

        cdef list children_1, children_2, children_3
        cdef int count_1
        cdef list indent_column_1, indent_column_2
        cdef int partial_tab_offset_1, partial_tab_offset_2
        cdef int partial_tab_width_1, partial_tab_width_2
        while True: # note: return at end of loop
            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '"':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break

            children_1 = []
            value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
            while True: # start capture
                count_0 = 0
                while True:
                    offset_1 = offset_0
                    column_1 = column_0
                    indent_column_1 = list(indent_column_0)
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        #print('entry rep rule', offset_0, offset_1)
                        while True: # start choice
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                if offset_2 + 2 <= buf_eof and buf[offset_2+0] == '\\' and buf[offset_2+1] == 'u':
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
                                elif 97 <= codepoint <= 102:
                                    offset_2 += 1
                                    column_2 += 1
                                elif 65 <= codepoint <= 70:
                                    offset_2 += 1
                                    column_2 += 1
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
                                elif 97 <= codepoint <= 102:
                                    offset_2 += 1
                                    column_2 += 1
                                elif 65 <= codepoint <= 70:
                                    offset_2 += 1
                                    column_2 += 1
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
                                elif 97 <= codepoint <= 102:
                                    offset_2 += 1
                                    column_2 += 1
                                elif 65 <= codepoint <= 70:
                                    offset_2 += 1
                                    column_2 += 1
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
                                elif 97 <= codepoint <= 102:
                                    offset_2 += 1
                                    column_2 += 1
                                elif 65 <= codepoint <= 70:
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
                                if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '\\':
                                    offset_2 += 1
                                    column_2 += 1
                                else:
                                    offset_2 = -1
                                    break

                                if offset_2 == buf_eof:
                                    offset_2 = -1
                                    break

                                codepoint = (buf[offset_2])

                                if codepoint == 34:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 92:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 47:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 98:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 102:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 110:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 114:
                                    offset_2 += 1
                                    column_2 += 1
                                elif codepoint == 116:
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

                                if codepoint == 92:
                                    offset_2 = -1
                                    break
                                elif codepoint == 34:
                                    offset_2 = -1
                                    break
                                else:
                                    offset_2 += 1
                                    column_2 += 1


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
                if offset_0 == -1:
                    break
                value_1 = count_0


                break
            if offset_0 == -1:
                break
            value_0.name = 'string'
            value_0.end = offset_0
            value_0.end_column = column_0
            value_0.value = None
            children_0.append(value_0)

            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '"':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    cdef (int, int, int, int) parse_list_literal(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
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
                if codepoint == '\r' and offset_0 + 1 < buf_eof and buf[offset_0+1] == '\n':
                    offset_0 +=2
                    column_0 = 0
                    indent_column_0[:] = (0, )
                elif codepoint in '\n\r':
                    offset_0 +=1
                    column_0 = 0
                    indent_column_0[:] = (0, )
                    count_0 +=1
                elif codepoint in ' \t':
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
                        offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
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
                                    if codepoint == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                        offset_2 +=2
                                        column_2 = 0
                                        indent_column_2[:] = (0, )
                                    elif codepoint in '\n\r':
                                        offset_2 +=1
                                        column_2 = 0
                                        indent_column_2[:] = (0, )
                                        count_2 +=1
                                    elif codepoint in ' \t':
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
                                    if codepoint == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                        offset_2 +=2
                                        column_2 = 0
                                        indent_column_2[:] = (0, )
                                    elif codepoint in '\n\r':
                                        offset_2 +=1
                                        column_2 = 0
                                        indent_column_2[:] = (0, )
                                        count_2 +=1
                                    elif codepoint in ' \t':
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

                                offset_2, column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_yaml_literal(buf, buf_start, buf_eof, offset_2, column_2, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
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

                        count_1 = 0
                        while offset_1 < buf_eof:
                            codepoint = buf[offset_1]
                            if codepoint == '\r' and offset_1 + 1 < buf_eof and buf[offset_1+1] == '\n':
                                offset_1 +=2
                                column_1 = 0
                                indent_column_1[:] = (0, )
                            elif codepoint in '\n\r':
                                offset_1 +=1
                                column_1 = 0
                                indent_column_1[:] = (0, )
                                count_1 +=1
                            elif codepoint in ' \t':
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
                                while offset_2 < buf_eof:
                                    codepoint = buf[offset_2]
                                    if codepoint == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                        offset_2 +=2
                                        column_2 = 0
                                        indent_column_2[:] = (0, )
                                    elif codepoint in '\n\r':
                                        offset_2 +=1
                                        column_2 = 0
                                        indent_column_2[:] = (0, )
                                        count_2 +=1
                                    elif codepoint in ' \t':
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
                            break
                        if offset_1 == -1:
                            break
                        value_3 = count_1

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

    cdef (int, int, int, int) parse_object_literal(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2
        cdef int column_1, column_2

        cdef list children_1, children_2, children_3
        cdef int count_1, count_2
        cdef list indent_column_1, indent_column_2
        cdef int partial_tab_offset_1, partial_tab_offset_2
        cdef int partial_tab_width_1, partial_tab_width_2
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
                if codepoint == '\r' and offset_0 + 1 < buf_eof and buf[offset_0+1] == '\n':
                    offset_0 +=2
                    column_0 = 0
                    indent_column_0[:] = (0, )
                elif codepoint in '\n\r':
                    offset_0 +=1
                    column_0 = 0
                    indent_column_0[:] = (0, )
                    count_0 +=1
                elif codepoint in ' \t':
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
                        offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_string_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                        if offset_1 == -1: break


                        count_1 = 0
                        while offset_1 < buf_eof:
                            codepoint = buf[offset_1]
                            if codepoint in ' \t':
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
                            if codepoint == '\r' and offset_1 + 1 < buf_eof and buf[offset_1+1] == '\n':
                                offset_1 +=2
                                column_1 = 0
                                indent_column_1[:] = (0, )
                            elif codepoint in '\n\r':
                                offset_1 +=1
                                column_1 = 0
                                indent_column_1[:] = (0, )
                                count_1 +=1
                            elif codepoint in ' \t':
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

                        offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
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
                                    if codepoint == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                        offset_2 +=2
                                        column_2 = 0
                                        indent_column_2[:] = (0, )
                                    elif codepoint in '\n\r':
                                        offset_2 +=1
                                        column_2 = 0
                                        indent_column_2[:] = (0, )
                                        count_2 +=1
                                    elif codepoint in ' \t':
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
                                    if codepoint == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                        offset_2 +=2
                                        column_2 = 0
                                        indent_column_2[:] = (0, )
                                    elif codepoint in '\n\r':
                                        offset_2 +=1
                                        column_2 = 0
                                        indent_column_2[:] = (0, )
                                        count_2 +=1
                                    elif codepoint in ' \t':
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

                                offset_2, column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_string_literal(buf, buf_start, buf_eof, offset_2, column_2, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
                                if offset_2 == -1: break


                                count_2 = 0
                                while offset_2 < buf_eof:
                                    codepoint = buf[offset_2]
                                    if codepoint in ' \t':
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
                                    if codepoint == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                        offset_2 +=2
                                        column_2 = 0
                                        indent_column_2[:] = (0, )
                                    elif codepoint in '\n\r':
                                        offset_2 +=1
                                        column_2 = 0
                                        indent_column_2[:] = (0, )
                                        count_2 +=1
                                    elif codepoint in ' \t':
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

                                offset_2, column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_yaml_literal(buf, buf_start, buf_eof, offset_2, column_2, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
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

                        count_1 = 0
                        while offset_1 < buf_eof:
                            codepoint = buf[offset_1]
                            if codepoint == '\r' and offset_1 + 1 < buf_eof and buf[offset_1+1] == '\n':
                                offset_1 +=2
                                column_1 = 0
                                indent_column_1[:] = (0, )
                            elif codepoint in '\n\r':
                                offset_1 +=1
                                column_1 = 0
                                indent_column_1[:] = (0, )
                                count_1 +=1
                            elif codepoint in ' \t':
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
                                while offset_2 < buf_eof:
                                    codepoint = buf[offset_2]
                                    if codepoint == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                        offset_2 +=2
                                        column_2 = 0
                                        indent_column_2[:] = (0, )
                                    elif codepoint in '\n\r':
                                        offset_2 +=1
                                        column_2 = 0
                                        indent_column_2[:] = (0, )
                                        count_2 +=1
                                    elif codepoint in ' \t':
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
                            break
                        if offset_1 == -1:
                            break
                        value_3 = count_1

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

    cdef (int, int, int, int) parse_yaml_eol(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2, offset_3
        cdef int column_1, column_2, column_3

        cdef list children_1, children_2, children_3
        cdef int count_1, count_2
        cdef list indent_column_1, indent_column_2, indent_column_3
        cdef int partial_tab_offset_1, partial_tab_offset_2, partial_tab_offset_3
        cdef int partial_tab_width_1, partial_tab_width_2, partial_tab_width_3
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
                    while True: # start choice
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = list(indent_column_1)
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            count_1 = 0
                            while offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
                                        if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                            width = partial_tab_width_2
                                        else:
                                            width  = (self.tabstop-((column_2)%self.tabstop));
                                        count_1 += width
                                        column_2 += width
                                        offset_2 += 1
                                    else:
                                        count_1 += 1
                                        column_2 += 1
                                        offset_2 += 1
                                else:
                                    break

                            if offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                    offset_2 +=2
                                    column_2 = 0
                                    indent_column_2[:] = (0, )
                                elif codepoint in '\n\r':
                                    offset_2 +=1
                                    column_2 = 0
                                    indent_column_2[:] = (0, )
                                else:
                                    offset_2 = -1
                                    break
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
                            count_1 = 0
                            while offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
                                        if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                            width = partial_tab_width_2
                                        else:
                                            width  = (self.tabstop-((column_2)%self.tabstop));
                                        count_1 += width
                                        column_2 += width
                                        offset_2 += 1
                                    else:
                                        count_1 += 1
                                        column_2 += 1
                                        offset_2 += 1
                                else:
                                    break

                            if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '#':
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
                                children_3 = [] if children_2 is not None else None
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
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                offset_2 = offset_3
                                column_2 = column_3
                                indent_column_2 = indent_column_3
                                partial_tab_offset_2 = partial_tab_offset_3
                                partial_tab_width_2 = partial_tab_width_3
                                count_1 += 1
                            if offset_2 == -1:
                                break
                            value_1 = count_1


                            if offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                    offset_2 +=2
                                    column_2 = 0
                                    indent_column_2[:] = (0, )
                                elif codepoint in '\n\r':
                                    offset_2 +=1
                                    column_2 = 0
                                    indent_column_2[:] = (0, )
                                else:
                                    offset_2 = -1
                                    break
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

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    cdef (int, int, int, int) parse_indented_list(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2, offset_3
        cdef int column_1, column_2

        cdef list children_1, children_2, children_3
        cdef int count_1
        cdef list indent_column_1, indent_column_2
        cdef int partial_tab_offset_1, partial_tab_offset_2
        cdef int partial_tab_width_1, partial_tab_width_2
        while True: # note: return at end of loop
            count_0 = column_0 - indent_column_0[len(indent_column_0)-1]
            # print(count_0, 'indent')
            def _indent(buf, buf_start, buf_eof, offset, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
                saw_tab, saw_not_tab = False, False
                start_column, start_offset = column, offset
                if count < 0: offset = -1
                while count > 0 and offset < buf_eof:
                    codepoint = buf[offset];
                    if codepoint in ' \t':
                        if not allow_mixed_indent:
                            if codepoint == '\t': saw_tab = True
                            else: saw_not_tab = True
                            if saw_tab and saw_not_tab:
                                 offset = -1; break
                        if codepoint != '\t':
                            column += 1
                            offset += 1
                            count -=1
                        else:
                            if offset == partial_tab_offset and partial_tab_width > 0:
                                width = partial_tab_width
                            else:
                                width  = (self.tabstop-((column)%self.tabstop));
                            if width <= count:
                                column += width
                                offset += 1
                                count -= width
                            else:
                                partial_tab_offset = offset
                                partial_tab_width = width-count
                                column += count
                                count -= width
                                break
                    elif codepoint == '\r' and offset_0 + 1 < buf_eof and buf[offset_0+1] == '\n':
                        break
                    elif codepoint in '\n\r':
                        break
                    else:
                        offset = -1
                        break
                return offset, column, partial_tab_offset, partial_tab_width
            prefix_0.append((_indent, None))
            indent_column_0.append(column_0)
            while True:
                children_1 = []
                value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
                while True: # start capture
                    if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '-':
                        offset_0 += 1
                        column_0 += 1
                    else:
                        offset_0 = -1
                        break

                    while True: # start choice
                        offset_1 = offset_0
                        column_1 = column_0
                        indent_column_1 = list(indent_column_0)
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            count_0 = 0
                            while offset_1 < buf_eof:
                                codepoint = buf[offset_1]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
                                        if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-((column_1)%self.tabstop));
                                        count_0 += width
                                        column_1 += width
                                        offset_1 += 1
                                    else:
                                        count_0 += 1
                                        column_1 += 1
                                        offset_1 += 1
                                else:
                                    break

                            offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_indented_value(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                            if offset_1 == -1: break



                            break
                        if offset_1 != -1:
                            offset_0 = offset_1
                            column_0 = column_1
                            indent_column_0 = indent_column_1
                            partial_tab_offset_0 = partial_tab_offset_1
                            partial_tab_width_0 = partial_tab_width_1
                            if children_2 is not None and children_2 is not None:
                                children_1.extend(children_2)
                            break
                        # end case
                        offset_1 = offset_0
                        column_1 = column_0
                        indent_column_1 = list(indent_column_0)
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                            if offset_1 == -1: break


                            if column_1 != 0:
                                offset_1 = -1
                                break
                            # print('start')
                            for indent, dedent in prefix_0:
                                # print(indent, dedent)
                                _children, _prefix = [], []
                                offset_2 = offset_1
                                offset_2, column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, buf_start, buf_eof, offset_2, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_2 == -1:
                                    offset_1 = -1
                                    break
                                offset_1 = offset_2
                                indent_column_1.append(column_1)
                            if offset_1 == -1:
                                break

                            count_0 = 0
                            while offset_1 < buf_eof:
                                codepoint = buf[offset_1]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
                                        if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-((column_1)%self.tabstop));
                                        count_0 += width
                                        column_1 += width
                                        offset_1 += 1
                                    else:
                                        count_0 += 1
                                        column_1 += 1
                                        offset_1 += 1
                                else:
                                    break
                            if count_0 < 1:
                                offset_1 = -1
                                break

                            offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_indented_value(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                            if offset_1 == -1: break



                            break
                        if offset_1 != -1:
                            offset_0 = offset_1
                            column_0 = column_1
                            indent_column_0 = indent_column_1
                            partial_tab_offset_0 = partial_tab_offset_1
                            partial_tab_width_0 = partial_tab_width_1
                            if children_2 is not None and children_2 is not None:
                                children_1.extend(children_2)
                            break
                        # end case
                        offset_0 = -1 # no more choices
                        break # end choice
                    if offset_0 == -1:
                        break

                    count_0 = 0
                    while True:
                        offset_1 = offset_0
                        column_1 = column_0
                        indent_column_1 = list(indent_column_0)
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True:
                            #print('entry rep rule', offset_0, offset_1)
                            offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                            if offset_1 == -1: break


                            if column_1 != 0:
                                offset_1 = -1
                                break
                            # print('start')
                            for indent, dedent in prefix_0:
                                # print(indent, dedent)
                                _children, _prefix = [], []
                                offset_2 = offset_1
                                offset_2, column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, buf_start, buf_eof, offset_2, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_2 == -1:
                                    offset_1 = -1
                                    break
                                offset_1 = offset_2
                                indent_column_1.append(column_1)
                            if offset_1 == -1:
                                break

                            if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '-':
                                offset_1 += 1
                                column_1 += 1
                            else:
                                offset_1 = -1
                                break

                            count_1 = 0
                            while offset_1 < buf_eof:
                                codepoint = buf[offset_1]
                                if codepoint in ' \t':
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
                            if count_1 < 1:
                                offset_1 = -1
                                break

                            while True: # start choice
                                offset_2 = offset_1
                                column_2 = column_1
                                indent_column_2 = list(indent_column_1)
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_3 = [] if children_2 is not None else None
                                while True: # case
                                    count_1 = 0
                                    while offset_2 < buf_eof:
                                        codepoint = buf[offset_2]
                                        if codepoint in ' \t':
                                            if codepoint == '\t':
                                                if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                    width = partial_tab_width_2
                                                else:
                                                    width  = (self.tabstop-((column_2)%self.tabstop));
                                                count_1 += width
                                                column_2 += width
                                                offset_2 += 1
                                            else:
                                                count_1 += 1
                                                column_2 += 1
                                                offset_2 += 1
                                        else:
                                            break

                                    offset_2, column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_indented_value(buf, buf_start, buf_eof, offset_2, column_2, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
                                    if offset_2 == -1: break



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
                                    offset_2, column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_2, column_2, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
                                    if offset_2 == -1: break


                                    if column_2 != 0:
                                        offset_2 = -1
                                        break
                                    # print('start')
                                    for indent, dedent in prefix_0:
                                        # print(indent, dedent)
                                        _children, _prefix = [], []
                                        offset_3 = offset_2
                                        offset_3, column_2, partial_tab_offset_2, partial_tab_width_2 = indent(buf, buf_start, buf_eof, offset_3, column_2, indent_column_2, _prefix, _children, partial_tab_offset_2, partial_tab_width_2)
                                        if _prefix or _children:
                                           raise Exception('bar')
                                        if offset_3 == -1:
                                            offset_2 = -1
                                            break
                                        offset_2 = offset_3
                                        indent_column_2.append(column_2)
                                    if offset_2 == -1:
                                        break

                                    count_1 = 0
                                    while offset_2 < buf_eof:
                                        codepoint = buf[offset_2]
                                        if codepoint in ' \t':
                                            if codepoint == '\t':
                                                if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                    width = partial_tab_width_2
                                                else:
                                                    width  = (self.tabstop-((column_2)%self.tabstop));
                                                count_1 += width
                                                column_2 += width
                                                offset_2 += 1
                                            else:
                                                count_1 += 1
                                                column_2 += 1
                                                offset_2 += 1
                                        else:
                                            break

                                    offset_2, column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_indented_value(buf, buf_start, buf_eof, offset_2, column_2, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
                                    if offset_2 == -1: break



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

                break
            prefix_0.pop()
            if len(indent_column_0) > 1: indent_column_0.pop()
            if offset_0 == -1: break

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    cdef (int, int, int, int) parse_indented_object(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1, offset_2, offset_3
        cdef int column_1, column_2

        cdef list children_1, children_2, children_3, children_4
        cdef int count_1
        cdef list indent_column_1, indent_column_2
        cdef int partial_tab_offset_1, partial_tab_offset_2
        cdef int partial_tab_width_1, partial_tab_width_2
        while True: # note: return at end of loop
            count_0 = column_0 - indent_column_0[len(indent_column_0)-1]
            # print(count_0, 'indent')
            def _indent(buf, buf_start, buf_eof, offset, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
                saw_tab, saw_not_tab = False, False
                start_column, start_offset = column, offset
                if count < 0: offset = -1
                while count > 0 and offset < buf_eof:
                    codepoint = buf[offset];
                    if codepoint in ' \t':
                        if not allow_mixed_indent:
                            if codepoint == '\t': saw_tab = True
                            else: saw_not_tab = True
                            if saw_tab and saw_not_tab:
                                 offset = -1; break
                        if codepoint != '\t':
                            column += 1
                            offset += 1
                            count -=1
                        else:
                            if offset == partial_tab_offset and partial_tab_width > 0:
                                width = partial_tab_width
                            else:
                                width  = (self.tabstop-((column)%self.tabstop));
                            if width <= count:
                                column += width
                                offset += 1
                                count -= width
                            else:
                                partial_tab_offset = offset
                                partial_tab_width = width-count
                                column += count
                                count -= width
                                break
                    elif codepoint == '\r' and offset_0 + 1 < buf_eof and buf[offset_0+1] == '\n':
                        break
                    elif codepoint in '\n\r':
                        break
                    else:
                        offset = -1
                        break
                return offset, column, partial_tab_offset, partial_tab_width
            prefix_0.append((_indent, None))
            indent_column_0.append(column_0)
            while True:
                children_1 = []
                value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
                while True: # start capture
                    children_2 = []
                    value_1 = Node(None, offset_0, offset_0, column_0, column_0, children_2, None)
                    while True: # start capture
                        offset_0, column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_identifier(buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_2, partial_tab_offset_0, partial_tab_width_0)
                        if offset_0 == -1: break


                        count_0 = 0
                        while offset_0 < buf_eof:
                            codepoint = buf[offset_0]
                            if codepoint in ' \t':
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

                        if offset_0 + 1 <= buf_eof and buf[offset_0+0] == ':':
                            offset_0 += 1
                            column_0 += 1
                        else:
                            offset_0 = -1
                            break

                        while True: # start choice
                            offset_1 = offset_0
                            column_1 = column_0
                            indent_column_1 = list(indent_column_0)
                            partial_tab_offset_1 = partial_tab_offset_0
                            partial_tab_width_1 = partial_tab_width_0
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                                if offset_1 == -1: break


                                if column_1 != 0:
                                    offset_1 = -1
                                    break
                                # print('start')
                                for indent, dedent in prefix_0:
                                    # print(indent, dedent)
                                    _children, _prefix = [], []
                                    offset_2 = offset_1
                                    offset_2, column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, buf_start, buf_eof, offset_2, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                    if _prefix or _children:
                                       raise Exception('bar')
                                    if offset_2 == -1:
                                        offset_1 = -1
                                        break
                                    offset_1 = offset_2
                                    indent_column_1.append(column_1)
                                if offset_1 == -1:
                                    break

                                count_0 = 0
                                while offset_1 < buf_eof:
                                    codepoint = buf[offset_1]
                                    if codepoint in ' \t':
                                        if codepoint == '\t':
                                            if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                                width = partial_tab_width_1
                                            else:
                                                width  = (self.tabstop-((column_1)%self.tabstop));
                                            count_0 += width
                                            column_1 += width
                                            offset_1 += 1
                                        else:
                                            count_0 += 1
                                            column_1 += 1
                                            offset_1 += 1
                                    else:
                                        break
                                if count_0 < 1:
                                    offset_1 = -1
                                    break

                                offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_indented_value(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                                if offset_1 == -1: break



                                break
                            if offset_1 != -1:
                                offset_0 = offset_1
                                column_0 = column_1
                                indent_column_0 = indent_column_1
                                partial_tab_offset_0 = partial_tab_offset_1
                                partial_tab_width_0 = partial_tab_width_1
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_1 = offset_0
                            column_1 = column_0
                            indent_column_1 = list(indent_column_0)
                            partial_tab_offset_1 = partial_tab_offset_0
                            partial_tab_width_1 = partial_tab_width_0
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                count_0 = 0
                                while offset_1 < buf_eof:
                                    codepoint = buf[offset_1]
                                    if codepoint in ' \t':
                                        if codepoint == '\t':
                                            if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                                width = partial_tab_width_1
                                            else:
                                                width  = (self.tabstop-((column_1)%self.tabstop));
                                            count_0 += width
                                            column_1 += width
                                            offset_1 += 1
                                        else:
                                            count_0 += 1
                                            column_1 += 1
                                            offset_1 += 1
                                    else:
                                        break

                                offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_indented_value(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                                if offset_1 == -1: break



                                break
                            if offset_1 != -1:
                                offset_0 = offset_1
                                column_0 = column_1
                                indent_column_0 = indent_column_1
                                partial_tab_offset_0 = partial_tab_offset_1
                                partial_tab_width_0 = partial_tab_width_1
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_0 = -1 # no more choices
                            break # end choice
                        if offset_0 == -1:
                            break

                        break
                    if offset_0 == -1:
                        break
                    value_1.name = 'pair'
                    value_1.end = offset_0
                    value_1.end_column = column_0
                    value_1.value = None
                    children_1.append(value_1)

                    count_0 = 0
                    while True:
                        offset_1 = offset_0
                        column_1 = column_0
                        indent_column_1 = list(indent_column_0)
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True:
                            #print('entry rep rule', offset_0, offset_1)
                            children_3 = []
                            value_3 = Node(None, offset_1, offset_1, column_1, column_1, children_3, None)
                            while True: # start capture
                                offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                                if offset_1 == -1: break


                                if column_1 != 0:
                                    offset_1 = -1
                                    break
                                # print('start')
                                for indent, dedent in prefix_0:
                                    # print(indent, dedent)
                                    _children, _prefix = [], []
                                    offset_2 = offset_1
                                    offset_2, column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, buf_start, buf_eof, offset_2, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                    if _prefix or _children:
                                       raise Exception('bar')
                                    if offset_2 == -1:
                                        offset_1 = -1
                                        break
                                    offset_1 = offset_2
                                    indent_column_1.append(column_1)
                                if offset_1 == -1:
                                    break

                                offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_identifier(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                                if offset_1 == -1: break


                                count_1 = 0
                                while offset_1 < buf_eof:
                                    codepoint = buf[offset_1]
                                    if codepoint in ' \t':
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

                                children_3.append(Node('value', offset_1, offset_1, column_1, column_1, (), 'a'))

                                while True: # start choice
                                    offset_2 = offset_1
                                    column_2 = column_1
                                    indent_column_2 = list(indent_column_1)
                                    partial_tab_offset_2 = partial_tab_offset_1
                                    partial_tab_width_2 = partial_tab_width_1
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        count_1 = 0
                                        while offset_2 < buf_eof:
                                            codepoint = buf[offset_2]
                                            if codepoint in ' \t':
                                                if codepoint == '\t':
                                                    if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                        width = partial_tab_width_2
                                                    else:
                                                        width  = (self.tabstop-((column_2)%self.tabstop));
                                                    count_1 += width
                                                    column_2 += width
                                                    offset_2 += 1
                                                else:
                                                    count_1 += 1
                                                    column_2 += 1
                                                    offset_2 += 1
                                            else:
                                                break

                                        offset_2, column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_indented_value(buf, buf_start, buf_eof, offset_2, column_2, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                        if offset_2 == -1: break



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
                                        offset_2, column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_2, column_2, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                        if offset_2 == -1: break


                                        if column_2 != 0:
                                            offset_2 = -1
                                            break
                                        # print('start')
                                        for indent, dedent in prefix_0:
                                            # print(indent, dedent)
                                            _children, _prefix = [], []
                                            offset_3 = offset_2
                                            offset_3, column_2, partial_tab_offset_2, partial_tab_width_2 = indent(buf, buf_start, buf_eof, offset_3, column_2, indent_column_2, _prefix, _children, partial_tab_offset_2, partial_tab_width_2)
                                            if _prefix or _children:
                                               raise Exception('bar')
                                            if offset_3 == -1:
                                                offset_2 = -1
                                                break
                                            offset_2 = offset_3
                                            indent_column_2.append(column_2)
                                        if offset_2 == -1:
                                            break

                                        count_1 = 0
                                        while offset_2 < buf_eof:
                                            codepoint = buf[offset_2]
                                            if codepoint in ' \t':
                                                if codepoint == '\t':
                                                    if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                        width = partial_tab_width_2
                                                    else:
                                                        width  = (self.tabstop-((column_2)%self.tabstop));
                                                    count_1 += width
                                                    column_2 += width
                                                    offset_2 += 1
                                                else:
                                                    count_1 += 1
                                                    column_2 += 1
                                                    offset_2 += 1
                                            else:
                                                break
                                        if count_1 < 1:
                                            offset_2 = -1
                                            break

                                        offset_2, column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_indented_value(buf, buf_start, buf_eof, offset_2, column_2, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                        if offset_2 == -1: break



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

                                break
                            if offset_1 == -1:
                                break
                            value_3.name = 'pair'
                            value_3.end = offset_1
                            value_3.end_column = column_1
                            value_3.value = None
                            children_2.append(value_3)

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
                    if offset_0 == -1:
                        break
                    value_2 = count_0

                    break
                if offset_0 == -1:
                    break
                value_0.name = 'object'
                value_0.end = offset_0
                value_0.end_column = column_0
                value_0.value = None
                children_0.append(value_0)

                break
            prefix_0.pop()
            if len(indent_column_0) > 1: indent_column_0.pop()
            if offset_0 == -1: break

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    cdef (int, int, int, int) parse_indented_value(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1
        cdef int column_1

        cdef list children_1

        cdef list indent_column_1
        cdef int partial_tab_offset_1
        cdef int partial_tab_width_1
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_indented_object(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_indented_list(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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

    cdef (int, int, int, int) parse_document(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):
        cdef Py_UCS4 codepoint
        cdef int offset_1
        cdef int column_1

        cdef list children_1
        cdef int count_1
        cdef list indent_column_1
        cdef int partial_tab_offset_1
        cdef int partial_tab_width_1
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
                    count_1 = 0
                    while offset_1 < buf_eof:
                        codepoint = buf[offset_1]
                        if codepoint in ' \t':
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

                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
                    if offset_1 == -1: break


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

            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_indented_object(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_indented_list(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_list_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_object_literal(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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

            count_0 = 0
            while offset_0 < buf_eof:
                codepoint = buf[offset_0]
                if codepoint in ' \t':
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
                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
                    if offset_1 == -1: break


                    count_1 = 0
                    while offset_1 < buf_eof:
                        codepoint = buf[offset_1]
                        if codepoint in ' \t':
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
                    if offset_1 < buf_eof:
                        codepoint = buf[offset_1]
                        if codepoint == '\r' and offset_1 + 1 < buf_eof and buf[offset_1+1] == '\n':
                            offset_1 +=2
                            column_1 = 0
                            indent_column_1[:] = (0, )
                        elif codepoint in '\n\r':
                            offset_1 +=1
                            column_1 = 0
                            indent_column_1[:] = (0, )
                        else:
                            offset_1 = -1
                            break

                    count_1 = 0
                    while offset_1 < buf_eof:
                        codepoint = buf[offset_1]
                        if codepoint in ' \t':
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
            value_2 = count_0


            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0
