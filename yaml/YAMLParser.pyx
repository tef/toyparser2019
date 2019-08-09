# cython: language_level=3, bounds_check=False
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


cdef class Parser:
    cpdef object builder, tabstop, cache, allow_mixed_indent 

    def __init__(self, builder=None, tabstop=None, allow_mixed_indent=True):
         self.builder = builder
         self.tabstop = tabstop or self.TABSTOP
         self.cache = None
         self.allow_mixed_indent = allow_mixed_indent

    NEWLINE = ('\n', '\r', '\r\n')
    WHITESPACE = (' ', '\t')
    TABSTOP = 8

    def parse(self, buf, offset=0, end=None, err=None):
        self.cache = dict()
        end = len(buf) if end is None else end
        line_start, prefix, eof, children = offset, [], end, []
        new_offset, line_start = self.parse_document(buf, offset, line_start, prefix, eof, children)
        if children and new_offset == end: return children[-1]
        print('no', offset, new_offset, end, buf[new_offset:])
        if err is not None: raise err(buf, new_offset, 'no')
    
    cdef (int, int) parse_literal(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_list_literal(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_object_literal(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                                        if buf[offset_4:offset_4+2] == '\\u':
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
                        value_0 = Node('string', offset_1, offset_2, list(children_2), None)
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
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        count_0 = 0
                        while count_0 < 1:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True:
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break
                                
                                chr = ord(buf[offset_3])
                                
                                if chr == 45:
                                    offset_3 += 1
                                elif chr == 43:
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break
                                
                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count_0 += 1
                            break
                        if offset_2 == -1:
                            break
                        
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True:
                                if offset_3 == buf_eof:
                                    offset_3 = -1
                                    break
                                
                                chr = ord(buf[offset_3])
                                
                                if 48 <= chr <= 57:
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break
                                
                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count_0 += 1
                        if count_0 < 1:
                            offset_2 = -1
                            break
                        if offset_2 == -1:
                            break
                        
                        count_0 = 0
                        while count_0 < 1:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True:
                                if buf[offset_3:offset_3+1] == '.':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break
                                
                                count_1 = 0
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
                                    count_1 += 1
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
                            break
                        if offset_2 == -1:
                            break
                        
                        count_0 = 0
                        while count_0 < 1:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True:
                                if buf[offset_3:offset_3+1] == 'e':
                                    offset_3 += 1
                                elif buf[offset_3:offset_3+1] == 'E':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break
                                
                                count_1 = 0
                                while count_1 < 1:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if buf[offset_4:offset_4+1] == '+':
                                            offset_4 += 1
                                        elif buf[offset_4:offset_4+1] == '-':
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break
                                        
                                        count_2 = 0
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
                                            count_2 += 1
                                        if offset_4 == -1:
                                            break
                                        
                                        break
                                    if offset_4 == -1:
                                        break
                                    if offset_3 == offset_4: break
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
                        value_1 = Node('number', offset_1, offset_2, list(children_2), None)
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
                        value_2 = self.builder['bool'](buf, offset_1, offset_2, children_2)
                    else:
                        value_2 = Node('bool', offset_1, offset_2, list(children_2), None)
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
                        value_3 = self.builder['bool'](buf, offset_1, offset_2, children_2)
                    else:
                        value_3 = Node('bool', offset_1, offset_2, list(children_2), None)
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
                        value_4 = self.builder['null'](buf, offset_1, offset_2, children_2)
                    else:
                        value_4 = Node('null', offset_1, offset_2, list(children_2), None)
                    children_1.append(value_4)
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
    
    cdef (int, int) parse_list_literal(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            if buf[offset_0:offset_0+1] == '[':
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
                elif chr in '\n\r':
                    offset_0 +=1
                    line_start_0 = offset_0
                    count_0 +=1
                elif chr in ' \t':
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
                        offset_2, line_start_1 = self.parse_literal(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
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
                                    if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        line_start_2 = offset_3
                                    elif chr in '\n\r':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                        count_2 +=1
                                    elif chr in ' \t':
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
                                    if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        line_start_2 = offset_3
                                    elif chr in '\n\r':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                        count_2 +=1
                                    elif chr in ' \t':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break
                                
                                offset_3, line_start_2 = self.parse_literal(buf, offset_3, line_start_2, prefix_0, buf_eof, children_3)
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
                            if chr == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                offset_2 +=2
                                line_start_1 = offset_2
                            elif chr in '\n\r':
                                offset_2 +=1
                                line_start_1 = offset_2
                                count_1 +=1
                            elif chr in ' \t':
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
                                    if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        line_start_2 = offset_3
                                    elif chr in '\n\r':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                        count_2 +=1
                                    elif chr in ' \t':
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
                value_0 = Node('list', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            if buf[offset_0:offset_0+1] == ']':
                offset_0 += 1
            else:
                offset_0 = -1
                break
            
            
            break
        return offset_0, line_start_0
    
    cdef (int, int) parse_object_literal(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            if buf[offset_0:offset_0+1] == '{':
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
                elif chr in '\n\r':
                    offset_0 +=1
                    line_start_0 = offset_0
                    count_0 +=1
                elif chr in ' \t':
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
                        if buf[offset_2:offset_2+1] == '"':
                            offset_2 += 1
                        else:
                            offset_2 = -1
                            break
                        
                        offset_3 = offset_2
                        children_3 = []
                        while True: # start capture
                            count_1 = 0
                            while True:
                                offset_4 = offset_3
                                line_start_2 = line_start_1
                                children_4 = []
                                while True:
                                    while True: # start choice
                                        offset_5 = offset_4
                                        line_start_3 = line_start_2
                                        children_5 = []
                                        while True: # case
                                            if buf[offset_5:offset_5+2] == '\\u':
                                                offset_5 += 2
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
                                            line_start_2 = line_start_3
                                            children_4.extend(children_5)
                                            break
                                        # end case
                                        offset_5 = offset_4
                                        line_start_3 = line_start_2
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
                                            else:
                                                offset_5 = -1
                                                break
                                            
                                            
                                            break
                                        if offset_5 != -1:
                                            offset_4 = offset_5
                                            line_start_2 = line_start_3
                                            children_4.extend(children_5)
                                            break
                                        # end case
                                        offset_5 = offset_4
                                        line_start_3 = line_start_2
                                        children_5 = []
                                        while True: # case
                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break
                                            
                                            chr = ord(buf[offset_5])
                                            
                                            if chr == 92:
                                                offset_5 = -1
                                                break
                                            elif chr == 34:
                                                offset_5 = -1
                                                break
                                            else:
                                                offset_5 += 1
                                            
                                            
                                            break
                                        if offset_5 != -1:
                                            offset_4 = offset_5
                                            line_start_2 = line_start_3
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
                                line_start_1 = line_start_2
                                count_1 += 1
                            if offset_3 == -1:
                                break
                            
                            break
                        if offset_3 == -1:
                            offset_2 = -1
                            break
                        if self.builder is not None:
                            value_0 = self.builder['string'](buf, offset_2, offset_3, children_3)
                        else:
                            value_0 = Node('string', offset_2, offset_3, list(children_3), None)
                        children_2.append(value_0)
                        offset_2 = offset_3
                        
                        if buf[offset_2:offset_2+1] == '"':
                            offset_2 += 1
                        else:
                            offset_2 = -1
                            break
                        
                        
                        count_1 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t':
                                offset_2 +=1
                                count_1 +=1
                            else:
                                break
                        
                        if buf[offset_2:offset_2+1] == ':':
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
                            elif chr in '\n\r':
                                offset_2 +=1
                                line_start_1 = offset_2
                                count_1 +=1
                            elif chr in ' \t':
                                offset_2 +=1
                                count_1 +=1
                            else:
                                break
                        
                        offset_2, line_start_1 = self.parse_literal(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
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
                                    if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        line_start_2 = offset_3
                                    elif chr in '\n\r':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                        count_2 +=1
                                    elif chr in ' \t':
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
                                    if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        line_start_2 = offset_3
                                    elif chr in '\n\r':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                        count_2 +=1
                                    elif chr in ' \t':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break
                                
                                if buf[offset_3:offset_3+1] == '"':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break
                                
                                offset_4 = offset_3
                                children_4 = []
                                while True: # start capture
                                    count_2 = 0
                                    while True:
                                        offset_5 = offset_4
                                        line_start_3 = line_start_2
                                        children_5 = []
                                        while True:
                                            while True: # start choice
                                                offset_6 = offset_5
                                                line_start_4 = line_start_3
                                                children_6 = []
                                                while True: # case
                                                    if buf[offset_6:offset_6+2] == '\\u':
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
                                                    line_start_3 = line_start_4
                                                    children_5.extend(children_6)
                                                    break
                                                # end case
                                                offset_6 = offset_5
                                                line_start_4 = line_start_3
                                                children_6 = []
                                                while True: # case
                                                    if buf[offset_6:offset_6+1] == '\\':
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
                                                    line_start_3 = line_start_4
                                                    children_5.extend(children_6)
                                                    break
                                                # end case
                                                offset_6 = offset_5
                                                line_start_4 = line_start_3
                                                children_6 = []
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
                                                    line_start_3 = line_start_4
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
                                        children_4.extend(children_5)
                                        offset_4 = offset_5
                                        line_start_2 = line_start_3
                                        count_2 += 1
                                    if offset_4 == -1:
                                        break
                                    
                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                if self.builder is not None:
                                    value_1 = self.builder['string'](buf, offset_3, offset_4, children_4)
                                else:
                                    value_1 = Node('string', offset_3, offset_4, list(children_4), None)
                                children_3.append(value_1)
                                offset_3 = offset_4
                                
                                if buf[offset_3:offset_3+1] == '"':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break
                                
                                
                                count_2 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break
                                
                                if buf[offset_3:offset_3+1] == ':':
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
                                    elif chr in '\n\r':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                        count_2 +=1
                                    elif chr in ' \t':
                                        offset_3 +=1
                                        count_2 +=1
                                    else:
                                        break
                                
                                offset_3, line_start_2 = self.parse_literal(buf, offset_3, line_start_2, prefix_0, buf_eof, children_3)
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
                            if chr == '\r' and offset_2 + 1 < buf_eof and buf[offset_2+1] == '\n':
                                offset_2 +=2
                                line_start_1 = offset_2
                            elif chr in '\n\r':
                                offset_2 +=1
                                line_start_1 = offset_2
                                count_1 +=1
                            elif chr in ' \t':
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
                                    if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                        offset_3 +=2
                                        line_start_2 = offset_3
                                    elif chr in '\n\r':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                        count_2 +=1
                                    elif chr in ' \t':
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
                value_1 = self.builder['object'](buf, offset_0, offset_1, children_1)
            else:
                value_1 = Node('object', offset_0, offset_1, list(children_1), None)
            children_0.append(value_1)
            offset_0 = offset_1
            
            if buf[offset_0:offset_0+1] == '}':
                offset_0 += 1
            else:
                offset_0 = -1
                break
            
            
            break
        return offset_0, line_start_0
    
    cdef (int, int) parse_indented_list(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            count_0 = offset_0 - line_start_0+  ((self.tabstop -1) * buf[line_start_0:offset_0].count('	'))
            def _indent(buf, offset, line_start, prefix, buf_eof, children, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
                saw_tab, saw_not_tab = False, False
                while count > 0 and offset < buf_eof:
                    chr = buf[offset]
                    if chr in ' \t':
                        offset +=1
                        count -= self.tabstop if chr == 9 else 1
                        if not allow_mixed_indent:
                            if chr == 9: saw_tab = True
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
                return offset, line_start
            prefix_0.append(_indent)
            line_start_0 = offset_0
            while True:
                offset_1 = offset_0
                children_1 = []
                while True: # start capture
                    if buf[offset_1:offset_1+1] == '-':
                        offset_1 += 1
                    else:
                        offset_1 = -1
                        break
                    
                    while True: # start choice
                        offset_2 = offset_1
                        line_start_1 = line_start_0
                        children_2 = []
                        while True: # case
                            count_0 = 0
                            while offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr in ' \t':
                                    offset_2 +=1
                                    count_0 +=1
                                else:
                                    break
                            
                            offset_2, line_start_1 = self.parse_indented_value(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                            if offset_2 == -1: break
                            
                            
                            
                            break
                        if offset_2 != -1:
                            offset_1 = offset_2
                            line_start_0 = line_start_1
                            children_1.extend(children_2)
                            break
                        # end case
                        offset_2 = offset_1
                        line_start_1 = line_start_0
                        children_2 = []
                        while True: # case
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
                                            count_1 = 0
                                            while offset_4 < buf_eof:
                                                chr = buf[offset_4]
                                                if chr in ' \t':
                                                    offset_4 +=1
                                                    count_1 +=1
                                                else:
                                                    break
                                            
                                            if offset_4 < buf_eof:
                                                chr = buf[offset_4]
                                                if chr == '\r' and offset_4 + 1 < buf_eof and buf[offset_4+1] == '\n':
                                                    offset_4 +=2
                                                    line_start_3 = offset_4
                                                elif chr in '\n\r':
                                                    offset_4 +=1
                                                    line_start_3 = offset_4
                                                else:
                                                    offset_4 = -1
                                                    break
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
                                            count_1 = 0
                                            while offset_4 < buf_eof:
                                                chr = buf[offset_4]
                                                if chr in ' \t':
                                                    offset_4 +=1
                                                    count_1 +=1
                                                else:
                                                    break
                                            
                                            if buf[offset_4:offset_4+1] == '#':
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
                                                count_1 += 1
                                            if offset_4 == -1:
                                                break
                                            
                                            if offset_4 < buf_eof:
                                                chr = buf[offset_4]
                                                if chr == '\r' and offset_4 + 1 < buf_eof and buf[offset_4+1] == '\n':
                                                    offset_4 +=2
                                                    line_start_3 = offset_4
                                                elif chr in '\n\r':
                                                    offset_4 +=1
                                                    line_start_3 = offset_4
                                                else:
                                                    offset_4 = -1
                                                    break
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
                            
                            if offset_2 != line_start_1:
                                offset_2 = -1
                                break
                            for indent in prefix_0:
                                _children, _prefix = [], []
                                offset_2, line_start_1 = indent(buf, offset_2, line_start_1, _prefix, buf_eof, _children)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_2 == -1:        break
                                line_start_1 = offset_2
                            if offset_2 == -1:
                                break
                            
                            count_0 = 0
                            while offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr in ' \t':
                                    offset_2 +=1
                                    count_0 +=1
                                else:
                                    break
                            if count_0 < 1:
                                offset_2 = -1
                                break
                            
                            offset_2, line_start_1 = self.parse_indented_value(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                            if offset_2 == -1: break
                            
                            
                            
                            break
                        if offset_2 != -1:
                            offset_1 = offset_2
                            line_start_0 = line_start_1
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
                        children_2 = []
                        while True:
                            count_1 = 0
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
                                            count_2 = 0
                                            while offset_4 < buf_eof:
                                                chr = buf[offset_4]
                                                if chr in ' \t':
                                                    offset_4 +=1
                                                    count_2 +=1
                                                else:
                                                    break
                                            
                                            if offset_4 < buf_eof:
                                                chr = buf[offset_4]
                                                if chr == '\r' and offset_4 + 1 < buf_eof and buf[offset_4+1] == '\n':
                                                    offset_4 +=2
                                                    line_start_3 = offset_4
                                                elif chr in '\n\r':
                                                    offset_4 +=1
                                                    line_start_3 = offset_4
                                                else:
                                                    offset_4 = -1
                                                    break
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
                                            count_2 = 0
                                            while offset_4 < buf_eof:
                                                chr = buf[offset_4]
                                                if chr in ' \t':
                                                    offset_4 +=1
                                                    count_2 +=1
                                                else:
                                                    break
                                            
                                            if buf[offset_4:offset_4+1] == '#':
                                                offset_4 += 1
                                            else:
                                                offset_4 = -1
                                                break
                                            
                                            count_2 = 0
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
                                                count_2 += 1
                                            if offset_4 == -1:
                                                break
                                            
                                            if offset_4 < buf_eof:
                                                chr = buf[offset_4]
                                                if chr == '\r' and offset_4 + 1 < buf_eof and buf[offset_4+1] == '\n':
                                                    offset_4 +=2
                                                    line_start_3 = offset_4
                                                elif chr in '\n\r':
                                                    offset_4 +=1
                                                    line_start_3 = offset_4
                                                else:
                                                    offset_4 = -1
                                                    break
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
                                count_1 += 1
                            if offset_2 == -1:
                                break
                            
                            if offset_2 != line_start_1:
                                offset_2 = -1
                                break
                            for indent in prefix_0:
                                _children, _prefix = [], []
                                offset_2, line_start_1 = indent(buf, offset_2, line_start_1, _prefix, buf_eof, _children)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_2 == -1:        break
                                line_start_1 = offset_2
                            if offset_2 == -1:
                                break
                            
                            if buf[offset_2:offset_2+1] == '-':
                                offset_2 += 1
                            else:
                                offset_2 = -1
                                break
                            
                            count_1 = 0
                            while offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr in ' \t':
                                    offset_2 +=1
                                    count_1 +=1
                                else:
                                    break
                            if count_1 < 1:
                                offset_2 = -1
                                break
                            
                            while True: # start choice
                                offset_3 = offset_2
                                line_start_2 = line_start_1
                                children_3 = []
                                while True: # case
                                    count_1 = 0
                                    while offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in ' \t':
                                            offset_3 +=1
                                            count_1 +=1
                                        else:
                                            break
                                    
                                    offset_3, line_start_2 = self.parse_indented_value(buf, offset_3, line_start_2, prefix_0, buf_eof, children_3)
                                    if offset_3 == -1: break
                                    
                                    
                                    
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
                                    count_1 = 0
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
                                                    count_2 = 0
                                                    while offset_5 < buf_eof:
                                                        chr = buf[offset_5]
                                                        if chr in ' \t':
                                                            offset_5 +=1
                                                            count_2 +=1
                                                        else:
                                                            break
                                                    
                                                    if offset_5 < buf_eof:
                                                        chr = buf[offset_5]
                                                        if chr == '\r' and offset_5 + 1 < buf_eof and buf[offset_5+1] == '\n':
                                                            offset_5 +=2
                                                            line_start_4 = offset_5
                                                        elif chr in '\n\r':
                                                            offset_5 +=1
                                                            line_start_4 = offset_5
                                                        else:
                                                            offset_5 = -1
                                                            break
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
                                                    count_2 = 0
                                                    while offset_5 < buf_eof:
                                                        chr = buf[offset_5]
                                                        if chr in ' \t':
                                                            offset_5 +=1
                                                            count_2 +=1
                                                        else:
                                                            break
                                                    
                                                    if buf[offset_5:offset_5+1] == '#':
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
                                                        line_start_4 = line_start_5
                                                        count_2 += 1
                                                    if offset_5 == -1:
                                                        break
                                                    
                                                    if offset_5 < buf_eof:
                                                        chr = buf[offset_5]
                                                        if chr == '\r' and offset_5 + 1 < buf_eof and buf[offset_5+1] == '\n':
                                                            offset_5 +=2
                                                            line_start_4 = offset_5
                                                        elif chr in '\n\r':
                                                            offset_5 +=1
                                                            line_start_4 = offset_5
                                                        else:
                                                            offset_5 = -1
                                                            break
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
                                        count_1 += 1
                                    if offset_3 == -1:
                                        break
                                    
                                    if offset_3 != line_start_2:
                                        offset_3 = -1
                                        break
                                    for indent in prefix_0:
                                        _children, _prefix = [], []
                                        offset_3, line_start_2 = indent(buf, offset_3, line_start_2, _prefix, buf_eof, _children)
                                        if _prefix or _children:
                                           raise Exception('bar')
                                        if offset_3 == -1:        break
                                        line_start_2 = offset_3
                                    if offset_3 == -1:
                                        break
                                    
                                    count_1 = 0
                                    while offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in ' \t':
                                            offset_3 +=1
                                            count_1 +=1
                                        else:
                                            break
                                    
                                    offset_3, line_start_2 = self.parse_indented_value(buf, offset_3, line_start_2, prefix_0, buf_eof, children_3)
                                    if offset_3 == -1: break
                                    
                                    
                                    
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
                            break
                        if offset_1 == offset_2: break
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
                    value_0 = self.builder['list'](buf, offset_0, offset_1, children_1)
                else:
                    value_0 = Node('list', offset_0, offset_1, list(children_1), None)
                children_0.append(value_0)
                offset_0 = offset_1
                
                break
            prefix_0.pop()
            if offset_0 == -1: break
            
            break
        return offset_0, line_start_0
    
    cdef (int, int) parse_indented_object(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            count_0 = offset_0 - line_start_0+  ((self.tabstop -1) * buf[line_start_0:offset_0].count('	'))
            def _indent(buf, offset, line_start, prefix, buf_eof, children, count=count_0, allow_mixed_indent=self.allow_mixed_indent):
                saw_tab, saw_not_tab = False, False
                while count > 0 and offset < buf_eof:
                    chr = buf[offset]
                    if chr in ' \t':
                        offset +=1
                        count -= self.tabstop if chr == 9 else 1
                        if not allow_mixed_indent:
                            if chr == 9: saw_tab = True
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
                return offset, line_start
            prefix_0.append(_indent)
            line_start_0 = offset_0
            while True:
                offset_1 = offset_0
                children_1 = []
                while True: # start capture
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        while True: # start choice
                            offset_3 = offset_2
                            line_start_1 = line_start_0
                            children_3 = []
                            while True: # case
                                offset_4 = offset_3
                                children_4 = []
                                while True: # start capture
                                    count_0 = 0
                                    while True:
                                        offset_5 = offset_4
                                        line_start_2 = line_start_1
                                        children_5 = []
                                        while True:
                                            if offset_5 == buf_eof:
                                                offset_5 = -1
                                                break
                                            
                                            chr = ord(buf[offset_5])
                                            
                                            if 97 <= chr <= 122:
                                                offset_5 += 1
                                            elif 65 <= chr <= 90:
                                                offset_5 += 1
                                            elif chr == 95:
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
                                        line_start_1 = line_start_2
                                        count_0 += 1
                                    if count_0 < 1:
                                        offset_4 = -1
                                        break
                                    if offset_4 == -1:
                                        break
                                    
                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                if self.builder is not None:
                                    value_0 = self.builder['identifier'](buf, offset_3, offset_4, children_4)
                                else:
                                    value_0 = Node('identifier', offset_3, offset_4, list(children_4), None)
                                children_3.append(value_0)
                                offset_3 = offset_4
                                
                                
                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                line_start_0 = line_start_1
                                children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            line_start_1 = line_start_0
                            children_3 = []
                            while True: # case
                                if buf[offset_3:offset_3+1] == '"':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break
                                
                                offset_4 = offset_3
                                children_4 = []
                                while True: # start capture
                                    count_0 = 0
                                    while True:
                                        offset_5 = offset_4
                                        line_start_2 = line_start_1
                                        children_5 = []
                                        while True:
                                            while True: # start choice
                                                offset_6 = offset_5
                                                line_start_3 = line_start_2
                                                children_6 = []
                                                while True: # case
                                                    if buf[offset_6:offset_6+2] == '\\u':
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
                                                    children_5.extend(children_6)
                                                    break
                                                # end case
                                                offset_6 = offset_5
                                                line_start_3 = line_start_2
                                                children_6 = []
                                                while True: # case
                                                    if buf[offset_6:offset_6+1] == '\\':
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
                                                    children_5.extend(children_6)
                                                    break
                                                # end case
                                                offset_6 = offset_5
                                                line_start_3 = line_start_2
                                                children_6 = []
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
                                        children_4.extend(children_5)
                                        offset_4 = offset_5
                                        line_start_1 = line_start_2
                                        count_0 += 1
                                    if offset_4 == -1:
                                        break
                                    
                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                if self.builder is not None:
                                    value_1 = self.builder['string'](buf, offset_3, offset_4, children_4)
                                else:
                                    value_1 = Node('string', offset_3, offset_4, list(children_4), None)
                                children_3.append(value_1)
                                offset_3 = offset_4
                                
                                if buf[offset_3:offset_3+1] == '"':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break
                                
                                
                                
                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                line_start_0 = line_start_1
                                children_2.extend(children_3)
                                break
                            # end case
                            offset_2 = -1 # no more choices
                            break # end choice
                        if offset_2 == -1:
                            break
                        
                        count_0 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t':
                                offset_2 +=1
                                count_0 +=1
                            else:
                                break
                        
                        if buf[offset_2:offset_2+1] == ':':
                            offset_2 += 1
                        else:
                            offset_2 = -1
                            break
                        
                        while True: # start choice
                            offset_3 = offset_2
                            line_start_1 = line_start_0
                            children_3 = []
                            while True: # case
                                count_0 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_2 = line_start_1
                                    children_4 = []
                                    while True:
                                        while True: # start choice
                                            offset_5 = offset_4
                                            line_start_3 = line_start_2
                                            children_5 = []
                                            while True: # case
                                                count_1 = 0
                                                while offset_5 < buf_eof:
                                                    chr = buf[offset_5]
                                                    if chr in ' \t':
                                                        offset_5 +=1
                                                        count_1 +=1
                                                    else:
                                                        break
                                                
                                                if offset_5 < buf_eof:
                                                    chr = buf[offset_5]
                                                    if chr == '\r' and offset_5 + 1 < buf_eof and buf[offset_5+1] == '\n':
                                                        offset_5 +=2
                                                        line_start_3 = offset_5
                                                    elif chr in '\n\r':
                                                        offset_5 +=1
                                                        line_start_3 = offset_5
                                                    else:
                                                        offset_5 = -1
                                                        break
                                                else:
                                                    offset_5 = -1
                                                    break
                                                
                                                
                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                line_start_2 = line_start_3
                                                children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            line_start_3 = line_start_2
                                            children_5 = []
                                            while True: # case
                                                count_1 = 0
                                                while offset_5 < buf_eof:
                                                    chr = buf[offset_5]
                                                    if chr in ' \t':
                                                        offset_5 +=1
                                                        count_1 +=1
                                                    else:
                                                        break
                                                
                                                if buf[offset_5:offset_5+1] == '#':
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break
                                                
                                                count_1 = 0
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
                                                    count_1 += 1
                                                if offset_5 == -1:
                                                    break
                                                
                                                if offset_5 < buf_eof:
                                                    chr = buf[offset_5]
                                                    if chr == '\r' and offset_5 + 1 < buf_eof and buf[offset_5+1] == '\n':
                                                        offset_5 +=2
                                                        line_start_3 = offset_5
                                                    elif chr in '\n\r':
                                                        offset_5 +=1
                                                        line_start_3 = offset_5
                                                    else:
                                                        offset_5 = -1
                                                        break
                                                else:
                                                    offset_5 = -1
                                                    break
                                                
                                                
                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                line_start_2 = line_start_3
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
                                    line_start_1 = line_start_2
                                    count_0 += 1
                                if offset_3 == -1:
                                    break
                                
                                if offset_3 != line_start_1:
                                    offset_3 = -1
                                    break
                                for indent in prefix_0:
                                    _children, _prefix = [], []
                                    offset_3, line_start_1 = indent(buf, offset_3, line_start_1, _prefix, buf_eof, _children)
                                    if _prefix or _children:
                                       raise Exception('bar')
                                    if offset_3 == -1:        break
                                    line_start_1 = offset_3
                                if offset_3 == -1:
                                    break
                                
                                count_0 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        offset_3 +=1
                                        count_0 +=1
                                    else:
                                        break
                                if count_0 < 1:
                                    offset_3 = -1
                                    break
                                
                                offset_3, line_start_1 = self.parse_indented_value(buf, offset_3, line_start_1, prefix_0, buf_eof, children_3)
                                if offset_3 == -1: break
                                
                                
                                
                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                line_start_0 = line_start_1
                                children_2.extend(children_3)
                                break
                            # end case
                            offset_3 = offset_2
                            line_start_1 = line_start_0
                            children_3 = []
                            while True: # case
                                count_0 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        offset_3 +=1
                                        count_0 +=1
                                    else:
                                        break
                                
                                offset_3, line_start_1 = self.parse_indented_value(buf, offset_3, line_start_1, prefix_0, buf_eof, children_3)
                                if offset_3 == -1: break
                                
                                
                                
                                break
                            if offset_3 != -1:
                                offset_2 = offset_3
                                line_start_0 = line_start_1
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
                        value_2 = self.builder['pair'](buf, offset_1, offset_2, children_2)
                    else:
                        value_2 = Node('pair', offset_1, offset_2, list(children_2), None)
                    children_1.append(value_2)
                    offset_1 = offset_2
                    
                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        line_start_1 = line_start_0
                        children_2 = []
                        while True:
                            offset_3 = offset_2
                            children_3 = []
                            while True: # start capture
                                count_1 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_2 = line_start_1
                                    children_4 = []
                                    while True:
                                        while True: # start choice
                                            offset_5 = offset_4
                                            line_start_3 = line_start_2
                                            children_5 = []
                                            while True: # case
                                                count_2 = 0
                                                while offset_5 < buf_eof:
                                                    chr = buf[offset_5]
                                                    if chr in ' \t':
                                                        offset_5 +=1
                                                        count_2 +=1
                                                    else:
                                                        break
                                                
                                                if offset_5 < buf_eof:
                                                    chr = buf[offset_5]
                                                    if chr == '\r' and offset_5 + 1 < buf_eof and buf[offset_5+1] == '\n':
                                                        offset_5 +=2
                                                        line_start_3 = offset_5
                                                    elif chr in '\n\r':
                                                        offset_5 +=1
                                                        line_start_3 = offset_5
                                                    else:
                                                        offset_5 = -1
                                                        break
                                                else:
                                                    offset_5 = -1
                                                    break
                                                
                                                
                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                line_start_2 = line_start_3
                                                children_4.extend(children_5)
                                                break
                                            # end case
                                            offset_5 = offset_4
                                            line_start_3 = line_start_2
                                            children_5 = []
                                            while True: # case
                                                count_2 = 0
                                                while offset_5 < buf_eof:
                                                    chr = buf[offset_5]
                                                    if chr in ' \t':
                                                        offset_5 +=1
                                                        count_2 +=1
                                                    else:
                                                        break
                                                
                                                if buf[offset_5:offset_5+1] == '#':
                                                    offset_5 += 1
                                                else:
                                                    offset_5 = -1
                                                    break
                                                
                                                count_2 = 0
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
                                                    count_2 += 1
                                                if offset_5 == -1:
                                                    break
                                                
                                                if offset_5 < buf_eof:
                                                    chr = buf[offset_5]
                                                    if chr == '\r' and offset_5 + 1 < buf_eof and buf[offset_5+1] == '\n':
                                                        offset_5 +=2
                                                        line_start_3 = offset_5
                                                    elif chr in '\n\r':
                                                        offset_5 +=1
                                                        line_start_3 = offset_5
                                                    else:
                                                        offset_5 = -1
                                                        break
                                                else:
                                                    offset_5 = -1
                                                    break
                                                
                                                
                                                break
                                            if offset_5 != -1:
                                                offset_4 = offset_5
                                                line_start_2 = line_start_3
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
                                    line_start_1 = line_start_2
                                    count_1 += 1
                                if offset_3 == -1:
                                    break
                                
                                if offset_3 != line_start_1:
                                    offset_3 = -1
                                    break
                                for indent in prefix_0:
                                    _children, _prefix = [], []
                                    offset_3, line_start_1 = indent(buf, offset_3, line_start_1, _prefix, buf_eof, _children)
                                    if _prefix or _children:
                                       raise Exception('bar')
                                    if offset_3 == -1:        break
                                    line_start_1 = offset_3
                                if offset_3 == -1:
                                    break
                                
                                while True: # start choice
                                    offset_4 = offset_3
                                    line_start_2 = line_start_1
                                    children_4 = []
                                    while True: # case
                                        offset_5 = offset_4
                                        children_5 = []
                                        while True: # start capture
                                            count_1 = 0
                                            while True:
                                                offset_6 = offset_5
                                                line_start_3 = line_start_2
                                                children_6 = []
                                                while True:
                                                    if offset_6 == buf_eof:
                                                        offset_6 = -1
                                                        break
                                                    
                                                    chr = ord(buf[offset_6])
                                                    
                                                    if 97 <= chr <= 122:
                                                        offset_6 += 1
                                                    elif 65 <= chr <= 90:
                                                        offset_6 += 1
                                                    elif chr == 95:
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
                                                line_start_2 = line_start_3
                                                count_1 += 1
                                            if count_1 < 1:
                                                offset_5 = -1
                                                break
                                            if offset_5 == -1:
                                                break
                                            
                                            break
                                        if offset_5 == -1:
                                            offset_4 = -1
                                            break
                                        if self.builder is not None:
                                            value_3 = self.builder['identifier'](buf, offset_4, offset_5, children_5)
                                        else:
                                            value_3 = Node('identifier', offset_4, offset_5, list(children_5), None)
                                        children_4.append(value_3)
                                        offset_4 = offset_5
                                        
                                        
                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_1 = line_start_2
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_2 = line_start_1
                                    children_4 = []
                                    while True: # case
                                        if buf[offset_4:offset_4+1] == '"':
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break
                                        
                                        offset_5 = offset_4
                                        children_5 = []
                                        while True: # start capture
                                            count_1 = 0
                                            while True:
                                                offset_6 = offset_5
                                                line_start_3 = line_start_2
                                                children_6 = []
                                                while True:
                                                    while True: # start choice
                                                        offset_7 = offset_6
                                                        line_start_4 = line_start_3
                                                        children_7 = []
                                                        while True: # case
                                                            if buf[offset_7:offset_7+2] == '\\u':
                                                                offset_7 += 2
                                                            else:
                                                                offset_7 = -1
                                                                break
                                                            
                                                            if offset_7 == buf_eof:
                                                                offset_7 = -1
                                                                break
                                                            
                                                            chr = ord(buf[offset_7])
                                                            
                                                            if 48 <= chr <= 57:
                                                                offset_7 += 1
                                                            elif 97 <= chr <= 102:
                                                                offset_7 += 1
                                                            elif 65 <= chr <= 70:
                                                                offset_7 += 1
                                                            else:
                                                                offset_7 = -1
                                                                break
                                                            
                                                            if offset_7 == buf_eof:
                                                                offset_7 = -1
                                                                break
                                                            
                                                            chr = ord(buf[offset_7])
                                                            
                                                            if 48 <= chr <= 57:
                                                                offset_7 += 1
                                                            elif 97 <= chr <= 102:
                                                                offset_7 += 1
                                                            elif 65 <= chr <= 70:
                                                                offset_7 += 1
                                                            else:
                                                                offset_7 = -1
                                                                break
                                                            
                                                            if offset_7 == buf_eof:
                                                                offset_7 = -1
                                                                break
                                                            
                                                            chr = ord(buf[offset_7])
                                                            
                                                            if 48 <= chr <= 57:
                                                                offset_7 += 1
                                                            elif 97 <= chr <= 102:
                                                                offset_7 += 1
                                                            elif 65 <= chr <= 70:
                                                                offset_7 += 1
                                                            else:
                                                                offset_7 = -1
                                                                break
                                                            
                                                            if offset_7 == buf_eof:
                                                                offset_7 = -1
                                                                break
                                                            
                                                            chr = ord(buf[offset_7])
                                                            
                                                            if 48 <= chr <= 57:
                                                                offset_7 += 1
                                                            elif 97 <= chr <= 102:
                                                                offset_7 += 1
                                                            elif 65 <= chr <= 70:
                                                                offset_7 += 1
                                                            else:
                                                                offset_7 = -1
                                                                break
                                                            
                                                            
                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            line_start_3 = line_start_4
                                                            children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_7 = offset_6
                                                        line_start_4 = line_start_3
                                                        children_7 = []
                                                        while True: # case
                                                            if buf[offset_7:offset_7+1] == '\\':
                                                                offset_7 += 1
                                                            else:
                                                                offset_7 = -1
                                                                break
                                                            
                                                            if offset_7 == buf_eof:
                                                                offset_7 = -1
                                                                break
                                                            
                                                            chr = ord(buf[offset_7])
                                                            
                                                            if chr == 34:
                                                                offset_7 += 1
                                                            elif chr == 92:
                                                                offset_7 += 1
                                                            elif chr == 47:
                                                                offset_7 += 1
                                                            elif chr == 98:
                                                                offset_7 += 1
                                                            elif chr == 102:
                                                                offset_7 += 1
                                                            elif chr == 110:
                                                                offset_7 += 1
                                                            elif chr == 114:
                                                                offset_7 += 1
                                                            elif chr == 116:
                                                                offset_7 += 1
                                                            else:
                                                                offset_7 = -1
                                                                break
                                                            
                                                            
                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            line_start_3 = line_start_4
                                                            children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_7 = offset_6
                                                        line_start_4 = line_start_3
                                                        children_7 = []
                                                        while True: # case
                                                            if offset_7 == buf_eof:
                                                                offset_7 = -1
                                                                break
                                                            
                                                            chr = ord(buf[offset_7])
                                                            
                                                            if chr == 92:
                                                                offset_7 = -1
                                                                break
                                                            elif chr == 34:
                                                                offset_7 = -1
                                                                break
                                                            else:
                                                                offset_7 += 1
                                                            
                                                            
                                                            break
                                                        if offset_7 != -1:
                                                            offset_6 = offset_7
                                                            line_start_3 = line_start_4
                                                            children_6.extend(children_7)
                                                            break
                                                        # end case
                                                        offset_6 = -1 # no more choices
                                                        break # end choice
                                                    if offset_6 == -1:
                                                        break
                                                    
                                                    break
                                                if offset_6 == -1:
                                                    break
                                                if offset_5 == offset_6: break
                                                children_5.extend(children_6)
                                                offset_5 = offset_6
                                                line_start_2 = line_start_3
                                                count_1 += 1
                                            if offset_5 == -1:
                                                break
                                            
                                            break
                                        if offset_5 == -1:
                                            offset_4 = -1
                                            break
                                        if self.builder is not None:
                                            value_3 = self.builder['string'](buf, offset_4, offset_5, children_5)
                                        else:
                                            value_3 = Node('string', offset_4, offset_5, list(children_5), None)
                                        children_4.append(value_3)
                                        offset_4 = offset_5
                                        
                                        if buf[offset_4:offset_4+1] == '"':
                                            offset_4 += 1
                                        else:
                                            offset_4 = -1
                                            break
                                        
                                        
                                        
                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_1 = line_start_2
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_3 = -1 # no more choices
                                    break # end choice
                                if offset_3 == -1:
                                    break
                                
                                count_1 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        offset_3 +=1
                                        count_1 +=1
                                    else:
                                        break
                                
                                if buf[offset_3:offset_3+1] == ':':
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
                                    children_4 = []
                                    while True: # case
                                        count_1 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t':
                                                offset_4 +=1
                                                count_1 +=1
                                            else:
                                                break
                                        
                                        offset_4, line_start_2 = self.parse_indented_value(buf, offset_4, line_start_2, prefix_0, buf_eof, children_4)
                                        if offset_4 == -1: break
                                        
                                        
                                        
                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_1 = line_start_2
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_2 = line_start_1
                                    children_4 = []
                                    while True: # case
                                        count_1 = 0
                                        while True:
                                            offset_5 = offset_4
                                            line_start_3 = line_start_2
                                            children_5 = []
                                            while True:
                                                while True: # start choice
                                                    offset_6 = offset_5
                                                    line_start_4 = line_start_3
                                                    children_6 = []
                                                    while True: # case
                                                        count_2 = 0
                                                        while offset_6 < buf_eof:
                                                            chr = buf[offset_6]
                                                            if chr in ' \t':
                                                                offset_6 +=1
                                                                count_2 +=1
                                                            else:
                                                                break
                                                        
                                                        if offset_6 < buf_eof:
                                                            chr = buf[offset_6]
                                                            if chr == '\r' and offset_6 + 1 < buf_eof and buf[offset_6+1] == '\n':
                                                                offset_6 +=2
                                                                line_start_4 = offset_6
                                                            elif chr in '\n\r':
                                                                offset_6 +=1
                                                                line_start_4 = offset_6
                                                            else:
                                                                offset_6 = -1
                                                                break
                                                        else:
                                                            offset_6 = -1
                                                            break
                                                        
                                                        
                                                        break
                                                    if offset_6 != -1:
                                                        offset_5 = offset_6
                                                        line_start_3 = line_start_4
                                                        children_5.extend(children_6)
                                                        break
                                                    # end case
                                                    offset_6 = offset_5
                                                    line_start_4 = line_start_3
                                                    children_6 = []
                                                    while True: # case
                                                        count_2 = 0
                                                        while offset_6 < buf_eof:
                                                            chr = buf[offset_6]
                                                            if chr in ' \t':
                                                                offset_6 +=1
                                                                count_2 +=1
                                                            else:
                                                                break
                                                        
                                                        if buf[offset_6:offset_6+1] == '#':
                                                            offset_6 += 1
                                                        else:
                                                            offset_6 = -1
                                                            break
                                                        
                                                        count_2 = 0
                                                        while True:
                                                            offset_7 = offset_6
                                                            line_start_5 = line_start_4
                                                            children_7 = []
                                                            while True:
                                                                if offset_7 == buf_eof:
                                                                    offset_7 = -1
                                                                    break
                                                                
                                                                chr = ord(buf[offset_7])
                                                                
                                                                if chr == 10:
                                                                    offset_7 = -1
                                                                    break
                                                                else:
                                                                    offset_7 += 1
                                                                
                                                                break
                                                            if offset_7 == -1:
                                                                break
                                                            if offset_6 == offset_7: break
                                                            children_6.extend(children_7)
                                                            offset_6 = offset_7
                                                            line_start_4 = line_start_5
                                                            count_2 += 1
                                                        if offset_6 == -1:
                                                            break
                                                        
                                                        if offset_6 < buf_eof:
                                                            chr = buf[offset_6]
                                                            if chr == '\r' and offset_6 + 1 < buf_eof and buf[offset_6+1] == '\n':
                                                                offset_6 +=2
                                                                line_start_4 = offset_6
                                                            elif chr in '\n\r':
                                                                offset_6 +=1
                                                                line_start_4 = offset_6
                                                            else:
                                                                offset_6 = -1
                                                                break
                                                        else:
                                                            offset_6 = -1
                                                            break
                                                        
                                                        
                                                        break
                                                    if offset_6 != -1:
                                                        offset_5 = offset_6
                                                        line_start_3 = line_start_4
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
                                            children_4.extend(children_5)
                                            offset_4 = offset_5
                                            line_start_2 = line_start_3
                                            count_1 += 1
                                        if offset_4 == -1:
                                            break
                                        
                                        if offset_4 != line_start_2:
                                            offset_4 = -1
                                            break
                                        for indent in prefix_0:
                                            _children, _prefix = [], []
                                            offset_4, line_start_2 = indent(buf, offset_4, line_start_2, _prefix, buf_eof, _children)
                                            if _prefix or _children:
                                               raise Exception('bar')
                                            if offset_4 == -1:        break
                                            line_start_2 = offset_4
                                        if offset_4 == -1:
                                            break
                                        
                                        count_1 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t':
                                                offset_4 +=1
                                                count_1 +=1
                                            else:
                                                break
                                        if count_1 < 1:
                                            offset_4 = -1
                                            break
                                        
                                        offset_4, line_start_2 = self.parse_indented_value(buf, offset_4, line_start_2, prefix_0, buf_eof, children_4)
                                        if offset_4 == -1: break
                                        
                                        
                                        
                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_1 = line_start_2
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
                                value_3 = self.builder['pair'](buf, offset_2, offset_3, children_3)
                            else:
                                value_3 = Node('pair', offset_2, offset_3, list(children_3), None)
                            children_2.append(value_3)
                            offset_2 = offset_3
                            
                            break
                        if offset_2 == -1:
                            break
                        if offset_1 == offset_2: break
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
                    value_4 = self.builder['object'](buf, offset_0, offset_1, children_1)
                else:
                    value_4 = Node('object', offset_0, offset_1, list(children_1), None)
                children_0.append(value_4)
                offset_0 = offset_1
                
                break
            prefix_0.pop()
            if offset_0 == -1: break
            
            break
        return offset_0, line_start_0
    
    cdef (int, int) parse_indented_value(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_indented_object(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_indented_list(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_literal(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
    
    cdef (int, int) parse_document(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            count_0 = 0
            while True:
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True:
                    count_1 = 0
                    while offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in ' \t':
                            offset_1 +=1
                            count_1 +=1
                        else:
                            break
                    
                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        line_start_2 = line_start_1
                        children_2 = []
                        while True:
                            while True: # start choice
                                offset_3 = offset_2
                                line_start_3 = line_start_2
                                children_3 = []
                                while True: # case
                                    count_2 = 0
                                    while offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in ' \t':
                                            offset_3 +=1
                                            count_2 +=1
                                        else:
                                            break
                                    
                                    if offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                            offset_3 +=2
                                            line_start_3 = offset_3
                                        elif chr in '\n\r':
                                            offset_3 +=1
                                            line_start_3 = offset_3
                                        else:
                                            offset_3 = -1
                                            break
                                    else:
                                        offset_3 = -1
                                        break
                                    
                                    
                                    break
                                if offset_3 != -1:
                                    offset_2 = offset_3
                                    line_start_2 = line_start_3
                                    children_2.extend(children_3)
                                    break
                                # end case
                                offset_3 = offset_2
                                line_start_3 = line_start_2
                                children_3 = []
                                while True: # case
                                    count_2 = 0
                                    while offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in ' \t':
                                            offset_3 +=1
                                            count_2 +=1
                                        else:
                                            break
                                    
                                    if buf[offset_3:offset_3+1] == '#':
                                        offset_3 += 1
                                    else:
                                        offset_3 = -1
                                        break
                                    
                                    count_2 = 0
                                    while True:
                                        offset_4 = offset_3
                                        line_start_4 = line_start_3
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
                                        line_start_3 = line_start_4
                                        count_2 += 1
                                    if offset_3 == -1:
                                        break
                                    
                                    if offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                            offset_3 +=2
                                            line_start_3 = offset_3
                                        elif chr in '\n\r':
                                            offset_3 +=1
                                            line_start_3 = offset_3
                                        else:
                                            offset_3 = -1
                                            break
                                    else:
                                        offset_3 = -1
                                        break
                                    
                                    
                                    break
                                if offset_3 != -1:
                                    offset_2 = offset_3
                                    line_start_2 = line_start_3
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
                        children_1.extend(children_2)
                        offset_1 = offset_2
                        line_start_1 = line_start_2
                        count_1 += 1
                    if offset_1 == -1:
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
            
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                while True: # start choice
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = []
                    while True: # case
                        offset_2, line_start_1 = self.parse_indented_object(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                        if offset_2 == -1: break
                        
                        
                        
                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        line_start_0 = line_start_1
                        children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = []
                    while True: # case
                        offset_2, line_start_1 = self.parse_indented_list(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                        if offset_2 == -1: break
                        
                        
                        
                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        line_start_0 = line_start_1
                        children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = []
                    while True: # case
                        offset_2, line_start_1 = self.parse_list_literal(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                        if offset_2 == -1: break
                        
                        
                        
                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        line_start_0 = line_start_1
                        children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = []
                    while True: # case
                        offset_2, line_start_1 = self.parse_object_literal(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                        if offset_2 == -1: break
                        
                        
                        
                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        line_start_0 = line_start_1
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
                value_0 = Node('document', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t':
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
                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        line_start_2 = line_start_1
                        children_2 = []
                        while True:
                            while True: # start choice
                                offset_3 = offset_2
                                line_start_3 = line_start_2
                                children_3 = []
                                while True: # case
                                    count_2 = 0
                                    while offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in ' \t':
                                            offset_3 +=1
                                            count_2 +=1
                                        else:
                                            break
                                    
                                    if offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                            offset_3 +=2
                                            line_start_3 = offset_3
                                        elif chr in '\n\r':
                                            offset_3 +=1
                                            line_start_3 = offset_3
                                        else:
                                            offset_3 = -1
                                            break
                                    else:
                                        offset_3 = -1
                                        break
                                    
                                    
                                    break
                                if offset_3 != -1:
                                    offset_2 = offset_3
                                    line_start_2 = line_start_3
                                    children_2.extend(children_3)
                                    break
                                # end case
                                offset_3 = offset_2
                                line_start_3 = line_start_2
                                children_3 = []
                                while True: # case
                                    count_2 = 0
                                    while offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in ' \t':
                                            offset_3 +=1
                                            count_2 +=1
                                        else:
                                            break
                                    
                                    if buf[offset_3:offset_3+1] == '#':
                                        offset_3 += 1
                                    else:
                                        offset_3 = -1
                                        break
                                    
                                    count_2 = 0
                                    while True:
                                        offset_4 = offset_3
                                        line_start_4 = line_start_3
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
                                        line_start_3 = line_start_4
                                        count_2 += 1
                                    if offset_3 == -1:
                                        break
                                    
                                    if offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr == '\r' and offset_3 + 1 < buf_eof and buf[offset_3+1] == '\n':
                                            offset_3 +=2
                                            line_start_3 = offset_3
                                        elif chr in '\n\r':
                                            offset_3 +=1
                                            line_start_3 = offset_3
                                        else:
                                            offset_3 = -1
                                            break
                                    else:
                                        offset_3 = -1
                                        break
                                    
                                    
                                    break
                                if offset_3 != -1:
                                    offset_2 = offset_3
                                    line_start_2 = line_start_3
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
                        children_1.extend(children_2)
                        offset_1 = offset_2
                        line_start_1 = line_start_2
                        count_1 += 1
                    if offset_1 == -1:
                        break
                    
                    count_1 = 0
                    while offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in ' \t':
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
            while True:
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True:
                    if offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr == '\r' and offset_1 + 1 < buf_eof and buf[offset_1+1] == '\n':
                            offset_1 +=2
                            line_start_1 = offset_1
                        elif chr in '\n\r':
                            offset_1 +=1
                            line_start_1 = offset_1
                        else:
                            offset_1 = -1
                            break
                    
                    count_1 = 0
                    while offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in ' \t':
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
            
            
            break
        return offset_0, line_start_0
    