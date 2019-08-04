from contextlib import contextmanager
from types import FunctionType

""" 
This is a lot of python magic so that you can define grammar rules inside a normal looking
python class:


class Example(Grammar):
    rule_name = rule( ...)

    @rule()
    def rule_name(self):
        ...

This gets turned into 
    rule_name = GrammarNode( .....)

Then you can turn GrammarNodes into ParseRules
    (kinda the same, with more guarantees about contents)

Then you can use them to parse

"""
                
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

class GrammarRule:
    """ Wraps rules that are assigned to the class dictionary"""
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
    """ A Special class dictionary that handles rule assignments """

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


"""

Inside the class definiton, you can call repeat(), accept(literal), range(..)
etc. These classes get transformed twice.

Once to remove GrammarRule() wrappers and to convert functions into GrammarNodes
I.e to turn it into a pure GrammarNode tree (canonical())
Then again to conver the GrammarNode tree into ParserNodes (make_rule())
"""

START_OF_LINE = 'start-of-line'
END_OF_LINE = 'end-of-line'
WHITESPACE = 'whitespace'
NEWLINE = 'newline'
END_OF_FILE = 'end-of-file'

SET_INDENT = 'set-indent'
MATCH_INDENT = 'match-indent'

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

class GrammarNode:
    def __init__(self, kind, *, rules=None, args=None):
        self.kind = kind
        self.rules = rules
        self.args = args

    def __str__(self):
        rules = ' '.join(str(x) for x in self.rules) if self.rules else ''
        args = str(self.args) if self.args else ''

        return f"{self.kind} ({rules or args})"

    def canonical(self, builder):
        rules = [r.canonical(builder) for r in self.rules] if self.rules else None
        return GrammarNode(self.kind, rules=rules, args=self.args)

    def make_rule(self):
        rules = [r.make_rule() for r in self.rules] if self.rules else None
        return ParserRule(self.kind, rules=rules, args=self.args)

class FunctionNode(GrammarNode):
    def __init__(self, fn, wrapper):
        self.fn = fn
        self.wrapper = wrapper

    def canonical(self, builder):
        return self.wrapper(builder.from_function(self.fn))

    def make_rule(self):
        raise Exception('Canonicalise first')

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
        return ParserRule(RULE, args=dict(name=self.name))

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
        return ParserRule(CHOICE, rules=[r.make_rule() for r in self.rules])

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
        return ParserRule(SEQUENCE, rules=[r.make_rule() for r in self.rules])

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
        return ParserRule(CAPTURE, args=dict(name=self.name), rules=[r.make_rule() for r in self.rules])

class RepeatNode(GrammarNode):
    def __init__(self, rules, min=0, max=None, key=None):
        self.min = min
        self.max = max
        self.rules = rules
        self.key = key if key is not None else object()

    def canonical(self, builder):
        rules = [r.canonical(builder) for r in self.rules]
        return RepeatNode(rules, self.min, self.max, self.key)

    def make_rule(self):
        return ParserRule(REPEAT, args=dict(min=self.min, max=self.max, key=self.key), rules=[r.make_rule() for r in self.rules])

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
        return ParserRule(LITERAL, args={'invert': self.invert, 'literals': self.args})

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
        return ParserRule(RANGE, args=dict(invert=self.invert, range=self.args))

