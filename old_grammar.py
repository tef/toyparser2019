START_OF_LINE = 'start-of-line'
INDENT = 'indent'
DEDENT = 'dedent'
END_OF_LINE = 'end-of-line'
WHITESPACE = 'whitespace'
NEWLINE = 'newline'
END_OF_FILE = 'end-of-file'

SET_LINE_PREFIX = 'set-line-prefix'

LOOKAHEAD = 'lookahead'
REJECT = 'reject'
ACCEPT_IF = 'accept-if'
REJECT_IF = 'reject-if'
COUNT = 'count'
VALUE = 'value'

RULE = 'rule'
LITERAL = 'literal'
RANGE = 'range'
SEQUENCE = 'seq'
CAPTURE = 'capture'
CHOICE = 'choice'
REPEAT = 'repeat'

PRINT = 'print'
TRACE = 'trace'



class ParserState:
    def __init__(self, buf, line_start,  offset, children, parent, indent, values):
        self.buf = buf
        self.line_start = line_start
        self.offset = offset
        self.children = children
        self.parent = parent
        self.indent = indent
        self.values = values

    @staticmethod
    def init(buf, offset):
        return ParserState(buf, offset, offset, [], None, None, {})

    def clone(self, line_start=None, offset=None, children=None, parent=None, indent=None, values=None):
        if line_start is None: line_start = self.line_start
        if offset is None: offset = self.offset
        if children is None: children = self.children
        if parent is None: parent = self.parent
        if indent is None: indent = self.indent
        if values is None: values = self.values

        return ParserState(self.buf, line_start, offset, children, parent, indent, values)

    def __bool__(self):
        return True

    def choice(self):
        return self.clone(children=[])

    def merge_choice(self, new):
        self.children.extend(new.children)
        return new.clone(children = self.children)

    def set_indent(self, tabstop, whitespace, newlines):
        count = self.offset-self.line_start + ((tabstop -1) * self.buf[self.line_start:self.offset].count('\t'))
        return self.clone(indent=((lambda s: s.advance_indent(count, tabstop, whitespace, newlines)), self.indent), line_start=self.offset)

    def pop_indent(self):
        return self.clone(indent=self.indent[1])

    def advance(self, text):
        if self.buf[self.offset:].startswith(text):
            return self.clone(offset=self.offset + len(text))

    def advance_prefix(self):
        if self.offset != self.line_start:
            return None

        indent = self.indent

        if not indent:
            return self

        def check(state, i):
            if not i: return state
            state = check(state, i[1])
            if not state: return None
            state = i[0](state)
            if state: 
                state.line_start = state.offset
            return state

        return check(self, indent)

    def advance_whitespace(self, literals, newlines, min=0, max=None, newline=False):
        state = self
        count = 0
        while max is None or count < max:
            while newline:
                new = state.advance_newline(newlines)
                if new:
                    count += 1
                    state = new
                else:
                    break

            for ws in literals:
                new = state.advance(ws)
                if new:
                    count += 1
                    state = new
                    break
            else: # the worst construct in python
                if newline:
                    new = state.advance_newline(newlines)
                    if new:
                        count += 1
                        state = new
                        continue
                break
            continue
        if count >= min:
            return state

    def advance_eof(self):
        if self.offset == len(self.buf):
            return self

    def advance_newline(self, literals):
        for nl in literals:
            new = self.advance(nl)
            if new:
                return new.clone(line_start=new.offset)

    def advance_indent(self, count, tabstop, literals, newlines):
        state = self
        stop = count
        offset = self.offset
        while stop > 0 and self.offset < len(self.buf):
            if self.buf[offset] in literals:
                stop -= 8 if self.buf[offset] == '\t' else 1 
                offset += 1
            elif self.buf[offset] in newlines:
                break
            else:
                offset = -1
                break
        if offset != -1:
            return state.clone(offset=offset)

    def advance_range(self, text):
        if '-' in text[1:2]:
            start, end = ord(text[0]), ord(text[2])
            # print(start, end, repr(text))
            if start <= ord(self.buf[self.offset]) <= end:
                return self.clone(offset=self.offset + 1)
        elif self.buf[self.offset:].startswith(text):
            return self.clone(offset=self.offset + len(text))

    def substring(self, end):
        return self.buf[self.offset:end.offset]

    def advance_any(self, n):
        return self.clone(offset = self.offset+n)

    def capture(self):
        return self.clone(children=[], parent=self)

    def build_node(self, name):
        self.parent.children.append(ParseNode(name, self.parent.offset, self.offset, self.children, None))
        return self.clone(children=self.parent.children, parent=self.parent.parent)

    def build_capture(self, builder):
        self.parent.children.append(builder(self.buf, self.parent.offset, self.offset, self.children))
        return self.clone(children=self.parent.children, parent=self.parent.parent)

    def merge_parent(self):
        self.parent.children.append(self.children)
        return self.clone(children=self.parent.children, parent=self.parent.parent)

    def add_child(self, value):
        self.children.append(value)

    def add_child_node(self, value):
        value = ParseNode('value', self.offset, self.offset, [],value)
        self.children.append(value)

