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

regex_0 = re.compile('[a-zA-Z_]')
regex_1 = re.compile('[\\-\\+]')
regex_2 = re.compile('[0-9]')
regex_3 = re.compile('(?:e|E)')
regex_4 = re.compile('(?:\\+|\\-)')
regex_5 = re.compile('[0-9a-fA-F]')
regex_6 = re.compile('[\\"\\\\\\/bfnrt]')
regex_7 = re.compile('[^\\\\\\"]')
regex_8 = re.compile('[^\\n]')

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

    def parse_yaml_literal(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
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

    def parse_true_literal(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            offset_1 = offset_0
            column_1 = column_0
            children_1 = []
            value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
            while True: # start capture
                if buf[offset_1:offset_1+4] == 'true':
                    offset_1 += 4
                    column_1 += 4
                else:
                    offset_1 = -1
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            value_0.name = 'bool'
            value_0.end = offset_1
            value_0.end_column = column_1
            value_0.value = None
            children_0.append(value_0)
            offset_0 = offset_1
            column_0 = column_1

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_false_literal(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            offset_1 = offset_0
            column_1 = column_0
            children_1 = []
            value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
            while True: # start capture
                if buf[offset_1:offset_1+5] == 'false':
                    offset_1 += 5
                    column_1 += 5
                else:
                    offset_1 = -1
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            value_0.name = 'bool'
            value_0.end = offset_1
            value_0.end_column = column_1
            value_0.value = None
            children_0.append(value_0)
            offset_0 = offset_1
            column_0 = column_1

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_null_literal(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            offset_1 = offset_0
            column_1 = column_0
            children_1 = []
            value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
            while True: # start capture
                if buf[offset_1:offset_1+4] == 'null':
                    offset_1 += 4
                    column_1 += 4
                else:
                    offset_1 = -1
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            value_0.name = 'null'
            value_0.end = offset_1
            value_0.end_column = column_1
            value_0.value = None
            children_0.append(value_0)
            offset_0 = offset_1
            column_0 = column_1

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_identifier(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
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
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = ord(buf[offset_3])

                                if 97 <= codepoint <= 122:
                                    offset_3 += 1
                                    column_3 += 1
                                elif 65 <= codepoint <= 90:
                                    offset_3 += 1
                                    column_3 += 1
                                elif codepoint == 95:
                                    offset_3 += 1
                                    column_3 += 1
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
                            column_2 = column_3
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
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
                    value_0.name = 'identifier'
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

    def parse_number_literal(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
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
                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break

                        codepoint = ord(buf[offset_2])

                        if codepoint == 45:
                            offset_2 += 1
                            column_2 += 1
                        elif codepoint == 43:
                            offset_2 += 1
                            column_2 += 1
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
                    column_1 = column_2
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    count_0 += 1
                    break
                if offset_1 == -1:
                    break

                count_0 = 0
                while True:
                    offset_2 = offset_1
                    column_2 = column_1
                    indent_column_1 = list(indent_column_0)
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break

                        codepoint = ord(buf[offset_2])

                        if 48 <= codepoint <= 57:
                            offset_2 += 1
                            column_2 += 1
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
                    column_1 = column_2
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    count_0 += 1
                if count_0 < 1:
                    offset_1 = -1
                    break
                if offset_1 == -1:
                    break

                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    column_2 = column_1
                    indent_column_1 = list(indent_column_0)
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        if buf[offset_2:offset_2+1] == '.':
                            offset_2 += 1
                            column_2 += 1
                        else:
                            offset_2 = -1
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
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = ord(buf[offset_3])

                                if 48 <= codepoint <= 57:
                                    offset_3 += 1
                                    column_3 += 1
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
                            column_2 = column_3
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
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
                    column_1 = column_2
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    count_0 += 1
                    break
                if offset_1 == -1:
                    break

                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    column_2 = column_1
                    indent_column_1 = list(indent_column_0)
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        if buf[offset_2:offset_2+1] == 'e':
                            offset_2 += 1
                            column_2 += 1
                        elif buf[offset_2:offset_2+1] == 'E':
                            offset_2 += 1
                            column_2 += 1
                        else:
                            offset_2 = -1
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
                                if buf[offset_3:offset_3+1] == '+':
                                    offset_3 += 1
                                    column_3 += 1
                                elif buf[offset_3:offset_3+1] == '-':
                                    offset_3 += 1
                                    column_3 += 1
                                else:
                                    offset_3 = -1
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
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        codepoint = ord(buf[offset_4])

                                        if 48 <= codepoint <= 57:
                                            offset_4 += 1
                                            column_4 += 1
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
                                    column_3 = column_4
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
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
            value_0.name = 'number'
            value_0.end = offset_1
            value_0.end_column = column_1
            value_0.value = None
            children_0.append(value_0)
            offset_0 = offset_1
            column_0 = column_1

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_string_literal(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            if buf[offset_0:offset_0+1] == '"':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break

            offset_1 = offset_0
            column_1 = column_0
            children_1 = []
            value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
            while True: # start capture
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    column_2 = column_1
                    indent_column_1 = list(indent_column_0)
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        while True: # start choice
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                if buf[offset_3:offset_3+2] == '\\u':
                                    offset_3 += 2
                                    column_3 += 2
                                else:
                                    offset_3 = -1
                                    break

                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = ord(buf[offset_3])

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

                                codepoint = ord(buf[offset_3])

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

                                codepoint = ord(buf[offset_3])

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

                                codepoint = ord(buf[offset_3])

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
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                if buf[offset_3:offset_3+1] == '\\':
                                    offset_3 += 1
                                    column_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = ord(buf[offset_3])

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
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_2 = list(indent_column_1)
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = ord(buf[offset_3])

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
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            value_0.name = 'string'
            value_0.end = offset_1
            value_0.end_column = column_1
            value_0.value = None
            children_0.append(value_0)
            offset_0 = offset_1
            column_0 = column_1

            if buf[offset_0:offset_0+1] == '"':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_list_literal(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
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
                        offset_2, column_2, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_literal(buf, buf_start, buf_eof, offset_2, column_2, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
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
                                    if codepoint == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        column_3 = 0
                                        indent_column_2[:] = (0, )
                                    elif codepoint in '\n\r':
                                        offset_3 +=1
                                        column_3 = 0
                                        indent_column_2[:] = (0, )
                                        count_2 +=1
                                    elif codepoint in ' \t':
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
                                    if codepoint == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        column_3 = 0
                                        indent_column_2[:] = (0, )
                                    elif codepoint in '\n\r':
                                        offset_3 +=1
                                        column_3 = 0
                                        indent_column_2[:] = (0, )
                                        count_2 +=1
                                    elif codepoint in ' \t':
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

                                offset_3, column_3, partial_tab_offset_2, partial_tab_width_2 = self.parse_yaml_literal(buf, buf_start, buf_eof, offset_3, column_3, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
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
                            if codepoint == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                offset_2 +=2
                                column_2 = 0
                                indent_column_1[:] = (0, )
                            elif codepoint in '\n\r':
                                offset_2 +=1
                                column_2 = 0
                                indent_column_1[:] = (0, )
                                count_1 +=1
                            elif codepoint in ' \t':
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
                                    if codepoint == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        column_3 = 0
                                        indent_column_2[:] = (0, )
                                    elif codepoint in '\n\r':
                                        offset_3 +=1
                                        column_3 = 0
                                        indent_column_2[:] = (0, )
                                        count_2 +=1
                                    elif codepoint in ' \t':
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

    def parse_object_literal(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
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
                        offset_2, column_2, partial_tab_offset_1, partial_tab_width_1 = self.parse_string_literal(buf, buf_start, buf_eof, offset_2, column_2, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                        if offset_2 == -1: break


                        count_1 = 0
                        while offset_2 < buf_eof:
                            codepoint = buf[offset_2]
                            if codepoint in ' \t':
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

                        if buf[offset_2:offset_2+1] == ':':
                            offset_2 += 1
                            column_2 += 1
                        else:
                            offset_2 = -1
                            break

                        count_1 = 0
                        while offset_2 < buf_eof:
                            codepoint = buf[offset_2]
                            if codepoint == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                offset_2 +=2
                                column_2 = 0
                                indent_column_1[:] = (0, )
                            elif codepoint in '\n\r':
                                offset_2 +=1
                                column_2 = 0
                                indent_column_1[:] = (0, )
                                count_1 +=1
                            elif codepoint in ' \t':
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

                        offset_2, column_2, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_literal(buf, buf_start, buf_eof, offset_2, column_2, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
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
                                    if codepoint == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        column_3 = 0
                                        indent_column_2[:] = (0, )
                                    elif codepoint in '\n\r':
                                        offset_3 +=1
                                        column_3 = 0
                                        indent_column_2[:] = (0, )
                                        count_2 +=1
                                    elif codepoint in ' \t':
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
                                    if codepoint == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        column_3 = 0
                                        indent_column_2[:] = (0, )
                                    elif codepoint in '\n\r':
                                        offset_3 +=1
                                        column_3 = 0
                                        indent_column_2[:] = (0, )
                                        count_2 +=1
                                    elif codepoint in ' \t':
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

                                offset_3, column_3, partial_tab_offset_2, partial_tab_width_2 = self.parse_string_literal(buf, buf_start, buf_eof, offset_3, column_3, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
                                if offset_3 == -1: break


                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t':
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

                                if buf[offset_3:offset_3+1] == ':':
                                    offset_3 += 1
                                    column_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        column_3 = 0
                                        indent_column_2[:] = (0, )
                                    elif codepoint in '\n\r':
                                        offset_3 +=1
                                        column_3 = 0
                                        indent_column_2[:] = (0, )
                                        count_2 +=1
                                    elif codepoint in ' \t':
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

                                offset_3, column_3, partial_tab_offset_2, partial_tab_width_2 = self.parse_yaml_literal(buf, buf_start, buf_eof, offset_3, column_3, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
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
                            if codepoint == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                offset_2 +=2
                                column_2 = 0
                                indent_column_1[:] = (0, )
                            elif codepoint in '\n\r':
                                offset_2 +=1
                                column_2 = 0
                                indent_column_1[:] = (0, )
                                count_1 +=1
                            elif codepoint in ' \t':
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
                                    if codepoint == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        column_3 = 0
                                        indent_column_2[:] = (0, )
                                    elif codepoint in '\n\r':
                                        offset_3 +=1
                                        column_3 = 0
                                        indent_column_2[:] = (0, )
                                        count_2 +=1
                                    elif codepoint in ' \t':
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

    def parse_yaml_eol(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
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

                            if buf[offset_2:offset_2+1] == '#':
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
                                    if offset_3 == buf_eof:
                                        offset_3 = -1
                                        break

                                    codepoint = ord(buf[offset_3])

                                    if codepoint == 10:
                                        offset_3 = -1
                                        break
                                    else:
                                        offset_3 += 1
                                        column_3 += 1


                                    break
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

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_indented_list(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = column_0 - indent_column_0[len(indent_column_0)-1]
            # print(count_0, 'indent')
            def _indent(buf, buf_start, buf_eof, offset, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
                saw_tab, saw_not_tab = False, False
                start_column, start_offset = column, offset
                while count > 0 and offset < buf_eof:
                    codepoint = buf[offset]
                    if codepoint in ' \t':
                        if not allow_mixed_indent:
                            if codepoint == '\t': saw_tab = True
                            else: saw_not_tab = True
                            if saw_tab and saw_not_tab:
                                 offset -1; break
                        if codepoint != '\t':
                            column += 1
                            offset += 1
                            count -=1
                        else:
                            if offset == partial_tab_offset and partial_tab_width > 0:
                                width = partial_tab_width
                            else:
                                width  = (self.tabstop-(column%self.tabstop))
                            if width <= count:
                                column += width
                                offset += 1
                                count -= width
                            else:
                                column += count
                                partial_tab_offset = offset
                                partial_tab_width = width-count
                                break
                    elif codepoint == '\r' and offset_0 + 1 < buf_eof and buf[offset_0+1] == '\n':
                        break
                    elif codepoint in '\n\r':
                        break
                    else:
                        offset = -1
                        break
                return offset, column, partial_tab_offset, partial_tab_width
            def _dedent(buf, buf_start, buf_eof, offset, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
                saw_tab, saw_not_tab = False, False
                start_column, start_offset = column, offset
                while count > 0 and offset < buf_eof:
                    codepoint = buf[offset]
                    if codepoint in ' \t':
                        if not allow_mixed_indent:
                            if codepoint == '\t': saw_tab = True
                            else: saw_not_tab = True
                            if saw_tab and saw_not_tab:
                                offset = start_offset; break
                        if codepoint != '\t':
                            column += 1
                            offset += 1
                            count -=1
                        else:
                            if offset == partial_tab_offset and partial_tab_width > 0:
                                width = partial_tab_width
                            else:
                                width  = (self.tabstop-(column%self.tabstop))
                            if width <= count:
                                column += width
                                offset += 1
                                count -= width
                            else: # we have indent, so break
                                offset = -1; break
                    elif codepoint == '\r' and offset_0 + 1 < buf_eof and buf[offset_0+1] == '\n':
                        offset = -1; break
                    elif codepoint in '\n\r':
                        offset = -1; break
                    else:
                        offset = start_offset
                if count == 0:
                        offset = -1
                return offset, column, partial_tab_offset, partial_tab_width
            prefix_0.append((_indent, _dedent))
            indent_column_0.append(column_0)
            while True:
                offset_1 = offset_0
                column_1 = column_0
                children_1 = []
                value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
                while True: # start capture
                    if buf[offset_1:offset_1+1] == '-':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    while True: # start choice
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_1 = list(indent_column_0)
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            count_0 = 0
                            while offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
                                        if offset_2 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-(column_2%self.tabstop))
                                        count_0 += width
                                        column_2 += width
                                        offset_2 += 1
                                    else:
                                        count_0 += 1
                                        column_2 += 1
                                        offset_2 += 1
                                else:
                                    break

                            offset_2, column_2, partial_tab_offset_1, partial_tab_width_1 = self.parse_indented_value(buf, buf_start, buf_eof, offset_2, column_2, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                            if offset_2 == -1: break



                            break
                        if offset_2 != -1:
                            offset_1 = offset_2
                            column_1 = column_2
                            indent_column_0 = indent_column_1
                            partial_tab_offset_0 = partial_tab_offset_1
                            partial_tab_width_0 = partial_tab_width_1
                            if children_2 is not None and children_2 is not None:
                                children_1.extend(children_2)
                            break
                        # end case
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_1 = list(indent_column_0)
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            offset_2, column_2, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_2, column_2, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                            if offset_2 == -1: break


                            if column_2 != 0:
                                offset_2 = -1
                                break
                            # print('start')
                            for indent, dedent in prefix_0:
                                # print(indent, dedent)
                                _children, _prefix = [], []
                                offset_3 = offset_2
                                offset_3, column_2, partial_tab_offset_1, partial_tab_width_1 = indent(buf, buf_start, buf_eof, offset_3, column_2, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_3 == -1:
                                    offset_2 = -1
                                    break
                                offset_2 = offset_3
                                indent_column_1.append(column_2)
                            if offset_2 == -1:
                                break

                            count_0 = 0
                            while offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
                                        if offset_2 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-(column_2%self.tabstop))
                                        count_0 += width
                                        column_2 += width
                                        offset_2 += 1
                                    else:
                                        count_0 += 1
                                        column_2 += 1
                                        offset_2 += 1
                                else:
                                    break
                            if count_0 < 1:
                                offset_2 = -1
                                break

                            offset_2, column_2, partial_tab_offset_1, partial_tab_width_1 = self.parse_indented_value(buf, buf_start, buf_eof, offset_2, column_2, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                            if offset_2 == -1: break



                            break
                        if offset_2 != -1:
                            offset_1 = offset_2
                            column_1 = column_2
                            indent_column_0 = indent_column_1
                            partial_tab_offset_0 = partial_tab_offset_1
                            partial_tab_width_0 = partial_tab_width_1
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
                        column_2 = column_1
                        indent_column_1 = list(indent_column_0)
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True:
                            offset_2, column_2, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_2, column_2, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                            if offset_2 == -1: break


                            if column_2 != 0:
                                offset_2 = -1
                                break
                            # print('start')
                            for indent, dedent in prefix_0:
                                # print(indent, dedent)
                                _children, _prefix = [], []
                                offset_3 = offset_2
                                offset_3, column_2, partial_tab_offset_1, partial_tab_width_1 = indent(buf, buf_start, buf_eof, offset_3, column_2, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_3 == -1:
                                    offset_2 = -1
                                    break
                                offset_2 = offset_3
                                indent_column_1.append(column_2)
                            if offset_2 == -1:
                                break

                            if buf[offset_2:offset_2+1] == '-':
                                offset_2 += 1
                                column_2 += 1
                            else:
                                offset_2 = -1
                                break

                            count_1 = 0
                            while offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
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
                            if count_1 < 1:
                                offset_2 = -1
                                break

                            while True: # start choice
                                offset_3 = offset_2
                                column_3 = column_2
                                indent_column_2 = list(indent_column_1)
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_3 = [] if children_2 is not None else None
                                while True: # case
                                    count_1 = 0
                                    while offset_3 < buf_eof:
                                        codepoint = buf[offset_3]
                                        if codepoint in ' \t':
                                            if codepoint == '\t':
                                                if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                    width = partial_tab_width_2
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

                                    offset_3, column_3, partial_tab_offset_2, partial_tab_width_2 = self.parse_indented_value(buf, buf_start, buf_eof, offset_3, column_3, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
                                    if offset_3 == -1: break



                                    break
                                if offset_3 != -1:
                                    offset_2 = offset_3
                                    column_2 = column_3
                                    indent_column_1 = indent_column_2
                                    partial_tab_offset_1 = partial_tab_offset_2
                                    partial_tab_width_1 = partial_tab_width_2
                                    if children_3 is not None and children_3 is not None:
                                        children_2.extend(children_3)
                                    break
                                # end case
                                offset_3 = offset_2
                                column_3 = column_2
                                indent_column_2 = list(indent_column_1)
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_3 = [] if children_2 is not None else None
                                while True: # case
                                    offset_3, column_3, partial_tab_offset_2, partial_tab_width_2 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_3, column_3, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
                                    if offset_3 == -1: break


                                    if column_3 != 0:
                                        offset_3 = -1
                                        break
                                    # print('start')
                                    for indent, dedent in prefix_0:
                                        # print(indent, dedent)
                                        _children, _prefix = [], []
                                        offset_4 = offset_3
                                        offset_4, column_3, partial_tab_offset_2, partial_tab_width_2 = indent(buf, buf_start, buf_eof, offset_4, column_3, indent_column_2, _prefix, _children, partial_tab_offset_2, partial_tab_width_2)
                                        if _prefix or _children:
                                           raise Exception('bar')
                                        if offset_4 == -1:
                                            offset_3 = -1
                                            break
                                        offset_3 = offset_4
                                        indent_column_2.append(column_3)
                                    if offset_3 == -1:
                                        break

                                    count_1 = 0
                                    while offset_3 < buf_eof:
                                        codepoint = buf[offset_3]
                                        if codepoint in ' \t':
                                            if codepoint == '\t':
                                                if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                    width = partial_tab_width_2
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

                                    offset_3, column_3, partial_tab_offset_2, partial_tab_width_2 = self.parse_indented_value(buf, buf_start, buf_eof, offset_3, column_3, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
                                    if offset_3 == -1: break



                                    break
                                if offset_3 != -1:
                                    offset_2 = offset_3
                                    column_2 = column_3
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

                break
            prefix_0.pop()
            if len(indent_column_0) > 1: indent_column_0.pop()
            if offset_0 == -1: break

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_indented_object(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = column_0 - indent_column_0[len(indent_column_0)-1]
            # print(count_0, 'indent')
            def _indent(buf, buf_start, buf_eof, offset, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
                saw_tab, saw_not_tab = False, False
                start_column, start_offset = column, offset
                while count > 0 and offset < buf_eof:
                    codepoint = buf[offset]
                    if codepoint in ' \t':
                        if not allow_mixed_indent:
                            if codepoint == '\t': saw_tab = True
                            else: saw_not_tab = True
                            if saw_tab and saw_not_tab:
                                 offset -1; break
                        if codepoint != '\t':
                            column += 1
                            offset += 1
                            count -=1
                        else:
                            if offset == partial_tab_offset and partial_tab_width > 0:
                                width = partial_tab_width
                            else:
                                width  = (self.tabstop-(column%self.tabstop))
                            if width <= count:
                                column += width
                                offset += 1
                                count -= width
                            else:
                                column += count
                                partial_tab_offset = offset
                                partial_tab_width = width-count
                                break
                    elif codepoint == '\r' and offset_0 + 1 < buf_eof and buf[offset_0+1] == '\n':
                        break
                    elif codepoint in '\n\r':
                        break
                    else:
                        offset = -1
                        break
                return offset, column, partial_tab_offset, partial_tab_width
            def _dedent(buf, buf_start, buf_eof, offset, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
                saw_tab, saw_not_tab = False, False
                start_column, start_offset = column, offset
                while count > 0 and offset < buf_eof:
                    codepoint = buf[offset]
                    if codepoint in ' \t':
                        if not allow_mixed_indent:
                            if codepoint == '\t': saw_tab = True
                            else: saw_not_tab = True
                            if saw_tab and saw_not_tab:
                                offset = start_offset; break
                        if codepoint != '\t':
                            column += 1
                            offset += 1
                            count -=1
                        else:
                            if offset == partial_tab_offset and partial_tab_width > 0:
                                width = partial_tab_width
                            else:
                                width  = (self.tabstop-(column%self.tabstop))
                            if width <= count:
                                column += width
                                offset += 1
                                count -= width
                            else: # we have indent, so break
                                offset = -1; break
                    elif codepoint == '\r' and offset_0 + 1 < buf_eof and buf[offset_0+1] == '\n':
                        offset = -1; break
                    elif codepoint in '\n\r':
                        offset = -1; break
                    else:
                        offset = start_offset
                if count == 0:
                        offset = -1
                return offset, column, partial_tab_offset, partial_tab_width
            prefix_0.append((_indent, _dedent))
            indent_column_0.append(column_0)
            while True:
                offset_1 = offset_0
                column_1 = column_0
                children_1 = []
                value_0 = Node(None, offset_0, offset_0, column_0, column_0, children_1, None)
                while True: # start capture
                    offset_2 = offset_1
                    column_2 = column_1
                    children_2 = []
                    value_1 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        offset_2, column_2, partial_tab_offset_0, partial_tab_width_0 = self.parse_identifier(buf, buf_start, buf_eof, offset_2, column_2, indent_column_0, prefix_0, children_2, partial_tab_offset_0, partial_tab_width_0)
                        if offset_2 == -1: break


                        count_0 = 0
                        while offset_2 < buf_eof:
                            codepoint = buf[offset_2]
                            if codepoint in ' \t':
                                if codepoint == '\t':
                                    if offset_2 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                                        width = partial_tab_width_0
                                    else:
                                        width  = (self.tabstop-(column_2%self.tabstop))
                                    count_0 += width
                                    column_2 += width
                                    offset_2 += 1
                                else:
                                    count_0 += 1
                                    column_2 += 1
                                    offset_2 += 1
                            else:
                                break

                        if buf[offset_2:offset_2+1] == ':':
                            offset_2 += 1
                            column_2 += 1
                        else:
                            offset_2 = -1
                            break

                        while True: # start choice
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_1 = list(indent_column_0)
                            partial_tab_offset_1 = partial_tab_offset_0
                            partial_tab_width_1 = partial_tab_width_0
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                offset_3, column_3, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_3, column_3, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                                if offset_3 == -1: break


                                if column_3 != 0:
                                    offset_3 = -1
                                    break
                                # print('start')
                                for indent, dedent in prefix_0:
                                    # print(indent, dedent)
                                    _children, _prefix = [], []
                                    offset_4 = offset_3
                                    offset_4, column_3, partial_tab_offset_1, partial_tab_width_1 = indent(buf, buf_start, buf_eof, offset_4, column_3, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                    if _prefix or _children:
                                       raise Exception('bar')
                                    if offset_4 == -1:
                                        offset_3 = -1
                                        break
                                    offset_3 = offset_4
                                    indent_column_1.append(column_3)
                                if offset_3 == -1:
                                    break

                                count_0 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                                width = partial_tab_width_1
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_0 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_0 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break
                                if count_0 < 1:
                                    offset_3 = -1
                                    break

                                offset_3, column_3, partial_tab_offset_1, partial_tab_width_1 = self.parse_indented_value(buf, buf_start, buf_eof, offset_3, column_3, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                                if offset_3 == -1: break



                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                column_2 = column_3
                                indent_column_0 = indent_column_1
                                partial_tab_offset_0 = partial_tab_offset_1
                                partial_tab_width_0 = partial_tab_width_1
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_1 = list(indent_column_0)
                            partial_tab_offset_1 = partial_tab_offset_0
                            partial_tab_width_1 = partial_tab_width_0
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                count_0 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                                width = partial_tab_width_1
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            count_0 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_0 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                offset_3, column_3, partial_tab_offset_1, partial_tab_width_1 = self.parse_indented_value(buf, buf_start, buf_eof, offset_3, column_3, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                                if offset_3 == -1: break



                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                column_2 = column_3
                                indent_column_0 = indent_column_1
                                partial_tab_offset_0 = partial_tab_offset_1
                                partial_tab_width_0 = partial_tab_width_1
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
                    value_1.name = 'pair'
                    value_1.end = offset_2
                    value_1.end_column = column_2
                    value_1.value = None
                    children_1.append(value_1)
                    offset_1 = offset_2
                    column_1 = column_2

                    count_0 = 0
                    while True:
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
                            value_2 = Node(None, offset_2, offset_2, column_2, column_2, children_3, None)
                            while True: # start capture
                                offset_3, column_3, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_3, column_3, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                                if offset_3 == -1: break


                                if column_3 != 0:
                                    offset_3 = -1
                                    break
                                # print('start')
                                for indent, dedent in prefix_0:
                                    # print(indent, dedent)
                                    _children, _prefix = [], []
                                    offset_4 = offset_3
                                    offset_4, column_3, partial_tab_offset_1, partial_tab_width_1 = indent(buf, buf_start, buf_eof, offset_4, column_3, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                    if _prefix or _children:
                                       raise Exception('bar')
                                    if offset_4 == -1:
                                        offset_3 = -1
                                        break
                                    offset_3 = offset_4
                                    indent_column_1.append(column_3)
                                if offset_3 == -1:
                                    break

                                offset_3, column_3, partial_tab_offset_1, partial_tab_width_1 = self.parse_identifier(buf, buf_start, buf_eof, offset_3, column_3, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                                if offset_3 == -1: break


                                count_1 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t':
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

                                children_3.append(Node('value', offset_3, offset_3, column_3, column_3, (), 'a'))

                                while True: # start choice
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_2 = list(indent_column_1)
                                    partial_tab_offset_2 = partial_tab_offset_1
                                    partial_tab_width_2 = partial_tab_width_1
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        count_1 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t':
                                                if codepoint == '\t':
                                                    if offset_4 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                        width = partial_tab_width_2
                                                    else:
                                                        width  = (self.tabstop-(column_4%self.tabstop))
                                                    count_1 += width
                                                    column_4 += width
                                                    offset_4 += 1
                                                else:
                                                    count_1 += 1
                                                    column_4 += 1
                                                    offset_4 += 1
                                            else:
                                                break

                                        offset_4, column_4, partial_tab_offset_2, partial_tab_width_2 = self.parse_indented_value(buf, buf_start, buf_eof, offset_4, column_4, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                        if offset_4 == -1: break



                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_3 = column_4
                                        indent_column_1 = indent_column_2
                                        partial_tab_offset_1 = partial_tab_offset_2
                                        partial_tab_width_1 = partial_tab_width_2
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_4 = column_3
                                    indent_column_2 = list(indent_column_1)
                                    partial_tab_offset_2 = partial_tab_offset_1
                                    partial_tab_width_2 = partial_tab_width_1
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        offset_4, column_4, partial_tab_offset_2, partial_tab_width_2 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_4, column_4, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                        if offset_4 == -1: break


                                        if column_4 != 0:
                                            offset_4 = -1
                                            break
                                        # print('start')
                                        for indent, dedent in prefix_0:
                                            # print(indent, dedent)
                                            _children, _prefix = [], []
                                            offset_5 = offset_4
                                            offset_5, column_4, partial_tab_offset_2, partial_tab_width_2 = indent(buf, buf_start, buf_eof, offset_5, column_4, indent_column_2, _prefix, _children, partial_tab_offset_2, partial_tab_width_2)
                                            if _prefix or _children:
                                               raise Exception('bar')
                                            if offset_5 == -1:
                                                offset_4 = -1
                                                break
                                            offset_4 = offset_5
                                            indent_column_2.append(column_4)
                                        if offset_4 == -1:
                                            break

                                        count_1 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t':
                                                if codepoint == '\t':
                                                    if offset_4 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                        width = partial_tab_width_2
                                                    else:
                                                        width  = (self.tabstop-(column_4%self.tabstop))
                                                    count_1 += width
                                                    column_4 += width
                                                    offset_4 += 1
                                                else:
                                                    count_1 += 1
                                                    column_4 += 1
                                                    offset_4 += 1
                                            else:
                                                break
                                        if count_1 < 1:
                                            offset_4 = -1
                                            break

                                        offset_4, column_4, partial_tab_offset_2, partial_tab_width_2 = self.parse_indented_value(buf, buf_start, buf_eof, offset_4, column_4, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                        if offset_4 == -1: break



                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_3 = column_4
                                        indent_column_1 = indent_column_2
                                        partial_tab_offset_1 = partial_tab_offset_2
                                        partial_tab_width_1 = partial_tab_width_2
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
                            value_2.name = 'pair'
                            value_2.end = offset_3
                            value_2.end_column = column_3
                            value_2.value = None
                            children_2.append(value_2)
                            offset_2 = offset_3
                            column_2 = column_3

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

                break
            prefix_0.pop()
            if len(indent_column_0) > 1: indent_column_0.pop()
            if offset_0 == -1: break

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_indented_value(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
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

    def parse_document(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
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
                    count_1 = 0
                    while offset_1 < buf_eof:
                        codepoint = buf[offset_1]
                        if codepoint in ' \t':
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

                    offset_1, column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_yaml_eol(buf, buf_start, buf_eof, offset_1, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
                    if offset_1 == -1: break


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
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = list(indent_column_0)
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
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


            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0
