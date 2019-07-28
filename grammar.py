from contextlib import contextmanager
from types import FunctionType

class GrammarNode:
    pass

class FunctionNode(GrammarNode):
    def __init__(self, fn, wrapper):
        self.fn = fn
        self.wrapper = wrapper

    def canonical(self, builder):
        return self.wrapper(builder.from_function(self.fn))

class NamedNode(GrammarNode):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __or__(self, right):
        return ChoiceNode([self, right])

    def canonical(self, builder):
        return self

    def make_rule(self):
        return ParserRule("rule", args=dict(name=self.name))

class ChoiceNode(GrammarNode):
    def __init__(self, rules):
        self.rules = rules
    def __str__(self):
        return f"({' | '.join(str(x) for x in self.rules)})"
    def __or__(self, right):
        rules = list(self.rules)
        rules.append(right)
        return ChoiceNode(rules)

    def canonical(self, builder):
        rules = [r.canonical(builder) for r in self.rules]
        if len(rules) == 1:
            return rules[0]
        return ChoiceNode(rules)

    def make_rule(self):
        return ParserRule("choice", rules=[r.make_rule() for r in self.rules])

class SequenceNode(GrammarNode):
    def __init__(self, rules):
        self.rules = rules
    def __str__(self):
        return f"({' '.join(str(x) for x in self.rules)})"

    def canonical(self, builder):
        rules = [r.canonical(builder) for r in self.rules]
        if len(rules) == 1:
            return rules[0]
        return SequenceNode(rules)

    def make_rule(self):
        return ParserRule("seq", rules=[r.make_rule() for r in self.rules])

class BlockNode(GrammarNode):
    def __init__(self, kind, rules):
        self.kind = kind
        self.rules = rules
    def __str__(self):
        return f"{self.kind} ({' '.join(str(x) for x in self.rules)})"

    def canonical(self, builder):
        rules = [r.canonical(builder) for r in self.rules]
        return self.__class__(rules)

    def make_rule(self):
        return ParserRule(self.kind, rules=[r.make_rule() for r in self.rules])

class ValueNode(GrammarNode):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"({self.value})"

    def canonical(self, builder):
        return self

    def make_rule(self):
        return ParserRule('value', args=dict(value=self.value))

class CaptureNode(GrammarNode):
    def __init__(self, name, rules):
        self.rules = rules
        self.name = name
    def __str__(self):
        return f"({' '.join(str(x) for x in self.rules)})"

    def canonical(self, builder):
        rules = [r.canonical(builder) for r in self.rules]
        return CaptureNode(self.name, rules)
    def make_rule(self):
        return ParserRule("capture", args=dict(name=self.name), rules=[r.make_rule() for r in self.rules])

class RepeatNode(GrammarNode):
    def __init__(self, rules, min=0, max=None, key=None):
        self.min = min
        self.max = max
        self.rules = rules
        self.key = key if key is not None else object()

    def __str__(self):
        if self.min == 0 and self.max == 1:
            return f"({' '.join(str(x) for x in self.rules)})?"
        elif self.min == 0 and self.max == None:
            return f"({' '.join(str(x) for x in self.rules)})*"
        elif self.min == 1 and self.max == None:
            return f"({' '.join(str(x) for x in self.rules)})+"
        elif self.min == 0:
            return f"({' '.join(str(x) for x in self.rules)})^{{,{self.max}}}"
        elif self.max == None:
            return f"({' '.join(str(x) for x in self.rules)})^{{{self.min},}}"
        else:
            return f"({' '.join(str(x) for x in self.rules)})^{{{self.min},{self.max}}}"
    def canonical(self, builder):
        rules = [r.canonical(builder) for r in self.rules]
        return RepeatNode(rules, self.min, self.max, self.key)
    def make_rule(self):
        return ParserRule("repeat", args=dict(min=self.min, max=self.max, key=self.key), rules=[r.make_rule() for r in self.rules])

class IndentNode(GrammarNode):
    def __init__(self, rules):
        self.rules = rules

    def canonical(self, builder):
        return self

    def __str__(self):
        return "<indent {}>".format(",".join(str(x) for x in self.rules))
    def make_rule(self):
        return ParserRule("set-indent", rules=[r.make_rule() for r in self.rules])

