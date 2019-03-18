from contextlib import contextmanager
from types import FunctionType

# Rules (aka right hand side of grammar)
#       not built directly

class Rule:
    pass

class FunctionRule(Rule):
    def __init__(self, name, inline, capture):
        self.name = name
        self.inline = inline
        self.capture = capture

    def build_rule(self, builder):
        return builder(self.name, self.inline, self.capture)

class NamedRule(Rule):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __or__(self, right):
        return ChoiceRule([self, right])

    def build_rule(self, builder):
        return self

class ChoiceRule(Rule):
    def __init__(self, rules):
        self.rules = rules
    def __str__(self):
        return f"({' | '.join(str(x) for x in self.rules)})"
    def __or__(self, right):
        rules = list(self.rules)
        rules.append(right)
        return ChoiceRule(rules)

    def build_rule(self, builder):
        rules = [r.build_rule(builder) for r in self.rules]
        if len(rules) == 1:
            return rules[0]
        return ChoiceRule(rules)

class SequenceRule(Rule):
    def __init__(self, rules):
        self.rules = rules
    def __str__(self):
        return f"({' '.join(str(x) for x in self.rules)})"

    def build_rule(self, builder):
        rules = [r.build_rule(builder) for r in self.rules]
        if len(rules) == 1:
            return rules[0]
        return SequenceRule(rules)

class CaptureRule(Rule):
    def __init__(self, name, rules):
        self.rules = rules
        self.name = name
    def __str__(self):
        return f"({' '.join(str(x) for x in self.rules)})"

    def build_rule(self, builder):
        rules = [r.build_rule(builder) for r in self.rules]
        return CaptureRule(self.name, rules)

class RepeatRule(Rule):
    def __init__(self, rules, min=0, max=None):
        self.min = min
        self.max = max
        self.rules = rules
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
    def build_rule(self, builder):
        rules = [r.build_rule(builder) for r in self.rules]
        return RepeatRule(rules, self.min, self.max)

class IndentRule(Rule):
    def __init__(self, rules):
        self.rules = rules

    def build_rule(self, builder):
        return self

    def __str__(self):
        return "<indent {}>".format(",".join(str(x) for x in self.rules))
class WhitespaceRule(Rule):
    def __init__(self, kind, min=0, max=None):
        self.kind = kind
        self.min = min
        self.max = max

    def build_rule(self, builder):
        return self

    def __str__(self):
        return self.kind

class LiteralRule(Rule):
    def __init__(self, args,exclude):
        self.args = args
        self.exclude = exclude

    def build_rule(self, rulebuilder):
        return self

    def __str__(self):
        if len(self.args) == 1:
            return "{!r}".format(self.args[0])
        return "|".join("{}".format(repr(a)) for a in self.args)

class RangeRule(Rule):
    def __init__(self, args,invert):
        self.args = args
        self.invert = invert

    def build_rule(self, rulebuilder):
        return self

    def __str__(self):
        invert = "^" if self.invert else ""
        if len(self.args) == 1:
            return "[{}{}]".format(invert, self.args[0])
        return "[{}{}]".format(invert, "".join(repr(a)[1:-1] for a in self.args))
# Builders
#

class RuleBuilder:
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

    def accept(self, *args, exclude=None):
        if self.block_mode: raise SyntaxError()
        self.rules.append(LiteralRule(args, exclude))

    def whitespace(self, min=0, max=None):
        if self.block_mode: raise SyntaxError()
        self.rules.append(WhitespaceRule("ws", min, max))

    def newline(self, *args, exclude=None):
        if self.block_mode: raise SyntaxError()
        self.rules.append(WhitespaceRule("nl"))

    def range(self, *args, invert=False):
        if self.block_mode: raise SyntaxError()
        self.rules.append(RangeRule(args, invert))

    def reject(self):
        if self.block_mode: raise SyntaxError()
        pass

    def indent(self):
        if self.block_mode: raise SyntaxError()
        self.rules.append(WhitespaceRule("indent"))

    @contextmanager
    def indented(self):
        if self.block_mode: raise SyntaxError()
        rules, self.rules = self.rules, []
        yield
        rules.append(IndentRule(self.rules))
        self.rules = rules
        
    @contextmanager
    def capture(self, name):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        yield
        rules.append(CaptureRule(name, self.rules))
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
        rules.append(ChoiceRule(self.rules))
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
        rules.append(SequenceRule(self.rules))
        self.rules = rules

    @contextmanager
    def repeat(self, min=0, max=None):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        yield
        rules.append(RepeatRule(self.rules, min=min, max=max))
        self.rules = rules

    @contextmanager
    def optional(self):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        yield
        rules.append(RepeatRule(self.rules, min=0, max=1))
        self.rules = rules

    def build(self, rule, inline, capture):
        if self.block_mode != "build": raise SyntaxError()
        self.block_mode = None
        self.rules = []

        rule(self)

        if self.block_mode: raise SyntaxError()
        self.block_mode = "build"
        rules, self.rules = self.rules, None

        if capture:
            rules = [CaptureRule(rules, capture)]

        if len(rules) == 1:
            return rules[0]
        return SequenceRule(rules)

