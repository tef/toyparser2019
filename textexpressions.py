class GrammarDict(dict):
    def __init__(self):
        dict.__init__(self)
        self.rules = {}
        for k, v in Builtins.__dict__.items():
            if not k.startswith("_"):
                dict.__setitem__(self, k, v)

    def __getitem__(self, key):
        if key.startswith('_'):
            return dict.__getitem__(self,key)
        if key not in self:
            rule = self.rules.get(key, NamedRule(key))
            self.rules[key] = rule
            return rule
        return dict.__getitem__(self,key)

    def __setitem__(self, key, value):
        if key.startswith('_'):
            return dict.__setitem__(self,key, value)
        if key not in self:
            rule = self.rules.get(key, NamedRule(key))
            dict.__setitem__(self, key, rule)
        return dict.__getitem__(self,key).append(value)

class Builtins:
    def accept(*args, exclude=None):
        return LiteralRule(args, exclude)

class Metaclass(type):
    @classmethod
    def __prepare__(metacls, name, bases, **args):
        r = GrammarDict()
        return r
    def __new__(metacls, name, bases, attrs, start=None, **args):
        rules = {}
        new_attrs = {'rules':rules}
        for key, value in attrs.items():
            if key.startswith("_"):
                new_attrs[key] = value
            elif value == Builtins.__dict__.get(key):
                pass # decorators need to be kept as called afterwards, lol
            elif isinstance(value, NamedRule):
                rules[key] = value
            else:
                new_attrs[key] = value
                
        return super().__new__(metacls, name, bases, new_attrs)
        
    # transform after initialisation

class NamedRule:
    def __init__(self, name):
        self.rules = []
        self.name = name

    def __str__(self):
        return f"<{self.name} {self.rules}>"

    def append(self, rule):
        if isinstance(rule, ChoiceRule):
            self.rules.extend(rule.rules)
        else:
            self.rules.append(rule)

    def __or__(self, right):
        return ChoiceRule([self, right])

class ChoiceRule:
    def __init__(self, rules):
        self.rules = rules
    def __or__(self, right):
        rules = list(self.rules)
        rules.append(right)
        return ChoiceRule(rules)

class SequenceRule:
    pass

class RepeatRule:
    pass

class LiteralRule:
    def __init__(self, args,exclude):
        self.args = args
        self.exclude = exclude

class builder:
    def accept(self):
        pass

    def reject(self):
        pass

    def choice(self):
            pass

    def literal(self, name):
        pass

    def any_literal(self, name):
        pass

    def repeat(self, min=None, max=None):
        pass
    
    def optional(self):
        pass

class repeatbuilder:
    pass

def build(class_def):
    pass

class Grammar(metaclass=Metaclass):
    pass