class BuiltinNode(GrammarNode):
    def __init__(self, kind, min=0, max=None):
        self.kind = kind
        self.min = min
        self.max = max

    def canonical(self, builder):
        return self

    def __str__(self):
        return self.kind

    def make_rule(self):
        return ParserRule(self.kind, args=dict(min=self.min, max=self.max))

class LiteralNode(GrammarNode):
    def __init__(self, args,invert=False):
        self.args = args
        self.invert = invert

    def canonical(self, rulebuilder):
        return self

    def __str__(self):
        if len(self.args) == 1:
            return "{!r}".format(self.args[0])
        return "|".join("{}".format(repr(a)) for a in self.args)

    def make_rule(self):
        return ParserRule("literal", rules=self.args, args={'invert': self.invert})

class PrintNode(GrammarNode):
    def __init__(self, args):
        self.args = args

    def canonical(self, rulebuilder):
        return self

    def __str__(self):
        return "<print>"

    def make_rule(self):
        return ParserRule("print",args={'args': self.args})

class ConditionNode(GrammarNode):
    def __init__(self, name, cond):
        self.name = name
        self.cond = cond
    def canonical(self, rulebuilder):
        return self

    def __str__(self):
        return "<cond>"

    def make_rule(self):
        return ParserRule(self.name,args={'cond': self.cond})

class RangeNode(GrammarNode):
    def __init__(self, args,invert):
        self.args = args
        self.invert = invert

    def canonical(self, rulebuilder):
        return self

    def __str__(self):
        invert = "^" if self.invert else ""
        if len(self.args) == 1:
            return "[{}{}]".format(invert, self.args[0])
        return "[{}{}]".format(invert, "".join(repr(a)[1:-1] for a in self.args))
    def make_rule(self):
        return ParserRule("range", args=dict(invert=self.invert, range=self.args))

class RecursiveNode(GrammarNode):
    def __init__(self, args):
        self.args = args

    def canonical(self, rulebuilder):
        args = [[r.canonical(rulebuilder) for r in rules] for rules in self.args]
        return RecursiveNode(args)

    def __str__(self):
        def _fmt(args):
            return "({})".format(",".join(str(x) for x in args))
        return "<recursive {}>".format("|".join("{}".format(_fmt(a)) for a in self.args))

    def make_rule(self):
        return ParserRule("recursive", args=args)

class OperatorNode(GrammarNode):
    def __init__(self, direction, rule):
        self.direction = direction
        self.rule = rule

    def canonical(self, rulebuilder):
        return OperatorNode(self.direction, self.rule.canonical(rulebuilder))

    def __str__(self):
        return "<{} {}>".format(self.direction, self.rule)

    def make_rule(self):
        return ParserRule("operator", args=self.direction, rules=[self.rule])
# Builders
#

