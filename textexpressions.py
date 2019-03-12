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
    def rule(*args, inline=False):
        if len(args) > 0:
            return SequenceRule(args)
        else:
            def _decorator(fn):
                return FunctionRule(fn)
            return _decorator

    def accept(*args, exclude=None):
        return LiteralRule(args, exclude)
    def repeat(*args, min=0, max=None):
        return RepeatRule(args, min=min, max=max)
    def optional(*args):
        return RepeatRule(args, min=0, max=1)
    def choice(*args):
        return ChoiceRule(args)
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
            def callback(self, named_rule=named_rule):
                return self.rule(named_rule)
            setattr(Builder, name, callback)

        build_rule = None
        def build_rule(rule):
            builder = Builder()
            rule(builder)
            return builder.build_rule()
            raise SyntaxError()

        new_attrs['rules'] = {k:r.build_rule(build_rule) for k,r in rules.items()}
        return new_attrs

class RuleSet:
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

class Rule:
    pass

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
        else:
            return f"({' '.join(str(x) for x in self.rules)})^[{self.min},{self.max}]"
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
        return "|".join("{!r}".format(a) for a in self.args)


class RuleBuilder:
    def __init__(self):
        self.rules = []
        self.choice_block = False

    def rule(self, rule):
        if self.choice_block: raise SyntaxError()
        self.rules.append(rule)

    def accept(self, *args, exclude=None):
        if self.choice_block: raise SyntaxError()
        self.rules.append(LiteralRule(args, exclude))

    def reject(self):
        if self.choice_block: raise SyntaxError()
        pass

    @contextmanager
    def choice(self):
        if self.choice_block: raise SyntaxError()
        rules = self.rules
        self.rules = []
        self.choice_block = True
        yield
        self.choice_block = False
        rules.append(ChoiceRule(self.rules))
        self.rules = rules


    @contextmanager
    def case(self):
        if not self.choice_block: raise SyntaxError()
        rules = self.rules
        self.rules = []
        self.choice_block = False
        yield
        self.choice_block = True
        rules.append(SequenceRule(self.rules))
        self.rules = rules

    @contextmanager
    def repeat(self, min=0, max=None):
        if self.choice_block: raise SyntaxError()
        rules = self.rules
        self.rules = []
        yield
        rules.append(RepeatRule(self.rules, min=min, max=max))
        self.rules = rules

    @contextmanager
    def optional(self):
        if self.choice_block: raise SyntaxError()
        rules = self.rules
        self.rules = []
        yield
        rules.append(RepeatRule(self.rules, min=0, max=1))
        self.rules = rules

    def build_rule(self):
        if self.choice_block: raise SyntaxError()
        if len(self.rules) == 1:
            return self.rules[0]
        return SequenceRule(self.rules)

class Grammar(metaclass=Metaclass):
    def Tokenizer(self):
        pass
    def canonicalise(self):
        pass

class Schema:
    pass


