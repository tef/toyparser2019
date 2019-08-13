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
    def __new__(metacls, name, bases, attrs, start=None, whitespace=None, newline=None, tabstop=None, **args):
        attrs = build_class_dict(attrs, start, whitespace, newline, tabstop)
        return super().__new__(metacls, name, bases, attrs)

def build_class_dict(attrs, start, whitespace, newline, tabstop):
    for name in attrs.named_rules:
        if name not in attrs:
            raise SyntaxError('missing rule', name)
    if whitespace:
        for x in whitespace:
            if len(x) != 1: raise Exception('bad')
    if newline:
        for x in newline:
            if len(x) != 1 and x != "\r\n": raise Exception('bad')
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
    
    rule_childs = {}
    dont_pop = set()
    for name, rule in rules.items():
        seen = set()
        def visits(rule):
            if rule.kind == RULE:
                seen.add(rule.args['name'])
            if rule.kind == SET_LINE_PREFIX:
                prefix = rule.args['prefix']
                if prefix: dont_pop.add(prefix)
            
        rule.visit(visits)
        rule_childs[name] = seen

    inlineable = {}
    to_inline = []

    for name, child in rule_childs.items():
        seen = set((name,))
        def walk(childs):
            for c in childs:
                if c in seen: return False
                seen.add(c)
                if not walk(rule_childs[c]):
                    return False
            return True
        if child:
            inlineable[name] = walk(child)
        else:
            inlineable[name] = True
            to_inline.append(name)
        
    all_rules = set(rules.keys())
    while to_inline:
        n = to_inline.pop(0)
        all_rules.remove(n)
        for name in all_rules:
            if name == n: continue
            if n not in rule_childs[name]: continue
            rules[name] = rules[name].inline(n, rules[n])
            
            rule_childs[name].remove(n)
            if not rule_childs[name]:
                to_inline.append(name)
        if n not in dont_pop: 
            safe = True
            for name, rule in rules.items():
                if name == n: continue
                def _visit(rule):
                    nonlocal safe
                    if rule.kind == RULE and rule.args['name'] == n:
                        safe = False
                    if rule.kind == SET_LINE_PREFIX and rule.args['prefix'] == n:
                        safe = False
                rule.visit(_visit)
                if not safe: break
            if safe:
                rules.pop(n)

    new_attrs['rules'] = rules
    new_attrs['start'] = start
    new_attrs['whitespace'] = whitespace
    new_attrs['newline'] = newline
    new_attrs['tabstop'] = tabstop or 8

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
PARTIAL_TAB = 'partial_tab'
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
BACKREF = 'backref'
CHOICE = 'choice'
REPEAT = 'repeat'
MEMOIZE = 'memoize'

PRINT = 'print'
TRACE = 'trace'

class GrammarNode:
    def __init__(self, kind, *, key=None, rules=None, args=None, regular=False, nullable=True):
        self.kind = kind
        self.rules = rules
        self.args = args
        self.key = key if key else object()
        self.regular = regular
        self.nullable = nullable

    def __str__(self):
        rules = ' '.join(str(x) for x in self.rules) if self.rules else ''
        args = str(self.args) if self.args else ''

        return f"{self.kind} ({rules or args})"

    def canonical(self, builder):
        rules = [r.canonical(builder) for r in self.rules] if self.rules else None
        return GrammarNode(self.kind, key=self.key, rules=rules, args=self.args, regular=self.regular, nullable=self.nullable)

    def make_rule(self):
        rules = [r.make_rule() for r in self.rules] if self.rules else None
        return ParserRule(self.kind, key=self.key, rules=rules, args=self.args, regular=self.regular, nullable=self.nullable)

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
        return ParserRule(RULE,  args=dict(name=self.name, inline=False))

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
        rules=[r.make_rule() for r in self.rules]
        nullable = any(r.nullable for r in rules)
        regular = all(r.regular for r in rules)
        return ParserRule(CHOICE, rules=rules, regular=regular, nullable=nullable)

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
        rules=[r.make_rule() for r in self.rules]
        nullable = any(r.nullable for r in rules)
        regular = all(r.regular for r in rules)
        return ParserRule(SEQUENCE, rules=rules, regular=regular, nullable=nullable)

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
    def __init__(self, name, args, rules, *, key=None):
        self.rules = rules
        self.name = name
        self.args = args
        self.key = key or object()

    def __str__(self):
        return f"({' '.join(str(x) for x in self.rules)})"

    def canonical(self, builder):
        rules = [r.canonical(builder) for r in self.rules]
        return CaptureNode(self.name, self.args, rules, key=self.key)
    def make_rule(self):
        args = dict()
        args['name'] = self.name
        args['nested'] = self.args['nested']
        rules=[r.make_rule() for r in self.rules]
        nullable = any(r.nullable for r in rules)
        regular = all(r.regular for r in rules)
        return ParserRule(CAPTURE, key=self.key, args=args, rules=rules, regular=regular, nullable=nullable)