class FunctionBuilder:
    def __init__(self, names):
        self.rules = None
        self.block_mode = "build"
        for name, rule in names.items():
            if hasattr(self, name): raise SyntaxError()
            def callback(rule=rule):
                self.rule(rule)
            setattr(self, name, callback)

    def rule(self, rule):
        if self.block_mode: raise SyntaxError()
        self.rules.append(rule)

    def accept(self, *args):
        if self.block_mode: raise SyntaxError()
        self.rules.append(LiteralNode(args))

    def whitespace(self, min=0, max=None):
        if self.block_mode: raise SyntaxError()
        self.rules.append(BuiltinNode("whitespace", min, max))

    def capture_value(self, value):
        if self.block_mode: raise SyntaxError()
        self.rules.append(ValueNode(value))

    def newline(self, *args, exclude=None):
        if self.block_mode: raise SyntaxError()
        self.rules.append(BuiltinNode("newline"))

    def eof(self, *args, exclude=None):
        if self.block_mode: raise SyntaxError()
        self.rules.append(BuiltinNode("eof"))

    def range(self, *args, invert=False):
        if self.block_mode: raise SyntaxError()
        self.rules.append(RangeNode(args, invert))

    def indent(self):
        if self.block_mode: raise SyntaxError()
        self.rules.append(BuiltinNode("match-indent"))
    def print(self, *args):
        if self.block_mode: raise SyntaxError()
        self.rules.append(PrintNode(args))

    def reject_if(self, cond):
        if self.block_mode: raise SyntaxError()
        self.rules.append(ConditionNode('reject-if', cond))

    def accept_if(self, cond):
        if self.block_mode: raise SyntaxError()
        self.rules.append(ConditionNode('accept-if', cond))


    @contextmanager
    def indented(self):
        if self.block_mode: raise SyntaxError()
        rules, self.rules = self.rules, []
        yield
        rules.append(IndentNode(self.rules))
        self.rules = rules
        
    @contextmanager
    def count(self, char):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        counter = CountNode(char, self.rules)
        yield counter.key
        rules.append(counter)
        self.rules = rules

    @contextmanager
    def capture(self, name):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        yield
        rules.append(CaptureNode(name, self.rules))
        self.rules = rules

    @contextmanager
    def trace(self):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        yield
        rules.append(BlockNode('trace', self.rules))
        self.rules = rules

    @contextmanager
    def lookahead(self):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        yield
        rules.append(BlockNode('lookahead', self.rules))
        self.rules = rules

    @contextmanager
    def reject(self):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        yield
        rules.append(BlockNode('reject', self.rules))
        self.rules = rules

    @contextmanager
    def choice(self):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        self.block_mode = "choice"
        yield
        if self.block_mode != "choice": raise SyntaxError()
        self.block_mode = None
        rules.append(ChoiceNode(self.rules))
        self.rules = rules

    @contextmanager
    def case(self):
        if self.block_mode != "choice": raise SyntaxError()
        rules = self.rules
        self.rules = []
        self.block_mode = None
        yield
        if self.block_mode: raise SyntaxError()
        self.block_mode = "choice"
        rules.append(SequenceNode(self.rules))
        self.rules = rules

    @contextmanager
    def repeat(self, min=0, max=None):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        r = RepeatNode(self.rules, min=min, max=max)
        yield r.key
        rules.append(r)
        self.rules = rules

    @contextmanager
    def optional(self):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        yield
        rules.append(RepeatNode(self.rules, min=0, max=1))
        self.rules = rules

    def from_function(self, fn):
        if self.block_mode != "build": raise SyntaxError()
        self.block_mode = None
        self.rules = []

        fn(self)

        if self.block_mode: raise SyntaxError()
        self.block_mode = "build"
        rules, self.rules = self.rules, None

        return rules

class CountNode(GrammarNode):
    def __init__(self, char, rules, key=None):
        self.char = char
        self.rules = rules
        self.key = object() if key is None else key 
    def __str__(self):
        return f"'count {self.char}' in ({' '.join(str(x) for x in self.rules)})"

    def canonical(self, builder):
        rules = [r.canonical(builder) for r in self.rules]
        return CountNode(self.name, rules, self.key)
    def make_rule(self):
        return ParserRule("count", args=dict(char=self.char, key=self.key), rules=[r.make_rule() for r in self.rules])

