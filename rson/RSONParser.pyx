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
    cpdef object builder, tabstop

    def __init__(self, builder=None):
         self.builder = builder
         self.tabstop = self.TABSTOP
         self.cache = None

    NEWLINE = ()
    WHITESPACE = (32, 9, 13, 10, 65279)
    TABSTOP = 8

    def parse(self, buf, offset=0, end=None, err=None):
        self.cache = dict()
        end = len(buf) if end is None else end
        line_start, prefix, eof, children = offset, [], end, []
        new_offset, line_start = self.parse_document(buf, offset, line_start, prefix, eof, children)
        if children and new_offset == end: return children[-1]
        print('no', offset, new_offset, end, buf[new_offset:])
        if err is not None: raise err(buf, new_offset, 'no')
    
    cdef (int, int) parse_document(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            offset_0, line_start_0 = self.parse_comment(buf, offset_0, line_start_0, prefix_0, buf_eof, children_0)
            if offset_0 == -1: break
            
            
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
                value_0 = Node('document', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            offset_0, line_start_0 = self.parse_comment(buf, offset_0, line_start_0, prefix_0, buf_eof, children_0)
            if offset_0 == -1: break
            
            
            
            break
        return offset_0, line_start_0
    
    cdef (int, int) parse_comment(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof:
                chr = ord(buf[offset_0])
                if chr == 32 or chr == 9 or chr == 13 or chr == 10 or chr == 65279:
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
                        chr = ord(buf[offset_1])
                        if chr == 32 or chr == 9 or chr == 13 or chr == 10 or chr == 65279:
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
                chr = ord(buf[offset_0])
                if chr == 32 or chr == 9 or chr == 13 or chr == 10 or chr == 65279:
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            
            break
        return offset_0, line_start_0
    
    cdef (int, int) parse_rson_value(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
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
                            value_0 = Node('identifier', offset_2, offset_3, list(children_3), None)
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
                        value_1 = Node('tagged', offset_1, offset_2, list(children_2), None)
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
    
    cdef (int, int) parse_rson_literal(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
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
                    offset_1, line_start_1 = self.parse_rson_string(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_rson_number(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_rson_true(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_rson_false(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_rson_null(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
    
    cdef (int, int) parse_rson_true(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                if buf[offset_1:offset_1+4] == 'true':
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
                value_0 = Node('bool', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            break
        return offset_0, line_start_0
    
    cdef (int, int) parse_rson_false(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                if buf[offset_1:offset_1+5] == 'false':
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
                value_0 = Node('bool', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            break
        return offset_0, line_start_0
    
    cdef (int, int) parse_rson_null(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                if buf[offset_1:offset_1+4] == 'null':
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
                value_0 = Node('null', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            break
        return offset_0, line_start_0
    
    cdef (int, int) parse_rson_number(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                while True: # start choice
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = []
                    while True: # case
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
                        
                        if buf[offset_2:offset_2+2] == '0x':
                            offset_2 += 2
                        else:
                            offset_2 = -1
                            break
                        
                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break
                        
                        chr = ord(buf[offset_2])
                        
                        if 48 <= chr <= 57:
                            offset_2 += 1
                        elif 65 <= chr <= 70:
                            offset_2 += 1
                        elif 97 <= chr <= 102:
                            offset_2 += 1
                        else:
                            offset_2 = -1
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
                                elif 65 <= chr <= 70:
                                    offset_3 += 1
                                elif 97 <= chr <= 102:
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
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count_0 += 1
                        if offset_2 == -1:
                            break
                        
                        
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
                        
                        if buf[offset_2:offset_2+2] == '0o':
                            offset_2 += 2
                        else:
                            offset_2 = -1
                            break
                        
                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break
                        
                        chr = ord(buf[offset_2])
                        
                        if 48 <= chr <= 56:
                            offset_2 += 1
                        else:
                            offset_2 = -1
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
                                
                                if 48 <= chr <= 56:
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
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count_0 += 1
                        if offset_2 == -1:
                            break
                        
                        
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
                        
                        if buf[offset_2:offset_2+2] == '0b':
                            offset_2 += 2
                        else:
                            offset_2 = -1
                            break
                        
                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break
                        
                        chr = ord(buf[offset_2])
                        
                        if 48 <= chr <= 49:
                            offset_2 += 1
                        else:
                            offset_2 = -1
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
                                
                                if 48 <= chr <= 49:
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
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count_0 += 1
                        if offset_2 == -1:
                            break
                        
                        
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
                        
                        while True: # start choice
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            children_3 = []
                            while True: # case
                                if buf[offset_3:offset_3+1] == '0':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
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
                            offset_2 = -1 # no more choices
                            break # end choice
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
                value_0 = self.builder['number'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = Node('number', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            break
        return offset_0, line_start_0
    
    cdef (int, int) parse_rson_string(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
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
                        value_1 = Node('string', offset_1, offset_2, list(children_2), None)
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
    
    cdef (int, int) parse_rson_list(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            if buf[offset_0:offset_0+1] == '[':
                offset_0 += 1
            else:
                offset_0 = -1
                break
            
            offset_0, line_start_0 = self.parse_comment(buf, offset_0, line_start_0, prefix_0, buf_eof, children_0)
            if offset_0 == -1: break
            
            
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
                                offset_3, line_start_2 = self.parse_comment(buf, offset_3, line_start_2, prefix_0, buf_eof, children_3)
                                if offset_3 == -1: break
                                
                                
                                if buf[offset_3:offset_3+1] == ',':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break
                                
                                offset_3, line_start_2 = self.parse_comment(buf, offset_3, line_start_2, prefix_0, buf_eof, children_3)
                                if offset_3 == -1: break
                                
                                
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
                        
                        offset_2, line_start_1 = self.parse_comment(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                        if offset_2 == -1: break
                        
                        
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
                                
                                offset_3, line_start_2 = self.parse_comment(buf, offset_3, line_start_2, prefix_0, buf_eof, children_3)
                                if offset_3 == -1: break
                                
                                
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
    
    cdef (int, int) parse_rson_object(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):
        cdef int count_0
        cpdef Py_UCS4 chr
        while True: # note: return at end of loop
            if buf[offset_0:offset_0+1] == '{':
                offset_0 += 1
            else:
                offset_0 = -1
                break
            
            offset_0, line_start_0 = self.parse_comment(buf, offset_0, line_start_0, prefix_0, buf_eof, children_0)
            if offset_0 == -1: break
            
            
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
                            
                            
                            offset_3, line_start_1 = self.parse_comment(buf, offset_3, line_start_1, prefix_0, buf_eof, children_3)
                            if offset_3 == -1: break
                            
                            
                            if buf[offset_3:offset_3+1] == ':':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break
                            
                            offset_3, line_start_1 = self.parse_comment(buf, offset_3, line_start_1, prefix_0, buf_eof, children_3)
                            if offset_3 == -1: break
                            
                            
                            offset_3, line_start_1 = self.parse_rson_value(buf, offset_3, line_start_1, prefix_0, buf_eof, children_3)
                            if offset_3 == -1: break
                            
                            
                            break
                        if offset_3 == -1:
                            offset_2 = -1
                            break
                        if self.builder is not None:
                            value_0 = self.builder['pair'](buf, offset_2, offset_3, children_3)
                        else:
                            value_0 = Node('pair', offset_2, offset_3, list(children_3), None)
                        children_2.append(value_0)
                        offset_2 = offset_3
                        
                        offset_2, line_start_1 = self.parse_comment(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                        if offset_2 == -1: break
                        
                        
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
                                
                                offset_3, line_start_2 = self.parse_comment(buf, offset_3, line_start_2, prefix_0, buf_eof, children_3)
                                if offset_3 == -1: break
                                
                                
                                offset_4 = offset_3
                                children_4 = []
                                while True: # start capture
                                    offset_4, line_start_2 = self.parse_rson_string(buf, offset_4, line_start_2, prefix_0, buf_eof, children_4)
                                    if offset_4 == -1: break
                                    
                                    
                                    offset_4, line_start_2 = self.parse_comment(buf, offset_4, line_start_2, prefix_0, buf_eof, children_4)
                                    if offset_4 == -1: break
                                    
                                    
                                    if buf[offset_4:offset_4+1] == ':':
                                        offset_4 += 1
                                    else:
                                        offset_4 = -1
                                        break
                                    
                                    offset_4, line_start_2 = self.parse_comment(buf, offset_4, line_start_2, prefix_0, buf_eof, children_4)
                                    if offset_4 == -1: break
                                    
                                    
                                    offset_4, line_start_2 = self.parse_rson_value(buf, offset_4, line_start_2, prefix_0, buf_eof, children_4)
                                    if offset_4 == -1: break
                                    
                                    
                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                if self.builder is not None:
                                    value_1 = self.builder['pair'](buf, offset_3, offset_4, children_4)
                                else:
                                    value_1 = Node('pair', offset_3, offset_4, list(children_4), None)
                                children_3.append(value_1)
                                offset_3 = offset_4
                                
                                offset_3, line_start_2 = self.parse_comment(buf, offset_3, line_start_2, prefix_0, buf_eof, children_3)
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
                                
                                offset_3, line_start_2 = self.parse_comment(buf, offset_3, line_start_2, prefix_0, buf_eof, children_3)
                                if offset_3 == -1: break
                                
                                
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
                value_2 = Node('object', offset_0, offset_1, list(children_1), None)
            children_0.append(value_2)
            offset_0 = offset_1
            
            if buf[offset_0:offset_0+1] == '}':
                offset_0 += 1
            else:
                offset_0 = -1
                break
            
            
            break
        return offset_0, line_start_0
    