# Builders

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

    def whitespace(self, min=0, max=None, newline=False):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(WHITESPACE, args=dict(min=min, max=max, newline=newline)))

    def capture_value(self, value):
        if self.block_mode: raise SyntaxError()
        self.rules.append(ValueNode(value))

    def newline(self):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(NEWLINE))

    def eof(self):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(END_OF_FILE))

    def end_of_line(self):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(END_OF_LINE))

    def start_of_line(self):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(START_OF_LINE))

    def range(self, *args, invert=False):
        if self.block_mode: raise SyntaxError()
        self.rules.append(RangeNode(args, invert))

    def indent(self):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(MATCH_INDENT))
    def print(self, *args):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(PRINT, args={'args':args}))

    def reject_if(self, cond):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(REJECT_IF, args=dict(cond=cond)))

    def accept_if(self, cond):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(ACCEPT_IF, args=dict(cond=cond)))

    @contextmanager
    def indented(self):
        if self.block_mode: raise SyntaxError()
        rules, self.rules = self.rules, []
        yield
        rules.append(GrammarNode(SET_INDENT, rules=self.rules))
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
    def trace(self, active=True):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        yield
        if active:
            rules.append(GrammarNode(TRACE, rules=self.rules))
        else:
            rules.extend(self.rules)
        self.rules = rules

    @contextmanager
    def lookahead(self):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        yield
        rules.append(GrammarNode(LOOKAHEAD, rules=self.rules))
        self.rules = rules

    @contextmanager
    def reject(self):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        yield
        rules.append(GrammarNode(REJECT, rules=self.rules))
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
        return ParserRule(COUNT, args=dict(char=self.char, key=self.key), rules=[r.make_rule() for r in self.rules])

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

    def capture(name, *args):
        return CaptureNode(name, args)
    def capture_value(arg):
        return ValueNode(arg)
    def accept(*args):
        return LiteralNode(args)
    def reject(*args):
        return GrammarNode(REJECT, rules=args)
    def lookahead(*args):
        return GrammarNode(LOOKAHEAD, rules=args)
    def trace(*args):
        return GrammarNode(TRACE, rules=args)
    def range(*args, exclude=None):
        return RangeNode(args, exclude)
    def repeat(*args, min=0, max=None):
        return RepeatNode(args, min=min, max=max)
    def optional(*args):
        return RepeatNode(args, min=0, max=1)
    def choice(*args):
        return ChoiceNode(args)
    whitespace = GrammarNode(WHITESPACE, args={'min':0, 'max':None, 'newline': False})
    eof = GrammarNode(END_OF_FILE)
    end_of_line = GrammarNode(END_OF_LINE)
    start_of_line = GrammarNode(START_OF_LINE)
    newline = GrammarNode(NEWLINE)

class ParserRule:
    def __init__(self, kind, *, args=None, rules=None):
        self.kind = kind
        self.args = args if args else None
        self.rules = rules if rules else None

    def __str__(self):
        rules =" ".join(str(r) for r in self.rules) if self.rules else None
        args = " ".join(f"{k}={v}" for k,v in self.args.items()) if self.args else None

        return "({} {})".format(self.kind, rules or args)

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
        self.children.extend(new.children)
        return new.clone(children = self.children)

    def set_indent(self):
        return self.clone(indent=(self.offset-self.line_start, self.indent))

    def pop_indent(self):
        return self.clone(indent=self.indent[1])

    def advance(self, text):
        if self.buf[self.offset:].startswith(text):
            return self.clone(offset=self.offset + len(text))

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
    def __init__(self, grammar, builder):
        self.grammar = grammar
        self.builder = builder

    def parse(self, buf, offset=0, err=None):
        name = self.grammar.start
        rule = self.grammar.rules[name]

        start = ParserState.init(buf, offset)
        end = self.parse_rule(rule, start)

        if end is None:
            if err is None: return
            raise err(buf, offset, "no")

        return start.children[-1]

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

        elif rule.kind == START_OF_LINE:
            if state.offset == state.line_start:
                return state
            return

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

        elif rule.kind == MATCH_INDENT:
            return state.advance_indent(self.grammar.whitespace)

        elif rule.kind == SET_INDENT:
            state = state.set_indent()
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
            key = rule.args['key']
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

        elif rule.kind == LITERAL:
            literals = rule.args['literals']
            if rule.args['invert']:
                for text in literals:
                    if state.advance(text):
                        return None
                return state
            else:
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
        return f"{self.name}_{self.n}" if self.n else self.name

    def incr(self):
        return VarBuilder(self.name, self.n+1)