class Builtins:
    """ These methods are exported as functions inside the class defintion """
    def rule(*args, inline=False, capture=None):
        def _wrapper(rules):
            if capture:
                return CaptureNode(capture, rules)
            elif len(rules) > 1:
                return SequenceNode(rules)
            else:
                return rules[0]
        if len(args) > 0:
            return GrammarRule(_wrapper(args))
        else:
            def _decorator(fn):
                return GrammarRule(FunctionNode(fn, _wrapper))
            return _decorator

    def recursive(*args):
        if len(args) > 0:
            return GrammarRule(RecursiveNode(args))
        else:
            raise SyntaxError()

    def operator(*args, capture=None, kind="left"):
        def _wrapper(rules):
            if capture:
                return OperatorNode(kind, CaptureNode(capture, rules))
            elif len(rules) > 1:
                return OperatorNode(kind, SequenceNode(rules))
            else:
                return OperatorNode(kind, rules[0])
        if len(args) > 0:
            return GrammarRule(_wrapper(args))
        else:
            def _decorator(fn):
                return GrammarRule(FunctionNode(fn, _wrapper))
            return _decorator

    def left(*args, capture=None):
        return Builtins.operator(*args, capture=capture, kind="left")

    def right(*args, capture=None):
        return Builtins.operator(*args, capture=capture, kind="right")

    def capture(name, *args):
        return CaptureNode(name, args)
    def capture_value(arg):
        return ValueNode(arg)
    def accept(*args):
        return LiteralNode(args)
    def reject(*args):
        return BlockNode('reject', args)
    def lookahead(*args):
        return BlockNode('lookahead', args)
    def trace(*args):
        return BlockNode('trace', args)
    def range(*args, exclude=None):
        return RangeNode(args, exclude)
    def repeat(*args, min=0, max=None):
        return RepeatNode(args, min=min, max=max)
    def optional(*args):
        return RepeatNode(args, min=0, max=1)
    def choice(*args):
        return ChoiceNode(args)
    whitespace = BuiltinNode("whitespace")
    eof = BuiltinNode('eof')
    newline = BuiltinNode("newline")

class ParserRule:
    def __init__(self, kind, *, args=None, rules=()):
        self.kind = kind
        self.args = args if args else {}
        self.rules = rules

    def __str__(self):
        return "({} {})".format(self.kind, ", ".join(str(r) for r in self.rules))