class RuleDef:
    def __init__(self, rule):
        self.rule = rule

    def build_rule(self, builder):
        return self.rule.build_rule(builder)

class Builtins:
    """ These methods are exported as functions inside the class defintion """
    def rule(*args, inline=False, capture=None):
        if len(args) > 0:
            if capture:
                return RuleDef(CaptureRule(capture, args))
            else:
                return RuleDef(SequenceRule(args))
        else:
            def _decorator(fn):
                return RuleDef(FunctionRule(fn, inline, capture))
            return _decorator

    def capture(name, *args):
        return CaptureRule(name, args)
    def accept(*args, exclude=None):
        return LiteralRule(args, exclude)
    def range(*args, exclude=None):
        return RangeRule(args, exclude)
    def repeat(*args, min=0, max=None):
        return RepeatRule(args, min=min, max=max)
    def optional(*args):
        return RepeatRule(args, min=0, max=1)
    def choice(*args):
        return ChoiceRule(args)
    whitespace = WhitespaceRule("ws")
    newline = WhitespaceRule("nl")

class Metaclass(type):
    """
    Allows us to provide Grammar with a special class dictionary
    and perform post processing
    """

    @classmethod
    def __prepare__(metacls, name, bases, **args):
        return RuleDict({k:v for k,v in Builtins.__dict__.items() if not k.startswith("_")})
    def __new__(metacls, name, bases, attrs, start=None, whitespace=None, newline=None, **args):
        attrs = attrs.build_class_dict(start, whitespace, newline)
        return super().__new__(metacls, name, bases, attrs)


class RuleDict(dict):
    """ A Special class dictionary that does all the sugar """

    def __init__(self, defaults):
        dict.__init__(self)
        self.named_rules = {}
        self.rulesets = {}

        for k, v in defaults.items():
            if not k.startswith("_"):
                dict.__setitem__(self, k, v)

    def __getitem__(self, key):
        if key.startswith('_') or key in self:
            return dict.__getitem__(self,key)

        if key in self.named_rules:
            return self.named_rules[key]
        else:
            rule = NamedRule(key)
            self.named_rules[key] = rule
            return rule

    def __setitem__(self, key, value):
        if key.startswith('_'):
            dict.__setitem__(self,key, value)
        elif key in self:
            ruleset = dict.__getitem__(self,key)
            is_ruleset = isinstance(ruleset, RuleSet)
            is_rule = isinstance(value, RuleDef)
            if is_ruleset and is_rule:
                ruleset.append(value.rule)
            elif not is_ruleset and not is_rule:
                dict.__setitem__(self,key, value)
            else:
                raise SyntaxError('rule / non rule mismatch in assignments')
        elif isinstance(value, RuleDef):
            rule = RuleSet([])
            rule.append(value.rule)
            dict.__setitem__(self, key, rule)
        else:
            dict.__setitem__(self,key, value)

    def build_class_dict(self, start, whitespace, newline):
        for name in self.named_rules:
            if name not in self:
                raise SyntaxError('missing rule', name)
        rules = {}
        new_attrs = {}
        for key, value in self.items():
            if key.startswith("_"):
                new_attrs[key] = value
            elif value == Builtins.__dict__.get(key):
                pass # decorators need to be kept as called afterwards, lol
            elif isinstance(value, RuleSet):
                rules[key] = value
            else:
                new_attrs[key] = value

        names = {name:self.named_rules.get(name, NamedRule(name)) for name in rules}

        builder = RuleBuilder(names)
        rules = {k:r.build_rule(builder.build) for k,r in rules.items()}

        properties = GrammarProperties(start, rules)
        
        new_attrs['rules'] = rules 
        new_attrs['properties'] = properties
        new_attrs['start'] = start
        new_attrs['whitespace'] = whitespace
        new_attrs['newline'] = newline

        return new_attrs

class RuleSet:
    """ Allows for multiple definitions of rules """

    def __init__(self, rules):
        self.rules = rules

    def append(self, rule):
        if isinstance(rule, ChoiceRule):
            self.rules.extend(rule.rules)
        elif isinstance(rule, Rule):
            self.rules.append(rule)
        else:
            raise SyntaxError('rule')

    def build_rule(self, rulebuilder):
        rules = []
        for rule in self.rules:
            rules.append(rule.build_rule(rulebuilder))
        if len(rules) == 1:
            return rules[0]
        return ChoiceRule(rules)