class ParseNode:
    def __init__(self, name, start, end, children, value):
        self.name = name
        self.start = start
        self.end = end
        self.children = children
        self.value = value

    def build(self, buf, builder):
        children = [child.build(buf, builder) for child in self.children]
        if self.name == "value": return self.value
        return builder[self.name](buf, self.start, self.end, children)

    def walk_top(self):
        yield self
        for child in self.children:
            yield from child.walk_top()

    def __str__(self):
        # children = ", ".join(str(x) for x in self.children)
        # children = " ({})".format(children) if children else ""
        # return "{}[{}:{}]{}".format(self.name, self.start, self.end, children)
        return "{}[{}:{}]".format(self.name, self.start, self.end)

class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.builder = None
        self.tabstop = 8

    def parse(self, buf, offset=0, err=None, builder=None):
        name = self.grammar.start
        rule = self.grammar.rules[name]

        start = ParserState.init(buf, offset)
        end = self.parse_rule(rule, start)

        if end is None:
            if err is None: return
            raise err(buf, offset, "no")
        if builder:
            return start.children[-1].build(builder)
        return ParseNode(self.grammar.capture, start.offset, end.offset, start.children, None)

    def parse_rule(self, rule, state):
        if rule.kind == PRINT:
            args = [state.values.get(a,a) for a in rule.args['args']]
            print('print', *args)
            return state

        elif rule.kind == TRACE:
            print('trace', repr(state.buf[state.offset:state.offset+5]),"...")
            for step in rule.rules:
                print('trace', state.offset, step.kind)
                state = self.parse_rule(step, state)
                if state is None:
                    print('trace', 'fail')
                    return None
            print('trace', 'ok', state.offset)
            return state

        elif rule.kind == RULE:
            name = rule.args['name']
            new_state = state.clone(values={})
            new_state = self.parse_rule(self.grammar.rules[name], new_state)
            if new_state:
                new_state.values = state.values
            return new_state

        elif rule.kind == END_OF_FILE:
            if state.offset == len(state.buf):
                return state
            return

        elif rule.kind == NEWLINE:
            return state.advance_newline(self.grammar.newline)

        elif rule.kind == END_OF_LINE:
            if state.offset == len(state.buf):
                return state
            return state.advance_newline(self.grammar.newline)

        elif rule.kind == WHITESPACE:
            _min, _max = rule.args['min'], rule.args['max']
            _newline = rule.args['newline']
            _min = state.values.get(_min, _min)
            _max = state.values.get(_max, _max)
            return state.advance_whitespace(self.grammar.whitespace, self.grammar.newline, _min, _max, _newline)

        elif rule.kind == INDENT:
            return state.advance_prefix()
        elif rule.kind == START_OF_LINE:
            if self.offset != self.line_start:
                return None
            return state

        elif rule.kind == SET_LINE_PREFIX:
            if rule.args['indent']: raise Exception('unfinished')
            state = state.set_indent(self.grammar.tabstop, self.grammar.whitespace, self.grammar.newline)
            for step in rule.rules:
                state = self.parse_rule(step, state)
                if state is None:
                    return None
            # print('exit', state.offset, repr(state.buf[state.offset:]), state.indent)
            return state.pop_indent()

        elif rule.kind == CHOICE:
            for option in rule.rules:
                # print('choice', repr(state.buf[state.offset:state.offset+5]), option)
                s = self.parse_rule(option, state.choice())
                if s is not None:
                    return state.merge_choice(s)

        elif rule.kind == SEQUENCE:
            for step in rule.rules:
                state = self.parse_rule(step, state)
                if state is None:
                    return None
            return state

        elif rule.kind == CAPTURE:
            name = rule.args['name']
            end = state.capture()
            for step in rule.rules:
                end = self.parse_rule(step, end)
                if end is None:
                    break
            if end:
                if self.builder:
                    return end.build_capture(self.builder[name])
                else:
                    return end.build_node(name)
            return None
        elif rule.kind == REJECT_IF:
            cond = rule.args['cond']
            if cond.calculate(state.values):
                return None
            return state

        elif rule.kind == ACCEPT_IF:
            cond = rule.args['cond']
            if cond.calculate(state.values):
                return state
            return None

        elif rule.kind == COUNT:
            start = state.offset

            for step in rule.rules:
                state = self.parse_rule(step, state)
                if state is None:
                    return
                    break
            char = rule.args['char']
            key = rule.key
            buf = state.buf[start:state.offset]
            # print('count', char,'in',buf, '=',buf.count(char))
            state.values[key] = buf.count(char)
            return state

        elif rule.kind == VALUE:
            value = rule.args['value']
            value = state.values.get(value, value)

            if self.builder:
                state.add_child(value)
            else:
                state.add_child_node(value)
            return state

        elif rule.kind == LOOKAHEAD:
            new_state = state.capture()
            for step in rule.rules:
                new_state = self.parse_rule(step, new_state)
                if new_state is None:
                    return None
            return state

        elif rule.kind == REJECT:
            new_state = state.capture()
            for step in rule.rules:
                new_state = self.parse_rule(step, new_state)
                if new_state is None:
                    return state
            return None

        elif rule.kind == REPEAT:
            start, end = rule.args['min'], rule.args['max']
            start = state.values.get(start, start)
            end = state.values.get(end, end)
            c= 0
            while c < start:
                start_offset = state.offset
                new = state.choice()
                for step in rule.rules:
                    # print('rep', repr(state.buf[state.offset:state.offset+5]), step, rule)
                    new = self.parse_rule(step, new)
                    if new is None:
                        return None
                state = state.merge_choice(new)
                c+=1
            while end is None or c < end:
                new = state.choice()
                for step in rule.rules:
                    # print('rep+', repr(state.buf[state.offset:state.offset+5]), step, rule)
                    new = self.parse_rule(step, new)
                    if new is None:
                        state.values[rule.key] = c
                        return state
                if new.offset == state.offset:
                    state.values[rule.key] = c
                    return state
                state = state.merge_choice(new)
                c+=1
            state.values[rule.key] = c
            return state

        elif rule.kind == LITERAL:
            literals = rule.args['literals']
            for text in literals:
                new_state = state.advance(text)
                if new_state:
                    return new_state

        elif rule.kind == RANGE:
            if state.offset == len(state.buf):
                return None

            if rule.args['invert']:
                # print(rule, state.buf[state.offset:], rule.args)
                for text in rule.args['range']:
                    new_state = state.advance_range(text)
                    #  print(new_state, repr(text))
                    if new_state:
                        return
                # print(rule, 'advance')
                return state.clone(offset=state.offset+1)
            else:
                for text in rule.args['range']:
                    new_state = state.advance_range(text)
                    if new_state:
                        return new_state
        else:
            raise Exception(rule.kind)