# Parser



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
        return new.clone(children = self.children+new.children)

    def set_indent(self):
        return self.clone(indent=(self.offset-self.line_start, self.indent))

    def pop_indent(self):
        return self.clone(indent=self.indent[1])

    def advance(self, text):
        if self.buf[self.offset:].startswith(text):
            return self.clone(offset=self.offset + len(text))

    def advance_whitespace(self, literals, min=0, max=None):
        state = self
        count = 0
        while max is None or count < max:
            for ws in literals:
                new = state.advance(ws)
                if new:
                    count += 1
                    state = new
                    break
            else:
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

    def advance_indent(self, literals):
        # print(self.line_start, self.offset, self.indent)
        state = self
        stop = self.line_start + self.indent[0]
        while state.offset < stop:
            for ws in literals:
                new = state.advance(ws)
                if new:
                    state = new
                    break
            else:
                break
        if state.offset == stop:
            return state

    def advance_range(self, text):
        if '-' in text[1:2]:
            start, end = ord(text[0]), ord(text[2])
            if start <= ord(self.buf[self.offset]) <= end:
                return self.clone(offset=self.offset + 1)
        elif self.buf[self.offset:].startswith(text):
            return self.clone(offset=self.offset + len(text))

    def substring(self, end):
        return self.buf[self.offset:end.offset]


    def capture(self):
        return self.clone(children=[], parent=self)

    def build_node(self, name):
        self.parent.children.append(ParseNode(name, self.parent.offset, self.offset, self.children, None))
        return self.clone(children=self.parent.children, parent=self.parent.parent)

    def build_capture(self, builder):
        self.parent.children.append(builder(self.parent.substring(self), self.children))
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
        return builder[self.name](buf[self.start:self.end], children)

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
    def __init__(self, grammar, builder):
        self.grammar = grammar
        self.builder = builder

    def parse(self, buf, offset=0):
        name = self.grammar.start
        rule = self.grammar.rules[name]

        start = ParserState.init(buf, offset)
        end = self.parse_rule(rule, start)

        if end is None:
            return

        return start.children[-1]

    def parse_rule(self, rule, state):
        if rule.kind == "print":
            args = [state.values.get(a,a) for a in rule.args['args']]
            print('print', *args)
            return state

        elif rule.kind == "trace":
            print('trace', repr(state.buf[state.offset:state.offset+5]),"...")
            for step in rule.rules:
                print('trace', state.offset, step.kind)
                state = self.parse_rule(step, state)
                if state is None:
                    print('trace', 'fail')
                    return None
            print('trace', 'ok', state.offset)
            return state
        
        elif rule.kind == "rule":
            name = rule.args['name']
            new_state = state.clone(values={})
            new_state = self.parse_rule(self.grammar.rules[name], new_state)
            if new_state:
                new_state.values = state.values
            return new_state

        elif rule.kind == "eof":
            if state.offset == len(state.buf):
                return state
            return

        elif rule.kind == "whitespace":
            _min, _max = rule.args['min'], rule.args['max']
            _min = state.values.get(_min, _min)
            _max = state.values.get(_max, _max)
            return state.advance_whitespace(self.grammar.whitespace, _min, _max)

        elif rule.kind == "newline":
            return state.advance_newline(self.grammar.newline)

        elif rule.kind == "match-indent":
            return state.advance_indent(self.grammar.whitespace)
        elif rule.kind == "set-indent":
            state = state.set_indent()
            for step in rule.rules:
                state = self.parse_rule(step, state)
                if state is None:
                    return None
            # print('exit', state.offset, repr(state.buf[state.offset:]), state.indent)
            return state.pop_indent()

        elif rule.kind == "choice":
            for option in rule.rules:
                # print('choice', repr(state.buf[state.offset:state.offset+5]), option)
                s = self.parse_rule(option, state.choice())
                if s is not None:
                    return state.merge_choice(s)
        elif rule.kind == "seq":
            for step in rule.rules:
                state = self.parse_rule(step, state)
                if state is None:
                    return None
            return state
        elif rule.kind == "capture":
            start = state
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
        elif rule.kind == "reject-if":
            cond = rule.args['cond']
            if cond.calculate(state.values):
                return None
            return state

        elif rule.kind == "accept-if":
            cond = rule.args['cond']
            if cond.calculate(state.values):
                return state
            return None
        elif rule.kind == "count":
            start = state.offset
            
            for step in rule.rules:
                state = self.parse_rule(step, state)
                if state is None:
                    return
                    break
            char = rule.args['char']
            key = rule.args['key']
            buf = state.buf[start:state.offset]
            print('count', char,'in',buf, '=',buf.count(char))
            state.values[key] = buf.count(char)
            return state
        elif rule.kind == "value":
            value = rule.args['value']
            value = state.values.get(value, value)

            if self.builder:
                state.add_child(value)
            else:
                state.add_child_node(value)
            return state

        elif rule.kind == "lookahead":
            new_state = state.capture()
            for step in rule.rules:
                new_state = self.parse_rule(step, new_state)
                if new_state is None:
                    return None
            return state

        elif rule.kind == "reject":
            new_state = state.capture()
            for step in rule.rules:
                new_state = self.parse_rule(step, new_state)
                if new_state is None:
                    return state
            return None

        elif rule.kind == "repeat":
            start, end = rule.args['min'], rule.args['max']
            start = state.values.get(start, start)
            end = state.values.get(end, end)
            c= 0
            while c < start:
                start_offset = state.offset
                for step in rule.rules:
                    # print('rep', repr(state.buf[state.offset:state.offset+5]), step, rule)
                    state = self.parse_rule(step, state)
                    if state is None:
                        return None
                c+=1
            while end is None or c < end:
                old = state
                for step in rule.rules:
                    # print('rep+', repr(state.buf[state.offset:state.offset+5]), step, rule)
                    new_state = self.parse_rule(step, state)
                    if new_state is None:
                        old.values[rule.args['key']] = c
                        return old
                    state = new_state
                if old.offset == state.offset:
                    state.values[rule.args['key']] = c
                    return state
                old = state
                c+=1
            state.values[rule.args['key']] = c
            return state

        elif rule.kind == "literal":
            if rule.args['invert']:
                for text in rule.rules:
                    if state.advance(text):
                        return None
                return state
            else:
                for text in rule.rules:
                    new_state = state.advance(text)
                    if new_state:
                        return new_state

        elif rule.kind == "range":
            if state.offset == len(state.buf):
                return None
            if rule.args['invert']:
                # print(rule, state.buf[state.offset:], rule.args)
                for text in rule.args['range']:
                    new_state = state.advance_range(text)
                    # print(new_state, text)
                    if new_state:
                        return
                return state.clone(offset=state.offset+1)
            else:
                for text in rule.args['range']:
                    new_state = state.advance_range(text)
                    if new_state:
                        return new_state
        else:
            raise Exception(rule.kind)
                
