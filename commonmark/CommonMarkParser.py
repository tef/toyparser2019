def _build(unicodedata):
    class Parser:
        def __init__(self, tabstop=None, allow_mixed_indent=False):
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
                return builder[self.name](buf, self, children)


        def parse(self, buf, offset=0, end=None, err=None, builder=None):
            self.cache = dict()
            end = len(buf) if end is None else end
            column, indent_column, eof = 0, (0, None), end
            prefix, children = [], []
            new_offset, column, indent_column, partial_tab_offset, partial_tab_width = self.parse_document(buf, offset, eof, column, indent_column, prefix, children, 0, 0)
            if children and new_offset == end:
                 if builder is None: return self.Node('document', offset, new_offset, children, None)
                 return children[-1].build(buf, builder)
            print('no', offset, new_offset, end, buf[new_offset:])
            if err is not None: raise err(buf, new_offset, 'no')

        def parse_document(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                count_0 = 0
                while True:
                    offset_1 = offset_0
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_1 = [] if children_0 is not None else None
                    while True:
                        if not (column_1 == indent_column_1[0] == 0):
                            offset_1 = -1
                            break
                        # print('start')
                        for indent, dedent in prefix_0:
                            # print(indent)
                            _children, _prefix = [], []
                            offset_2 = offset_1
                            offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_2, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                            if _prefix or _children:
                               raise Exception('bar')
                            if offset_2 == -1:
                                offset_1 = -1
                                break
                            offset_1 = offset_2
                            indent_column_1 = (column_1, indent_column_1)
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
                                offset_2, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_empty_lines(buf, offset_2, buf_eof, column_2, indent_column_2, prefix_0, children_2, partial_tab_offset_2, partial_tab_width_2)
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

                if offset_0 != buf_eof:
                    offset_0 = -1
                    break


                break
            return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

        def parse_empty_lines(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
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

                if offset_0 < buf_eof:
                    codepoint = buf[offset_0]
                    if codepoint in '\n':
                        offset_0 +=1
                        column_0 = 0
                        indent_column_0 = (0, None)
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
                        if not (column_1 == indent_column_1[0] == 0):
                            offset_1 = -1
                            break
                        # print('start')
                        for indent, dedent in prefix_0:
                            # print(indent)
                            _children, _prefix = [], []
                            offset_2 = offset_1
                            offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_2, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                            if _prefix or _children:
                               raise Exception('bar')
                            if offset_2 == -1:
                                offset_1 = -1
                                break
                            offset_1 = offset_2
                            indent_column_1 = (column_1, indent_column_1)
                        if offset_1 == -1:
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

                        if offset_1 < buf_eof:
                            codepoint = buf[offset_1]
                            if codepoint in '\n':
                                offset_1 +=1
                                column_1 = 0
                                indent_column_1 = (0, None)
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
                value_0 = self.Node('empty_line', offset_0, offset_1, children_1, None)
                children_0.append(value_0)
                offset_0 = offset_1


                break
            return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

        def parse_line_end(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
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

                if offset_0 < buf_eof:
                    codepoint = buf[offset_0]
                    if codepoint in '\n':
                        offset_0 +=1
                        column_0 = 0
                        indent_column_0 = (0, None)
                    else:
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
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_tilde_code_block(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_backtick_code_block(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_ordered_list(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_unordered_list(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                    codepoint = buf[offset_0]
                    if codepoint in ' \t':
                        if codepoint == '\t':
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
                                        codepoint = buf[offset_3]
                                        if codepoint in ' \t':
                                            if codepoint == '\t':
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
                                        codepoint = buf[offset_3]
                                        if codepoint in ' \t':
                                            if codepoint == '\t':
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
                                        codepoint = buf[offset_3]
                                        if codepoint in ' \t':
                                            if codepoint == '\t':
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
                    codepoint = buf[offset_0]
                    if codepoint in ' \t':
                        if codepoint == '\t':
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
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
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
                                        offset_4 = offset_3 + 0
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
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t':
                                                if codepoint == '\t':
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

                if offset_0 < buf_eof:
                    codepoint = buf[offset_0]
                    if codepoint in '\n':
                        offset_0 +=1
                        column_0 = 0
                        indent_column_0 = (0, None)
                    else:
                        offset_0 = -1
                        break


                break
            return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

        def parse_indented_code_block(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                count_0 = 0
                while offset_0 < buf_eof and count_0 < 4:
                    codepoint = buf[offset_0]
                    if codepoint in ' \t':
                        if codepoint == '\t':
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
                    count_0 = column_0 - indent_column_0[0]
                    # print(count_0, 'indent')
                    def _indent(buf, offset, buf_eof, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
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
                            elif codepoint in '\n':
                                break
                            else:
                                offset = -1
                                break
                        return offset, column, indent_column, partial_tab_offset, partial_tab_width
                    def _dedent(buf, offset, buf_eof, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
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
                            elif codepoint in '\n':
                                offset = -1; break
                            else:
                                offset = start_offset
                        if count == 0:
                                offset = -1
                        return offset, column, indent_column, partial_tab_offset, partial_tab_width
                    prefix_0.append((_indent, _dedent))
                    indent_column_0 = (column_0, indent_column_0)
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
                            children_2.append(self.Node('value', offset_2, offset_2, (), value_0))

                            break
                        if offset_2 == -1:
                            offset_1 = -1
                            break
                        value_1 = self.Node('partial_indent', offset_1, offset_2, children_2, None)
                        children_1.append(value_1)
                        offset_1 = offset_2

                        offset_2 = offset_1
                        children_2 = []
                        while True: # start capture
                            count_0 = 0
                            while offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
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

                                    codepoint = ord(buf[offset_3])

                                    if codepoint == 10:
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
                        value_2 = self.Node('indented_code_line', offset_1, offset_2, children_2, None)
                        children_1.append(value_2)
                        offset_1 = offset_2

                        if offset_1 < buf_eof:
                            codepoint = buf[offset_1]
                            if codepoint in '\n':
                                offset_1 +=1
                                column_0 = 0
                                indent_column_0 = (0, None)
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
                                                if not (column_3 == indent_column_3[0] == 0):
                                                    offset_4 = -1
                                                    break
                                                # print('start')
                                                for indent, dedent in prefix_0:
                                                    # print(indent)
                                                    _children, _prefix = [], []
                                                    offset_5 = offset_4
                                                    offset_5, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_5, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                                    if _prefix or _children:
                                                       raise Exception('bar')
                                                    if offset_5 == -1:
                                                        offset_4 = -1
                                                        break
                                                    offset_4 = offset_5
                                                    indent_column_3 = (column_3, indent_column_3)
                                                if offset_4 == -1:
                                                    break

                                                offset_5 = offset_4
                                                children_5 = []
                                                while True: # start capture
                                                    count_2 = 0
                                                    while offset_5 < buf_eof:
                                                        codepoint = buf[offset_5]
                                                        if codepoint in ' \t':
                                                            if codepoint == '\t':
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
                                                value_3 = self.Node('indented_code_line', offset_4, offset_5, children_5, None)
                                                children_4.append(value_3)
                                                offset_4 = offset_5

                                                if offset_4 < buf_eof:
                                                    codepoint = buf[offset_4]
                                                    if codepoint in '\n':
                                                        offset_4 +=1
                                                        column_3 = 0
                                                        indent_column_3 = (0, None)
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

                                        while True: # start lookahed
                                            children_4 = []
                                            offset_4 = offset_3 + 0
                                            column_3 = column_2
                                            indent_column_3 = indent_column_2
                                            partial_tab_offset_3 = partial_tab_offset_2
                                            partial_tab_width_3 = partial_tab_width_2
                                            if not (column_3 == indent_column_3[0] == 0):
                                                offset_4 = -1
                                                break
                                            # print('start')
                                            for indent, dedent in prefix_0:
                                                # print(indent)
                                                _children, _prefix = [], []
                                                offset_5 = offset_4
                                                offset_5, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_5, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                                if _prefix or _children:
                                                   raise Exception('bar')
                                                if offset_5 == -1:
                                                    offset_4 = -1
                                                    break
                                                offset_4 = offset_5
                                                indent_column_3 = (column_3, indent_column_3)
                                            if offset_4 == -1:
                                                break

                                            count_1 = 0
                                            while offset_4 < buf_eof:
                                                codepoint = buf[offset_4]
                                                if codepoint in ' \t':
                                                    if codepoint == '\t':
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

                                            codepoint = ord(buf[offset_4])

                                            if codepoint == 10:
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
                                        if not (column_2 == indent_column_2[0] == 0):
                                            offset_3 = -1
                                            break
                                        # print('start')
                                        for indent, dedent in prefix_0:
                                            # print(indent)
                                            _children, _prefix = [], []
                                            offset_4 = offset_3
                                            offset_4, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = indent(buf, offset_4, buf_eof, column_2, indent_column_2, _prefix, _children, partial_tab_offset_2, partial_tab_width_2)
                                            if _prefix or _children:
                                               raise Exception('bar')
                                            if offset_4 == -1:
                                                offset_3 = -1
                                                break
                                            offset_3 = offset_4
                                            indent_column_2 = (column_2, indent_column_2)
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
                                            children_4.append(self.Node('value', offset_4, offset_4, (), value_4))

                                            break
                                        if offset_4 == -1:
                                            offset_3 = -1
                                            break
                                        value_5 = self.Node('partial_indent', offset_3, offset_4, children_4, None)
                                        children_3.append(value_5)
                                        offset_3 = offset_4

                                        offset_4 = offset_3
                                        children_4 = []
                                        while True: # start capture
                                            count_1 = 0
                                            while offset_4 < buf_eof:
                                                codepoint = buf[offset_4]
                                                if codepoint in ' \t':
                                                    if codepoint == '\t':
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

                                                    codepoint = ord(buf[offset_5])

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
                                        value_6 = self.Node('indented_code_line', offset_3, offset_4, children_4, None)
                                        children_3.append(value_6)
                                        offset_3 = offset_4

                                        if offset_3 < buf_eof:
                                            codepoint = buf[offset_3]
                                            if codepoint in '\n':
                                                offset_3 +=1
                                                column_2 = 0
                                                indent_column_2 = (0, None)
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
                    if indent_column_0 != (0, None): indent_column_0 = indent_column_0[1]
                    if offset_1 == -1: break

                    break
                if offset_1 == -1:
                    offset_0 = -1
                    break
                value_7 = self.Node('indented_code', offset_0, offset_1, children_1, None)
                children_0.append(value_7)
                offset_0 = offset_1


                break
            return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

        def parse_start_fenced_block(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                count_0 = 0
                while offset_0 < buf_eof and count_0 < 3:
                    codepoint = buf[offset_0]
                    if codepoint in ' \t':
                        if codepoint == '\t':
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
                    while offset_1 < buf_eof and count_0 < 3:
                        codepoint = buf[offset_1]
                        if codepoint in ' \t':
                            if codepoint == '\t':
                                if offset_1 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                                    width = partial_tab_width_0
                                else:
                                    width  = (self.tabstop-(column_1%self.tabstop))
                                if count_0 + width > 3:
                                    new_width = 3 - count_0
                                    count_0 += new_width
                                    column_1 += new_width
                                    partial_tab_offset_0 = offset_1
                                    partial_tab_width_0 = width - new_width
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

                    break
                if offset_1 == -1:
                    offset_0 = -1; break
                value_0 = column_1 - column_0
                offset_0 = offset_1
                column_0 = column_1

                offset_1 = offset_0
                children_1 = []
                while True: # start capture
                    offset_2 = offset_1
                    column_1 = column_0
                    while True: # start count
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_1 = indent_column_0
                            partial_tab_offset_1 = partial_tab_offset_0
                            partial_tab_width_1 = partial_tab_width_0
                            children_2 = [] if children_1 is not None else None
                            while True:
                                if buf[offset_3:offset_3+1] == '`':
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
                        if count_0 < 3:
                            offset_2 = -1
                            break
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1; break
                    value_1 = buf[offset_1:offset_2].count('`')
                    offset_1 = offset_2
                    column_0 = column_1

                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            column_1 = column_0
                            indent_column_1 = indent_column_0
                            partial_tab_offset_1 = partial_tab_offset_0
                            partial_tab_width_1 = partial_tab_width_0
                            children_3 = [] if children_2 is not None else None
                            while True:
                                while True: # start reject
                                    children_4 = []
                                    offset_4 = offset_3 + 0
                                    column_2 = column_1
                                    indent_column_2 = indent_column_1
                                    partial_tab_offset_2 = partial_tab_offset_1
                                    partial_tab_width_2 = partial_tab_width_1
                                    if buf[offset_4:offset_4+1] == '`':
                                        offset_4 += 1
                                        column_2 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    break
                                if offset_4 != -1:
                                    offset_3 = -1
                                    break

                                while True: # start choice
                                    offset_4 = offset_3
                                    column_2 = column_1
                                    indent_column_2 = indent_column_1
                                    partial_tab_offset_2 = partial_tab_offset_1
                                    partial_tab_width_2 = partial_tab_width_1
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        offset_4, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_escaped_text(buf, offset_4, buf_eof, column_2, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                        if offset_4 == -1: break



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
                                        offset_4, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_html_entity(buf, offset_4, buf_eof, column_2, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                        if offset_4 == -1: break



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
                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            codepoint = ord(buf[offset_5])

                                            if codepoint == 10:
                                                offset_5 = -1
                                                break
                                            else:
                                                offset_5 += 1
                                                column_2 += 1

                                            count_1 = 0
                                            while True:
                                                offset_6 = offset_5
                                                column_3 = column_2
                                                indent_column_3 = indent_column_2
                                                partial_tab_offset_3 = partial_tab_offset_2
                                                partial_tab_width_3 = partial_tab_width_2
                                                children_6 = [] if children_5 is not None else None
                                                while True:
                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    codepoint = ord(buf[offset_6])

                                                    if codepoint == 10:
                                                        offset_6 = -1
                                                        break
                                                    elif codepoint == 92:
                                                        offset_6 = -1
                                                        break
                                                    elif codepoint == 38:
                                                        offset_6 = -1
                                                        break
                                                    elif codepoint == 96:
                                                        offset_6 = -1
                                                        break
                                                    else:
                                                        offset_6 += 1
                                                        column_3 += 1

                                                    break
                                                if offset_6 == -1:
                                                    break
                                                if offset_5 == offset_6: break
                                                if children_6 is not None and children_6 is not None:
                                                    children_5.extend(children_6)
                                                offset_5 = offset_6
                                                column_2 = column_3
                                                indent_column_2 = indent_column_3
                                                partial_tab_offset_2 = partial_tab_offset_3
                                                partial_tab_width_2 = partial_tab_width_3
                                                count_1 += 1
                                            if offset_5 == -1:
                                                break

                                            break
                                        if offset_5 == -1:
                                            offset_4 = -1
                                            break
                                        value_2 = self.Node('text', offset_4, offset_5, children_5, None)
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
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_3 = self.Node('info', offset_1, offset_2, children_2, None)
                    children_1.append(value_3)
                    offset_1 = offset_2

                    offset_1, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_line_end(buf, offset_1, buf_eof, column_0, indent_column_0, prefix_0, children_1, partial_tab_offset_0, partial_tab_width_0)
                    if offset_1 == -1: break


                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        column_1 = column_0
                        indent_column_1 = indent_column_0
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True:
                            if not (column_1 == indent_column_1[0] == 0):
                                offset_2 = -1
                                break
                            # print('start')
                            for indent, dedent in prefix_0:
                                # print(indent)
                                _children, _prefix = [], []
                                offset_3 = offset_2
                                offset_3, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_3, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_3 == -1:
                                    offset_2 = -1
                                    break
                                offset_2 = offset_3
                                indent_column_1 = (column_1, indent_column_1)
                            if offset_2 == -1:
                                break

                            while True: # start reject
                                children_3 = []
                                offset_3 = offset_2 + 0
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                count_1 = 0
                                while offset_3 < buf_eof and count_1 < 3:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t':
                                        if codepoint == '\t':
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

                                count_1 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if buf[offset_4:offset_4+1] == '`':
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_2 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t':
                                                if codepoint == '\t':
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
                                if count_1 < value_1:
                                    offset_3 = -1
                                    break
                                if offset_3 == -1:
                                    break

                                if offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in '\n':
                                        offset_3 +=1
                                        column_2 = 0
                                        indent_column_2 = (0, None)
                                    else:
                                        offset_3 = -1
                                        break

                                break
                            if offset_3 != -1:
                                offset_2 = -1
                                break

                            count_1 = 0
                            while offset_2 < buf_eof and count_1 < value_0:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
                                        if offset_2 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-(column_1%self.tabstop))
                                        if count_1 + width > value_0:
                                            new_width = value_0 - count_1
                                            count_1 += new_width
                                            column_1 += new_width
                                            partial_tab_offset_1 = offset_2
                                            partial_tab_width_1 = width - new_width
                                            break
                                        count_1 += width
                                        column_1 += width
                                        offset_2 += 1
                                    else:
                                        count_1 += 1
                                        column_1 += 1
                                        offset_2 += 1
                                else:
                                    break

                            offset_3 = offset_2
                            children_3 = []
                            while True: # start capture
                                count_1 = 0
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

                                        codepoint = ord(buf[offset_4])

                                        if codepoint == 10:
                                            offset_4 = -1
                                            break
                                        else:
                                            offset_4 += 1
                                            column_2 += 1

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

                                break
                            if offset_3 == -1:
                                offset_2 = -1
                                break
                            value_4 = self.Node('text', offset_2, offset_3, children_3, None)
                            children_2.append(value_4)
                            offset_2 = offset_3

                            offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_line_end(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
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

                    while True: # start choice
                        offset_2 = offset_1
                        column_1 = column_0
                        indent_column_1 = indent_column_0
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            while True: # start reject
                                children_3 = []
                                offset_3 = offset_2 + 0
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                if not (column_2 == indent_column_2[0] == 0):
                                    offset_3 = -1
                                    break
                                # print('start')
                                for indent, dedent in prefix_0:
                                    # print(indent)
                                    _children, _prefix = [], []
                                    offset_4 = offset_3
                                    offset_4, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = indent(buf, offset_4, buf_eof, column_2, indent_column_2, _prefix, _children, partial_tab_offset_2, partial_tab_width_2)
                                    if _prefix or _children:
                                       raise Exception('bar')
                                    if offset_4 == -1:
                                        offset_3 = -1
                                        break
                                    offset_3 = offset_4
                                    indent_column_2 = (column_2, indent_column_2)
                                if offset_3 == -1:
                                    break

                                break
                            if offset_3 != -1:
                                offset_2 = -1
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
                            while offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
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

                            if offset_2 != buf_eof:
                                offset_2 = -1
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
                            if not (column_1 == indent_column_1[0] == 0):
                                offset_2 = -1
                                break
                            # print('start')
                            for indent, dedent in prefix_0:
                                # print(indent)
                                _children, _prefix = [], []
                                offset_3 = offset_2
                                offset_3, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_3, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_3 == -1:
                                    offset_2 = -1
                                    break
                                offset_2 = offset_3
                                indent_column_1 = (column_1, indent_column_1)
                            if offset_2 == -1:
                                break

                            count_0 = 0
                            while offset_2 < buf_eof and count_0 < 3:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
                                        if offset_2 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-(column_1%self.tabstop))
                                        if count_0 + width > 3:
                                            new_width = 3 - count_0
                                            count_0 += new_width
                                            column_1 += new_width
                                            partial_tab_offset_1 = offset_2
                                            partial_tab_width_1 = width - new_width
                                            break
                                        count_0 += width
                                        column_1 += width
                                        offset_2 += 1
                                    else:
                                        count_0 += 1
                                        column_1 += 1
                                        offset_2 += 1
                                else:
                                    break

                            count_0 = 0
                            while True:
                                offset_3 = offset_2
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_3 = [] if children_2 is not None else None
                                while True:
                                    count_1 = 0
                                    while offset_3 < buf_eof:
                                        codepoint = buf[offset_3]
                                        if codepoint in ' \t':
                                            if codepoint == '\t':
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

                                    if buf[offset_3:offset_3+1] == '`':
                                        offset_3 += 1
                                        column_2 += 1
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
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                count_0 += 1
                            if count_0 < value_1:
                                offset_2 = -1
                                break
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

                            offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_line_end(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
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
                value_5 = self.Node('fenced_code', offset_0, offset_1, children_1, None)
                children_0.append(value_5)
                offset_0 = offset_1


                break
            return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

        def parse_tilde_code_block(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                offset_1 = offset_0
                column_1 = column_0
                while True: # start count
                    count_0 = 0
                    while offset_1 < buf_eof and count_0 < 3:
                        codepoint = buf[offset_1]
                        if codepoint in ' \t':
                            if codepoint == '\t':
                                if offset_1 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                                    width = partial_tab_width_0
                                else:
                                    width  = (self.tabstop-(column_1%self.tabstop))
                                if count_0 + width > 3:
                                    new_width = 3 - count_0
                                    count_0 += new_width
                                    column_1 += new_width
                                    partial_tab_offset_0 = offset_1
                                    partial_tab_width_0 = width - new_width
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

                    break
                if offset_1 == -1:
                    offset_0 = -1; break
                value_0 = column_1 - column_0
                offset_0 = offset_1
                column_0 = column_1

                offset_1 = offset_0
                children_1 = []
                while True: # start capture
                    offset_2 = offset_1
                    column_1 = column_0
                    while True: # start count
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            column_2 = column_1
                            indent_column_1 = indent_column_0
                            partial_tab_offset_1 = partial_tab_offset_0
                            partial_tab_width_1 = partial_tab_width_0
                            children_2 = [] if children_1 is not None else None
                            while True:
                                if buf[offset_3:offset_3+1] == '~':
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
                        if count_0 < 3:
                            offset_2 = -1
                            break
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1; break
                    value_1 = buf[offset_1:offset_2].count('~')
                    offset_1 = offset_2
                    column_0 = column_1

                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        count_0 = 0
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
                                        offset_4, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_escaped_text(buf, offset_4, buf_eof, column_2, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                        if offset_4 == -1: break



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
                                        offset_4, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_html_entity(buf, offset_4, buf_eof, column_2, indent_column_2, prefix_0, children_4, partial_tab_offset_2, partial_tab_width_2)
                                        if offset_4 == -1: break



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
                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            codepoint = ord(buf[offset_5])

                                            if codepoint == 10:
                                                offset_5 = -1
                                                break
                                            else:
                                                offset_5 += 1
                                                column_2 += 1

                                            count_1 = 0
                                            while True:
                                                offset_6 = offset_5
                                                column_3 = column_2
                                                indent_column_3 = indent_column_2
                                                partial_tab_offset_3 = partial_tab_offset_2
                                                partial_tab_width_3 = partial_tab_width_2
                                                children_6 = [] if children_5 is not None else None
                                                while True:
                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    codepoint = ord(buf[offset_6])

                                                    if codepoint == 10:
                                                        offset_6 = -1
                                                        break
                                                    elif codepoint == 92:
                                                        offset_6 = -1
                                                        break
                                                    elif codepoint == 38:
                                                        offset_6 = -1
                                                        break
                                                    else:
                                                        offset_6 += 1
                                                        column_3 += 1

                                                    break
                                                if offset_6 == -1:
                                                    break
                                                if offset_5 == offset_6: break
                                                if children_6 is not None and children_6 is not None:
                                                    children_5.extend(children_6)
                                                offset_5 = offset_6
                                                column_2 = column_3
                                                indent_column_2 = indent_column_3
                                                partial_tab_offset_2 = partial_tab_offset_3
                                                partial_tab_width_2 = partial_tab_width_3
                                                count_1 += 1
                                            if offset_5 == -1:
                                                break

                                            break
                                        if offset_5 == -1:
                                            offset_4 = -1
                                            break
                                        value_2 = self.Node('text', offset_4, offset_5, children_5, None)
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
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_3 = self.Node('info', offset_1, offset_2, children_2, None)
                    children_1.append(value_3)
                    offset_1 = offset_2

                    offset_1, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_line_end(buf, offset_1, buf_eof, column_0, indent_column_0, prefix_0, children_1, partial_tab_offset_0, partial_tab_width_0)
                    if offset_1 == -1: break


                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        column_1 = column_0
                        indent_column_1 = indent_column_0
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True:
                            if not (column_1 == indent_column_1[0] == 0):
                                offset_2 = -1
                                break
                            # print('start')
                            for indent, dedent in prefix_0:
                                # print(indent)
                                _children, _prefix = [], []
                                offset_3 = offset_2
                                offset_3, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_3, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_3 == -1:
                                    offset_2 = -1
                                    break
                                offset_2 = offset_3
                                indent_column_1 = (column_1, indent_column_1)
                            if offset_2 == -1:
                                break

                            while True: # start reject
                                children_3 = []
                                offset_3 = offset_2 + 0
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                count_1 = 0
                                while offset_3 < buf_eof and count_1 < 3:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t':
                                        if codepoint == '\t':
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

                                count_1 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_3 = indent_column_2
                                    partial_tab_offset_3 = partial_tab_offset_2
                                    partial_tab_width_3 = partial_tab_width_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if buf[offset_4:offset_4+1] == '~':
                                            offset_4 += 1
                                            column_3 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_2 = 0
                                        while offset_4 < buf_eof:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t':
                                                if codepoint == '\t':
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
                                if count_1 < value_1:
                                    offset_3 = -1
                                    break
                                if offset_3 == -1:
                                    break

                                break
                            if offset_3 != -1:
                                offset_2 = -1
                                break

                            count_1 = 0
                            while offset_2 < buf_eof and count_1 < value_0:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
                                        if offset_2 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-(column_1%self.tabstop))
                                        if count_1 + width > value_0:
                                            new_width = value_0 - count_1
                                            count_1 += new_width
                                            column_1 += new_width
                                            partial_tab_offset_1 = offset_2
                                            partial_tab_width_1 = width - new_width
                                            break
                                        count_1 += width
                                        column_1 += width
                                        offset_2 += 1
                                    else:
                                        count_1 += 1
                                        column_1 += 1
                                        offset_2 += 1
                                else:
                                    break

                            offset_3 = offset_2
                            children_3 = []
                            while True: # start capture
                                count_1 = 0
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

                                        codepoint = ord(buf[offset_4])

                                        if codepoint == 10:
                                            offset_4 = -1
                                            break
                                        else:
                                            offset_4 += 1
                                            column_2 += 1

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

                                break
                            if offset_3 == -1:
                                offset_2 = -1
                                break
                            value_4 = self.Node('text', offset_2, offset_3, children_3, None)
                            children_2.append(value_4)
                            offset_2 = offset_3

                            offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_line_end(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
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

                    while True: # start choice
                        offset_2 = offset_1
                        column_1 = column_0
                        indent_column_1 = indent_column_0
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            while True: # start reject
                                children_3 = []
                                offset_3 = offset_2 + 0
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                if not (column_2 == indent_column_2[0] == 0):
                                    offset_3 = -1
                                    break
                                # print('start')
                                for indent, dedent in prefix_0:
                                    # print(indent)
                                    _children, _prefix = [], []
                                    offset_4 = offset_3
                                    offset_4, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = indent(buf, offset_4, buf_eof, column_2, indent_column_2, _prefix, _children, partial_tab_offset_2, partial_tab_width_2)
                                    if _prefix or _children:
                                       raise Exception('bar')
                                    if offset_4 == -1:
                                        offset_3 = -1
                                        break
                                    offset_3 = offset_4
                                    indent_column_2 = (column_2, indent_column_2)
                                if offset_3 == -1:
                                    break

                                break
                            if offset_3 != -1:
                                offset_2 = -1
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
                            while offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
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

                            if offset_2 != buf_eof:
                                offset_2 = -1
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
                            if not (column_1 == indent_column_1[0] == 0):
                                offset_2 = -1
                                break
                            # print('start')
                            for indent, dedent in prefix_0:
                                # print(indent)
                                _children, _prefix = [], []
                                offset_3 = offset_2
                                offset_3, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_3, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_3 == -1:
                                    offset_2 = -1
                                    break
                                offset_2 = offset_3
                                indent_column_1 = (column_1, indent_column_1)
                            if offset_2 == -1:
                                break

                            count_0 = 0
                            while offset_2 < buf_eof and count_0 < 3:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
                                        if offset_2 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-(column_1%self.tabstop))
                                        if count_0 + width > 3:
                                            new_width = 3 - count_0
                                            count_0 += new_width
                                            column_1 += new_width
                                            partial_tab_offset_1 = offset_2
                                            partial_tab_width_1 = width - new_width
                                            break
                                        count_0 += width
                                        column_1 += width
                                        offset_2 += 1
                                    else:
                                        count_0 += 1
                                        column_1 += 1
                                        offset_2 += 1
                                else:
                                    break

                            count_0 = 0
                            while True:
                                offset_3 = offset_2
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_3 = [] if children_2 is not None else None
                                while True:
                                    count_1 = 0
                                    while offset_3 < buf_eof:
                                        codepoint = buf[offset_3]
                                        if codepoint in ' \t':
                                            if codepoint == '\t':
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

                                    if buf[offset_3:offset_3+1] == '~':
                                        offset_3 += 1
                                        column_2 += 1
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
                                column_1 = column_2
                                indent_column_1 = indent_column_2
                                partial_tab_offset_1 = partial_tab_offset_2
                                partial_tab_width_1 = partial_tab_width_2
                                count_0 += 1
                            if count_0 < value_1:
                                offset_2 = -1
                                break
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

                            offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_line_end(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
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
                value_5 = self.Node('fenced_code', offset_0, offset_1, children_1, None)
                children_0.append(value_5)
                offset_0 = offset_1


                break
            return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

        def parse_start_blockquote(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                count_0 = 0
                while offset_0 < buf_eof and count_0 < 3:
                    codepoint = buf[offset_0]
                    if codepoint in ' \t':
                        if codepoint == '\t':
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
                        while True: # start lookahed
                            children_2 = []
                            offset_2 = offset_1 + 0
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            count_0 = 0
                            while offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
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
                                codepoint = buf[offset_2]
                                if codepoint in '\n':
                                    offset_2 +=1
                                    column_2 = 0
                                    indent_column_2 = (0, None)
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
                            codepoint = buf[offset_1]
                            if codepoint in ' \t':
                                if codepoint == '\t':
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

                        while True: # start lookahed
                            children_2 = []
                            offset_2 = offset_1 + 0
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            if offset_2 == buf_eof:
                                offset_2 = -1
                                break

                            codepoint = ord(buf[offset_2])

                            if codepoint == 10:
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

        def parse_blockquote_interrupt(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                while True: # start choice
                    offset_1 = offset_0
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_1 = [] if children_0 is not None else None
                    while True: # case
                        count_0 = 0
                        while offset_1 < buf_eof:
                            codepoint = buf[offset_1]
                            if codepoint in ' \t':
                                if codepoint == '\t':
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

                        if offset_1 < buf_eof:
                            codepoint = buf[offset_1]
                            if codepoint in '\n':
                                offset_1 +=1
                                column_1 = 0
                                indent_column_1 = (0, None)
                            else:
                                offset_1 = -1
                                break
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
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_start_fenced_block(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_start_list(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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

        def parse_blockquote(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                offset_1 = offset_0
                children_1 = []
                while True: # start capture
                    offset_1, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_start_blockquote(buf, offset_1, buf_eof, column_0, indent_column_0, prefix_0, children_1, partial_tab_offset_0, partial_tab_width_0)
                    if offset_1 == -1: break


                    while True: # start choice
                        offset_2 = offset_1
                        column_1 = column_0
                        indent_column_1 = indent_column_0
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

                            if offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in '\n':
                                    offset_2 +=1
                                    column_1 = 0
                                    indent_column_1 = (0, None)
                                else:
                                    offset_2 = -1
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
                            prefix_0.append((self.parse_start_blockquote, self.parse_blockquote_interrupt))
                            indent_column_1 = (column_1, indent_column_1)
                            while True:
                                offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_block_element(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                                if offset_2 == -1: break


                                break
                            prefix_0.pop()
                            if indent_column_1 != (0, None): indent_column_1 = indent_column_1[1]
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

                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        column_1 = column_0
                        indent_column_1 = indent_column_0
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True:
                            if not (column_1 == indent_column_1[0] == 0):
                                offset_2 = -1
                                break
                            # print('start')
                            for indent, dedent in prefix_0:
                                # print(indent)
                                _children, _prefix = [], []
                                offset_3 = offset_2
                                offset_3, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_3, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_3 == -1:
                                    offset_2 = -1
                                    break
                                offset_2 = offset_3
                                indent_column_1 = (column_1, indent_column_1)
                            if offset_2 == -1:
                                break

                            offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_start_blockquote(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                            if offset_2 == -1: break


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
                                        codepoint = buf[offset_3]
                                        if codepoint in ' \t':
                                            if codepoint == '\t':
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
                                        codepoint = buf[offset_3]
                                        if codepoint in '\n':
                                            offset_3 +=1
                                            column_2 = 0
                                            indent_column_2 = (0, None)
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
                                offset_3 = offset_2
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_3 = [] if children_2 is not None else None
                                while True: # case
                                    prefix_0.append((self.parse_start_blockquote, self.parse_blockquote_interrupt))
                                    indent_column_2 = (column_2, indent_column_2)
                                    while True:
                                        offset_3, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_block_element(buf, offset_3, buf_eof, column_2, indent_column_2, prefix_0, children_3, partial_tab_offset_2, partial_tab_width_2)
                                        if offset_3 == -1: break


                                        break
                                    prefix_0.pop()
                                    if indent_column_2 != (0, None): indent_column_2 = indent_column_2[1]
                                    if offset_3 == -1: break


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
                value_0 = self.Node('blockquote', offset_0, offset_1, children_1, None)
                children_0.append(value_0)
                offset_0 = offset_1

                break
            return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

        def parse_start_list(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                count_0 = 0
                while offset_0 < buf_eof and count_0 < 3:
                    codepoint = buf[offset_0]
                    if codepoint in ' \t':
                        if codepoint == '\t':
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
                        if offset_1 == buf_eof:
                            offset_1 = -1
                            break

                        codepoint = ord(buf[offset_1])

                        if codepoint == 45:
                            offset_1 += 1
                            column_1 += 1
                        elif codepoint == 42:
                            offset_1 += 1
                            column_1 += 1
                        elif codepoint == 43:
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
                        count_0 = 0
                        while count_0 < 9:
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
                            indent_column_1 = indent_column_2
                            partial_tab_offset_1 = partial_tab_offset_2
                            partial_tab_width_1 = partial_tab_width_2
                            count_0 += 1
                        if count_0 < 1:
                            offset_1 = -1
                            break
                        if offset_1 == -1:
                            break

                        if offset_1 == buf_eof:
                            offset_1 = -1
                            break

                        codepoint = ord(buf[offset_1])

                        if codepoint == 46:
                            offset_1 += 1
                            column_1 += 1
                        elif codepoint == 41:
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

                while True: # start choice
                    offset_1 = offset_0
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_1 = [] if children_0 is not None else None
                    while True: # case
                        while True: # start lookahed
                            children_2 = []
                            offset_2 = offset_1 + 0
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            count_0 = 0
                            while offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
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
                                codepoint = buf[offset_2]
                                if codepoint in '\n':
                                    offset_2 +=1
                                    column_2 = 0
                                    indent_column_2 = (0, None)
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
                            codepoint = buf[offset_1]
                            if codepoint in '\n':
                                offset_1 +=1
                                column_1 = 0
                                indent_column_1 = (0, None)
                                count_0 +=1
                            elif codepoint in ' \t':
                                if codepoint == '\t':
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
                        if count_0 < 1:
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

        def parse_list_interrupts(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                while True: # start choice
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
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_start_fenced_block(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_start_list(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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

        def parse_list_item(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                while True: # start choice
                    offset_1 = offset_0
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_1 = [] if children_0 is not None else None
                    while True: # case
                        while True: # start lookahed
                            children_2 = []
                            offset_2 = offset_1 + 0
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            count_0 = 0
                            while offset_2 < buf_eof and count_0 < 4:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
                                        if offset_2 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                            width = partial_tab_width_2
                                        else:
                                            width  = (self.tabstop-(column_2%self.tabstop))
                                        if count_0 + width > 4:
                                            new_width = 4 - count_0
                                            count_0 += new_width
                                            column_2 += new_width
                                            partial_tab_offset_2 = offset_2
                                            partial_tab_width_2 = width - new_width
                                            break
                                        count_0 += width
                                        column_2 += width
                                        offset_2 += 1
                                    else:
                                        count_0 += 1
                                        column_2 += 1
                                        offset_2 += 1
                                else:
                                    break
                            if count_0 < 4:
                                offset_2 = -1
                                break

                            while True: # start reject
                                children_3 = []
                                offset_3 = offset_2 + 0
                                column_3 = column_2
                                indent_column_3 = indent_column_2
                                partial_tab_offset_3 = partial_tab_offset_2
                                partial_tab_width_3 = partial_tab_width_2
                                offset_3, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = self.parse_line_end(buf, offset_3, buf_eof, column_3, indent_column_3, prefix_0, children_3, partial_tab_offset_3, partial_tab_width_3)
                                if offset_3 == -1: break


                                break
                            if offset_3 != -1:
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
                        while True: # start lookahed
                            children_2 = []
                            offset_2 = offset_1 + 0
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            offset_2, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_start_fenced_block(buf, offset_2, buf_eof, column_2, indent_column_2, prefix_0, children_2, partial_tab_offset_2, partial_tab_width_2)
                            if offset_2 == -1: break


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
                        while offset_1 < buf_eof:
                            codepoint = buf[offset_1]
                            if codepoint in ' \t':
                                if codepoint == '\t':
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

                        while True: # start reject
                            children_2 = []
                            offset_2 = offset_1 + 0
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            if offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in '\n':
                                    offset_2 +=1
                                    column_2 = 0
                                    indent_column_2 = (0, None)
                                else:
                                    offset_2 = -1
                                    break
                            else:
                                offset_2 = -1
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
                    offset_1 = offset_0
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    children_1 = [] if children_0 is not None else None
                    while True: # case
                        while True: # start lookahed
                            children_2 = []
                            offset_2 = offset_1 + 0
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            count_0 = 0
                            while offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
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
                                codepoint = buf[offset_2]
                                if codepoint in '\n':
                                    offset_2 +=1
                                    column_2 = 0
                                    indent_column_2 = (0, None)
                                else:
                                    offset_2 = -1
                                    break
                            else:
                                offset_2 = -1
                                break

                            break
                        if offset_2 == -1:
                            offset_1 = -1
                            break

                        count_0 = column_1 - indent_column_1[0]
                        # print(count_0, 'indent')
                        def _indent(buf, offset, buf_eof, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
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
                                elif codepoint in '\n':
                                    break
                                else:
                                    offset = -1
                                    break
                            return offset, column, indent_column, partial_tab_offset, partial_tab_width
                        def _dedent(buf, offset, buf_eof, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
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
                                elif codepoint in '\n':
                                    offset = -1; break
                                else:
                                    offset = start_offset
                            if count == 0:
                                    offset = -1
                            return offset, column, indent_column, partial_tab_offset, partial_tab_width
                        prefix_0.append((_indent, _dedent))
                        indent_column_1 = (column_1, indent_column_1)
                        while True:
                            count_0 = 0
                            while offset_1 < buf_eof:
                                codepoint = buf[offset_1]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
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

                            if offset_1 < buf_eof:
                                codepoint = buf[offset_1]
                                if codepoint in '\n':
                                    offset_1 +=1
                                    column_1 = 0
                                    indent_column_1 = (0, None)
                                else:
                                    offset_1 = -1
                                    break
                            else:
                                offset_1 = -1
                                break

                            if not (column_1 == indent_column_1[0] == 0):
                                offset_1 = -1
                                break
                            # print('start')
                            for indent, dedent in prefix_0:
                                # print(indent)
                                _children, _prefix = [], []
                                offset_2 = offset_1
                                offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_2, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_2 == -1:
                                    offset_1 = -1
                                    break
                                offset_1 = offset_2
                                indent_column_1 = (column_1, indent_column_1)
                            if offset_1 == -1:
                                break

                            break
                        prefix_0.pop()
                        if indent_column_1 != (0, None): indent_column_1 = indent_column_1[1]
                        if offset_1 == -1: break

                        count_0 = 0
                        while offset_1 < buf_eof and count_0 < 1:
                            codepoint = buf[offset_1]
                            if codepoint in ' \t':
                                if codepoint == '\t':
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
                        if count_0 < 1:
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

                value_0 = column_0 - indent_column_0[0]

                count_0 = value_0
                # print(count_0, 'indent')
                def _indent(buf, offset, buf_eof, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
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
                        elif codepoint in '\n':
                            break
                        else:
                            offset = -1
                            break
                    return offset, column, indent_column, partial_tab_offset, partial_tab_width
                prefix_0.append((_indent, self.parse_list_interrupts))
                indent_column_0 = (column_0, indent_column_0)
                while True:
                    offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_block_element(buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0)
                    if offset_0 == -1: break


                    break
                prefix_0.pop()
                if indent_column_0 != (0, None): indent_column_0 = indent_column_0[1]
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
                        count_1 = value_0
                        # print(count_1, 'indent')
                        def _indent(buf, offset, buf_eof, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_1, allow_mixed_indent=self.allow_mixed_indent):
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
                                elif codepoint in '\n':
                                    break
                                else:
                                    offset = -1
                                    break
                            return offset, column, indent_column, partial_tab_offset, partial_tab_width
                        prefix_0.append((_indent, self.parse_list_interrupts))
                        indent_column_1 = (column_1, indent_column_1)
                        while True:
                            if not (column_1 == indent_column_1[0] == 0):
                                offset_1 = -1
                                break
                            # print('start')
                            for indent, dedent in prefix_0:
                                # print(indent)
                                _children, _prefix = [], []
                                offset_2 = offset_1
                                offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_2, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_2 == -1:
                                    if dedent is None:
                                        offset_1 = -1
                                        break
                                    _children, _prefix = [], []
                                    offset_2 = offset_1
                                    offset_2, _column, _indent_column, _partial_tab_offset, _partial_tab_width = dedent(buf, offset_2, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                    if offset_2 != -1:
                                        offset_1 = -1
                                        break
                                    else:
                                        offset_2 = offset_1
                                offset_1 = offset_2
                                indent_column_1 = (column_1, indent_column_1)
                            if offset_1 == -1:
                                break

                            count_1 = 0
                            while count_1 < 1:
                                offset_2 = offset_1
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_2 = [] if children_1 is not None else None
                                while True:
                                    count_2 = 0
                                    while True:
                                        offset_3 = offset_2
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_3 = [] if children_2 is not None else None
                                        while True:
                                            count_3 = 0
                                            while offset_3 < buf_eof:
                                                codepoint = buf[offset_3]
                                                if codepoint in ' \t':
                                                    if codepoint == '\t':
                                                        if offset_3 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                            width = partial_tab_width_3
                                                        else:
                                                            width  = (self.tabstop-(column_3%self.tabstop))
                                                        count_3 += width
                                                        column_3 += width
                                                        offset_3 += 1
                                                    else:
                                                        count_3 += 1
                                                        column_3 += 1
                                                        offset_3 += 1
                                                else:
                                                    break

                                            offset_4 = offset_3
                                            children_4 = []
                                            while True: # start capture
                                                if offset_4 < buf_eof:
                                                    codepoint = buf[offset_4]
                                                    if codepoint in '\n':
                                                        offset_4 +=1
                                                        column_3 = 0
                                                        indent_column_3 = (0, None)
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
                                            value_1 = self.Node('empty', offset_3, offset_4, children_4, None)
                                            children_3.append(value_1)
                                            offset_3 = offset_4

                                            if not (column_3 == indent_column_3[0] == 0):
                                                offset_3 = -1
                                                break
                                            # print('start')
                                            for indent, dedent in prefix_0:
                                                # print(indent)
                                                _children, _prefix = [], []
                                                offset_4 = offset_3
                                                offset_4, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_4, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                                if _prefix or _children:
                                                   raise Exception('bar')
                                                if offset_4 == -1:
                                                    offset_3 = -1
                                                    break
                                                offset_3 = offset_4
                                                indent_column_3 = (column_3, indent_column_3)
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
                                        indent_column_2 = indent_column_3
                                        partial_tab_offset_2 = partial_tab_offset_3
                                        partial_tab_width_2 = partial_tab_width_3
                                        count_2 += 1
                                    if offset_2 == -1:
                                        break

                                    while True: # start lookahed
                                        children_3 = []
                                        offset_3 = offset_2 + 0
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        count_2 = 0
                                        while offset_3 < buf_eof:
                                            codepoint = buf[offset_3]
                                            if codepoint in ' \t':
                                                if codepoint == '\t':
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
                                break
                            if offset_1 == -1:
                                break

                            break
                        prefix_0.pop()
                        if indent_column_1 != (0, None): indent_column_1 = indent_column_1[1]
                        if offset_1 == -1: break

                        count_1 = value_0
                        # print(count_1, 'indent')
                        def _indent(buf, offset, buf_eof, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count=count_1, allow_mixed_indent=self.allow_mixed_indent):
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
                                elif codepoint in '\n':
                                    break
                                else:
                                    offset = -1
                                    break
                            return offset, column, indent_column, partial_tab_offset, partial_tab_width
                        prefix_0.append((_indent, self.parse_list_interrupts))
                        indent_column_1 = (column_1, indent_column_1)
                        while True:
                            offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_block_element(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
                            if offset_1 == -1: break


                            break
                        prefix_0.pop()
                        if indent_column_1 != (0, None): indent_column_1 = indent_column_1[1]
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


                break
            return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

        def parse_unordered_list(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                while True: # start reject
                    children_1 = []
                    offset_1 = offset_0 + 0
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_thematic_break(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
                    if offset_1 == -1: break


                    break
                if offset_1 != -1:
                    offset_0 = -1
                    break

                offset_1 = offset_0
                children_1 = []
                while True: # start capture
                    count_0 = 0
                    while offset_1 < buf_eof and count_0 < 3:
                        codepoint = buf[offset_1]
                        if codepoint in ' \t':
                            if codepoint == '\t':
                                if offset_1 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                                    width = partial_tab_width_0
                                else:
                                    width  = (self.tabstop-(column_0%self.tabstop))
                                if count_0 + width > 3:
                                    new_width = 3 - count_0
                                    count_0 += new_width
                                    column_0 += new_width
                                    partial_tab_offset_0 = offset_1
                                    partial_tab_width_0 = width - new_width
                                    break
                                count_0 += width
                                column_0 += width
                                offset_1 += 1
                            else:
                                count_0 += 1
                                column_0 += 1
                                offset_1 += 1
                        else:
                            break

                    offset_2 = offset_1
                    while True: # start backref
                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break

                        codepoint = ord(buf[offset_2])

                        if codepoint == 45:
                            offset_2 += 1
                            column_0 += 1
                        elif codepoint == 42:
                            offset_2 += 1
                            column_0 += 1
                        elif codepoint == 43:
                            offset_2 += 1
                            column_0 += 1
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_0 = buf[offset_1:offset_2]
                    offset_1 = offset_2

                    while True: # start choice
                        offset_2 = offset_1
                        column_1 = column_0
                        indent_column_1 = indent_column_0
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            while True: # start lookahed
                                children_3 = []
                                offset_3 = offset_2 + 0
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                count_0 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_0 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_0 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                if offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in '\n':
                                        offset_3 +=1
                                        column_2 = 0
                                        indent_column_2 = (0, None)
                                    else:
                                        offset_3 = -1
                                        break

                                break
                            if offset_3 == -1:
                                offset_2 = -1
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
                            while offset_2 < buf_eof and count_0 < 1:
                                codepoint = buf[offset_2]
                                if codepoint in '\n':
                                    offset_2 +=1
                                    column_1 = 0
                                    indent_column_1 = (0, None)
                                    count_0 +=1
                                elif codepoint in ' \t':
                                    if codepoint == '\t':
                                        if offset_2 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-(column_1%self.tabstop))
                                        if count_0 + width > 1:
                                            new_width = 1 - count_0
                                            count_0 += new_width
                                            column_1 += new_width
                                            partial_tab_offset_1 = offset_2
                                            partial_tab_width_1 = width - new_width
                                            break
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

                    while True: # start choice
                        offset_2 = offset_1
                        column_1 = column_0
                        indent_column_1 = indent_column_0
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            offset_3 = offset_2
                            children_3 = []
                            while True: # start capture
                                offset_3, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_list_item(buf, offset_3, buf_eof, column_1, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                                if offset_3 == -1: break


                                break
                            if offset_3 == -1:
                                offset_2 = -1
                                break
                            value_1 = self.Node('list_item', offset_2, offset_3, children_3, None)
                            children_2.append(value_1)
                            offset_2 = offset_3


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
                            offset_3 = offset_2
                            children_3 = []
                            while True: # start capture
                                count_0 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                                width = partial_tab_width_1
                                            else:
                                                width  = (self.tabstop-(column_1%self.tabstop))
                                            count_0 += width
                                            column_1 += width
                                            offset_3 += 1
                                        else:
                                            count_0 += 1
                                            column_1 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                break
                            if offset_3 == -1:
                                offset_2 = -1
                                break
                            value_2 = self.Node('list_item', offset_2, offset_3, children_3, None)
                            children_2.append(value_2)
                            offset_2 = offset_3

                            if offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in '\n':
                                    offset_2 +=1
                                    column_1 = 0
                                    indent_column_1 = (0, None)
                                else:
                                    offset_2 = -1
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

                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        column_1 = column_0
                        indent_column_1 = indent_column_0
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True:
                            if not (column_1 == indent_column_1[0] == 0):
                                offset_2 = -1
                                break
                            # print('start')
                            for indent, dedent in prefix_0:
                                # print(indent)
                                _children, _prefix = [], []
                                offset_3 = offset_2
                                offset_3, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_3, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_3 == -1:
                                    offset_2 = -1
                                    break
                                offset_2 = offset_3
                                indent_column_1 = (column_1, indent_column_1)
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
                                        codepoint = buf[offset_3]
                                        if codepoint in ' \t':
                                            if codepoint == '\t':
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
                                        codepoint = buf[offset_3]
                                        if codepoint in '\n':
                                            offset_3 +=1
                                            column_2 = 0
                                            indent_column_2 = (0, None)
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
                                                if not (column_3 == indent_column_3[0] == 0):
                                                    offset_5 = -1
                                                    break
                                                # print('start')
                                                for indent, dedent in prefix_0:
                                                    # print(indent)
                                                    _children, _prefix = [], []
                                                    offset_6 = offset_5
                                                    offset_6, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_6, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                                    if _prefix or _children:
                                                       raise Exception('bar')
                                                    if offset_6 == -1:
                                                        offset_5 = -1
                                                        break
                                                    offset_5 = offset_6
                                                    indent_column_3 = (column_3, indent_column_3)
                                                if offset_5 == -1:
                                                    break

                                                count_2 = 0
                                                while offset_5 < buf_eof:
                                                    codepoint = buf[offset_5]
                                                    if codepoint in ' \t':
                                                        if codepoint == '\t':
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
                                                    codepoint = buf[offset_5]
                                                    if codepoint in '\n':
                                                        offset_5 +=1
                                                        column_3 = 0
                                                        indent_column_3 = (0, None)
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
                                    value_3 = self.Node('empty', offset_3, offset_4, children_4, None)
                                    children_3.append(value_3)
                                    offset_3 = offset_4

                                    while True: # start lookahed
                                        children_4 = []
                                        offset_4 = offset_3 + 0
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        if not (column_3 == indent_column_3[0] == 0):
                                            offset_4 = -1
                                            break
                                        # print('start')
                                        for indent, dedent in prefix_0:
                                            # print(indent)
                                            _children, _prefix = [], []
                                            offset_5 = offset_4
                                            offset_5, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_5, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                            if _prefix or _children:
                                               raise Exception('bar')
                                            if offset_5 == -1:
                                                offset_4 = -1
                                                break
                                            offset_4 = offset_5
                                            indent_column_3 = (column_3, indent_column_3)
                                        if offset_4 == -1:
                                            break

                                        count_1 = 0
                                        while offset_4 < buf_eof and count_1 < 3:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t':
                                                if codepoint == '\t':
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

                                        if buf[offset_4:offset_4+len(value_0)] == value_0:
                                            offset_4 += len(value_0)
                                            column_3 += len(value_0)
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
                                    while True: # start reject
                                        children_4 = []
                                        offset_4 = offset_3 + 0
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        offset_4, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = self.parse_thematic_break(buf, offset_4, buf_eof, column_3, indent_column_3, prefix_0, children_4, partial_tab_offset_3, partial_tab_width_3)
                                        if offset_4 == -1: break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = -1
                                        break

                                    count_1 = 0
                                    while offset_3 < buf_eof and count_1 < 3:
                                        codepoint = buf[offset_3]
                                        if codepoint in ' \t':
                                            if codepoint == '\t':
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

                                    if buf[offset_3:offset_3+len(value_0)] == value_0:
                                        offset_3 += len(value_0)
                                        column_2 += len(value_0)
                                    else:
                                        offset_3 = -1
                                        break

                                    while True: # start choice
                                        offset_4 = offset_3
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_4 = [] if children_3 is not None else None
                                        while True: # case
                                            while True: # start lookahed
                                                children_5 = []
                                                offset_5 = offset_4 + 0
                                                column_4 = column_3
                                                indent_column_4 = indent_column_3
                                                partial_tab_offset_4 = partial_tab_offset_3
                                                partial_tab_width_4 = partial_tab_width_3
                                                count_1 = 0
                                                while offset_5 < buf_eof:
                                                    codepoint = buf[offset_5]
                                                    if codepoint in ' \t':
                                                        if codepoint == '\t':
                                                            if offset_5 == partial_tab_offset_4 and partial_tab_width_4 > 0:
                                                                width = partial_tab_width_4
                                                            else:
                                                                width  = (self.tabstop-(column_4%self.tabstop))
                                                            count_1 += width
                                                            column_4 += width
                                                            offset_5 += 1
                                                        else:
                                                            count_1 += 1
                                                            column_4 += 1
                                                            offset_5 += 1
                                                    else:
                                                        break

                                                if offset_5 < buf_eof:
                                                    codepoint = buf[offset_5]
                                                    if codepoint in '\n':
                                                        offset_5 +=1
                                                        column_4 = 0
                                                        indent_column_4 = (0, None)
                                                    else:
                                                        offset_5 = -1
                                                        break

                                                break
                                            if offset_5 == -1:
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
                                            count_1 = 0
                                            while offset_4 < buf_eof and count_1 < 1:
                                                codepoint = buf[offset_4]
                                                if codepoint in '\n':
                                                    offset_4 +=1
                                                    column_3 = 0
                                                    indent_column_3 = (0, None)
                                                    count_1 +=1
                                                elif codepoint in ' \t':
                                                    if codepoint == '\t':
                                                        if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                            width = partial_tab_width_3
                                                        else:
                                                            width  = (self.tabstop-(column_3%self.tabstop))
                                                        if count_1 + width > 1:
                                                            new_width = 1 - count_1
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
                                            if count_1 < 1:
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

                                    while True: # start choice
                                        offset_4 = offset_3
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_4 = [] if children_3 is not None else None
                                        while True: # case
                                            offset_5 = offset_4
                                            children_5 = []
                                            while True: # start capture
                                                offset_5, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = self.parse_list_item(buf, offset_5, buf_eof, column_3, indent_column_3, prefix_0, children_5, partial_tab_offset_3, partial_tab_width_3)
                                                if offset_5 == -1: break


                                                break
                                            if offset_5 == -1:
                                                offset_4 = -1
                                                break
                                            value_4 = self.Node('list_item', offset_4, offset_5, children_5, None)
                                            children_4.append(value_4)
                                            offset_4 = offset_5


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
                                            offset_5 = offset_4
                                            children_5 = []
                                            while True: # start capture
                                                count_1 = 0
                                                while offset_5 < buf_eof:
                                                    codepoint = buf[offset_5]
                                                    if codepoint in ' \t':
                                                        if codepoint == '\t':
                                                            if offset_5 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                                width = partial_tab_width_3
                                                            else:
                                                                width  = (self.tabstop-(column_3%self.tabstop))
                                                            count_1 += width
                                                            column_3 += width
                                                            offset_5 += 1
                                                        else:
                                                            count_1 += 1
                                                            column_3 += 1
                                                            offset_5 += 1
                                                    else:
                                                        break

                                                break
                                            if offset_5 == -1:
                                                offset_4 = -1
                                                break
                                            value_5 = self.Node('list_item', offset_4, offset_5, children_5, None)
                                            children_4.append(value_5)
                                            offset_4 = offset_5

                                            if offset_4 < buf_eof:
                                                codepoint = buf[offset_4]
                                                if codepoint in '\n':
                                                    offset_4 +=1
                                                    column_3 = 0
                                                    indent_column_3 = (0, None)
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
                value_6 = self.Node('unordered_list', offset_0, offset_1, children_1, None)
                children_0.append(value_6)
                offset_0 = offset_1


                break
            return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

        def parse_ordered_list(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                offset_1 = offset_0
                children_1 = []
                while True: # start capture
                    count_0 = 0
                    while offset_1 < buf_eof and count_0 < 3:
                        codepoint = buf[offset_1]
                        if codepoint in ' \t':
                            if codepoint == '\t':
                                if offset_1 == partial_tab_offset_0 and partial_tab_width_0 > 0:
                                    width = partial_tab_width_0
                                else:
                                    width  = (self.tabstop-(column_0%self.tabstop))
                                if count_0 + width > 3:
                                    new_width = 3 - count_0
                                    count_0 += new_width
                                    column_0 += new_width
                                    partial_tab_offset_0 = offset_1
                                    partial_tab_width_0 = width - new_width
                                    break
                                count_0 += width
                                column_0 += width
                                offset_1 += 1
                            else:
                                count_0 += 1
                                column_0 += 1
                                offset_1 += 1
                        else:
                            break

                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        count_0 = 0
                        while count_0 < 9:
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

                                codepoint = ord(buf[offset_3])

                                if 48 <= codepoint <= 57:
                                    offset_3 += 1
                                    column_1 += 1
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
                    value_0 = self.Node('ordered_list_start', offset_1, offset_2, children_2, None)
                    children_1.append(value_0)
                    offset_1 = offset_2

                    offset_2 = offset_1
                    while True: # start backref
                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break

                        codepoint = ord(buf[offset_2])

                        if codepoint == 46:
                            offset_2 += 1
                            column_0 += 1
                        elif codepoint == 41:
                            offset_2 += 1
                            column_0 += 1
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    value_1 = buf[offset_1:offset_2]
                    offset_1 = offset_2

                    while True: # start choice
                        offset_2 = offset_1
                        column_1 = column_0
                        indent_column_1 = indent_column_0
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            while True: # start lookahed
                                children_3 = []
                                offset_3 = offset_2 + 0
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                count_0 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_2 and partial_tab_width_2 > 0:
                                                width = partial_tab_width_2
                                            else:
                                                width  = (self.tabstop-(column_2%self.tabstop))
                                            count_0 += width
                                            column_2 += width
                                            offset_3 += 1
                                        else:
                                            count_0 += 1
                                            column_2 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                if offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in '\n':
                                        offset_3 +=1
                                        column_2 = 0
                                        indent_column_2 = (0, None)
                                    else:
                                        offset_3 = -1
                                        break

                                break
                            if offset_3 == -1:
                                offset_2 = -1
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
                            while offset_2 < buf_eof and count_0 < 1:
                                codepoint = buf[offset_2]
                                if codepoint in '\n':
                                    offset_2 +=1
                                    column_1 = 0
                                    indent_column_1 = (0, None)
                                    count_0 +=1
                                elif codepoint in ' \t':
                                    if codepoint == '\t':
                                        if offset_2 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                            width = partial_tab_width_1
                                        else:
                                            width  = (self.tabstop-(column_1%self.tabstop))
                                        if count_0 + width > 1:
                                            new_width = 1 - count_0
                                            count_0 += new_width
                                            column_1 += new_width
                                            partial_tab_offset_1 = offset_2
                                            partial_tab_width_1 = width - new_width
                                            break
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

                    while True: # start choice
                        offset_2 = offset_1
                        column_1 = column_0
                        indent_column_1 = indent_column_0
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True: # case
                            offset_3 = offset_2
                            children_3 = []
                            while True: # start capture
                                offset_3, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_list_item(buf, offset_3, buf_eof, column_1, indent_column_1, prefix_0, children_3, partial_tab_offset_1, partial_tab_width_1)
                                if offset_3 == -1: break


                                break
                            if offset_3 == -1:
                                offset_2 = -1
                                break
                            value_2 = self.Node('list_item', offset_2, offset_3, children_3, None)
                            children_2.append(value_2)
                            offset_2 = offset_3


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
                            offset_3 = offset_2
                            children_3 = []
                            while True: # start capture
                                count_0 = 0
                                while offset_3 < buf_eof:
                                    codepoint = buf[offset_3]
                                    if codepoint in ' \t':
                                        if codepoint == '\t':
                                            if offset_3 == partial_tab_offset_1 and partial_tab_width_1 > 0:
                                                width = partial_tab_width_1
                                            else:
                                                width  = (self.tabstop-(column_1%self.tabstop))
                                            count_0 += width
                                            column_1 += width
                                            offset_3 += 1
                                        else:
                                            count_0 += 1
                                            column_1 += 1
                                            offset_3 += 1
                                    else:
                                        break

                                break
                            if offset_3 == -1:
                                offset_2 = -1
                                break
                            value_3 = self.Node('list_item', offset_2, offset_3, children_3, None)
                            children_2.append(value_3)
                            offset_2 = offset_3

                            if offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in '\n':
                                    offset_2 +=1
                                    column_1 = 0
                                    indent_column_1 = (0, None)
                                else:
                                    offset_2 = -1
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

                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        column_1 = column_0
                        indent_column_1 = indent_column_0
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True:
                            if not (column_1 == indent_column_1[0] == 0):
                                offset_2 = -1
                                break
                            # print('start')
                            for indent, dedent in prefix_0:
                                # print(indent)
                                _children, _prefix = [], []
                                offset_3 = offset_2
                                offset_3, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_3, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_3 == -1:
                                    offset_2 = -1
                                    break
                                offset_2 = offset_3
                                indent_column_1 = (column_1, indent_column_1)
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
                                        codepoint = buf[offset_3]
                                        if codepoint in ' \t':
                                            if codepoint == '\t':
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
                                        codepoint = buf[offset_3]
                                        if codepoint in '\n':
                                            offset_3 +=1
                                            column_2 = 0
                                            indent_column_2 = (0, None)
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
                                                if not (column_3 == indent_column_3[0] == 0):
                                                    offset_5 = -1
                                                    break
                                                # print('start')
                                                for indent, dedent in prefix_0:
                                                    # print(indent)
                                                    _children, _prefix = [], []
                                                    offset_6 = offset_5
                                                    offset_6, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_6, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                                    if _prefix or _children:
                                                       raise Exception('bar')
                                                    if offset_6 == -1:
                                                        offset_5 = -1
                                                        break
                                                    offset_5 = offset_6
                                                    indent_column_3 = (column_3, indent_column_3)
                                                if offset_5 == -1:
                                                    break

                                                count_2 = 0
                                                while offset_5 < buf_eof:
                                                    codepoint = buf[offset_5]
                                                    if codepoint in ' \t':
                                                        if codepoint == '\t':
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
                                                    codepoint = buf[offset_5]
                                                    if codepoint in '\n':
                                                        offset_5 +=1
                                                        column_3 = 0
                                                        indent_column_3 = (0, None)
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
                                    value_4 = self.Node('empty', offset_3, offset_4, children_4, None)
                                    children_3.append(value_4)
                                    offset_3 = offset_4

                                    while True: # start lookahed
                                        children_4 = []
                                        offset_4 = offset_3 + 0
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        if not (column_3 == indent_column_3[0] == 0):
                                            offset_4 = -1
                                            break
                                        # print('start')
                                        for indent, dedent in prefix_0:
                                            # print(indent)
                                            _children, _prefix = [], []
                                            offset_5 = offset_4
                                            offset_5, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_5, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                            if _prefix or _children:
                                               raise Exception('bar')
                                            if offset_5 == -1:
                                                offset_4 = -1
                                                break
                                            offset_4 = offset_5
                                            indent_column_3 = (column_3, indent_column_3)
                                        if offset_4 == -1:
                                            break

                                        count_1 = 0
                                        while offset_4 < buf_eof and count_1 < 3:
                                            codepoint = buf[offset_4]
                                            if codepoint in ' \t':
                                                if codepoint == '\t':
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

                                        count_1 = 0
                                        while count_1 < 9:
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

                                                codepoint = ord(buf[offset_5])

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
                                        if count_1 < 1:
                                            offset_4 = -1
                                            break
                                        if offset_4 == -1:
                                            break

                                        if buf[offset_4:offset_4+len(value_1)] == value_1:
                                            offset_4 += len(value_1)
                                            column_3 += len(value_1)
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
                                        codepoint = buf[offset_3]
                                        if codepoint in ' \t':
                                            if codepoint == '\t':
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

                                    count_1 = 0
                                    while count_1 < 9:
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

                                            codepoint = ord(buf[offset_4])

                                            if 48 <= codepoint <= 57:
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
                                        count_1 += 1
                                    if count_1 < 1:
                                        offset_3 = -1
                                        break
                                    if offset_3 == -1:
                                        break

                                    if buf[offset_3:offset_3+len(value_1)] == value_1:
                                        offset_3 += len(value_1)
                                        column_2 += len(value_1)
                                    else:
                                        offset_3 = -1
                                        break

                                    while True: # start choice
                                        offset_4 = offset_3
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_4 = [] if children_3 is not None else None
                                        while True: # case
                                            while True: # start lookahed
                                                children_5 = []
                                                offset_5 = offset_4 + 0
                                                column_4 = column_3
                                                indent_column_4 = indent_column_3
                                                partial_tab_offset_4 = partial_tab_offset_3
                                                partial_tab_width_4 = partial_tab_width_3
                                                count_1 = 0
                                                while offset_5 < buf_eof:
                                                    codepoint = buf[offset_5]
                                                    if codepoint in ' \t':
                                                        if codepoint == '\t':
                                                            if offset_5 == partial_tab_offset_4 and partial_tab_width_4 > 0:
                                                                width = partial_tab_width_4
                                                            else:
                                                                width  = (self.tabstop-(column_4%self.tabstop))
                                                            count_1 += width
                                                            column_4 += width
                                                            offset_5 += 1
                                                        else:
                                                            count_1 += 1
                                                            column_4 += 1
                                                            offset_5 += 1
                                                    else:
                                                        break

                                                if offset_5 < buf_eof:
                                                    codepoint = buf[offset_5]
                                                    if codepoint in '\n':
                                                        offset_5 +=1
                                                        column_4 = 0
                                                        indent_column_4 = (0, None)
                                                    else:
                                                        offset_5 = -1
                                                        break

                                                break
                                            if offset_5 == -1:
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
                                            count_1 = 0
                                            while offset_4 < buf_eof and count_1 < 1:
                                                codepoint = buf[offset_4]
                                                if codepoint in '\n':
                                                    offset_4 +=1
                                                    column_3 = 0
                                                    indent_column_3 = (0, None)
                                                    count_1 +=1
                                                elif codepoint in ' \t':
                                                    if codepoint == '\t':
                                                        if offset_4 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                            width = partial_tab_width_3
                                                        else:
                                                            width  = (self.tabstop-(column_3%self.tabstop))
                                                        if count_1 + width > 1:
                                                            new_width = 1 - count_1
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
                                            if count_1 < 1:
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

                                    while True: # start choice
                                        offset_4 = offset_3
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_4 = [] if children_3 is not None else None
                                        while True: # case
                                            offset_5 = offset_4
                                            children_5 = []
                                            while True: # start capture
                                                offset_5, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = self.parse_list_item(buf, offset_5, buf_eof, column_3, indent_column_3, prefix_0, children_5, partial_tab_offset_3, partial_tab_width_3)
                                                if offset_5 == -1: break


                                                break
                                            if offset_5 == -1:
                                                offset_4 = -1
                                                break
                                            value_5 = self.Node('list_item', offset_4, offset_5, children_5, None)
                                            children_4.append(value_5)
                                            offset_4 = offset_5


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
                                            offset_5 = offset_4
                                            children_5 = []
                                            while True: # start capture
                                                count_1 = 0
                                                while offset_5 < buf_eof:
                                                    codepoint = buf[offset_5]
                                                    if codepoint in ' \t':
                                                        if codepoint == '\t':
                                                            if offset_5 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                                width = partial_tab_width_3
                                                            else:
                                                                width  = (self.tabstop-(column_3%self.tabstop))
                                                            count_1 += width
                                                            column_3 += width
                                                            offset_5 += 1
                                                        else:
                                                            count_1 += 1
                                                            column_3 += 1
                                                            offset_5 += 1
                                                    else:
                                                        break

                                                break
                                            if offset_5 == -1:
                                                offset_4 = -1
                                                break
                                            value_6 = self.Node('list_item', offset_4, offset_5, children_5, None)
                                            children_4.append(value_6)
                                            offset_4 = offset_5

                                            if offset_4 < buf_eof:
                                                codepoint = buf[offset_4]
                                                if codepoint in '\n':
                                                    offset_4 +=1
                                                    column_3 = 0
                                                    indent_column_3 = (0, None)
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
                value_7 = self.Node('ordered_list', offset_0, offset_1, children_1, None)
                children_0.append(value_7)
                offset_0 = offset_1

                break
            return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

        def parse_setext_heading_line(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                count_0 = 0
                while offset_0 < buf_eof and count_0 < 3:
                    codepoint = buf[offset_0]
                    if codepoint in ' \t':
                        if codepoint == '\t':
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

        def parse_no_setext_heading_line(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                while True: # start reject
                    children_1 = []
                    offset_1 = offset_0 + 0
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_setext_heading_line(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
                    if offset_1 == -1: break


                    break
                if offset_1 != -1:
                    offset_0 = -1
                    break

                break
            return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

        def parse_para(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                count_0 = 0
                while offset_0 < buf_eof and count_0 < 3:
                    codepoint = buf[offset_0]
                    if codepoint in ' \t':
                        if codepoint == '\t':
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
                    prefix_0.append((self.parse_no_setext_heading_line, None))
                    indent_column_0 = (column_0, indent_column_0)
                    while True:
                        offset_1, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0 = self.parse_inline_element(buf, offset_1, buf_eof, column_0, indent_column_0, prefix_0, children_1, partial_tab_offset_0, partial_tab_width_0)
                        if offset_1 == -1: break


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
                                        while True: # start choice
                                            offset_4 = offset_3
                                            column_3 = column_2
                                            indent_column_3 = indent_column_2
                                            partial_tab_offset_3 = partial_tab_offset_2
                                            partial_tab_width_3 = partial_tab_width_2
                                            children_4 = [] if children_3 is not None else None
                                            while True: # case
                                                while True: # start choice
                                                    offset_5 = offset_4
                                                    column_4 = column_3
                                                    indent_column_4 = indent_column_3
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_5 = [] if children_4 is not None else None
                                                    while True: # case
                                                        count_1 = 0
                                                        while offset_5 < buf_eof:
                                                            codepoint = buf[offset_5]
                                                            if codepoint in ' \t':
                                                                if codepoint == '\t':
                                                                    if offset_5 == partial_tab_offset_4 and partial_tab_width_4 > 0:
                                                                        width = partial_tab_width_4
                                                                    else:
                                                                        width  = (self.tabstop-(column_4%self.tabstop))
                                                                    count_1 += width
                                                                    column_4 += width
                                                                    offset_5 += 1
                                                                else:
                                                                    count_1 += 1
                                                                    column_4 += 1
                                                                    offset_5 += 1
                                                            else:
                                                                break
                                                        if count_1 < 2:
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
                                                        if buf[offset_5:offset_5+1] == '\\':
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

                                                offset_5 = offset_4
                                                children_5 = []
                                                while True: # start capture
                                                    if offset_5 < buf_eof:
                                                        codepoint = buf[offset_5]
                                                        if codepoint in '\n':
                                                            offset_5 +=1
                                                            column_3 = 0
                                                            indent_column_3 = (0, None)
                                                        else:
                                                            offset_5 = -1
                                                            break
                                                    else:
                                                        offset_5 = -1
                                                        break

                                                    break
                                                if offset_5 == -1:
                                                    offset_4 = -1
                                                    break
                                                value_0 = self.Node('hardbreak', offset_4, offset_5, children_5, None)
                                                children_4.append(value_0)
                                                offset_4 = offset_5


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
                                                count_1 = 0
                                                while offset_4 < buf_eof:
                                                    codepoint = buf[offset_4]
                                                    if codepoint in ' \t':
                                                        if codepoint == '\t':
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

                                                offset_5 = offset_4
                                                children_5 = []
                                                while True: # start capture
                                                    if offset_5 < buf_eof:
                                                        codepoint = buf[offset_5]
                                                        if codepoint in '\n':
                                                            offset_5 +=1
                                                            column_3 = 0
                                                            indent_column_3 = (0, None)
                                                        else:
                                                            offset_5 = -1
                                                            break
                                                    else:
                                                        offset_5 = -1
                                                        break

                                                    break
                                                if offset_5 == -1:
                                                    offset_4 = -1
                                                    break
                                                value_1 = self.Node('softbreak', offset_4, offset_5, children_5, None)
                                                children_4.append(value_1)
                                                offset_4 = offset_5


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

                                        if not (column_2 == indent_column_2[0] == 0):
                                            offset_3 = -1
                                            break
                                        # print('start')
                                        for indent, dedent in prefix_0:
                                            # print(indent)
                                            _children, _prefix = [], []
                                            offset_4 = offset_3
                                            offset_4, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = indent(buf, offset_4, buf_eof, column_2, indent_column_2, _prefix, _children, partial_tab_offset_2, partial_tab_width_2)
                                            if _prefix or _children:
                                               raise Exception('bar')
                                            if offset_4 == -1:
                                                if dedent is None:
                                                    offset_3 = -1
                                                    break
                                                _children, _prefix = [], []
                                                offset_4 = offset_3
                                                offset_4, _column, _indent_column, _partial_tab_offset, _partial_tab_width = dedent(buf, offset_4, buf_eof, column_2, indent_column_2, _prefix, _children, partial_tab_offset_2, partial_tab_width_2)
                                                if offset_4 != -1:
                                                    offset_3 = -1
                                                    break
                                                else:
                                                    offset_4 = offset_3
                                            offset_3 = offset_4
                                            indent_column_2 = (column_2, indent_column_2)
                                        if offset_3 == -1:
                                            break

                                        while True: # start reject
                                            children_4 = []
                                            offset_4 = offset_3 + 0
                                            column_3 = column_2
                                            indent_column_3 = indent_column_2
                                            partial_tab_offset_3 = partial_tab_offset_2
                                            partial_tab_width_3 = partial_tab_width_2
                                            while True: # start choice
                                                offset_5 = offset_4
                                                column_4 = column_3
                                                indent_column_4 = indent_column_3
                                                partial_tab_offset_4 = partial_tab_offset_3
                                                partial_tab_width_4 = partial_tab_width_3
                                                children_5 = [] if children_4 is not None else None
                                                while True: # case
                                                    offset_5, column_4, indent_column_4, partial_tab_offset_4, partial_tab_width_4 = self.parse_thematic_break(buf, offset_5, buf_eof, column_4, indent_column_4, prefix_0, children_5, partial_tab_offset_4, partial_tab_width_4)
                                                    if offset_5 == -1: break



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
                                                    offset_5, column_4, indent_column_4, partial_tab_offset_4, partial_tab_width_4 = self.parse_atx_heading(buf, offset_5, buf_eof, column_4, indent_column_4, prefix_0, children_5, partial_tab_offset_4, partial_tab_width_4)
                                                    if offset_5 == -1: break



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
                                                    offset_5, column_4, indent_column_4, partial_tab_offset_4, partial_tab_width_4 = self.parse_start_fenced_block(buf, offset_5, buf_eof, column_4, indent_column_4, prefix_0, children_5, partial_tab_offset_4, partial_tab_width_4)
                                                    if offset_5 == -1: break



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
                                                    offset_5, column_4, indent_column_4, partial_tab_offset_4, partial_tab_width_4 = self.parse_start_blockquote(buf, offset_5, buf_eof, column_4, indent_column_4, prefix_0, children_5, partial_tab_offset_4, partial_tab_width_4)
                                                    if offset_5 == -1: break



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
                                                    count_1 = 0
                                                    while offset_5 < buf_eof and count_1 < 3:
                                                        codepoint = buf[offset_5]
                                                        if codepoint in ' \t':
                                                            if codepoint == '\t':
                                                                if offset_5 == partial_tab_offset_4 and partial_tab_width_4 > 0:
                                                                    width = partial_tab_width_4
                                                                else:
                                                                    width  = (self.tabstop-(column_4%self.tabstop))
                                                                if count_1 + width > 3:
                                                                    new_width = 3 - count_1
                                                                    count_1 += new_width
                                                                    column_4 += new_width
                                                                    partial_tab_offset_4 = offset_5
                                                                    partial_tab_width_4 = width - new_width
                                                                    break
                                                                count_1 += width
                                                                column_4 += width
                                                                offset_5 += 1
                                                            else:
                                                                count_1 += 1
                                                                column_4 += 1
                                                                offset_5 += 1
                                                        else:
                                                            break

                                                    while True: # start choice
                                                        offset_6 = offset_5
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_6 = [] if children_5 is not None else None
                                                        while True: # case
                                                            if offset_6 == buf_eof:
                                                                offset_6 = -1
                                                                break

                                                            codepoint = ord(buf[offset_6])

                                                            if codepoint == 45:
                                                                offset_6 += 1
                                                                column_5 += 1
                                                            elif codepoint == 42:
                                                                offset_6 += 1
                                                                column_5 += 1
                                                            elif codepoint == 43:
                                                                offset_6 += 1
                                                                column_5 += 1
                                                            else:
                                                                offset_6 = -1
                                                                break


                                                            break
                                                        if offset_6 != -1:
                                                            offset_5 = offset_6
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_6 is not None and children_6 is not None:
                                                                children_5.extend(children_6)
                                                            break
                                                        # end case
                                                        offset_6 = offset_5
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_6 = [] if children_5 is not None else None
                                                        while True: # case
                                                            if buf[offset_6:offset_6+1] == '1':
                                                                offset_6 += 1
                                                                column_5 += 1
                                                            else:
                                                                offset_6 = -1
                                                                break

                                                            if offset_6 == buf_eof:
                                                                offset_6 = -1
                                                                break

                                                            codepoint = ord(buf[offset_6])

                                                            if codepoint == 46:
                                                                offset_6 += 1
                                                                column_5 += 1
                                                            elif codepoint == 41:
                                                                offset_6 += 1
                                                                column_5 += 1
                                                            else:
                                                                offset_6 = -1
                                                                break


                                                            break
                                                        if offset_6 != -1:
                                                            offset_5 = offset_6
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_6 is not None and children_6 is not None:
                                                                children_5.extend(children_6)
                                                            break
                                                        # end case
                                                        offset_5 = -1 # no more choices
                                                        break # end choice
                                                    if offset_5 == -1:
                                                        break

                                                    count_1 = 0
                                                    while offset_5 < buf_eof:
                                                        codepoint = buf[offset_5]
                                                        if codepoint in ' \t':
                                                            if codepoint == '\t':
                                                                if offset_5 == partial_tab_offset_4 and partial_tab_width_4 > 0:
                                                                    width = partial_tab_width_4
                                                                else:
                                                                    width  = (self.tabstop-(column_4%self.tabstop))
                                                                count_1 += width
                                                                column_4 += width
                                                                offset_5 += 1
                                                            else:
                                                                count_1 += 1
                                                                column_4 += 1
                                                                offset_5 += 1
                                                        else:
                                                            break
                                                    if count_1 < 1:
                                                        offset_5 = -1
                                                        break

                                                    while True: # start reject
                                                        children_6 = []
                                                        offset_6 = offset_5 + 0
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        count_1 = 0
                                                        while offset_6 < buf_eof:
                                                            codepoint = buf[offset_6]
                                                            if codepoint in ' \t':
                                                                if codepoint == '\t':
                                                                    if offset_6 == partial_tab_offset_5 and partial_tab_width_5 > 0:
                                                                        width = partial_tab_width_5
                                                                    else:
                                                                        width  = (self.tabstop-(column_5%self.tabstop))
                                                                    count_1 += width
                                                                    column_5 += width
                                                                    offset_6 += 1
                                                                else:
                                                                    count_1 += 1
                                                                    column_5 += 1
                                                                    offset_6 += 1
                                                            else:
                                                                break

                                                        if offset_6 < buf_eof:
                                                            codepoint = buf[offset_6]
                                                            if codepoint in '\n':
                                                                offset_6 +=1
                                                                column_5 = 0
                                                                indent_column_5 = (0, None)
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
                                        if offset_4 != -1:
                                            offset_3 = -1
                                            break

                                        count_1 = 0
                                        while offset_3 < buf_eof:
                                            codepoint = buf[offset_3]
                                            if codepoint in ' \t':
                                                if codepoint == '\t':
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

                                        while True: # start reject
                                            children_4 = []
                                            offset_4 = offset_3 + 0
                                            column_3 = column_2
                                            indent_column_3 = indent_column_2
                                            partial_tab_offset_3 = partial_tab_offset_2
                                            partial_tab_width_3 = partial_tab_width_2
                                            if offset_4 < buf_eof:
                                                codepoint = buf[offset_4]
                                                if codepoint in '\n':
                                                    offset_4 +=1
                                                    column_3 = 0
                                                    indent_column_3 = (0, None)
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
                                        offset_4 = offset_3
                                        children_4 = []
                                        while True: # start capture
                                            count_1 = 0
                                            while offset_4 < buf_eof:
                                                codepoint = buf[offset_4]
                                                if codepoint in ' \t':
                                                    if codepoint == '\t':
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
                                        value_2 = self.Node('whitespace', offset_3, offset_4, children_4, None)
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

                                offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_inline_element(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
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
                    prefix_0.pop()
                    if indent_column_0 != (0, None): indent_column_0 = indent_column_0[1]
                    if offset_1 == -1: break

                    while True: # start choice
                        offset_2 = offset_1
                        column_1 = column_0
                        indent_column_1 = indent_column_0
                        partial_tab_offset_1 = partial_tab_offset_0
                        partial_tab_width_1 = partial_tab_width_0
                        children_2 = [] if children_1 is not None else None
                        while True: # case
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

                            count_0 = 0
                            while offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
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

                            if offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in '\n':
                                    offset_2 +=1
                                    column_1 = 0
                                    indent_column_1 = (0, None)
                                else:
                                    offset_2 = -1
                                    break
                            else:
                                offset_2 = -1
                                break

                            if not (column_1 == indent_column_1[0] == 0):
                                offset_2 = -1
                                break
                            # print('start')
                            for indent, dedent in prefix_0:
                                # print(indent)
                                _children, _prefix = [], []
                                offset_3 = offset_2
                                offset_3, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = indent(buf, offset_3, buf_eof, column_1, indent_column_1, _prefix, _children, partial_tab_offset_1, partial_tab_width_1)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_3 == -1:
                                    offset_2 = -1
                                    break
                                offset_2 = offset_3
                                indent_column_1 = (column_1, indent_column_1)
                            if offset_2 == -1:
                                break

                            offset_2, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_setext_heading_line(buf, offset_2, buf_eof, column_1, indent_column_1, prefix_0, children_2, partial_tab_offset_1, partial_tab_width_1)
                            if offset_2 == -1: break


                            children_2.append(self.Node('value', offset_2, offset_2, (), 'setext'))


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
                                    while True: # start choice
                                        offset_4 = offset_3
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_4 = [] if children_3 is not None else None
                                        while True: # case
                                            while True: # start choice
                                                offset_5 = offset_4
                                                column_4 = column_3
                                                indent_column_4 = indent_column_3
                                                partial_tab_offset_4 = partial_tab_offset_3
                                                partial_tab_width_4 = partial_tab_width_3
                                                children_5 = [] if children_4 is not None else None
                                                while True: # case
                                                    while True: # start choice
                                                        offset_6 = offset_5
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_6 = [] if children_5 is not None else None
                                                        while True: # case
                                                            count_1 = 0
                                                            while offset_6 < buf_eof:
                                                                codepoint = buf[offset_6]
                                                                if codepoint in ' \t':
                                                                    if codepoint == '\t':
                                                                        if offset_6 == partial_tab_offset_5 and partial_tab_width_5 > 0:
                                                                            width = partial_tab_width_5
                                                                        else:
                                                                            width  = (self.tabstop-(column_5%self.tabstop))
                                                                        count_1 += width
                                                                        column_5 += width
                                                                        offset_6 += 1
                                                                    else:
                                                                        count_1 += 1
                                                                        column_5 += 1
                                                                        offset_6 += 1
                                                                else:
                                                                    break
                                                            if count_1 < 2:
                                                                offset_6 = -1
                                                                break


                                                            break
                                                        if offset_6 != -1:
                                                            offset_5 = offset_6
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
                                                            if children_6 is not None and children_6 is not None:
                                                                children_5.extend(children_6)
                                                            break
                                                        # end case
                                                        offset_6 = offset_5
                                                        column_5 = column_4
                                                        indent_column_5 = indent_column_4
                                                        partial_tab_offset_5 = partial_tab_offset_4
                                                        partial_tab_width_5 = partial_tab_width_4
                                                        children_6 = [] if children_5 is not None else None
                                                        while True: # case
                                                            if buf[offset_6:offset_6+1] == '\\':
                                                                offset_6 += 1
                                                                column_5 += 1
                                                            else:
                                                                offset_6 = -1
                                                                break


                                                            break
                                                        if offset_6 != -1:
                                                            offset_5 = offset_6
                                                            column_4 = column_5
                                                            indent_column_4 = indent_column_5
                                                            partial_tab_offset_4 = partial_tab_offset_5
                                                            partial_tab_width_4 = partial_tab_width_5
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
                                                            codepoint = buf[offset_6]
                                                            if codepoint in '\n':
                                                                offset_6 +=1
                                                                column_4 = 0
                                                                indent_column_4 = (0, None)
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
                                                    value_3 = self.Node('hardbreak', offset_5, offset_6, children_6, None)
                                                    children_5.append(value_3)
                                                    offset_5 = offset_6


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
                                                    count_1 = 0
                                                    while offset_5 < buf_eof:
                                                        codepoint = buf[offset_5]
                                                        if codepoint in ' \t':
                                                            if codepoint == '\t':
                                                                if offset_5 == partial_tab_offset_4 and partial_tab_width_4 > 0:
                                                                    width = partial_tab_width_4
                                                                else:
                                                                    width  = (self.tabstop-(column_4%self.tabstop))
                                                                count_1 += width
                                                                column_4 += width
                                                                offset_5 += 1
                                                            else:
                                                                count_1 += 1
                                                                column_4 += 1
                                                                offset_5 += 1
                                                        else:
                                                            break

                                                    offset_6 = offset_5
                                                    children_6 = []
                                                    while True: # start capture
                                                        if offset_6 < buf_eof:
                                                            codepoint = buf[offset_6]
                                                            if codepoint in '\n':
                                                                offset_6 +=1
                                                                column_4 = 0
                                                                indent_column_4 = (0, None)
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
                                                    value_3 = self.Node('softbreak', offset_5, offset_6, children_6, None)
                                                    children_5.append(value_3)
                                                    offset_5 = offset_6


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

                                            if not (column_3 == indent_column_3[0] == 0):
                                                offset_4 = -1
                                                break
                                            # print('start')
                                            for indent, dedent in prefix_0:
                                                # print(indent)
                                                _children, _prefix = [], []
                                                offset_5 = offset_4
                                                offset_5, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_5, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                                if _prefix or _children:
                                                   raise Exception('bar')
                                                if offset_5 == -1:
                                                    if dedent is None:
                                                        offset_4 = -1
                                                        break
                                                    _children, _prefix = [], []
                                                    offset_5 = offset_4
                                                    offset_5, _column, _indent_column, _partial_tab_offset, _partial_tab_width = dedent(buf, offset_5, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                                    if offset_5 != -1:
                                                        offset_4 = -1
                                                        break
                                                    else:
                                                        offset_5 = offset_4
                                                offset_4 = offset_5
                                                indent_column_3 = (column_3, indent_column_3)
                                            if offset_4 == -1:
                                                break

                                            while True: # start reject
                                                children_5 = []
                                                offset_5 = offset_4 + 0
                                                column_4 = column_3
                                                indent_column_4 = indent_column_3
                                                partial_tab_offset_4 = partial_tab_offset_3
                                                partial_tab_width_4 = partial_tab_width_3
                                                while True: # start choice
                                                    offset_6 = offset_5
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    children_6 = [] if children_5 is not None else None
                                                    while True: # case
                                                        offset_6, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_thematic_break(buf, offset_6, buf_eof, column_5, indent_column_5, prefix_0, children_6, partial_tab_offset_5, partial_tab_width_5)
                                                        if offset_6 == -1: break



                                                        break
                                                    if offset_6 != -1:
                                                        offset_5 = offset_6
                                                        column_4 = column_5
                                                        indent_column_4 = indent_column_5
                                                        partial_tab_offset_4 = partial_tab_offset_5
                                                        partial_tab_width_4 = partial_tab_width_5
                                                        if children_6 is not None and children_6 is not None:
                                                            children_5.extend(children_6)
                                                        break
                                                    # end case
                                                    offset_6 = offset_5
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    children_6 = [] if children_5 is not None else None
                                                    while True: # case
                                                        offset_6, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_atx_heading(buf, offset_6, buf_eof, column_5, indent_column_5, prefix_0, children_6, partial_tab_offset_5, partial_tab_width_5)
                                                        if offset_6 == -1: break



                                                        break
                                                    if offset_6 != -1:
                                                        offset_5 = offset_6
                                                        column_4 = column_5
                                                        indent_column_4 = indent_column_5
                                                        partial_tab_offset_4 = partial_tab_offset_5
                                                        partial_tab_width_4 = partial_tab_width_5
                                                        if children_6 is not None and children_6 is not None:
                                                            children_5.extend(children_6)
                                                        break
                                                    # end case
                                                    offset_6 = offset_5
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    children_6 = [] if children_5 is not None else None
                                                    while True: # case
                                                        offset_6, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_start_fenced_block(buf, offset_6, buf_eof, column_5, indent_column_5, prefix_0, children_6, partial_tab_offset_5, partial_tab_width_5)
                                                        if offset_6 == -1: break



                                                        break
                                                    if offset_6 != -1:
                                                        offset_5 = offset_6
                                                        column_4 = column_5
                                                        indent_column_4 = indent_column_5
                                                        partial_tab_offset_4 = partial_tab_offset_5
                                                        partial_tab_width_4 = partial_tab_width_5
                                                        if children_6 is not None and children_6 is not None:
                                                            children_5.extend(children_6)
                                                        break
                                                    # end case
                                                    offset_6 = offset_5
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    children_6 = [] if children_5 is not None else None
                                                    while True: # case
                                                        offset_6, column_5, indent_column_5, partial_tab_offset_5, partial_tab_width_5 = self.parse_start_blockquote(buf, offset_6, buf_eof, column_5, indent_column_5, prefix_0, children_6, partial_tab_offset_5, partial_tab_width_5)
                                                        if offset_6 == -1: break



                                                        break
                                                    if offset_6 != -1:
                                                        offset_5 = offset_6
                                                        column_4 = column_5
                                                        indent_column_4 = indent_column_5
                                                        partial_tab_offset_4 = partial_tab_offset_5
                                                        partial_tab_width_4 = partial_tab_width_5
                                                        if children_6 is not None and children_6 is not None:
                                                            children_5.extend(children_6)
                                                        break
                                                    # end case
                                                    offset_6 = offset_5
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    children_6 = [] if children_5 is not None else None
                                                    while True: # case
                                                        count_1 = 0
                                                        while offset_6 < buf_eof and count_1 < 3:
                                                            codepoint = buf[offset_6]
                                                            if codepoint in ' \t':
                                                                if codepoint == '\t':
                                                                    if offset_6 == partial_tab_offset_5 and partial_tab_width_5 > 0:
                                                                        width = partial_tab_width_5
                                                                    else:
                                                                        width  = (self.tabstop-(column_5%self.tabstop))
                                                                    if count_1 + width > 3:
                                                                        new_width = 3 - count_1
                                                                        count_1 += new_width
                                                                        column_5 += new_width
                                                                        partial_tab_offset_5 = offset_6
                                                                        partial_tab_width_5 = width - new_width
                                                                        break
                                                                    count_1 += width
                                                                    column_5 += width
                                                                    offset_6 += 1
                                                                else:
                                                                    count_1 += 1
                                                                    column_5 += 1
                                                                    offset_6 += 1
                                                            else:
                                                                break

                                                        while True: # start choice
                                                            offset_7 = offset_6
                                                            column_6 = column_5
                                                            indent_column_6 = indent_column_5
                                                            partial_tab_offset_6 = partial_tab_offset_5
                                                            partial_tab_width_6 = partial_tab_width_5
                                                            children_7 = [] if children_6 is not None else None
                                                            while True: # case
                                                                if offset_7 == buf_eof:
                                                                    offset_7 = -1
                                                                    break

                                                                codepoint = ord(buf[offset_7])

                                                                if codepoint == 45:
                                                                    offset_7 += 1
                                                                    column_6 += 1
                                                                elif codepoint == 42:
                                                                    offset_7 += 1
                                                                    column_6 += 1
                                                                elif codepoint == 43:
                                                                    offset_7 += 1
                                                                    column_6 += 1
                                                                else:
                                                                    offset_7 = -1
                                                                    break


                                                                break
                                                            if offset_7 != -1:
                                                                offset_6 = offset_7
                                                                column_5 = column_6
                                                                indent_column_5 = indent_column_6
                                                                partial_tab_offset_5 = partial_tab_offset_6
                                                                partial_tab_width_5 = partial_tab_width_6
                                                                if children_7 is not None and children_7 is not None:
                                                                    children_6.extend(children_7)
                                                                break
                                                            # end case
                                                            offset_7 = offset_6
                                                            column_6 = column_5
                                                            indent_column_6 = indent_column_5
                                                            partial_tab_offset_6 = partial_tab_offset_5
                                                            partial_tab_width_6 = partial_tab_width_5
                                                            children_7 = [] if children_6 is not None else None
                                                            while True: # case
                                                                if buf[offset_7:offset_7+1] == '1':
                                                                    offset_7 += 1
                                                                    column_6 += 1
                                                                else:
                                                                    offset_7 = -1
                                                                    break

                                                                if offset_7 == buf_eof:
                                                                    offset_7 = -1
                                                                    break

                                                                codepoint = ord(buf[offset_7])

                                                                if codepoint == 46:
                                                                    offset_7 += 1
                                                                    column_6 += 1
                                                                elif codepoint == 41:
                                                                    offset_7 += 1
                                                                    column_6 += 1
                                                                else:
                                                                    offset_7 = -1
                                                                    break


                                                                break
                                                            if offset_7 != -1:
                                                                offset_6 = offset_7
                                                                column_5 = column_6
                                                                indent_column_5 = indent_column_6
                                                                partial_tab_offset_5 = partial_tab_offset_6
                                                                partial_tab_width_5 = partial_tab_width_6
                                                                if children_7 is not None and children_7 is not None:
                                                                    children_6.extend(children_7)
                                                                break
                                                            # end case
                                                            offset_6 = -1 # no more choices
                                                            break # end choice
                                                        if offset_6 == -1:
                                                            break

                                                        count_1 = 0
                                                        while offset_6 < buf_eof:
                                                            codepoint = buf[offset_6]
                                                            if codepoint in ' \t':
                                                                if codepoint == '\t':
                                                                    if offset_6 == partial_tab_offset_5 and partial_tab_width_5 > 0:
                                                                        width = partial_tab_width_5
                                                                    else:
                                                                        width  = (self.tabstop-(column_5%self.tabstop))
                                                                    count_1 += width
                                                                    column_5 += width
                                                                    offset_6 += 1
                                                                else:
                                                                    count_1 += 1
                                                                    column_5 += 1
                                                                    offset_6 += 1
                                                            else:
                                                                break
                                                        if count_1 < 1:
                                                            offset_6 = -1
                                                            break

                                                        while True: # start reject
                                                            children_7 = []
                                                            offset_7 = offset_6 + 0
                                                            column_6 = column_5
                                                            indent_column_6 = indent_column_5
                                                            partial_tab_offset_6 = partial_tab_offset_5
                                                            partial_tab_width_6 = partial_tab_width_5
                                                            count_1 = 0
                                                            while offset_7 < buf_eof:
                                                                codepoint = buf[offset_7]
                                                                if codepoint in ' \t':
                                                                    if codepoint == '\t':
                                                                        if offset_7 == partial_tab_offset_6 and partial_tab_width_6 > 0:
                                                                            width = partial_tab_width_6
                                                                        else:
                                                                            width  = (self.tabstop-(column_6%self.tabstop))
                                                                        count_1 += width
                                                                        column_6 += width
                                                                        offset_7 += 1
                                                                    else:
                                                                        count_1 += 1
                                                                        column_6 += 1
                                                                        offset_7 += 1
                                                                else:
                                                                    break

                                                            if offset_7 < buf_eof:
                                                                codepoint = buf[offset_7]
                                                                if codepoint in '\n':
                                                                    offset_7 +=1
                                                                    column_6 = 0
                                                                    indent_column_6 = (0, None)
                                                                else:
                                                                    offset_7 = -1
                                                                    break

                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = -1
                                                            break


                                                        break
                                                    if offset_6 != -1:
                                                        offset_5 = offset_6
                                                        column_4 = column_5
                                                        indent_column_4 = indent_column_5
                                                        partial_tab_offset_4 = partial_tab_offset_5
                                                        partial_tab_width_4 = partial_tab_width_5
                                                        if children_6 is not None and children_6 is not None:
                                                            children_5.extend(children_6)
                                                        break
                                                    # end case
                                                    offset_5 = -1 # no more choices
                                                    break # end choice
                                                if offset_5 == -1:
                                                    break

                                                break
                                            if offset_5 != -1:
                                                offset_4 = -1
                                                break

                                            count_1 = 0
                                            while offset_4 < buf_eof:
                                                codepoint = buf[offset_4]
                                                if codepoint in ' \t':
                                                    if codepoint == '\t':
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

                                            while True: # start reject
                                                children_5 = []
                                                offset_5 = offset_4 + 0
                                                column_4 = column_3
                                                indent_column_4 = indent_column_3
                                                partial_tab_offset_4 = partial_tab_offset_3
                                                partial_tab_width_4 = partial_tab_width_3
                                                if offset_5 < buf_eof:
                                                    codepoint = buf[offset_5]
                                                    if codepoint in '\n':
                                                        offset_5 +=1
                                                        column_4 = 0
                                                        indent_column_4 = (0, None)
                                                    else:
                                                        offset_5 = -1
                                                        break
                                                else:
                                                    offset_5 = -1
                                                    break

                                                break
                                            if offset_5 != -1:
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
                                            offset_5 = offset_4
                                            children_5 = []
                                            while True: # start capture
                                                count_1 = 0
                                                while offset_5 < buf_eof:
                                                    codepoint = buf[offset_5]
                                                    if codepoint in ' \t':
                                                        if codepoint == '\t':
                                                            if offset_5 == partial_tab_offset_3 and partial_tab_width_3 > 0:
                                                                width = partial_tab_width_3
                                                            else:
                                                                width  = (self.tabstop-(column_3%self.tabstop))
                                                            count_1 += width
                                                            column_3 += width
                                                            offset_5 += 1
                                                        else:
                                                            count_1 += 1
                                                            column_3 += 1
                                                            offset_5 += 1
                                                    else:
                                                        break

                                                break
                                            if offset_5 == -1:
                                                offset_4 = -1
                                                break
                                            value_3 = self.Node('whitespace', offset_4, offset_5, children_5, None)
                                            children_4.append(value_3)
                                            offset_4 = offset_5


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
                            while offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in ' \t':
                                    if codepoint == '\t':
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

                            if offset_2 < buf_eof:
                                codepoint = buf[offset_2]
                                if codepoint in '\n':
                                    offset_2 +=1
                                    column_1 = 0
                                    indent_column_1 = (0, None)
                                else:
                                    offset_2 = -1
                                    break

                            children_2.append(self.Node('value', offset_2, offset_2, (), 'para'))


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
                value_4 = self.Node('para', offset_0, offset_1, children_1, None)
                children_0.append(value_4)
                offset_0 = offset_1


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
                        while True: # start reject
                            children_2 = []
                            offset_2 = offset_1 + 0
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            offset_2, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_left_flank(buf, offset_2, buf_eof, column_2, indent_column_2, prefix_0, children_2, partial_tab_offset_2, partial_tab_width_2)
                            if offset_2 == -1: break


                            break
                        if offset_2 != -1:
                            offset_1 = -1
                            break

                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_right_flank(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                            offset_2 = offset_1 + 0
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            offset_2, column_2, indent_column_2, partial_tab_offset_2, partial_tab_width_2 = self.parse_right_flank(buf, offset_2, buf_eof, column_2, indent_column_2, prefix_0, children_2, partial_tab_offset_2, partial_tab_width_2)
                            if offset_2 == -1: break


                            break
                        if offset_2 != -1:
                            offset_1 = -1
                            break

                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_left_flank(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_html_entity(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                        offset_1, column_1, indent_column_1, partial_tab_offset_1, partial_tab_width_1 = self.parse_escaped_text(buf, offset_1, buf_eof, column_1, indent_column_1, prefix_0, children_1, partial_tab_offset_1, partial_tab_width_1)
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
                        offset_2 = offset_1
                        children_2 = []
                        while True: # start capture
                            if offset_2 == buf_eof:
                                offset_2 = -1
                                break

                            codepoint = ord(buf[offset_2])

                            if codepoint == 32:
                                offset_2 = -1
                                break
                            elif codepoint == 10:
                                offset_2 = -1
                                break
                            elif codepoint == 92:
                                offset_2 = -1
                                break
                            else:
                                offset_2 += 1
                                column_1 += 1

                            count_0 = 0
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

                                    codepoint = ord(buf[offset_3])

                                    if codepoint == 32:
                                        offset_3 = -1
                                        break
                                    elif codepoint == 10:
                                        offset_3 = -1
                                        break
                                    elif codepoint == 92:
                                        offset_3 = -1
                                        break
                                    elif codepoint == 60:
                                        offset_3 = -1
                                        break
                                    elif codepoint == 96:
                                        offset_3 = -1
                                        break
                                    elif codepoint == 42:
                                        offset_3 = -1
                                        break
                                    elif codepoint == 95:
                                        offset_3 = -1
                                        break
                                    elif codepoint == 38:
                                        offset_3 = -1
                                        break
                                    elif codepoint == 91:
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
                                count_0 += 1
                            if offset_2 == -1:
                                break

                            break
                        if offset_2 == -1:
                            offset_1 = -1
                            break
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
                    offset_0 = -1 # no more choices
                    break # end choice
                if offset_0 == -1:
                    break

                break
            return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

        def parse_escaped_text(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                if buf[offset_0:offset_0+1] == '\\':
                    offset_0 += 1
                    column_0 += 1
                else:
                    offset_0 = -1
                    break

                while True: # start reject
                    children_1 = []
                    offset_1 = offset_0 + 0
                    column_1 = column_0
                    indent_column_1 = indent_column_0
                    partial_tab_offset_1 = partial_tab_offset_0
                    partial_tab_width_1 = partial_tab_width_0
                    if offset_1 < buf_eof:
                        codepoint = buf[offset_1]
                        if codepoint in '\n':
                            offset_1 +=1
                            column_1 = 0
                            indent_column_1 = (0, None)
                        else:
                            offset_1 = -1
                            break
                    else:
                        offset_1 = -1
                        break

                    count_0 = 0
                    while offset_1 < buf_eof:
                        codepoint = buf[offset_1]
                        if codepoint in ' \t':
                            if codepoint == '\t':
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

                    if offset_1 == buf_eof:
                        offset_1 = -1
                        break

                    codepoint = ord(buf[offset_1])

                    if codepoint == 10:
                        offset_1 = -1
                        break
                    else:
                        offset_1 += 1
                        column_1 += 1

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

                            codepoint = ord(buf[offset_2])

                            if 33 <= codepoint <= 47:
                                offset_2 += 1
                                column_1 += 1
                            elif 58 <= codepoint <= 64:
                                offset_2 += 1
                                column_1 += 1
                            elif 91 <= codepoint <= 96:
                                offset_2 += 1
                                column_1 += 1
                            elif 123 <= codepoint <= 126:
                                offset_2 += 1
                                column_1 += 1
                            else:
                                offset_2 = -1
                                break

                            break
                        if offset_2 == -1:
                            offset_1 = -1
                            break
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

        def parse_html_entity(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
                if buf[offset_0:offset_0+1] == '&':
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
                        if buf[offset_1:offset_1+1] == '#':
                            offset_1 += 1
                            column_1 += 1
                        else:
                            offset_1 = -1
                            break

                        offset_2 = offset_1
                        children_2 = []
                        while True: # start capture
                            count_0 = 0
                            while count_0 < 7:
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

                                    codepoint = ord(buf[offset_3])

                                    if 48 <= codepoint <= 57:
                                        offset_3 += 1
                                        column_2 += 1
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
                                column_1 = column_2
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
                        value_0 = self.Node('dec_entity', offset_1, offset_2, children_2, None)
                        children_1.append(value_0)
                        offset_1 = offset_2

                        if buf[offset_1:offset_1+1] == ';':
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
                        if buf[offset_1:offset_1+1] == '#':
                            offset_1 += 1
                            column_1 += 1
                        else:
                            offset_1 = -1
                            break

                        if offset_1 == buf_eof:
                            offset_1 = -1
                            break

                        codepoint = ord(buf[offset_1])

                        if codepoint == 120:
                            offset_1 += 1
                            column_1 += 1
                        elif codepoint == 88:
                            offset_1 += 1
                            column_1 += 1
                        else:
                            offset_1 = -1
                            break

                        offset_2 = offset_1
                        children_2 = []
                        while True: # start capture
                            if offset_2 == buf_eof:
                                offset_2 = -1
                                break

                            codepoint = ord(buf[offset_2])

                            if 48 <= codepoint <= 57:
                                offset_2 += 1
                                column_1 += 1
                            elif 97 <= codepoint <= 102:
                                offset_2 += 1
                                column_1 += 1
                            elif 65 <= codepoint <= 70:
                                offset_2 += 1
                                column_1 += 1
                            else:
                                offset_2 = -1
                                break

                            count_0 = 0
                            while count_0 < 6:
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

                                    codepoint = ord(buf[offset_3])

                                    if 48 <= codepoint <= 57:
                                        offset_3 += 1
                                        column_2 += 1
                                    elif 97 <= codepoint <= 102:
                                        offset_3 += 1
                                        column_2 += 1
                                    elif 65 <= codepoint <= 70:
                                        offset_3 += 1
                                        column_2 += 1
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
                        value_1 = self.Node('hex_entity', offset_1, offset_2, children_2, None)
                        children_1.append(value_1)
                        offset_1 = offset_2

                        if buf[offset_1:offset_1+1] == ';':
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
                        offset_2 = offset_1
                        children_2 = []
                        while True: # start capture
                            if offset_2 == buf_eof:
                                offset_2 = -1
                                break

                            codepoint = ord(buf[offset_2])

                            if 97 <= codepoint <= 122:
                                offset_2 += 1
                                column_1 += 1
                            elif 65 <= codepoint <= 90:
                                offset_2 += 1
                                column_1 += 1
                            else:
                                offset_2 = -1
                                break

                            count_0 = 0
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

                                    codepoint = ord(buf[offset_3])

                                    if 48 <= codepoint <= 57:
                                        offset_3 += 1
                                        column_2 += 1
                                    elif 97 <= codepoint <= 122:
                                        offset_3 += 1
                                        column_2 += 1
                                    elif 65 <= codepoint <= 90:
                                        offset_3 += 1
                                        column_2 += 1
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
                                column_1 = column_2
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
                        value_2 = self.Node('named_entity', offset_1, offset_2, children_2, None)
                        children_1.append(value_2)
                        offset_1 = offset_2

                        if buf[offset_1:offset_1+1] == ';':
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

        def parse_left_flank(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
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
                            while True: # start lookahed
                                children_3 = []
                                offset_3 = offset_2 + -1
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = ord(buf[offset_3])

                                if unicodedata.category(chr(codepoint)) == 'Zs':
                                    offset_3 += 1
                                    column_2 += 1
                                elif unicodedata.category(chr(codepoint)) in ('Zl', 'Zp', 'Cc'):
                                    offset_3 += 1
                                    column_2 += 1
                                elif unicodedata.category(chr(codepoint)).startswith('P'):
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                break
                            if offset_3 == -1:
                                offset_2 = -1
                                break

                            offset_3 = offset_2
                            column_2 = column_1
                            while True: # start count
                                offset_4 = offset_3
                                while True: # start backref
                                    if offset_4 == buf_eof:
                                        offset_4 = -1
                                        break

                                    codepoint = ord(buf[offset_4])

                                    if codepoint == 95:
                                        offset_4 += 1
                                        column_2 += 1
                                    elif codepoint == 42:
                                        offset_4 += 1
                                        column_2 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                value_0 = buf[offset_3:offset_4]
                                offset_3 = offset_4

                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_2 = indent_column_1
                                    partial_tab_offset_2 = partial_tab_offset_1
                                    partial_tab_width_2 = partial_tab_width_1
                                    children_3 = [] if children_2 is not None else None
                                    while True:
                                        if buf[offset_4:offset_4+len(value_0)] == value_0:
                                            offset_4 += len(value_0)
                                            column_3 += len(value_0)
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_3 is not None and children_3 is not None:
                                        children_2.extend(children_3)
                                    offset_3 = offset_4
                                    column_2 = column_3
                                    indent_column_1 = indent_column_2
                                    partial_tab_offset_1 = partial_tab_offset_2
                                    partial_tab_width_1 = partial_tab_width_2
                                    count_0 += 1
                                if offset_3 == -1:
                                    break

                                break
                            if offset_3 == -1:
                                offset_2 = -1; break
                            value_1 = column_2 - column_1
                            offset_2 = offset_3
                            column_1 = column_2

                            while True: # start reject
                                children_3 = []
                                offset_3 = offset_2 + 0
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = ord(buf[offset_3])

                                if unicodedata.category(chr(codepoint)) == 'Zs':
                                    offset_3 += 1
                                    column_2 += 1
                                elif unicodedata.category(chr(codepoint)) in ('Zl', 'Zp', 'Cc'):
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                break
                            if offset_3 != -1:
                                offset_2 = -1
                                break

                            children_2.append(self.Node('value', offset_2, offset_2, (), 'left'))

                            children_2.append(self.Node('value', offset_2, offset_2, (), value_0))

                            children_2.append(self.Node('value', offset_2, offset_2, (), value_1))


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
                            while True: # start reject
                                children_3 = []
                                offset_3 = offset_2 + -1
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = ord(buf[offset_3])

                                if unicodedata.category(chr(codepoint)).startswith('P'):
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                break
                            if offset_3 != -1:
                                offset_2 = -1
                                break

                            offset_3 = offset_2
                            column_2 = column_1
                            while True: # start count
                                offset_4 = offset_3
                                while True: # start backref
                                    if offset_4 == buf_eof:
                                        offset_4 = -1
                                        break

                                    codepoint = ord(buf[offset_4])

                                    if codepoint == 95:
                                        offset_4 += 1
                                        column_2 += 1
                                    elif codepoint == 42:
                                        offset_4 += 1
                                        column_2 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                value_2 = buf[offset_3:offset_4]
                                offset_3 = offset_4

                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_2 = indent_column_1
                                    partial_tab_offset_2 = partial_tab_offset_1
                                    partial_tab_width_2 = partial_tab_width_1
                                    children_3 = [] if children_2 is not None else None
                                    while True:
                                        if buf[offset_4:offset_4+len(value_2)] == value_2:
                                            offset_4 += len(value_2)
                                            column_3 += len(value_2)
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_3 is not None and children_3 is not None:
                                        children_2.extend(children_3)
                                    offset_3 = offset_4
                                    column_2 = column_3
                                    indent_column_1 = indent_column_2
                                    partial_tab_offset_1 = partial_tab_offset_2
                                    partial_tab_width_1 = partial_tab_width_2
                                    count_0 += 1
                                if offset_3 == -1:
                                    break

                                break
                            if offset_3 == -1:
                                offset_2 = -1; break
                            value_3 = column_2 - column_1
                            offset_2 = offset_3
                            column_1 = column_2

                            while True: # start reject
                                children_3 = []
                                offset_3 = offset_2 + 0
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = ord(buf[offset_3])

                                if unicodedata.category(chr(codepoint)) == 'Zs':
                                    offset_3 += 1
                                    column_2 += 1
                                elif unicodedata.category(chr(codepoint)) in ('Zl', 'Zp', 'Cc'):
                                    offset_3 += 1
                                    column_2 += 1
                                elif unicodedata.category(chr(codepoint)).startswith('P'):
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                break
                            if offset_3 != -1:
                                offset_2 = -1
                                break

                            children_2.append(self.Node('value', offset_2, offset_2, (), 'left'))

                            children_2.append(self.Node('value', offset_2, offset_2, (), value_2))

                            children_2.append(self.Node('value', offset_2, offset_2, (), value_3))


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
                value_4 = self.Node('left_flank', offset_0, offset_1, children_1, None)
                children_0.append(value_4)
                offset_0 = offset_1

                break
            return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

        def parse_right_flank(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
            while True: # note: return at end of loop
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
                            while True: # start reject
                                children_3 = []
                                offset_3 = offset_2 + -1
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = ord(buf[offset_3])

                                if unicodedata.category(chr(codepoint)) == 'Zs':
                                    offset_3 += 1
                                    column_2 += 1
                                elif unicodedata.category(chr(codepoint)) in ('Zl', 'Zp', 'Cc'):
                                    offset_3 += 1
                                    column_2 += 1
                                elif unicodedata.category(chr(codepoint)).startswith('P'):
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                break
                            if offset_3 != -1:
                                offset_2 = -1
                                break

                            offset_3 = offset_2
                            column_2 = column_1
                            while True: # start count
                                offset_4 = offset_3
                                while True: # start backref
                                    if offset_4 == buf_eof:
                                        offset_4 = -1
                                        break

                                    codepoint = ord(buf[offset_4])

                                    if codepoint == 95:
                                        offset_4 += 1
                                        column_2 += 1
                                    elif codepoint == 42:
                                        offset_4 += 1
                                        column_2 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                value_0 = buf[offset_3:offset_4]
                                offset_3 = offset_4

                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_2 = indent_column_1
                                    partial_tab_offset_2 = partial_tab_offset_1
                                    partial_tab_width_2 = partial_tab_width_1
                                    children_3 = [] if children_2 is not None else None
                                    while True:
                                        if buf[offset_4:offset_4+len(value_0)] == value_0:
                                            offset_4 += len(value_0)
                                            column_3 += len(value_0)
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_3 is not None and children_3 is not None:
                                        children_2.extend(children_3)
                                    offset_3 = offset_4
                                    column_2 = column_3
                                    indent_column_1 = indent_column_2
                                    partial_tab_offset_1 = partial_tab_offset_2
                                    partial_tab_width_1 = partial_tab_width_2
                                    count_0 += 1
                                if offset_3 == -1:
                                    break

                                break
                            if offset_3 == -1:
                                offset_2 = -1; break
                            value_1 = column_2 - column_1
                            offset_2 = offset_3
                            column_1 = column_2

                            children_2.append(self.Node('value', offset_2, offset_2, (), 'right'))

                            children_2.append(self.Node('value', offset_2, offset_2, (), value_0))

                            children_2.append(self.Node('value', offset_2, offset_2, (), value_1))


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
                            while True: # start reject
                                children_3 = []
                                offset_3 = offset_2 + -1
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = ord(buf[offset_3])

                                if unicodedata.category(chr(codepoint)) == 'Zs':
                                    offset_3 += 1
                                    column_2 += 1
                                elif unicodedata.category(chr(codepoint)) in ('Zl', 'Zp', 'Cc'):
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                break
                            if offset_3 != -1:
                                offset_2 = -1
                                break

                            offset_3 = offset_2
                            column_2 = column_1
                            while True: # start count
                                offset_4 = offset_3
                                while True: # start backref
                                    if offset_4 == buf_eof:
                                        offset_4 = -1
                                        break

                                    codepoint = ord(buf[offset_4])

                                    if codepoint == 95:
                                        offset_4 += 1
                                        column_2 += 1
                                    elif codepoint == 42:
                                        offset_4 += 1
                                        column_2 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                value_2 = buf[offset_3:offset_4]
                                offset_3 = offset_4

                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    column_3 = column_2
                                    indent_column_2 = indent_column_1
                                    partial_tab_offset_2 = partial_tab_offset_1
                                    partial_tab_width_2 = partial_tab_width_1
                                    children_3 = [] if children_2 is not None else None
                                    while True:
                                        if buf[offset_4:offset_4+len(value_2)] == value_2:
                                            offset_4 += len(value_2)
                                            column_3 += len(value_2)
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_3 is not None and children_3 is not None:
                                        children_2.extend(children_3)
                                    offset_3 = offset_4
                                    column_2 = column_3
                                    indent_column_1 = indent_column_2
                                    partial_tab_offset_1 = partial_tab_offset_2
                                    partial_tab_width_1 = partial_tab_width_2
                                    count_0 += 1
                                if offset_3 == -1:
                                    break

                                break
                            if offset_3 == -1:
                                offset_2 = -1; break
                            value_3 = column_2 - column_1
                            offset_2 = offset_3
                            column_1 = column_2

                            while True: # start lookahed
                                children_3 = []
                                offset_3 = offset_2 + 0
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                codepoint = ord(buf[offset_3])

                                if unicodedata.category(chr(codepoint)) == 'Zs':
                                    offset_3 += 1
                                    column_2 += 1
                                elif unicodedata.category(chr(codepoint)) in ('Zl', 'Zp', 'Cc'):
                                    offset_3 += 1
                                    column_2 += 1
                                elif unicodedata.category(chr(codepoint)).startswith('P'):
                                    offset_3 += 1
                                    column_2 += 1
                                else:
                                    offset_3 = -1
                                    break

                                break
                            if offset_3 == -1:
                                offset_2 = -1
                                break

                            children_2.append(self.Node('value', offset_2, offset_2, (), 'right'))

                            children_2.append(self.Node('value', offset_2, offset_2, (), value_2))

                            children_2.append(self.Node('value', offset_2, offset_2, (), value_3))


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
                value_4 = self.Node('right_flank', offset_0, offset_1, children_1, None)
                children_0.append(value_4)
                offset_0 = offset_1

                break
            return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0

        def parse_code_span(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
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
                        column_2 = column_1
                        while True: # start count
                            count_0 = 0
                            while True:
                                offset_3 = offset_2
                                column_3 = column_2
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_2 = [] if children_1 is not None else None
                                while True:
                                    if buf[offset_3:offset_3+1] == '`':
                                        offset_3 += 1
                                        column_3 += 1
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
                            offset_1 = -1; break
                        value_0 = buf[offset_1:offset_2].count('`')
                        offset_1 = offset_2
                        column_1 = column_2

                        offset_2 = offset_1
                        children_2 = []
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
                                            offset_5 = offset_4
                                            children_5 = []
                                            while True: # start capture
                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                codepoint = ord(buf[offset_5])

                                                if codepoint == 10:
                                                    offset_5 = -1
                                                    break
                                                elif codepoint == 96:
                                                    offset_5 = -1
                                                    break
                                                else:
                                                    offset_5 += 1
                                                    column_3 += 1

                                                count_1 = 0
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

                                                        codepoint = ord(buf[offset_6])

                                                        if codepoint == 10:
                                                            offset_6 = -1
                                                            break
                                                        elif codepoint == 96:
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
                                                    count_1 += 1
                                                if offset_5 == -1:
                                                    break

                                                break
                                            if offset_5 == -1:
                                                offset_4 = -1
                                                break
                                            value_1 = self.Node('text', offset_4, offset_5, children_5, None)
                                            children_4.append(value_1)
                                            offset_4 = offset_5


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
                                            offset_5 = offset_4
                                            children_5 = []
                                            while True: # start capture
                                                if offset_5 < buf_eof:
                                                    codepoint = buf[offset_5]
                                                    if codepoint in '\n':
                                                        offset_5 +=1
                                                        column_3 = 0
                                                        indent_column_3 = (0, None)
                                                    else:
                                                        offset_5 = -1
                                                        break
                                                else:
                                                    offset_5 = -1
                                                    break

                                                break
                                            if offset_5 == -1:
                                                offset_4 = -1
                                                break
                                            value_2 = self.Node('text', offset_4, offset_5, children_5, None)
                                            children_4.append(value_2)
                                            offset_4 = offset_5

                                            if not (column_3 == indent_column_3[0] == 0):
                                                offset_4 = -1
                                                break
                                            # print('start')
                                            for indent, dedent in prefix_0:
                                                # print(indent)
                                                _children, _prefix = [], []
                                                offset_5 = offset_4
                                                offset_5, column_3, indent_column_3, partial_tab_offset_3, partial_tab_width_3 = indent(buf, offset_5, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                                if _prefix or _children:
                                                   raise Exception('bar')
                                                if offset_5 == -1:
                                                    if dedent is None:
                                                        offset_4 = -1
                                                        break
                                                    _children, _prefix = [], []
                                                    offset_5 = offset_4
                                                    offset_5, _column, _indent_column, _partial_tab_offset, _partial_tab_width = dedent(buf, offset_5, buf_eof, column_3, indent_column_3, _prefix, _children, partial_tab_offset_3, partial_tab_width_3)
                                                    if offset_5 != -1:
                                                        offset_4 = -1
                                                        break
                                                    else:
                                                        offset_5 = offset_4
                                                offset_4 = offset_5
                                                indent_column_3 = (column_3, indent_column_3)
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
                                        offset_4 = offset_3
                                        column_3 = column_2
                                        indent_column_3 = indent_column_2
                                        partial_tab_offset_3 = partial_tab_offset_2
                                        partial_tab_width_3 = partial_tab_width_2
                                        children_4 = [] if children_3 is not None else None
                                        while True: # case
                                            while True: # start reject
                                                children_5 = []
                                                offset_5 = offset_4 + 0
                                                column_4 = column_3
                                                indent_column_4 = indent_column_3
                                                partial_tab_offset_4 = partial_tab_offset_3
                                                partial_tab_width_4 = partial_tab_width_3
                                                count_1 = 0
                                                while count_1 < value_0:
                                                    offset_6 = offset_5
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    children_6 = [] if children_5 is not None else None
                                                    while True:
                                                        if buf[offset_6:offset_6+1] == '`':
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
                                                    count_1 += 1
                                                if count_1 < value_0:
                                                    offset_5 = -1
                                                    break
                                                if offset_5 == -1:
                                                    break

                                                while True: # start choice
                                                    offset_6 = offset_5
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    children_6 = [] if children_5 is not None else None
                                                    while True: # case
                                                        if offset_6 == buf_eof:
                                                            offset_6 = -1
                                                            break

                                                        codepoint = ord(buf[offset_6])

                                                        if codepoint == 96:
                                                            offset_6 = -1
                                                            break
                                                        else:
                                                            offset_6 += 1
                                                            column_5 += 1


                                                        break
                                                    if offset_6 != -1:
                                                        offset_5 = offset_6
                                                        column_4 = column_5
                                                        indent_column_4 = indent_column_5
                                                        partial_tab_offset_4 = partial_tab_offset_5
                                                        partial_tab_width_4 = partial_tab_width_5
                                                        if children_6 is not None and children_6 is not None:
                                                            children_5.extend(children_6)
                                                        break
                                                    # end case
                                                    offset_6 = offset_5
                                                    column_5 = column_4
                                                    indent_column_5 = indent_column_4
                                                    partial_tab_offset_5 = partial_tab_offset_4
                                                    partial_tab_width_5 = partial_tab_width_4
                                                    children_6 = [] if children_5 is not None else None
                                                    while True: # case
                                                        if offset_6 != buf_eof:
                                                            offset_6 = -1
                                                            break


                                                        break
                                                    if offset_6 != -1:
                                                        offset_5 = offset_6
                                                        column_4 = column_5
                                                        indent_column_4 = indent_column_5
                                                        partial_tab_offset_4 = partial_tab_offset_5
                                                        partial_tab_width_4 = partial_tab_width_5
                                                        if children_6 is not None and children_6 is not None:
                                                            children_5.extend(children_6)
                                                        break
                                                    # end case
                                                    offset_5 = -1 # no more choices
                                                    break # end choice
                                                if offset_5 == -1:
                                                    break

                                                break
                                            if offset_5 != -1:
                                                offset_4 = -1
                                                break

                                            offset_5 = offset_4
                                            children_5 = []
                                            while True: # start capture
                                                count_1 = 0
                                                while True:
                                                    offset_6 = offset_5
                                                    column_4 = column_3
                                                    indent_column_4 = indent_column_3
                                                    partial_tab_offset_4 = partial_tab_offset_3
                                                    partial_tab_width_4 = partial_tab_width_3
                                                    children_6 = [] if children_5 is not None else None
                                                    while True:
                                                        if buf[offset_6:offset_6+1] == '`':
                                                            offset_6 += 1
                                                            column_4 += 1
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
                                                    column_3 = column_4
                                                    indent_column_3 = indent_column_4
                                                    partial_tab_offset_3 = partial_tab_offset_4
                                                    partial_tab_width_3 = partial_tab_width_4
                                                    count_1 += 1
                                                if offset_5 == -1:
                                                    break

                                                break
                                            if offset_5 == -1:
                                                offset_4 = -1
                                                break
                                            value_3 = self.Node('text', offset_4, offset_5, children_5, None)
                                            children_4.append(value_3)
                                            offset_4 = offset_5


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
                            if count_0 < 1:
                                offset_2 = -1
                                break
                            if offset_2 == -1:
                                break

                            break
                        if offset_2 == -1:
                            offset_1 = -1
                            break
                        value_4 = self.Node('code_span', offset_1, offset_2, children_2, None)
                        children_1.append(value_4)
                        offset_1 = offset_2

                        count_0 = 0
                        while count_0 < value_0:
                            offset_2 = offset_1
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            children_2 = [] if children_1 is not None else None
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

                        while True: # start reject
                            children_2 = []
                            offset_2 = offset_1 + 0
                            column_2 = column_1
                            indent_column_2 = indent_column_1
                            partial_tab_offset_2 = partial_tab_offset_1
                            partial_tab_width_2 = partial_tab_width_1
                            if buf[offset_2:offset_2+1] == '`':
                                offset_2 += 1
                                column_2 += 1
                            else:
                                offset_2 = -1
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
                            count_0 = 0
                            while True:
                                offset_3 = offset_2
                                column_2 = column_1
                                indent_column_2 = indent_column_1
                                partial_tab_offset_2 = partial_tab_offset_1
                                partial_tab_width_2 = partial_tab_width_1
                                children_3 = [] if children_2 is not None else None
                                while True:
                                    if buf[offset_3:offset_3+1] == '`':
                                        offset_3 += 1
                                        column_2 += 1
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
                                column_1 = column_2
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
                        value_5 = self.Node('text', offset_1, offset_2, children_2, None)
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

    return Parser