class MemoizeNode(GrammarNode):
    def __init__(self, rules, *, key=None):
        self.rules = rules
        self.key = key or object()

    def __str__(self):
        return f"({' '.join(str(x) for x in self.rules)})"

    def canonical(self, builder):
        rules = [r.canonical(builder) for r in self.rules]
        return MemoizeNode(rules, key=self.key)

    def make_rule(self):
        args = dict()
        return ParserRule(MEMOIZE, key=self.key, args=args, rules=[r.make_rule() for r in self.rules])

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
        args=dict(min=self.min, max=self.max, )
        rules=[r.make_rule() for r in self.rules]
        nullable = any(r.nullable for r in rules)
        regular = all(r.regular for r in rules)
        return ParserRule(REPEAT, key=self.key, args=args, rules=rules, regular=regular, nullable=nullable)

class LiteralNode(GrammarNode):
    def __init__(self, args,invert=False):
        if not args or "" in args:
            raise Exception('bad')
        self.args = args
        self.invert = invert

    def canonical(self, rulebuilder):
        return self

    def __str__(self):
        if len(self.args) == 1:
            return "{!r}".format(self.args[0])
        return "|".join("{}".format(repr(a)) for a in self.args)

    def make_rule(self):
        return ParserRule(LITERAL, args={'invert': self.invert, 'literals': self.args}, nullable=False, regular=True)

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
        return ParserRule(RANGE, args=dict(invert=self.invert, range=self.args), nullable=False, regular=True)

# Builders
NULL = object()

class FunctionBuilder:
    def __init__(self, names):
        self.rules = None
        self.block_mode = "build"
        for name, rule in names.items():
            if hasattr(self, name): raise SyntaxError()
            def callback(*, rule=rule):
                self.rule(rule)
            def _repeat(min=0, max=None, *, rule=rule):
                if self.block_mode: raise SyntaxError()
                self.rule(RepeatNode([rule], min=min, max=max))
            def _inline(min=0, max=None, *, rule=rule):
                if self.block_mode: raise SyntaxError()
                self.rule(GrammarNode(RULE, args=dict(name=rule.name, inline=True)))
            def _lookahead(*, rule=rule):
                if self.block_mode: raise SyntaxError()
                self.rule(GrammarNode(LOOKAHEAD, rules=[rule]))
            def _reject(*, rule=rule):
                if self.block_mode: raise SyntaxError()
                self.rule(GrammarNode(REJECT, rules=[rule]))

            @contextmanager
            def _as_prefix(*, rule=rule, name=name):
                if self.block_mode: raise SyntaxError()
                rules, self.rules = self.rules, []
                yield
                rules.append(GrammarNode(SET_LINE_PREFIX, args=dict(prefix=name, count=None), rules=self.rules))
                self.rules = rules
            callback.repeat = _repeat
            callback.as_line_prefix = _as_prefix
            callback.inline = _inline
            setattr(self, name, callback)

    def rule(self, rule):
        if self.block_mode: raise SyntaxError()
        self.rules.append(rule)

    def accept(self, *args):
        if self.block_mode: raise SyntaxError()
        self.rules.append(LiteralNode(args))

    def whitespace(self, min=0, max=None, newline=False):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(WHITESPACE, args=dict(min=min, max=max, newline=newline), nullable=(not min), regular=True))

    def partial_tab(self,):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(PARTIAL_TAB))


    def newline(self):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(NEWLINE, regular=True, nullable=False))

    def eof(self):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(END_OF_FILE, regular=False, nullable=True))

    def end_of_line(self):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(END_OF_LINE, regular=True, nullable=True))

    def start_of_line(self):
        if self.block_mode: raise SyntaxError()
        self.rules.append(GrammarNode(START_OF_LINE))

    def range(self, *args, invert=False):
        if self.block_mode: raise SyntaxError()
        self.rules.append(RangeNode(args, invert))

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
    def indented(self, count=None):
        if self.block_mode: raise SyntaxError()
        rules, self.rules = self.rules, []
        yield
        rules.append(GrammarNode(SET_LINE_PREFIX, args=dict(prefix=None, count=count), rules=self.rules))
        self.rules = rules

    @contextmanager
    def count(self, char=None, columns=None):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        counter = CountNode(dict(char=char, columns=columns), self.rules)
        yield counter.key
        rules.append(counter)
        self.rules = rules

    def backref(self):
        if self.block_mode: raise SyntaxError()
        
        @contextmanager
        def _capture():
            rules = self.rules
            self.rules = []
            c= GrammarNode(BACKREF, rules=self.rules)
            yield c.key
            rules.append(c)
            self.rules = rules

        return _capture()

    def capture_buffer(self, name):
        return self.capture_node(name, nested=False)

    def capture_node(self, name, nested=True):
        if self.block_mode: raise SyntaxError()
        if name is None:
            raise Exception('missing name')
        
        @contextmanager
        def _capture():
            rules = self.rules
            self.rules = []
            c= CaptureNode(name, args=dict(nested=nested), rules=self.rules)
            yield c.key
            rules.append(c)
            self.rules = rules

        return _capture()

    def capture_value(self, value):
        if self.block_mode: raise SyntaxError()
        self.rules.append(ValueNode(value))

    @contextmanager
    def memoize(self):
        if self.block_mode: raise SyntaxError()
        rules = self.rules
        self.rules = []
        yield
        rules.append(MemoizeNode(self.rules))
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
    def __init__(self, args, rules, key=None):
        self.args = args
        self.rules = rules
        self.key = object() if key is None else key
    def __str__(self):
        return f"'count {self.args}' in ({' '.join(str(x) for x in self.rules)})"

    def canonical(self, builder):
        rules = [r.canonical(builder) for r in self.rules]
        return CountNode(self.name, self.args, rules, self.key)
    def make_rule(self):
        args = dict(self.args)
        return ParserRule(COUNT, key=self.key, args=args, rules=[r.make_rule() for r in self.rules])

