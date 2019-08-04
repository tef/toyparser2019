class Parser:
    def __init__(self, builder):
         self.builder = builder

    NEWLINE = ()
    WHITESPACE = (' ', '\t', '\r', '\n')

    class ParseNode:
        def __init__(self, name, start, end, children, value):
            self.name = name
            self.start = start
            self.end = end
            self.children = children
            self.value = value
        def __str__(self):
            return '{}[{}:{}]'.format(self.name, self.start, self.end)
    
    def parse(self, buf, offset=0):
        line_start, indent, children = offset, None, []
        new_offset, line_start = self.parse_document(buf, offset, line_start, indent, children)
        return children[-1] if new_offset else None
    
    def parse_document(self, buf, offset, line_start, indent, children):
        while True: # note: return at end of loop
            count = 0
            while offset != len(buf):
                if buf[offset] in self.WHITESPACE:
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
                        offset_2, line_start_1 = self.parse_json_list(buf, offset_2, line_start_1, indent,children_2)
                        if offset_2 is None: break
                        
                        
                        break
                    if offset_2 is not None:
                        offset_1 = offset_2
                        line_start = line_start_1
                        children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    line_start_1 = line_start
                    children_2 = []
                    while True: # case
                        offset_2, line_start_1 = self.parse_json_object(buf, offset_2, line_start_1, indent,children_2)
                        if offset_2 is None: break
                        
                        
                        break
                    if offset_2 is not None:
                        offset_1 = offset_2
                        line_start = line_start_1
                        children_1.extend(children_2)
                        break
                    # end case
                    offset_1 = None # no more choices
                    break # end choice
                if offset_1 is None:
                    break
                
                break
            if offset_1 is None:
                offset = None
                break
            children.append(self.ParseNode('document', offset, offset_1, children_1, None))
            offset = offset_1
            
            
            break
        return offset, line_start
    
    def parse_json_value(self, buf, offset, line_start, indent, children):
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset
                line_start_1 = line_start
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_json_list(buf, offset_1, line_start_1, indent,children_1)
                    if offset_1 is None: break
                    
                    
                    break
                if offset_1 is not None:
                    offset = offset_1
                    line_start = line_start_1
                    children.extend(children_1)
                    break
                # end case
                offset_1 = offset
                line_start_1 = line_start
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_json_object(buf, offset_1, line_start_1, indent,children_1)
                    if offset_1 is None: break
                    
                    
                    break
                if offset_1 is not None:
                    offset = offset_1
                    line_start = line_start_1
                    children.extend(children_1)
                    break
                # end case
                offset_1 = offset
                line_start_1 = line_start
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_json_string(buf, offset_1, line_start_1, indent,children_1)
                    if offset_1 is None: break
                    
                    
                    break
                if offset_1 is not None:
                    offset = offset_1
                    line_start = line_start_1
                    children.extend(children_1)
                    break
                # end case
                offset_1 = offset
                line_start_1 = line_start
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_json_number(buf, offset_1, line_start_1, indent,children_1)
                    if offset_1 is None: break
                    
                    
                    break
                if offset_1 is not None:
                    offset = offset_1
                    line_start = line_start_1
                    children.extend(children_1)
                    break
                # end case
                offset_1 = offset
                line_start_1 = line_start
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_json_true(buf, offset_1, line_start_1, indent,children_1)
                    if offset_1 is None: break
                    
                    
                    break
                if offset_1 is not None:
                    offset = offset_1
                    line_start = line_start_1
                    children.extend(children_1)
                    break
                # end case
                offset_1 = offset
                line_start_1 = line_start
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_json_false(buf, offset_1, line_start_1, indent,children_1)
                    if offset_1 is None: break
                    
                    
                    break
                if offset_1 is not None:
                    offset = offset_1
                    line_start = line_start_1
                    children.extend(children_1)
                    break
                # end case
                offset_1 = offset
                line_start_1 = line_start
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_json_null(buf, offset_1, line_start_1, indent,children_1)
                    if offset_1 is None: break
                    
                    
                    break
                if offset_1 is not None:
                    offset = offset_1
                    line_start = line_start_1
                    children.extend(children_1)
                    break
                # end case
                offset = None # no more choices
                break # end choice
            if offset is None:
                break
            
            break
        return offset, line_start
    
    def parse_json_true(self, buf, offset, line_start, indent, children):
        while True: # note: return at end of loop
            offset_1 = offset
            children_1 = []
            while True: # start capture
                if buf[offset_1:offset_1+4] == 'true':
                    offset_1 += 4
                else:
                    offset_1 = None
                    break
                
                break
            if offset_1 is None:
                offset = None
                break
            children.append(self.ParseNode('bool', offset, offset_1, children_1, None))
            offset = offset_1
            
            break
        return offset, line_start
    
    def parse_json_false(self, buf, offset, line_start, indent, children):
        while True: # note: return at end of loop
            offset_1 = offset
            children_1 = []
            while True: # start capture
                if buf[offset_1:offset_1+5] == 'false':
                    offset_1 += 5
                else:
                    offset_1 = None
                    break
                
                break
            if offset_1 is None:
                offset = None
                break
            children.append(self.ParseNode('bool', offset, offset_1, children_1, None))
            offset = offset_1
            
            break
        return offset, line_start
    
    def parse_json_null(self, buf, offset, line_start, indent, children):
        while True: # note: return at end of loop
            offset_1 = offset
            children_1 = []
            while True: # start capture
                if buf[offset_1:offset_1+4] == 'null':
                    offset_1 += 4
                else:
                    offset_1 = None
                    break
                
                break
            if offset_1 is None:
                offset = None
                break
            children.append(self.ParseNode('null', offset, offset_1, children_1, None))
            offset = offset_1
            
            break
        return offset, line_start
    
    def parse_json_number(self, buf, offset, line_start, indent, children):
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
                        offset_2 = None
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
                            offset_2 = None
                            break
                        
                        
                        break
                    if offset_2 is not None:
                        offset_1 = offset_2
                        line_start = line_start_1
                        children_1.extend(children_2)
                        break
                    # end case
                    offset_2 = offset_1
                    line_start_1 = line_start
                    children_2 = []
                    while True: # case
                        if offset_2 == len(buf):
                            offset_2 = None
                            break
                        elif '1' <= buf[offset_2] <= '9':
                            offset_2 += 1
                        else:
                            offset_2 = None
                            break
                        
                        count = 0
                        while True:
                            offset_3 = offset_2
                            line_start_2 = line_start_1
                            if offset_3 == len(buf):
                                offset_3 = None
                                break
                            elif '0' <= buf[offset_3] <= '9':
                                offset_3 += 1
                            else:
                                offset_3 = None
                                break
                            
                            if offset_2 == offset_3: break
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count += 1
                        
                        
                        break
                    if offset_2 is not None:
                        offset_1 = offset_2
                        line_start = line_start_1
                        children_1.extend(children_2)
                        break
                    # end case
                    offset_1 = None # no more choices
                    break # end choice
                if offset_1 is None:
                    break
                
                count = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start
                    if buf[offset_2:offset_2+1] == '.':
                        offset_2 += 1
                    else:
                        offset_2 = None
                        break
                    
                    count_1 = 0
                    while True:
                        offset_3 = offset_2
                        line_start_2 = line_start_1
                        if offset_3 == len(buf):
                            offset_3 = None
                            break
                        elif '0' <= buf[offset_3] <= '9':
                            offset_3 += 1
                        else:
                            offset_3 = None
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
                        offset_2 = None
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
                            offset_3 = None
                            break
                        
                        count_2 = 0
                        while True:
                            offset_4 = offset_3
                            line_start_3 = line_start_2
                            if offset_4 == len(buf):
                                offset_4 = None
                                break
                            elif '0' <= buf[offset_4] <= '9':
                                offset_4 += 1
                            else:
                                offset_4 = None
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
            if offset_1 is None:
                offset = None
                break
            children.append(self.ParseNode('number', offset, offset_1, children_1, None))
            offset = offset_1
            
            break
        return offset, line_start
    
    def parse_json_string(self, buf, offset, line_start, indent, children):
        while True: # note: return at end of loop
            if buf[offset:offset+1] == '"':
                offset += 1
            else:
                offset = None
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
                                offset_3 = None
                                break
                            
                            if offset_3 == len(buf):
                                offset_3 = None
                                break
                            elif '0' <= buf[offset_3] <= '9':
                                offset_3 += 1
                            elif 'a' <= buf[offset_3] <= 'f':
                                offset_3 += 1
                            elif 'A' <= buf[offset_3] <= 'F':
                                offset_3 += 1
                            else:
                                offset_3 = None
                                break
                            
                            if offset_3 == len(buf):
                                offset_3 = None
                                break
                            elif '0' <= buf[offset_3] <= '9':
                                offset_3 += 1
                            elif 'a' <= buf[offset_3] <= 'f':
                                offset_3 += 1
                            elif 'A' <= buf[offset_3] <= 'F':
                                offset_3 += 1
                            else:
                                offset_3 = None
                                break
                            
                            if offset_3 == len(buf):
                                offset_3 = None
                                break
                            elif '0' <= buf[offset_3] <= '9':
                                offset_3 += 1
                            elif 'a' <= buf[offset_3] <= 'f':
                                offset_3 += 1
                            elif 'A' <= buf[offset_3] <= 'F':
                                offset_3 += 1
                            else:
                                offset_3 = None
                                break
                            
                            if offset_3 == len(buf):
                                offset_3 = None
                                break
                            elif '0' <= buf[offset_3] <= '9':
                                offset_3 += 1
                            elif 'a' <= buf[offset_3] <= 'f':
                                offset_3 += 1
                            elif 'A' <= buf[offset_3] <= 'F':
                                offset_3 += 1
                            else:
                                offset_3 = None
                                break
                            
                            
                            break
                        if offset_3 is not None:
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
                                offset_3 = None
                                break
                            
                            if offset_3 == len(buf):
                                offset_3 = None
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
                                offset_3 = None
                                break
                            
                            
                            break
                        if offset_3 is not None:
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            children_1.extend(children_2)
                            break
                        # end case
                        offset_3 = offset_2
                        line_start_2 = line_start_1
                        children_2 = []
                        while True: # case
                            if offset_3 == len(buf):
                                offset_3 = None
                                break
                            elif buf[offset_3] == '\\':
                                offset_3 = None
                                break
                            elif buf[offset_3] == '"':
                                offset_3 = None
                                break
                            else:
                                offset_3 += 1
                            
                            
                            break
                        if offset_3 is not None:
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            children_1.extend(children_2)
                            break
                        # end case
                        offset_2 = None # no more choices
                        break # end choice
                    if offset_2 is None:
                        break
                    
                    if offset_1 == offset_2: break
                    offset_1 = offset_2
                    line_start = line_start_1
                    count += 1
                
                break
            if offset_1 is None:
                offset = None
                break
            children.append(self.ParseNode('string', offset, offset_1, children_1, None))
            offset = offset_1
            
            if buf[offset:offset+1] == '"':
                offset += 1
            else:
                offset = None
                break
            
            
            break
        return offset, line_start
    
    def parse_json_list(self, buf, offset, line_start, indent, children):
        while True: # note: return at end of loop
            if buf[offset:offset+1] == '[':
                offset += 1
            else:
                offset = None
                break
            
            count = 0
            while offset != len(buf):
                if buf[offset] in self.WHITESPACE:
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
                    offset_2, line_start_1 = self.parse_json_value(buf, offset_2, line_start_1, indent,children_1)
                    if offset_2 is None: break
                    
                    
                    count_1 = 0
                    while True:
                        offset_3 = offset_2
                        line_start_2 = line_start_1
                        count_2 = 0
                        while offset_3 != len(buf):
                            if buf[offset_3] in self.WHITESPACE:
                                offset_3 +=1
                                count_2 +=1
                            else:
                                break
                        
                        if buf[offset_3:offset_3+1] == ',':
                            offset_3 += 1
                        else:
                            offset_3 = None
                            break
                        
                        count_2 = 0
                        while offset_3 != len(buf):
                            if buf[offset_3] in self.WHITESPACE:
                                offset_3 +=1
                                count_2 +=1
                            else:
                                break
                        
                        offset_3, line_start_2 = self.parse_json_value(buf, offset_3, line_start_2, indent,children_1)
                        if offset_3 is None: break
                        
                        
                        if offset_2 == offset_3: break
                        offset_2 = offset_3
                        line_start_1 = line_start_2
                        count_1 += 1
                    
                    if offset_1 == offset_2: break
                    offset_1 = offset_2
                    line_start = line_start_1
                    count += 1
                
                break
            if offset_1 is None:
                offset = None
                break
            children.append(self.ParseNode('list', offset, offset_1, children_1, None))
            offset = offset_1
            
            if buf[offset:offset+1] == ']':
                offset += 1
            else:
                offset = None
                break
            
            
            break
        return offset, line_start
    
    def parse_json_object(self, buf, offset, line_start, indent, children):
        while True: # note: return at end of loop
            if buf[offset:offset+1] == '{':
                offset += 1
            else:
                offset = None
                break
            
            count = 0
            while offset != len(buf):
                if buf[offset] in self.WHITESPACE:
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
                        offset_3, line_start_1 = self.parse_json_string(buf, offset_3, line_start_1, indent,children_2)
                        if offset_3 is None: break
                        
                        
                        count_1 = 0
                        while offset_3 != len(buf):
                            if buf[offset_3] in self.WHITESPACE:
                                offset_3 +=1
                                count_1 +=1
                            else:
                                break
                        
                        if buf[offset_3:offset_3+1] == ':':
                            offset_3 += 1
                        else:
                            offset_3 = None
                            break
                        
                        count_1 = 0
                        while offset_3 != len(buf):
                            if buf[offset_3] in self.WHITESPACE:
                                offset_3 +=1
                                count_1 +=1
                            else:
                                break
                        
                        offset_3, line_start_1 = self.parse_json_value(buf, offset_3, line_start_1, indent,children_2)
                        if offset_3 is None: break
                        
                        
                        break
                    if offset_3 is None:
                        offset_2 = None
                        break
                    children_1.append(self.ParseNode('pair', offset_2, offset_3, children_2, None))
                    offset_2 = offset_3
                    
                    count_1 = 0
                    while offset_2 != len(buf):
                        if buf[offset_2] in self.WHITESPACE:
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
                            offset_3 = None
                            break
                        
                        count_2 = 0
                        while offset_3 != len(buf):
                            if buf[offset_3] in self.WHITESPACE:
                                offset_3 +=1
                                count_2 +=1
                            else:
                                break
                        
                        offset_4 = offset_3
                        children_2 = []
                        while True: # start capture
                            offset_4, line_start_2 = self.parse_json_string(buf, offset_4, line_start_2, indent,children_2)
                            if offset_4 is None: break
                            
                            
                            count_2 = 0
                            while offset_4 != len(buf):
                                if buf[offset_4] in self.WHITESPACE:
                                    offset_4 +=1
                                    count_2 +=1
                                else:
                                    break
                            
                            if buf[offset_4:offset_4+1] == ':':
                                offset_4 += 1
                            else:
                                offset_4 = None
                                break
                            
                            count_2 = 0
                            while offset_4 != len(buf):
                                if buf[offset_4] in self.WHITESPACE:
                                    offset_4 +=1
                                    count_2 +=1
                                else:
                                    break
                            
                            offset_4, line_start_2 = self.parse_json_value(buf, offset_4, line_start_2, indent,children_2)
                            if offset_4 is None: break
                            
                            
                            break
                        if offset_4 is None:
                            offset_3 = None
                            break
                        children_1.append(self.ParseNode('pair', offset_3, offset_4, children_2, None))
                        offset_3 = offset_4
                        
                        count_2 = 0
                        while offset_3 != len(buf):
                            if buf[offset_3] in self.WHITESPACE:
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
            if offset_1 is None:
                offset = None
                break
            children.append(self.ParseNode('object', offset, offset_1, children_1, None))
            offset = offset_1
            
            if buf[offset:offset+1] == '}':
                offset += 1
            else:
                offset = None
                break
            
            
            break
        return offset, line_start
    