class GrammarProperties:
    def __init__(self, start, rules):
        nullable = {}
        left_corners = {}
        stack = [start]

        while stack:
            head = stack.pop()

    

class ParserState:
    def __init__(self, buf, line_start,  offset, children, parent, indent):
        self.buf = buf
        self.line_start = line_start
        self.offset = offset
        self.children = children
        self.parent = parent
        self.indent = indent

    @staticmethod
    def init(buf, offset):
        return ParserState(buf, offset, offset, [], None, None)

    def clone(self, line_start=None, offset=None, children=None, parent=None, indent=None):
        if line_start is None: line_start = self.line_start
        if offset is None: offset = self.offset
        if children is None: children = self.children
        if parent is None: parent = self.parent
        if indent is None: indent = self.indent

        return ParserState(self.buf, line_start, offset, children, parent, indent)

    def __bool__(self):
        return True

    def set_indent(self):
        return self.clone(indent=(self.offset-self.line_start, self.indent))

    def pop_indent(self):
        # print(self.indent)
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

    def advance_newline(self, literals):
        for nl in literals:
            new = self.advance(nl)
            if new:
                return new.clone(line_start=new.offset)

    def advance_indent(self, literals):
        # nprint(self.line_start, self.offset, self.indent)
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
        self.parent.children.append(ParseNode(name, self.parent.offset, self.offset, self.children))
        return self.clone(children=self.parent.children, parent=self.parent.parent)

    def build_capture(self, builder):
        self.parent.children.append(builder(self.parent.substring(self), self.children))
        return self.clone(children=self.parent.children, parent=self.parent.parent)

class ParseNode:
    def __init__(self, name, start, end, children):
        self.name = name
        self.start = start
        self.end = end
        self.children = children

    def build(self, buf, builder):
        children = [child.build(buf, builder) for child in self.children]
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
        if state.offset == len(state.buf):
            return
        if isinstance(rule, NamedRule):
            # print(rule.name)
            end = self.parse_rule(self.grammar.rules[rule.name], state)
            return end

        # print(rule, repr(state.buf[state.offset:state.offset+5]))
        if isinstance(rule, ChoiceRule):
            for option in rule.rules:
                # nprint('choice', repr(state.buf[state.offset:state.offset+5]), option)
                s = self.parse_rule(option, state)
                if s is not None:
                    return s
        if isinstance(rule, RepeatRule):
            start, end = rule.min, rule.max
            c= 0
            while c < start:
                for step in rule.rules:
                    # print('rep', repr(state.buf[state.offset:state.offset+5]), step, rule)
                    state = self.parse_rule(step, state)
                    if state is None:
                        return None
                c+=1
            while end is None or c < end:
                old = state
                for step in rule.rules:
                    # nnprint('rep+', repr(state.buf[state.offset:state.offset+5]), step, rule)
                    new_state = self.parse_rule(step, state)
                    if new_state is None:
                        return old
                    state = new_state
                old = state
                c+=1
            return state
        if isinstance(rule, CaptureRule):
            start = state
            end = state.capture()
            for step in rule.rules:
                end = self.parse_rule(step, end)
                if end is None:
                    break
            if end:
                if rule.name in self.builder:
                    return end.build_capture(self.builder[rule.name])
                else:
                    return end.build_node(rule.name)
            return None

        if isinstance(rule, SequenceRule):
            for step in rule.rules:
                state = self.parse_rule(step, state)
                if state is None:
                    return None
            return state
        if isinstance(rule, LiteralRule):
            for text in rule.args:
                new_state = state.advance(text)
                if new_state:
                    return new_state
        if isinstance(rule, RangeRule):
            if rule.invert:
                # print(rule, state.buf[state.offset:], rule.args)
                for text in rule.args:
                    new_state = state.advance_range(text)
                    # print(new_state, text)
                    if new_state:
                        return
                return state.clone(offset=state.offset+1)
            else:
                for text in rule.args:
                    new_state = state.advance_range(text)
                    if new_state:
                        return new_state
        if isinstance(rule, WhitespaceRule):
            if rule.kind == "ws":
                return state.advance_whitespace(self.grammar.whitespace, rule.min, rule.max)
            if rule.kind == "nl":
                return state.advance_newline(self.grammar.newline)
            if rule.kind == "indent":
                return state.advance_indent(self.grammar.whitespace)
        if isinstance(rule, IndentRule):
            state = state.set_indent()
            for step in rule.rules:
                state = self.parse_rule(step, state)
                if state is None:
                    return None
            # print('exit', state.offset, repr(state.buf[state.offset:]), state.indent)
            return state.pop_indent()
                
def parser(grammar, builder):
    return Parser(grammar, builder)

class Grammar(metaclass=Metaclass):
    pass

Grammar.parser = classmethod(parser)


class Regex(Grammar, whitespace=[]):
    pattern = rule(pattern, accept("*"))