class Builtins:
    """ These methods are exported as functions inside the class defintion """
    def rule(*args, inline=False, capture=None):
        def _wrapper(rules):
            if capture:
                return CaptureNode(capture, dict(nested=True), rules)
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
        return CaptureNode(name,dict(nested=True), args)
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
    def partial_tab():
        return GrammarNode(PARTIAL_TAB)
    whitespace = GrammarNode(WHITESPACE, args={'min':0, 'max':None, 'newline': False})
    eof = GrammarNode(END_OF_FILE)
    end_of_line = GrammarNode(END_OF_LINE)
    start_of_line = GrammarNode(START_OF_LINE)
    newline = GrammarNode(NEWLINE)

class ParserRule:
    def __init__(self, kind, *, key=None,  args=None, rules=None, nullable=True, regular=False):
        self.kind = kind
        self.args = args if args else None
        self.rules = rules if rules else None
        self.nullable = nullable
        self.regular = regular
        self.key = key

    def __str__(self):
        rules =" ".join(str(r) for r in self.rules) if self.rules else None
        args = " ".join(f"{k}={v}" for k,v in self.args.items()) if self.args else None

        return "({} {})".format(self.kind, rules or args)

    def visit(self, visitor):
        visitor(self)
        if self.rules:
            for r in self.rules:
                r.visit(visitor)
    def inline(self, name, rule):
        if self.kind == RULE:
            if self.args['name'] == name and self.args['inline']:
                return rule
            else:
                return self
        if not self.rules:
            return self
        rules = [r.inline(name, rule) for r in self.rules]
        nullable = any(r.nullable for r in rules)
        regular = all(r.regular for r in rules)
        return ParserRule(self.kind, key=self.key, args=self.args, rules=rules, nullable=nullable, regular=regular)

            

# Parser


class ParserBuilder:
    def __init__(self, output, indent, placeholders):
        self.output = output
        self.placeholders = placeholders
        self.indent = indent

    def append_placeholder(self):
        key = object()
        self.placeholders[key] = len(self.output), self.indent
        self.output.append(key)
        return key

    def replace_placeholder(self, key, line):
        lineno, indent = self.placeholders.pop(key) 
        self.output[lineno] = (f"{' ' * indent}{line}")
        

    def add_indent(self, n=4):
        return ParserBuilder(self.output, self.indent+n, self.placeholders)

    def append(self, line):
        self.output.append(f"{' ' * self.indent}{line}")

    def as_string(self):
        if self.placeholders: raise Exception("no")
        return "\n".join(o.rstrip() for o in self.output)

    def extend(self, lines):
        if isinstance(lines, str): raise Exception('no')
        for line in lines:
            self.output.append(f"{' ' * self.indent}{line}")


class VarBuilder:
    def __init__(self, name,*, maxes=None, n=0):
        self.n = n
        self.name = name
        self.maxes = maxes
        if maxes is not None:
            maxes[name] = max(maxes.get(name,0), n)

    def __str__(self):
        return f"{self.name}_{self.n}" # if self.n else self.name

    def incr(self):
        return VarBuilder(self.name, maxes=self.maxes, n=self.n+1)


