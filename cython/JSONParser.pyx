# cython: language_level=3
class ParseNode:
    def __init__(self, name, start, end, children, value):
        self.name = name
        self.start = start
        self.end = end
        self.children = children
        self.value = value
    def __str__(self):
        return '{}[{}:{}]'.format(self.name, self.start, self.end)

cdef class Parser:
    cpdef object builder

    def __init__(self, builder):
         self.builder = builder

    NEWLINE = ()
    WHITESPACE = (' ', '\t', '\r', '\n')

    def parse(self, buf, offset=0):
        line_start, indent, eof, children = offset, 0, len(buf), []
        new_offset, line_start = self.parse_document(buf, offset, line_start, indent, eof, children)
        return children[-1] if new_offset == eof else None
    
    cdef (int, int) parse_document(self, str buf, int offset, int line_start, int indent, int buf_eof, list children):
        cdef int count
        cpdef Py_UNICODE chr
        while True: # note: return at end of loop
            count = 0
            while offset != buf_eof:
                chr = buf[offset]
                if chr == ' ' or chr == '\t' or chr == '\r' or chr == '\n':
                    offset +=1
                    count +=1
                else:
                    break
            
            offset_1 = offset
            children_1 = []
            while True: # start capture
                while True: # start choice
                    offset_2 = offset_1
                    line_start_1 = line_start
                    children_2 = []
                    while True: # case
                        offset_2, line_start_1 = self.parse_json_list(buf, offset_2, line_start_1, indent, buf_eof, children_2)
                        if offset_2 == -1: break
                        
                        
                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        line_start = line_start_1
                        children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    line_start_1 = line_start
                    children_2 = []
                    while True: # case
                        offset_2, line_start_1 = self.parse_json_object(buf, offset_2, line_start_1, indent, buf_eof, children_2)
                        if offset_2 == -1: break
                        
                        
                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        line_start = line_start_1
                        children_1.extend(children_2)
                        break
                    # end case
                    offset_1 = -1 # no more choices
                    break # end choice
                if offset_1 == -1:
                    break
                
                break
            if offset_1 == -1:
                offset = -1
                break
            if self.builder is not None:
                children.append(self.builder['document'](buf, offset, offset_1, children_1))
            else:
                children.append(ParseNode('document', offset, offset_1, list(children_1), None))
            offset = offset_1
            
            
            break
        return offset, line_start
    
    cdef (int, int) parse_json_value(self, str buf, int offset, int line_start, int indent, int buf_eof, list children):
        cdef int count
        cpdef Py_UNICODE chr
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset
                line_start_1 = line_start
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
                        children_1.append(self.builder['bool'](buf, offset_1, offset_2, children_2))
                    else:
                        children_1.append(ParseNode('bool', offset_1, offset_2, list(children_2), None))
                    offset_1 = offset_2
                    
                    
                    break
                if offset_1 != -1:
                    offset = offset_1
                    line_start = line_start_1
                    children.extend(children_1)
                    break
                # end case
                offset_1 = offset
                line_start_1 = line_start
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
                        children_1.append(self.builder['bool'](buf, offset_1, offset_2, children_2))
                    else:
                        children_1.append(ParseNode('bool', offset_1, offset_2, list(children_2), None))
                    offset_1 = offset_2
                    
                    
                    break
                if offset_1 != -1:
                    offset = offset_1
                    line_start = line_start_1
                    children.extend(children_1)
                    break
                # end case
                offset_1 = offset
                line_start_1 = line_start
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
                        children_1.append(self.builder['bool'](buf, offset_1, offset_2, children_2))
                    else:
                        children_1.append(ParseNode('bool', offset_1, offset_2, list(children_2), None))
                    offset_1 = offset_2
                    
                    
                    break
                if offset_1 != -1:
                    offset = offset_1
                    line_start = line_start_1
                    children.extend(children_1)
                    break
                # end case
                offset_1 = offset
                line_start_1 = line_start
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_json_number(buf, offset_1, line_start_1, indent, buf_eof, children_1)
                    if offset_1 == -1: break
                    
                    
                    
                    break
                if offset_1 != -1:
                    offset = offset_1
                    line_start = line_start_1
                    children.extend(children_1)
                    break
                # end case
                offset_1 = offset
                line_start_1 = line_start
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_json_string(buf, offset_1, line_start_1, indent, buf_eof, children_1)
                    if offset_1 == -1: break
                    
                    
                    
                    break
                if offset_1 != -1:
                    offset = offset_1
                    line_start = line_start_1
                    children.extend(children_1)
                    break
                # end case
                offset_1 = offset
                line_start_1 = line_start
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_json_list(buf, offset_1, line_start_1, indent, buf_eof, children_1)
                    if offset_1 == -1: break
                    
                    
                    
                    break
                if offset_1 != -1:
                    offset = offset_1
                    line_start = line_start_1
                    children.extend(children_1)
                    break
                # end case
                offset_1 = offset
                line_start_1 = line_start
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_json_object(buf, offset_1, line_start_1, indent, buf_eof, children_1)
                    if offset_1 == -1: break
                    
                    
                    
                    break
                if offset_1 != -1:
                    offset = offset_1
                    line_start = line_start_1
                    children.extend(children_1)
                    break
                # end case
                offset = -1 # no more choices
                break # end choice
            if offset == -1:
                break
            
            break
        return offset, line_start
    
    cdef (int, int) parse_json_number(self, str buf, int offset, int line_start, int indent, int buf_eof, list children):
        cdef int count
        cpdef Py_UNICODE chr
        while True: # note: return at end of loop
            offset_1 = offset
            children_1 = []
            while True: # start capture
                count = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start
                    if buf[offset_2:offset_2+1] == '-':
                        offset_2 += 1
                    else:
                        offset_2 = -1
                        break
                    
                    if offset_1 == offset_2: break
                    offset_1 = offset_2
                    line_start = line_start_1
                    count += 1
                
                while True: # start choice
                    offset_2 = offset_1
                    line_start_1 = line_start
                    children_2 = []
                    while True: # case
                        if buf[offset_2:offset_2+1] == '0':
                            offset_2 += 1
                        else:
                            offset_2 = -1
                            break
                        
                        
                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        line_start = line_start_1
                        children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    line_start_1 = line_start
                    children_2 = []
                    while True: # case
                        if offset_2 == buf_eof:
                            offset_2 = -1
                            break
                        elif '1' <= buf[offset_2] <= '9':
                            offset_2 += 1
                        else:
                            offset_2 = -1
                            break
                        
                        count = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            if offset_3 == buf_eof:
                                offset_3 = -1
                                break
                            elif '0' <= buf[offset_3] <= '9':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break
                            
                            if offset_2 == offset_3: break
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count += 1
                        
                        
                        break
                    if offset_2 != -1:
                        offset_1 = offset_2
                        line_start = line_start_1
                        children_1.extend(children_2)
                        break
                    # end case
                    offset_1 = -1 # no more choices
                    break # end choice
                if offset_1 == -1:
                    break
                
                count = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start
                    if buf[offset_2:offset_2+1] == '.':
                        offset_2 += 1
                    else:
                        offset_2 = -1
                        break
                    
                    count_1 = 0
                    while True:
                        offset_3 = offset_2
                        line_start_2 = line_start_1
                        if offset_3 == buf_eof:
                            offset_3 = -1
                            break
                        elif '0' <= buf[offset_3] <= '9':
                            offset_3 += 1
                        else:
                            offset_3 = -1
                            break
                        
                        if offset_2 == offset_3: break
                        offset_2 = offset_3
                        line_start_1 = line_start_2
                        count_1 += 1
                    
                    if offset_1 == offset_2: break
                    offset_1 = offset_2
                    line_start = line_start_1
                    count += 1
                
                count = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start
                    if buf[offset_2:offset_2+1] == 'e':
                        offset_2 += 1
                    elif buf[offset_2:offset_2+1] == 'E':
                        offset_2 += 1
                    else:
                        offset_2 = -1
                        break
                    
                    count_1 = 0
                    while True:
                        offset_3 = offset_2
                        line_start_2 = line_start_1
                        if buf[offset_3:offset_3+1] == '+':
                            offset_3 += 1
                        elif buf[offset_3:offset_3+1] == '-':
                            offset_3 += 1
                        else:
                            offset_3 = -1
                            break
                        
                        count_2 = 0
                        while True:
                            offset_4 = offset_3
                            line_start_3 = line_start_2
                            if offset_4 == buf_eof:
                                offset_4 = -1
                                break
                            elif '0' <= buf[offset_4] <= '9':
                                offset_4 += 1
                            else:
                                offset_4 = -1
                                break
                            
                            if offset_3 == offset_4: break
                            offset_3 = offset_4
                            line_start_2 = line_start_3
                            count_2 += 1
                        
                        if offset_2 == offset_3: break
                        offset_2 = offset_3
                        line_start_1 = line_start_2
                        count_1 += 1
                    
                    if offset_1 == offset_2: break
                    offset_1 = offset_2
                    line_start = line_start_1
                    count += 1
                
                break
            if offset_1 == -1:
                offset = -1
                break
            if self.builder is not None:
                children.append(self.builder['number'](buf, offset, offset_1, children_1))
            else:
                children.append(ParseNode('number', offset, offset_1, list(children_1), None))
            offset = offset_1
            
            break
        return offset, line_start
    
    cdef (int, int) parse_json_string(self, str buf, int offset, int line_start, int indent, int buf_eof, list children):
        cdef int count
        cpdef Py_UNICODE chr
        while True: # note: return at end of loop
            if buf[offset:offset+1] == '"':
                offset += 1
            else:
                offset = -1
                break
            
            offset_1 = offset
            children_1 = []
            while True: # start capture
                count = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start
                    while True: # start choice
                        offset_3 = offset_2
                        line_start_2 = line_start_1
                        children_2 = []
                        while True: # case
                            if buf[offset_3:offset_3+2] == '\\u':
                                offset_3 += 2
                            else:
                                offset_3 = -1
                                break
                            
                            if offset_3 == buf_eof:
                                offset_3 = -1
                                break
                            elif '0' <= buf[offset_3] <= '9':
                                offset_3 += 1
                            elif 'a' <= buf[offset_3] <= 'f':
                                offset_3 += 1
                            elif 'A' <= buf[offset_3] <= 'F':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break
                            
                            if offset_3 == buf_eof:
                                offset_3 = -1
                                break
                            elif '0' <= buf[offset_3] <= '9':
                                offset_3 += 1
                            elif 'a' <= buf[offset_3] <= 'f':
                                offset_3 += 1
                            elif 'A' <= buf[offset_3] <= 'F':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break
                            
                            if offset_3 == buf_eof:
                                offset_3 = -1
                                break
                            elif '0' <= buf[offset_3] <= '9':
                                offset_3 += 1
                            elif 'a' <= buf[offset_3] <= 'f':
                                offset_3 += 1
                            elif 'A' <= buf[offset_3] <= 'F':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break
                            
                            if offset_3 == buf_eof:
                                offset_3 = -1
                                break
                            elif '0' <= buf[offset_3] <= '9':
                                offset_3 += 1
                            elif 'a' <= buf[offset_3] <= 'f':
                                offset_3 += 1
                            elif 'A' <= buf[offset_3] <= 'F':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break
                            
                            
                            break
                        if offset_3 != -1:
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            children_1.extend(children_2)
                            break
                        # end case
                        offset_3 = offset_2
                        line_start_2 = line_start_1
                        children_2 = []
                        while True: # case
                            if buf[offset_3:offset_3+1] == '\\':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break
                            
                            if offset_3 == buf_eof:
                                offset_3 = -1
                                break
                            elif buf[offset_3] == '"':
                                offset_3 += 1
                            elif buf[offset_3] == '\\':
                                offset_3 += 1
                            elif buf[offset_3] == '/':
                                offset_3 += 1
                            elif buf[offset_3] == 'b':
                                offset_3 += 1
                            elif buf[offset_3] == 'f':
                                offset_3 += 1
                            elif buf[offset_3] == 'n':
                                offset_3 += 1
                            elif buf[offset_3] == 'r':
                                offset_3 += 1
                            elif buf[offset_3] == 't':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break
                            
                            
                            break
                        if offset_3 != -1:
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            children_1.extend(children_2)
                            break
                        # end case
                        offset_3 = offset_2
                        line_start_2 = line_start_1
                        children_2 = []
                        while True: # case
                            if offset_3 == buf_eof:
                                offset_3 = -1
                                break
                            elif buf[offset_3] == '\\':
                                offset_3 = -1
                                break
                            elif buf[offset_3] == '"':
                                offset_3 = -1
                                break
                            else:
                                offset_3 += 1
                            
                            
                            break
                        if offset_3 != -1:
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            children_1.extend(children_2)
                            break
                        # end case
                        offset_2 = -1 # no more choices
                        break # end choice
                    if offset_2 == -1:
                        break
                    
                    if offset_1 == offset_2: break
                    offset_1 = offset_2
                    line_start = line_start_1
                    count += 1
                
                break
            if offset_1 == -1:
                offset = -1
                break
            if self.builder is not None:
                children.append(self.builder['string'](buf, offset, offset_1, children_1))
            else:
                children.append(ParseNode('string', offset, offset_1, list(children_1), None))
            offset = offset_1
            
            if buf[offset:offset+1] == '"':
                offset += 1
            else:
                offset = -1
                break
            
            
            break
        return offset, line_start
    
    cdef (int, int) parse_json_list(self, str buf, int offset, int line_start, int indent, int buf_eof, list children):
        cdef int count
        cpdef Py_UNICODE chr
        while True: # note: return at end of loop
            if buf[offset:offset+1] == '[':
                offset += 1
            else:
                offset = -1
                break
            
            count = 0
            while offset != buf_eof:
                chr = buf[offset]
                if chr == ' ' or chr == '\t' or chr == '\r' or chr == '\n':
                    offset +=1
                    count +=1
                else:
                    break
            
            offset_1 = offset
            children_1 = []
            while True: # start capture
                count = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start
                    offset_2, line_start_1 = self.parse_json_value(buf, offset_2, line_start_1, indent, buf_eof, children_1)
                    if offset_2 == -1: break
                    
                    
                    count_1 = 0
                    while True:
                        offset_3 = offset_2
                        line_start_2 = line_start_1
                        count_2 = 0
                        while offset_3 != buf_eof:
                            chr = buf[offset_3]
                            if chr == ' ' or chr == '\t' or chr == '\r' or chr == '\n':
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
                        while offset_3 != buf_eof:
                            chr = buf[offset_3]
                            if chr == ' ' or chr == '\t' or chr == '\r' or chr == '\n':
                                offset_3 +=1
                                count_2 +=1
                            else:
                                break
                        
                        offset_3, line_start_2 = self.parse_json_value(buf, offset_3, line_start_2, indent, buf_eof, children_1)
                        if offset_3 == -1: break
                        
                        
                        if offset_2 == offset_3: break
                        offset_2 = offset_3
                        line_start_1 = line_start_2
                        count_1 += 1
                    
                    if offset_1 == offset_2: break
                    offset_1 = offset_2
                    line_start = line_start_1
                    count += 1
                
                break
            if offset_1 == -1:
                offset = -1
                break
            if self.builder is not None:
                children.append(self.builder['list'](buf, offset, offset_1, children_1))
            else:
                children.append(ParseNode('list', offset, offset_1, list(children_1), None))
            offset = offset_1
            
            if buf[offset:offset+1] == ']':
                offset += 1
            else:
                offset = -1
                break
            
            
            break
        return offset, line_start
    
    cdef (int, int) parse_json_object(self, str buf, int offset, int line_start, int indent, int buf_eof, list children):
        cdef int count
        cpdef Py_UNICODE chr
        while True: # note: return at end of loop
            if buf[offset:offset+1] == '{':
                offset += 1
            else:
                offset = -1
                break
            
            count = 0
            while offset != buf_eof:
                chr = buf[offset]
                if chr == ' ' or chr == '\t' or chr == '\r' or chr == '\n':
                    offset +=1
                    count +=1
                else:
                    break
            
            offset_1 = offset
            children_1 = []
            while True: # start capture
                count = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start
                    offset_3 = offset_2
                    children_2 = []
                    while True: # start capture
                        offset_3, line_start_1 = self.parse_json_string(buf, offset_3, line_start_1, indent, buf_eof, children_2)
                        if offset_3 == -1: break
                        
                        
                        count_1 = 0
                        while offset_3 != buf_eof:
                            chr = buf[offset_3]
                            if chr == ' ' or chr == '\t' or chr == '\r' or chr == '\n':
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
                        while offset_3 != buf_eof:
                            chr = buf[offset_3]
                            if chr == ' ' or chr == '\t' or chr == '\r' or chr == '\n':
                                offset_3 +=1
                                count_1 +=1
                            else:
                                break
                        
                        offset_3, line_start_1 = self.parse_json_value(buf, offset_3, line_start_1, indent, buf_eof, children_2)
                        if offset_3 == -1: break
                        
                        
                        break
                    if offset_3 == -1:
                        offset_2 = -1
                        break
                    if self.builder is not None:
                        children_1.append(self.builder['pair'](buf, offset_2, offset_3, children_2))
                    else:
                        children_1.append(ParseNode('pair', offset_2, offset_3, list(children_2), None))
                    offset_2 = offset_3
                    
                    count_1 = 0
                    while offset_2 != buf_eof:
                        chr = buf[offset_2]
                        if chr == ' ' or chr == '\t' or chr == '\r' or chr == '\n':
                            offset_2 +=1
                            count_1 +=1
                        else:
                            break
                    
                    count_1 = 0
                    while True:
                        offset_3 = offset_2
                        line_start_2 = line_start_1
                        if buf[offset_3:offset_3+1] == ',':
                            offset_3 += 1
                        else:
                            offset_3 = -1
                            break
                        
                        count_2 = 0
                        while offset_3 != buf_eof:
                            chr = buf[offset_3]
                            if chr == ' ' or chr == '\t' or chr == '\r' or chr == '\n':
                                offset_3 +=1
                                count_2 +=1
                            else:
                                break
                        
                        offset_4 = offset_3
                        children_2 = []
                        while True: # start capture
                            offset_4, line_start_2 = self.parse_json_string(buf, offset_4, line_start_2, indent, buf_eof, children_2)
                            if offset_4 == -1: break
                            
                            
                            count_2 = 0
                            while offset_4 != buf_eof:
                                chr = buf[offset_4]
                                if chr == ' ' or chr == '\t' or chr == '\r' or chr == '\n':
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
                            while offset_4 != buf_eof:
                                chr = buf[offset_4]
                                if chr == ' ' or chr == '\t' or chr == '\r' or chr == '\n':
                                    offset_4 +=1
                                    count_2 +=1
                                else:
                                    break
                            
                            offset_4, line_start_2 = self.parse_json_value(buf, offset_4, line_start_2, indent, buf_eof, children_2)
                            if offset_4 == -1: break
                            
                            
                            break
                        if offset_4 == -1:
                            offset_3 = -1
                            break
                        if self.builder is not None:
                            children_1.append(self.builder['pair'](buf, offset_3, offset_4, children_2))
                        else:
                            children_1.append(ParseNode('pair', offset_3, offset_4, list(children_2), None))
                        offset_3 = offset_4
                        
                        count_2 = 0
                        while offset_3 != buf_eof:
                            chr = buf[offset_3]
                            if chr == ' ' or chr == '\t' or chr == '\r' or chr == '\n':
                                offset_3 +=1
                                count_2 +=1
                            else:
                                break
                        
                        if offset_2 == offset_3: break
                        offset_2 = offset_3
                        line_start_1 = line_start_2
                        count_1 += 1
                    
                    if offset_1 == offset_2: break
                    offset_1 = offset_2
                    line_start = line_start_1
                    count += 1
                
                break
            if offset_1 == -1:
                offset = -1
                break
            if self.builder is not None:
                children.append(self.builder['object'](buf, offset, offset_1, children_1))
            else:
                children.append(ParseNode('object', offset, offset_1, list(children_1), None))
            offset = offset_1
            
            if buf[offset:offset+1] == '}':
                offset += 1
            else:
                offset = -1
                break
            
            
            break
        return offset, line_start
    