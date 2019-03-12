from contextlib import contextmanager
from types import FunctionType

class Metaclass(type):
    @classmethod
    def __prepare__(metacls, name, bases, **args):
        return GrammarDict()
    def __new__(metacls, name, bases, attrs, start=None, **args):
        attrs = attrs.build_attrs() 
        attrs['start'] = start
        return super().__new__(metacls, name, bases, attrs)

class Builtins:
    def accept(*args, exclude=None):
        return LiteralRule(args, exclude)

class GrammarDict(dict):
    def __init__(self):
        dict.__init__(self)
        self.named_rules = {}
        self.rulesets = {}

        for k, v in Builtins.__dict__.items():
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
            dict.__getitem__(self,key).append(value)
        else:
            rule = RuleSet()
            dict.__setitem__(self, key, rule)
            rule.append(value)

    def build_attrs(self):
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
        class Builder(RuleBuilder):
            pass

        for name in rules:
            named_rule = self.named_rules.get(name, NamedRule(name))
            def callback(self):
                return self.rule(named_rule)
            setattr(Builder, name, callback)

        new_attrs['rules'] = {k:r.build_rule(Builder) for k,r in rules.items()}
        return new_attrs
                
class RuleSet:
    def __init__(self):
        self.rules = []

    def append(self, rule):
        if isinstance(rule, ChoiceRule):
            self.rules.extend(rule.rules)
        else:
            self.rules.append(rule)

    def build_rule(self, rulebuilder):
        rules = []
        for rule in self.rules:
            if isinstance(rule, FunctionType):
                builder = rulebuilder()
                rule(builder)
                rule = builder.build_rule()
            rules.append(rule)
        if len(rules) == 1:
            return rules[0]
        return ChoiceRule(rules)

class Rule:
    pass

class NamedRule(Rule):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __or__(self, right):
        return ChoiceRule([self, right])

class ChoiceRule(Rule):
    def __init__(self, rules):
        self.rules = rules
    def __str__(self):
        return f"({' | '.join(str(x) for x in self.rules)})"
    def __or__(self, right):
        rules = list(self.rules)
        rules.append(right)
        return ChoiceRule(rules)

class SequenceRule(Rule):
    def __init__(self, rules):
        self.rules = rules
    def __str__(self):
        return f"({' '.join(str(x) for x in self.rules)})"

class RepeatRule(Rule):
    def __init__(self, rules):
        self.rules = rules
    def __str__(self):
        return f"({' '.join(str(x) for x in self.rules)})*"

class LiteralRule(Rule):
    def __init__(self, args,exclude):
        self.args = args
        self.exclude = exclude

    def __str__(self):
        if len(self.args) == 1:
            return "{!r}".format(self.args[0])
        return "{!r}".format(self.args)


class RuleBuilder:
    def __init__(self):
        self.rules = [] 

    def rule(self, rule):
        self.rules.append(rule)

    def accept(self, *args, exclude=None):
        self.rules.append(LiteralRule(args, exclude))

    def reject(self):
        pass

    @contextmanager
    def choice(self):
        rules = self.rules
        self.rules = []
        yield
        rules.append(ChoiceRule(self.rules))
        self.rules = rules


    @contextmanager
    def case(self):
        rules = self.rules
        self.rules = []
        yield
        rules.append(SequenceRule(self.rules))
        self.rules = rules

    @contextmanager
    def repeat(self, min=None, max=None):
        rules = self.rules
        self.rules = []
        yield
        rules.append(RepeatRule(self.rules))
        self.rules = rules
    
    @contextmanager
    def optional(self):
        rules = self.rules
        self.rules = []
        yield
        rules.append(RepeatRule(self.rules))
        self.rules = rules

    def build_rule(self):
        if len(self.rules) == 1:
            return self.rules[0]
        return SequenceRule(self.rules)

class Grammar(metaclass=Metaclass):
    pass