def compile_old(grammar, builder=None):

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
            if _min is not None and _min > 0:
                _min = repr(_min) # value todo
                steps.append(f"while {count} < {_min}:")
                build_subrules(rule.rules, steps.add_indent(), state, new_count)
                steps.append("    count += 1")
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

        elif rule.kind == SET_INDENT:
            steps.append(f'{state} = {state}.set_indent()')
            build_subrules(rule.rules, steps, state, count)
            steps.append(f'{state} = {state}.pop_indent()')

        elif rule.kind == MATCH_INDENT:
            steps.extend((
                f"{state} = {state}.advance_indent(self.WHITESPACE)",
                f"if {state} is None: break",
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
        elif rule.kind == START_OF_LINE:
            steps.extend((
                f"if {state}.offset != {state}.line_start:",
                f"    {state} = None",
                f"    break",
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
        f"    def __init__(self, builder):",
        f"         self.builder = builder",
        "",
        f"    NEWLINE = {newline}",
        f"    WHITESPACE = {whitespace}",
        "",
    ))

    output = output.add_indent(4)

    start_rule = grammar.start
    output.extend((
        f"def parse(self, buf, offset=0):",
        f"    start = ParserState.init(buf, offset)",
        f"    end = self.parse_{start_rule}(start)",
        f"    return start.children[-1] if end else None",
        f"",
    ))

    for name, rule in grammar.rules.items():
        output.append(f"def parse_{name}(self, state):")
        # output.append(f"    print('{name}')")
        output.append(f"    while True: # note: return at end of loop")

        build_steps(rule, output.add_indent(8), VarBuilder("state"), VarBuilder("count"))
        output.append(f"        break")
        # output.append(f"    print('exit {name}', state)")
        output.append(f"    return state")
        output.append("")

    output = output.add_indent(-4)
    output.append("return Parser")
    
    glob, loc = {}, {}
    # for lineno, line in enumerate(output.output):
    #    print(lineno, '\t', line)
    exec(output.as_string(), glob, loc)
    return loc['closure'](ParserState)(builder)

def compile_python(grammar, builder=None, cython=False):

    def build_subrules(rules, steps, offset, line_start, indent, children, count): 
        for subrule in rules:
            build_steps(subrule, steps, offset, line_start, indent, children, count)

    def build_steps(rule, steps, offset, line_start, indent, children, count):
        # steps.append(f"print('start', {repr(str(rule))})")
        if rule.kind == SEQUENCE:
            build_subrules(rule.rules, steps, offset, line_start, indent, children, count)

        elif rule.kind == CAPTURE:
            name = repr(rule.args['name'])
            children_0 = children.incr()
            offset_0 = offset.incr()
            steps.append(f"{offset_0} = {offset}")
            steps.append(f"{children_0} = []")
            steps.append(f"while True: # start capture")
            build_subrules(rule.rules, steps.add_indent(), offset_0, line_start, indent, children_0, count)
            steps.append(f"    break")
            steps.append(f"if {offset_0} == -1:")
            steps.append(f"    {offset} = -1")
            steps.append(f"    break")
            if cython:
                steps.extend((
                    f"if self.builder is not None:",
                    f"    {children}.append(self.builder[{name}](buf, {offset}, {offset_0}, {children_0}))",
                    f"else:",
                    f"    {children}.append(ParseNode({name}, {offset}, {offset_0}, list({children_0}), None))",
                ))
            elif builder:
                steps.append(f"{children}.append(self.builder[{name}](buf, {offset}, {offset_0}, {children_0}))")
            else:
                steps.append(f"{children}.append(self.ParseNode({name}, {offset}, {offset_0}, {children_0}, None))")
            steps.append(f"{offset} = {offset_0}")

        elif rule.kind == CHOICE:
            children_0 = children.incr()
            offset_0 = offset.incr()
            line_start_0 = line_start.incr()

            steps.append(f"while True: # start choice")

            steps_0 = steps.add_indent()
            for subrule in rule.rules:
                steps_0.append(f"{offset_0} = {offset}")
                steps_0.append(f"{line_start_0} = {line_start}")
                steps_0.append(f"{children_0} = []")
                steps_0.append(f"while True: # case")
                build_steps(subrule, steps_0.add_indent(), offset_0, line_start_0, indent, children_0, count)
                steps_0.append(f"    break")
                steps_0.append(f"if {offset_0} != -1:")
                steps_0.append(f"    {offset} = {offset_0}")
                steps_0.append(f"    {line_start} = {line_start_0}")
                steps_0.append(f"    {children}.extend({children_0})")
                steps_0.append(f"    break")
                steps_0.append(f"# end case")

            steps_0.append(f"{offset} = -1 # no more choices")
            steps_0.append(f"break # end choice")
            steps.append(f"if {offset} == -1:")
            steps.append(f"    break")

        elif rule.kind == REPEAT:
            _min = rule.args['min']
            _max = rule.args['max']

            cond = "True"
            if _max is not None and _max > 1:
                cond = f"{count} < {repr(_max)}"
            
            steps.extend((
                f"{count} = 0",
                f"while {cond}:",
            ))
            new_count = count.incr()
            offset_0 = offset.incr()
            line_start_0 = line_start.incr()
            steps_0 = steps.add_indent()

            steps_0.append(f"{offset_0} = {offset}")
            steps_0.append(f"{line_start_0} = {line_start}")

            for subrule in rule.rules:
                build_steps(subrule, steps_0, offset_0, line_start_0, indent, children, new_count)
            steps_0.append(f"if {offset} == {offset_0}: break")
            steps_0.append(f"{offset} = {offset_0}")
            steps_0.append(f"{line_start} = {line_start_0}")
            steps_0.append(f"{count} += 1")
            if _max == "1":
                steps_0.append(f"break")

            if _min is not None and _min > 0:
                steps.extend((
                    f"if {count} < {repr(_min)}:",
                    f"    {offset} = -1",
                    f"    break",
                ))

        elif rule.kind == LOOKAHEAD:
            steps_0 = steps.add_indent()
            children_0 = children.incr()
            offset_0 = offset.incr()
            line_start_0 = line_start.incr()
            steps.append(f"while True: # start reject")
            steps_0.append(f"{children_0} = []")
            steps_0.append(f"{offset_0}, {line_start_0} = {offset}, {line_start}")
            build_subrules(rule.rules, steps_0, offset_0, line_start_0, indent, children_0, count)
            steps_0.append("break")

            steps.append(f'if {offset_0} == -1:')
            steps.append(f'    {offset} = -1')
            steps.append(f'    break')

        elif rule.kind == REJECT:
            steps_0 = steps.add_indent()
            children_0 = children.incr()
            offset_0 = offset.incr()
            line_start_0 = line_start.incr()
            steps.append(f"while True: # start reject")
            steps_0.append(f"{children_0} = []")
            steps_0.append(f"{offset_0}, {line_start_0} = {offset}, {line_start}")
            # steps_0.append(f'print("reject", {offset_0})')
            build_subrules(rule.rules, steps_0, offset_0, line_start_0, indent, children_0, count)
            steps_0.append("break")

            # steps.append(f'print("exit", {offset_0})')
            steps.append(f'if {offset_0} != -1:')
            steps.append(f'    {offset} = -1')
            steps.append(f'    break')

        elif rule.kind == ACCEPT_IF:
            steps.append(f'raise Exception("{rule.kind} missing") # unfinished {rule}')

        elif rule.kind == REJECT_IF:
            steps.append(f'raise Exception("{rule.kind} missing") # unfinished {rule}')

        elif rule.kind == COUNT:
            steps.append(f'raise Exception("{rule.kind} missing") # unfinished {rule}')

        elif rule.kind == VALUE:
            steps.append(f'raise Exception("{rule.kind} missing") # unfinished {rule}')

        elif rule.kind == SET_INDENT:
            indent_0 = indent.incr()
            steps.append(f'{indent_0} = {offset} - {line_start}')
            build_subrules(rule.rules, steps, offset, line_start, indent_0, children, count)

        elif rule.kind == MATCH_INDENT:
            steps.extend((
                f"{count} = {line_start} + {indent}",
                f"if {count} >= buf_eof:"
                f"    {offset} == -1; break",
                f"while {offset} < {count}:",
                f"    if buf[{offset}] in self.WHITESPACE:",
                f"        {offset} +=1",
                f"    else:",
                f"        break",
                f"if {offset} != {count}:",
                f"    {offset} = -1",
                f"    break",
            ))

        elif rule.kind == RULE:
            steps.extend((
                f"{offset}, {line_start} = self.parse_{rule.args['name']}(buf, {offset}, {line_start}, {indent}, buf_eof, {children})",
                f"if {offset} == -1: break",
                f"",
            ))
            
        elif rule.kind == RANGE:
            invert = rule.args['invert']
            steps.extend((
                f"if {offset} == buf_eof:",
                f"    {offset} = -1",
                f"    break",
                f"",
                f"chr = buf[{offset}]"
                f"",
            ))

            for idx, literal in enumerate(rule.args['range']):
                _if = {0:"if"}.get(idx, "elif")
                if '-' in literal and len(literal) == 3:
                    start, end = repr(literal[0]), repr(literal[2])

                    if invert:
                        steps.extend((
                            f"{_if} {start} <= chr <= {end}:",
                            f"    {offset} = -1",
                            f"    break",
                        ))
                    else:
                        steps.extend((
                            f"{_if} {start} <= chr <= {end}:",
                            f"    {offset} += 1",
                        ))

                elif len(literal) == 1:
                    literal = repr(literal)
                    if invert:
                        steps.extend((
                            f"{_if} chr == {literal}:",
                            f"    {offset} = -1",
                            f"    break",
                        ))
                    else:
                        steps.extend((
                            f"{_if} chr == {literal}:",
                            f"    {offset} += 1",
                        ))
                else:
                    raise Exception('bad range')

            if not invert:
                steps.extend((
                    f"else:",
                    f"    {offset} = -1",
                    f"    break",
                ))
            else:
                steps.extend((
                    f"else:",
                    f"    {offset} += 1",
                ))

            

        elif rule.kind == LITERAL:
            literal = rule.args['literals'][0]
            length = len(literal)
            literal = repr(literal)
            steps.extend((
                f"if buf[{offset}:{offset}+{length}] == {literal}:",
                f"    {offset} += {length}",
            ))

            for literal in rule.args['literals'][1:]:
                length = len(literal)
                literal = repr(literal)
                steps.extend((
                    f"elif buf[{offset}:{offset}+{length}] == {literal}:",
                    f"    {offset} += {length}",
                ))

            steps.extend((
                f"else:",
                f"    {offset} = -1",
                f"    break",
            ))


        elif rule.kind == WHITESPACE:
            _min = rule.args['min']
            _max = rule.args['max']
            _newline = rule.args['newline']

            cond = [f"{offset} < buf_eof"]
            if _max is not None:
                cond.append(f"{count} < {repr(_max)}")
            
            cond2 =f"chr in self.WHITESPACE"
            if cython: cond2 = " or ".join(f"chr == {repr(chr)}" for chr in grammar.whitespace)

            if _newline:
                cond3 =f"chr in self.NEWLINE"
                if cython: cond3 = " or ".join(f"chr == {repr(chr)}" for chr in grammar.newline)
                steps.extend((
                    f"{count} = 0",
                    f"while {' and '.join(cond)}:",
                    f"    chr = buf[{offset}]",
                    f"    if {cond3}:",
                    f"        {offset} +=1",
                    f"        {line_start} = {offset}",
                    f"        {count} +=1",
                    f"    elif {cond2}:",
                    f"        {offset} +=1",
                    f"        {count} +=1",
                    f"    else:",
                    f"        break",
                ))

            else:
                steps.extend((
                    f"{count} = 0",
                    f"while {' and '.join(cond)}:",
                    f"    chr = buf[{offset}]",
                    f"    if {cond2}:",
                    f"        {offset} +=1",
                    f"        {count} +=1",
                    f"    else:",
                    f"        break",
                ))
            if _min is not None and _min > 0:
                steps.extend((
                    f"if {count} < {repr(_min)}:"
                    f"    {offset} = -1",
                    f"    break",
                ))

        elif rule.kind == NEWLINE:
            cond =f"chr in self.NEWLINE"

            if cython: cond = " or ".join(f"chr == {repr(chr)}" for chr in grammar.newline)
            steps.extend((
                f"if {offset} < buf_eof:",
                f"    chr = buf[{offset}]",
                f"    if {cond}:",
                f"        {offset} +=1",
                f"        {line_start} = {offset}",
                f"    else:",
                f"        {offset} = -1",
                f"        break",
                f"else:",
                f"    {offset} = -1",
                f"    break",
            ))
        elif rule.kind == START_OF_LINE:
            steps.extend((
                f"if {offset} != {line_start}:",
                f"    {offset} = -1",
                f"    break",
            ))
        elif rule.kind == END_OF_LINE:
            cond =f"chr in self.NEWLINE"
            if cython: cond = " or ".join(f"chr == {repr(chr)}" for chr in grammar.newline)

            steps.extend((
                f"if {offset} < buf_eof:",
                f"    chr = buf[{offset}]",
                f"    if {cond}:",
                f"        {offset} +=1",
                f"        {line_start} = {offset}",
                f"    else:",
                f"        {offset} = -1",
                f"        break",
            ))
        elif rule.kind == END_OF_FILE:
            steps.extend((
                f"if {offset} != buf_eof:",
                f"    {offset} = -1",
                f"    break",
            ))

        elif rule.kind == PRINT:
            steps.append(f'raise Exception("{rule.kind} missing") # unfinished {rule}')
        elif rule.kind == TRACE:
            steps.append(f'raise Exception("{rule.kind} missing") # unfinished {rule}')
        else:
            raise Exception(f'Unknown kind {rule.kind}')

        # steps.append(f"print('end', {repr(str(rule))}, {offset})")
        steps.append("")
        return steps

    output = ParserBuilder([], 0)
    newline = repr(tuple(grammar.newline)) if grammar.newline else '()'
    whitespace = repr(tuple(grammar.whitespace)) if grammar.whitespace else '()'


    parse_node = (
        f"class ParseNode:",
        f"    def __init__(self, name, start, end, children, value):",
        f"        self.name = name",
        f"        self.start = start",
        f"        self.end = end",
        f"        self.children = children",
        f"        self.value = value",
        f"    def __str__(self):",
        "        return '{}[{}:{}]'.format(self.name, self.start, self.end)",
        f"",
    )
    if cython:
        output.append('# cython: language_level=3')
        output.extend(parse_node)
        output.extend((
            f"cdef class Parser:",
            f"    cpdef object builder",
            f"",
            f"    def __init__(self, builder):",
            f"         self.builder = builder",
            f"",
            f"    NEWLINE = {newline}",
            f"    WHITESPACE = {whitespace}",
            "",
        ))
        output = output.add_indent(4)
    else:
        output.extend((
            f"class Parser:",
            f"    def __init__(self, builder):",
            f"         self.builder = builder",
            "",
            f"    NEWLINE = {newline}",
            f"    WHITESPACE = {whitespace}",
            "",
        ))

        output = output.add_indent(4)

        output.extend(parse_node)

    start_rule = grammar.start
    output.extend((
        f"def parse(self, buf, offset=0, err=None):",
        f"    line_start, indent, eof, children = offset, 0, len(buf), []",
        f"    new_offset, line_start = self.parse_{start_rule}(buf, offset, line_start, indent, eof, children)",
        f"    if children and new_offset > offset: return children[-1]",
        f"    if err is not None: raise err(buf, offset, 'no')",
        f"",
    ))

    for name, rule in grammar.rules.items():
        if cython:
            output.append(f"cdef (int, int) parse_{name}(self, str buf, int offset, int line_start, int indent, int buf_eof, list children):")
            output.append(f"    cdef int count")
            output.append(f"    cpdef Py_UNICODE chr")
        else:
            output.append(f"def parse_{name}(self, buf, offset, line_start, indent, buf_eof, children):")
        # output.append(f"    print('enter {name},',offset,line_start,indent, repr(buf[offset:offset+10]))")
        output.append(f"    while True: # note: return at end of loop")

        build_steps(rule, 
                output.add_indent(8), 
                VarBuilder("offset"), 
                VarBuilder('line_start'), 
                VarBuilder('indent'),
                VarBuilder('children'),
                VarBuilder("count"))
        output.append(f"        break")
        # output.append(f"    print(('exit' if offset != -1 else 'fail'), '{name}', offset, line_start, repr(buf[offset: offset+10]))")
        output.append(f"    return offset, line_start")
        output.append("")
    # for lineno, line in enumerate(output.output):
    #     print(lineno, '\t', line)
    return output.as_string()


def compile(grammar, builder=None):
    output = compile_python(grammar, builder)
    glob, loc = {}, {}
    exec(output, glob, loc)
    return loc['Parser'](builder)

class Grammar(metaclass=Metaclass):
    pass

# cannot use decorator because `classmethod` won't resolve. heh

def parser(grammar, builder):
    return Parser(grammar, builder)

Grammar.parser = classmethod(parser)
Grammar.compile_old = classmethod(compile_old)
Grammar.compile = classmethod(compile)
