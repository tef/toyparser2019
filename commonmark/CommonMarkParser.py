class Parser:
    def __init__(self, builder=None, tabstop=None, allow_mixed_indent=False):
         self.builder = builder
         self.tabstop = tabstop or self.TABSTOP
         self.cache = None
         self.allow_mixed_indent = allow_mixed_indent

    NEWLINE = ('\n',)
    WHITESPACE = (' ', '\t')
    TABSTOP = 4

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
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = []
                    while True:
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
                        
                        offset_2, line_start_1 = self.parse_block_element(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                        if offset_2 == -1: break
                        
                        
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
                value_0 = self.builder['document'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('document', offset_0, offset_1, list(children_1), None)
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
            
            if offset_0 != buf_eof:
                offset_0 = -1
                break
            
            
            break
        return offset_0, line_start_0
    
    def parse_block_element(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_empty_lines(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_indented_code_block(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_fenced_code_block(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_blockquote(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_atx_heading(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_thematic_break(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_block_list(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_setext_heading(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    offset_1, line_start_1 = self.parse_para(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
    
    def parse_inline_element(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            offset_0, line_start_0 = self.parse_word(buf, offset_0, line_start_0, prefix_0, buf_eof, children_0)
            if offset_0 == -1: break
            
            
            break
        return offset_0, line_start_0
    
    def parse_thematic_break(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                while True: # start choice
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
                                if buf[offset_3:offset_3+1] == '-':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break
                                
                                count_1 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        offset_3 +=1
                                        count_1 +=1
                                    else:
                                        break
                                
                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count_0 += 1
                        if count_0 < 3:
                            offset_2 = -1
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
                                if buf[offset_3:offset_3+1] == '*':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break
                                
                                count_1 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        offset_3 +=1
                                        count_1 +=1
                                    else:
                                        break
                                
                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count_0 += 1
                        if count_0 < 3:
                            offset_2 = -1
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
                                if buf[offset_3:offset_3+1] == '_':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break
                                
                                count_1 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        offset_3 +=1
                                        count_1 +=1
                                    else:
                                        break
                                
                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_1 = line_start_2
                            count_0 += 1
                        if count_0 < 3:
                            offset_2 = -1
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
                value_0 = self.builder['thematic_break'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('thematic_break', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            offset_0, line_start_0 = self.parse_line_end(buf, offset_0, line_start_0, prefix_0, buf_eof, children_0)
            if offset_0 == -1: break
            
            
            
            break
        return offset_0, line_start_0
    
    def parse_atx_heading(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                offset_2 = offset_1
                while True: # start count
                    count_0 = 0
                    while count_0 < 6:
                        offset_3 = offset_2
                        line_start_1 = line_start_0
                        children_2 = []
                        while True:
                            if buf[offset_3:offset_3+1] == '#':
                                offset_3 += 1
                            else:
                                offset_3 = -1
                                break
                            
                            break
                        if offset_3 == -1:
                            break
                        if offset_2 == offset_3: break
                        children_1.extend(children_2)
                        offset_2 = offset_3
                        line_start_0 = line_start_1
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
                
                if self.builder is not None:
                    children_1.append(value_0)
                else:
                    children_1.append(self.Node('value', offset_1, offset_1, (), value_0))
                
                while True: # start choice
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = []
                    while True: # case
                        offset_2, line_start_1 = self.parse_line_end(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
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
                
                offset_2 = offset_1
                children_2 = []
                while True: # start capture
                    offset_2, line_start_0 = self.parse_inline_element(buf, offset_2, line_start_0, prefix_0, buf_eof, children_2)
                    if offset_2 == -1: break
                    
                    
                    count_0 = 0
                    while True:
                        offset_3 = offset_2
                        line_start_1 = line_start_0
                        children_3 = []
                        while True:
                            while True: # start reject
                                children_4 = []
                                offset_4, line_start_2 = offset_3, line_start_1
                                offset_4, line_start_2 = self.parse_atx_heading_end(buf, offset_4, line_start_2, prefix_0, buf_eof, children_4)
                                if offset_4 == -1: break
                                
                                
                                break
                            if offset_4 != -1:
                                offset_3 = -1
                                break
                            
                            count_1 = 0
                            while offset_3 < buf_eof:
                                chr = buf[offset_3]
                                if chr in ' \t':
                                    offset_3 +=1
                                    count_1 +=1
                                else:
                                    break
                            
                            offset_3, line_start_1 = self.parse_inline_element(buf, offset_3, line_start_1, prefix_0, buf_eof, children_3)
                            if offset_3 == -1: break
                            
                            
                            break
                        if offset_3 == -1:
                            break
                        if offset_2 == offset_3: break
                        children_2.extend(children_3)
                        offset_2 = offset_3
                        line_start_0 = line_start_1
                        count_0 += 1
                    if offset_2 == -1:
                        break
                    
                    break
                if offset_2 == -1:
                    offset_1 = -1
                    break
                if self.builder is not None:
                    value_1 = self.builder['text'](buf, offset_1, offset_2, children_2)
                else:
                    value_1 = self.Node('text', offset_1, offset_2, list(children_2), None)
                children_1.append(value_1)
                offset_1 = offset_2
                
                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_2 = self.builder['atx_heading'](buf, offset_0, offset_1, children_1)
            else:
                value_2 = self.Node('atx_heading', offset_0, offset_1, list(children_1), None)
            children_0.append(value_2)
            offset_0 = offset_1
            
            offset_0, line_start_0 = self.parse_atx_heading_end(buf, offset_0, line_start_0, prefix_0, buf_eof, children_0)
            if offset_0 == -1: break
            
            
            
            break
        return offset_0, line_start_0
    
    def parse_atx_heading_end(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            count_0 = 0
            while count_0 < 1:
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
                    if count_1 < 1:
                        offset_1 = -1
                        break
                    
                    count_1 = 0
                    while True:
                        offset_2 = offset_1
                        line_start_2 = line_start_1
                        children_2 = []
                        while True:
                            if buf[offset_2:offset_2+1] == '#':
                                offset_2 += 1
                            else:
                                offset_2 = -1
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
                break
            if offset_0 == -1:
                break
            
            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            if offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in '\n':
                    offset_0 +=1
                    line_start_0 = offset_0
                else:
                    offset_0 = -1
                    break
            
            
            break
        return offset_0, line_start_0
    
    def parse_setext_heading(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                offset_1, line_start_0 = self.parse_inline_para(buf, offset_1, line_start_0, prefix_0, buf_eof, children_1)
                if offset_1 == -1: break
                
                
                count_0 = 0
                while offset_1 < buf_eof:
                    chr = buf[offset_1]
                    if chr in ' \t':
                        offset_1 +=1
                        count_0 +=1
                    else:
                        break
                
                if offset_1 < buf_eof:
                    chr = buf[offset_1]
                    if chr in '\n':
                        offset_1 +=1
                        line_start_0 = offset_1
                    else:
                        offset_1 = -1
                        break
                else:
                    offset_1 = -1
                    break
                
                if offset_1 != line_start_0:
                    offset_1 = -1
                    break
                for indent in prefix_0:
                    _children, _prefix = [], []
                    offset_1, line_start_0 = indent(buf, offset_1, line_start_0, _prefix, buf_eof, _children)
                    if _prefix or _children:
                       raise Exception('bar')
                    if offset_1 == -1:        break
                    line_start_0 = offset_1
                if offset_1 == -1:
                    break
                
                offset_1, line_start_0 = self.parse_setext_heading_line(buf, offset_1, line_start_0, prefix_0, buf_eof, children_1)
                if offset_1 == -1: break
                
                
                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['setext_heading'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('setext_heading', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            
            break
        return offset_0, line_start_0
    
    def parse_setext_heading_line(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            while True: # start choice
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        line_start_2 = line_start_1
                        children_2 = []
                        while True:
                            if buf[offset_2:offset_2+1] == '-':
                                offset_2 += 1
                            else:
                                offset_2 = -1
                                break
                            
                            break
                        if offset_2 == -1:
                            break
                        if offset_1 == offset_2: break
                        children_1.extend(children_2)
                        offset_1 = offset_2
                        line_start_1 = line_start_2
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
                    line_start_0 = line_start_1
                    children_0.extend(children_1)
                    break
                # end case
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        line_start_2 = line_start_1
                        children_2 = []
                        while True:
                            if buf[offset_2:offset_2+1] == '=':
                                offset_2 += 1
                            else:
                                offset_2 = -1
                                break
                            
                            break
                        if offset_2 == -1:
                            break
                        if offset_1 == offset_2: break
                        children_1.extend(children_2)
                        offset_1 = offset_2
                        line_start_1 = line_start_2
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
                    line_start_0 = line_start_1
                    children_0.extend(children_1)
                    break
                # end case
                offset_0 = -1 # no more choices
                break # end choice
            if offset_0 == -1:
                break
            
            offset_0, line_start_0 = self.parse_line_end(buf, offset_0, line_start_0, prefix_0, buf_eof, children_0)
            if offset_0 == -1: break
            
            
            
            break
        return offset_0, line_start_0
    
    def parse_indented_code_block(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 4:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            if count_0 < 4:
                offset_0 = -1
                break
            
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
                    elif chr in '\n':
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
                        count_0 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_1 = line_start_0
                            children_3 = []
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
                                
                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_0 = line_start_1
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
                        value_0 = self.builder['text'](buf, offset_1, offset_2, children_2)
                    else:
                        value_0 = self.Node('text', offset_1, offset_2, list(children_2), None)
                    children_1.append(value_0)
                    offset_1 = offset_2
                    
                    if offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in '\n':
                            offset_1 +=1
                            line_start_0 = offset_1
                        else:
                            offset_1 = -1
                            break
                    
                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        line_start_1 = line_start_0
                        children_2 = []
                        while True:
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
                                    
                                    offset_4 = offset_3
                                    children_4 = []
                                    while True: # start capture
                                        count_1 = 0
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
                                        value_1 = self.builder['text'](buf, offset_3, offset_4, children_4)
                                    else:
                                        value_1 = self.Node('text', offset_3, offset_4, list(children_4), None)
                                    children_3.append(value_1)
                                    offset_3 = offset_4
                                    
                                    if offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in '\n':
                                            offset_3 +=1
                                            line_start_2 = offset_3
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
                                    offset_4 = offset_3
                                    children_4 = []
                                    while True: # start capture
                                        count_1 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t':
                                                offset_4 +=1
                                                count_1 +=1
                                            else:
                                                break
                                        
                                        break
                                    if offset_4 == -1:
                                        offset_3 = -1
                                        break
                                    if self.builder is not None:
                                        value_2 = self.builder['text'](buf, offset_3, offset_4, children_4)
                                    else:
                                        value_2 = self.Node('text', offset_3, offset_4, list(children_4), None)
                                    children_3.append(value_2)
                                    offset_3 = offset_4
                                    
                                    if offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in '\n':
                                            offset_3 +=1
                                            line_start_2 = offset_3
                                        else:
                                            offset_3 = -1
                                            break
                                    else:
                                        offset_3 = -1
                                        break
                                    
                                    count_1 = 0
                                    while True:
                                        offset_4 = offset_3
                                        line_start_3 = line_start_2
                                        children_4 = []
                                        while True:
                                            if offset_4 != line_start_3:
                                                offset_4 = -1
                                                break
                                            for indent in prefix_0:
                                                _children, _prefix = [], []
                                                offset_4, line_start_3 = indent(buf, offset_4, line_start_3, _prefix, buf_eof, _children)
                                                if _prefix or _children:
                                                   raise Exception('bar')
                                                if offset_4 == -1:        break
                                                line_start_3 = offset_4
                                            if offset_4 == -1:
                                                break
                                            
                                            offset_5 = offset_4
                                            children_5 = []
                                            while True: # start capture
                                                count_2 = 0
                                                while offset_5 < buf_eof:
                                                    chr = buf[offset_5]
                                                    if chr in ' \t':
                                                        offset_5 +=1
                                                        count_2 +=1
                                                    else:
                                                        break
                                                
                                                break
                                            if offset_5 == -1:
                                                offset_4 = -1
                                                break
                                            if self.builder is not None:
                                                value_3 = self.builder['text'](buf, offset_4, offset_5, children_5)
                                            else:
                                                value_3 = self.Node('text', offset_4, offset_5, list(children_5), None)
                                            children_4.append(value_3)
                                            offset_4 = offset_5
                                            
                                            if offset_4 < buf_eof:
                                                chr = buf[offset_4]
                                                if chr in '\n':
                                                    offset_4 +=1
                                                    line_start_3 = offset_4
                                                else:
                                                    offset_4 = -1
                                                    break
                                            else:
                                                offset_4 = -1
                                                break
                                            
                                            if offset_4 < buf_eof:
                                                chr = buf[offset_4]
                                                if chr in '\n':
                                                    offset_4 +=1
                                                    line_start_3 = offset_4
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
                                    
                                    while True: # start reject
                                        children_4 = []
                                        offset_4, line_start_3 = offset_3, line_start_2
                                        if offset_4 != line_start_3:
                                            offset_4 = -1
                                            break
                                        for indent in prefix_0:
                                            _children, _prefix = [], []
                                            offset_4, line_start_3 = indent(buf, offset_4, line_start_3, _prefix, buf_eof, _children)
                                            if _prefix or _children:
                                               raise Exception('bar')
                                            if offset_4 == -1:        break
                                            line_start_3 = offset_4
                                        if offset_4 == -1:
                                            break
                                        
                                        break
                                    if offset_4 == -1:
                                        offset_3 = -1
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
                    value_4 = self.builder['indented_code'](buf, offset_0, offset_1, children_1)
                else:
                    value_4 = self.Node('indented_code', offset_0, offset_1, list(children_1), None)
                children_0.append(value_4)
                offset_0 = offset_1
                
                break
            prefix_0.pop()
            if offset_0 == -1: break
            
            
            break
        return offset_0, line_start_0
    
    def parse_fenced_code_block(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                while True: # start choice
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = []
                    while True: # case
                        offset_2, line_start_1 = self.parse_tilde_code_block(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
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
                        offset_2, line_start_1 = self.parse_backtick_code_block(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
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
                value_0 = self.builder['fenced_code'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('fenced_code', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            
            break
        return offset_0, line_start_0
    
    def parse_start_fenced_block(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            while True: # start choice
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    if buf[offset_1:offset_1+3] == '```':
                        offset_1 += 3
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
                    if buf[offset_1:offset_1+3] == '~~~':
                        offset_1 += 3
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
    
    def parse_backtick_code_block(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            if buf[offset_0:offset_0+3] == '```':
                offset_0 += 3
            else:
                offset_0 = -1
                break
            
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = []
                    while True:
                        while True: # start reject
                            children_3 = []
                            offset_3, line_start_2 = offset_2, line_start_1
                            if buf[offset_3:offset_3+3] == '```':
                                offset_3 += 3
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
                value_0 = self.builder['info'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('info', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            offset_0, line_start_0 = self.parse_line_end(buf, offset_0, line_start_0, prefix_0, buf_eof, children_0)
            if offset_0 == -1: break
            
            
            count_0 = 0
            while True:
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True:
                    if offset_1 != line_start_1:
                        offset_1 = -1
                        break
                    for indent in prefix_0:
                        _children, _prefix = [], []
                        offset_1, line_start_1 = indent(buf, offset_1, line_start_1, _prefix, buf_eof, _children)
                        if _prefix or _children:
                           raise Exception('bar')
                        if offset_1 == -1:        break
                        line_start_1 = offset_1
                    if offset_1 == -1:
                        break
                    
                    while True: # start reject
                        children_2 = []
                        offset_2, line_start_2 = offset_1, line_start_1
                        count_1 = 0
                        while offset_2 < buf_eof and count_1 < 3:
                            chr = buf[offset_2]
                            if chr in ' \t':
                                offset_2 +=1
                                count_1 +=1
                            else:
                                break
                        
                        if buf[offset_2:offset_2+3] == '```':
                            offset_2 += 3
                        else:
                            offset_2 = -1
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
                            line_start_2 = line_start_1
                            children_3 = []
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
                        
                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_1 = self.builder['text'](buf, offset_1, offset_2, children_2)
                    else:
                        value_1 = self.Node('text', offset_1, offset_2, list(children_2), None)
                    children_1.append(value_1)
                    offset_1 = offset_2
                    
                    offset_1, line_start_1 = self.parse_line_end(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
                    if offset_1 == -1: break
                    
                    
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
            
            if offset_0 != line_start_0:
                offset_0 = -1
                break
            for indent in prefix_0:
                _children, _prefix = [], []
                offset_0, line_start_0 = indent(buf, offset_0, line_start_0, _prefix, buf_eof, _children)
                if _prefix or _children:
                   raise Exception('bar')
                if offset_0 == -1:        break
                line_start_0 = offset_0
            if offset_0 == -1:
                break
            
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            if buf[offset_0:offset_0+3] == '```':
                offset_0 += 3
            else:
                offset_0 = -1
                break
            
            offset_0, line_start_0 = self.parse_line_end(buf, offset_0, line_start_0, prefix_0, buf_eof, children_0)
            if offset_0 == -1: break
            
            
            
            break
        return offset_0, line_start_0
    
    def parse_tilde_code_block(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            if buf[offset_0:offset_0+3] == '~~~':
                offset_0 += 3
            else:
                offset_0 = -1
                break
            
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
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
                    line_start_0 = line_start_1
                    count_0 += 1
                if offset_1 == -1:
                    break
                
                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['info'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('info', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            offset_0, line_start_0 = self.parse_line_end(buf, offset_0, line_start_0, prefix_0, buf_eof, children_0)
            if offset_0 == -1: break
            
            
            count_0 = 0
            while True:
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True:
                    if offset_1 != line_start_1:
                        offset_1 = -1
                        break
                    for indent in prefix_0:
                        _children, _prefix = [], []
                        offset_1, line_start_1 = indent(buf, offset_1, line_start_1, _prefix, buf_eof, _children)
                        if _prefix or _children:
                           raise Exception('bar')
                        if offset_1 == -1:        break
                        line_start_1 = offset_1
                    if offset_1 == -1:
                        break
                    
                    while True: # start reject
                        children_2 = []
                        offset_2, line_start_2 = offset_1, line_start_1
                        count_1 = 0
                        while offset_2 < buf_eof and count_1 < 3:
                            chr = buf[offset_2]
                            if chr in ' \t':
                                offset_2 +=1
                                count_1 +=1
                            else:
                                break
                        
                        if buf[offset_2:offset_2+3] == '~~~':
                            offset_2 += 3
                        else:
                            offset_2 = -1
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
                            line_start_2 = line_start_1
                            children_3 = []
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
                        
                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_1 = self.builder['text'](buf, offset_1, offset_2, children_2)
                    else:
                        value_1 = self.Node('text', offset_1, offset_2, list(children_2), None)
                    children_1.append(value_1)
                    offset_1 = offset_2
                    
                    offset_1, line_start_1 = self.parse_line_end(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
                    if offset_1 == -1: break
                    
                    
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
            
            if offset_0 != line_start_0:
                offset_0 = -1
                break
            for indent in prefix_0:
                _children, _prefix = [], []
                offset_0, line_start_0 = indent(buf, offset_0, line_start_0, _prefix, buf_eof, _children)
                if _prefix or _children:
                   raise Exception('bar')
                if offset_0 == -1:        break
                line_start_0 = offset_0
            if offset_0 == -1:
                break
            
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            if buf[offset_0:offset_0+3] == '~~~':
                offset_0 += 3
            else:
                offset_0 = -1
                break
            
            offset_0, line_start_0 = self.parse_line_end(buf, offset_0, line_start_0, prefix_0, buf_eof, children_0)
            if offset_0 == -1: break
            
            
            
            break
        return offset_0, line_start_0
    
    def parse_blockquote_prefix(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            while True: # start choice
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True: # case
                    offset_1, line_start_1 = self.parse_start_blockquote(buf, offset_1, line_start_1, prefix_0, buf_eof, children_1)
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
                    while True: # start reject
                        children_2 = []
                        offset_2, line_start_2 = offset_1, line_start_1
                        while True: # start choice
                            offset_3 = offset_2
                            line_start_3 = line_start_2
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
                                
                                if offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in '\n':
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
                                offset_3, line_start_3 = self.parse_thematic_break(buf, offset_3, line_start_3, prefix_0, buf_eof, children_3)
                                if offset_3 == -1: break
                                
                                
                                
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
                                offset_3, line_start_3 = self.parse_setext_heading_line(buf, offset_3, line_start_3, prefix_0, buf_eof, children_3)
                                if offset_3 == -1: break
                                
                                
                                
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
                                offset_3, line_start_3 = self.parse_start_fenced_block(buf, offset_3, line_start_3, prefix_0, buf_eof, children_3)
                                if offset_3 == -1: break
                                
                                
                                
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
                                offset_3, line_start_3 = self.parse_start_list(buf, offset_3, line_start_3, prefix_0, buf_eof, children_3)
                                if offset_3 == -1: break
                                
                                
                                
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
                    if offset_2 != -1:
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
    
    def parse_start_blockquote(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            if buf[offset_0:offset_0+1] == '>':
                offset_0 += 1
            else:
                offset_0 = -1
                break
            
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 1:
                chr = buf[offset_0]
                if chr in '\n':
                    offset_0 +=1
                    line_start_0 = offset_0
                    count_0 +=1
                elif chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            
            break
        return offset_0, line_start_0
    
    def parse_blockquote(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                offset_1, line_start_0 = self.parse_start_blockquote(buf, offset_1, line_start_0, prefix_0, buf_eof, children_1)
                if offset_1 == -1: break
                
                
                prefix_0.append(self.parse_blockquote_prefix)
                line_start_0 = offset_1
                while True:
                    offset_1, line_start_0 = self.parse_block_element(buf, offset_1, line_start_0, prefix_0, buf_eof, children_1)
                    if offset_1 == -1: break
                    
                    
                    count_0 = 0
                    while True:
                        offset_2 = offset_1
                        line_start_1 = line_start_0
                        children_2 = []
                        while True:
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
                            
                            while True: # start choice
                                offset_3 = offset_2
                                line_start_2 = line_start_1
                                children_3 = []
                                while True: # case
                                    offset_3, line_start_2 = self.parse_block_element(buf, offset_3, line_start_2, prefix_0, buf_eof, children_3)
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
                                    while offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in ' \t':
                                            offset_3 +=1
                                            count_1 +=1
                                        else:
                                            break
                                    
                                    if offset_3 < buf_eof:
                                        chr = buf[offset_3]
                                        if chr in '\n':
                                            offset_3 +=1
                                            line_start_2 = offset_3
                                        else:
                                            offset_3 = -1
                                            break
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
                prefix_0.pop()
                if offset_1 == -1: break
                
                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['blockquote'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('blockquote', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            break
        return offset_0, line_start_0
    
    def parse_start_list(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            if buf[offset_0:offset_0+1] == '-':
                offset_0 += 1
            else:
                offset_0 = -1
                break
            
            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            if count_0 < 1:
                offset_0 = -1
                break
            
            
            break
        return offset_0, line_start_0
    
    def parse_block_list(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                offset_1, line_start_0 = self.parse_start_list(buf, offset_1, line_start_0, prefix_0, buf_eof, children_1)
                if offset_1 == -1: break
                
                
                offset_2 = offset_1
                children_2 = []
                while True: # start capture
                    offset_2, line_start_0 = self.parse_list_item(buf, offset_2, line_start_0, prefix_0, buf_eof, children_2)
                    if offset_2 == -1: break
                    
                    
                    break
                if offset_2 == -1:
                    offset_1 = -1
                    break
                if self.builder is not None:
                    value_0 = self.builder['list_item'](buf, offset_1, offset_2, children_2)
                else:
                    value_0 = self.Node('list_item', offset_1, offset_2, list(children_2), None)
                children_1.append(value_0)
                offset_1 = offset_2
                
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = []
                    while True:
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
                                
                                if offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in '\n':
                                        offset_3 +=1
                                        line_start_2 = offset_3
                                    else:
                                        offset_3 = -1
                                        break
                                else:
                                    offset_3 = -1
                                    break
                                
                                count_1 = 0
                                while True:
                                    offset_4 = offset_3
                                    line_start_3 = line_start_2
                                    children_4 = []
                                    while True:
                                        if offset_4 != line_start_3:
                                            offset_4 = -1
                                            break
                                        for indent in prefix_0:
                                            _children, _prefix = [], []
                                            offset_4, line_start_3 = indent(buf, offset_4, line_start_3, _prefix, buf_eof, _children)
                                            if _prefix or _children:
                                               raise Exception('bar')
                                            if offset_4 == -1:        break
                                            line_start_3 = offset_4
                                        if offset_4 == -1:
                                            break
                                        
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
                                            if chr in '\n':
                                                offset_4 +=1
                                                line_start_3 = offset_4
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
                                    children_3.extend(children_4)
                                    offset_3 = offset_4
                                    line_start_2 = line_start_3
                                    count_1 += 1
                                if offset_3 == -1:
                                    break
                                
                                while True: # start reject
                                    children_4 = []
                                    offset_4, line_start_3 = offset_3, line_start_2
                                    if offset_4 != line_start_3:
                                        offset_4 = -1
                                        break
                                    for indent in prefix_0:
                                        _children, _prefix = [], []
                                        offset_4, line_start_3 = indent(buf, offset_4, line_start_3, _prefix, buf_eof, _children)
                                        if _prefix or _children:
                                           raise Exception('bar')
                                        if offset_4 == -1:        break
                                        line_start_3 = offset_4
                                    if offset_4 == -1:
                                        break
                                    
                                    count_1 = 0
                                    while offset_4 < buf_eof and count_1 < 3:
                                        chr = buf[offset_4]
                                        if chr in ' \t':
                                            offset_4 +=1
                                            count_1 +=1
                                        else:
                                            break
                                    
                                    if buf[offset_4:offset_4+1] == '-':
                                        offset_4 += 1
                                    else:
                                        offset_4 = -1
                                        break
                                    
                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                
                                offset_4 = offset_3
                                if self.builder is not None:
                                    value_1 = self.builder['empty'](buf, offset_3, offset_4, children_4)
                                else:
                                    value_1 = self.Node('empty', offset_3, offset_4, list(children_4), None)
                                children_3.append(value_1)
                                offset_3 = offset_4
                                
                                
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
                                while offset_3 < buf_eof and count_1 < 3:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        offset_3 +=1
                                        count_1 +=1
                                    else:
                                        break
                                
                                if buf[offset_3:offset_3+1] == '-':
                                    offset_3 += 1
                                else:
                                    offset_3 = -1
                                    break
                                
                                count_1 = 0
                                while offset_3 < buf_eof:
                                    chr = buf[offset_3]
                                    if chr in ' \t':
                                        offset_3 +=1
                                        count_1 +=1
                                    else:
                                        break
                                if count_1 < 1:
                                    offset_3 = -1
                                    break
                                
                                offset_4 = offset_3
                                children_4 = []
                                while True: # start capture
                                    offset_4, line_start_2 = self.parse_list_item(buf, offset_4, line_start_2, prefix_0, buf_eof, children_4)
                                    if offset_4 == -1: break
                                    
                                    
                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                if self.builder is not None:
                                    value_2 = self.builder['list_item'](buf, offset_3, offset_4, children_4)
                                else:
                                    value_2 = self.Node('list_item', offset_3, offset_4, list(children_4), None)
                                children_3.append(value_2)
                                offset_3 = offset_4
                                
                                
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
                value_3 = self.builder['block_list'](buf, offset_0, offset_1, children_1)
            else:
                value_3 = self.Node('block_list', offset_0, offset_1, list(children_1), None)
            children_0.append(value_3)
            offset_0 = offset_1
            
            break
        return offset_0, line_start_0
    
    def parse_list_item(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
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
                    elif chr in '\n':
                        break
                    else:
                        offset = -1
                        break
                return offset, line_start
            prefix_0.append(_indent)
            line_start_0 = offset_0
            while True:
                offset_0, line_start_0 = self.parse_block_element(buf, offset_0, line_start_0, prefix_0, buf_eof, children_0)
                if offset_0 == -1: break
                
                
                count_0 = 0
                while True:
                    offset_1 = offset_0
                    line_start_1 = line_start_0
                    children_1 = []
                    while True:
                        if offset_1 != line_start_1:
                            offset_1 = -1
                            break
                        for indent in prefix_0:
                            _children, _prefix = [], []
                            offset_1, line_start_1 = indent(buf, offset_1, line_start_1, _prefix, buf_eof, _children)
                            if _prefix or _children:
                               raise Exception('bar')
                            if offset_1 == -1:        break
                            line_start_1 = offset_1
                        if offset_1 == -1:
                            break
                        
                        while True: # start choice
                            offset_2 = offset_1
                            line_start_2 = line_start_1
                            children_2 = []
                            while True: # case
                                offset_2, line_start_2 = self.parse_block_element(buf, offset_2, line_start_2, prefix_0, buf_eof, children_2)
                                if offset_2 == -1: break
                                
                                
                                
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
                                count_1 = 0
                                while True:
                                    offset_3 = offset_2
                                    line_start_3 = line_start_2
                                    children_3 = []
                                    while True:
                                        if offset_3 != line_start_3:
                                            offset_3 = -1
                                            break
                                        for indent in prefix_0:
                                            _children, _prefix = [], []
                                            offset_3, line_start_3 = indent(buf, offset_3, line_start_3, _prefix, buf_eof, _children)
                                            if _prefix or _children:
                                               raise Exception('bar')
                                            if offset_3 == -1:        break
                                            line_start_3 = offset_3
                                        if offset_3 == -1:
                                            break
                                        
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
                                            if chr in '\n':
                                                offset_3 +=1
                                                line_start_3 = offset_3
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
                                    children_2.extend(children_3)
                                    offset_2 = offset_3
                                    line_start_2 = line_start_3
                                    count_1 += 1
                                if offset_2 == -1:
                                    break
                                
                                while True: # start reject
                                    children_3 = []
                                    offset_3, line_start_3 = offset_2, line_start_2
                                    if offset_3 != line_start_3:
                                        offset_3 = -1
                                        break
                                    for indent in prefix_0:
                                        _children, _prefix = [], []
                                        offset_3, line_start_3 = indent(buf, offset_3, line_start_3, _prefix, buf_eof, _children)
                                        if _prefix or _children:
                                           raise Exception('bar')
                                        if offset_3 == -1:        break
                                        line_start_3 = offset_3
                                    if offset_3 == -1:
                                        break
                                    
                                    break
                                if offset_3 == -1:
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
            prefix_0.pop()
            if offset_0 == -1: break
            
            break
        return offset_0, line_start_0
    
    def parse_para(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof and count_0 < 3:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            offset_1 = offset_0
            children_1 = []
            count_0 = ('memo_0', offset_0)
            if count_0 in self.cache:
                offset_1, line_start_0, children_1 = self.cache[count_0]
            else:
                while True:
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        offset_3 = offset_2
                        children_3 = []
                        while True: # start capture
                            offset_3, line_start_0 = self.parse_inline_element(buf, offset_3, line_start_0, prefix_0, buf_eof, children_3)
                            if offset_3 == -1: break
                            
                            
                            break
                        if offset_3 == -1:
                            offset_2 = -1
                            break
                        if self.builder is not None:
                            value_0 = self.builder['text'](buf, offset_2, offset_3, children_3)
                        else:
                            value_0 = self.Node('text', offset_2, offset_3, list(children_3), None)
                        children_2.append(value_0)
                        offset_2 = offset_3
                        
                        count_1 = 0
                        while True:
                            offset_3 = offset_2
                            line_start_1 = line_start_0
                            children_3 = []
                            while True:
                                while True: # start reject
                                    children_4 = []
                                    offset_4, line_start_2 = offset_3, line_start_1
                                    if offset_4 < buf_eof:
                                        chr = buf[offset_4]
                                        if chr in '\n':
                                            offset_4 +=1
                                            line_start_2 = offset_4
                                        else:
                                            offset_4 = -1
                                            break
                                    else:
                                        offset_4 = -1
                                        break
                                    
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
                                        if chr in '\n':
                                            offset_4 +=1
                                            line_start_2 = offset_4
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
                                
                                while True: # start reject
                                    children_4 = []
                                    offset_4, line_start_2 = offset_3, line_start_1
                                    if offset_4 < buf_eof:
                                        chr = buf[offset_4]
                                        if chr in '\n':
                                            offset_4 +=1
                                            line_start_2 = offset_4
                                        else:
                                            offset_4 = -1
                                            break
                                    else:
                                        offset_4 = -1
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
                                        if chr in '\n':
                                            offset_4 +=1
                                            line_start_2 = offset_4
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
                                
                                while True: # start choice
                                    offset_4 = offset_3
                                    line_start_2 = line_start_1
                                    children_4 = []
                                    while True: # case
                                        count_2 = 0
                                        while offset_4 < buf_eof and count_2 < 1:
                                            chr = buf[offset_4]
                                            if chr in ' \t':
                                                offset_4 +=1
                                                count_2 +=1
                                            else:
                                                break
                                        
                                        if offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in '\n':
                                                offset_4 +=1
                                                line_start_2 = offset_4
                                            else:
                                                offset_4 = -1
                                                break
                                        else:
                                            offset_4 = -1
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
                                        
                                        while True: # start reject
                                            children_5 = []
                                            offset_5, line_start_3 = offset_4, line_start_2
                                            while True: # start choice
                                                offset_6 = offset_5
                                                line_start_4 = line_start_3
                                                children_6 = []
                                                while True: # case
                                                    offset_6, line_start_4 = self.parse_thematic_break(buf, offset_6, line_start_4, prefix_0, buf_eof, children_6)
                                                    if offset_6 == -1: break
                                                    
                                                    
                                                    
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
                                                    offset_6, line_start_4 = self.parse_setext_heading_line(buf, offset_6, line_start_4, prefix_0, buf_eof, children_6)
                                                    if offset_6 == -1: break
                                                    
                                                    
                                                    
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
                                                    offset_6, line_start_4 = self.parse_start_fenced_block(buf, offset_6, line_start_4, prefix_0, buf_eof, children_6)
                                                    if offset_6 == -1: break
                                                    
                                                    
                                                    
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
                                                    offset_6, line_start_4 = self.parse_start_list(buf, offset_6, line_start_4, prefix_0, buf_eof, children_6)
                                                    if offset_6 == -1: break
                                                    
                                                    
                                                    
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
                                                    offset_6, line_start_4 = self.parse_start_blockquote(buf, offset_6, line_start_4, prefix_0, buf_eof, children_6)
                                                    if offset_6 == -1: break
                                                    
                                                    
                                                    
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
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break
                                        
                                        count_2 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t':
                                                offset_4 +=1
                                                count_2 +=1
                                            else:
                                                break
                                        
                                        
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
                                        count_2 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t':
                                                offset_4 +=1
                                                count_2 +=1
                                            else:
                                                break
                                        if count_2 < 2:
                                            offset_4 = -1
                                            break
                                        
                                        if offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in '\n':
                                                offset_4 +=1
                                                line_start_2 = offset_4
                                            else:
                                                offset_4 = -1
                                                break
                                        else:
                                            offset_4 = -1
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
                                        
                                        while True: # start reject
                                            children_5 = []
                                            offset_5, line_start_3 = offset_4, line_start_2
                                            while True: # start choice
                                                offset_6 = offset_5
                                                line_start_4 = line_start_3
                                                children_6 = []
                                                while True: # case
                                                    offset_6, line_start_4 = self.parse_thematic_break(buf, offset_6, line_start_4, prefix_0, buf_eof, children_6)
                                                    if offset_6 == -1: break
                                                    
                                                    
                                                    
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
                                                    offset_6, line_start_4 = self.parse_setext_heading_line(buf, offset_6, line_start_4, prefix_0, buf_eof, children_6)
                                                    if offset_6 == -1: break
                                                    
                                                    
                                                    
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
                                                    offset_6, line_start_4 = self.parse_start_fenced_block(buf, offset_6, line_start_4, prefix_0, buf_eof, children_6)
                                                    if offset_6 == -1: break
                                                    
                                                    
                                                    
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
                                                    offset_6, line_start_4 = self.parse_start_list(buf, offset_6, line_start_4, prefix_0, buf_eof, children_6)
                                                    if offset_6 == -1: break
                                                    
                                                    
                                                    
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
                                                    offset_6, line_start_4 = self.parse_start_blockquote(buf, offset_6, line_start_4, prefix_0, buf_eof, children_6)
                                                    if offset_6 == -1: break
                                                    
                                                    
                                                    
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
                                        if offset_5 != -1:
                                            offset_4 = -1
                                            break
                                        
                                        offset_5 = offset_4
                                        if self.builder is not None:
                                            value_1 = self.builder['empty'](buf, offset_4, offset_5, children_5)
                                        else:
                                            value_1 = self.Node('empty', offset_4, offset_5, list(children_5), None)
                                        children_4.append(value_1)
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
                                        count_2 = 0
                                        while offset_4 < buf_eof:
                                            chr = buf[offset_4]
                                            if chr in ' \t':
                                                offset_4 +=1
                                                count_2 +=1
                                            else:
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
                                
                                offset_4 = offset_3
                                children_4 = []
                                while True: # start capture
                                    offset_4, line_start_1 = self.parse_inline_element(buf, offset_4, line_start_1, prefix_0, buf_eof, children_4)
                                    if offset_4 == -1: break
                                    
                                    
                                    break
                                if offset_4 == -1:
                                    offset_3 = -1
                                    break
                                if self.builder is not None:
                                    value_2 = self.builder['text'](buf, offset_3, offset_4, children_4)
                                else:
                                    value_2 = self.Node('text', offset_3, offset_4, list(children_4), None)
                                children_3.append(value_2)
                                offset_3 = offset_4
                                
                                break
                            if offset_3 == -1:
                                break
                            if offset_2 == offset_3: break
                            children_2.extend(children_3)
                            offset_2 = offset_3
                            line_start_0 = line_start_1
                            count_1 += 1
                        if offset_2 == -1:
                            break
                        
                        
                        count_1 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t':
                                offset_2 +=1
                                count_1 +=1
                            else:
                                break
                        
                        if offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in '\n':
                                offset_2 +=1
                                line_start_0 = offset_2
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
                        value_3 = self.Node('para', offset_1, offset_2, list(children_2), None)
                    children_1.append(value_3)
                    offset_1 = offset_2
                    
                    break
                self.cache[count_0] = (offset_1, line_start_0, children_1)
            offset_0 = offset_1
            children_0.extend(children_1)
            if offset_0 == -1:
                break
            
            
            break
        return offset_0, line_start_0
    
    def parse_inline_para(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                offset_1, line_start_0 = self.parse_inline_element(buf, offset_1, line_start_0, prefix_0, buf_eof, children_1)
                if offset_1 == -1: break
                
                
                break
            if offset_1 == -1:
                offset_0 = -1
                break
            if self.builder is not None:
                value_0 = self.builder['text'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('text', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            count_0 = 0
            while True:
                offset_1 = offset_0
                line_start_1 = line_start_0
                children_1 = []
                while True:
                    while True: # start reject
                        children_2 = []
                        offset_2, line_start_2 = offset_1, line_start_1
                        if offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in '\n':
                                offset_2 +=1
                                line_start_2 = offset_2
                            else:
                                offset_2 = -1
                                break
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
                        
                        if offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in '\n':
                                offset_2 +=1
                                line_start_2 = offset_2
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
                    
                    while True: # start reject
                        children_2 = []
                        offset_2, line_start_2 = offset_1, line_start_1
                        if offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in '\n':
                                offset_2 +=1
                                line_start_2 = offset_2
                            else:
                                offset_2 = -1
                                break
                        else:
                            offset_2 = -1
                            break
                        
                        if offset_2 != line_start_2:
                            offset_2 = -1
                            break
                        for indent in prefix_0:
                            _children, _prefix = [], []
                            offset_2, line_start_2 = indent(buf, offset_2, line_start_2, _prefix, buf_eof, _children)
                            if _prefix or _children:
                               raise Exception('bar')
                            if offset_2 == -1:        break
                            line_start_2 = offset_2
                        if offset_2 == -1:
                            break
                        
                        count_1 = 0
                        while offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in ' \t':
                                offset_2 +=1
                                count_1 +=1
                            else:
                                break
                        
                        if offset_2 < buf_eof:
                            chr = buf[offset_2]
                            if chr in '\n':
                                offset_2 +=1
                                line_start_2 = offset_2
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
                    
                    while True: # start choice
                        offset_2 = offset_1
                        line_start_2 = line_start_1
                        children_2 = []
                        while True: # case
                            count_1 = 0
                            while offset_2 < buf_eof and count_1 < 1:
                                chr = buf[offset_2]
                                if chr in ' \t':
                                    offset_2 +=1
                                    count_1 +=1
                                else:
                                    break
                            
                            if offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr in '\n':
                                    offset_2 +=1
                                    line_start_2 = offset_2
                                else:
                                    offset_2 = -1
                                    break
                            else:
                                offset_2 = -1
                                break
                            
                            if offset_2 != line_start_2:
                                offset_2 = -1
                                break
                            for indent in prefix_0:
                                _children, _prefix = [], []
                                offset_2, line_start_2 = indent(buf, offset_2, line_start_2, _prefix, buf_eof, _children)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_2 == -1:        break
                                line_start_2 = offset_2
                            if offset_2 == -1:
                                break
                            
                            while True: # start reject
                                children_3 = []
                                offset_3, line_start_3 = offset_2, line_start_2
                                while True: # start choice
                                    offset_4 = offset_3
                                    line_start_4 = line_start_3
                                    children_4 = []
                                    while True: # case
                                        offset_4, line_start_4 = self.parse_thematic_break(buf, offset_4, line_start_4, prefix_0, buf_eof, children_4)
                                        if offset_4 == -1: break
                                        
                                        
                                        
                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_3 = line_start_4
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_4 = line_start_3
                                    children_4 = []
                                    while True: # case
                                        offset_4, line_start_4 = self.parse_setext_heading_line(buf, offset_4, line_start_4, prefix_0, buf_eof, children_4)
                                        if offset_4 == -1: break
                                        
                                        
                                        
                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_3 = line_start_4
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_4 = line_start_3
                                    children_4 = []
                                    while True: # case
                                        offset_4, line_start_4 = self.parse_start_fenced_block(buf, offset_4, line_start_4, prefix_0, buf_eof, children_4)
                                        if offset_4 == -1: break
                                        
                                        
                                        
                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_3 = line_start_4
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_4 = line_start_3
                                    children_4 = []
                                    while True: # case
                                        offset_4, line_start_4 = self.parse_start_list(buf, offset_4, line_start_4, prefix_0, buf_eof, children_4)
                                        if offset_4 == -1: break
                                        
                                        
                                        
                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_3 = line_start_4
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_4 = line_start_3
                                    children_4 = []
                                    while True: # case
                                        offset_4, line_start_4 = self.parse_start_blockquote(buf, offset_4, line_start_4, prefix_0, buf_eof, children_4)
                                        if offset_4 == -1: break
                                        
                                        
                                        
                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_3 = line_start_4
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_3 = -1 # no more choices
                                    break # end choice
                                if offset_3 == -1:
                                    break
                                
                                break
                            if offset_3 != -1:
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
                            count_1 = 0
                            while offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr in ' \t':
                                    offset_2 +=1
                                    count_1 +=1
                                else:
                                    break
                            if count_1 < 2:
                                offset_2 = -1
                                break
                            
                            if offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr in '\n':
                                    offset_2 +=1
                                    line_start_2 = offset_2
                                else:
                                    offset_2 = -1
                                    break
                            else:
                                offset_2 = -1
                                break
                            
                            if offset_2 != line_start_2:
                                offset_2 = -1
                                break
                            for indent in prefix_0:
                                _children, _prefix = [], []
                                offset_2, line_start_2 = indent(buf, offset_2, line_start_2, _prefix, buf_eof, _children)
                                if _prefix or _children:
                                   raise Exception('bar')
                                if offset_2 == -1:        break
                                line_start_2 = offset_2
                            if offset_2 == -1:
                                break
                            
                            while True: # start reject
                                children_3 = []
                                offset_3, line_start_3 = offset_2, line_start_2
                                while True: # start choice
                                    offset_4 = offset_3
                                    line_start_4 = line_start_3
                                    children_4 = []
                                    while True: # case
                                        offset_4, line_start_4 = self.parse_thematic_break(buf, offset_4, line_start_4, prefix_0, buf_eof, children_4)
                                        if offset_4 == -1: break
                                        
                                        
                                        
                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_3 = line_start_4
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_4 = line_start_3
                                    children_4 = []
                                    while True: # case
                                        offset_4, line_start_4 = self.parse_setext_heading_line(buf, offset_4, line_start_4, prefix_0, buf_eof, children_4)
                                        if offset_4 == -1: break
                                        
                                        
                                        
                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_3 = line_start_4
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_4 = line_start_3
                                    children_4 = []
                                    while True: # case
                                        offset_4, line_start_4 = self.parse_start_fenced_block(buf, offset_4, line_start_4, prefix_0, buf_eof, children_4)
                                        if offset_4 == -1: break
                                        
                                        
                                        
                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_3 = line_start_4
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_4 = line_start_3
                                    children_4 = []
                                    while True: # case
                                        offset_4, line_start_4 = self.parse_start_list(buf, offset_4, line_start_4, prefix_0, buf_eof, children_4)
                                        if offset_4 == -1: break
                                        
                                        
                                        
                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_3 = line_start_4
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_4 = offset_3
                                    line_start_4 = line_start_3
                                    children_4 = []
                                    while True: # case
                                        offset_4, line_start_4 = self.parse_start_blockquote(buf, offset_4, line_start_4, prefix_0, buf_eof, children_4)
                                        if offset_4 == -1: break
                                        
                                        
                                        
                                        break
                                    if offset_4 != -1:
                                        offset_3 = offset_4
                                        line_start_3 = line_start_4
                                        children_3.extend(children_4)
                                        break
                                    # end case
                                    offset_3 = -1 # no more choices
                                    break # end choice
                                if offset_3 == -1:
                                    break
                                
                                break
                            if offset_3 != -1:
                                offset_2 = -1
                                break
                            
                            offset_3 = offset_2
                            if self.builder is not None:
                                value_1 = self.builder['empty'](buf, offset_2, offset_3, children_3)
                            else:
                                value_1 = self.Node('empty', offset_2, offset_3, list(children_3), None)
                            children_2.append(value_1)
                            offset_2 = offset_3
                            
                            
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
                            count_1 = 0
                            while offset_2 < buf_eof:
                                chr = buf[offset_2]
                                if chr in ' \t':
                                    offset_2 +=1
                                    count_1 +=1
                                else:
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
                    
                    offset_2 = offset_1
                    children_2 = []
                    while True: # start capture
                        offset_2, line_start_1 = self.parse_inline_element(buf, offset_2, line_start_1, prefix_0, buf_eof, children_2)
                        if offset_2 == -1: break
                        
                        
                        break
                    if offset_2 == -1:
                        offset_1 = -1
                        break
                    if self.builder is not None:
                        value_2 = self.builder['text'](buf, offset_1, offset_2, children_2)
                    else:
                        value_2 = self.Node('text', offset_1, offset_2, list(children_2), None)
                    children_1.append(value_2)
                    offset_1 = offset_2
                    
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
    
    def parse_empty_lines(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
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
                    
                    if offset_1 < buf_eof:
                        chr = buf[offset_1]
                        if chr in '\n':
                            offset_1 +=1
                            line_start_1 = offset_1
                        else:
                            offset_1 = -1
                            break
                    else:
                        offset_1 = -1
                        break
                    
                    if offset_1 != line_start_1:
                        offset_1 = -1
                        break
                    for indent in prefix_0:
                        _children, _prefix = [], []
                        offset_1, line_start_1 = indent(buf, offset_1, line_start_1, _prefix, buf_eof, _children)
                        if _prefix or _children:
                           raise Exception('bar')
                        if offset_1 == -1:        break
                        line_start_1 = offset_1
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
            if count_0 < 1:
                offset_0 = -1
                break
            if offset_0 == -1:
                break
            
            offset_1 = offset_0
            if self.builder is not None:
                value_0 = self.builder['empty'](buf, offset_0, offset_1, children_1)
            else:
                value_0 = self.Node('empty', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            
            break
        return offset_0, line_start_0
    
    def parse_line_end(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            count_0 = 0
            while offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in ' \t':
                    offset_0 +=1
                    count_0 +=1
                else:
                    break
            
            if offset_0 < buf_eof:
                chr = buf[offset_0]
                if chr in '\n':
                    offset_0 +=1
                    line_start_0 = offset_0
                else:
                    offset_0 = -1
                    break
            
            
            break
        return offset_0, line_start_0
    
    def parse_word(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):
        while True: # note: return at end of loop
            offset_1 = offset_0
            children_1 = []
            while True: # start capture
                count_0 = 0
                while True:
                    offset_2 = offset_1
                    line_start_1 = line_start_0
                    children_2 = []
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
                        else:
                            offset_2 += 1
                        
                        break
                    if offset_2 == -1:
                        break
                    if offset_1 == offset_2: break
                    children_1.extend(children_2)
                    offset_1 = offset_2
                    line_start_0 = line_start_1
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
                value_0 = self.Node('text', offset_0, offset_1, list(children_1), None)
            children_0.append(value_0)
            offset_0 = offset_1
            
            break
        return offset_0, line_start_0
    