def compile_python(grammar, builder=None, cython=False):
    memoized = {}

    def build_subrules(rules, steps, offset, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values):
        for subrule in rules:
            build_steps(subrule, steps, offset, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values)

    def build_steps(rule, steps, offset, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values):
        # steps.append(f"print('start', {repr(str(rule))})")
        if rule.kind == SEQUENCE:
            build_subrules(rule.rules, steps, offset, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values)

        elif rule.kind == MEMOIZE:
            key = rule.key
            value = memoized.get(key)
            if not value:
                value = repr(f"memo_{len(memoized)}")
                memoized[key] = value

            children_0 = children.incr()
            offset_0 = offset.incr()
            steps.append(f"{offset_0} = {offset}")
            steps.append(f"{children_0} = [] if {children} is not None else None")
            steps.append(f"{count} = ({value}, {offset})")
            steps.append(f"if {count} in self.cache:")
            steps.append(f"    {offset_0}, {column}, {indent_column}, {children_0}, {partial_tab_offset}, {partial_tab_width} = self.cache[{count}]")
            steps.append("else:")

            steps_0 = steps.add_indent()
            steps_0.append(f"while True:")
            build_subrules(rule.rules, steps_0.add_indent(), offset_0, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children_0, count.incr(), values)
            steps_0.append(f"    break")

            steps_0.append(f"self.cache[{count}] = ({offset_0}, {column}, {indent_column}, {children_0}, {partial_tab_offset},{partial_tab_width})")

            steps.append(f"{offset} = {offset_0}")
            steps.append(f"if {children_0} is not None and {children_0} is not None:")
            steps.append(f"    {children}.extend({children_0})")
            steps.append(f"if {offset} == -1:")
            steps.append(f"    break")

        elif rule.kind == BACKREF:
            children_0 = children.incr()
            offset_0 = offset.incr()
            steps.append(f"{offset_0} = {offset}")
            if not rule.rules:
                raise Exception('bad')
            steps.append(f"while True: # start backref")
            build_subrules(rule.rules, steps.add_indent(), offset_0, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children_0, count, values)
            steps.append(f"    break")
            steps.append(f"if {offset_0} == -1:")
            steps.append(f"    {offset} = -1")
            steps.append(f"    break")

            value = VarBuilder('value', n=len(values))
            values[rule.key] = value

            steps.extend((
                f"{value} = buf[{offset}:{offset_0}]",
            ))
            steps.append(f"{offset} = {offset_0}")

        elif rule.kind == CAPTURE:
            name = repr(rule.args['name'])
            children_0 = children.incr()
            offset_0 = offset.incr()
            steps.append(f"{offset_0} = {offset}")
            if rule.rules:
                if rule.args['nested']:
                    steps.append(f"{children_0} = []")
                else:
                    steps.append(f"{children_0} = None")
                steps.append(f"while True: # start capture")
                build_subrules(rule.rules, steps.add_indent(), offset_0, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children_0, count, values)
                steps.append(f"    break")
                steps.append(f"if {offset_0} == -1:")
                steps.append(f"    {offset} = -1")
                steps.append(f"    break")
            if cython:
                node = "Node"
            else:
                node = "self.Node"

            value = VarBuilder('value', n=len(values))
            values[rule.key] = value

            steps.extend((
                # f"print(len(buf), {offset}, {offset_0}, {children})",
                f"if self.builder is not None:",
                f"    {value} = self.builder[{name}](buf, {offset}, {offset_0}, {children_0})",
                f"else:",
                f"    {value} = {node}({name}, {offset}, {offset_0}, {children_0}, None)",
                f"{children}.append({value})",
            ))
            steps.append(f"{offset} = {offset_0}")

        elif rule.kind == CHOICE:
            children_0 = children.incr()
            offset_0 = offset.incr()
            column_0 = column.incr()
            indent_column_0 = indent_column.incr()
            partial_tab_offset_0 = partial_tab_offset.incr()
            partial_tab_width_0 = partial_tab_width.incr()

            steps.append(f"while True: # start choice")

            steps_0 = steps.add_indent()
            for subrule in rule.rules:
                steps_0.append(f"{offset_0} = {offset}")
                steps_0.append(f"{column_0} = {column}")
                steps_0.append(f"{indent_column_0} = {indent_column}")
                steps_0.append(f"{partial_tab_offset_0} = {partial_tab_offset}")
                steps_0.append(f"{partial_tab_width_0} = {partial_tab_width}")
                steps_0.append(f"{children_0} = [] if {children} is not None else None")
                steps_0.append(f"while True: # case")
                build_steps(subrule, steps_0.add_indent(), offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0, prefix, children_0, count, values)
                steps_0.append(f"    break")
                steps_0.append(f"if {offset_0} != -1:")
                steps_0.append(f"    {offset} = {offset_0}")
                steps_0.append(f"    {column} = {column_0}")
                steps_0.append(f"    {indent_column} = {indent_column_0}")
                steps_0.append(f"    {partial_tab_offset} = {partial_tab_offset_0}")
                steps_0.append(f"    {partial_tab_width} = {partial_tab_width_0}")
                steps_0.append(f"    if {children_0} is not None and {children_0} is not None:")
                steps_0.append(f"        {children}.extend({children_0})")
                steps_0.append(f"    break")
                steps_0.append(f"# end case")

            steps_0.append(f"{offset} = -1 # no more choices")
            steps_0.append(f"break # end choice")
            steps.append(f"if {offset} == -1:")
            steps.append(f"    break")

        elif rule.kind == REPEAT:
            _min = rule.args['min']
            _max = rule.args['max']

            _minv = values.get(_min)
            if _minv:
                _min = _minv
            else:
                _minv = repr(_min)

            _maxv = values.get(_max)
            if _maxv: _max = _maxv
            else: _maxv = repr(_max)

            cond = "True"
            if _max:
                cond = f"{count} < {_maxv}"


            steps.extend((
                f"{count} = 0",
                f"while {cond}:",
            ))
            new_count = count.incr()
            offset_0 = offset.incr()
            column_0 = column.incr()
            indent_column_0 = indent_column.incr()
            partial_tab_offset_0 = partial_tab_offset.incr()
            partial_tab_width_0 = partial_tab_width.incr()
            steps_0 = steps.add_indent()
            children_0 = children.incr()
            steps_0.append(f"{offset_0} = {offset}")
            steps_0.append(f"{column_0} = {column}")
            steps_0.append(f"{indent_column_0} = {indent_column}")
            steps_0.append(f"{partial_tab_offset_0} = {partial_tab_offset}")
            steps_0.append(f"{partial_tab_width_0} = {partial_tab_width}")
            steps_0.append(f"{children_0} = [] if {children} is not None else None")


            steps_0.append("while True:")
            for subrule in rule.rules:
                    build_steps(subrule, steps_0.add_indent(), offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0, prefix, children_0, new_count, values)
            steps_0.append("    break")
            steps_0.append(f"if {offset_0} == -1:")
            steps_0.append(f"    break")

            steps_0.append(f"if {offset} == {offset_0}: break")
            steps_0.append(f"if {children_0} is not None and {children_0} is not None:")
            steps_0.append(f"    {children}.extend({children_0})")
            steps_0.append(f"{offset} = {offset_0}")
            steps_0.append(f"{column} = {column_0}")
            steps_0.append(f"{indent_column} = {indent_column_0}")
            steps_0.append(f"{partial_tab_offset} = {partial_tab_offset_0}")
            steps_0.append(f"{partial_tab_width} = {partial_tab_width_0}")
            steps_0.append(f"{count} += 1")
            if _max == 1:
                steps_0.append(f"break")

            if _min:
                steps.extend((
                    f"if {count} < {_minv}:",
                    f"    {offset} = -1",
                    f"    break",
                ))
            steps.append(f"if {offset} == -1:")
            steps.append(f"    break")

        elif rule.kind == LOOKAHEAD:
            steps_0 = steps.add_indent()
            children_0 = children.incr()
            offset_0 = offset.incr()
            column_0 = column.incr()
            indent_column_0 = column.incr()
            partial_tab_offset_0 = partial_tab_offset.incr()
            partial_tab_width_0 = partial_tab_width.incr()
            steps.append(f"while True: # start reject")
            steps_0.append(f"{children_0} = []")
            steps_0.append(f"{offset_0} = {offset}")
            steps_0.append(f"{column_0} = {column}")
            steps_0.append(f"{indent_column_0} = {indent_column}")
            steps_0.append(f"{partial_tab_offset_0} = {partial_tab_offset}")
            steps_0.append(f"{partial_tab_width_0} = {partial_tab_width}")
            build_subrules(rule.rules, steps_0, offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0, prefix, children_0, count, values)
            steps_0.append("break")

            steps.append(f'if {offset_0} == -1:')
            steps.append(f'    {offset} = -1')
            steps.append(f'    break')

        elif rule.kind == REJECT:
            steps_0 = steps.add_indent()
            children_0 = children.incr()
            offset_0 = offset.incr()
            column_0 = column.incr()
            indent_column_0 = indent_column.incr()
            partial_tab_offset_0 = partial_tab_offset.incr()
            partial_tab_width_0 = partial_tab_width.incr()
            steps.append(f"while True: # start reject")
            steps_0.append(f"{children_0} = []")
            steps_0.append(f"{offset_0} = {offset}")
            steps_0.append(f"{column_0} = {column}")
            steps_0.append(f"{indent_column_0} = {indent_column}")
            steps_0.append(f"{partial_tab_offset_0} = {partial_tab_offset}")
            steps_0.append(f"{partial_tab_width_0} = {partial_tab_width}")
            # steps_0.append(f'print("reject", {offset_0})')
            build_subrules(rule.rules, steps_0, offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0, prefix, children_0, count, values)
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
            offset_0 = offset.incr()
            column_0 = column.incr()
            steps.append(f"{offset_0} = {offset}")
            steps.append(f"{column_0} = {column}")
            steps.append(f"while True: # start count")
            build_subrules(rule.rules, steps.add_indent(), offset_0, column_0, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values)
            steps.append("    break")
            steps.append(f"if {offset_0} == -1:")
            steps.append(f"    {offset} = -1; break")
            # find var name
            var_name = VarBuilder('value',n=len(values))
            values[rule.key] = var_name
            if rule.args['columns']:
                value = f"{column_0} - {column}"
            elif rule.args['char']:
                value = f"buf[{offset}:{offset_0}].count({repr(rule.args['char'])})"
            else:
                raise Exception('bad')
            steps.append(f"{var_name} = {value}") 
            steps.append(f"{offset} = {offset_0}")
            steps.append(f"{column} = {column_0}")


        elif rule.kind == VALUE:
            if cython:
                node = "Node"
            else:
                node = "self.Node"
            value = rule.args['value']
            value = values.get(value, repr(value))

            steps.extend((
                f"if self.builder is not None:",
                f"    {children}.append({value})",
                f"else:",
                f"    {children}.append({node}('value', {offset}, {offset}, (), {value}))",
            ))

        elif rule.kind == SET_LINE_PREFIX:
            cond =f"chr in {repr(''.join(grammar.whitespace))}"

            cond2 =f"chr in {repr(''.join(grammar_newline))}"

            if rule.args['prefix'] is None:
                c = rule.args['count']
                if c:
                    steps.append(f"{count} = {values.get(c, repr(c))}")
                else:
                    c0 = count.incr()
                    steps.extend((
                        f"{count} = {column} - {indent_column}",
                    ))
                    
                steps.extend((
                        f"def _indent(buf, offset, buf_eof, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count={count}, allow_mixed_indent=self.allow_mixed_indent):",
                        f"    saw_tab, saw_not_tab = False, False",
                        f"    while count > 0 and offset < buf_eof:",
                        f"        chr = buf[offset]",
                        f"        if {cond}:",
                        f"            if not allow_mixed_indent:",
                        f"                if chr == '\\t': saw_tab = True",
                        f"                else: saw_not_tab = True",
                        f"                if saw_tab and saw_not_tab:",
                        f"                     offset -1; break",
                        f"            if chr != '\\t':",
                        f"                column += 1",
                        f"                offset += 1",
                        f"                count -=1",
                        f"            else:",
                        f"                if offset == partial_tab_offset and partial_tab_width > 0:",
                        f"                    width = partial_tab_width",
                        f"                else:",
                        f"                    width  = (self.tabstop-(column%self.tabstop))",
                        f"                if width <= count:",
                        f"                    column += width",
                        f"                    offset += 1",
                        f"                    count -= width",
                        f"                else:",
                        f"                    column += count",
                        f"                    partial_tab_offset = offset",
                        f"                    partial_tab_width = width-count",
                        f"                    break",
                ))
                if newline_rn:
                    steps.extend((
                        f"        elif chr == '\\r' and {offset} + 1 < buf_eof and buf[{offset}+1] == '\\n':", 
                        f"            break",
                    ))
                steps.extend((
                        f"        elif {cond2}:",
                        f"            break",
                        f"        else:",
                        f"            offset = -1",
                        f"            break",
                #        f"    print('nice', offset)",
                        f"    return offset, column, indent_column, partial_tab_offset, partial_tab_width",
                        f'{prefix}.append(_indent)',
                ))
            else:
                prule = rule.args['prefix']
                steps.append(f'{prefix}.append(self.parse_{prule})')

            steps.append(f'{indent_column} = {column}')

            steps.append('while True:')
            build_subrules(rule.rules, steps.add_indent(), offset, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values)
            steps.append('    break')

            steps.append(f'{prefix}.pop()')
            steps.append(f'if {offset} == -1: break')

        elif rule.kind == START_OF_LINE:
            offset_0 = offset.incr()
            steps.extend((
                f"if not ({column} == {indent_column} == 0):",
                f"    {offset} = -1",
                f"    break",
                f"for indent in {prefix}:",
                f"    _children, _prefix = [], []",
                f"    {offset}, {column}, {indent_column}, {partial_tab_offset}, {partial_tab_width} = indent(buf, {offset}, buf_eof, {column}, {indent_column}, _prefix, _children, {partial_tab_offset}, {partial_tab_width})",
                f"    if _prefix or _children:",
                f"       raise Exception('bar')",
                f"    if {offset} == -1:"
                f"        break",
                f"    {indent_column} = {column}",
                f"if {offset} == -1:",
                f"    break",
            ))

        elif rule.kind == RULE:
            steps.extend((
                f"{offset}, {column}, {indent_column}, {partial_tab_offset}, {partial_tab_width} = self.parse_{rule.args['name']}(buf, {offset}, buf_eof, {column}, {indent_column}, {prefix}, {children}, {partial_tab_offset}, {partial_tab_width})",
                f"if {offset} == -1: break",
                f"",
            ))

        elif rule.kind == RANGE:
            invert = rule.args['invert']
            _ord = "" if cython else "ord"
            steps.extend((
                f"if {offset} == buf_eof:",
                f"    {offset} = -1",
                f"    break",
                f"",
                f"chr = {_ord}(buf[{offset}])",
                f"",
            ))

            literals = rule.args['range']

            for idx, literal in enumerate(rule.args['range']):
                _if = {0:"if"}.get(idx, "elif")
                if '-' in literal and len(literal) == 3:
                    start, end = ord(literal[0]), repr(ord(literal[2]))

                    if start > 0:
                        start = f"{start} <= "
                    else:
                        start =""


                    if invert:
                        steps.extend((
                            f"{_if} {start}chr <= {end}:",
                            f"    {offset} = -1",
                            f"    break",
                        ))
                    else:
                        steps.extend((
                            f"{_if} {start}chr <= {end}:",
                            f"    {offset} += 1",
                            f"    {column} += 1",
                        ))

                elif len(literal) == 1:
                    literal = repr(ord(literal))
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
                            f"    {column} += 1",
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
                    f"    {column} += 1",
                ))



        elif rule.kind == LITERAL:
            literals = rule.args['literals']

            for idx, literal in enumerate(rule.args['literals']):
                _if = {0:"if"}.get(idx, "elif")

                if literal in values:
                    vliteral = values[literal]
                    length = f"len({vliteral})"
                    cond = f"buf[{offset}:{offset}+{length}] == {(vliteral)}"
                else:
                    length = len(literal)
                    vliteral = repr(literal)
                    if cython:
                        cond = [f"{offset} + {length} <= buf_eof"]
                        for i, c in enumerate(literal):
                             cond.append(f"buf[{offset}+{i}] == {repr(c)}")
                        cond = " and ".join(cond)
                    else:
                        cond = f"buf[{offset}:{offset}+{length}] == {(vliteral)}"

                steps.extend((
                    f"{_if} {cond}:",
                    f"    {offset} += {length}",
                    f"    {column} += {length}",
                ))

            steps.extend((
                f"else:",
                f"    {offset} = -1",
                f"    break",
            ))

        elif rule.kind == PARTIAL_TAB:
            steps.extend((
                f"if {offset} == {partial_tab_offset} and {partial_tab_width} > 0:",
                f"    {offset} += 1",
                f"    {column} += {partial_tab_width}",
            ))

        elif rule.kind == WHITESPACE:
            _min = rule.args['min']
            _max = rule.args['max']

            _minv = values.get(_min)
            if _minv:
                _min = _minv
            else:
                _minv = repr(_min)

            _maxv = values.get(_max)
            if _maxv:
                _max = _maxv
            else:
                _maxv = repr(_max)

            _newline = rule.args['newline']

            cond = [f"{offset} < buf_eof"]
            if _max:
                cond.append(f"{count} < {_maxv}")

            cond2 =f"chr in {repr(''.join(grammar.whitespace))}"
            cond3 =f"chr in {repr(''.join(grammar_newline))}"

            steps.extend((
                        f"{count} = 0",
                        f"while {' and '.join(cond)}:",
                        f"    chr = buf[{offset}]",
            ))

            if _newline:
                if newline_rn:
                    steps.extend((
                        f"    if chr == '\\r' and {offset} + 1 < buf_eof and buf[{offset}+1] == '\\n':", 
                        f"        {offset} +=2",
                        f"        {column} = 0",
                        f"        {indent_column} = 0",
                        f"    elif {cond3}:", # in newline
                    ))
                else:
                    steps.extend((
                        f"    if {cond3}:", # in newlne
                    ))
                steps.extend((
                        f"        {offset} +=1",
                        f"        {column} = 0",
                        f"        {indent_column} = 0",
                        f"        {count} +=1",
                        f"    elif {cond2}:",
                ))
            else:
                steps.extend((
                        f"    if {cond2}:",
                ))

            steps.extend((
                        f"        if chr == '\\t':",
                        f"            if {offset} == {partial_tab_offset} and {partial_tab_width} > 0:",
                        f"                width = {partial_tab_width}",
                        f"            else:",
                        f"                width  = (self.tabstop-({column}%self.tabstop))",
            ))
            if _max: steps.extend((
                        f"            if {count} + width > {_maxv}:",
                        f"                new_width = {_maxv} - {count}",
                        f"                {count} += new_width",
                        f"                {column} += new_width",
                        f"                {partial_tab_offset} = {offset}",
                        f"                {partial_tab_width} = width - new_width",
                        f"                break",
            ))
            steps.extend((
                        f"            {count} += width",
                        f"            {column} += width",
                        f"            {offset} += 1",
                        f"        else:",
                        f"            {count} += 1",
                        f"            {column} += 1",
                        f"            {offset} += 1",
                        f"    else:",
                        f"        break",
                ))
            if _min:
                steps.extend((
                    f"if {count} < {_minv}:",
                    f"    {offset} = -1",
                    f"    break",
                ))

            # XXX? Clear offset?
                    

        elif rule.kind == NEWLINE:
            cond =f"chr in {repr(''.join(grammar_newline))}"
            steps.extend((
                f"if {offset} < buf_eof:",
                f"    chr = buf[{offset}]",
            ))
            if newline_rn:
                steps.extend((
                    f"    if chr == '\\r' and {offset} + 1 < buf_eof and buf[{offset}+1] == '\\n':", 
                    f"        {offset} +=2",
                    f"        {column} = 0",
                    f"        {indent_column} = 0",
                    f"    elif {cond}:",
                ))
            else:
                steps.extend((
                    f"    if {cond}:",
            ))
            steps.extend((
                    f"        {offset} +=1",
                    f"        {column} = 0",
                    f"        {indent_column} = 0",
                    f"    else:",
                    f"        {offset} = -1",
                    f"        break",
                    f"else:",
                    f"    {offset} = -1",
                    f"    break",
            ))

        elif rule.kind == END_OF_LINE:
            cond =f"chr in {repr(''.join(grammar_newline))}"

            steps.extend((
                f"if {offset} < buf_eof:",
                f"    chr = buf[{offset}]",
            ))
            if newline_rn:
                steps.extend((
                    f"    if chr == '\\r' and {offset} + 1 < buf_eof and buf[{offset}+1] == '\\n':", 
                    f"        {offset} +=2",
                    f"        {column} = 0",
                    f"        {indent_column} = 0",
                    f"    elif {cond}:",
                ))
            else:
                steps.extend((
                    f"    if {cond}:",
            ))
            steps.extend((
                    f"        {offset} +=1",
                    f"        {column} = 0",
                    f"        {indent_column} = 0",
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
            args = [values.get(a, repr(a)) for a in rule.args['args']]
            steps.append(f"print('print', {', '.join(args)}, 'at' ,{offset},'col', {column}, repr(buf[{offset}:{offset}+15]), {prefix})")
        elif rule.kind == TRACE:
            steps.append(f"print('begin trace', 'at' ,{offset}, repr(buf[{offset}:{offset}+5]))")
            steps.append('while True:')
            for subrule in rule.rules:
                build_steps(subrule, steps.add_indent(), offset, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values)
                steps.append(f"    print('..... trace', 'at' ,{offset}, repr(buf[{offset}:{offset}+5]))")

            steps.append('    break')
            steps.append(f"print('exit trace', 'at' ,{offset}, repr(buf[{offset}:{offset}+5]))")
        else:
            raise Exception(f'Unknown kind {rule.kind}')

        # steps.append(f"print('end', {repr(str(rule))}, {offset})")
        steps.append("")
        return steps

    output = ParserBuilder([], 0, {})
    grammar_newline = tuple(n for n in grammar.newline if n!='\r\n') if grammar.newline else ()
    newline = repr(tuple(grammar.newline)) if grammar.newline else '()'
    newline_rn = bool(grammar.newline) and '\r\n' in grammar.newline
    whitespace = repr(tuple(grammar.whitespace)) if grammar.whitespace else '()'
    whitespace_tab = bool(grammar.whitespace) and '\t' in grammar.whitespace



    parse_node = (
        f"class Node:",
        f"    def __init__(self, name, start, end, children, value):",
        f"        self.name = name",
        f"        self.start = start",
        f"        self.end = end",
        f"        self.children = children if children is not None else ()",
        f"        self.value = value",
        f"    def __str__(self):",
        "        return '{}[{}:{}]'.format(self.name, self.start, self.end)",
        f'    def build(self, buf, builder):',
        f'        children = [child.build(buf, builder) for child in self.children]',
        f'        if self.name == "value": return self.value',
        f'        return builder[self.name](buf, self.start, self.end, children)',
        f'',
        f"",
    )
    if cython:
        output.append('# cython: language_level=3, bounds_check=False')
        output.extend(parse_node)
        output.extend((
            f"cdef class Parser:",
            f"    cdef dict builder, cache",
            f"    cdef int tabstop",
            f"    cdef int allow_mixed_indent ",
            f"",
            f"    def __init__(self, builder=None, tabstop=None, allow_mixed_indent=True):",
            f"         self.builder = builder",
            f"         self.tabstop = tabstop or {grammar.tabstop}",
            f"         self.cache = None",
            f"         self.allow_mixed_indent = allow_mixed_indent",
            "",
        ))
        output = output.add_indent(4)

    else:
        output.extend((
            f"class Parser:",
            f"    def __init__(self, builder=None, tabstop=None, allow_mixed_indent=False):",
            f"         self.builder = builder",
            f"         self.tabstop = tabstop or {grammar.tabstop}",
            f"         self.cache = None",
            f"         self.allow_mixed_indent = allow_mixed_indent",
            "",
        ))

        output = output.add_indent(4)
        output.extend(parse_node)

    start_rule = grammar.start
    output.extend((
        f"def parse(self, buf, offset=0, end=None, err=None):",
        f"    self.cache = dict()",
        f"    end = len(buf) if end is None else end",
        f"    column, indent_column, eof = offset, offset, end",
        f"    prefix, children = [], []",
        f"    new_offset, column, indent_column, partial_tab_offset, partial_tab_width = self.parse_{start_rule}(buf, offset, eof, column, indent_column, prefix, children, 0, 0)",
        f"    if children and new_offset == end: return children[-1]",
        f"    print('no', offset, new_offset, end, buf[new_offset:])",
        f"    if err is not None: raise err(buf, new_offset, 'no')",
        f"",
    ))

    varnames = {
            "offset":"cdef int", "column":"cdef int", 
            "prefix":"cdef list", "children":"cdef list", "count":"cdef int", "indent_column":"cdef int",
            "partial_tab_offset":"cdef int", "partial_tab_width": "cdef int"}
    for name, rule in grammar.rules.items():
        cdefs = {}
        if cython:
            output.append(f"cdef (int, int, int, int, int) parse_{name}(self, str buf, int offset_0, int buf_eof, int column_0, int indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):")
            output.append(f"    cdef Py_UCS4 chr")
            
            for v in varnames:
                cdefs[v] = output.add_indent(4).append_placeholder()
        else:
            output.append(f"def parse_{name}(self, buf, offset_0, buf_eof, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):")
   #     output.append(f"    print('enter {name},',offset_0,column_0,prefix_0, repr(buf[offset_0:offset_0+10]))")
        output.append(f"    while True: # note: return at end of loop")

        values = {}
        maxes = {}
        build_steps(rule,
                output.add_indent(8),
                VarBuilder("offset", maxes=maxes),
                VarBuilder('column', maxes=maxes),
                VarBuilder('indent_column', maxes=maxes),
                VarBuilder('partial_tab_offset', maxes=maxes),
                VarBuilder('partial_tab_width', maxes=maxes),
                VarBuilder('prefix', maxes=maxes),
                VarBuilder('children', maxes=maxes),
                VarBuilder("count", maxes=maxes), values, )
        if cdefs:
            for v,p in cdefs.items():
                line = ", ".join(f"{v}_{n}" for n in range(1, maxes[v]+1))
                line = f"{varnames[v]} {line}" if line else ""
                output.replace_placeholder(p, line)
        output.append(f"        break")
    #     output.append(f"    print(('exit' if offset_0 != -1 else 'fail'), '{name}', offset_0, column_0, repr(buf[offset_0: offset_0+10]))")
        output.append(f"    return offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0")
        output.append("")
    # for lineno, line in enumerate(output.output):
    #    print(lineno, '\t', line)
    return output.as_string()


def parser(grammar, builder=None):
    output = compile_python(grammar, builder)
    glob, loc = {}, {}
    exec(output, glob, loc)
    return loc['Parser'](builder)

class Grammar(metaclass=Metaclass):
    pass

Grammar.parser = classmethod(parser)
