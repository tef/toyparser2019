class RuleDict(dict):
    def __getitem__(self, key):
        if key.startswith('_'):
            return dict.__getitem__(self,key)
        if key not in self:
            dict.__setitem__(self, key, Node())
        return dict.__getitem__(self,key)

    def __setitem__(self, key, value):
        if key.startswith('_'):
            return dict.__setitem__(self,key, value)
        if key not in self:
            dict.__setitem__(self, key, Node())
        return dict.__getitem__(self,key).append(value)

class Builtins:
    def literal(name):
        return Node(name)

class Metaclass(type):
    @classmethod
    def __prepare__(metacls, name, bases, **args):
        r = RuleDict()
        for k, v in Builtins.__dict__.items():
            if not k.startswith("_"):
                dict.__setitem__(r, k, v)
        return r
    # transform after initialisation

class Node:
    def __init__(self, rules=None):
        self.rules = [] if rules is None else rules
    def append(self, rule):
        self.rules.append(rule)
    def __or__(self, right):
        if isinstance(right, Node):
            rules = list(self.rules)
            rules.append(right)
            return Node(rules)

class builder:
    def literal(self, name):
        pass

    def any_literal(self, name):
        pass

    def repeat(self, min=None, max=None):
        pass

class repeatbuilder:
    pass

def build(class_def):
    pass

class Grammar(metaclass=Metaclass):
    def __init_subclass__(cls, start, **kwargs):
        print(kwargs)
        super().__init_subclass__(**kwargs)


