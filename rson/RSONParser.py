class Parser:
    def __init__(self, builder=None, tabstop=None, allow_mixed_indent=False):
         self.builder = builder
         self.tabstop = tabstop or self.TABSTOP
         self.cache = None
         self.allow_mixed_indent = allow_mixed_indent

    NEWLINE = ()
    WHITESPACE = (' ', '\t', '\r', '\n', '\ufeff')
    TABSTOP = 8

    class Node:
        def __init__(self, name, start, end, children, value):
            self.name = name
            self.start = start
            self.end = end
            self.children = children
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
                if chr in ' \t\r\n\ufeff':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break

            count_0 = 0
            while True:
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True:
                    if buf[offset_1:offset_1+1] == '#':
                        offset_1 += 1
                    else:
                        offset_1 = -1
                        break

                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        line_start_2 = line_start_1
                        children_2 = []
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

                            break
                        if offset_2 == -1:
                            break
                        if offset_1 == offset_2: break
                        children_1.extend(children_2)
                        offset_1 = offset_2
                        line_start_1 = line_start_2
                        count_1 += 1
                    if offset_1 == -1:
                        break

                    count_1 = 0
                    while offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in ' \t\r\n\ufeff':
                            offset_1 +=1
                            count_1 +=1
                        else:
                            break

                    break
                if offset_1 == -1:
                    break
                if offset_0 == offset_1: break
                children_0.extend(children_1)
                offset_0 = offset_1
                line_start_0 = line_start_1
                count_0 += 1
            if offset_0 == -1:
                break

            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t\r\n\ufeff':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break


            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                offset_1, line_start_0 = self.parse_rson_value(buf, offset_1, line_start_0, prefix_0, buf_eof, children_1)
                if offset_1 == -1: break


                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['document'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('document', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1

            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t\r\n\ufeff':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break

            count_0 = 0
            while True:
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True:
                    if buf[offset_1:offset_1+1] == '#':
                        offset_1 += 1
                    else:
                        offset_1 = -1
                        break

                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        line_start_2 = line_start_1
                        children_2 = []
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

                            break
                        if offset_2 == -1:
                            break
                        if offset_1 == offset_2: break
                        children_1.extend(children_2)
                        offset_1 = offset_2
                        line_start_1 = line_start_2
                        count_1 += 1
                    if offset_1 == -1:
                        break

                    count_1 = 0
                    while offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in ' \t\r\n\ufeff':
                            offset_1 +=1
                            count_1 +=1
                        else:
                            break

                    break
                if offset_1 == -1:
                    break
                if offset_0 == offset_1: break
                children_0.extend(children_1)
                offset_0 = offset_1
                line_start_0 = line_start_1
                count_0 += 1
            if offset_0 == -1:
                break

            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t\r\n\ufeff':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break



            break
        return offset_0, line_start_0

    def parse_rson_value(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        if buf[offset_2:offset_2+1] == '@':
                            offset_2 += 1
                        else:
                            offset_2 = -1
                            break

                        offset_3 = offset_2
                        children_3 = []
                        while True: # start capture
                            if offset_3 == buf_eof:
                                offset_3 = -1
                                break

                            chr = ord(buf[offset_3])

                            if 97 <= chr <= 122:
                                offset_3 += 1
                            elif 97 <= chr <= 90:
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break

                            count_0 = 0
                            while True:
                                offset_4 = offset_3
                                line_start_2 = line_start_1
                                children_4 = []
                                while True:
                                    if offset_4 == buf_eof:
                                        offset_4 = -1
                                        break

                                    chr = ord(buf[offset_4])

                                    if 48 <= chr <= 57:
                                        offset_4 += 1
                                    elif 97 <= chr <= 122:
                                        offset_4 += 1
                                    elif 65 <= chr <= 90:
                                        offset_4 += 1
                                    elif chr == 95:
                                        offset_4 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    break
                                if offset_4 == -1:
                                    break
                                if offset_3 == offset_4: break
                                children_3.extend(children_4)
                                offset_3 = offset_4
                                line_start_1 = line_start_2
                                count_0 += 1
                            if offset_3 == -1:
                                break

                            break
                        if offset_3 == -1:
                            offset_2 = -1
                            break
                        if self.builder is not None:
                            value_0 = self.builder['identifier'](buf, offset_2, offset_3, children_3)
                        else:
                            value_0 = self.Node('identifier', offset_2, offset_3, list(children_3), None)
                        children_2.append(value_0)
                        offset_2 = offset_3

                        if buf[offset_2:offset_2+1] == ' ':
                            offset_2 += 1
                        else:
                            offset_2 = -1
                            break

                        offset_2, line_start_1 = self.parse_rson_literal(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                        if offset_2 == -1: break


                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_1 = self.builder['tagged'](buf, offset_1, offset_2, children_2)
                    else:
                        value_1 = self.Node('tagged', offset_1, offset_2, list(children_2), None)
                    children_1.append(value_1)
                    offset_1 = offset_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_rson_literal(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
                    if offset_1 == -1: break



                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    children_0.extend(children_1)
                    break
                # end case
                offset_0 = -1 # no more choices
                break # end choice
            if offset_0 == -1:
                break

            break
        return offset_0, line_start_0

    def parse_rson_literal(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_rson_list(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
                    if offset_1 == -1: break



                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_rson_object(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
                    if offset_1 == -1: break



                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    while True: # start choice
                        offset_2 = offset_1
                        line_start_2 = line_start_1
                        children_2 = []
                        while True: # case
                            if buf[offset_2:offset_2+1] == '"':
                                offset_2 += 1
                            else:
                                offset_2 = -1
                                break

                            offset_3 = offset_2
                            children_3 = []
                            while True: # start capture
                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        while True: # start choice
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
                                            while True: # case
                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if chr <= 31:
                                                    offset_5 = -1
                                                    break
                                                elif chr == 92:
                                                    offset_5 = -1
                                                    break
                                                elif chr == 34:
                                                    offset_5 = -1
                                                    break
                                                elif 55296 <= chr <= 57343:
                                                    offset_5 = -1
                                                    break
                                                else:
                                                    offset_5 += 1


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                line_start_3 = line_start_4
                                                children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
                                            while True: # case
                                                if buf[offset_5:offset_5+2] == '\\x':
                                                    offset_5 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6, line_start_5 = offset_5, line_start_4
                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    chr = ord(buf[offset_6])

                                                    if 48 <= chr <= 49:
                                                        offset_6 += 1
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

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                line_start_3 = line_start_4
                                                children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
                                            while True: # case
                                                if buf[offset_5:offset_5+2] == '\\u':
                                                    offset_5 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6, line_start_5 = offset_5, line_start_4
                                                    if buf[offset_6:offset_6+3] == '000':
                                                        offset_6 += 3
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    chr = ord(buf[offset_6])

                                                    if 48 <= chr <= 49:
                                                        offset_6 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6, line_start_5 = offset_5, line_start_4
                                                    if buf[offset_6:offset_6+1] == 'D':
                                                        offset_6 += 1
                                                    elif buf[offset_6:offset_6+1] == 'd':
                                                        offset_6 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    chr = ord(buf[offset_6])

                                                    if 56 <= chr <= 57:
                                                        offset_6 += 1
                                                    elif 65 <= chr <= 70:
                                                        offset_6 += 1
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

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                line_start_3 = line_start_4
                                                children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
                                            while True: # case
                                                if buf[offset_5:offset_5+2] == '\\U':
                                                    offset_5 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6, line_start_5 = offset_5, line_start_4
                                                    if buf[offset_6:offset_6+7] == '0000000':
                                                        offset_6 += 7
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    chr = ord(buf[offset_6])

                                                    if 48 <= chr <= 49:
                                                        offset_6 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6, line_start_5 = offset_5, line_start_4
                                                    if buf[offset_6:offset_6+4] == '0000':
                                                        offset_6 += 4
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if buf[offset_6:offset_6+1] == 'D':
                                                        offset_6 += 1
                                                    elif buf[offset_6:offset_6+1] == 'd':
                                                        offset_6 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    chr = ord(buf[offset_6])

                                                    if 56 <= chr <= 57:
                                                        offset_6 += 1
                                                    elif 65 <= chr <= 70:
                                                        offset_6 += 1
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

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                line_start_3 = line_start_4
                                                children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
                                            while True: # case
                                                if buf[offset_5:offset_5+1] == '\\':
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if chr == 34:
                                                    offset_5 += 1
                                                elif chr == 92:
                                                    offset_5 += 1
                                                elif chr == 47:
                                                    offset_5 += 1
                                                elif chr == 98:
                                                    offset_5 += 1
                                                elif chr == 102:
                                                    offset_5 += 1
                                                elif chr == 110:
                                                    offset_5 += 1
                                                elif chr == 114:
                                                    offset_5 += 1
                                                elif chr == 116:
                                                    offset_5 += 1
                                                elif chr == 39:
                                                    offset_5 += 1
                                                elif chr == 10:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                line_start_3 = line_start_4
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
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_0 += 1
                                if offset_3 == -1:
                                    break

                                break
                            if offset_3 == -1:
                                offset_2 = -1
                                break
                            if self.builder is not None:
                                value_0 = self.builder['string'](buf, offset_2, offset_3, children_3)
                            else:
                                value_0 = self.Node('string', offset_2, offset_3, list(children_3), None)
                            children_2.append(value_0)
                            offset_2 = offset_3

                            if buf[offset_2:offset_2+1] == '"':
                                offset_2 += 1
                            else:
                                offset_2 = -1
                                break


                            break
                        if offset_2 != -1:
                            offset_1 = offset_2
                            line_start_1 = line_start_2
                            children_1.extend(children_2)
                            break
                        # end case
                        offset_2 = offset_1
                        line_start_2 = line_start_1
                        children_2 = []
                        while True: # case
                            if buf[offset_2:offset_2+1] == "'":
                                offset_2 += 1
                            else:
                                offset_2 = -1
                                break

                            offset_3 = offset_2
                            children_3 = []
                            while True: # start capture
                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        while True: # start choice
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
                                            while True: # case
                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if chr <= 31:
                                                    offset_5 = -1
                                                    break
                                                elif chr == 92:
                                                    offset_5 = -1
                                                    break
                                                elif chr == 39:
                                                    offset_5 = -1
                                                    break
                                                elif 55296 <= chr <= 57343:
                                                    offset_5 = -1
                                                    break
                                                else:
                                                    offset_5 += 1


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                line_start_3 = line_start_4
                                                children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
                                            while True: # case
                                                if buf[offset_5:offset_5+2] == '\\x':
                                                    offset_5 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6, line_start_5 = offset_5, line_start_4
                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    chr = ord(buf[offset_6])

                                                    if 48 <= chr <= 49:
                                                        offset_6 += 1
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

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                line_start_3 = line_start_4
                                                children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
                                            while True: # case
                                                if buf[offset_5:offset_5+2] == '\\u':
                                                    offset_5 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6, line_start_5 = offset_5, line_start_4
                                                    if buf[offset_6:offset_6+2] == '00':
                                                        offset_6 += 2
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    chr = ord(buf[offset_6])

                                                    if 48 <= chr <= 49:
                                                        offset_6 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6, line_start_5 = offset_5, line_start_4
                                                    if buf[offset_6:offset_6+1] == 'D':
                                                        offset_6 += 1
                                                    elif buf[offset_6:offset_6+1] == 'd':
                                                        offset_6 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    chr = ord(buf[offset_6])

                                                    if 56 <= chr <= 57:
                                                        offset_6 += 1
                                                    elif 65 <= chr <= 70:
                                                        offset_6 += 1
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

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                line_start_3 = line_start_4
                                                children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
                                            while True: # case
                                                if buf[offset_5:offset_5+2] == '\\U':
                                                    offset_5 += 2
                                                else:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6, line_start_5 = offset_5, line_start_4
                                                    if buf[offset_6:offset_6+6] == '000000':
                                                        offset_6 += 6
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    chr = ord(buf[offset_6])

                                                    if 48 <= chr <= 49:
                                                        offset_6 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    break
                                                if offset_6 != -1:
                                                    offset_5 = -1
                                                    break

                                                while True: # start reject
                                                    children_6 = []
                                                    offset_6, line_start_5 = offset_5, line_start_4
                                                    if buf[offset_6:offset_6+4] == '0000':
                                                        offset_6 += 4
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if buf[offset_6:offset_6+1] == 'D':
                                                        offset_6 += 1
                                                    elif buf[offset_6:offset_6+1] == 'd':
                                                        offset_6 += 1
                                                    else:
                                                        offset_6 = -1
                                                        break

                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    chr = ord(buf[offset_6])

                                                    if 56 <= chr <= 57:
                                                        offset_6 += 1
                                                    elif 65 <= chr <= 70:
                                                        offset_6 += 1
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

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if 48 <= chr <= 57:
                                                    offset_5 += 1
                                                elif 97 <= chr <= 102:
                                                    offset_5 += 1
                                                elif 65 <= chr <= 70:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                line_start_3 = line_start_4
                                                children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
                                            while True: # case
                                                if buf[offset_5:offset_5+1] == '\\':
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                if offset_5 == buf_eof:
                                                    offset_5 = -1
                                                    break

                                                chr = ord(buf[offset_5])

                                                if chr == 34:
                                                    offset_5 += 1
                                                elif chr == 92:
                                                    offset_5 += 1
                                                elif chr == 47:
                                                    offset_5 += 1
                                                elif chr == 98:
                                                    offset_5 += 1
                                                elif chr == 102:
                                                    offset_5 += 1
                                                elif chr == 110:
                                                    offset_5 += 1
                                                elif chr == 114:
                                                    offset_5 += 1
                                                elif chr == 116:
                                                    offset_5 += 1
                                                elif chr == 39:
                                                    offset_5 += 1
                                                elif chr == 10:
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break


                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                line_start_3 = line_start_4
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
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_0 += 1
                                if offset_3 == -1:
                                    break

                                break
                            if offset_3 == -1:
                                offset_2 = -1
                                break
                            if self.builder is not None:
                                value_1 = self.builder['string'](buf, offset_2, offset_3, children_3)
                            else:
                                value_1 = self.Node('string', offset_2, offset_3, list(children_3), None)
                            children_2.append(value_1)
                            offset_2 = offset_3

                            if buf[offset_2:offset_2+1] == "'":
                                offset_2 += 1
                            else:
                                offset_2 = -1
                                break


                            break
                        if offset_2 != -1:
                            offset_1 = offset_2
                            line_start_1 = line_start_2
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
                    line_start_0 = line_start_1
                    children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        while True: # start choice
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True: # case
                                count_0 = 0
                                while count_0 < 1:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if chr == 45:
                                            offset_4 += 1
                                        elif chr == 43:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_0 += 1
                                    break
                                if offset_3 == -1:
                                    break

                                if buf[offset_3:offset_3+2] == '0x':
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
                                elif 65 <= chr <= 70:
                                    offset_3 += 1
                                elif 97 <= chr <= 102:
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if 48 <= chr <= 57:
                                            offset_4 += 1
                                        elif 65 <= chr <= 70:
                                            offset_4 += 1
                                        elif 97 <= chr <= 102:
                                            offset_4 += 1
                                        elif chr == 95:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
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
                                children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True: # case
                                count_0 = 0
                                while count_0 < 1:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if chr == 45:
                                            offset_4 += 1
                                        elif chr == 43:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_0 += 1
                                    break
                                if offset_3 == -1:
                                    break

                                if buf[offset_3:offset_3+2] == '0o':
                                    offset_3 += 2
                                else:
                                    offset_3 = -1
                                    break

                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = ord(buf[offset_3])

                                if 48 <= chr <= 56:
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if 48 <= chr <= 56:
                                            offset_4 += 1
                                        elif chr == 95:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
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
                                children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True: # case
                                count_0 = 0
                                while count_0 < 1:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if chr == 45:
                                            offset_4 += 1
                                        elif chr == 43:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_0 += 1
                                    break
                                if offset_3 == -1:
                                    break

                                if buf[offset_3:offset_3+2] == '0b':
                                    offset_3 += 2
                                else:
                                    offset_3 = -1
                                    break

                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break

                                chr = ord(buf[offset_3])

                                if 48 <= chr <= 49:
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if 48 <= chr <= 49:
                                            offset_4 += 1
                                        elif chr == 95:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
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
                                children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True: # case
                                count_0 = 0
                                while count_0 < 1:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if chr == 45:
                                            offset_4 += 1
                                        elif chr == 43:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_0 += 1
                                    break
                                if offset_3 == -1:
                                    break

                                while True: # start choice
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True: # case
                                        if buf[offset_4:offset_4+1] == '0':
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_2 = line_start_3
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True: # case
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if 49 <= chr <= 57:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_0 = 0
                                        while True:
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
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
                                            children_4.extend(children_5)
                                            offset_4 = offset_5
                                            line_start_3 = line_start_4
                                            count_0 += 1
                                        if offset_4 == -1:
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_2 = line_start_3
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
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if buf[offset_4:offset_4+1] == '.':
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_1 = 0
                                        while True:
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
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
                                            children_4.extend(children_5)
                                            offset_4 = offset_5
                                            line_start_3 = line_start_4
                                            count_1 += 1
                                        if offset_4 == -1:
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_0 += 1
                                    break
                                if offset_3 == -1:
                                    break

                                count_0 = 0
                                while count_0 < 1:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if buf[offset_4:offset_4+1] == 'e':
                                            offset_4 += 1
                                        elif buf[offset_4:offset_4+1] == 'E':
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_1 = 0
                                        while count_1 < 1:
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
                                            while True:
                                                if buf[offset_5:offset_5+1] == '+':
                                                    offset_5 += 1
                                                elif buf[offset_5:offset_5+1] == '-':
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break

                                                count_2 = 0
                                                while True:
                                                    offset_6 = offset_5
                                                    line_start_5 = line_start_4
                                                    children_6 = []
                                                    while True:
                                                        if offset_6 == buf_eof:
                                                            offset_6 = -1
                                                            break

                                                        chr = ord(buf[offset_6])

                                                        if 48 <= chr <= 57:
                                                            offset_6 += 1
                                                        else:
                                                            offset_6 = -1
                                                            break

                                                        break
                                                    if offset_6 == -1:
                                                        break
                                                    if offset_5 == offset_6: break
                                                    children_5.extend(children_6)
                                                    offset_5 = offset_6
                                                    line_start_4 = line_start_5
                                                    count_2 += 1
                                                if offset_5 == -1:
                                                    break

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            children_4.extend(children_5)
                                            offset_4 = offset_5
                                            line_start_3 = line_start_4
                                            count_1 += 1
                                            break
                                        if offset_4 == -1:
                                            break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_0 += 1
                                    break
                                if offset_3 == -1:
                                    break


                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                line_start_1 = line_start_2
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
                        value_2 = self.builder['number'](buf, offset_1, offset_2, children_2)
                    else:
                        value_2 = self.Node('number', offset_1, offset_2, list(children_2), None)
                    children_1.append(value_2)
                    offset_1 = offset_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        if buf[offset_2:offset_2+4] == 'true':
                            offset_2 += 4
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
                        value_3 = self.Node('bool', offset_1, offset_2, list(children_2), None)
                    children_1.append(value_3)
                    offset_1 = offset_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        if buf[offset_2:offset_2+5] == 'false':
                            offset_2 += 5
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
                        value_4 = self.Node('bool', offset_1, offset_2, list(children_2), None)
                    children_1.append(value_4)
                    offset_1 = offset_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        if buf[offset_2:offset_2+4] == 'null':
                            offset_2 += 4
                        else:
                            offset_2 = -1
                            break

                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_5 = self.builder['null'](buf, offset_1, offset_2, children_2)
                    else:
                        value_5 = self.Node('null', offset_1, offset_2, list(children_2), None)
                    children_1.append(value_5)
                    offset_1 = offset_2


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    children_0.extend(children_1)
                    break
                # end case
                offset_0 = -1 # no more choices
                break # end choice
            if offset_0 == -1:
                break

            break
        return offset_0, line_start_0

    def parse_rson_string(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    if buf[offset_1:offset_1+1] == '"':
                        offset_1 += 1
                    else:
                        offset_1 = -1
                        break

                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True:
                                while True: # start choice
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True: # case
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if chr <= 31:
                                            offset_4 = -1
                                            break
                                        elif chr == 92:
                                            offset_4 = -1
                                            break
                                        elif chr == 34:
                                            offset_4 = -1
                                            break
                                        elif 55296 <= chr <= 57343:
                                            offset_4 = -1
                                            break
                                        else:
                                            offset_4 += 1


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_2 = line_start_3
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True: # case
                                        if buf[offset_4:offset_4+2] == '\\x':
                                            offset_4 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5, line_start_4 = offset_4, line_start_3
                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            chr = ord(buf[offset_5])

                                            if 48 <= chr <= 49:
                                                offset_5 += 1
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
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True: # case
                                        if buf[offset_4:offset_4+2] == '\\u':
                                            offset_4 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5, line_start_4 = offset_4, line_start_3
                                            if buf[offset_5:offset_5+3] == '000':
                                                offset_5 += 3
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            chr = ord(buf[offset_5])

                                            if 48 <= chr <= 49:
                                                offset_5 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5, line_start_4 = offset_4, line_start_3
                                            if buf[offset_5:offset_5+1] == 'D':
                                                offset_5 += 1
                                            elif buf[offset_5:offset_5+1] == 'd':
                                                offset_5 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            chr = ord(buf[offset_5])

                                            if 56 <= chr <= 57:
                                                offset_5 += 1
                                            elif 65 <= chr <= 70:
                                                offset_5 += 1
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
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True: # case
                                        if buf[offset_4:offset_4+2] == '\\U':
                                            offset_4 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5, line_start_4 = offset_4, line_start_3
                                            if buf[offset_5:offset_5+7] == '0000000':
                                                offset_5 += 7
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            chr = ord(buf[offset_5])

                                            if 48 <= chr <= 49:
                                                offset_5 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5, line_start_4 = offset_4, line_start_3
                                            if buf[offset_5:offset_5+4] == '0000':
                                                offset_5 += 4
                                            else:
                                                offset_5 = -1
                                                break

                                            if buf[offset_5:offset_5+1] == 'D':
                                                offset_5 += 1
                                            elif buf[offset_5:offset_5+1] == 'd':
                                                offset_5 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            chr = ord(buf[offset_5])

                                            if 56 <= chr <= 57:
                                                offset_5 += 1
                                            elif 65 <= chr <= 70:
                                                offset_5 += 1
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
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True: # case
                                        if buf[offset_4:offset_4+1] == '\\':
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
                                        elif chr == 39:
                                            offset_4 += 1
                                        elif chr == 10:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_2 = line_start_3
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
                        value_0 = self.Node('string', offset_1, offset_2, list(children_2), None)
                    children_1.append(value_0)
                    offset_1 = offset_2

                    if buf[offset_1:offset_1+1] == '"':
                        offset_1 += 1
                    else:
                        offset_1 = -1
                        break


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    if buf[offset_1:offset_1+1] == "'":
                        offset_1 += 1
                    else:
                        offset_1 = -1
                        break

                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True:
                                while True: # start choice
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True: # case
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if chr <= 31:
                                            offset_4 = -1
                                            break
                                        elif chr == 92:
                                            offset_4 = -1
                                            break
                                        elif chr == 39:
                                            offset_4 = -1
                                            break
                                        elif 55296 <= chr <= 57343:
                                            offset_4 = -1
                                            break
                                        else:
                                            offset_4 += 1


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_2 = line_start_3
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True: # case
                                        if buf[offset_4:offset_4+2] == '\\x':
                                            offset_4 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5, line_start_4 = offset_4, line_start_3
                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            chr = ord(buf[offset_5])

                                            if 48 <= chr <= 49:
                                                offset_5 += 1
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
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True: # case
                                        if buf[offset_4:offset_4+2] == '\\u':
                                            offset_4 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5, line_start_4 = offset_4, line_start_3
                                            if buf[offset_5:offset_5+2] == '00':
                                                offset_5 += 2
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            chr = ord(buf[offset_5])

                                            if 48 <= chr <= 49:
                                                offset_5 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5, line_start_4 = offset_4, line_start_3
                                            if buf[offset_5:offset_5+1] == 'D':
                                                offset_5 += 1
                                            elif buf[offset_5:offset_5+1] == 'd':
                                                offset_5 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            chr = ord(buf[offset_5])

                                            if 56 <= chr <= 57:
                                                offset_5 += 1
                                            elif 65 <= chr <= 70:
                                                offset_5 += 1
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
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True: # case
                                        if buf[offset_4:offset_4+2] == '\\U':
                                            offset_4 += 2
                                        else:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5, line_start_4 = offset_4, line_start_3
                                            if buf[offset_5:offset_5+6] == '000000':
                                                offset_5 += 6
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            chr = ord(buf[offset_5])

                                            if 48 <= chr <= 49:
                                                offset_5 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            break
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break

                                        while True: # start reject
                                            children_5 = []
                                            offset_5, line_start_4 = offset_4, line_start_3
                                            if buf[offset_5:offset_5+4] == '0000':
                                                offset_5 += 4
                                            else:
                                                offset_5 = -1
                                                break

                                            if buf[offset_5:offset_5+1] == 'D':
                                                offset_5 += 1
                                            elif buf[offset_5:offset_5+1] == 'd':
                                                offset_5 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break

                                            chr = ord(buf[offset_5])

                                            if 56 <= chr <= 57:
                                                offset_5 += 1
                                            elif 65 <= chr <= 70:
                                                offset_5 += 1
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
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True: # case
                                        if buf[offset_4:offset_4+1] == '\\':
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
                                        elif chr == 39:
                                            offset_4 += 1
                                        elif chr == 10:
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break


                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_2 = line_start_3
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
                        value_1 = self.builder['string'](buf, offset_1, offset_2, children_2)
                    else:
                        value_1 = self.Node('string', offset_1, offset_2, list(children_2), None)
                    children_1.append(value_1)
                    offset_1 = offset_2

                    if buf[offset_1:offset_1+1] == "'":
                        offset_1 += 1
                    else:
                        offset_1 = -1
                        break


                    break
                if offset_1 != -1:
                    offset_0 = offset_1
                    line_start_0 = line_start_1
                    children_0.extend(children_1)
                    break
                # end case
                offset_0 = -1 # no more choices
                break # end choice
            if offset_0 == -1:
                break

            break
        return offset_0, line_start_0

    def parse_rson_list(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            if buf[offset_0:offset_0+1] == '[':
                offset_0 += 1
            else:
                offset_0 = -1
                break

            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t\r\n\ufeff':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break

            count_0 = 0
            while True:
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True:
                    if buf[offset_1:offset_1+1] == '#':
                        offset_1 += 1
                    else:
                        offset_1 = -1
                        break

                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        line_start_2 = line_start_1
                        children_2 = []
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

                            break
                        if offset_2 == -1:
                            break
                        if offset_1 == offset_2: break
                        children_1.extend(children_2)
                        offset_1 = offset_2
                        line_start_1 = line_start_2
                        count_1 += 1
                    if offset_1 == -1:
                        break

                    count_1 = 0
                    while offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in ' \t\r\n\ufeff':
                            offset_1 +=1
                            count_1 +=1
                        else:
                            break

                    break
                if offset_1 == -1:
                    break
                if offset_0 == offset_1: break
                children_0.extend(children_1)
                offset_0 = offset_1
                line_start_0 = line_start_1
                count_0 += 1
            if offset_0 == -1:
                break

            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t\r\n\ufeff':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break


            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = []
                    while True:
                        offset_2, line_start_1 = self.parse_rson_value(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                        if offset_2 == -1: break


                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True:
                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n\ufeff':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if buf[offset_4:offset_4+1] == '#':
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
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

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            children_4.extend(children_5)
                                            offset_4 = offset_5
                                            line_start_3 = line_start_4
                                            count_3 += 1
                                        if offset_4 == -1:
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t\r\n\ufeff':
                                                offset_4 +=1
                                                count_3 +=1
                                            else:
                                                break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n\ufeff':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break


                                if buf[offset_3:offset_3+1] == ',':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n\ufeff':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if buf[offset_4:offset_4+1] == '#':
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
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

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            children_4.extend(children_5)
                                            offset_4 = offset_5
                                            line_start_3 = line_start_4
                                            count_3 += 1
                                        if offset_4 == -1:
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t\r\n\ufeff':
                                                offset_4 +=1
                                                count_3 +=1
                                            else:
                                                break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n\ufeff':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break


                                offset_3, line_start_2 = self.parse_rson_value(buf, offset_3, line_start_2, prefix_0, buf_eof, children_3)
                                if offset_3 == -1: break


                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count_1 += 1
                        if offset_2 == -1:
                            break

                        count_1 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t\r\n\ufeff':
                                offset_2 +=1
                                count_1 +=1
                            else:
                                break

                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True:
                                if buf[offset_3:offset_3+1] == '#':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if chr == 10:
                                            offset_4 = -1
                                            break
                                        else:
                                            offset_4 += 1

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n\ufeff':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break

                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count_1 += 1
                        if offset_2 == -1:
                            break

                        count_1 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t\r\n\ufeff':
                                offset_2 +=1
                                count_1 +=1
                            else:
                                break


                        count_1 = 0
                        while count_1 < 1:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True:
                                if buf[offset_3:offset_3+1] == ',':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n\ufeff':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if buf[offset_4:offset_4+1] == '#':
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
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

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            children_4.extend(children_5)
                                            offset_4 = offset_5
                                            line_start_3 = line_start_4
                                            count_3 += 1
                                        if offset_4 == -1:
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t\r\n\ufeff':
                                                offset_4 +=1
                                                count_3 +=1
                                            else:
                                                break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n\ufeff':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break


                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count_1 += 1
                            break
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        break
                    if offset_1 == offset_2: break
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
                value_0 = self.Node('list', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1

            if buf[offset_0:offset_0+1] == ']':
                offset_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, line_start_0

    def parse_rson_object(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            if buf[offset_0:offset_0+1] == '{':
                offset_0 += 1
            else:
                offset_0 = -1
                break

            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t\r\n\ufeff':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break

            count_0 = 0
            while True:
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True:
                    if buf[offset_1:offset_1+1] == '#':
                        offset_1 += 1
                    else:
                        offset_1 = -1
                        break

                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        line_start_2 = line_start_1
                        children_2 = []
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

                            break
                        if offset_2 == -1:
                            break
                        if offset_1 == offset_2: break
                        children_1.extend(children_2)
                        offset_1 = offset_2
                        line_start_1 = line_start_2
                        count_1 += 1
                    if offset_1 == -1:
                        break

                    count_1 = 0
                    while offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in ' \t\r\n\ufeff':
                            offset_1 +=1
                            count_1 +=1
                        else:
                            break

                    break
                if offset_1 == -1:
                    break
                if offset_0 == offset_1: break
                children_0.extend(children_1)
                offset_0 = offset_1
                line_start_0 = line_start_1
                count_0 += 1
            if offset_0 == -1:
                break

            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t\r\n\ufeff':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break


            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while count_0 < 1:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = []
                    while True:
                        offset_3 = offset_2
                        children_3 = []
                        while True: # start capture
                            offset_3, line_start_1 = self.parse_rson_string(buf, offset_3, line_start_1, prefix_0, buf_eof, children_3)
                            if offset_3 == -1: break


                            count_1 = 0
                            while offset_3 < buf_eof:
                                chr = buf[offset_3]
                                if chr in ' \t\r\n\ufeff':
                                    offset_3 +=1
                                    count_1 +=1
                                else:
                                    break

                            count_1 = 0
                            while True:
                                offset_4 = offset_3
                                line_start_2 = line_start_1
                                children_4 = []
                                while True:
                                    if buf[offset_4:offset_4+1] == '#':
                                        offset_4 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    count_2 = 0
                                    while True:
                                        offset_5 = offset_4
                                        line_start_3 = line_start_2
                                        children_5 = []
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

                                            break
                                        if offset_5 == -1:
                                            break
                                        if offset_4 == offset_5: break
                                        children_4.extend(children_5)
                                        offset_4 = offset_5
                                        line_start_2 = line_start_3
                                        count_2 += 1
                                    if offset_4 == -1:
                                        break

                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        chr = buf[offset_4]
                                        if chr in ' \t\r\n\ufeff':
                                            offset_4 +=1
                                            count_2 +=1
                                        else:
                                            break

                                    break
                                if offset_4 == -1:
                                    break
                                if offset_3 == offset_4: break
                                children_3.extend(children_4)
                                offset_3 = offset_4
                                line_start_1 = line_start_2
                                count_1 += 1
                            if offset_3 == -1:
                                break

                            count_1 = 0
                            while offset_3 < buf_eof:
                                chr = buf[offset_3]
                                if chr in ' \t\r\n\ufeff':
                                    offset_3 +=1
                                    count_1 +=1
                                else:
                                    break


                            if buf[offset_3:offset_3+1] == ':':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break

                            count_1 = 0
                            while offset_3 < buf_eof:
                                chr = buf[offset_3]
                                if chr in ' \t\r\n\ufeff':
                                    offset_3 +=1
                                    count_1 +=1
                                else:
                                    break

                            count_1 = 0
                            while True:
                                offset_4 = offset_3
                                line_start_2 = line_start_1
                                children_4 = []
                                while True:
                                    if buf[offset_4:offset_4+1] == '#':
                                        offset_4 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    count_2 = 0
                                    while True:
                                        offset_5 = offset_4
                                        line_start_3 = line_start_2
                                        children_5 = []
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

                                            break
                                        if offset_5 == -1:
                                            break
                                        if offset_4 == offset_5: break
                                        children_4.extend(children_5)
                                        offset_4 = offset_5
                                        line_start_2 = line_start_3
                                        count_2 += 1
                                    if offset_4 == -1:
                                        break

                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        chr = buf[offset_4]
                                        if chr in ' \t\r\n\ufeff':
                                            offset_4 +=1
                                            count_2 +=1
                                        else:
                                            break

                                    break
                                if offset_4 == -1:
                                    break
                                if offset_3 == offset_4: break
                                children_3.extend(children_4)
                                offset_3 = offset_4
                                line_start_1 = line_start_2
                                count_1 += 1
                            if offset_3 == -1:
                                break

                            count_1 = 0
                            while offset_3 < buf_eof:
                                chr = buf[offset_3]
                                if chr in ' \t\r\n\ufeff':
                                    offset_3 +=1
                                    count_1 +=1
                                else:
                                    break


                            offset_3, line_start_1 = self.parse_rson_value(buf, offset_3, line_start_1, prefix_0, buf_eof, children_3)
                            if offset_3 == -1: break


                            break
                        if offset_3 == -1:
                            offset_2 = -1
                            break
                        if self.builder is not None:
                            value_0 = self.builder['pair'](buf, offset_2, offset_3, children_3)
                        else:
                            value_0 = self.Node('pair', offset_2, offset_3, list(children_3), None)
                        children_2.append(value_0)
                        offset_2 = offset_3

                        count_1 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t\r\n\ufeff':
                                offset_2 +=1
                                count_1 +=1
                            else:
                                break

                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True:
                                if buf[offset_3:offset_3+1] == '#':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if offset_4 == buf_eof:
                                            offset_4 = -1
                                            break

                                        chr = ord(buf[offset_4])

                                        if chr == 10:
                                            offset_4 = -1
                                            break
                                        else:
                                            offset_4 += 1

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n\ufeff':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break

                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count_1 += 1
                        if offset_2 == -1:
                            break

                        count_1 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t\r\n\ufeff':
                                offset_2 +=1
                                count_1 +=1
                            else:
                                break


                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True:
                                if buf[offset_3:offset_3+1] == ',':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n\ufeff':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if buf[offset_4:offset_4+1] == '#':
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
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

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            children_4.extend(children_5)
                                            offset_4 = offset_5
                                            line_start_3 = line_start_4
                                            count_3 += 1
                                        if offset_4 == -1:
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t\r\n\ufeff':
                                                offset_4 +=1
                                                count_3 +=1
                                            else:
                                                break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n\ufeff':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break


                                offset_4 = offset_3
                                children_4 = []
                                while True: # start capture
                                    offset_4, line_start_2 = self.parse_rson_string(buf, offset_4, line_start_2, prefix_0, buf_eof, children_4)
                                    if offset_4 == -1: break


                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        chr = buf[offset_4]
                                        if chr in ' \t\r\n\ufeff':
                                            offset_4 +=1
                                            count_2 +=1
                                        else:
                                            break

                                    count_2 = 0
                                    while True:
                                        offset_5 = offset_4
                                        line_start_3 = line_start_2
                                        children_5 = []
                                        while True:
                                            if buf[offset_5:offset_5+1] == '#':
                                                offset_5 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            count_3 = 0
                                            while True:
                                                offset_6 = offset_5
                                                line_start_4 = line_start_3
                                                children_6 = []
                                                while True:
                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    chr = ord(buf[offset_6])

                                                    if chr == 10:
                                                        offset_6 = -1
                                                        break
                                                    else:
                                                        offset_6 += 1

                                                    break
                                                if offset_6 == -1:
                                                    break
                                                if offset_5 == offset_6: break
                                                children_5.extend(children_6)
                                                offset_5 = offset_6
                                                line_start_3 = line_start_4
                                                count_3 += 1
                                            if offset_5 == -1:
                                                break

                                            count_3 = 0
                                            while offset_5 < buf_eof:
                                                chr = buf[offset_5]
                                                if chr in ' \t\r\n\ufeff':
                                                    offset_5 +=1
                                                    count_3 +=1
                                                else:
                                                    break

                                            break
                                        if offset_5 == -1:
                                            break
                                        if offset_4 == offset_5: break
                                        children_4.extend(children_5)
                                        offset_4 = offset_5
                                        line_start_2 = line_start_3
                                        count_2 += 1
                                    if offset_4 == -1:
                                        break

                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        chr = buf[offset_4]
                                        if chr in ' \t\r\n\ufeff':
                                            offset_4 +=1
                                            count_2 +=1
                                        else:
                                            break


                                    if buf[offset_4:offset_4+1] == ':':
                                        offset_4 += 1
                                    else:
                                        offset_4 = -1
                                        break

                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        chr = buf[offset_4]
                                        if chr in ' \t\r\n\ufeff':
                                            offset_4 +=1
                                            count_2 +=1
                                        else:
                                            break

                                    count_2 = 0
                                    while True:
                                        offset_5 = offset_4
                                        line_start_3 = line_start_2
                                        children_5 = []
                                        while True:
                                            if buf[offset_5:offset_5+1] == '#':
                                                offset_5 += 1
                                            else:
                                                offset_5 = -1
                                                break

                                            count_3 = 0
                                            while True:
                                                offset_6 = offset_5
                                                line_start_4 = line_start_3
                                                children_6 = []
                                                while True:
                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break

                                                    chr = ord(buf[offset_6])

                                                    if chr == 10:
                                                        offset_6 = -1
                                                        break
                                                    else:
                                                        offset_6 += 1

                                                    break
                                                if offset_6 == -1:
                                                    break
                                                if offset_5 == offset_6: break
                                                children_5.extend(children_6)
                                                offset_5 = offset_6
                                                line_start_3 = line_start_4
                                                count_3 += 1
                                            if offset_5 == -1:
                                                break

                                            count_3 = 0
                                            while offset_5 < buf_eof:
                                                chr = buf[offset_5]
                                                if chr in ' \t\r\n\ufeff':
                                                    offset_5 +=1
                                                    count_3 +=1
                                                else:
                                                    break

                                            break
                                        if offset_5 == -1:
                                            break
                                        if offset_4 == offset_5: break
                                        children_4.extend(children_5)
                                        offset_4 = offset_5
                                        line_start_2 = line_start_3
                                        count_2 += 1
                                    if offset_4 == -1:
                                        break

                                    count_2 = 0
                                    while offset_4 < buf_eof:
                                        chr = buf[offset_4]
                                        if chr in ' \t\r\n\ufeff':
                                            offset_4 +=1
                                            count_2 +=1
                                        else:
                                            break


                                    offset_4, line_start_2 = self.parse_rson_value(buf, offset_4, line_start_2, prefix_0, buf_eof, children_4)
                                    if offset_4 == -1: break


                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                if self.builder is not None:
                                    value_1 = self.builder['pair'](buf, offset_3, offset_4, children_4)
                                else:
                                    value_1 = self.Node('pair', offset_3, offset_4, list(children_4), None)
                                children_3.append(value_1)
                                offset_3 = offset_4

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n\ufeff':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if buf[offset_4:offset_4+1] == '#':
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
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

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            children_4.extend(children_5)
                                            offset_4 = offset_5
                                            line_start_3 = line_start_4
                                            count_3 += 1
                                        if offset_4 == -1:
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t\r\n\ufeff':
                                                offset_4 +=1
                                                count_3 +=1
                                            else:
                                                break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n\ufeff':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break


                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count_1 += 1
                        if offset_2 == -1:
                            break

                        count_1 = 0
                        while count_1 < 1:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True:
                                if buf[offset_3:offset_3+1] == ',':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n\ufeff':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break

                                count_2 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if buf[offset_4:offset_4+1] == '#':
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break

                                        count_3 = 0
                                        while True:
                                            offset_5 = offset_4
                                            line_start_4 = line_start_3
                                            children_5 = []
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

                                                break
                                            if offset_5 == -1:
                                                break
                                            if offset_4 == offset_5: break
                                            children_4.extend(children_5)
                                            offset_4 = offset_5
                                            line_start_3 = line_start_4
                                            count_3 += 1
                                        if offset_4 == -1:
                                            break

                                        count_3 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t\r\n\ufeff':
                                                offset_4 +=1
                                                count_3 +=1
                                            else:
                                                break

                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_2 += 1
                                if offset_3 == -1:
                                    break

                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t\r\n\ufeff':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break


                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count_1 += 1
                            break
                        if offset_2 == -1:
                            break

                        break
                    if offset_2 == -1:
                        break
                    if offset_1 == offset_2: break
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
                value_2 = self.builder['object'](buf, offset_0, offset_1, children_1)
            else:
                value_2 = self.Node('object', offset_0, offset_1, list(children_1), None)
            children_0.append(value_2)
            offset_0 = offset_1

            if buf[offset_0:offset_0+1] == '}':
                offset_0 += 1
            else:
                offset_0 = -1
                break


            break
        return offset_0, line_start_0
