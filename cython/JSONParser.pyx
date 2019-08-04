# cython: language_level=3, boundscheck=False
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
    cdef object builder

    NEWLINE = ()
    WHITESPACE = (' ', '\t', '\r', '\n')

    def parse(self, buf, offset=0):
        line_start, indent, eof, children = offset, len(buf), None, []
        new_offset, line_start = self.parse_document(buf, offset, line_start, indent, eof, children)
        return children[-1] if new_offset else None
    
    cdef (int, int) parse_document(self, str buf, int offset, int line_start, int indent, int buf_eof, list children):
        cdef int count
        cdef Py_UNICODE chr
        while True: # note: return at end of loop
            count = 0
            while offset != buf_eof:
                chr = buf[offset]
                if chr == '(' or chr == "'" or chr == ' ' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 't' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'r' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'n' or chr == "'" or chr == ')':
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
                children.append(self.ParseNode('document', offset, offset_1, children_1, None))
            else:
                children.append(ParseNode('document', offset, offset_1, children_1, None))
            offset = offset_1
            
            
            break
        return offset, line_start
    
    cdef (int, int) parse_json_value(self, str buf, int offset, int line_start, int indent, int buf_eof, list children):
        cdef int count
        cdef Py_UNICODE chr
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
                        children_1.append(self.ParseNode('bool', offset_1, offset_2, children_2, None))
                    else:
                        children_1.append(ParseNode('bool', offset_1, offset_2, children_2, None))
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
                        children_1.append(self.ParseNode('bool', offset_1, offset_2, children_2, None))
                    else:
                        children_1.append(ParseNode('bool', offset_1, offset_2, children_2, None))
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
                        children_1.append(self.ParseNode('bool', offset_1, offset_2, children_2, None))
                    else:
                        children_1.append(ParseNode('bool', offset_1, offset_2, children_2, None))
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
                        count = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            if buf[offset_3:offset_3+1] == '-':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break
                            
                            if offset_2 == offset_3: break
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count += 1
                        
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
                                elif '1' <= buf[offset_3] <= '9':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break
                                
                                count = 0
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
                                    count += 1
                                
                                
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
                        
                        count = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            if buf[offset_3:offset_3+1] == '.':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break
                            
                            count_1 = 0
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
                                count_1 += 1
                            
                            if offset_2 == offset_3: break
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count += 1
                        
                        count = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            if buf[offset_3:offset_3+1] == 'e':
                                offset_3 += 1
                            elif buf[offset_3:offset_3+1] == 'E':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break
                            
                            count_1 = 0
                            while True:
                                offset_4 = offset_3
                                line_start_3 = line_start_2
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
                                    if offset_5 == buf_eof:
                                        offset_5 = -1
                                        break
                                    elif '0' <= buf[offset_5] <= '9':
                                        offset_5 += 1
                                    else:
                                        offset_5 = -1
                                        break
                                    
                                    if offset_4 == offset_5: break
                                    offset_4 = offset_5
                                    line_start_3 = line_start_4
                                    count_2 += 1
                                
                                if offset_3 == offset_4: break
                                offset_3 = offset_4
                                line_start_2 = line_start_3
                                count_1 += 1
                            
                            if offset_2 == offset_3: break
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count += 1
                        
                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        children_1.append(self.ParseNode('number', offset_1, offset_2, children_2, None))
                    else:
                        children_1.append(ParseNode('number', offset_1, offset_2, children_2, None))
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
    
    cdef (int, int) parse_json_string(self, str buf, int offset, int line_start, int indent, int buf_eof, list children):
        cdef int count
        cdef Py_UNICODE chr
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
                children.append(self.ParseNode('string', offset, offset_1, children_1, None))
            else:
                children.append(ParseNode('string', offset, offset_1, children_1, None))
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
        cdef Py_UNICODE chr
        while True: # note: return at end of loop
            if buf[offset:offset+1] == '[':
                offset += 1
            else:
                offset = -1
                break
            
            count = 0
            while offset != buf_eof:
                chr = buf[offset]
                if chr == '(' or chr == "'" or chr == ' ' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 't' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'r' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'n' or chr == "'" or chr == ')':
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
                            if chr == '(' or chr == "'" or chr == ' ' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 't' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'r' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'n' or chr == "'" or chr == ')':
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
                            if chr == '(' or chr == "'" or chr == ' ' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 't' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'r' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'n' or chr == "'" or chr == ')':
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
                children.append(self.ParseNode('list', offset, offset_1, children_1, None))
            else:
                children.append(ParseNode('list', offset, offset_1, children_1, None))
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
        cdef Py_UNICODE chr
        while True: # note: return at end of loop
            if buf[offset:offset+1] == '{':
                offset += 1
            else:
                offset = -1
                break
            
            count = 0
            while offset != buf_eof:
                chr = buf[offset]
                if chr == '(' or chr == "'" or chr == ' ' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 't' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'r' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'n' or chr == "'" or chr == ')':
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
                            if chr == '(' or chr == "'" or chr == ' ' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 't' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'r' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'n' or chr == "'" or chr == ')':
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
                            if chr == '(' or chr == "'" or chr == ' ' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 't' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'r' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'n' or chr == "'" or chr == ')':
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
                        children_1.append(self.ParseNode('pair', offset_2, offset_3, children_2, None))
                    else:
                        children_1.append(ParseNode('pair', offset_2, offset_3, children_2, None))
                    offset_2 = offset_3
                    
                    count_1 = 0
                    while offset_2 != buf_eof:
                        chr = buf[offset_2]
                        if chr == '(' or chr == "'" or chr == ' ' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 't' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'r' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'n' or chr == "'" or chr == ')':
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
                            if chr == '(' or chr == "'" or chr == ' ' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 't' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'r' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'n' or chr == "'" or chr == ')':
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
                                if chr == '(' or chr == "'" or chr == ' ' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 't' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'r' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'n' or chr == "'" or chr == ')':
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
                                if chr == '(' or chr == "'" or chr == ' ' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 't' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'r' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'n' or chr == "'" or chr == ')':
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
                            children_1.append(self.ParseNode('pair', offset_3, offset_4, children_2, None))
                        else:
                            children_1.append(ParseNode('pair', offset_3, offset_4, children_2, None))
                        offset_3 = offset_4
                        
                        count_2 = 0
                        while offset_3 != buf_eof:
                            chr = buf[offset_3]
                            if chr == '(' or chr == "'" or chr == ' ' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 't' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'r' or chr == "'" or chr == ',' or chr == ' ' or chr == "'" or chr == '\\' or chr == 'n' or chr == "'" or chr == ')':
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
                children.append(self.ParseNode('object', offset, offset_1, children_1, None))
            else:
                children.append(ParseNode('object', offset, offset_1, children_1, None))
            offset = offset_1
            
            if buf[offset:offset+1] == '}':
                offset += 1
            else:
                offset = -1
                break
            
            
            break
        return offset, line_start
    