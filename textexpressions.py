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
    def accept(*args, exclude=None):
        return Node(args)

class Metaclass(type):
    @classmethod
    def __prepare__(metacls, name, bases, **args):
        r = RuleDict()
        for k, v in Builtins.__dict__.items():
            if not k.startswith("_"):
                dict.__setitem__(r, k, v)
        return r
    def __new__(metacls, name, bases, attrs, start=None, **args):
        return super().__new__(metacls, name, bases, attrs)
        
    # transform after initialisation

class Grammar(metaclass=Metaclass):
    pass

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


