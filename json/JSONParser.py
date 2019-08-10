class Parser:
    def __init__(self, builder=None, tabstop=None, allow_mixed_indent=False):
         self.builder = builder
         self.tabstop = tabstop or 8
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
        line_start, prefix, eof, children = offset, [], end, []
        new_offset, line_start = self.parse_document(buf, offset, line_start, prefix, eof, children)
        if children and new_offset == end: return children[-1]
        print('no', offset, new_offset, end, buf[new_offset:])
        if err is not None: raise err(buf, new_offset, 'no')

    def parse_document(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t\r\n':
                    offset_0 +=1
                    count_0 += self.tabstop if chr == '	' else 1
                else:
                    break

            while True: # start reject
                children_1 = []
                offset_1, line_start_1 = offset_0, line_start_0
                if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '[':
                    offset_1 += 1
                elif offset_1 + 1 <= buf_eof and buf[offset_1+0] == '{':
                    offset_1 += 1
                else:
                    offset_1 = -1
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break

            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                while True: # start choice
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = [] if children_1 is not None else None
                    while True: # case
                        offset_2, line_start_1 = self.parse_json_list(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                        if offset_2 == -1: break



                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        line_start_0 = line_start_1
                        if children_2 is not None and children_2 is not None:
                            children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = [] if children_1 is not None else None
                    while True: # case
                        offset_2, line_start_1 = self.parse_json_object(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                        if offset_2 == -1: break



                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        line_start_0 = line_start_1
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
                value_0 = self.Node('document', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1


            break
        return offset_0, line_start_0

    def parse_json_value(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, line_start_1 = self.parse_json_list(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
                    if offset_1 == -1: break



                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_1, line_start_1 = self.parse_json_object(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
                    if offset_1 == -1: break



                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '"':
                        offset_1 += 1
                    else:
                        offset_1 = -1
                        break

                    offset_2 = offset_1
                    children_2 = None
                    while True: # start capture
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                while True: # start choice
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 + 2 <= buf_eof and buf[offset_4+0] == '\\' and buf[offset_4+1] == 'u':
                                            offset_4 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if 48 <= chr <= 57:
                                            offset_4 += 1
                                        elif 97 <= chr <= 102:
                                            offset_4 += 1
                                        elif 65 <= chr <= 70:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if 48 <= chr <= 57:
                                            offset_4 += 1
                                        elif 97 <= chr <= 102:
                                            offset_4 += 1
                                        elif 65 <= chr <= 70:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if 48 <= chr <= 57:
                                            offset_4 += 1
                                        elif 97 <= chr <= 102:
                                            offset_4 += 1
                                        elif 65 <= chr <= 70:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if 48 <= chr <= 57:
                                            offset_4 += 1
                                        elif 97 <= chr <= 102:
                                            offset_4 += 1
                                        elif 65 <= chr <= 70:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_2 = line_start_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '\\':
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if chr == 34:
                                            offset_4 += 1
                                        elif chr == 92:
                                            offset_4 += 1
                                        elif chr == 47:
                                            offset_4 += 1
                                        elif chr == 98:
                                            offset_4 += 1
                                        elif chr == 102:
                                            offset_4 += 1
                                        elif chr == 110:
                                            offset_4 += 1
                                        elif chr == 114:
                                            offset_4 += 1
                                        elif chr == 116:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_2 = line_start_3
                                        if children_4 is not None and children_4 is not None:
                                            children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = [] if children_3 is not None else None
                                    while True: # case
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if chr == 92:
                                            offset_4 = -1
                                            break
                                        elif chr == 34:
                                            offset_4 = -1
                                            break
                                        else:
                                            offset_4 += 1


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_2 = line_start_3
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
                            line_start_1 = line_start_2
                            count_0 += 1
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_0 = self.builder['string'](buf, offset_1, offset_2, children_2)
                    else:
                        value_0 = self.Node('string', offset_1, offset_2, children_2, None)
                    children_1.append(value_0)
                    offset_1 = offset_2

                    if offset_1 + 1 <= buf_eof and buf[offset_1+0] == '"':
                        offset_1 += 1
                    else:
                        offset_1 = -1
                        break



                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    children_2 = None
                    while True: # start capture
                        count_0 = 0
                        while count_0 < 1:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '-':
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
                            count_0 += 1
                            break
                        if offset_2 == -1:
                            break

                        while True: # start choice
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '0':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break


                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                line_start_1 = line_start_2
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = ord(buf[offset_3])

                                if 49 <= chr <= 57:
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

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
                                    count_0 += 1
                                if offset_3 == -1:
                                    break


                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                line_start_1 = line_start_2
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_2 = -1 # no more choices
                            break # end choice
                        if offset_2 == -1:
                            break

                        count_0 = 0
                        while count_0 < 1:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '.':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_1 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

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
                                    count_1 += 1
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
                            count_0 += 1
                            break
                        if offset_2 == -1:
                            break

                        count_0 = 0
                        while count_0 < 1:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                if offset_3 + 1 <= buf_eof and buf[offset_3+0] == 'e':
                                    offset_3 += 1
                                elif offset_3 + 1 <= buf_eof and buf[offset_3+0] == 'E':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_1 = 0
                                while count_1 < 1:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = [] if children_3 is not None else None
                                    while True:
                                        if offset_4 + 1 <= buf_eof and buf[offset_4+0] == '+':
                                            offset_4 += 1
                                        elif offset_4 + 1 <= buf_eof and buf[offset_4+0] == '-':
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_2 = 0
                                        while True:
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = [] if children_4 is not None else None
                                            while True:
                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
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
                                            line_start_3 = line_start_4
                                            count_2 += 1
                                        if offset_4 == -1:
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    if children_4 is not None and children_4 is not None:
                                        children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_1 += 1
                                    break
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
                            count_0 += 1
                            break
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_1 = self.builder['number'](buf, offset_1, offset_2, children_2)
                    else:
                        value_1 = self.Node('number', offset_1, offset_2, children_2, None)
                    children_1.append(value_1)
                    offset_1 = offset_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    children_2 = None
                    while True: # start capture
                        if offset_2 + 4 <= buf_eof and buf[offset_2+0] == 't' and buf[offset_2+1] == 'r' and buf[offset_2+2] == 'u' and buf[offset_2+3] == 'e':
                            offset_2 += 4
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_2 = self.builder['bool'](buf, offset_1, offset_2, children_2)
                    else:
                        value_2 = self.Node('bool', offset_1, offset_2, children_2, None)
                    children_1.append(value_2)
                    offset_1 = offset_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    children_2 = None
                    while True: # start capture
                        if offset_2 + 5 <= buf_eof and buf[offset_2+0] == 'f' and buf[offset_2+1] == 'a' and buf[offset_2+2] == 'l' and buf[offset_2+3] == 's' and buf[offset_2+4] == 'e':
                            offset_2 += 5
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_3 = self.builder['bool'](buf, offset_1, offset_2, children_2)
                    else:
                        value_3 = self.Node('bool', offset_1, offset_2, children_2, None)
                    children_1.append(value_3)
                    offset_1 = offset_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = [] if children_0 is not None else None
                while True: # case
                    offset_2 = offset_1
                    children_2 = None
                    while True: # start capture
                        if offset_2 + 4 <= buf_eof and buf[offset_2+0] == 'n' and buf[offset_2+1] == 'u' and buf[offset_2+2] == 'l' and buf[offset_2+3] == 'l':
                            offset_2 += 4
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_4 = self.builder['bool'](buf, offset_1, offset_2, children_2)
                    else:
                        value_4 = self.Node('bool', offset_1, offset_2, children_2, None)
                    children_1.append(value_4)
                    offset_1 = offset_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    if children_1 is not None and children_1 is not None:
                        children_0.extend(children_1)
                    break
                # end case
                offset_0 = -1 # no more choices
                break # end choice
            if offset_0 == -1:
                break

            break
        return offset_0, line_start_0

    def parse_json_string(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '"':
                offset_0 += 1
            else:
                offset_0 = -1
                break

            offset_1 = offset_0
            children_1 = None
            while True: # start capture
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        while True: # start choice
                            offset_3 = offset_2
                            line_start_2 = line_start_1
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

                                chr = ord(buf[offset_3])

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

                                chr = ord(buf[offset_3])

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

                                chr = ord(buf[offset_3])

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

                                chr = ord(buf[offset_3])

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
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            line_start_2 = line_start_1
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

                                chr = ord(buf[offset_3])

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
                                if children_3 is not None and children_3 is not None:
                                    children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = [] if children_2 is not None else None
                            while True: # case
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = ord(buf[offset_3])

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
                value_0 = self.Node('string', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '"':
                offset_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, line_start_0

    def parse_json_list(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '[':
                offset_0 += 1
            else:
                offset_0 = -1
                break

            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t\r\n':
                    offset_0 +=1
                    count_0 += self.tabstop if chr == '	' else 1
                else:
                    break

            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        offset_2, line_start_1 = self.parse_json_value(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                        if offset_2 == -1: break


                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = [] if children_2 is not None else None
                            while True:
                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n':
                                        offset_3 +=1
                                        count_2 += self.tabstop if chr == '	' else 1
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
                                    if chr in ' \t\r\n':
                                        offset_3 +=1
                                        count_2 += self.tabstop if chr == '	' else 1
                                    else:
                                        break

                                offset_3, line_start_2 = self.parse_json_value(buf, offset_3, line_start_2, prefix_0, buf_eof, children_3)
                                if offset_3 == -1: break


                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            if children_3 is not None and children_3 is not None:
                                children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
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
                value_0 = self.Node('list', offset_0, offset_1, children_1, None)
            children_0.append(value_0)
            offset_0 = offset_1

            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == ']':
                offset_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, line_start_0

    def parse_json_object(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '{':
                offset_0 += 1
            else:
                offset_0 = -1
                break

            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t\r\n':
                    offset_0 +=1
                    count_0 += self.tabstop if chr == '	' else 1
                else:
                    break

            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = [] if children_1 is not None else None
                    while True:
                        offset_3 = offset_2
                        children_3 = []
                        while True: # start capture
                            if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '"':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break

                            offset_4 = offset_3
                            children_4 = None
                            while True: # start capture
                                count_1 = 0
                                while True:
                                    offset_5 = offset_4
                                    line_start_2 = line_start_1
                                    children_5 = [] if children_4 is not None else None
                                    while True:
                                        while True: # start choice
                                            offset_6 = offset_5
                                            line_start_3 = line_start_2
                                            children_6 = [] if children_5 is not None else None
                                            while True: # case
                                                if offset_6 + 2 <= buf_eof and buf[offset_6+0] == '\\' and buf[offset_6+1] == 'u':
                                                    offset_6 += 2
                                                else:
                                                    offset_6 = -1
                                                    break

                                                if offset_6 == buf_eof:
                                                    offset_6 = -1
                                                    break

                                                chr = ord(buf[offset_6])

                                                if 48 <= chr <= 57:
                                                    offset_6 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_6 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_6 += 1
                                                else:
                                                    offset_6 = -1
                                                    break

                                                if offset_6 == buf_eof:
                                                    offset_6 = -1
                                                    break

                                                chr = ord(buf[offset_6])

                                                if 48 <= chr <= 57:
                                                    offset_6 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_6 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_6 += 1
                                                else:
                                                    offset_6 = -1
                                                    break

                                                if offset_6 == buf_eof:
                                                    offset_6 = -1
                                                    break

                                                chr = ord(buf[offset_6])

                                                if 48 <= chr <= 57:
                                                    offset_6 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_6 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_6 += 1
                                                else:
                                                    offset_6 = -1
                                                    break

                                                if offset_6 == buf_eof:
                                                    offset_6 = -1
                                                    break

                                                chr = ord(buf[offset_6])

                                                if 48 <= chr <= 57:
                                                    offset_6 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_6 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_6 += 1
                                                else:
                                                    offset_6 = -1
                                                    break


                                                break
                                            if offset_6 != -1:
                                                offset_5 = offset_6
                                                line_start_2 = line_start_3
                                                if children_6 is not None and children_6 is not None:
                                                    children_5.extend(children_6)
                                                break
                                            # end case
                                            offset_6 = offset_5
                                            line_start_3 = line_start_2
                                            children_6 = [] if children_5 is not None else None
                                            while True: # case
                                                if offset_6 + 1 <= buf_eof and buf[offset_6+0] == '\\':
                                                    offset_6 += 1
                                                else:
                                                    offset_6 = -1
                                                    break

                                                if offset_6 == buf_eof:
                                                    offset_6 = -1
                                                    break

                                                chr = ord(buf[offset_6])

                                                if chr == 34:
                                                    offset_6 += 1
                                                elif chr == 92:
                                                    offset_6 += 1
                                                elif chr == 47:
                                                    offset_6 += 1
                                                elif chr == 98:
                                                    offset_6 += 1
                                                elif chr == 102:
                                                    offset_6 += 1
                                                elif chr == 110:
                                                    offset_6 += 1
                                                elif chr == 114:
                                                    offset_6 += 1
                                                elif chr == 116:
                                                    offset_6 += 1
                                                else:
                                                    offset_6 = -1
                                                    break


                                                break
                                            if offset_6 != -1:
                                                offset_5 = offset_6
                                                line_start_2 = line_start_3
                                                if children_6 is not None and children_6 is not None:
                                                    children_5.extend(children_6)
                                                break
                                            # end case
                                            offset_6 = offset_5
                                            line_start_3 = line_start_2
                                            children_6 = [] if children_5 is not None else None
                                            while True: # case
                                                if offset_6 == buf_eof:
                                                    offset_6 = -1
                                                    break

                                                chr = ord(buf[offset_6])

                                                if chr == 92:
                                                    offset_6 = -1
                                                    break
                                                elif chr == 34:
                                                    offset_6 = -1
                                                    break
                                                else:
                                                    offset_6 += 1


                                                break
                                            if offset_6 != -1:
                                                offset_5 = offset_6
                                                line_start_2 = line_start_3
                                                if children_6 is not None and children_6 is not None:
                                                    children_5.extend(children_6)
                                                break
                                            # end case
                                            offset_5 = -1 # no more choices
                                            break # end choice
                                        if offset_5 == -1:
                                            break

                                        break
                                    if offset_5 == -1:
                                        break
                                    if offset_4 == offset_5: break
                                    if children_5 is not None and children_5 is not None:
                                        children_4.extend(children_5)
                                    offset_4 = offset_5
                                    line_start_1 = line_start_2
                                    count_1 += 1
                                if offset_4 == -1:
                                    break

                                break
                            if offset_4 == -1:
                                offset_3 = -1
                                break
                            if self.builder is not None:
                                value_0 = self.builder['string'](buf, offset_3, offset_4, children_4)
                            else:
                                value_0 = self.Node('string', offset_3, offset_4, children_4, None)
                            children_3.append(value_0)
                            offset_3 = offset_4

                            if offset_3 + 1 <= buf_eof and buf[offset_3+0] == '"':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break


                            count_1 = 0
                            while offset_3 < buf_eof:
                                chr = buf[offset_3]
                                if chr in ' \t\r\n':
                                    offset_3 +=1
                                    count_1 += self.tabstop if chr == '	' else 1
                                else:
                                    break

                            if offset_3 + 1 <= buf_eof and buf[offset_3+0] == ':':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break

                            count_1 = 0
                            while offset_3 < buf_eof:
                                chr = buf[offset_3]
                                if chr in ' \t\r\n':
                                    offset_3 +=1
                                    count_1 += self.tabstop if chr == '	' else 1
                                else:
                                    break

                            offset_3, line_start_1 = self.parse_json_value(buf, offset_3, line_start_1, prefix_0, buf_eof, children_3)
                            if offset_3 == -1: break


                            break
                        if offset_3 == -1:
                            offset_2 = -1
                            break
                        if self.builder is not None:
                            value_1 = self.builder['pair'](buf, offset_2, offset_3, children_3)
                        else:
                            value_1 = self.Node('pair', offset_2, offset_3, children_3, None)
                        children_2.append(value_1)
                        offset_2 = offset_3

                        count_1 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t\r\n':
                                offset_2 +=1
                                count_1 += self.tabstop if chr == '	' else 1
                            else:
                                break

                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
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
                                    if chr in ' \t\r\n':
                                        offset_3 +=1
                                        count_2 += self.tabstop if chr == '	' else 1
                                    else:
                                        break

                                offset_4 = offset_3
                                children_4 = []
                                while True: # start capture
                                    offset_4, line_start_2 = self.parse_json_string(buf, offset_4, line_start_2, prefix_0, buf_eof, children_4)
                                    if offset_4 == -1: break


                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        chr = buf[offset_4]
                                        if chr in ' \t\r\n':
                                            offset_4 +=1
                                            count_2 += self.tabstop if chr == '	' else 1
                                        else:
                                            break

                                    if offset_4 + 1 <= buf_eof and buf[offset_4+0] == ':':
                                        offset_4 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        chr = buf[offset_4]
                                        if chr in ' \t\r\n':
                                            offset_4 +=1
                                            count_2 += self.tabstop if chr == '	' else 1
                                        else:
                                            break

                                    offset_4, line_start_2 = self.parse_json_value(buf, offset_4, line_start_2, prefix_0, buf_eof, children_4)
                                    if offset_4 == -1: break


                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                if self.builder is not None:
                                    value_2 = self.builder['pair'](buf, offset_3, offset_4, children_4)
                                else:
                                    value_2 = self.Node('pair', offset_3, offset_4, children_4, None)
                                children_3.append(value_2)
                                offset_3 = offset_4

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n':
                                        offset_3 +=1
                                        count_2 += self.tabstop if chr == '	' else 1
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
                    count_0 += 1
                    break
                if offset_1 == -1:
                    break

                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_3 = self.builder['object'](buf, offset_0, offset_1, children_1)
            else:
                value_3 = self.Node('object', offset_0, offset_1, children_1, None)
            children_0.append(value_3)
            offset_0 = offset_1

            if offset_0 + 1 <= buf_eof and buf[offset_0+0] == '}':
                offset_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, line_start_0