class ParserBuilder:
    def __init__(self, output, indent):
        self.output = output
        self.indent = indent

    def add_indent(self, n=4):
        return ParserBuilder(self.output, self.indent+n)

    def append(self, line):
        self.output.append(f"{' ' * self.indent}{line}")

    def as_string(self):
        return "\n".join(self.output)

    def extend(self, lines):
        for line in lines:
            self.output.append(f"{' ' * self.indent}{line}")


class VarBuilder:
    def __init__(self, name, n=0):
        self.n = n
        self.name = name

    def __str__(self):
        return f"{self.name}_{self.n}" # if self.n else self.name

    def incr(self):
        return VarBuilder(self.name, self.n+1)

def compile(grammar, builder=None):

    def build_subrules(rules, steps, state, count):
        for subrule in rules:
            build_steps(subrule, steps, state, count)

    def build_steps(rule, steps, state, count):
        # steps.append(f"print('start', {repr(str(rule))})")
        if rule.kind == SEQUENCE:
            build_subrules(rule.rules, steps, state, count)

        elif rule.kind == CAPTURE:
            name = repr(rule.args['name'])
            steps.append(f"{state} = {state}.capture()")
            steps.append(f"while True: # start capture")
            build_subrules(rule.rules, steps.add_indent(), state, count)
            steps.append(f"    break")
            steps.append(f"if {state} is None: break")
            if builder:
                steps.append(f"{state} = {state}.build_capture(self.builder[{name}])")
            else:
                steps.append(f"{state} = {state}.build_node({name})")

        elif rule.kind == CHOICE:
            steps.append(f"while True: # start choice")
            choice = state.incr()
            steps_0 = steps.add_indent()
            for subrule in rule.rules:
                steps_0.append(f"{choice} = {state}.choice()")
                # steps_0.append(f"print('choice')")
                steps_0.append(f"while True: # case")
                build_steps(subrule, steps_0.add_indent(), choice, count)
                steps_0.append(f"    break")
                steps_0.append(f"if {choice} is not None:")
                steps_0.append(f"    {state} = {state}.merge_choice({choice})")
                steps_0.append(f"    break")
                steps_0.append(f"# end case")
                # steps_0.append(f"print('next_choice')")
                steps_0.append(f"")

            steps_0.append(f"{state} = None")
            # steps_0.append(f"print('choice failed')")
            steps_0.append(f"break # end choice")
            steps.extend((
                f"if {state} is None: break",
                f"",
            ))

        elif rule.kind == REPEAT:
            _min = rule.args['min']
            _max = rule.args['max']
            steps.append(f"{count} = 0")
            new_count = count.incr()
            state_0 = state.incr()
            if _min is not None and _min > 0:
                _min = repr(_min) # value todo
                steps.append(f"while {count} < {_min}:")
                steps.append(f"{state_0} = {state}.choice()")
                build_subrules(rule.rules, steps.add_indent(), state_0, new_count)
                steps.append(f"    count += 1")
                steps.appena(f"    {state}.merge_choice({state_0})")
                steps.append(f"if {state} is None: break")

            if _max is not None and _max > 1:
                _max = repr(_max) # value todo
                steps.append(f"while {count} < {_max}:")
            else:
                steps.append(f"while True:")

            state_0 = state.incr()
            steps_0 = steps.add_indent()
            steps_0.append(f"{state_0} = {state}")
            for subrule in rule.rules:
                build_steps(subrule, steps_0, state_0, new_count)
            steps_0.append(f"if {state}.offset == {state_0}.offset: break")
            steps_0.append(f"{state} = {state_0}")
            steps_0.append(f"{count} += 1")
            if _max == "1":
                steps_0.append(f"break")

            steps.append("")

        elif rule.kind == LOOKAHEAD:
            state_0 = state.incr()
            steps_0 = steps.add_indent()
            steps.append(f"while True: # start lookahead")
            steps_0.append(f"{state_0} = {state}.capture()")
            build_subrules(rule.rules, steps_0, state_0, count)

            steps.append(f'if {state_0} is None:')
            steps.append(f'    {state} = None')
            steps.append(f'    break')

        elif rule.kind == REJECT:
            steps_0 = steps.add_indent()
            state_0 = state.incr()
            steps.append(f"while True: # start reject")
            steps_0.append(f"{state_0} = {state}.capture()")
            build_subrules(rule.rules, steps_0, state_0, count)

            steps.append(f'if {state_0} is not None:')
            steps.append(f'    {state} = None')
            steps.append(f'    break')

        elif rule.kind == ACCEPT_IF:
            steps.append(f'raise Exception("{rule.kind} missing") # unfinished {rule}')

        elif rule.kind == REJECT_IF:
            steps.append(f'raise Exception("{rule.kind} missing") # unfinished {rule}')

        elif rule.kind == COUNT:
            steps.append(f'raise Exception("{rule.kind} missing") # unfinished {rule}')

        elif rule.kind == VALUE:
            steps.append(f'raise Exception("{rule.kind} missing") # unfinished {rule}')

        elif rule.kind == SET_LINE_PREFIX:
            steps.append(f'{state} = {state}.set_indent(self.tabstop, self.WHITESPACE, self.NEWLINE)')
            steps.append('while True:')
            build_subrules(rule.rules, steps.add_indent(), state, count)
            steps.apppend('    break')
            steps.append(f'if {state}: {state} = {state}.pop_indent()')
            steps.extend((
                f"if {state} is None:",
                f"    break",
                f"",
            ))

        elif rule.kind == START_OF_LINE:
            steps.extend((
                f"if {state}.line_start != {state}.offset:",
                f"    break",
                f"",
            ))

        elif rule.kind == INDENT:
            steps.extend((
                f"{state} = {state}.advance_prefix()",
                f"if {state} is None:",
                f"    break",
                f"",
            ))

        elif rule.kind == RULE:
            steps.extend((
                f"{state} = self.parse_{rule.args['name']}({state})",
                f"if {state} is None: break",
                f"",
            ))

        elif rule.kind == RANGE:
            invert = rule.args['invert']
            steps.append(f'if {state}.advance_eof():')
            steps.append(f'    {state} = None')
            steps.append(f'    break')
            state_0 = state.incr()
            steps_0 = steps.add_indent()
            if len(rule.args['range']) > 1:
                steps.append(f'while True:')
                for literal in rule.args['range']:
                    literal = repr(literal)
                    steps_0.append(f"{state_0} = {state}.advance_range({literal})")
                    steps_0.append(f"if {state_0} is not None: break")
                steps_0.append('break')
            else:
                literal = repr(rule.args['range'][0])
                steps.append(f"{state_0} = {state}.advance_range({literal})")

            if not invert:
                steps.append(f'{state} = {state_0}')
                steps.append(f'if {state} is None: break')
            else:
                steps.append(f'if {state_0} is not None:')
                steps.append(f'    {state} = None')
                steps.append(f'    break')
                steps.append(f'else:')
                steps.append(f'    {state} = {state}.advance_any(1)')

            steps.append('')




        elif rule.kind == LITERAL:
            if len(rule.args['literals']) > 1:
                steps.append(f'while True:')
                state_0 = state.incr()
                steps_0 = steps.add_indent()
                for literal in rule.args['literals']:
                    literal = repr(literal)
                    steps_0.append(f"{state_0} = {state}.advance({literal})")
                    steps_0.append(f"if {state_0} is not None: break")
                steps_0.append('break')
                steps.append(f'{state} = {state_0}')
                steps.append(f'if {state} is None: break')
            else:
                literal = repr(rule.args['literals'][0])
                steps.append(f"{state} = {state}.advance({literal})")
                steps.append(f"if {state} is None: break")

            steps.append(f'')

        elif rule.kind == WHITESPACE:
            _min, _max = rule.args['min'], rule.args['max']
            _newline = rule.args['newline']
            steps.append(f"{state} = {state}.advance_whitespace(self.WHITESPACE, self.NEWLINE, {repr(_min)}, {repr(_max)}, {repr(_newline)})")
            if _min is not None and _min > 0:
                steps.append(f"if {state} is None: break")
            steps.append(f"")

        elif rule.kind == NEWLINE:
            steps.extend((
                f"{state} = {state}.advance_newline(self.NEWLINE)",
                f"if {state} is None: break",
                f"",
            ))
        elif rule.kind == END_OF_LINE:
            steps.extend((
                f"if {state}.offset != len({state}.buf):",
                f"    {state} = {state}.advance_newline(self.NEWLINE)",
                f"    if {state} is None: break",
            ))
        elif rule.kind == END_OF_FILE:
            steps.extend((
                f"if {state}.offset != len({state}.buf):",
                f"    {state} = None",
                f"    break",
            ))

        elif rule.kind == PRINT:
            steps.append(f'raise Exception("{rule.kind} missing") # unfinished {rule}')
        elif rule.kind == TRACE:
            steps.append(f'raise Exception("{rule.kind} missing") # unfinished {rule}')
        else:
            raise Exception(f'Unknown kind {rule.kind}')

        # steps.append(f"print('end', {repr(str(rule))}, {state})")
        return steps

    output = ParserBuilder([], 0)
    newline = repr(tuple(grammar.newline)) if grammar.newline else '()'
    whitespace = repr(tuple(grammar.whitespace)) if grammar.whitespace else '()'

    output.append("def closure(ParserState):")
    output = output.add_indent(4)
    output.extend((
        f"class Parser:",
        f"    def __init__(self, builder=None):",
        f"         self.builder = None",
        f"         self.tabstop = self.TABSTOP",
        "",
        f"    NEWLINE = {newline}",
        f"    WHITESPACE = {whitespace}",
        f"    TABSTOP = {repr(grammar.tabstop)}",
        "",
    ))

    output = output.add_indent(4)

    start_rule = grammar.start
    output.extend((
        f"def parse(self, buf, offset=0, builder=None):",
        f"    start = ParserState.init(buf, offset)",
        f"    end = self.parse_{start_rule}(start)",
        f"    if not end: return None",
        f"    if builder is not None: return start.children[-1].build(builder)",
        f"    return ParseNode({repr(grammar.capture)}, start.offset, end.offset, start.children, None) if end else None",
        f"",
    ))

    for name, rule in grammar.rules.items():
        output.append(f"def parse_{name}(self, state_0):")
        # output.append(f"    print('{name}')")
        output.append(f"    while True: # note: return at end of loop")

        build_steps(rule, output.add_indent(8), VarBuilder("state"), VarBuilder("count"))
        output.append(f"        break")
        # output.append(f"    print('exit {name}', state)")
        output.append(f"    return state_0")
        output.append("")

    output = output.add_indent(-4)
    output.append("return Parser")

    glob, loc = {}, {}
    # for lineno, line in enumerate(output.output):
    #    print(lineno, '\t', line)
    exec(output.as_string(), glob, loc)
    return loc['closure'](ParserState)(builder)