# Grammar

class GrammarRule:
    def __init__(self, rule):
        self.rule = rule

    def canonical(self, builder):
        return self.rule.canonical(builder)

class GrammarRuleSet:
    """ Allows for multiple definitions of rules """

    def __init__(self, rules):
        self.rules = rules

    def append(self, value):
        rule = value.rule
        if rule is self: raise Exception()
        if isinstance(rule, ChoiceNode):
            if self in rule.rules: raise Exception()
            self.rules.extend(rule.rules)
        elif isinstance(rule, GrammarNode):
            self.rules.append(rule)
        else:
            raise SyntaxError('rule')

    def canonical(self, rulebuilder):
        rules = []
        for rule in self.rules:
            rules.append(rule.canonical(rulebuilder))
        if len(rules) == 1:
            return rules[0]
        return ChoiceNode(rules)

class GrammarDict(dict):
    """ A Special class dictionary that does all the sugar """

    def __init__(self, defaults):
        dict.__init__(self)
        self.named_rules = {}
        self.rulesets = {}

        for k, v in defaults.items():
            if not k.startswith("_"):
                dict.__setitem__(self, k, v)

    def __getitem__(self, key):
        if key.startswith('_'):
            return dict.__getitem__(self,key)

        if key in self:
            value = dict.__getitem__(self,key)
            if not isinstance(value, GrammarRuleSet):
                return value

        if key in self.named_rules:
            return self.named_rules[key]
        else:
            rule = NamedNode(key)
            self.named_rules[key] = rule
            return rule

    def __setitem__(self, key, value):
        if key.startswith('_'):
            dict.__setitem__(self,key, value)
        elif key in self:
            ruleset = dict.__getitem__(self,key)
            is_ruleset = isinstance(ruleset, GrammarRuleSet)
            is_rule = isinstance(value, GrammarRule)
            if is_ruleset and is_rule:
                ruleset.append(value)
            elif not is_ruleset and not is_rule:
                dict.__setitem__(self,key, value)
            else:
                raise SyntaxError('rule / non rule mismatch in assignments')
        elif isinstance(value, GrammarRule):
            rule = GrammarRuleSet([])
            rule.append(value)
            dict.__setitem__(self, key, rule)
        else:
            dict.__setitem__(self,key, value)


def build_class_dict(attrs, start, whitespace, newline):
    for name in attrs.named_rules:
        if name not in attrs:
            raise SyntaxError('missing rule', name)
    rules = {}
    new_attrs = {}
    for key, value in attrs.items():
        if key.startswith("_"):
            new_attrs[key] = value
        elif value == Builtins.__dict__.get(key):
            pass # decorators need to be kept as called afterwards, lol
        elif isinstance(value, GrammarRuleSet):
            rules[key] = value
        else:
            new_attrs[key] = value

    names = {name:attrs.named_rules.get(name, NamedNode(name)) for name in rules}

    builder = FunctionBuilder(names)
    rules = {k:r.canonical(builder).make_rule() for k,r in rules.items()}

    new_attrs['rules'] = rules 
    new_attrs['start'] = start
    new_attrs['whitespace'] = whitespace
    new_attrs['newline'] = newline

    return new_attrs


class Metaclass(type):
    """
    Allows us to provide Grammar with a special class dictionary
    and perform post processing
    """

    @classmethod
    def __prepare__(metacls, name, bases, **args):
        return GrammarDict({k:v for k,v in Builtins.__dict__.items() if not k.startswith("_")})
    def __new__(metacls, name, bases, attrs, start=None, whitespace=None, newline=None, **args):
        attrs = build_class_dict(attrs, start, whitespace, newline)
        return super().__new__(metacls, name, bases, attrs)


class Grammar(metaclass=Metaclass):
    pass

# cannot use decorator because `classmethod` won't resolve. heh

def parser(grammar, builder):
    return Parser(grammar, builder)

Grammar.parser = classmethod(parser)
