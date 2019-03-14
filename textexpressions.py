from contextlib import contextmanager
from types import FunctionType

class Rule:
    pass

# Rules (aka right hand side of grammar)
#       not built directly

class FunctionRule(Rule):
    def __init__(self, name):
        self.name = name

    def build_rule(self, builder):
        return builder(self.name)

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
        if len(self.rules) == 1:
            return self.rules[0]
        return self

class SequenceRule(Rule):
    def __init__(self, rules):
        self.rules = rules
    def __str__(self):
        return f"({' '.join(str(x) for x in self.rules)})"

    def build_rule(self, builder):
        if len(self.rules) == 1:
            return self.rules[0]
        return self

class CaptureRule(Rule):
    def __init__(self, name, rules):
        self.rules = rules
        self.name = name
    def __str__(self):
        return f"({' '.join(str(x) for x in self.rules)})"

    def build_rule(self, builder):
        return self

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
        return self

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

class RangeLiteralRule(Rule):
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

    def range(self, *args, invert=False):
        if self.block_mode: raise SyntaxError()
        self.rules.append(RangeLiteralRule(args, invert))

    def reject(self):
        if self.block_mode: raise SyntaxError()
        pass

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

    def build(self, rule):
        if self.block_mode != "build": raise SyntaxError()
        self.block_mode = None
        self.rules = []

        rule(self)

        if self.block_mode: raise SyntaxError()
        self.block_mode = "build"
        rules, self.rules = self.rules, None

        if len(rules) == 1:
            return rules[0]
        return SequenceRule(rules)

class Builtins:
    """ These methods are exported as functions inside the class defintion """
    def rule(*args, inline=False):
        if len(args) > 0:
            return SequenceRule(args)
        else:
            def _decorator(fn):
                return FunctionRule(fn)
            return _decorator

    def capture(name, *args):
        return CaptureRule(name, args)
    def accept(*args, exclude=None):
        return LiteralRule(args, exclude)
    def range(*args, exclude=None):
        return LiteralRule(args, exclude)
    def repeat(*args, min=0, max=None):
        return RepeatRule(args, min=min, max=max)
    def optional(*args):
        return RepeatRule(args, min=0, max=1)
    def choice(*args):
        return ChoiceRule(args)

class Metaclass(type):
    """
    Allows us to provide Grammar with a special class dictionary
    and perform post processing
    """

    @classmethod
    def __prepare__(metacls, name, bases, **args):
        return RuleDict({k:v for k,v in Builtins.__dict__.items() if not k.startswith("_")})
    def __new__(metacls, name, bases, attrs, start=None, **args):
        attrs = attrs.build_attrs()
        attrs['start'] = start
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
            is_rule = isinstance(value, Rule)
            if is_ruleset and is_rule:
                ruleset.append(value)
            elif not is_ruleset and not is_rule:
                dict.__setitem__(self,key, value)
            else:
                raise SyntaxError('rule / non rule mismatch in assignments')
        elif isinstance(value, Rule):
            rule = RuleSet([])
            rule.append(value)
            dict.__setitem__(self, key, rule)
        else:
            dict.__setitem__(self,key, value)

    def build_attrs(self):
        for name in self.named_rules:
            if name not in self:
                raise SyntaxError('missing')
        rules = {}
        attrs = dict(self)
        new_attrs = {}
        for key, value in attrs.items():
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
        new_attrs['rules'] = {k:r.build_rule(builder.build) for k,r in rules.items()}
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

class Schema: pass

class Grammar(metaclass=Metaclass):
    pass

@classmethod
def _parser(self, builder):
    return Parser(self, builder)

Grammar.parser = _parser

class ParseNode:
    def __init__(self, name, start, end, children):
        self.name = name
        self.start = start
        self.end = end
        self.children = children

    def __str__(self):
        children = ", ".join(str(x) for x in self.children)
        children = " ({})".format(children) if children else ""
        return "{}[{}:{}]{}".format(self.name, self.start, self.end, children)

class Parser:
    def __init__(self, grammar, builder):
        self.grammar = grammar
        self.builder = builder
        self.stack = None

    def parse(self, buf, offset=0):
        start = self.grammar.rules[self.grammar.start]
        self.stack = []
        end = self.parse_rule(start, buf, offset)
        stack, self.stack = self.stack, None
        if end:
            name = self.grammar.start
            if name in self.builder:
                return self.builder[name](buf[offset:end])
            else:
                return ParseNode(name, offset, end, stack)

    def parse_rule(self, rule, buf, offset):
        if isinstance(rule, NamedRule):
            end = self.parse_rule(self.grammar.rules[rule.name], buf, offset)
            return end

        if isinstance(rule, ChoiceRule):
            for option in rule.rules:
                o = self.parse_rule(option, buf, offset)
                if o is not None:
                    return o
        if isinstance(rule, RepeatRule):
            start, end = rule.min, rule.max
            c= 0
            while c < start:
                for step in rule.rules:
                    offset = self.parse_rule(step, buf, offset)
                    if offset is None:
                        return None
                c+=1
            while end is None or c < end:
                for step in rule.rules:
                    new_offset = self.parse_rule(step, buf, offset)
                    if new_offset is None:
                        return offset
                    offset = new_offset
                c+=1
            return offset
        if isinstance(rule, CaptureRule):
            start = offset
            stack, self.stack = self.stack, []
            for step in rule.rules:
                offset = self.parse_rule(step, buf, offset)
                if offset is None:
                    break
            if offset:
                if rule.name in self.builder:
                    stack.append(self.builder[rule.name](buf[start:offset]))
                else:
                    stack.append(ParseNode(rule.name, start, offset, self.stack))
            self.stack = stack

            return offset

        if isinstance(rule, SequenceRule):
            for step in rule.rules:
                offset = self.parse_rule(step, buf, offset)
                if offset is None:
                    return None
            return offset
        if isinstance(rule, LiteralRule):
            for text in rule.args:
                if buf[offset:].startswith(text):
                    return offset + len(text)
        if isinstance(rule, RangeLiteralRule):
            for text in rule.args:
                if '-' in text:
                    start, end = ord(text[0]), ord(text[2])
                    if start <= ord(buf[offset]) <= end:
                        return offset + 1
                elif buf[offset:].startswith(text):
                    return offset + len(text)


