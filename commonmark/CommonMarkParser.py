class Parser:
    def __init__(self, builder=None, tabstop=None, allow_mixed_indent=False):
         self.builder = builder
         self.tabstop = tabstop or 4
         self.cache = None
         self.allow_mixed_indent = allow_mixed_indent

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


    def parse(self, buf, offset=0, end=None, err=None):
        self.cache = dict()
        end = len(buf) if end is None else end
        column, indent_column, eof = offset, offset, end
        prefix, children = [], []
        new_offset, column, indent_column, partial_tab_offset, partial_tab_width = self.parse_document(buf, offset, eof, column, indent_column, prefix, children, 0, 0)
        if children and new_offset == end: return children[-1]
        print('no', offset, new_offset, end, buf[new_offset:])
        if err is not None: raise err(buf, new_offset, 'no')

    def parse_document(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        if not (column_1 == indent_column_1 == 0):
                            offset_2 = -1
                            break
                        for indent in prefix_0:
                            _children, _prefix = [], []
                            offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_2, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                            if _prefix or _children:
                               raise Exception('bar')
                            if offset_2 == -1:        break
                            indent_column_1 = column_1
                        if offset_2 == -1:
                            break

                        offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_block_element(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                        if offset_2 == -1: break


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
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['document'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('document', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
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

            if offset_0 != buf_eof:
                offset_0 = -1
                break


            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_block_element(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_empty_lines(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_indented_code_block(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_fenced_code_block(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_blockquote(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_atx_heading(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_thematic_break(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_block_list(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_setext_heading(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_para(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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

    def parse_thematic_break(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        if count_0 + width > 3:
                            new_width = 3 - count_0
                            count_0 += new_width
                            column_0 += new_width
                            partial_tab_offset_0 = offset_0
                            partial_tab_width_0 = width - new_width
                            break
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
                while True: # start choice
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True: # case
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if buf[offset_3:offset_3+1] == '-':
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_1 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        if chr == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_1 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_1 += 1
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
                            count_0 += 1
                        if count_0 < 3:
                            offset_2 = -1
                            break
                        if offset_2 == -1:
                            break


                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        column_0 = column_1
                        indent_column_0 = indent_column_1
                        partial_tab_offset_0 = partial_tab_offset_1
                        partial_tab_width_0 = partial_tab_width_1
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True: # case
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if buf[offset_3:offset_3+1] == '*':
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_1 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        if chr == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_1 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_1 += 1
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
                            count_0 += 1
                        if count_0 < 3:
                            offset_2 = -1
                            break
                        if offset_2 == -1:
                            break


                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        column_0 = column_1
                        indent_column_0 = indent_column_1
                        partial_tab_offset_0 = partial_tab_offset_1
                        partial_tab_width_0 = partial_tab_width_1
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True: # case
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if buf[offset_3:offset_3+1] == '_':
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_1 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        if chr == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_1 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_1 += 1
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
                            count_0 += 1
                        if count_0 < 3:
                            offset_2 = -1
                            break
                        if offset_2 == -1:
                            break


                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        column_0 = column_1
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

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['thematic_break'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('thematic_break', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_line_end(buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0)
            if offset_0 == -1: break



            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_atx_heading(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        if count_0 + width > 3:
                            new_width = 3 - count_0
                            count_0 += new_width
                            column_0 += new_width
                            partial_tab_offset_0 = offset_0
                            partial_tab_width_0 = width - new_width
                            break
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
                offset_2 = offset_1
                column_1 = column_0
                while True: # start count
                    count_0 = 0
                    while count_0 < 6:
                        offset_3 = offset_2
                        column_2 = column_1
                        indent_column_1 = indent_column_0
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True:
                            if buf[offset_3:offset_3+1] == '#':
                                offset_3 += 1
                                column_2 += 1
                            else:
                                offset_3 = -1
                                break

                            break
                        if offset_3 == -1:
                            break
                        if offset_2 == offset_3: break
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        offset_2 = offset_3
                        column_1 = column_2
                        indent_column_0 = indent_column_1
                        partial_tab_offset_0 = partial_tab_offset_1
                        partial_tab_width_0 = partial_tab_width_1
                        count_0 += 1
                    if count_0 < 1:
                        offset_2 = -1
                        break
                    if offset_2 == -1:
                        break

                    break
                if offset_2 == -1:
                    offset_1 = -1; break
                value_0 = buf[offset_1:offset_2].count('#')
                offset_1 = offset_2
                column_0 = column_1

                if self.builder is not None:
                    children_1.append(value_0)
                else:
                    children_1.append(self.Node('value', offset_1, offset_1, (), value_0))

                while True: # start choice
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True: # case
                        offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_atx_heading_end(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                        if offset_2 == -1: break



                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        column_0 = column_1
                        indent_column_0 = indent_column_1
                        partial_tab_offset_0 = partial_tab_offset_1
                        partial_tab_width_0 = partial_tab_width_1
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True: # case
                        count_0 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t':
                                if chr == '\t':
                                    if offset_2 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                        width = partial_tab_width_1
                                    else:
                                        width  = (self.tabstop-(column_1%self.tabstop))
                                    count_0 += width
                                    column_1 += width
                                    offset_2 += 1
                                else:
                                    count_0 += 1
                                    column_1 += 1
                                    offset_2 += 1
                            else:
                                break
                        if count_0 < 1:
                            offset_2 = -1
                            break

                        offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_inline_element(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                        if offset_2 == -1: break


                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                while True: # start reject
                                    children_4 = []
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    offset_4, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = self.parse_atx_heading_end(buf, offset_4, buf_eof, column_3, indent_column_3, prefix_0, children_4, partial_tab_offset_3, partial_tab_width_3)
                                    if offset_4 == -1: break


                                    break
                                if offset_4 != -1:
                                    offset_3 = -1
                                    break

                                offset_4 = offset_3
                                children_4 = []
                                while True: # start capture
                                    count_1 = 0
                                    while offset_4 < buf_eof:
                                        chr = buf[offset_4]
                                        if chr in ' \t':
                                            if chr == '\t':
                                                if offset_4 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                    width = partial_tab_width_2
                                                else:
                                                    width  = (self.tabstop-(column_2%self.tabstop))
                                                count_1 += width
                                                column_2 += width
                                                offset_4 += 1
                                            else:
                                                count_1 += 1
                                                column_2 += 1
                                                offset_4 += 1
                                        else:
                                            break

                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                if self.builder is not None:
                                    value_1 = self.builder['whitespace'](buf, offset_3, offset_4, children_4)
                                else:
                                    value_1 = self.Node('whitespace', offset_3, offset_4, children_4, None)
                                children_3.append(value_1)
                                offset_3 = offset_4

                                offset_3, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_inline_element(buf, offset_3, buf_eof, column_2, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
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
                            count_0 += 1
                        if offset_2 == -1:
                            break

                        count_0 = 0
                        while count_0 < 1:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if buf[offset_3:offset_3+1] == '\\':
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                if self.builder is not None:
                                    children_3.append('\\')
                                else:
                                    children_3.append(self.Node('value', offset_3, offset_3, (), '\\'))

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
                            break
                        if offset_2 == -1:
                            break

                        offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_atx_heading_end(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                        if offset_2 == -1: break



                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        column_0 = column_1
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

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_2 = self.builder['atx_heading'](buf, offset_0, offset_1, children_1)
            else:
                value_2 = self.Node('atx_heading', offset_0, offset_1, children_1, None)
            children_0.append(value_2)
            offset_0 = offset_1


            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_atx_heading_end(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = 0
            while count_0 < 1:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    count_1 = 0
                    while offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in ' \t':
                            if chr == '\t':
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
                    if count_1 < 1:
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
                            if buf[offset_2:offset_2+1] == '#':
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
                        indent_column_1 = indent_column_2
                        partial_tab_offset_1 = partial_tab_offset_2
                        partial_tab_width_1 = partial_tab_width_2
                        count_1 += 1
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
                break
            if offset_0 == -1:
                break

            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
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

            if offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in '\n':
                    offset_0 +=1
                    column_0 = 0
                    indent_column_0 = 0
                else:
                    offset_0 = -1
                    break


            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_setext_heading(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        if count_0 + width > 3:
                            new_width = 3 - count_0
                            count_0 += new_width
                            column_0 += new_width
                            partial_tab_offset_0 = offset_0
                            partial_tab_width_0 = width - new_width
                            break
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
                offset_1, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_para_line(buf, offset_1, buf_eof, column_0, indent_column_0, prefix_0, children_1, partial_tab_offset_0, partial_tab_width_0)
                if offset_1 == -1: break


                count_0 = 0
                while offset_1 < buf_eof:
                    chr = buf[offset_1]
                    if chr in ' \t':
                        if chr == '\t':
                            if offset_1 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                                width = partial_tab_width_0
                            else:
                                width  = (self.tabstop-(column_0%self.tabstop))
                            count_0 += width
                            column_0 += width
                            offset_1 += 1
                        else:
                            count_0 += 1
                            column_0 += 1
                            offset_1 += 1
                    else:
                        break

                if offset_1 < buf_eof:
                    chr = buf[offset_1]
                    if chr in '\n':
                        offset_1 +=1
                        column_0 = 0
                        indent_column_0 = 0
                    else:
                        offset_1 = -1
                        break
                else:
                    offset_1 = -1
                    break

                if not (column_0 == indent_column_0 == 0):
                    offset_1 = -1
                    break
                for indent in prefix_0:
                    _children, _prefix = [], []
                    offset_1, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = indent(buf, offset_1, buf_eof, column_0, indent_column_0, _prefix, _children, partial_tab_offset_0, partial_tab_width_0)
                    if _prefix or _children:
                       raise Exception('bar')
                    if offset_1 == -1:        break
                    indent_column_0 = column_0
                if offset_1 == -1:
                    break

                offset_1, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_setext_heading_line(buf, offset_1, buf_eof, column_0, indent_column_0, prefix_0, children_1, partial_tab_offset_0, partial_tab_width_0)
                if offset_1 == -1: break


                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['setext_heading'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('setext_heading', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1


            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_setext_heading_line(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        if count_0 + width > 3:
                            new_width = 3 - count_0
                            count_0 += new_width
                            column_0 += new_width
                            partial_tab_offset_0 = offset_0
                            partial_tab_width_0 = width - new_width
                            break
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break

            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            if buf[offset_2:offset_2+1] == '=':
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
                        indent_column_1 = indent_column_2
                        partial_tab_offset_1 = partial_tab_offset_2
                        partial_tab_width_1 = partial_tab_width_2
                        count_0 += 1
                    if count_0 < 1:
                        offset_1 = -1
                        break
                    if offset_1 == -1:
                        break

                    if self.builder is not None:
                        children_1.append(1)
                    else:
                        children_1.append(self.Node('value', offset_1, offset_1, (), 1))


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
                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            if buf[offset_2:offset_2+1] == '-':
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
                        indent_column_1 = indent_column_2
                        partial_tab_offset_1 = partial_tab_offset_2
                        partial_tab_width_1 = partial_tab_width_2
                        count_0 += 1
                    if count_0 < 1:
                        offset_1 = -1
                        break
                    if offset_1 == -1:
                        break

                    if self.builder is not None:
                        children_1.append(2)
                    else:
                        children_1.append(self.Node('value', offset_1, offset_1, (), 2))


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

            offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_line_end(buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0)
            if offset_0 == -1: break



            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_indented_code_block(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 4:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        if count_0 + width > 4:
                            new_width = 4 - count_0
                            count_0 += new_width
                            column_0 += new_width
                            partial_tab_offset_0 = offset_0
                            partial_tab_width_0 = width - new_width
                            break
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break
            if count_0 < 4:
                offset_0 = -1
                break

            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = column_0 - indent_column_0
                def _indent(buf, offset, buf_eof, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
                    saw_tab, saw_not_tab = False, False
                    while count > 0 and offset < buf_eof:
                        chr = buf[offset]
                        if chr in ' \t':
                            if not allow_mixed_indent:
                                if chr == '\t': saw_tab = True
                                else: saw_not_tab = True
                                if saw_tab and saw_not_tab:
                                     offset -1; break
                            if chr != '\t':
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
                        elif chr in '\n':
                            break
                        else:
                            offset = -1
                            break
                    return offset, column, indent_column, partial_tab_offset, partial_tab_width
                prefix_0.append(_indent)
                indent_column_0 = column_0
                while True:
                    offset_2 = offset_1
                    column_1 = column_0
                    while True: # start count
                        if offset_2 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            offset_2 += 1
                            column_1 += partial_tab_width_0

                        break
                    if offset_2 == -1:
                        offset_1 = -1; break
                    value_0 = column_1 - column_0
                    offset_1 = offset_2
                    column_0 = column_1

                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        if self.builder is not None:
                            children_2.append(value_0)
                        else:
                            children_2.append(self.Node('value', offset_2, offset_2, (), value_0))

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_1 = self.builder['partial_indent'](buf, offset_1, offset_2, children_2)
                    else:
                        value_1 = self.Node('partial_indent', offset_1, offset_2, children_2, None)
                    children_1.append(value_1)
                    offset_1 = offset_2

                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        count_0 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t':
                                if chr == '\t':
                                    if offset_2 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                                        width = partial_tab_width_0
                                    else:
                                        width  = (self.tabstop-(column_0%self.tabstop))
                                    count_0 += width
                                    column_0 += width
                                    offset_2 += 1
                                else:
                                    count_0 += 1
                                    column_0 += 1
                                    offset_2 += 1
                            else:
                                break

                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            column_1 = column_0
                            indent_column_1 = indent_column_0
                            partial_tab_offset_1 = partial_tab_offset_0
                            partial_tab_width_1 = partial_tab_width_0
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = ord(buf[offset_3])

                                if chr == 10:
                                    offset_3 = -1
                                    break
                                else:
                                    offset_3 += 1
                                    column_1 += 1

                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            column_0 = column_1
                            indent_column_0 = indent_column_1
                            partial_tab_offset_0 = partial_tab_offset_1
                            partial_tab_width_0 = partial_tab_width_1
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
                        value_2 = self.builder['code_line'](buf, offset_1, offset_2, children_2)
                    else:
                        value_2 = self.Node('code_line', offset_1, offset_2, children_2, None)
                    children_1.append(value_2)
                    offset_1 = offset_2

                    if offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in '\n':
                            offset_1 +=1
                            column_0 = 0
                            indent_column_0 = 0
                        else:
                            offset_1 = -1
                            break

                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        column_1 = column_0
                        indent_column_1 = indent_column_0
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True:
                            while True: # start choice
                                offset_3 = offset_2
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_3 = [] if children_2 is not None else None
                                while True: # case
                                    count_1 = 0
                                    while True:
                                        offset_4 = offset_3
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_4 = [] if children_3 is not None else None
                                        while True:
                                            if not (column_3 == indent_column_3 == 0):
                                                offset_4 = -1
                                                break
                                            for indent in prefix_0:
                                                _children, _prefix = [], []
                                                offset_4, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_4, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                                if _prefix or _children:
                                                   raise Exception('bar')
                                                if offset_4 == -1:        break
                                                indent_column_3 = column_3
                                            if offset_4 == -1:
                                                break

                                            offset_5 = offset_4
                                            children_5 = []
                                            while True: # start capture
                                                count_2 = 0
                                                while offset_5 < buf_eof:
                                                    chr = buf[offset_5]
                                                    if chr in ' \t':
                                                        if chr == '\t':
                                                            if offset_5 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                                width = partial_tab_width_3
                                                            else:
                                                                width  = (self.tabstop-(column_3%self.tabstop))
                                                            count_2 += width
                                                            column_3 += width
                                                            offset_5 += 1
                                                        else:
                                                            count_2 += 1
                                                            column_3 += 1
                                                            offset_5 += 1
                                                    else:
                                                        break

                                                break
                                            if offset_5 == -1:
                                                offset_4 = -1
                                                break
                                            if self.builder is not None:
                                                value_3 = self.builder['code_line'](buf, offset_4, offset_5, children_5)
                                            else:
                                                value_3 = self.Node('code_line', offset_4, offset_5, children_5, None)
                                            children_4.append(value_3)
                                            offset_4 = offset_5

                                            if offset_4 < buf_eof:
                                                chr = buf[offset_4]
                                                if chr in '\n':
                                                    offset_4 +=1
                                                    column_3 = 0
                                                    indent_column_3 = 0
                                                else:
                                                    offset_4 = -1
                                                    break
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
                                        count_1 += 1
                                    if count_1 < 1:
                                        offset_3 = -1
                                        break
                                    if offset_3 == -1:
                                        break

                                    while True: # start reject
                                        children_4 = []
                                        offset_4 = offset_3
                                        column_3 = column_2
                                        column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        if not (column_3 == column_3 == 0):
                                            offset_4 = -1
                                            break
                                        for indent in prefix_0:
                                            _children, _prefix = [], []
                                            offset_4, column_3, column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_4, buf_eof, column_3, column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                            if _prefix or _children:
                                               raise Exception('bar')
                                            if offset_4 == -1:        break
                                            column_3 = column_3
                                        if offset_4 == -1:
                                            break

                                        count_1 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t':
                                                if chr == '\t':
                                                    if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                        width = partial_tab_width_3
                                                    else:
                                                        width  = (self.tabstop-(column_3%self.tabstop))
                                                    count_1 += width
                                                    column_3 += width
                                                    offset_4 += 1
                                                else:
                                                    count_1 += 1
                                                    column_3 += 1
                                                    offset_4 += 1
                                            else:
                                                break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if chr == 10:
                                            offset_4 = -1
                                            break
                                        else:
                                            offset_4 += 1
                                            column_3 += 1

                                        break
                                    if offset_4 == -1:
                                        offset_3 = -1
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
                                    if not (column_2 == indent_column_2 == 0):
                                        offset_3 = -1
                                        break
                                    for indent in prefix_0:
                                        _children, _prefix = [], []
                                        offset_3, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = indent(buf, offset_3, buf_eof, column_2, indent_column_2, _prefix, _children, partial_tab_offset_2, partial_tab_width_2)
                                        if _prefix or _children:
                                           raise Exception('bar')
                                        if offset_3 == -1:        break
                                        indent_column_2 = column_2
                                    if offset_3 == -1:
                                        break

                                    offset_4 = offset_3
                                    column_3 = column_2
                                    while True: # start count
                                        if offset_4 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                            offset_4 += 1
                                            column_3 += partial_tab_width_2

                                        break
                                    if offset_4 == -1:
                                        offset_3 = -1; break
                                    value_4 = column_3 - column_2
                                    offset_3 = offset_4
                                    column_2 = column_3

                                    offset_4 = offset_3
                                    children_4 = []
                                    while True: # start capture
                                        if self.builder is not None:
                                            children_4.append(value_4)
                                        else:
                                            children_4.append(self.Node('value', offset_4, offset_4, (), value_4))

                                        break
                                    if offset_4 == -1:
                                        offset_3 = -1
                                        break
                                    if self.builder is not None:
                                        value_5 = self.builder['partial_indent'](buf, offset_3, offset_4, children_4)
                                    else:
                                        value_5 = self.Node('partial_indent', offset_3, offset_4, children_4, None)
                                    children_3.append(value_5)
                                    offset_3 = offset_4

                                    offset_4 = offset_3
                                    children_4 = []
                                    while True: # start capture
                                        count_1 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t':
                                                if chr == '\t':
                                                    if offset_4 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                        width = partial_tab_width_2
                                                    else:
                                                        width  = (self.tabstop-(column_2%self.tabstop))
                                                    count_1 += width
                                                    column_2 += width
                                                    offset_4 += 1
                                                else:
                                                    count_1 += 1
                                                    column_2 += 1
                                                    offset_4 += 1
                                            else:
                                                break

                                        count_1 = 0
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

                                                chr = ord(buf[offset_5])

                                                if chr == 10:
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
                                            count_1 += 1
                                        if count_1 < 1:
                                            offset_4 = -1
                                            break
                                        if offset_4 == -1:
                                            break

                                        break
                                    if offset_4 == -1:
                                        offset_3 = -1
                                        break
                                    if self.builder is not None:
                                        value_6 = self.builder['code_line'](buf, offset_3, offset_4, children_4)
                                    else:
                                        value_6 = self.Node('code_line', offset_3, offset_4, children_4, None)
                                    children_3.append(value_6)
                                    offset_3 = offset_4

                                    if offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in '\n':
                                            offset_3 +=1
                                            column_2 = 0
                                            indent_column_2 = 0
                                        else:
                                            offset_3 = -1
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
                    if offset_1 == -1:
                        break

                    break
                prefix_0.pop()
                if offset_1 == -1: break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_7 = self.builder['indented_code'](buf, offset_0, offset_1, children_1)
            else:
                value_7 = self.Node('indented_code', offset_0, offset_1, children_1, None)
            children_0.append(value_7)
            offset_0 = offset_1


            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_fenced_code_block(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        if count_0 + width > 3:
                            new_width = 3 - count_0
                            count_0 += new_width
                            column_0 += new_width
                            partial_tab_offset_0 = offset_0
                            partial_tab_width_0 = width - new_width
                            break
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
                while True: # start choice
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True: # case
                        offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_tilde_code_block(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                        if offset_2 == -1: break



                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        column_0 = column_1
                        indent_column_0 = indent_column_1
                        partial_tab_offset_0 = partial_tab_offset_1
                        partial_tab_width_0 = partial_tab_width_1
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True: # case
                        offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_backtick_code_block(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                        if offset_2 == -1: break



                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        column_0 = column_1
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

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['fenced_code'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('fenced_code', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1


            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_start_fenced_block(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        if count_0 + width > 3:
                            new_width = 3 - count_0
                            count_0 += new_width
                            column_0 += new_width
                            partial_tab_offset_0 = offset_0
                            partial_tab_width_0 = width - new_width
                            break
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break

            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    if buf[offset_1:offset_1+3] == '```':
                        offset_1 += 3
                        column_1 += 3
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
                    if buf[offset_1:offset_1+3] == '~~~':
                        offset_1 += 3
                        column_1 += 3
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

    def parse_backtick_code_block(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            offset_1 = offset_0
            column_1 = column_0
            while True: # start count
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    column_2 = column_1
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_1 = [] if children_0 is not None else None
                    while True:
                        if buf[offset_2:offset_2+1] == '`':
                            offset_2 += 1
                            column_2 += 1
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        break
                    if offset_1 == offset_2: break
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    offset_1 = offset_2
                    column_1 = column_2
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    count_0 += 1
                if count_0 < 3:
                    offset_1 = -1
                    break
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1; break
            value_0 = buf[offset_0:offset_1].count('`')
            offset_0 = offset_1
            column_0 = column_1

            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        while True: # start reject
                            children_3 = []
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            if buf[offset_3:offset_3+1] == '`':
                                offset_3 += 1
                                column_2 += 1
                            else:
                                offset_3 = -1
                                break

                            break
                        if offset_3 != -1:
                            offset_2 = -1
                            break

                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break

                        chr = ord(buf[offset_2])

                        if chr == 10:
                            offset_2 = -1
                            break
                        else:
                            offset_2 += 1
                            column_1 += 1

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
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_1 = self.builder['info'](buf, offset_0, offset_1, children_1)
            else:
                value_1 = self.Node('info', offset_0, offset_1, children_1, None)
            children_0.append(value_1)
            offset_0 = offset_1

            offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_line_end(buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0)
            if offset_0 == -1: break


            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    if not (column_1 == indent_column_1 == 0):
                        offset_1 = -1
                        break
                    for indent in prefix_0:
                        _children, _prefix = [], []
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_1, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                        if _prefix or _children:
                           raise Exception('bar')
                        if offset_1 == -1:        break
                        indent_column_1 = column_1
                    if offset_1 == -1:
                        break

                    while True: # start reject
                        children_2 = []
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        count_1 = 0
                        while offset_2 < buf_eof and count_1 < 3:
                            chr = buf[offset_2]
                            if chr in ' \t':
                                if chr == '\t':
                                    if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                        width = partial_tab_width_2
                                    else:
                                        width  = (self.tabstop-(column_2%self.tabstop))
                                    if count_1 + width > 3:
                                        new_width = 3 - count_1
                                        count_1 += new_width
                                        column_2 += new_width
                                        partial_tab_offset_2 = offset_2
                                        partial_tab_width_2 = width - new_width
                                        break
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
                            indent_column_3 = indent_column_2
                            partial_tab_offset_3 = partial_tab_offset_2
                            partial_tab_width_3 = partial_tab_width_2
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if buf[offset_3:offset_3+1] == '`':
                                    offset_3 += 1
                                    column_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        if chr == '\t':
                                            if offset_3 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                width = partial_tab_width_3
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
                            indent_column_2 = indent_column_3
                            partial_tab_offset_2 = partial_tab_offset_3
                            partial_tab_width_2 = partial_tab_width_3
                            count_1 += 1
                        if count_1 < value_0:
                            offset_2 = -1
                            break
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 != -1:
                        offset_1 = -1
                        break

                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = ord(buf[offset_3])

                                if chr == 10:
                                    offset_3 = -1
                                    break
                                else:
                                    offset_3 += 1
                                    column_2 += 1

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

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_2 = self.builder['text'](buf, offset_1, offset_2, children_2)
                    else:
                        value_2 = self.Node('text', offset_1, offset_2, children_2, None)
                    children_1.append(value_2)
                    offset_1 = offset_2

                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_line_end(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    if offset_1 != buf_eof:
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
                    if not (column_1 == indent_column_1 == 0):
                        offset_1 = -1
                        break
                    for indent in prefix_0:
                        _children, _prefix = [], []
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_1, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                        if _prefix or _children:
                           raise Exception('bar')
                        if offset_1 == -1:        break
                        indent_column_1 = column_1
                    if offset_1 == -1:
                        break

                    count_0 = 0
                    while offset_1 < buf_eof and count_0 < 3:
                        chr = buf[offset_1]
                        if chr in ' \t':
                            if chr == '\t':
                                if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                    width = partial_tab_width_1
                                else:
                                    width  = (self.tabstop-(column_1%self.tabstop))
                                if count_0 + width > 3:
                                    new_width = 3 - count_0
                                    count_0 += new_width
                                    column_1 += new_width
                                    partial_tab_offset_1 = offset_1
                                    partial_tab_width_1 = width - new_width
                                    break
                                count_0 += width
                                column_1 += width
                                offset_1 += 1
                            else:
                                count_0 += 1
                                column_1 += 1
                                offset_1 += 1
                        else:
                            break

                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            count_1 = 0
                            while offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr in ' \t':
                                    if chr == '\t':
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

                            if buf[offset_2:offset_2+1] == '`':
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
                        indent_column_1 = indent_column_2
                        partial_tab_offset_1 = partial_tab_offset_2
                        partial_tab_width_1 = partial_tab_width_2
                        count_0 += 1
                    if count_0 < value_0:
                        offset_1 = -1
                        break
                    if offset_1 == -1:
                        break

                    count_0 = 0
                    while offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in ' \t':
                            if chr == '\t':
                                if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                    width = partial_tab_width_1
                                else:
                                    width  = (self.tabstop-(column_1%self.tabstop))
                                count_0 += width
                                column_1 += width
                                offset_1 += 1
                            else:
                                count_0 += 1
                                column_1 += 1
                                offset_1 += 1
                        else:
                            break

                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_line_end(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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

    def parse_tilde_code_block(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            offset_1 = offset_0
            column_1 = column_0
            while True: # start count
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    column_2 = column_1
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_1 = [] if children_0 is not None else None
                    while True:
                        if buf[offset_2:offset_2+1] == '~':
                            offset_2 += 1
                            column_2 += 1
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        break
                    if offset_1 == offset_2: break
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    offset_1 = offset_2
                    column_1 = column_2
                    indent_column_0 = indent_column_1
                    partial_tab_offset_0 = partial_tab_offset_1
                    partial_tab_width_0 = partial_tab_width_1
                    count_0 += 1
                if count_0 < 3:
                    offset_1 = -1
                    break
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1; break
            value_0 = buf[offset_0:offset_1].count('~')
            offset_0 = offset_1
            column_0 = column_1

            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break

                        chr = ord(buf[offset_2])

                        if chr == 10:
                            offset_2 = -1
                            break
                        else:
                            offset_2 += 1
                            column_1 += 1

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
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_1 = self.builder['info'](buf, offset_0, offset_1, children_1)
            else:
                value_1 = self.Node('info', offset_0, offset_1, children_1, None)
            children_0.append(value_1)
            offset_0 = offset_1

            offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_line_end(buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0)
            if offset_0 == -1: break


            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    if not (column_1 == indent_column_1 == 0):
                        offset_1 = -1
                        break
                    for indent in prefix_0:
                        _children, _prefix = [], []
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_1, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                        if _prefix or _children:
                           raise Exception('bar')
                        if offset_1 == -1:        break
                        indent_column_1 = column_1
                    if offset_1 == -1:
                        break

                    while True: # start reject
                        children_2 = []
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        count_1 = 0
                        while offset_2 < buf_eof and count_1 < 3:
                            chr = buf[offset_2]
                            if chr in ' \t':
                                if chr == '\t':
                                    if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                        width = partial_tab_width_2
                                    else:
                                        width  = (self.tabstop-(column_2%self.tabstop))
                                    if count_1 + width > 3:
                                        new_width = 3 - count_1
                                        count_1 += new_width
                                        column_2 += new_width
                                        partial_tab_offset_2 = offset_2
                                        partial_tab_width_2 = width - new_width
                                        break
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
                            indent_column_3 = indent_column_2
                            partial_tab_offset_3 = partial_tab_offset_2
                            partial_tab_width_3 = partial_tab_width_2
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if buf[offset_3:offset_3+1] == '~':
                                    offset_3 += 1
                                    column_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        if chr == '\t':
                                            if offset_3 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                width = partial_tab_width_3
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
                            indent_column_2 = indent_column_3
                            partial_tab_offset_2 = partial_tab_offset_3
                            partial_tab_width_2 = partial_tab_width_3
                            count_1 += 1
                        if count_1 < value_0:
                            offset_2 = -1
                            break
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 != -1:
                        offset_1 = -1
                        break

                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = ord(buf[offset_3])

                                if chr == 10:
                                    offset_3 = -1
                                    break
                                else:
                                    offset_3 += 1
                                    column_2 += 1

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

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_2 = self.builder['text'](buf, offset_1, offset_2, children_2)
                    else:
                        value_2 = self.Node('text', offset_1, offset_2, children_2, None)
                    children_1.append(value_2)
                    offset_1 = offset_2

                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_line_end(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    if offset_1 != buf_eof:
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
                    if not (column_1 == indent_column_1 == 0):
                        offset_1 = -1
                        break
                    for indent in prefix_0:
                        _children, _prefix = [], []
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_1, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                        if _prefix or _children:
                           raise Exception('bar')
                        if offset_1 == -1:        break
                        indent_column_1 = column_1
                    if offset_1 == -1:
                        break

                    count_0 = 0
                    while offset_1 < buf_eof and count_0 < 3:
                        chr = buf[offset_1]
                        if chr in ' \t':
                            if chr == '\t':
                                if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                    width = partial_tab_width_1
                                else:
                                    width  = (self.tabstop-(column_1%self.tabstop))
                                if count_0 + width > 3:
                                    new_width = 3 - count_0
                                    count_0 += new_width
                                    column_1 += new_width
                                    partial_tab_offset_1 = offset_1
                                    partial_tab_width_1 = width - new_width
                                    break
                                count_0 += width
                                column_1 += width
                                offset_1 += 1
                            else:
                                count_0 += 1
                                column_1 += 1
                                offset_1 += 1
                        else:
                            break

                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True:
                            count_1 = 0
                            while offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr in ' \t':
                                    if chr == '\t':
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

                            if buf[offset_2:offset_2+1] == '~':
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
                        indent_column_1 = indent_column_2
                        partial_tab_offset_1 = partial_tab_offset_2
                        partial_tab_width_1 = partial_tab_width_2
                        count_0 += 1
                    if count_0 < value_0:
                        offset_1 = -1
                        break
                    if offset_1 == -1:
                        break

                    count_0 = 0
                    while offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in ' \t':
                            if chr == '\t':
                                if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                    width = partial_tab_width_1
                                else:
                                    width  = (self.tabstop-(column_1%self.tabstop))
                                count_0 += width
                                column_1 += width
                                offset_1 += 1
                            else:
                                count_0 += 1
                                column_1 += 1
                                offset_1 += 1
                        else:
                            break

                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_line_end(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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

    def parse_blockquote_prefix(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_start_blockquote(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    while True: # start reject
                        children_2 = []
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        while True: # start choice
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_3 = indent_column_2
                            partial_tab_offset_3 = partial_tab_offset_2
                            partial_tab_width_3 = partial_tab_width_2
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                count_0 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        if chr == '\t':
                                            if offset_3 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                width = partial_tab_width_3
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

                                if offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in '\n':
                                        offset_3 +=1
                                        column_3 = 0
                                        indent_column_3 = 0
                                    else:
                                        offset_3 = -1
                                        break
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
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_3 = indent_column_2
                            partial_tab_offset_3 = partial_tab_offset_2
                            partial_tab_width_3 = partial_tab_width_2
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                count_0 = 0
                                while offset_3 < buf_eof and count_0 < 4:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        if chr == '\t':
                                            if offset_3 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                width = partial_tab_width_3
                                            else:
                                                width  = (self.tabstop-(column_3%self.tabstop))
                                            if count_0 + width > 4:
                                                new_width = 4 - count_0
                                                count_0 += new_width
                                                column_3 += new_width
                                                partial_tab_offset_3 = offset_3
                                                partial_tab_width_3 = width - new_width
                                                break
                                            count_0 += width
                                            column_3 += width
                                            offset_3 += 1
                                        else:
                                            count_0 += 1
                                            column_3 += 1
                                            offset_3 += 1
                                    else:
                                        break
                                if count_0 < 4:
                                    offset_3 = -1
                                    break

                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = ord(buf[offset_3])

                                if chr == 32:
                                    offset_3 = -1
                                    break
                                elif chr == 9:
                                    offset_3 = -1
                                    break
                                elif chr == 10:
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
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_3 = indent_column_2
                            partial_tab_offset_3 = partial_tab_offset_2
                            partial_tab_width_3 = partial_tab_width_2
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                offset_3, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = self.parse_thematic_break(buf, offset_3, buf_eof, column_3, indent_column_3, prefix_0, children_3, partial_tab_offset_3, partial_tab_width_3)
                                if offset_3 == -1: break



                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                column_2 = column_3
                                indent_column_2 = indent_column_3
                                partial_tab_offset_2 = partial_tab_offset_3
                                partial_tab_width_2 = partial_tab_width_3
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_3 = indent_column_2
                            partial_tab_offset_3 = partial_tab_offset_2
                            partial_tab_width_3 = partial_tab_width_2
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                offset_3, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = self.parse_atx_heading(buf, offset_3, buf_eof, column_3, indent_column_3, prefix_0, children_3, partial_tab_offset_3, partial_tab_width_3)
                                if offset_3 == -1: break



                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                column_2 = column_3
                                indent_column_2 = indent_column_3
                                partial_tab_offset_2 = partial_tab_offset_3
                                partial_tab_width_2 = partial_tab_width_3
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_3 = indent_column_2
                            partial_tab_offset_3 = partial_tab_offset_2
                            partial_tab_width_3 = partial_tab_width_2
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                offset_3, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = self.parse_start_fenced_block(buf, offset_3, buf_eof, column_3, indent_column_3, prefix_0, children_3, partial_tab_offset_3, partial_tab_width_3)
                                if offset_3 == -1: break



                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                column_2 = column_3
                                indent_column_2 = indent_column_3
                                partial_tab_offset_2 = partial_tab_offset_3
                                partial_tab_width_2 = partial_tab_width_3
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_3 = indent_column_2
                            partial_tab_offset_3 = partial_tab_offset_2
                            partial_tab_width_3 = partial_tab_width_2
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                offset_3, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = self.parse_start_list(buf, offset_3, buf_eof, column_3, indent_column_3, prefix_0, children_3, partial_tab_offset_3, partial_tab_width_3)
                                if offset_3 == -1: break



                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                column_2 = column_3
                                indent_column_2 = indent_column_3
                                partial_tab_offset_2 = partial_tab_offset_3
                                partial_tab_width_2 = partial_tab_width_3
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            column_3 = column_2
                            indent_column_3 = indent_column_2
                            partial_tab_offset_3 = partial_tab_offset_2
                            partial_tab_width_3 = partial_tab_width_2
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                offset_3, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = self.parse_setext_heading_line(buf, offset_3, buf_eof, column_3, indent_column_3, prefix_0, children_3, partial_tab_offset_3, partial_tab_width_3)
                                if offset_3 == -1: break



                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                column_2 = column_3
                                indent_column_2 = indent_column_3
                                partial_tab_offset_2 = partial_tab_offset_3
                                partial_tab_width_2 = partial_tab_width_3
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_2 = -1 # no more choices
                            break # end choice
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 != -1:
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

    def parse_start_blockquote(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        if count_0 + width > 3:
                            new_width = 3 - count_0
                            count_0 += new_width
                            column_0 += new_width
                            partial_tab_offset_0 = offset_0
                            partial_tab_width_0 = width - new_width
                            break
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break

            if buf[offset_0:offset_0+1] == '>':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break

            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    while True: # start reject
                        children_2 = []
                        offset_2 = offset_1
                        column_2 = column_1
                        column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        count_0 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t':
                                if chr == '\t':
                                    if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                        width = partial_tab_width_2
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

                        if offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in '\n':
                                offset_2 +=1
                                column_2 = 0
                                column_2 = 0
                            else:
                                offset_2 = -1
                                break

                        break
                    if offset_2 == -1:
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
                    count_0 = 0
                    while offset_1 < buf_eof and count_0 < 1:
                        chr = buf[offset_1]
                        if chr in ' \t':
                            if chr == '\t':
                                if offset_1 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                    width = partial_tab_width_1
                                else:
                                    width  = (self.tabstop-(column_1%self.tabstop))
                                if count_0 + width > 1:
                                    new_width = 1 - count_0
                                    count_0 += new_width
                                    column_1 += new_width
                                    partial_tab_offset_1 = offset_1
                                    partial_tab_width_1 = width - new_width
                                    break
                                count_0 += width
                                column_1 += width
                                offset_1 += 1
                            else:
                                count_0 += 1
                                column_1 += 1
                                offset_1 += 1
                        else:
                            break

                    while True: # start reject
                        children_2 = []
                        offset_2 = offset_1
                        column_2 = column_1
                        column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break

                        chr = ord(buf[offset_2])

                        if chr == 10:
                            offset_2 = -1
                            break
                        else:
                            offset_2 += 1
                            column_2 += 1

                        break
                    if offset_2 == -1:
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

    def parse_blockquote(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                offset_1, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_start_blockquote(buf, offset_1, buf_eof, column_0, indent_column_0, prefix_0, children_1, partial_tab_offset_0, partial_tab_width_0)
                if offset_1 == -1: break


                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        prefix_0.append(self.parse_blockquote_prefix)
                        indent_column_1 = column_1
                        while True:
                            offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_block_element(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
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
                                    if not (column_2 == indent_column_2 == 0):
                                        offset_3 = -1
                                        break
                                    for indent in prefix_0:
                                        _children, _prefix = [], []
                                        offset_3, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = indent(buf, offset_3, buf_eof, column_2, indent_column_2, _prefix, _children, partial_tab_offset_2, partial_tab_width_2)
                                        if _prefix or _children:
                                           raise Exception('bar')
                                        if offset_3 == -1:        break
                                        indent_column_2 = column_2
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
                                            offset_4, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = self.parse_block_element(buf, offset_4, buf_eof, column_3, indent_column_3, prefix_0, children_4, partial_tab_offset_3, partial_tab_width_3)
                                            if offset_4 == -1: break



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
                                            count_2 = 0
                                            while offset_4 < buf_eof:
                                                chr = buf[offset_4]
                                                if chr in ' \t':
                                                    if chr == '\t':
                                                        if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                            width = partial_tab_width_3
                                                        else:
                                                            width  = (self.tabstop-(column_3%self.tabstop))
                                                        count_2 += width
                                                        column_3 += width
                                                        offset_4 += 1
                                                    else:
                                                        count_2 += 1
                                                        column_3 += 1
                                                        offset_4 += 1
                                                else:
                                                    break

                                            if offset_4 < buf_eof:
                                                chr = buf[offset_4]
                                                if chr in '\n':
                                                    offset_4 +=1
                                                    column_3 = 0
                                                    indent_column_3 = 0
                                                else:
                                                    offset_4 = -1
                                                    break
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
                                count_1 += 1
                            if offset_2 == -1:
                                break

                            break
                        prefix_0.pop()
                        if offset_2 == -1: break

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
            if self.builder is not None:
                value_0 = self.builder['blockquote'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('blockquote', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_start_list(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        if count_0 + width > 3:
                            new_width = 3 - count_0
                            count_0 += new_width
                            column_0 += new_width
                            partial_tab_offset_0 = offset_0
                            partial_tab_width_0 = width - new_width
                            break
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break

            if buf[offset_0:offset_0+1] == '-':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break

            count_0 = 0
            while offset_0 < buf_eof and count_0 < 1:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        if count_0 + width > 1:
                            new_width = 1 - count_0
                            count_0 += new_width
                            column_0 += new_width
                            partial_tab_offset_0 = offset_0
                            partial_tab_width_0 = width - new_width
                            break
                        count_0 += width
                        column_0 += width
                        offset_0 += 1
                    else:
                        count_0 += 1
                        column_0 += 1
                        offset_0 += 1
                else:
                    break
            if count_0 < 1:
                offset_0 = -1
                break


            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_block_list(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                offset_1, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_start_list(buf, offset_1, buf_eof, column_0, indent_column_0, prefix_0, children_1, partial_tab_offset_0, partial_tab_width_0)
                if offset_1 == -1: break


                offset_2 = offset_1
                children_2 = []
                while True: # start capture
                    offset_2, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_list_item(buf, offset_2, buf_eof, column_0, indent_column_0, prefix_0, children_2, partial_tab_offset_0, partial_tab_width_0)
                    if offset_2 == -1: break


                    break
                if offset_2 == -1:
                    offset_1 = -1
                    break
                if self.builder is not None:
                    value_0 = self.builder['list_item'](buf, offset_1, offset_2, children_2)
                else:
                    value_0 = self.Node('list_item', offset_1, offset_2, children_2, None)
                children_1.append(value_0)
                offset_1 = offset_2

                count_0 = 0
                while True:
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        if not (column_1 == indent_column_1 == 0):
                            offset_2 = -1
                            break
                        for indent in prefix_0:
                            _children, _prefix = [], []
                            offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_2, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                            if _prefix or _children:
                               raise Exception('bar')
                            if offset_2 == -1:        break
                            indent_column_1 = column_1
                        if offset_2 == -1:
                            break

                        while True: # start choice
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                count_1 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        if chr == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_1 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_1 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                if offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in '\n':
                                        offset_3 +=1
                                        column_2 = 0
                                        indent_column_2 = 0
                                    else:
                                        offset_3 = -1
                                        break
                                else:
                                    offset_3 = -1
                                    break

                                offset_4 = offset_3
                                children_4 = []
                                while True: # start capture
                                    count_1 = 0
                                    while True:
                                        offset_5 = offset_4
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            if not (column_3 == indent_column_3 == 0):
                                                offset_5 = -1
                                                break
                                            for indent in prefix_0:
                                                _children, _prefix = [], []
                                                offset_5, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_5, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                                if _prefix or _children:
                                                   raise Exception('bar')
                                                if offset_5 == -1:        break
                                                indent_column_3 = column_3
                                            if offset_5 == -1:
                                                break

                                            count_2 = 0
                                            while offset_5 < buf_eof:
                                                chr = buf[offset_5]
                                                if chr in ' \t':
                                                    if chr == '\t':
                                                        if offset_5 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                            width = partial_tab_width_3
                                                        else:
                                                            width  = (self.tabstop-(column_3%self.tabstop))
                                                        count_2 += width
                                                        column_3 += width
                                                        offset_5 += 1
                                                    else:
                                                        count_2 += 1
                                                        column_3 += 1
                                                        offset_5 += 1
                                                else:
                                                    break

                                            if offset_5 < buf_eof:
                                                chr = buf[offset_5]
                                                if chr in '\n':
                                                    offset_5 +=1
                                                    column_3 = 0
                                                    indent_column_3 = 0
                                                else:
                                                    offset_5 = -1
                                                    break
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
                                        column_2 = column_3
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        count_1 += 1
                                    if offset_4 == -1:
                                        break

                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                if self.builder is not None:
                                    value_1 = self.builder['empty'](buf, offset_3, offset_4, children_4)
                                else:
                                    value_1 = self.Node('empty', offset_3, offset_4, children_4, None)
                                children_3.append(value_1)
                                offset_3 = offset_4

                                while True: # start reject
                                    children_4 = []
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    if not (column_3 == column_3 == 0):
                                        offset_4 = -1
                                        break
                                    for indent in prefix_0:
                                        _children, _prefix = [], []
                                        offset_4, column_3, column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_4, buf_eof, column_3, column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                        if _prefix or _children:
                                           raise Exception('bar')
                                        if offset_4 == -1:        break
                                        column_3 = column_3
                                    if offset_4 == -1:
                                        break

                                    count_1 = 0
                                    while offset_4 < buf_eof and count_1 < 3:
                                        chr = buf[offset_4]
                                        if chr in ' \t':
                                            if chr == '\t':
                                                if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                    width = partial_tab_width_3
                                                else:
                                                    width  = (self.tabstop-(column_3%self.tabstop))
                                                if count_1 + width > 3:
                                                    new_width = 3 - count_1
                                                    count_1 += new_width
                                                    column_3 += new_width
                                                    partial_tab_offset_3 = offset_4
                                                    partial_tab_width_3 = width - new_width
                                                    break
                                                count_1 += width
                                                column_3 += width
                                                offset_4 += 1
                                            else:
                                                count_1 += 1
                                                column_3 += 1
                                                offset_4 += 1
                                        else:
                                            break

                                    if buf[offset_4:offset_4+1] == '-':
                                        offset_4 += 1
                                        column_3 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
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
                                count_1 = 0
                                while offset_3 < buf_eof and count_1 < 3:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        if chr == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            if count_1 + width > 3:
                                                new_width = 3 - count_1
                                                count_1 += new_width
                                                column_2 += new_width
                                                partial_tab_offset_2 = offset_3
                                                partial_tab_width_2 = width - new_width
                                                break
                                            count_1 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_1 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                if buf[offset_3:offset_3+1] == '-':
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_1 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        if chr == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_1 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_1 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break
                                if count_1 < 1:
                                    offset_3 = -1
                                    break

                                offset_4 = offset_3
                                children_4 = []
                                while True: # start capture
                                    offset_4, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_list_item(buf, offset_4, buf_eof, column_2, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                    if offset_4 == -1: break


                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                if self.builder is not None:
                                    value_2 = self.builder['list_item'](buf, offset_3, offset_4, children_4)
                                else:
                                    value_2 = self.Node('list_item', offset_3, offset_4, children_4, None)
                                children_3.append(value_2)
                                offset_3 = offset_4


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
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_3 = self.builder['block_list'](buf, offset_0, offset_1, children_1)
            else:
                value_3 = self.Node('block_list', offset_0, offset_1, children_1, None)
            children_0.append(value_3)
            offset_0 = offset_1

            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_list_item(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = column_0 - indent_column_0
            def _indent(buf, offset, buf_eof, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
                saw_tab, saw_not_tab = False, False
                while count > 0 and offset < buf_eof:
                    chr = buf[offset]
                    if chr in ' \t':
                        if not allow_mixed_indent:
                            if chr == '\t': saw_tab = True
                            else: saw_not_tab = True
                            if saw_tab and saw_not_tab:
                                 offset -1; break
                        if chr != '\t':
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
                    elif chr in '\n':
                        break
                    else:
                        offset = -1
                        break
                return offset, column, indent_column, partial_tab_offset, partial_tab_width
            prefix_0.append(_indent)
            indent_column_0 = column_0
            while True:
                offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_block_element(buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0)
                if offset_0 == -1: break


                count_0 = 0
                while True:
                    offset_1 = offset_0
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_1 = [] if children_0 is not None else None
                    while True:
                        if not (column_1 == indent_column_1 == 0):
                            offset_1 = -1
                            break
                        for indent in prefix_0:
                            _children, _prefix = [], []
                            offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_1, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                            if _prefix or _children:
                               raise Exception('bar')
                            if offset_1 == -1:        break
                            indent_column_1 = column_1
                        if offset_1 == -1:
                            break

                        while True: # start choice
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_2 = [] if children_1 is not None else None
                            while True: # case
                                offset_2, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_block_element(buf, offset_2, buf_eof, column_2, indent_column_2, prefix_0, children_2, partial_tab_offset_2, partial_tab_width_2)
                                if offset_2 == -1: break



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
                                count_1 = 0
                                while True:
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_3 = [] if children_2 is not None else None
                                    while True:
                                        if not (column_3 == indent_column_3 == 0):
                                            offset_3 = -1
                                            break
                                        for indent in prefix_0:
                                            _children, _prefix = [], []
                                            offset_3, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_3, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                            if _prefix or _children:
                                               raise Exception('bar')
                                            if offset_3 == -1:        break
                                            indent_column_3 = column_3
                                        if offset_3 == -1:
                                            break

                                        count_2 = 0
                                        while offset_3 < buf_eof:
                                            chr = buf[offset_3]
                                            if chr in ' \t':
                                                if chr == '\t':
                                                    if offset_3 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                        width = partial_tab_width_3
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

                                        if offset_3 < buf_eof:
                                            chr = buf[offset_3]
                                            if chr in '\n':
                                                offset_3 +=1
                                                column_3 = 0
                                                indent_column_3 = 0
                                            else:
                                                offset_3 = -1
                                                break
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
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    count_1 += 1
                                if offset_2 == -1:
                                    break

                                while True: # start reject
                                    children_3 = []
                                    offset_3 = offset_2
                                    column_3 = column_2
                                    column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    if not (column_3 == column_3 == 0):
                                        offset_3 = -1
                                        break
                                    for indent in prefix_0:
                                        _children, _prefix = [], []
                                        offset_3, column_3, column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_3, buf_eof, column_3, column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                        if _prefix or _children:
                                           raise Exception('bar')
                                        if offset_3 == -1:        break
                                        column_3 = column_3
                                    if offset_3 == -1:
                                        break

                                    break
                                if offset_3 == -1:
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
            prefix_0.pop()
            if offset_0 == -1: break

            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_para(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
                        if offset_0 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                            width = partial_tab_width_0
                        else:
                            width  = (self.tabstop-(column_0%self.tabstop))
                        if count_0 + width > 3:
                            new_width = 3 - count_0
                            count_0 += new_width
                            column_0 += new_width
                            partial_tab_offset_0 = offset_0
                            partial_tab_width_0 = width - new_width
                            break
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
            children_1 = [] if children_0 is not None else None
            count_0 = ('memo_0', offset_0)
            if count_0 in self.cache:
                offset_1, column_0, indent_column_0, children_1, partial_tab_offset_0, partial_tab_width_0 = self.cache[count_0]
            else:
                while True:
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        offset_2, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_inline_element(buf, offset_2, buf_eof, column_0, indent_column_0, prefix_0, children_2, partial_tab_offset_0, partial_tab_width_0)
                        if offset_2 == -1: break


                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            column_1 = column_0
                            indent_column_1 = indent_column_0
                            partial_tab_offset_1 = partial_tab_offset_0
                            partial_tab_width_1 = partial_tab_width_0
                            children_3 = [] if children_2 is not None else None
                            while True:
                                while True: # start choice
                                    offset_4 = offset_3
                                    column_2 = column_1
                                    indent_column_2 = indent_column_1
                                    partial_tab_offset_2 = partial_tab_offset_1
                                    partial_tab_width_2 = partial_tab_width_1
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        while True: # start choice
                                            offset_5 = offset_4
                                            column_3 = column_2
                                            indent_column_3 = indent_column_2
                                            partial_tab_offset_3 = partial_tab_offset_2
                                            partial_tab_width_3 = partial_tab_width_2
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                while True: # start choice
                                                    offset_6 = offset_5
                                                    column_4 = column_3
                                                    indent_column_4 = indent_column_3
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_6 = [] if children_5 is not None else None
                                                    while True: # case
                                                        count_2 = 0
                                                        while offset_6 < buf_eof:
                                                            chr = buf[offset_6]
                                                            if chr in ' \t':
                                                                if chr == '\t':
                                                                    if offset_6 == partial_tab_offset_4 and partial_tab_width_4 > 0:
                                                                        width = partial_tab_width_4
                                                                    else:
                                                                        width  = (self.tabstop-(column_4%self.tabstop))
                                                                    count_2 += width
                                                                    column_4 += width
                                                                    offset_6 += 1
                                                                else:
                                                                    count_2 += 1
                                                                    column_4 += 1
                                                                    offset_6 += 1
                                                            else:
                                                                break
                                                        if count_2 < 2:
                                                            offset_6 = -1
                                                            break


                                                        break
                                                    if offset_6 != -1:
                                                        offset_5 = offset_6
                                                        column_3 = column_4
                                                        indent_column_3 = indent_column_4
                                                        partial_tab_offset_3 = partial_tab_offset_4
                                                        partial_tab_width_3 = partial_tab_width_4
                                                        if children_6 is not None and children_6 is not None:
                                                            children_5.extend(children_6)
                                                        break
                                                    # end case
                                                    offset_6 = offset_5
                                                    column_4 = column_3
                                                    indent_column_4 = indent_column_3
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_6 = [] if children_5 is not None else None
                                                    while True: # case
                                                        if buf[offset_6:offset_6+1] == '\\':
                                                            offset_6 += 1
                                                            column_4 += 1
                                                        else:
                                                            offset_6 = -1
                                                            break


                                                        break
                                                    if offset_6 != -1:
                                                        offset_5 = offset_6
                                                        column_3 = column_4
                                                        indent_column_3 = indent_column_4
                                                        partial_tab_offset_3 = partial_tab_offset_4
                                                        partial_tab_width_3 = partial_tab_width_4
                                                        if children_6 is not None and children_6 is not None:
                                                            children_5.extend(children_6)
                                                        break
                                                    # end case
                                                    offset_5 = -1 # no more choices
                                                    break # end choice
                                                if offset_5 == -1:
                                                    break

                                                offset_6 = offset_5
                                                children_6 = []
                                                while True: # start capture
                                                    if offset_6 < buf_eof:
                                                        chr = buf[offset_6]
                                                        if chr in '\n':
                                                            offset_6 +=1
                                                            column_3 = 0
                                                            indent_column_3 = 0
                                                        else:
                                                            offset_6 = -1
                                                            break
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 == -1:
                                                    offset_5 = -1
                                                    break
                                                if self.builder is not None:
                                                    value_0 = self.builder['hardbreak'](buf, offset_5, offset_6, children_6)
                                                else:
                                                    value_0 = self.Node('hardbreak', offset_5, offset_6, children_6, None)
                                                children_5.append(value_0)
                                                offset_5 = offset_6


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_2 = column_3
                                                indent_column_2 = indent_column_3
                                                partial_tab_offset_2 = partial_tab_offset_3
                                                partial_tab_width_2 = partial_tab_width_3
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_3 = column_2
                                            indent_column_3 = indent_column_2
                                            partial_tab_offset_3 = partial_tab_offset_2
                                            partial_tab_width_3 = partial_tab_width_2
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                count_2 = 0
                                                while offset_5 < buf_eof:
                                                    chr = buf[offset_5]
                                                    if chr in ' \t':
                                                        if chr == '\t':
                                                            if offset_5 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                                width = partial_tab_width_3
                                                            else:
                                                                width  = (self.tabstop-(column_3%self.tabstop))
                                                            count_2 += width
                                                            column_3 += width
                                                            offset_5 += 1
                                                        else:
                                                            count_2 += 1
                                                            column_3 += 1
                                                            offset_5 += 1
                                                    else:
                                                        break

                                                offset_6 = offset_5
                                                children_6 = []
                                                while True: # start capture
                                                    if offset_6 < buf_eof:
                                                        chr = buf[offset_6]
                                                        if chr in '\n':
                                                            offset_6 +=1
                                                            column_3 = 0
                                                            indent_column_3 = 0
                                                        else:
                                                            offset_6 = -1
                                                            break
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 == -1:
                                                    offset_5 = -1
                                                    break
                                                if self.builder is not None:
                                                    value_1 = self.builder['softbreak'](buf, offset_5, offset_6, children_6)
                                                else:
                                                    value_1 = self.Node('softbreak', offset_5, offset_6, children_6, None)
                                                children_5.append(value_1)
                                                offset_5 = offset_6


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_2 = column_3
                                                indent_column_2 = indent_column_3
                                                partial_tab_offset_2 = partial_tab_offset_3
                                                partial_tab_width_2 = partial_tab_width_3
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_4 = -1 # no more choices
                                            break # end choice
                                        if offset_4 == -1:
                                            break

                                        while True: # start choice
                                            offset_5 = offset_4
                                            column_3 = column_2
                                            indent_column_3 = indent_column_2
                                            partial_tab_offset_3 = partial_tab_offset_2
                                            partial_tab_width_3 = partial_tab_width_2
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                if not (column_3 == indent_column_3 == 0):
                                                    offset_5 = -1
                                                    break
                                                for indent in prefix_0:
                                                    _children, _prefix = [], []
                                                    offset_5, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_5, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                                    if _prefix or _children:
                                                       raise Exception('bar')
                                                    if offset_5 == -1:        break
                                                    indent_column_3 = column_3
                                                if offset_5 == -1:
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5
                                                    column_4 = column_3
                                                    indent_column_4 = indent_column_3
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    while True: # start choice
                                                        offset_7 = offset_6
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_7 = [] if children_6 is not None else None
                                                        while True: # case
                                                            offset_7, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_thematic_break(buf, offset_7, buf_eof, column_5, indent_column_5, prefix_0, children_7, partial_tab_offset_5, partial_tab_width_5)
                                                            if offset_7 == -1: break



                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_7 is not None and children_7 is not None:
                                                                children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_7 = offset_6
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_7 = [] if children_6 is not None else None
                                                        while True: # case
                                                            offset_7, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_atx_heading(buf, offset_7, buf_eof, column_5, indent_column_5, prefix_0, children_7, partial_tab_offset_5, partial_tab_width_5)
                                                            if offset_7 == -1: break



                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_7 is not None and children_7 is not None:
                                                                children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_7 = offset_6
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_7 = [] if children_6 is not None else None
                                                        while True: # case
                                                            offset_7, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_start_fenced_block(buf, offset_7, buf_eof, column_5, indent_column_5, prefix_0, children_7, partial_tab_offset_5, partial_tab_width_5)
                                                            if offset_7 == -1: break



                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_7 is not None and children_7 is not None:
                                                                children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_7 = offset_6
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_7 = [] if children_6 is not None else None
                                                        while True: # case
                                                            offset_7, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_start_list(buf, offset_7, buf_eof, column_5, indent_column_5, prefix_0, children_7, partial_tab_offset_5, partial_tab_width_5)
                                                            if offset_7 == -1: break



                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_7 is not None and children_7 is not None:
                                                                children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_7 = offset_6
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_7 = [] if children_6 is not None else None
                                                        while True: # case
                                                            offset_7, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_start_blockquote(buf, offset_7, buf_eof, column_5, indent_column_5, prefix_0, children_7, partial_tab_offset_5, partial_tab_width_5)
                                                            if offset_7 == -1: break



                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_7 is not None and children_7 is not None:
                                                                children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_7 = offset_6
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_7 = [] if children_6 is not None else None
                                                        while True: # case
                                                            offset_7, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_setext_heading_line(buf, offset_7, buf_eof, column_5, indent_column_5, prefix_0, children_7, partial_tab_offset_5, partial_tab_width_5)
                                                            if offset_7 == -1: break



                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_7 is not None and children_7 is not None:
                                                                children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_6 = -1 # no more choices
                                                        break # end choice
                                                    if offset_6 == -1:
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                count_2 = 0
                                                while offset_5 < buf_eof:
                                                    chr = buf[offset_5]
                                                    if chr in ' \t':
                                                        if chr == '\t':
                                                            if offset_5 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                                width = partial_tab_width_3
                                                            else:
                                                                width  = (self.tabstop-(column_3%self.tabstop))
                                                            count_2 += width
                                                            column_3 += width
                                                            offset_5 += 1
                                                        else:
                                                            count_2 += 1
                                                            column_3 += 1
                                                            offset_5 += 1
                                                    else:
                                                        break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5
                                                    column_4 = column_3
                                                    indent_column_4 = indent_column_3
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    if offset_6 < buf_eof:
                                                        chr = buf[offset_6]
                                                        if chr in '\n':
                                                            offset_6 +=1
                                                            column_4 = 0
                                                            indent_column_4 = 0
                                                        else:
                                                            offset_6 = -1
                                                            break
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_2 = column_3
                                                indent_column_2 = indent_column_3
                                                partial_tab_offset_2 = partial_tab_offset_3
                                                partial_tab_width_2 = partial_tab_width_3
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_3 = column_2
                                            indent_column_3 = indent_column_2
                                            partial_tab_offset_3 = partial_tab_offset_2
                                            partial_tab_width_3 = partial_tab_width_2
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5
                                                    column_4 = column_3
                                                    indent_column_4 = indent_column_3
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    if not (column_4 == indent_column_4 == 0):
                                                        offset_6 = -1
                                                        break
                                                    for indent in prefix_0:
                                                        _children, _prefix = [], []
                                                        offset_6, column_4, indent_column_4, partial_tab_offset_4, partial_tab_width_4 = indent(buf, offset_6, buf_eof, column_4, indent_column_4, _prefix, _children, partial_tab_offset_4, partial_tab_width_4)
                                                        if _prefix or _children:
                                                           raise Exception('bar')
                                                        if offset_6 == -1:        break
                                                        indent_column_4 = column_4
                                                    if offset_6 == -1:
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5
                                                    column_4 = column_3
                                                    indent_column_4 = indent_column_3
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    while True: # start choice
                                                        offset_7 = offset_6
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_7 = [] if children_6 is not None else None
                                                        while True: # case
                                                            offset_7, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_thematic_break(buf, offset_7, buf_eof, column_5, indent_column_5, prefix_0, children_7, partial_tab_offset_5, partial_tab_width_5)
                                                            if offset_7 == -1: break



                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_7 is not None and children_7 is not None:
                                                                children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_7 = offset_6
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_7 = [] if children_6 is not None else None
                                                        while True: # case
                                                            offset_7, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_atx_heading(buf, offset_7, buf_eof, column_5, indent_column_5, prefix_0, children_7, partial_tab_offset_5, partial_tab_width_5)
                                                            if offset_7 == -1: break



                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_7 is not None and children_7 is not None:
                                                                children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_7 = offset_6
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_7 = [] if children_6 is not None else None
                                                        while True: # case
                                                            offset_7, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_start_fenced_block(buf, offset_7, buf_eof, column_5, indent_column_5, prefix_0, children_7, partial_tab_offset_5, partial_tab_width_5)
                                                            if offset_7 == -1: break



                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_7 is not None and children_7 is not None:
                                                                children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_7 = offset_6
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_7 = [] if children_6 is not None else None
                                                        while True: # case
                                                            offset_7, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_start_list(buf, offset_7, buf_eof, column_5, indent_column_5, prefix_0, children_7, partial_tab_offset_5, partial_tab_width_5)
                                                            if offset_7 == -1: break



                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_7 is not None and children_7 is not None:
                                                                children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_7 = offset_6
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_7 = [] if children_6 is not None else None
                                                        while True: # case
                                                            offset_7, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_start_blockquote(buf, offset_7, buf_eof, column_5, indent_column_5, prefix_0, children_7, partial_tab_offset_5, partial_tab_width_5)
                                                            if offset_7 == -1: break



                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_7 is not None and children_7 is not None:
                                                                children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_7 = offset_6
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_7 = [] if children_6 is not None else None
                                                        while True: # case
                                                            offset_7, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_setext_heading_line(buf, offset_7, buf_eof, column_5, indent_column_5, prefix_0, children_7, partial_tab_offset_5, partial_tab_width_5)
                                                            if offset_7 == -1: break



                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_7 is not None and children_7 is not None:
                                                                children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_6 = -1 # no more choices
                                                        break # end choice
                                                    if offset_6 == -1:
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                count_2 = 0
                                                while offset_5 < buf_eof:
                                                    chr = buf[offset_5]
                                                    if chr in ' \t':
                                                        if chr == '\t':
                                                            if offset_5 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                                width = partial_tab_width_3
                                                            else:
                                                                width  = (self.tabstop-(column_3%self.tabstop))
                                                            count_2 += width
                                                            column_3 += width
                                                            offset_5 += 1
                                                        else:
                                                            count_2 += 1
                                                            column_3 += 1
                                                            offset_5 += 1
                                                    else:
                                                        break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6 = offset_5
                                                    column_4 = column_3
                                                    indent_column_4 = indent_column_3
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    if offset_6 < buf_eof:
                                                        chr = buf[offset_6]
                                                        if chr in '\n':
                                                            offset_6 +=1
                                                            column_4 = 0
                                                            indent_column_4 = 0
                                                        else:
                                                            offset_6 = -1
                                                            break
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_2 = column_3
                                                indent_column_2 = indent_column_3
                                                partial_tab_offset_2 = partial_tab_offset_3
                                                partial_tab_width_2 = partial_tab_width_3
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_4 = -1 # no more choices
                                            break # end choice
                                        if offset_4 == -1:
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_1 = column_2
                                        indent_column_1 = indent_column_2
                                        partial_tab_offset_1 = partial_tab_offset_2
                                        partial_tab_width_1 = partial_tab_width_2
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    column_2 = column_1
                                    indent_column_2 = indent_column_1
                                    partial_tab_offset_2 = partial_tab_offset_1
                                    partial_tab_width_2 = partial_tab_width_1
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        offset_5 = offset_4
                                        children_5 = []
                                        while True: # start capture
                                            count_2 = 0
                                            while offset_5 < buf_eof:
                                                chr = buf[offset_5]
                                                if chr in ' \t':
                                                    if chr == '\t':
                                                        if offset_5 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                            width = partial_tab_width_2
                                                        else:
                                                            width  = (self.tabstop-(column_2%self.tabstop))
                                                        count_2 += width
                                                        column_2 += width
                                                        offset_5 += 1
                                                    else:
                                                        count_2 += 1
                                                        column_2 += 1
                                                        offset_5 += 1
                                                else:
                                                    break

                                            break
                                        if offset_5 == -1:
                                            offset_4 = -1
                                            break
                                        if self.builder is not None:
                                            value_2 = self.builder['whitespace'](buf, offset_4, offset_5, children_5)
                                        else:
                                            value_2 = self.Node('whitespace', offset_4, offset_5, children_5, None)
                                        children_4.append(value_2)
                                        offset_4 = offset_5


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        column_1 = column_2
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

                                offset_3, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_inline_element(buf, offset_3, buf_eof, column_1, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                                if offset_3 == -1: break


                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            column_0 = column_1
                            indent_column_0 = indent_column_1
                            partial_tab_offset_0 = partial_tab_offset_1
                            partial_tab_width_0 = partial_tab_width_1
                            count_1 += 1
                        if offset_2 == -1:
                            break


                        count_1 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t':
                                if chr == '\t':
                                    if offset_2 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                                        width = partial_tab_width_0
                                    else:
                                        width  = (self.tabstop-(column_0%self.tabstop))
                                    count_1 += width
                                    column_0 += width
                                    offset_2 += 1
                                else:
                                    count_1 += 1
                                    column_0 += 1
                                    offset_2 += 1
                            else:
                                break

                        count_1 = 0
                        while count_1 < 1:
                            offset_3 = offset_2
                            column_1 = column_0
                            indent_column_1 = indent_column_0
                            partial_tab_offset_1 = partial_tab_offset_0
                            partial_tab_width_1 = partial_tab_width_0
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if buf[offset_3:offset_3+1] == '\\':
                                    offset_3 += 1
                                    column_1 += 1
                                else:
                                    offset_3 = -1
                                    break

                                if self.builder is not None:
                                    children_3.append('\\')
                                else:
                                    children_3.append(self.Node('value', offset_3, offset_3, (), '\\'))

                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            column_0 = column_1
                            indent_column_0 = indent_column_1
                            partial_tab_offset_0 = partial_tab_offset_1
                            partial_tab_width_0 = partial_tab_width_1
                            count_1 += 1
                            break
                        if offset_2 == -1:
                            break

                        if offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in '\n':
                                offset_2 +=1
                                column_0 = 0
                                indent_column_0 = 0
                            else:
                                offset_2 = -1
                                break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_3 = self.builder['para'](buf, offset_1, offset_2, children_2)
                    else:
                        value_3 = self.Node('para', offset_1, offset_2, children_2, None)
                    children_1.append(value_3)
                    offset_1 = offset_2

                    break
                self.cache[count_0] = (offset_1, column_0, indent_column_0, children_1, partial_tab_offset_0,partial_tab_width_0)
            offset_0 = offset_1
            if children_1 is not None and children_1 is not None:
                children_0.extend(children_1)
            if offset_0 == -1:
                break


            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_para_line(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_inline_element(buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0)
            if offset_0 == -1: break


            count_0 = 0
            while True:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    while True: # start choice
                        offset_2 = offset_1
                        column_2 = column_1
                        indent_column_2 = indent_column_1
                        partial_tab_offset_2 = partial_tab_offset_1
                        partial_tab_width_2 = partial_tab_width_1
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            while True: # start choice
                                offset_3 = offset_2
                                column_3 = column_2
                                indent_column_3 = indent_column_2
                                partial_tab_offset_3 = partial_tab_offset_2
                                partial_tab_width_3 = partial_tab_width_2
                                children_3 = [] if children_2 is not None else None
                                while True: # case
                                    while True: # start choice
                                        offset_4 = offset_3
                                        column_4 = column_3
                                        indent_column_4 = indent_column_3
                                        partial_tab_offset_4 = partial_tab_offset_3
                                        partial_tab_width_4 = partial_tab_width_3
                                        children_4 = [] if children_3 is not None else None
                                        while True: # case
                                            count_1 = 0
                                            while offset_4 < buf_eof:
                                                chr = buf[offset_4]
                                                if chr in ' \t':
                                                    if chr == '\t':
                                                        if offset_4 == partial_tab_offset_4 and partial_tab_width_4 > 0:
                                                            width = partial_tab_width_4
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
                                            if count_1 < 2:
                                                offset_4 = -1
                                                break


                                            break
                                        if offset_4 != -1:
                                            offset_3 = offset_4
                                            column_3 = column_4
                                            indent_column_3 = indent_column_4
                                            partial_tab_offset_3 = partial_tab_offset_4
                                            partial_tab_width_3 = partial_tab_width_4
                                            if children_4 is not None and children_4 is not None:
                                                children_3.extend(children_4)
                                            break
                                        # end case
                                        offset_4 = offset_3
                                        column_4 = column_3
                                        indent_column_4 = indent_column_3
                                        partial_tab_offset_4 = partial_tab_offset_3
                                        partial_tab_width_4 = partial_tab_width_3
                                        children_4 = [] if children_3 is not None else None
                                        while True: # case
                                            if buf[offset_4:offset_4+1] == '\\':
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
                                            if children_4 is not None and children_4 is not None:
                                                children_3.extend(children_4)
                                            break
                                        # end case
                                        offset_3 = -1 # no more choices
                                        break # end choice
                                    if offset_3 == -1:
                                        break

                                    offset_4 = offset_3
                                    children_4 = []
                                    while True: # start capture
                                        if offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in '\n':
                                                offset_4 +=1
                                                column_3 = 0
                                                indent_column_3 = 0
                                            else:
                                                offset_4 = -1
                                                break
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        offset_3 = -1
                                        break
                                    if self.builder is not None:
                                        value_0 = self.builder['hardbreak'](buf, offset_3, offset_4, children_4)
                                    else:
                                        value_0 = self.Node('hardbreak', offset_3, offset_4, children_4, None)
                                    children_3.append(value_0)
                                    offset_3 = offset_4


                                    break
                                if offset_3 != -1:
                                    offset_2 = offset_3
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    if children_3 is not None and children_3 is not None:
                                        children_2.extend(children_3)
                                    break
                                # end case
                                offset_3 = offset_2
                                column_3 = column_2
                                indent_column_3 = indent_column_2
                                partial_tab_offset_3 = partial_tab_offset_2
                                partial_tab_width_3 = partial_tab_width_2
                                children_3 = [] if children_2 is not None else None
                                while True: # case
                                    count_1 = 0
                                    while offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in ' \t':
                                            if chr == '\t':
                                                if offset_3 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                    width = partial_tab_width_3
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

                                    offset_4 = offset_3
                                    children_4 = []
                                    while True: # start capture
                                        if offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in '\n':
                                                offset_4 +=1
                                                column_3 = 0
                                                indent_column_3 = 0
                                            else:
                                                offset_4 = -1
                                                break
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        offset_3 = -1
                                        break
                                    if self.builder is not None:
                                        value_1 = self.builder['softbreak'](buf, offset_3, offset_4, children_4)
                                    else:
                                        value_1 = self.Node('softbreak', offset_3, offset_4, children_4, None)
                                    children_3.append(value_1)
                                    offset_3 = offset_4


                                    break
                                if offset_3 != -1:
                                    offset_2 = offset_3
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    if children_3 is not None and children_3 is not None:
                                        children_2.extend(children_3)
                                    break
                                # end case
                                offset_2 = -1 # no more choices
                                break # end choice
                            if offset_2 == -1:
                                break

                            while True: # start choice
                                offset_3 = offset_2
                                column_3 = column_2
                                indent_column_3 = indent_column_2
                                partial_tab_offset_3 = partial_tab_offset_2
                                partial_tab_width_3 = partial_tab_width_2
                                children_3 = [] if children_2 is not None else None
                                while True: # case
                                    if not (column_3 == indent_column_3 == 0):
                                        offset_3 = -1
                                        break
                                    for indent in prefix_0:
                                        _children, _prefix = [], []
                                        offset_3, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_3, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                        if _prefix or _children:
                                           raise Exception('bar')
                                        if offset_3 == -1:        break
                                        indent_column_3 = column_3
                                    if offset_3 == -1:
                                        break

                                    while True: # start reject
                                        children_4 = []
                                        offset_4 = offset_3
                                        column_4 = column_3
                                        indent_column_4 = indent_column_3
                                        partial_tab_offset_4 = partial_tab_offset_3
                                        partial_tab_width_4 = partial_tab_width_3
                                        while True: # start choice
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_5 = indent_column_4
                                            partial_tab_offset_5 = partial_tab_offset_4
                                            partial_tab_width_5 = partial_tab_width_4
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                offset_5, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_thematic_break(buf, offset_5, buf_eof, column_5, indent_column_5, prefix_0, children_5, partial_tab_offset_5, partial_tab_width_5)
                                                if offset_5 == -1: break



                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_4 = indent_column_5
                                                partial_tab_offset_4 = partial_tab_offset_5
                                                partial_tab_width_4 = partial_tab_width_5
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_5 = indent_column_4
                                            partial_tab_offset_5 = partial_tab_offset_4
                                            partial_tab_width_5 = partial_tab_width_4
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                offset_5, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_atx_heading(buf, offset_5, buf_eof, column_5, indent_column_5, prefix_0, children_5, partial_tab_offset_5, partial_tab_width_5)
                                                if offset_5 == -1: break



                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_4 = indent_column_5
                                                partial_tab_offset_4 = partial_tab_offset_5
                                                partial_tab_width_4 = partial_tab_width_5
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_5 = indent_column_4
                                            partial_tab_offset_5 = partial_tab_offset_4
                                            partial_tab_width_5 = partial_tab_width_4
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                offset_5, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_start_fenced_block(buf, offset_5, buf_eof, column_5, indent_column_5, prefix_0, children_5, partial_tab_offset_5, partial_tab_width_5)
                                                if offset_5 == -1: break



                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_4 = indent_column_5
                                                partial_tab_offset_4 = partial_tab_offset_5
                                                partial_tab_width_4 = partial_tab_width_5
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_5 = indent_column_4
                                            partial_tab_offset_5 = partial_tab_offset_4
                                            partial_tab_width_5 = partial_tab_width_4
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                offset_5, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_start_list(buf, offset_5, buf_eof, column_5, indent_column_5, prefix_0, children_5, partial_tab_offset_5, partial_tab_width_5)
                                                if offset_5 == -1: break



                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_4 = indent_column_5
                                                partial_tab_offset_4 = partial_tab_offset_5
                                                partial_tab_width_4 = partial_tab_width_5
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_5 = indent_column_4
                                            partial_tab_offset_5 = partial_tab_offset_4
                                            partial_tab_width_5 = partial_tab_width_4
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                offset_5, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_start_blockquote(buf, offset_5, buf_eof, column_5, indent_column_5, prefix_0, children_5, partial_tab_offset_5, partial_tab_width_5)
                                                if offset_5 == -1: break



                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_4 = indent_column_5
                                                partial_tab_offset_4 = partial_tab_offset_5
                                                partial_tab_width_4 = partial_tab_width_5
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_5 = indent_column_4
                                            partial_tab_offset_5 = partial_tab_offset_4
                                            partial_tab_width_5 = partial_tab_width_4
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                offset_5, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_setext_heading_line(buf, offset_5, buf_eof, column_5, indent_column_5, prefix_0, children_5, partial_tab_offset_5, partial_tab_width_5)
                                                if offset_5 == -1: break



                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_4 = indent_column_5
                                                partial_tab_offset_4 = partial_tab_offset_5
                                                partial_tab_width_4 = partial_tab_width_5
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_4 = -1 # no more choices
                                            break # end choice
                                        if offset_4 == -1:
                                            break

                                        break
                                    if offset_4 != -1:
                                        offset_3 = -1
                                        break

                                    count_1 = 0
                                    while offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in ' \t':
                                            if chr == '\t':
                                                if offset_3 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                    width = partial_tab_width_3
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

                                    while True: # start reject
                                        children_4 = []
                                        offset_4 = offset_3
                                        column_4 = column_3
                                        indent_column_4 = indent_column_3
                                        partial_tab_offset_4 = partial_tab_offset_3
                                        partial_tab_width_4 = partial_tab_width_3
                                        if offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in '\n':
                                                offset_4 +=1
                                                column_4 = 0
                                                indent_column_4 = 0
                                            else:
                                                offset_4 = -1
                                                break
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 != -1:
                                        offset_3 = -1
                                        break


                                    break
                                if offset_3 != -1:
                                    offset_2 = offset_3
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    if children_3 is not None and children_3 is not None:
                                        children_2.extend(children_3)
                                    break
                                # end case
                                offset_3 = offset_2
                                column_3 = column_2
                                indent_column_3 = indent_column_2
                                partial_tab_offset_3 = partial_tab_offset_2
                                partial_tab_width_3 = partial_tab_width_2
                                children_3 = [] if children_2 is not None else None
                                while True: # case
                                    while True: # start reject
                                        children_4 = []
                                        offset_4 = offset_3
                                        column_4 = column_3
                                        indent_column_4 = indent_column_3
                                        partial_tab_offset_4 = partial_tab_offset_3
                                        partial_tab_width_4 = partial_tab_width_3
                                        if not (column_4 == indent_column_4 == 0):
                                            offset_4 = -1
                                            break
                                        for indent in prefix_0:
                                            _children, _prefix = [], []
                                            offset_4, column_4, indent_column_4, partial_tab_offset_4, partial_tab_width_4 = indent(buf, offset_4, buf_eof, column_4, indent_column_4, _prefix, _children, partial_tab_offset_4, partial_tab_width_4)
                                            if _prefix or _children:
                                               raise Exception('bar')
                                            if offset_4 == -1:        break
                                            indent_column_4 = column_4
                                        if offset_4 == -1:
                                            break

                                        break
                                    if offset_4 != -1:
                                        offset_3 = -1
                                        break

                                    while True: # start reject
                                        children_4 = []
                                        offset_4 = offset_3
                                        column_4 = column_3
                                        indent_column_4 = indent_column_3
                                        partial_tab_offset_4 = partial_tab_offset_3
                                        partial_tab_width_4 = partial_tab_width_3
                                        while True: # start choice
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_5 = indent_column_4
                                            partial_tab_offset_5 = partial_tab_offset_4
                                            partial_tab_width_5 = partial_tab_width_4
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                offset_5, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_thematic_break(buf, offset_5, buf_eof, column_5, indent_column_5, prefix_0, children_5, partial_tab_offset_5, partial_tab_width_5)
                                                if offset_5 == -1: break



                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_4 = indent_column_5
                                                partial_tab_offset_4 = partial_tab_offset_5
                                                partial_tab_width_4 = partial_tab_width_5
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_5 = indent_column_4
                                            partial_tab_offset_5 = partial_tab_offset_4
                                            partial_tab_width_5 = partial_tab_width_4
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                offset_5, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_atx_heading(buf, offset_5, buf_eof, column_5, indent_column_5, prefix_0, children_5, partial_tab_offset_5, partial_tab_width_5)
                                                if offset_5 == -1: break



                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_4 = indent_column_5
                                                partial_tab_offset_4 = partial_tab_offset_5
                                                partial_tab_width_4 = partial_tab_width_5
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_5 = indent_column_4
                                            partial_tab_offset_5 = partial_tab_offset_4
                                            partial_tab_width_5 = partial_tab_width_4
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                offset_5, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_start_fenced_block(buf, offset_5, buf_eof, column_5, indent_column_5, prefix_0, children_5, partial_tab_offset_5, partial_tab_width_5)
                                                if offset_5 == -1: break



                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_4 = indent_column_5
                                                partial_tab_offset_4 = partial_tab_offset_5
                                                partial_tab_width_4 = partial_tab_width_5
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_5 = indent_column_4
                                            partial_tab_offset_5 = partial_tab_offset_4
                                            partial_tab_width_5 = partial_tab_width_4
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                offset_5, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_start_list(buf, offset_5, buf_eof, column_5, indent_column_5, prefix_0, children_5, partial_tab_offset_5, partial_tab_width_5)
                                                if offset_5 == -1: break



                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_4 = indent_column_5
                                                partial_tab_offset_4 = partial_tab_offset_5
                                                partial_tab_width_4 = partial_tab_width_5
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_5 = indent_column_4
                                            partial_tab_offset_5 = partial_tab_offset_4
                                            partial_tab_width_5 = partial_tab_width_4
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                offset_5, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_start_blockquote(buf, offset_5, buf_eof, column_5, indent_column_5, prefix_0, children_5, partial_tab_offset_5, partial_tab_width_5)
                                                if offset_5 == -1: break



                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_4 = indent_column_5
                                                partial_tab_offset_4 = partial_tab_offset_5
                                                partial_tab_width_4 = partial_tab_width_5
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            column_5 = column_4
                                            indent_column_5 = indent_column_4
                                            partial_tab_offset_5 = partial_tab_offset_4
                                            partial_tab_width_5 = partial_tab_width_4
                                            children_5 = [] if children_4 is not None else None
                                            while True: # case
                                                offset_5, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_setext_heading_line(buf, offset_5, buf_eof, column_5, indent_column_5, prefix_0, children_5, partial_tab_offset_5, partial_tab_width_5)
                                                if offset_5 == -1: break



                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                column_4 = column_5
                                                indent_column_4 = indent_column_5
                                                partial_tab_offset_4 = partial_tab_offset_5
                                                partial_tab_width_4 = partial_tab_width_5
                                                if children_5 is not None and children_5 is not None:
                                                    children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_4 = -1 # no more choices
                                            break # end choice
                                        if offset_4 == -1:
                                            break

                                        break
                                    if offset_4 != -1:
                                        offset_3 = -1
                                        break

                                    count_1 = 0
                                    while offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in ' \t':
                                            if chr == '\t':
                                                if offset_3 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                    width = partial_tab_width_3
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

                                    while True: # start reject
                                        children_4 = []
                                        offset_4 = offset_3
                                        column_4 = column_3
                                        indent_column_4 = indent_column_3
                                        partial_tab_offset_4 = partial_tab_offset_3
                                        partial_tab_width_4 = partial_tab_width_3
                                        if offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in '\n':
                                                offset_4 +=1
                                                column_4 = 0
                                                indent_column_4 = 0
                                            else:
                                                offset_4 = -1
                                                break
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 != -1:
                                        offset_3 = -1
                                        break


                                    break
                                if offset_3 != -1:
                                    offset_2 = offset_3
                                    column_2 = column_3
                                    indent_column_2 = indent_column_3
                                    partial_tab_offset_2 = partial_tab_offset_3
                                    partial_tab_width_2 = partial_tab_width_3
                                    if children_3 is not None and children_3 is not None:
                                        children_2.extend(children_3)
                                    break
                                # end case
                                offset_2 = -1 # no more choices
                                break # end choice
                            if offset_2 == -1:
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
                            offset_3 = offset_2
                            children_3 = []
                            while True: # start capture
                                count_1 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        if chr == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_1 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_1 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                break
                            if offset_3 == -1:
                                offset_2 = -1
                                break
                            if self.builder is not None:
                                value_2 = self.builder['whitespace'](buf, offset_2, offset_3, children_3)
                            else:
                                value_2 = self.Node('whitespace', offset_2, offset_3, children_3, None)
                            children_2.append(value_2)
                            offset_2 = offset_3


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

                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_inline_element(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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


            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
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
            while count_0 < 1:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    if buf[offset_1:offset_1+1] == '\\':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    if self.builder is not None:
                        children_1.append('\\')
                    else:
                        children_1.append(self.Node('value', offset_1, offset_1, (), '\\'))

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
                break
            if offset_0 == -1:
                break


            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_empty_lines(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
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

            if offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in '\n':
                    offset_0 +=1
                    column_0 = 0
                    indent_column_0 = 0
                else:
                    offset_0 = -1
                    break
            else:
                offset_0 = -1
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
                    if not (column_1 == indent_column_1 == 0):
                        offset_1 = -1
                        break
                    for indent in prefix_0:
                        _children, _prefix = [], []
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_1, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                        if _prefix or _children:
                           raise Exception('bar')
                        if offset_1 == -1:        break
                        indent_column_1 = column_1
                    if offset_1 == -1:
                        break

                    count_1 = 0
                    while offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in ' \t':
                            if chr == '\t':
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

                    if offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in '\n':
                            offset_1 +=1
                            column_1 = 0
                            indent_column_1 = 0
                        else:
                            offset_1 = -1
                            break
                    else:
                        offset_1 = -1
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

            offset_1 = offset_0
            if self.builder is not None:
                value_0 = self.builder['empty'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('empty', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1


            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_line_end(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t':
                    if chr == '\t':
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

            if offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in '\n':
                    offset_0 +=1
                    column_0 = 0
                    indent_column_0 = 0
                else:
                    offset_0 = -1
                    break


            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_inline_element(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_code_span(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_escaped(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_word(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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

    def parse_code_span(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            offset_1 = offset_0
            column_1 = column_0
            while True: # start count
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    column_2 = column_1
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_1 = [] if children_0 is not None else None
                    while True:
                        if buf[offset_2:offset_2+1] == '`':
                            offset_2 += 1
                            column_2 += 1
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        break
                    if offset_1 == offset_2: break
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
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

                break
            if offset_1 == -1:
                offset_0 = -1; break
            value_0 = buf[offset_0:offset_1].count('`')
            offset_0 = offset_1
            column_0 = column_1

            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        while True: # start choice
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = ord(buf[offset_3])

                                if chr == 96:
                                    offset_3 = -1
                                    break
                                else:
                                    offset_3 += 1
                                    column_2 += 1


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
                                while True: # start reject
                                    children_4 = []
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    count_1 = 0
                                    while count_1 < value_0:
                                        offset_5 = offset_4
                                        column_4 = column_3
                                        indent_column_4 = indent_column_3
                                        partial_tab_offset_4 = partial_tab_offset_3
                                        partial_tab_width_4 = partial_tab_width_3
                                        children_5 = [] if children_4 is not None else None
                                        while True:
                                            if buf[offset_5:offset_5+1] == '`':
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
                                    if count_1 < value_0:
                                        offset_4 = -1
                                        break
                                    if offset_4 == -1:
                                        break

                                    break
                                if offset_4 != -1:
                                    offset_3 = -1
                                    break

                                if buf[offset_3:offset_3+1] == '`':
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
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
                if count_0 < 1:
                    offset_1 = -1
                    break
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_1 = self.builder['code_span'](buf, offset_0, offset_1, children_1)
            else:
                value_1 = self.Node('code_span', offset_0, offset_1, children_1, None)
            children_0.append(value_1)
            offset_0 = offset_1

            count_0 = 0
            while count_0 < value_0:
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                children_1 = [] if children_0 is not None else None
                while True:
                    if buf[offset_1:offset_1+1] == '`':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
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
            if count_0 < value_0:
                offset_0 = -1
                break
            if offset_0 == -1:
                break


            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_escaped(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            if buf[offset_0:offset_0+1] == '\\':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break

            while True: # start reject
                children_1 = []
                offset_1 = offset_0
                column_1 = column_0
                indent_column_1 = indent_column_0
                partial_tab_offset_1 = partial_tab_offset_0
                partial_tab_width_1 = partial_tab_width_0
                if offset_1 < buf_eof:
                    chr = buf[offset_1]
                    if chr in '\n':
                        offset_1 +=1
                        column_1 = 0
                        indent_column_1 = 0
                    else:
                        offset_1 = -1
                        break
                else:
                    offset_1 = -1
                    break

                break
            if offset_1 != -1:
                offset_0 = -1
                break

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
                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break

                        chr = ord(buf[offset_2])

                        if 33 <= chr <= 47:
                            offset_2 += 1
                            column_1 += 1
                        elif 58 <= chr <= 64:
                            offset_2 += 1
                            column_1 += 1
                        elif 91 <= chr <= 96:
                            offset_2 += 1
                            column_1 += 1
                        elif 123 <= chr <= 126:
                            offset_2 += 1
                            column_1 += 1
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_0 = self.builder['text'](buf, offset_1, offset_2, children_2)
                    else:
                        value_0 = self.Node('text', offset_1, offset_2, children_2, None)
                    children_1.append(value_0)
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
                    if self.builder is not None:
                        children_1.append('\\')
                    else:
                        children_1.append(self.Node('value', offset_1, offset_1, (), '\\'))


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

    def parse_word(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break

                        chr = ord(buf[offset_2])

                        if chr == 32:
                            offset_2 = -1
                            break
                        elif chr == 10:
                            offset_2 = -1
                            break
                        elif chr == 92:
                            offset_2 = -1
                            break
                        else:
                            offset_2 += 1
                            column_1 += 1

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
                if count_0 < 1:
                    offset_1 = -1
                    break
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['text'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('text', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            break
        return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0
