# cython: language_level=3, bounds_check=False
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
    cdef dict builder, cache
    cdef int tabstop
    cdef int allow_mixed_indent

    def __init__(self, builder=None, tabstop=None, allow_mixed_indent=True):
         self.builder = builder
         self.tabstop = tabstop or 8
         self.cache = None
         self.allow_mixed_indent = allow_mixed_indent

    def parse(self, buf, offset=0, end=None, err=None):
        self.cache = dict()
        end = len(buf) if end is None else end
        line_start, indent_end, eof = offset, offset, end
        prefix, children = [], []
        new_offset, line_start, indent_end = self.parse_document(buf, offset, eof, line_start, indent_end, prefix, children)
        if children and new_offset == end: return children[-1]
        print('no', offset, new_offset, end, buf[new_offset:])
        if err is not None: raise err(buf, new_offset, 'no')

    cdef (int, int, int) parse_literal(self, str buf, int offset_0, int buf_eof, int line_start_0, int indent_end_0,  list prefix_0, list children_0):
        cdef Py_UCS4 chr
        cdef int offset_1
        cdef int line_start_1

        cdef list children_1

        cdef int indent_end_1
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, line_start_1, indent_end_1 = self.parse_list_literal(buf, offset_1, buf_eof, line_start_1, indent_end_1, prefix_0, children_1)
                    if offset_1 == -1: break


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    indent_end_0 = indent_end_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, line_start_1, indent_end_1 = self.parse_object_literal(buf, offset_1, buf_eof, line_start_1, indent_end_1, prefix_0, children_1)
                    if offset_1 == -1: break


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    indent_end_0 = indent_end_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, line_start_1, indent_end_1 = self.parse_string_literal(buf, offset_1, buf_eof, line_start_1, indent_end_1, prefix_0, children_1)
                    if offset_1 == -1: break


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    indent_end_0 = indent_end_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, line_start_1, indent_end_1 = self.parse_number_literal(buf, offset_1, buf_eof, line_start_1, indent_end_1, prefix_0, children_1)
                    if offset_1 == -1: break


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    indent_end_0 = indent_end_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, line_start_1, indent_end_1 = self.parse_true_literal(buf, offset_1, buf_eof, line_start_1, indent_end_1, prefix_0, children_1)
                    if offset_1 == -1: break


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    indent_end_0 = indent_end_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, line_start_1, indent_end_1 = self.parse_false_literal(buf, offset_1, buf_eof, line_start_1, indent_end_1, prefix_0, children_1)
                    if offset_1 == -1: break


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    indent_end_0 = indent_end_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, line_start_1, indent_end_1 = self.parse_null_literal(buf, offset_1, buf_eof, line_start_1, indent_end_1, prefix_0, children_1)
                    if offset_1 == -1: break


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    indent_end_0 = indent_end_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_0 = -1 # no more choices
                break # end choice
            if offset_0 == -1:
                break

            break
        return offset_0, line_start_0, indent_end_0

    cdef (int, int, int) parse_true_literal(self, str buf, int offset_0, int buf_eof, int line_start_0, int indent_end_0,  list prefix_0, list children_0):
        cdef Py_UCS4 chr
        cdef int offset_1


        cdef list children_1


        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                if offset_1 + 4 <= buf_eof and buf[offset_1+0] == 't' and buf[offset_1+1] == 'r' and buf[offset_1+2] == 'u' and buf[offset_1+3] == 'e':
                    offset_1 += 4
                else:
                    offset_1 = -1
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['bool'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = Node('bool', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            break
        return offset_0, line_start_0, indent_end_0

    cdef (int, int, int) parse_false_literal(self, str buf, int offset_0, int buf_eof, int line_start_0, int indent_end_0,  list prefix_0, list children_0):
        cdef Py_UCS4 chr
        cdef int offset_1


        cdef list children_1


        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                if offset_1 + 5 <= buf_eof and buf[offset_1+0] == 'f' and buf[offset_1+1] == 'a' and buf[offset_1+2] == 'l' and buf[offset_1+3] == 's' and buf[offset_1+4] == 'e':
                    offset_1 += 5
                else:
                    offset_1 = -1
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['bool'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = Node('bool', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            break
        return offset_0, line_start_0, indent_end_0

    cdef (int, int, int) parse_null_literal(self, str buf, int offset_0, int buf_eof, int line_start_0, int indent_end_0,  list prefix_0, list children_0):
        cdef Py_UCS4 chr
        cdef int offset_1


        cdef list children_1


        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                if offset_1 + 4 <= buf_eof and buf[offset_1+0] == 'n' and buf[offset_1+1] == 'u' and buf[offset_1+2] == 'l' and buf[offset_1+3] == 'l':
                    offset_1 += 4
                else:
                    offset_1 = -1
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['null'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = Node('null', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            break
        return offset_0, line_start_0, indent_end_0

    cdef (int, int, int) parse_identifier(self, str buf, int offset_0, int buf_eof, int line_start_0, int indent_end_0,  list prefix_0, list children_0):
        cdef Py_UCS4 chr
        cdef int offset_1, offset_2, offset_3
        cdef int line_start_1, line_start_2

        cdef list children_1, children_2, children_3
        cdef int count_1
        cdef int indent_end_1, indent_end_2
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            indent_end_2 = indent_end_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = (buf[offset_3])

                                if 97 <= chr <= 122:
                                    offset_3 += 1
                                elif 65 <= chr <= 90:
                                    offset_3 += 1
                                elif chr == 95:
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            indent_end_2 = indent_end_2
                            count_0 += 1
                        if count_0 < 1:
                            offset_2 = -1
                            break
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_0 = self.builder['identifier'](buf, offset_1, offset_2, children_2)
                    else:
                        value_0 = Node('identifier', offset_1, offset_2, children_2, None)
                    children_1.append(value_0)
                    offset_1 = offset_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    indent_end_0 = indent_end_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, line_start_1, indent_end_1 = self.parse_string_literal(buf, offset_1, buf_eof, line_start_1, indent_end_1, prefix_0, children_1)
                    if offset_1 == -1: break



                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    indent_end_0 = indent_end_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_0 = -1 # no more choices
                break # end choice
            if offset_0 == -1:
                break

            break
        return offset_0, line_start_0, indent_end_0

    cdef (int, int, int) parse_number_literal(self, str buf, int offset_0, int buf_eof, int line_start_0, int indent_end_0,  list prefix_0, list children_0):
        cdef Py_UCS4 chr
        cdef int offset_1, offset_2, offset_3, offset_4
        cdef int line_start_1, line_start_2, line_start_3

        cdef list children_1, children_2, children_3, children_4
        cdef int count_1, count_2, count_3
        cdef int indent_end_1, indent_end_2, indent_end_3
        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    indent_end_1 = indent_end_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break

                        chr = (buf[offset_2])

                        if chr == 45:
                            offset_2 += 1
                        elif chr == 43:
                            offset_2 += 1
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        break
                    if offset_1 == offset_2: break
                    if children_2 is not None and children_2 is not None:
                        children_1.extend(children_2)
                    offset_1 = offset_2
                    line_start_0 = line_start_1
                    indent_end_1 = indent_end_1
                    count_0 += 1
                    break
                if offset_1 == -1:
                    break

                count_0 = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    indent_end_1 = indent_end_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break

                        chr = (buf[offset_2])

                        if 48 <= chr <= 57:
                            offset_2 += 1
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        break
                    if offset_1 == offset_2: break
                    if children_2 is not None and children_2 is not None:
                        children_1.extend(children_2)
                    offset_1 = offset_2
                    line_start_0 = line_start_1
                    indent_end_1 = indent_end_1
                    count_0 += 1
                if count_0 < 1:
                    offset_1 = -1
                    break
                if offset_1 == -1:
                    break

                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    indent_end_1 = indent_end_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '.':
                            offset_2 += 1
                        else:
                            offset_2 = -1
                            break

                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            indent_end_2 = indent_end_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = (buf[offset_3])

                                if 48 <= chr <= 57:
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            indent_end_2 = indent_end_2
                            count_1 += 1
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        break
                    if offset_1 == offset_2: break
                    if children_2 is not None and children_2 is not None:
                        children_1.extend(children_2)
                    offset_1 = offset_2
                    line_start_0 = line_start_1
                    indent_end_1 = indent_end_1
                    count_0 += 1
                    break
                if offset_1 == -1:
                    break

                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    indent_end_1 = indent_end_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        if offset_2 + 1 <= buf_eof and buf[offset_2+0] == 'e':
                            offset_2 += 1
                        elif offset_2 + 1 <= buf_eof and buf[offset_2+0] == 'E':
                            offset_2 += 1
                        else:
                            offset_2 = -1
                            break

                        count_1 = 0
                        while count_1 < 1:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            indent_end_2 = indent_end_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '+':
                                    offset_3 += 1
                                elif offset_3 + 1 <= buf_eof and buf[offset_3+0] == '-':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    indent_end_3 = indent_end_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = (buf[offset_4])

                                        if 48 <= chr <= 57:
                                            offset_4 += 1
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
                                    line_start_2 = line_start_3
                                    indent_end_3 = indent_end_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            indent_end_2 = indent_end_2
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
                    line_start_0 = line_start_1
                    indent_end_1 = indent_end_1
                    count_0 += 1
                    break
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['number'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = Node('number', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            break
        return offset_0, line_start_0, indent_end_0

    cdef (int, int, int) parse_string_literal(self, str buf, int offset_0, int buf_eof, int line_start_0, int indent_end_0,  list prefix_0, list children_0):
        cdef Py_UCS4 chr
        cdef int offset_1, offset_2, offset_3
        cdef int line_start_1, line_start_2

        cdef list children_1, children_2, children_3
        cdef int count_1
        cdef int indent_end_1, indent_end_2
        while True: # note: return at end of loop
            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '"':
                offset_0 += 1
            else:
                offset_0 = -1
                break

            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    indent_end_1 = indent_end_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        while True: # start choice
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            indent_end_2 = indent_end_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                if offset_3 + 2 <= buf_eof and buf[offset_3+0] == '\\' and buf[offset_3+1] == 'u':
                                    offset_3 += 2
                                else:
                                    offset_3 = -1
                                    break

                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = (buf[offset_3])

                                if 48 <= chr <= 57:
                                    offset_3 += 1
                                elif 97 <= chr <= 102:
                                    offset_3 += 1
                                elif 65 <= chr <= 70:
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = (buf[offset_3])

                                if 48 <= chr <= 57:
                                    offset_3 += 1
                                elif 97 <= chr <= 102:
                                    offset_3 += 1
                                elif 65 <= chr <= 70:
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = (buf[offset_3])

                                if 48 <= chr <= 57:
                                    offset_3 += 1
                                elif 97 <= chr <= 102:
                                    offset_3 += 1
                                elif 65 <= chr <= 70:
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = (buf[offset_3])

                                if 48 <= chr <= 57:
                                    offset_3 += 1
                                elif 97 <= chr <= 102:
                                    offset_3 += 1
                                elif 65 <= chr <= 70:
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break


                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                line_start_1 = line_start_2
                                indent_end_1 = indent_end_2
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            indent_end_2 = indent_end_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '\\':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = (buf[offset_3])

                                if chr == 34:
                                    offset_3 += 1
                                elif chr == 92:
                                    offset_3 += 1
                                elif chr == 47:
                                    offset_3 += 1
                                elif chr == 98:
                                    offset_3 += 1
                                elif chr == 102:
                                    offset_3 += 1
                                elif chr == 110:
                                    offset_3 += 1
                                elif chr == 114:
                                    offset_3 += 1
                                elif chr == 116:
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break


                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                line_start_1 = line_start_2
                                indent_end_1 = indent_end_2
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            indent_end_2 = indent_end_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = (buf[offset_3])

                                if chr == 92:
                                    offset_3 = -1
                                    break
                                elif chr == 34:
                                    offset_3 = -1
                                    break
                                else:
                                    offset_3 += 1


                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                line_start_1 = line_start_2
                                indent_end_1 = indent_end_2
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
                        break
                    if offset_1 == offset_2: break
                    if children_2 is not None and children_2 is not None:
                        children_1.extend(children_2)
                    offset_1 = offset_2
                    line_start_0 = line_start_1
                    indent_end_1 = indent_end_1
                    count_0 += 1
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['string'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = Node('string', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '"':
                offset_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, line_start_0, indent_end_0

    cdef (int, int, int) parse_list_literal(self, str buf, int offset_0, int buf_eof, int line_start_0, int indent_end_0,  list prefix_0, list children_0):
        cdef Py_UCS4 chr
        cdef int offset_1, offset_2, offset_3
        cdef int line_start_1, line_start_2

        cdef list children_1, children_2, children_3
        cdef int count_1, count_2
        cdef int indent_end_1, indent_end_2
        while True: # note: return at end of loop
            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '[':
                offset_0 += 1
            else:
                offset_0 = -1
                break

            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr == '\r' and offset_0 + 1 < buf_eof and buf[offset_0+1] == '\n':
                    offset_0 +=2
                    line_start_0 = offset_0
                    indent_end_0 = offset_0
                elif chr in '\n\r':
                    offset_0 +=1
                    line_start_0 = offset_0
                    indent_end_0 = offset_0
                    count_0 +=1
                elif chr in ' \t':
                    count_0 += (self.tabstop-(offset_0-line_start_0)%self.tabstop) if chr == '	' else 1
                    offset_0 +=1
                else:
                    break

            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    indent_end_1 = indent_end_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        offset_2, line_start_1, indent_end_1 = self.parse_literal(buf, offset_2, buf_eof, line_start_1, indent_end_1, prefix_0, children_2)
                        if offset_2 == -1: break


                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            indent_end_2 = indent_end_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        line_start_2 = offset_3
                                        indent_end_2 = offset_3
                                    elif chr in '\n\r':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                        indent_end_2 = offset_3
                                        count_2 +=1
                                    elif chr in ' \t':
                                        count_2 += (self.tabstop-(offset_3-line_start_2)%self.tabstop) if chr == '	' else 1
                                        offset_3 +=1
                                    else:
                                        break

                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == ',':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        line_start_2 = offset_3
                                        indent_end_2 = offset_3
                                    elif chr in '\n\r':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                        indent_end_2 = offset_3
                                        count_2 +=1
                                    elif chr in ' \t':
                                        count_2 += (self.tabstop-(offset_3-line_start_2)%self.tabstop) if chr == '	' else 1
                                        offset_3 +=1
                                    else:
                                        break

                                offset_3, line_start_2, indent_end_2 = self.parse_literal(buf, offset_3, buf_eof, line_start_2, indent_end_2, prefix_0, children_3)
                                if offset_3 == -1: break


                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            indent_end_2 = indent_end_2
                            count_1 += 1
                        if offset_2 == -1:
                            break

                        count_1 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                offset_2 +=2
                                line_start_1 = offset_2
                                indent_end_1 = offset_2
                            elif chr in '\n\r':
                                offset_2 +=1
                                line_start_1 = offset_2
                                indent_end_1 = offset_2
                                count_1 +=1
                            elif chr in ' \t':
                                count_1 += (self.tabstop-(offset_2-line_start_1)%self.tabstop) if chr == '	' else 1
                                offset_2 +=1
                            else:
                                break

                        count_1 = 0
                        while count_1 < 1:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            indent_end_2 = indent_end_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == ',':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        line_start_2 = offset_3
                                        indent_end_2 = offset_3
                                    elif chr in '\n\r':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                        indent_end_2 = offset_3
                                        count_2 +=1
                                    elif chr in ' \t':
                                        count_2 += (self.tabstop-(offset_3-line_start_2)%self.tabstop) if chr == '	' else 1
                                        offset_3 +=1
                                    else:
                                        break

                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            indent_end_2 = indent_end_2
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
                    line_start_0 = line_start_1
                    indent_end_1 = indent_end_1
                    count_0 += 1
                    break
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['list'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = Node('list', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == ']':
                offset_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, line_start_0, indent_end_0

    cdef (int, int, int) parse_object_literal(self, str buf, int offset_0, int buf_eof, int line_start_0, int indent_end_0,  list prefix_0, list children_0):
        cdef Py_UCS4 chr
        cdef int offset_1, offset_2, offset_3
        cdef int line_start_1, line_start_2

        cdef list children_1, children_2, children_3
        cdef int count_1, count_2
        cdef int indent_end_1, indent_end_2
        while True: # note: return at end of loop
            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '{':
                offset_0 += 1
            else:
                offset_0 = -1
                break

            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr == '\r' and offset_0 + 1 < buf_eof and buf[offset_0+1] == '\n':
                    offset_0 +=2
                    line_start_0 = offset_0
                    indent_end_0 = offset_0
                elif chr in '\n\r':
                    offset_0 +=1
                    line_start_0 = offset_0
                    indent_end_0 = offset_0
                    count_0 +=1
                elif chr in ' \t':
                    count_0 += (self.tabstop-(offset_0-line_start_0)%self.tabstop) if chr == '	' else 1
                    offset_0 +=1
                else:
                    break

            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    indent_end_1 = indent_end_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        offset_2, line_start_1, indent_end_1 = self.parse_string_literal(buf, offset_2, buf_eof, line_start_1, indent_end_1, prefix_0, children_2)
                        if offset_2 == -1: break


                        count_1 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t':
                                offset_2 +=1
                                count_1 += (self.tabstop-(offset_2-line_start_1)%self.tabstop) if chr == '	' else 1
                            else:
                                break

                        if offset_2 + 1 <= buf_eof and buf[offset_2+0] == ':':
                            offset_2 += 1
                        else:
                            offset_2 = -1
                            break

                        count_1 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                offset_2 +=2
                                line_start_1 = offset_2
                                indent_end_1 = offset_2
                            elif chr in '\n\r':
                                offset_2 +=1
                                line_start_1 = offset_2
                                indent_end_1 = offset_2
                                count_1 +=1
                            elif chr in ' \t':
                                count_1 += (self.tabstop-(offset_2-line_start_1)%self.tabstop) if chr == '	' else 1
                                offset_2 +=1
                            else:
                                break

                        offset_2, line_start_1, indent_end_1 = self.parse_literal(buf, offset_2, buf_eof, line_start_1, indent_end_1, prefix_0, children_2)
                        if offset_2 == -1: break


                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            indent_end_2 = indent_end_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        line_start_2 = offset_3
                                        indent_end_2 = offset_3
                                    elif chr in '\n\r':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                        indent_end_2 = offset_3
                                        count_2 +=1
                                    elif chr in ' \t':
                                        count_2 += (self.tabstop-(offset_3-line_start_2)%self.tabstop) if chr == '	' else 1
                                        offset_3 +=1
                                    else:
                                        break

                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == ',':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        line_start_2 = offset_3
                                        indent_end_2 = offset_3
                                    elif chr in '\n\r':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                        indent_end_2 = offset_3
                                        count_2 +=1
                                    elif chr in ' \t':
                                        count_2 += (self.tabstop-(offset_3-line_start_2)%self.tabstop) if chr == '	' else 1
                                        offset_3 +=1
                                    else:
                                        break

                                offset_3, line_start_2, indent_end_2 = self.parse_string_literal(buf, offset_3, buf_eof, line_start_2, indent_end_2, prefix_0, children_3)
                                if offset_3 == -1: break


                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        offset_3 +=1
                                        count_2 += (self.tabstop-(offset_3-line_start_2)%self.tabstop) if chr == '	' else 1
                                    else:
                                        break

                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == ':':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        line_start_2 = offset_3
                                        indent_end_2 = offset_3
                                    elif chr in '\n\r':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                        indent_end_2 = offset_3
                                        count_2 +=1
                                    elif chr in ' \t':
                                        count_2 += (self.tabstop-(offset_3-line_start_2)%self.tabstop) if chr == '	' else 1
                                        offset_3 +=1
                                    else:
                                        break

                                offset_3, line_start_2, indent_end_2 = self.parse_literal(buf, offset_3, buf_eof, line_start_2, indent_end_2, prefix_0, children_3)
                                if offset_3 == -1: break


                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            indent_end_2 = indent_end_2
                            count_1 += 1
                        if offset_2 == -1:
                            break

                        count_1 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                offset_2 +=2
                                line_start_1 = offset_2
                                indent_end_1 = offset_2
                            elif chr in '\n\r':
                                offset_2 +=1
                                line_start_1 = offset_2
                                indent_end_1 = offset_2
                                count_1 +=1
                            elif chr in ' \t':
                                count_1 += (self.tabstop-(offset_2-line_start_1)%self.tabstop) if chr == '	' else 1
                                offset_2 +=1
                            else:
                                break

                        count_1 = 0
                        while count_1 < 1:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            indent_end_2 = indent_end_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == ',':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        line_start_2 = offset_3
                                        indent_end_2 = offset_3
                                    elif chr in '\n\r':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                        indent_end_2 = offset_3
                                        count_2 +=1
                                    elif chr in ' \t':
                                        count_2 += (self.tabstop-(offset_3-line_start_2)%self.tabstop) if chr == '	' else 1
                                        offset_3 +=1
                                    else:
                                        break

                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            indent_end_2 = indent_end_2
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
                    line_start_0 = line_start_1
                    indent_end_1 = indent_end_1
                    count_0 += 1
                    break
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['object'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = Node('object', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '}':
                offset_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, line_start_0, indent_end_0

    cdef (int, int, int) parse_yaml_eol(self, str buf, int offset_0, int buf_eof, int line_start_0, int indent_end_0,  list prefix_0, list children_0):
        cdef Py_UCS4 chr
        cdef int offset_1, offset_2, offset_3
        cdef int line_start_1, line_start_2, line_start_3

        cdef list children_1, children_2, children_3
        cdef int count_1, count_2
        cdef int indent_end_1, indent_end_2, indent_end_3
        while True: # note: return at end of loop
            count_0 = 0
            while True:
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True:
                    while True: # start choice
                        offset_2 = offset_1
                        line_start_2 = line_start_1
                        indent_end_2 = indent_end_1
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            count_1 = 0
                            while offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr in ' \t':
                                    offset_2 +=1
                                    count_1 += (self.tabstop-(offset_2-line_start_2)%self.tabstop) if chr == '	' else 1
                                else:
                                    break

                            if offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                    offset_2 +=2
                                    line_start_2 = offset_2
                                    indent_end_2 = offset_2
                                elif chr in '\n\r':
                                    offset_2 +=1
                                    line_start_2 = offset_2
                                    indent_end_2 = offset_2
                                else:
                                    offset_2 = -1
                                    break
                            else:
                                offset_2 = -1
                                break


                            break
                        if offset_2 != -1:
                            offset_1 = offset_2
                            line_start_1 = line_start_2
                            indent_end_1 = indent_end_2
                            if children_2 is not None and children_2 is not None:
                                children_1.extend(children_2)
                            break
                        # end case
                        offset_2 = offset_1
                        line_start_2 = line_start_1
                        indent_end_2 = indent_end_1
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            count_1 = 0
                            while offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr in ' \t':
                                    offset_2 +=1
                                    count_1 += (self.tabstop-(offset_2-line_start_2)%self.tabstop) if chr == '	' else 1
                                else:
                                    break

                            if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '#':
                                offset_2 += 1
                            else:
                                offset_2 = -1
                                break

                            count_1 = 0
                            while True:
                                offset_3 = offset_2
                                line_start_3 = line_start_2
                                indent_end_3 = indent_end_2
                                children_3 = [] if children_2 is not None else None
                                while True:
                                    if offset_3 == buf_eof:
                                        offset_3 = -1
                                        break

                                    chr = (buf[offset_3])

                                    if chr == 10:
                                        offset_3 = -1
                                        break
                                    else:
                                        offset_3 += 1

                                    break
                                if offset_3 == -1:
                                    break
                                if offset_2 == offset_3: break
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                offset_2 = offset_3
                                line_start_2 = line_start_3
                                indent_end_3 = indent_end_3
                                count_1 += 1
                            if offset_2 == -1:
                                break

                            if offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                    offset_2 +=2
                                    line_start_2 = offset_2
                                    indent_end_2 = offset_2
                                elif chr in '\n\r':
                                    offset_2 +=1
                                    line_start_2 = offset_2
                                    indent_end_2 = offset_2
                                else:
                                    offset_2 = -1
                                    break
                            else:
                                offset_2 = -1
                                break


                            break
                        if offset_2 != -1:
                            offset_1 = offset_2
                            line_start_1 = line_start_2
                            indent_end_1 = indent_end_2
                            if children_2 is not None and children_2 is not None:
                                children_1.extend(children_2)
                            break
                        # end case
                        offset_1 = -1 # no more choices
                        break # end choice
                    if offset_1 == -1:
                        break

                    break
                if offset_1 == -1:
                    break
                if offset_0 == offset_1: break
                if children_1 is not None and children_1 is not None:
                    children_0.extend(children_1)
                offset_0 = offset_1
                line_start_0 = line_start_1
                indent_end_1 = indent_end_1
                count_0 += 1
            if offset_0 == -1:
                break

            break
        return offset_0, line_start_0, indent_end_0

    cdef (int, int, int) parse_indented_list(self, str buf, int offset_0, int buf_eof, int line_start_0, int indent_end_0,  list prefix_0, list children_0):
        cdef Py_UCS4 chr
        cdef int offset_1, offset_2, offset_3, offset_4
        cdef int line_start_1, line_start_2

        cdef list children_1, children_2, children_3
        cdef int count_1
        cdef int indent_end_1, indent_end_2
        while True: # note: return at end of loop
            count_0 = 0
            count_1 = indent_end_0
            for chr in buf[indent_end_0:offset_0]:
                count_0 += (self.tabstop-(count_1-line_start_0)%self.tabstop) if chr == '	' else 1
                count_1 +=1

            def _indent(buf, offset, buf_eof, line_start, indent_end,  prefix,  children, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
                saw_tab, saw_not_tab = False, False
                while count > 0 and offset < buf_eof:
                    chr = buf[offset]
                    if chr in ' \t':
                        offset +=1
                        count -= (self.tabstop-(offset-line_start)%self.tabstop) if chr == '	' else 1
                        if not allow_mixed_indent:
                            if chr == '	': saw_tab = True
                            else: saw_not_tab = True
                            if saw_tab and saw_not_tab:
                                 offset -1; break
                    elif chr == '\r' and offset_0 + 1 < buf_eof and buf[offset_0+1] == '\n':
                        break
                    elif chr in '\n\r':
                        break
                    else:
                        offset = -1
                        break
                return offset, line_start, indent_end
            prefix_0.append(_indent)
            indent_end_0 = offset_0
            while True:
                offset_1 = offset_0
                children_1 = []
                while True: # start capture
                    if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '-':
                        offset_1 += 1
                    else:
                        offset_1 = -1
                        break

                    while True: # start choice
                        offset_2 = offset_1
                        line_start_1 = line_start_0
                        indent_end_1 = indent_end_0
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            count_0 = 0
                            while offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr in ' \t':
                                    offset_2 +=1
                                    count_0 += (self.tabstop-(offset_2-line_start_1)%self.tabstop) if chr == '	' else 1
                                else:
                                    break

                            offset_2, line_start_1, indent_end_1 = self.parse_indented_value(buf, offset_2, buf_eof, line_start_1, indent_end_1, prefix_0, children_2)
                            if offset_2 == -1: break



                            break
                        if offset_2 != -1:
                            offset_1 = offset_2
                            line_start_0 = line_start_1
                            indent_end_0 = indent_end_1
                            if children_2 is not None and children_2 is not None:
                                children_1.extend(children_2)
                            break
                        # end case
                        offset_2 = offset_1
                        line_start_1 = line_start_0
                        indent_end_1 = indent_end_0
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            offset_2, line_start_1, indent_end_1 = self.parse_yaml_eol(buf, offset_2, buf_eof, line_start_1, indent_end_1, prefix_0, children_2)
                            if offset_2 == -1: break


                            if offset_2 != line_start_1 != indent_end_1:
                                offset_2 = -1
                                break
                            indent_end_1 = offset_2
                            for indent in prefix_0:
                                _children, _prefix = [], []
                                offset_2, line_start_1, indent_end_1 = indent(buf, offset_2, buf_eof, line_start_1, indent_end_1, _prefix, _children)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_2 == -1:        break
                                indent_end_1 = offset_2
                            if offset_2 == -1:
                                break

                            count_0 = 0
                            while offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr in ' \t':
                                    offset_2 +=1
                                    count_0 += (self.tabstop-(offset_2-line_start_1)%self.tabstop) if chr == '	' else 1
                                else:
                                    break
                            if count_0 < 1:
                                offset_2 = -1
                                break

                            offset_2, line_start_1, indent_end_1 = self.parse_indented_value(buf, offset_2, buf_eof, line_start_1, indent_end_1, prefix_0, children_2)
                            if offset_2 == -1: break



                            break
                        if offset_2 != -1:
                            offset_1 = offset_2
                            line_start_0 = line_start_1
                            indent_end_0 = indent_end_1
                            if children_2 is not None and children_2 is not None:
                                children_1.extend(children_2)
                            break
                        # end case
                        offset_1 = -1 # no more choices
                        break # end choice
                    if offset_1 == -1:
                        break

                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        line_start_1 = line_start_0
                        indent_end_1 = indent_end_0
                        children_2 = [] if children_1 is not None else None
                        while True:
                            offset_2, line_start_1, indent_end_1 = self.parse_yaml_eol(buf, offset_2, buf_eof, line_start_1, indent_end_1, prefix_0, children_2)
                            if offset_2 == -1: break


                            if offset_2 != line_start_1 != indent_end_1:
                                offset_2 = -1
                                break
                            indent_end_1 = offset_2
                            for indent in prefix_0:
                                _children, _prefix = [], []
                                offset_2, line_start_1, indent_end_1 = indent(buf, offset_2, buf_eof, line_start_1, indent_end_1, _prefix, _children)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_2 == -1:        break
                                indent_end_1 = offset_2
                            if offset_2 == -1:
                                break

                            if offset_2 + 1 <= buf_eof and buf[offset_2+0] == '-':
                                offset_2 += 1
                            else:
                                offset_2 = -1
                                break

                            count_1 = 0
                            while offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr in ' \t':
                                    offset_2 +=1
                                    count_1 += (self.tabstop-(offset_2-line_start_1)%self.tabstop) if chr == '	' else 1
                                else:
                                    break
                            if count_1 < 1:
                                offset_2 = -1
                                break

                            while True: # start choice
                                offset_3 = offset_2
                                line_start_2 = line_start_1
                                indent_end_2 = indent_end_1
                                children_3 = [] if children_2 is not None else None
                                while True: # case
                                    count_1 = 0
                                    while offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in ' \t':
                                            offset_3 +=1
                                            count_1 += (self.tabstop-(offset_3-line_start_2)%self.tabstop) if chr == '	' else 1
                                        else:
                                            break

                                    offset_3, line_start_2, indent_end_2 = self.parse_indented_value(buf, offset_3, buf_eof, line_start_2, indent_end_2, prefix_0, children_3)
                                    if offset_3 == -1: break



                                    break
                                if offset_3 != -1:
                                    offset_2 = offset_3
                                    line_start_1 = line_start_2
                                    indent_end_1 = indent_end_2
                                    if children_3 is not None and children_3 is not None:
                                        children_2.extend(children_3)
                                    break
                                # end case
                                offset_3 = offset_2
                                line_start_2 = line_start_1
                                indent_end_2 = indent_end_1
                                children_3 = [] if children_2 is not None else None
                                while True: # case
                                    offset_3, line_start_2, indent_end_2 = self.parse_yaml_eol(buf, offset_3, buf_eof, line_start_2, indent_end_2, prefix_0, children_3)
                                    if offset_3 == -1: break


                                    if offset_3 != line_start_2 != indent_end_2:
                                        offset_3 = -1
                                        break
                                    indent_end_2 = offset_3
                                    for indent in prefix_0:
                                        _children, _prefix = [], []
                                        offset_3, line_start_2, indent_end_2 = indent(buf, offset_3, buf_eof, line_start_2, indent_end_2, _prefix, _children)
                                        if _prefix or _children:
                                           raise Exception('bar')
                                        if offset_3 == -1:        break
                                        indent_end_2 = offset_3
                                    if offset_3 == -1:
                                        break

                                    count_1 = 0
                                    while offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in ' \t':
                                            offset_3 +=1
                                            count_1 += (self.tabstop-(offset_3-line_start_2)%self.tabstop) if chr == '	' else 1
                                        else:
                                            break

                                    offset_3, line_start_2, indent_end_2 = self.parse_indented_value(buf, offset_3, buf_eof, line_start_2, indent_end_2, prefix_0, children_3)
                                    if offset_3 == -1: break



                                    break
                                if offset_3 != -1:
                                    offset_2 = offset_3
                                    line_start_1 = line_start_2
                                    indent_end_1 = indent_end_2
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
                            break
                        if offset_1 == offset_2: break
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        offset_1 = offset_2
                        line_start_0 = line_start_1
                        indent_end_1 = indent_end_1
                        count_0 += 1
                    if offset_1 == -1:
                        break

                    break
                if offset_1 == -1:
                    offset_0 = -1
                    break
                if self.builder is not None:
                    value_0 = self.builder['list'](buf, offset_0, offset_1, children_1)
                else:
                    value_0 = Node('list', offset_0, offset_1, children_1, None)
                children_0.append(value_0)
                offset_0 = offset_1

                break
            prefix_0.pop()
            if offset_0 == -1: break

            break
        return offset_0, line_start_0, indent_end_0

    cdef (int, int, int) parse_indented_object(self, str buf, int offset_0, int buf_eof, int line_start_0, int indent_end_0,  list prefix_0, list children_0):
        cdef Py_UCS4 chr
        cdef int offset_1, offset_2, offset_3, offset_4, offset_5
        cdef int line_start_1, line_start_2

        cdef list children_1, children_2, children_3, children_4
        cdef int count_1
        cdef int indent_end_1, indent_end_2
        while True: # note: return at end of loop
            count_0 = 0
            count_1 = indent_end_0
            for chr in buf[indent_end_0:offset_0]:
                count_0 += (self.tabstop-(count_1-line_start_0)%self.tabstop) if chr == '	' else 1
                count_1 +=1

            def _indent(buf, offset, buf_eof, line_start, indent_end,  prefix,  children, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
                saw_tab, saw_not_tab = False, False
                while count > 0 and offset < buf_eof:
                    chr = buf[offset]
                    if chr in ' \t':
                        offset +=1
                        count -= (self.tabstop-(offset-line_start)%self.tabstop) if chr == '	' else 1
                        if not allow_mixed_indent:
                            if chr == '	': saw_tab = True
                            else: saw_not_tab = True
                            if saw_tab and saw_not_tab:
                                 offset -1; break
                    elif chr == '\r' and offset_0 + 1 < buf_eof and buf[offset_0+1] == '\n':
                        break
                    elif chr in '\n\r':
                        break
                    else:
                        offset = -1
                        break
                return offset, line_start, indent_end
            prefix_0.append(_indent)
            indent_end_0 = offset_0
            while True:
                offset_1 = offset_0
                children_1 = []
                while True: # start capture
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        offset_2, line_start_0, indent_end_0 = self.parse_identifier(buf, offset_2, buf_eof, line_start_0, indent_end_0, prefix_0, children_2)
                        if offset_2 == -1: break


                        count_0 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t':
                                offset_2 +=1
                                count_0 += (self.tabstop-(offset_2-line_start_0)%self.tabstop) if chr == '	' else 1
                            else:
                                break

                        if offset_2 + 1 <= buf_eof and buf[offset_2+0] == ':':
                            offset_2 += 1
                        else:
                            offset_2 = -1
                            break

                        while True: # start choice
                            offset_3 = offset_2
                            line_start_1 = line_start_0
                            indent_end_1 = indent_end_0
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                offset_3, line_start_1, indent_end_1 = self.parse_yaml_eol(buf, offset_3, buf_eof, line_start_1, indent_end_1, prefix_0, children_3)
                                if offset_3 == -1: break


                                if offset_3 != line_start_1 != indent_end_1:
                                    offset_3 = -1
                                    break
                                indent_end_1 = offset_3
                                for indent in prefix_0:
                                    _children, _prefix = [], []
                                    offset_3, line_start_1, indent_end_1 = indent(buf, offset_3, buf_eof, line_start_1, indent_end_1, _prefix, _children)
                                    if _prefix or _children:
                                       raise Exception('bar')
                                    if offset_3 == -1:        break
                                    indent_end_1 = offset_3
                                if offset_3 == -1:
                                    break

                                count_0 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        offset_3 +=1
                                        count_0 += (self.tabstop-(offset_3-line_start_1)%self.tabstop) if chr == '	' else 1
                                    else:
                                        break
                                if count_0 < 1:
                                    offset_3 = -1
                                    break

                                offset_3, line_start_1, indent_end_1 = self.parse_indented_value(buf, offset_3, buf_eof, line_start_1, indent_end_1, prefix_0, children_3)
                                if offset_3 == -1: break



                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                line_start_0 = line_start_1
                                indent_end_0 = indent_end_1
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            line_start_1 = line_start_0
                            indent_end_1 = indent_end_0
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                count_0 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        offset_3 +=1
                                        count_0 += (self.tabstop-(offset_3-line_start_1)%self.tabstop) if chr == '	' else 1
                                    else:
                                        break

                                offset_3, line_start_1, indent_end_1 = self.parse_indented_value(buf, offset_3, buf_eof, line_start_1, indent_end_1, prefix_0, children_3)
                                if offset_3 == -1: break



                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                line_start_0 = line_start_1
                                indent_end_0 = indent_end_1
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
                    if self.builder is not None:
                        value_0 = self.builder['pair'](buf, offset_1, offset_2, children_2)
                    else:
                        value_0 = Node('pair', offset_1, offset_2, children_2, None)
                    children_1.append(value_0)
                    offset_1 = offset_2

                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        line_start_1 = line_start_0
                        indent_end_1 = indent_end_0
                        children_2 = [] if children_1 is not None else None
                        while True:
                            offset_3 = offset_2
                            children_3 = []
                            while True: # start capture
                                offset_3, line_start_1, indent_end_1 = self.parse_yaml_eol(buf, offset_3, buf_eof, line_start_1, indent_end_1, prefix_0, children_3)
                                if offset_3 == -1: break


                                if offset_3 != line_start_1 != indent_end_1:
                                    offset_3 = -1
                                    break
                                indent_end_1 = offset_3
                                for indent in prefix_0:
                                    _children, _prefix = [], []
                                    offset_3, line_start_1, indent_end_1 = indent(buf, offset_3, buf_eof, line_start_1, indent_end_1, _prefix, _children)
                                    if _prefix or _children:
                                       raise Exception('bar')
                                    if offset_3 == -1:        break
                                    indent_end_1 = offset_3
                                if offset_3 == -1:
                                    break

                                offset_3, line_start_1, indent_end_1 = self.parse_identifier(buf, offset_3, buf_eof, line_start_1, indent_end_1, prefix_0, children_3)
                                if offset_3 == -1: break


                                count_1 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        offset_3 +=1
                                        count_1 += (self.tabstop-(offset_3-line_start_1)%self.tabstop) if chr == '	' else 1
                                    else:
                                        break

                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == ':':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                if self.builder is not None:
                                    children_3.append('a')
                                else:
                                    children_3.append(Node('value', offset_3, offset_3, (), 'a'))

                                while True: # start choice
                                    offset_4 = offset_3
                                    line_start_2 = line_start_1
                                    indent_end_2 = indent_end_1
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        count_1 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t':
                                                offset_4 +=1
                                                count_1 += (self.tabstop-(offset_4-line_start_2)%self.tabstop) if chr == '	' else 1
                                            else:
                                                break

                                        offset_4, line_start_2, indent_end_2 = self.parse_indented_value(buf, offset_4, buf_eof, line_start_2, indent_end_2, prefix_0, children_4)
                                        if offset_4 == -1: break



                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_1 = line_start_2
                                        indent_end_1 = indent_end_2
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_2 = line_start_1
                                    indent_end_2 = indent_end_1
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        offset_4, line_start_2, indent_end_2 = self.parse_yaml_eol(buf, offset_4, buf_eof, line_start_2, indent_end_2, prefix_0, children_4)
                                        if offset_4 == -1: break


                                        if offset_4 != line_start_2 != indent_end_2:
                                            offset_4 = -1
                                            break
                                        indent_end_2 = offset_4
                                        for indent in prefix_0:
                                            _children, _prefix = [], []
                                            offset_4, line_start_2, indent_end_2 = indent(buf, offset_4, buf_eof, line_start_2, indent_end_2, _prefix, _children)
                                            if _prefix or _children:
                                               raise Exception('bar')
                                            if offset_4 == -1:        break
                                            indent_end_2 = offset_4
                                        if offset_4 == -1:
                                            break

                                        count_1 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t':
                                                offset_4 +=1
                                                count_1 += (self.tabstop-(offset_4-line_start_2)%self.tabstop) if chr == '	' else 1
                                            else:
                                                break
                                        if count_1 < 1:
                                            offset_4 = -1
                                            break

                                        offset_4, line_start_2, indent_end_2 = self.parse_indented_value(buf, offset_4, buf_eof, line_start_2, indent_end_2, prefix_0, children_4)
                                        if offset_4 == -1: break



                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_1 = line_start_2
                                        indent_end_1 = indent_end_2
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
                                offset_2 = -1
                                break
                            if self.builder is not None:
                                value_1 = self.builder['pair'](buf, offset_2, offset_3, children_3)
                            else:
                                value_1 = Node('pair', offset_2, offset_3, children_3, None)
                            children_2.append(value_1)
                            offset_2 = offset_3

                            break
                        if offset_2 == -1:
                            break
                        if offset_1 == offset_2: break
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        offset_1 = offset_2
                        line_start_0 = line_start_1
                        indent_end_1 = indent_end_1
                        count_0 += 1
                    if offset_1 == -1:
                        break

                    break
                if offset_1 == -1:
                    offset_0 = -1
                    break
                if self.builder is not None:
                    value_2 = self.builder['object'](buf, offset_0, offset_1, children_1)
                else:
                    value_2 = Node('object', offset_0, offset_1, children_1, None)
                children_0.append(value_2)
                offset_0 = offset_1

                break
            prefix_0.pop()
            if offset_0 == -1: break

            break
        return offset_0, line_start_0, indent_end_0

    cdef (int, int, int) parse_indented_value(self, str buf, int offset_0, int buf_eof, int line_start_0, int indent_end_0,  list prefix_0, list children_0):
        cdef Py_UCS4 chr
        cdef int offset_1
        cdef int line_start_1

        cdef list children_1

        cdef int indent_end_1
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, line_start_1, indent_end_1 = self.parse_indented_object(buf, offset_1, buf_eof, line_start_1, indent_end_1, prefix_0, children_1)
                    if offset_1 == -1: break



                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    indent_end_0 = indent_end_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, line_start_1, indent_end_1 = self.parse_indented_list(buf, offset_1, buf_eof, line_start_1, indent_end_1, prefix_0, children_1)
                    if offset_1 == -1: break



                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    indent_end_0 = indent_end_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, line_start_1, indent_end_1 = self.parse_literal(buf, offset_1, buf_eof, line_start_1, indent_end_1, prefix_0, children_1)
                    if offset_1 == -1: break



                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    indent_end_0 = indent_end_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_0 = -1 # no more choices
                break # end choice
            if offset_0 == -1:
                break

            break
        return offset_0, line_start_0, indent_end_0

    cdef (int, int, int) parse_document(self, str buf, int offset_0, int buf_eof, int line_start_0, int indent_end_0,  list prefix_0, list children_0):
        cdef Py_UCS4 chr
        cdef int offset_1, offset_2
        cdef int line_start_1

        cdef list children_1, children_2
        cdef int count_1
        cdef int indent_end_1
        while True: # note: return at end of loop
            count_0 = 0
            while True:
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True:
                    count_1 = 0
                    while offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in ' \t':
                            offset_1 +=1
                            count_1 += (self.tabstop-(offset_1-line_start_1)%self.tabstop) if chr == '	' else 1
                        else:
                            break

                    offset_1, line_start_1, indent_end_1 = self.parse_yaml_eol(buf, offset_1, buf_eof, line_start_1, indent_end_1, prefix_0, children_1)
                    if offset_1 == -1: break


                    break
                if offset_1 == -1:
                    break
                if offset_0 == offset_1: break
                if children_1 is not None and children_1 is not None:
                    children_0.extend(children_1)
                offset_0 = offset_1
                line_start_0 = line_start_1
                indent_end_1 = indent_end_1
                count_0 += 1
            if offset_0 == -1:
                break

            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                while True: # start choice
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    indent_end_1 = indent_end_0
                    children_2 = [] if children_1 is not None else None
                    while True: # case
                        offset_2, line_start_1, indent_end_1 = self.parse_indented_object(buf, offset_2, buf_eof, line_start_1, indent_end_1, prefix_0, children_2)
                        if offset_2 == -1: break



                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        line_start_0 = line_start_1
                        indent_end_0 = indent_end_1
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    indent_end_1 = indent_end_0
                    children_2 = [] if children_1 is not None else None
                    while True: # case
                        offset_2, line_start_1, indent_end_1 = self.parse_indented_list(buf, offset_2, buf_eof, line_start_1, indent_end_1, prefix_0, children_2)
                        if offset_2 == -1: break



                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        line_start_0 = line_start_1
                        indent_end_0 = indent_end_1
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    indent_end_1 = indent_end_0
                    children_2 = [] if children_1 is not None else None
                    while True: # case
                        offset_2, line_start_1, indent_end_1 = self.parse_list_literal(buf, offset_2, buf_eof, line_start_1, indent_end_1, prefix_0, children_2)
                        if offset_2 == -1: break



                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        line_start_0 = line_start_1
                        indent_end_0 = indent_end_1
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    indent_end_1 = indent_end_0
                    children_2 = [] if children_1 is not None else None
                    while True: # case
                        offset_2, line_start_1, indent_end_1 = self.parse_object_literal(buf, offset_2, buf_eof, line_start_1, indent_end_1, prefix_0, children_2)
                        if offset_2 == -1: break



                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        line_start_0 = line_start_1
                        indent_end_0 = indent_end_1
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        break
                    # end case
                    offset_1 = -1 # no more choices
                    break # end choice
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['document'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = Node('document', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 += (self.tabstop-(offset_0-line_start_0)%self.tabstop) if chr == '	' else 1
                else:
                    break

            count_0 = 0
            while True:
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True:
                    offset_1, line_start_1, indent_end_1 = self.parse_yaml_eol(buf, offset_1, buf_eof, line_start_1, indent_end_1, prefix_0, children_1)
                    if offset_1 == -1: break


                    count_1 = 0
                    while offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in ' \t':
                            offset_1 +=1
                            count_1 += (self.tabstop-(offset_1-line_start_1)%self.tabstop) if chr == '	' else 1
                        else:
                            break

                    break
                if offset_1 == -1:
                    break
                if offset_0 == offset_1: break
                if children_1 is not None and children_1 is not None:
                    children_0.extend(children_1)
                offset_0 = offset_1
                line_start_0 = line_start_1
                indent_end_1 = indent_end_1
                count_0 += 1
            if offset_0 == -1:
                break

            count_0 = 0
            while True:
                offset_1 = offset_0
                line_start_1 = line_start_0
                indent_end_1 = indent_end_0
                children_1 = [] if children_0 is not None else None
                while True:
                    if offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr == '\r' and offset_1 + 1 < buf_eof and buf[offset_1+1] == '\n':
                            offset_1 +=2
                            line_start_1 = offset_1
                            indent_end_1 = offset_1
                        elif chr in '\n\r':
                            offset_1 +=1
                            line_start_1 = offset_1
                            indent_end_1 = offset_1
                        else:
                            offset_1 = -1
                            break

                    count_1 = 0
                    while offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in ' \t':
                            offset_1 +=1
                            count_1 += (self.tabstop-(offset_1-line_start_1)%self.tabstop) if chr == '	' else 1
                        else:
                            break

                    break
                if offset_1 == -1:
                    break
                if offset_0 == offset_1: break
                if children_1 is not None and children_1 is not None:
                    children_0.extend(children_1)
                offset_0 = offset_1
                line_start_0 = line_start_1
                indent_end_1 = indent_end_1
                count_0 += 1
            if offset_0 == -1:
                break


            break
        return offset_0, line_start_0, indent_end_0
