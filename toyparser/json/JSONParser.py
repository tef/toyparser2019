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

regex_0 = re.compile(r'''(?:\[|\{)''')
regex_1 = re.compile(r'''(?:(?:(?:(?:\\u)[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F])|(?:(?:\\)["\\/bfnrt])|(?:[^\\"])))*''')
regex_2 = re.compile(r'''(?:(?:\-))?''')
regex_3 = re.compile(r'''(?:(?:(?:0))|(?:[1-9](?:[0-9])*))''')
regex_4 = re.compile(r'''(?:(?:\.)(?:[0-9])*)?''')
regex_5 = re.compile(r'''(?:(?:e|E)(?:(?:\+|\-)(?:[0-9])*)?)?''')

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
                _match = regex_0.match(buf, offset_1)
                if _match:
                    _end = _match.end()
                    column_1 += (_end - offset_1)
                    offset_1 = _end
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

    def parse_json_value(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
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
                    if buf[offset_1:offset_1+1] == '"':
                        offset_1 += 1
                        column_1 += 1
                    else:
                        offset_1 = -1
                        break

                    children_2 = None
                    value_0 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        _match = regex_1.match(buf, offset_1)
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
                    value_0.name = 'string'
                    value_0.end = offset_1
                    value_0.end_column = column_1
                    value_0.value = None
                    children_1.append(value_0)

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
                    children_2 = None
                    value_1 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
                    while True: # start capture
                        _match = regex_2.match(buf, offset_1)
                        if _match:
                            _end = _match.end()
                            column_1 += (_end - offset_1)
                            offset_1 = _end
                        else:
                            offset_1 = -1
                            break

                        _match = regex_3.match(buf, offset_1)
                        if _match:
                            _end = _match.end()
                            column_1 += (_end - offset_1)
                            offset_1 = _end
                        else:
                            offset_1 = -1
                            break

                        _match = regex_4.match(buf, offset_1)
                        if _match:
                            _end = _match.end()
                            column_1 += (_end - offset_1)
                            offset_1 = _end
                        else:
                            offset_1 = -1
                            break

                        _match = regex_5.match(buf, offset_1)
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
                    value_1.name = 'number'
                    value_1.end = offset_1
                    value_1.end_column = column_1
                    value_1.value = None
                    children_1.append(value_1)


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
                        if buf[offset_1:offset_1+4] == 'true':
                            offset_1 += 4
                            column_1 += 4
                        else:
                            offset_1 = -1
                            break

                        break
                    if offset_1 == -1:
                        break
                    value_2.name = 'bool'
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
                    value_3 = Node(None, offset_1, offset_1, column_1, column_1, children_2, None)
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
                    value_3.name = 'bool'
                    value_3.end = offset_1
                    value_3.end_column = column_1
                    value_3.value = None
                    children_1.append(value_3)


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
                        if buf[offset_1:offset_1+4] == 'null':
                            offset_1 += 4
                            column_1 += 4
                        else:
                            offset_1 = -1
                            break

                        break
                    if offset_1 == -1:
                        break
                    value_4.name = 'bool'
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
                offset_0 = -1 # no more choices
                break # end choice
            if offset_0 == -1:
                break

            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_json_list(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
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

                                if buf[offset_2:offset_2+1] == ',':
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

            if buf[offset_0:offset_0+1] == ']':
                offset_0 += 1
                column_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0

    def parse_json_object(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):
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
                            if buf[offset_1:offset_1+1] == '"':
                                offset_1 += 1
                                column_1 += 1
                            else:
                                offset_1 = -1
                                break

                            children_4 = None
                            value_3 = Node(None, offset_1, offset_1, column_1, column_1, children_4, None)
                            while True: # start capture
                                _match = regex_1.match(buf, offset_1)
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
                            value_3.name = 'string'
                            value_3.end = offset_1
                            value_3.end_column = column_1
                            value_3.value = None
                            children_3.append(value_3)

                            if buf[offset_1:offset_1+1] == '"':
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

                            if buf[offset_1:offset_1+1] == ':':
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
                                if buf[offset_2:offset_2+1] == ',':
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
                                value_5 = Node(None, offset_2, offset_2, column_2, column_2, children_4, None)
                                while True: # start capture
                                    if buf[offset_2:offset_2+1] == '"':
                                        offset_2 += 1
                                        column_2 += 1
                                    else:
                                        offset_2 = -1
                                        break

                                    children_5 = None
                                    value_6 = Node(None, offset_2, offset_2, column_2, column_2, children_5, None)
                                    while True: # start capture
                                        _match = regex_1.match(buf, offset_2)
                                        if _match:
                                            _end = _match.end()
                                            column_2 += (_end - offset_2)
                                            offset_2 = _end
                                        else:
                                            offset_2 = -1
                                            break

                                        break
                                    if offset_2 == -1:
                                        break
                                    value_6.name = 'string'
                                    value_6.end = offset_2
                                    value_6.end_column = column_2
                                    value_6.value = None
                                    children_4.append(value_6)

                                    if buf[offset_2:offset_2+1] == '"':
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

                                    if buf[offset_2:offset_2+1] == ':':
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
                                value_5.name = 'pair'
                                value_5.end = offset_2
                                value_5.end_column = column_2
                                value_5.value = None
                                children_3.append(value_5)

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
