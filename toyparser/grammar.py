from contextlib import contextmanager
from types import FunctionType
import re

import os.path

def sibling(file, fn):
    return os.path.join(os.path.dirname(file), fn)

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
class BadGrammar(Exception):
    pass

class Metaclass(type):
    """
    Allows us to provide Grammar with a special class dictionary
    and perform post processing
    """

    @classmethod
    def __prepare__(metacls, name, bases, **args):
        return GrammarDict({k:v for k,v in Builtins.__dict__.items() if not k.startswith("_")})
    def __new__(metacls, name, bases, attrs, **args):
        attrs = build_grammar_rules(attrs, args)
        return super().__new__(metacls, name, bases, attrs)

class GrammarRule:
    """ Wraps rules that are assigned to the class dictionary"""
    def __init__(self, rule, options):
        self.rule = rule
        self.options = options

    def canonical(self, builder):
        return self.rule.canonical(builder)

class GrammarRuleSet:
    """ Allows for multiple definitions of rules """


    def __init__(self, rules):
        self.rules = rules

    def append(self, value):
        inner_rule = value.rule
        if inner_rule is self: raise BadGrammar('recursive')
        if isinstance(inner_rule, ChoiceNode):
            if self in inner_rule.rules: raise Exception()
        if isinstance(value, GrammarRule):
            self.rules.append(value)
        else:
            raise BadGrammar('Rule', value, 'is not a grammar definition')

    def canonical(self, rulebuilder):
        rules = []
        for rule in self.rules:
            rules.append(rule.canonical(rulebuilder))
        if len(rules) == 1:
            return rules[0]
        return ChoiceNode(rules)

    def options(self):
        opts = {}
        for rule in self.rules:
            for k,v in rule.options.items():
                if k not in opts:
                    opts[k]=v
                else:
                    raise Exception('no')
        return opts
                

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
            elif is_ruleset and not is_rule:
                raise BadGrammar('rule', key, 'reassigned')
            else:
                raise BadGrammar('non rule', key, 'reassigned with rule')
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
INDENT = 'indent'
DEDENT = 'dedent'
END_OF_LINE = 'end-of-line'
WHITESPACE = 'whitespace'
PARTIAL_TAB = 'partial_tab'
NEWLINE = 'newline'
END_OF_FILE = 'end-of-file'

SET_LINE_PREFIX = 'set-line-prefix'

LOOKAHEAD = 'lookahead'
REJECT = 'reject'
COUNT = 'count'
VALUE = 'value'
VARIABLE = 'variable'
UNTIL = 'until'
SET_VAR = 'set-variable'
REGULAR ='regular'

RULE = 'rule'
LITERAL = 'literal'
RANGE = 'range'
SEQUENCE = 'seq'
PARALLEL = 'parallel'
CAPTURE = 'capture'
PARSEAHEAD = 'parseahead'
BACKREF = 'backref'
COLUMN = 'column'
CHOICE = 'choice'
REPEAT = 'repeat'
MEMOIZE = 'memoize'

SHUNT = 'shunt'
ACCEPT_IF = 'accept-if'
REJECT_IF = 'reject-if'
PRINT = 'print'
TRACE = 'trace'

class Key:
    pass

class GrammarNode:
    def __init__(self, kind, *, key=None, rules=None, args=None):
        self.kind = kind
        self.rules = rules
        self.args = args
        self.key = key if key else Key()

    def __str__(self):
        rules = ' '.join(str(x) for x in self.rules) if self.rules else ''
        args = str(self.args) if self.args else ''

        return f"{self.kind} ({rules or args})"

    def __or__(self, right):
        return ChoiceNode([self, right])

    def canonical(self, builder):
        rules = [r.canonical(builder) for r in self.rules] if self.rules else None
        return GrammarNode(self.kind, key=self.key, rules=rules, args=self.args,)

    def make_rule(self):
        rules = [r.make_rule() for r in self.rules] if self.rules else None
        return ParserRule(self.kind, key=self.key, rules=rules, args=self.args)

class FunctionNode(GrammarNode):
    def __init__(self, fn, wrapper):
        self.fn = fn
        self.wrapper = wrapper

    def canonical(self, builder):
        return self.wrapper(builder.from_function(self.fn))

    def make_rule(self):
        raise Exception('Canonicalise FunctionNodes first')

class NamedNode(GrammarNode):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def canonical(self, builder):
        return self

    def make_rule(self):
        return ParserRule(RULE,  args=dict(name=self.name, inline=False))

class ChoiceNode(GrammarNode):
    def __init__(self, rules):
        GrammarNode.__init__(self, CHOICE, rules=rules)

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
        return ParserRule(CHOICE, rules=rules)

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
        return ParserRule(SEQUENCE, rules=rules)

# Builders
NULL = object()

class FunctionBuilder:
    def __init__(self, names):
        self.rules = None
        self.block_mode = "build"
        class Rule:
            def __init__(inner, name, rule):
                inner.name, inner.rule = name, rule
            def __call__(inner):
                if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
                self.rules.append(inner.rule)
            def repeat(inner, min=0, max=None):
                if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
                self.rules.append(GrammarNode(REPEAT, rules=[inner.rule], args=dict(min=min, max=max)))
            def optional(inner):
                if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
                self.rules.append(GrammarNode(REPEAT, rules=[inner.rule], args=dict(min=0, max=1)))
            def inline(inner):
                if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
                self.rules.append(GrammarNode(RULE, args=dict(name=inner.name, inline=True)))
            def lookahead(inner):
                if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
                self.rules.append(GrammarNode(LOOKAHEAD, rules=[inner.rule]))
            def reject(inner):
                if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
                self.rules.append(GrammarNode(REJECT, rules=[inner.rule]))

            @contextmanager
            def as_indent(inner, dedent=None):
                if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
                rules, self.rules = self.rules, []
                yield
                rules.append(GrammarNode(SET_LINE_PREFIX, args=dict(indent=inner.name, dedent=dedent, count=None), rules=self.rules))
                self.rules = rules

            @contextmanager
            def as_dedent(inner, count=None):
                if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
                rules, self.rules = self.rules, []
                yield
                rules.append(GrammarNode(SET_LINE_PREFIX, args=dict(indent=None, count=count, dedent=inner.name), rules=self.rules))
                self.rules = rules

        for name, rule in names.items():
            if hasattr(self, name): raise BadGrammar('Can\'t override ',name,'with rule. Rename it')
            setattr(self, name, Rule(name, rule))

    def from_function(self, fn):
        if self.block_mode != "build": raise SyntaxError()
        self.block_mode = None
        self.rules = []

        fn(self)

        if self.block_mode: raise SyntaxError()
        self.block_mode = "build"
        rules, self.rules = self.rules, None

        return rules

    def rule(self, rule):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        self.rules.append(rule.rule)

    def literal(self, *args, transform=None):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        if any(a == "" for a in args): raise BadGrammar("empty literal")
        node = GrammarNode(LITERAL, args=dict(literals=args, transform=transform))
        self.rules.append(node)

    def whitespace(self, min=0, max=None, newline=False):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        self.rules.append(GrammarNode(WHITESPACE, args=dict(min=min, max=max, newline=newline)))

    def partial_tab(self,):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        self.rules.append(GrammarNode(PARTIAL_TAB))

    def newline(self):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        self.rules.append(GrammarNode(NEWLINE))

    def end_of_file(self):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        self.rules.append(GrammarNode(END_OF_FILE ))

    def end_of_line(self):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        self.rules.append(GrammarNode(END_OF_LINE, ))

    def start_of_line(self):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        self.rules.append(GrammarNode(START_OF_LINE))

    def indent(self, partial=False):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        self.rules.append(GrammarNode(INDENT, args=dict(partial=partial)))

    def dedent(self):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        self.rules.append(GrammarNode(DEDENT))

    def range(self, *args, invert=False, unicode_whitespace=None, unicode_punctuation=None, unicode_newline=None):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        named_ranges = dict(
                unicode_whitespace=unicode_whitespace,
                unicode_newline=unicode_newline,
                unicode_punctuation=unicode_punctuation,
        )
        self.rules.append(GrammarNode(RANGE, args=dict(range=args, invert=invert, named_ranges=named_ranges)))

    def print(self, *args):
        if self.block_mode: raise SyntaxError()
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        self.rules.append(GrammarNode(PRINT, args={'args':args}))

    def reject_if(self, cond):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        self.rules.append(GrammarNode(REJECT_IF, args=dict(cond=cond)))

    def accept_if(self, cond):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        self.rules.append(GrammarNode(ACCEPT_IF, args=dict(cond=cond)))

    @contextmanager
    def indented(self, count=None, indent=None, dedent=None):
        indent = indent.name if indent else None
        dedent = dedent.name if dedent else None
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        rules, self.rules = self.rules, []
        yield
        rules.append(GrammarNode(SET_LINE_PREFIX, args=dict(indent=indent, dedent=dedent, count=count), rules=self.rules))
        self.rules = rules

    @contextmanager
    def count(self, char=None, columns=None):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        rules = self.rules
        self.rules = []
        counter = GrammarNode(COUNT, args=dict(char=char, columns=columns), rules=self.rules)
        yield counter.key
        rules.append(counter)
        self.rules = rules

    def column(self, from_prefix=False):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        o = GrammarNode(COLUMN, args=dict(from_prefix=from_prefix))
        self.rules.append(o)
        return o.key

    def backref(self):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        
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

    def capture_node(self, name, nested=True, value=None, parent=None):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        if name is None:
            raise Exception('missing name')
        
        @contextmanager
        def _capture():
            rules = self.rules
            self.rules = []
            c= GrammarNode(CAPTURE, args=dict(name=name, nested=nested, value=value, parent=None), rules=self.rules)
            yield c.key
            rules.append(c)
            self.rules = rules

        return _capture()

    def capture_value(self, value, name="value"):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        node = GrammarNode(VALUE, args=dict(name=name, value=value))
        self.rules.append(node)

    @contextmanager
    def regular(self, name=None):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        rules = self.rules
        self.rules = []
        node = GrammarNode(REGULAR, args=dict(name=name), rules=self.rules)
        yield node.key
        rules.append(node)
        self.rules = rules
    @contextmanager
    def until(self, offset):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        rules = self.rules
        self.rules = []
        node = GrammarNode(UNTIL, args=dict(offset=offset), rules=self.rules)
        yield node.key
        rules.append(node)
        self.rules = rules

    @contextmanager
    def variable(self, value):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        rules = self.rules
        self.rules = []
        node = GrammarNode(VARIABLE, args=dict(value=value), rules=self.rules)
        yield node.key
        rules.append(node)
        self.rules = rules

    @contextmanager
    def parseahead(self):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        rules = self.rules
        self.rules = []
        node = GrammarNode(PARSEAHEAD, rules=self.rules)
        yield node.key
        rules.append(node)
        self.rules = rules

    def set_variable(self, var, value):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        node = GrammarNode(SET_VAR, args=dict(var=var, value=value))
        self.rules.append(node)

    @contextmanager
    def memoize(self):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        rules = self.rules
        self.rules = []
        yield
        rules.append(GrammarNode(MEMOIZE, rules=self.rules))
        self.rules = rules

    @contextmanager
    def trace(self, active=True):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        rules = self.rules
        self.rules = []
        yield
        if active:
            rules.append(GrammarNode(TRACE, rules=self.rules))
        else:
            rules.extend(self.rules)
        self.rules = rules

    @contextmanager
    def lookahead(self, *, offset=0):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        rules = self.rules
        self.rules = []
        yield
        rules.append(GrammarNode(LOOKAHEAD, rules=self.rules, args=dict(offset=offset)))
        self.rules = rules

    @contextmanager
    def reject(self, *, offset=0):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        rules = self.rules
        self.rules = []
        yield
        rules.append(GrammarNode(REJECT, rules=self.rules, args=dict(offset=offset)))
        self.rules = rules

    @contextmanager
    def choice(self):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        rules = self.rules
        self.rules = []
        self.block_mode = "choice"
        yield
        if self.block_mode != "choice": raise Exception('Buggy code has wiped context')
        self.block_mode = None
        rules.append(ChoiceNode(self.rules))
        self.rules = rules

    @contextmanager
    def parallel(self):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        rules = self.rules
        self.rules = []
        self.block_mode = "parallel"
        yield
        if self.block_mode != "parallel": raise Exception('Buggy code has wiped context')
        self.block_mode = None
        rules.append(GrammarNode(PARALLEL, rules=self.rules))
        self.rules = rules

    @contextmanager
    def case(self):
        if self.block_mode not in ("choice", "parallel"): raise BadGrammar('Case outside of choice')
        old = self.block_mode
        rules = self.rules
        self.rules = []
        self.block_mode = None
        yield
        if self.block_mode: raise SyntaxError()
        self.block_mode = old
        rules.append(SequenceNode(self.rules))
        self.rules = rules

    @contextmanager
    def repeat(self, min=0, max=None):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        rules = self.rules
        self.rules = []
        r = GrammarNode(REPEAT, rules=self.rules, args=dict(min=min, max=max))
        yield r.key
        rules.append(r)
        self.rules = rules

    @contextmanager
    def optional(self):
        if self.block_mode: raise BadGrammar('Can\'t invoke rule inside', self.block_mode)
        rules = self.rules
        self.rules = []
        yield
        rules.append(GrammarNode(REPEAT, rules=self.rules, args=dict(min=0, max=1)))
        self.rules = rules

UNDEF = object()
class Builtins:
    """ These methods are exported as functions inside the class defintion """
    def rule(*args, start=UNDEF, inline=UNDEF, capture=None):
        options = {}
        if inline is not UNDEF: options['inline'] = inline
        if start is not UNDEF: options['start'] = start
        def _wrapper(rules):
            if capture:
                return GrammarNode(CAPTURE,args=dict(name=capture, nested=True, value=None), rules=rules)
            elif len(rules) > 1:
                return SequenceNode(rules)
            else:
                return rules[0]
        if len(args) > 0:
            return GrammarRule(_wrapper(args), options=options)
        else:
            def _decorator(fn):
                return GrammarRule(FunctionNode(fn, _wrapper), options=options)
            return _decorator

    def capture(name, *args):
        return GrammarRoad(CAPURE, dict(name=capture, nested=True), rules=args)
    def capture_value(arg):
        return GrammarNode(VALUE, args=dict(value=arg))
    def literal(*args):
        if any(a == "" for a in args): raise BadGrammar("empty literal")
        node = GrammarNode(LITERAL, args=dict(literals=args, transform=None))
        return node
    def reject(*args):
        return GrammarNode(REJECT, rules=args, args=dict(offset=0))
    def lookahead(*args):
        return GrammarNode(LOOKAHEAD, rules=args, args=dict(offset=0))
    def trace(*args):
        return GrammarNode(TRACE, rules=args)
    def range(*args, invert=False):
        return GrammarNode(RANGE, args=dict(range=args, invert=invert, named_ranges={}))
    def repeat(*args, min=0, max=None):
        return GrammarNode(REPEAT, rules=args, args=dict(min=min, max=max))
    def optional(*args):
        return GrammarNode(REPEAT, rules=args, args=dict(min=0, max=1))
    def choice(*args):
        return ChoiceNode(args)
    def partial_tab():
        return GrammarNode(PARTIAL_TAB)
    whitespace = GrammarNode(WHITESPACE, args={'min':0, 'max':None, 'newline': False})
    end_of_file = GrammarNode(END_OF_FILE)
    end_of_line = GrammarNode(END_OF_LINE)
    start_of_line = GrammarNode(START_OF_LINE)
    newline = GrammarNode(NEWLINE)


def build_grammar_rules(attrs, args):
    start = args.get('start')
    whitespace = args.get('whitespace')
    newline = args.get('newline')
    capture = args.get('capture')
    tabstop = args.get('tabstop')

    for name in attrs.named_rules:
        if name not in attrs:
            raise BadGrammar('missing rule', name)
    if whitespace:
        for x in whitespace:
            if len(x) != 1: raise BadGrammar('Whitespace characters must be exactly one codepoint.')
    if newline:
        for x in newline:
            if len(x) != 1 and x != "\r\n": raise BadGrammar('Newline characters must be exactly one codepoint, or CRLF.')
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
    rule_options = {k:r.options() for k,r in rules.items()}
    if start is None:
        candidates = []
        for name, options in rule_options.items():
            if options.get('start'):
                candidates.append(name)
        if len(candidates)==1:
            start = candidates[0]

    rules = {k:r.canonical(builder).make_rule() for k,r in rules.items()}
    
    grammar_options = {
            'start' : start,
            'capture': capture or start,
            'whitespace': whitespace,
            'newline': newline,
            'tabstop': tabstop or 8,
            'inline': args.get('inline', False)
    }

    ## inline transform

    rule_childs = {}
    dont_pop = set()
    if start:
        dont_pop.add(start)
    for name, rule in rules.items():
        seen = set()
        def visits(rule):
            if rule.kind == RULE:
                seen.add(rule.args['name'])
            if rule.kind == SET_LINE_PREFIX:
                indent = rule.args['indent']
                dedent = rule.args['dedent']
                if indent: dont_pop.add(indent)
                if dedent: dont_pop.add(dedent)
            
        rule.visit_head(visits)
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
            rules[name] = rules[name].inline(n, rules[n], rule_options[n], grammar_options)
            
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
                    if rule.kind == SET_LINE_PREFIX and rule.args['indent'] == n:
                        safe = False
                    if rule.kind == SET_LINE_PREFIX and rule.args.get('dedent') == n:
                        safe = False
                rule.visit_head(_visit)
                if not safe: break
            if safe:
                rules.pop(n)

    ## regular

    def _regular(rule):
        if rule.kind == LITERAL:
            rule.regular = all(isinstance(l, str) for l in rule.args['literals'])
        elif rule.kind == RANGE:
            if any(v for v in rule.args['named_ranges'].values()):
                rule.regular = False
            else:
                rule.regular = all(isinstance(l, str) for l in rule.args['range']) 
        elif rule.kind == REPEAT:
            _min,_max= rule.args['min'], rule.args['max'] 
            rule.regular = all((
                _min is None or isinstance(_min, int), 
                _max is None or isinstance(_max, int), 
                all(r.regular for r in rule.rules)))
        elif rule.kind == SEQUENCE:
            rule.regular = all(r.regular for r in rule.rules)
        elif rule.kind == REGULAR:
            rule.regular = all(r.regular for r in rule.rules)
        elif rule.kind == CHOICE:
            rule.regular = all(r.regular for r in rule.rules)
        else:
            rule.regular = False
    def _lift_regular(rule):
        if rule.regular:
            if rule.kind == REGULAR:
                rule.args['rule'] = ParserRule(SEQUENCE, rules=rule.rules)
                rule.rules = None
                return rule
            if rule.kind == LITERAL and len(rule.args['literals']) == 1:
                return rule
            return ParserRule(REGULAR, args=dict(rule=rule, name=None))
        elif rule.kind == REGULAR:
            raise Exception('no')
        return rule

    for name in list(rules):
        rules[name].visit_tail(_regular)
        rules[name] = rules[name].transform_head(_lift_regular)

    
    ## build attrs

    new_attrs.update(grammar_options)

    new_attrs['rules'] = rules
    new_attrs['rule_options'] = rule_options

    return new_attrs

class ParserRule:
    def __init__(self, kind, *, key=None,  args=None, rules=None, nullable=None, regular=None):
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

    def re_key(self):
        keys = {}
        def _visitor(node):
            new_key = Key()
            old_key = node.key
            keys[old_key] = new_key
        self.visit_head(_visitor)

        def _re_key(node, children):

            def r(v):
                if isinstance(v, Key): return keys[v]
                if isinstance(v, tuple): return tuple(r(x) for x in v)
                if isinstance(v, list): return list(r(x) for x in v)
                if isinstance(v, dict): return {k:r(x) for k,x in v.items()}
                return v

            args = {k: r(v) for k,v in node.args.items()} if node.args else None
            key = keys[node.key]
            node = ParserRule( node.kind, key=key, rules=children,  args = args, nullable=node.nullable, regular=node.regular)
            return node
        return self.transform_tail(_re_key)

    def visit_head(self, visitor):
        visitor(self)
        if self.rules:
            for r in self.rules:
                r.visit_head(visitor)

    def visit_tail(self, visitor):
        if self.rules:
            for r in self.rules:
                r.visit_tail(visitor)
        visitor(self)

    def transform_head(self, visitor):
        self = visitor(self)
        if self.rules:
            self.rules = [r.transform_head(visitor) for r in self.rules]
        return self 

    def transform_tail(self, visitor):
        if self.rules:
            rules = [r.transform_tail(visitor) for r in self.rules]
            return visitor(self, rules)
        else:
            return visitor(self, self.rules)

    def inline(self, name, rule, rule_options, grammar_options):
        if self.kind == RULE:
            if self.args['name'] == name and (grammar_options.get('inline') or self.args['inline'] or rule_options.get('inline')):
                r = rule.re_key()
                return r
            else:
                return self
        if not self.rules:
            return self
        self.rules = [r.inline(name, rule, rule_options, grammar_options) for r in self.rules]
        return self

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
        if self.placeholders: raise Exception("Codegen leftover placeholders in output")
        return "\n".join(o.rstrip() for o in self.output)

    def extend(self, lines):
        if isinstance(lines, str): raise Exception('Dont use extend with strings, pal')
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


def compile_python(grammar, cython=False, wrap=False):
    memoized = {}
    regexes = {}
    use_regexes = not cython
    node = "Node"
    if cython:
        wrap = False

    def build_subrules(rules, steps, offset, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values):
        for subrule in rules:
            build_steps(subrule, steps, offset, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values)

    def build_steps(rule, steps, offset, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values):
        # steps.append(f"print('start', {repr(str(rule))})")
        if rule.kind == REGULAR:
            if not use_regexes:
                build_steps(rule.args['rule'], steps, offset, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values)
            else:
                regex = rule.args['name']
                steps.extend((
                    f"_match = {regex}.match(buf, {offset})",
                    #f"print({repr(rule.args['regex'])})",
                    #f"print(('no: ' + buf[{offset}:{offset}+15]) if not _match else buf[{offset}:_match.end()])",
                    f"if _match:",
                    f"    _end = _match.end()",
                    f"    {column} += (_end - {offset})",
                    f"    {offset} = _end",
                    f"else:",
                    f"    {offset} = -1",
                    f"    break",
                ))
        elif rule.kind == SEQUENCE:
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
            steps.append(f"    {offset_0}, {column}, {indent_column}[:], {children_0}, {partial_tab_offset}, {partial_tab_width} = self.cache[{count}]")
            steps.append("else:")

            steps_0 = steps.add_indent()
            steps_0.append(f"while True:")
            build_subrules(rule.rules, steps_0.add_indent(), offset_0, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children_0, count.incr(), values)
            steps_0.append(f"    break")

            steps_0.append(f"self.cache[{count}] = ({offset_0}, {column}, list({indent_column}), {children_0}, {partial_tab_offset},{partial_tab_width})")

            steps.append(f"{offset} = {offset_0}")
            steps.append(f"if {children_0} is not None and {children_0} is not None:")
            steps.append(f"    {children}.extend({children_0})")
            steps.append(f"if {offset} == -1:")
            steps.append(f"    break")

        elif rule.kind == BACKREF:
            offset_0 = offset.incr()
            steps.append(f"{offset_0} = {offset}")
            if not rule.rules:
                raise Exception('empty rules')

            value = VarBuilder('value', n=len(values))
            values[rule.key] = value

            steps.append(f"while True: # start backref")
            build_subrules(rule.rules, steps.add_indent(), offset_0, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values)
            steps.append(f"    break")
            steps.append(f"if {offset_0} == -1:")
            steps.append(f"    {offset} = -1")
            steps.append(f"    break")


            steps.extend((
                f"{value} = buf[{offset}:{offset_0}]",
            ))
            steps.append(f"{offset} = {offset_0}")

        elif rule.kind == COLUMN:
            value = VarBuilder('value', n=len(values))
            values[rule.key] = value

            if rule.args.get('from_prefix'):
                steps.append( f"{value} = {column} - {indent_column}[len({indent_column})-1]")
            else:
                steps.append( f"{value} = {column}")

        elif rule.kind == CAPTURE:
            children_0 = children.incr()
            value = VarBuilder('value', n=len(values))
            if rule.key in values: raise Exception('what', rule.key)
            values[rule.key] = value

            if rule.args['nested']:
                steps.append(f"{children_0} = []")
            else:
                steps.append(f"{children_0} = None")

            steps.append(f"{value} = {node}(None, {offset}, {offset}, {column}, {column}, {children_0}, None)")
            if rule.rules:
                steps.append(f"while True: # start capture")
                build_subrules(rule.rules, steps.add_indent(), offset, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children_0, count, values)
                steps.append(f"    break")
                steps.append(f"if {offset} == -1:")
                steps.append(f"    break")

            name = rule.args['name']
            name = values.get(name, repr(name))

            captured_value = rule.args['value'] 
            captured_value = values.get(captured_value, repr(captured_value))

            steps.extend((
                # f"print(len(buf), {offset}, {offset_0}, {children})",
                f"{value}.name = {name}",
                f"{value}.end = {offset}",
                f"{value}.end_column = {column}",
                f"{value}.value = {captured_value}",
            ))

            if rule.args.get('parent'):
                raise Exception('broken')
                key = rule.args['parent']
                parent = values[key]
            else:
                parent = children

            steps.append(f"{parent}.append({value})")

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
                steps_0.append(f"{indent_column_0} = list({indent_column})")
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
            value = VarBuilder('value', n=len(values))
            if rule.key in values: raise Exception('what', rule.key)
            values[rule.key] = value

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
            if _max is not None:
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
            steps_0.append(f"{indent_column_0} = list({indent_column})")
            steps_0.append(f"{partial_tab_offset_0} = {partial_tab_offset}")
            steps_0.append(f"{partial_tab_width_0} = {partial_tab_width}")
            steps_0.append(f"{children_0} = [] if {children} is not None else None")


            steps_0.append("while True:")
            steps_0.append(f"    #print('entry rep rule', {offset}, {offset_0})")
            for subrule in rule.rules:
                    build_steps(subrule, steps_0.add_indent(), offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0, prefix, children_0, new_count, values)
            steps_0.append(f"    #print('safe exit rep rule', {offset}, {offset_0})")
            steps_0.append("    break")
            steps_0.append(f"#print('exit rep rule', {offset}, {offset_0})")
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

            if _min is not None and _min != 0:
                steps.extend((
                    f"if {count} < {_minv}:",
                    f"#    print('min exit', {offset})",
                    f"    {offset} = -1",
                    f"    break",
                ))
            steps.append(f"if {offset} == -1:")
            steps.append(f"    break")
            steps.append(f"{value} = {count}")

        elif rule.kind == PARSEAHEAD:
            steps_0 = steps.add_indent()
            offset_0 = offset.incr()
            column_0 = column.incr()
            indent_column_0 = indent_column.incr()
            partial_tab_offset_0 = partial_tab_offset.incr()
            partial_tab_width_0 = partial_tab_width.incr()
            steps.append(f"while True: # start parse ahead")
            steps_0.append(f"{offset_0} = {offset}")
            steps_0.append(f"{column_0} = {column}")
            steps_0.append(f"{indent_column_0} = list({indent_column})")
            steps_0.append(f"{partial_tab_offset_0} = {partial_tab_offset}")
            steps_0.append(f"{partial_tab_width_0} = {partial_tab_width}")
            build_subrules(rule.rules, steps_0, offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0, prefix, children, count, values)
            steps_0.append("break")

            steps.append(f'if {offset_0} == -1:')
            steps.append(f'    {offset} = -1')
            steps.append(f'    break')
             
            var_name = VarBuilder('value',n=len(values))
            values[rule.key] = var_name
            
            steps.append(f'{var_name} = {offset_0}')
        elif rule.kind == UNTIL:
            value = rule.args['offset']
            value = values.get(value, repr(value))

            offset_0 = offset.incr()
            count = count.incr()
            steps.append(f"{offset_0} = {offset}")
            steps.append(f"{count} = buf_eof")
            steps.append(f"buf_eof = {value}")
            if not rule.rules:
                raise Exception('empty rules')
            steps.append(f"while True: # start until")
            build_subrules(rule.rules, steps.add_indent(), offset_0, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count.incr(), values)
            steps.append(f"    break")
            steps.append(f"buf_eof = {count}")
            steps.append(f"if {offset_0} == -1 or {offset_0} != {value}:")
            steps.append(f"    {offset} = -1")
            steps.append(f"    break")

            steps.append(f"{offset} = {offset_0}")

        elif rule.kind == PARALLEL:
            children_0 = children.incr()
            offset_0 = offset.incr()
            column_0 = column.incr()
            indent_column_0 = indent_column.incr()
            partial_tab_offset_0 = partial_tab_offset.incr()
            partial_tab_width_0 = partial_tab_width.incr()
            count_0 = count.incr()
            count_1 = count_0.incr()

            steps.append(f"{count} = buf_eof")
            steps.append(f"{count_0} = buf_eof")
            steps.append(f"{children_0} = [] if {children} is not None else None")
            steps.append(f"while True: # start parallel")

            steps_0 = steps.add_indent()
            for n, subrule in enumerate(rule.rules):
                steps_0.append(f"{offset_0} = {offset}")
                steps_0.append(f"{column_0} = {column}")
                steps_0.append(f"{indent_column_0} = list({indent_column})")
                steps_0.append(f"{partial_tab_offset_0} = {partial_tab_offset}")
                steps_0.append(f"{partial_tab_width_0} = {partial_tab_width}")
                if n > 0:
                    steps_0.append(f"buf_eof = {count_0}")
                steps_0.append(f"while True: # case")
                build_steps(subrule, steps_0.add_indent(), offset_0, column_0, indent_column_0, partial_tab_offset_0, partial_tab_width_0, prefix, children_0, count_1, values)
                steps_0.append(f"    break")

                steps_0.append(f"if {offset_0} == -1:")
                steps_0.append(f"    {offset} = -1")
                steps_0.append(f"    break")
                if n == 0:
                    steps_0.append(f"{count_0} = {offset_0}")
                else:
                    steps_0.append(f"if {offset_0} != {count_0}:")
                    steps_0.append(f"    {offset} = -1")
                    steps_0.append(f"    break")

                steps_0.append(f"# end case")

            steps_0.append(f"break # end parallel")

            steps.append(f"buf_eof = {count}")
            steps.append(f"if {offset} == -1:")
            steps.append(f"    break")
            steps.append(f"{offset} = {offset_0}")
            steps.append(f"{column} = {column_0}")
            steps.append(f"{indent_column} = {indent_column_0}")
            steps.append(f"{partial_tab_offset} = {partial_tab_offset_0}")
            steps.append(f"{partial_tab_width} = {partial_tab_width_0}")
            steps.append(f"if {children_0} is not None and {children_0} is not None:")
            steps.append(f"    {children}.extend({children_0})")


        elif rule.kind == LOOKAHEAD:
            steps_0 = steps.add_indent()
            children_0 = children.incr()
            offset_0 = offset.incr()
            column_0 = column.incr()
            indent_column_0 = indent_column.incr()
            partial_tab_offset_0 = partial_tab_offset.incr()
            partial_tab_width_0 = partial_tab_width.incr()
            steps.append(f"while True: # start lookahed")
            steps_0.append(f"{children_0} = []")
            steps_0.append(f"{offset_0} = {offset} + {rule.args['offset']}")
            steps_0.append(f"{column_0} = {column}")
            steps_0.append(f"{indent_column_0} = list({indent_column})")
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
            steps_0.append(f"{offset_0} = {offset} + {rule.args['offset']}")
            steps_0.append(f"{column_0} = {column}")
            steps_0.append(f"{indent_column_0} = list({indent_column})")
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
            # find var name
            var_name = VarBuilder('value',n=len(values))
            values[rule.key] = var_name
            offset_0 = offset.incr()
            column_0 = column.incr()
            steps.append(f"{offset_0} = {offset}")
            steps.append(f"{column_0} = {column}")
            steps.append(f"while True: # start count")
            build_subrules(rule.rules, steps.add_indent(), offset_0, column_0, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values)
            steps.append("    break")
            steps.append(f"if {offset_0} == -1:")
            steps.append(f"    {offset} = -1; break")

            if rule.args['columns']:
                value = f"{column_0} - {column}"
            elif rule.args['char']:
                char = rule.args['char']
                char = values.get(char, repr(char))
                value = f"buf[{offset}:{offset_0}].count({char})"
            else:
                raise Exception('bad args to count rule')
            steps.append(f"{var_name} = {value}") 
            steps.append(f"{offset} = {offset_0}")
            steps.append(f"{column} = {column_0}")

        elif rule.kind == SET_VAR:
            var = rule.args['var']
            var = values.get(var)
            value = rule.args['value']
            value = values.get(value, repr(value))

            steps.append(f"{var} = {value}")


        elif rule.kind == VARIABLE:
            value = VarBuilder('value', n=len(values))
            values[rule.key] = value
            steps.append(f"{value} = {repr(rule.args['value'])}")
            offset_0 = offset.incr()
            steps.append(f"{offset_0} = {offset}")
            if not rule.rules:
                raise Exception('empty rules')
            steps.append(f"while True: # start backref")
            build_subrules(rule.rules, steps.add_indent(), offset_0, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values)
            steps.append(f"    break")
            steps.append(f"if {offset_0} == -1:")
            steps.append(f"    {offset} = -1")
            steps.append(f"    break")

            steps.append(f"{offset} = {offset_0}")

        elif rule.kind == VALUE:
            value = rule.args['value']
            name = rule.args['name']
            value = values.get(value, repr(value))

            steps.extend((
                f"{children}.append({node}({repr(name)}, {offset}, {offset}, {column}, {column}, (), {value}))",
            ))

        elif rule.kind == SET_LINE_PREFIX:
            cond =f"codepoint in {repr(''.join(grammar.whitespace))}"

            cond2 =f"codepoint in {repr(''.join(grammar_newline))}"

            if rule.args['indent'] is None:
                c = rule.args['count']
                if c:
                    steps.append(f"{count} = {values.get(c, repr(c))}")
                else:
                    c0 = count.incr()
                    steps.extend((
                        f"{count} = {column} - {indent_column}[len({indent_column})-1]",
                    ))

                steps.append(f"# print({count}, 'indent')")
                    
                steps.extend((
                        f"def _indent(buf, buf_start, buf_eof, offset, column, indent_column,  prefix,  children, partial_tab_offset, partial_tab_width, count={count}, allow_mixed_indent=self.allow_mixed_indent):",
                        f"    saw_tab, saw_not_tab = False, False",
                        f"    start_column, start_offset = column, offset",
                        f"    if count < 0: offset = -1",
                        f"    while count > 0 and offset < buf_eof:",
                        f"        codepoint = buf[offset]",
                        f"        if {cond}:",
                        f"            if not allow_mixed_indent:",
                        f"                if codepoint == '\\t': saw_tab = True",
                        f"                else: saw_not_tab = True",
                        f"                if saw_tab and saw_not_tab:",
                        f"                     offset -1; break",
                        f"            if codepoint != '\\t':",
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
                        f"        elif codepoint == '\\r' and {offset} + 1 < buf_eof and buf[{offset}+1] == '\\n':", 
                        f"            break",
                    ))
                steps.extend((
                        f"        elif {cond2}:",
                        f"            break",
                        f"        else:",
                        f"            offset = -1",
                        f"            break",
                        f"    return offset, column, partial_tab_offset, partial_tab_width",
                ))


                if not rule.args['dedent']:
                    steps.extend((
                        f'{prefix}.append((_indent, None))',
                    ))

                else:
                    dedent = rule.args['dedent']
                    if cython:
                        steps.append(f'_dedent = lambda b, st, en, off, col, idt, pf, ch, tab_off, tab_w:'
                                 f'self.parse_{dedent}(b, st, en, off, col, idt, pf, ch, tab_off, tab_w)')
                        steps.append(f'{prefix}.append((_indent, _dedent))')
                    else:
                        dedent = f"self.parse_{dedent}" if dedent else repr(None)
                        steps.append(f'{prefix}.append((_indent, {dedent}))')
            else:
                prule = rule.args['indent']
                dedent = rule.args['dedent']
                if cython:
                    steps.append(f'_indent = lambda b, st, en, off, col, idt, pf, ch, tab_off, tab_w:'
                                 f'self.parse_{prule}(b, st, en, off, col, idt, pf, ch, tab_off, tab_w)')
                    if dedent:
                        steps.append(f'_dedent = lambda b, st, en, off, col, idt, pf, ch, tab_off, tab_w:'
                                 f'self.parse_{dedent}(b, st, en, off, col, idt, pf, ch, tab_off, tab_w)')
                    else:
                        steps.append(f'_dedent = None')
                    steps.append(f'{prefix}.append((_indent, _dedent))')
                else:
                    prule = rule.args['indent']
                    dedent = f"self.parse_{dedent}" if dedent else repr(None)
                    steps.append(f'{prefix}.append((self.parse_{prule}, {dedent}))')


            steps.append(f'{indent_column}.append({column})')

            steps.append('while True:')
            build_subrules(rule.rules, steps.add_indent(), offset, column, indent_column, partial_tab_offset, partial_tab_width, prefix, children, count, values)
            steps.append('    break')

            steps.append(f'{prefix}.pop()')
            steps.append(f'if len({indent_column}) > 1: {indent_column}.pop()')
            steps.append(f'if {offset} == -1: break')

        elif rule.kind == START_OF_LINE:
            steps.extend((
                f"if not ({column} == 0 and len({indent_column}) == 1):",
                f"    {offset} = -1",
                f"    break",
            ))
        elif rule.kind == INDENT:
            # if partial
            # break to dedent
            offset_0 = offset.incr()
            partial = rule.args['partial']
            steps.extend((
                f"if {column} != 0:",
                f"    {offset} = -1",
                f"    break",
                f"# print('start')",
                f"for indent, dedent in {prefix}:",
                f"    # print(indent, dedent)",
                f"    _children, _prefix = [], []",
                f"    {offset_0} = {offset}",
                f"    {offset_0}, {column}, {partial_tab_offset}, {partial_tab_width} = indent(buf, buf_start, buf_eof, {offset_0}, {column}, {indent_column}, _prefix, _children, {partial_tab_offset}, {partial_tab_width})",
                f"    if _prefix or _children:",
                f"       raise Exception('bar')",
            ))

            if partial: steps.extend((
                f"    if {offset_0} == -1:",
                f"        if dedent is None:",
                f"            {offset} = -1",
                f"            break",
                f"        _children, _prefix = [], []",
                f"        {offset_0} = {offset}",
                f"        {offset_0}, _column, _partial_tab_offset, _partial_tab_width = dedent(buf, buf_start, buf_eof, {offset_0}, {column}, list({indent_column}), _prefix, _children, {partial_tab_offset}, {partial_tab_width})",
                f"        if {offset_0} != -1:",
                f"            {offset} = -1",
                f"            break",
                f"        else:",
                f"            {offset_0} = {offset}",
                ))
            else:steps.extend((
                f"    if {offset_0} == -1:",
                f"        {offset} = -1",
                f"        break",
                ))

            steps.extend((
                f"    {offset} = {offset_0}",
                f"    {indent_column}.append({column})",
                f"if {offset} == -1:",
                f"    break",
            ))
        elif rule.kind == DEDENT:
            raise Exception('broken')
            # if partial
            # break to dedent
            # for each pair
            # if indent matches or dedent doesnt, continue
            # if not -1, fail
            offset_0 = offset.incr()
            offset_1 = offset_0.incr()
            offset_2 = offset_2.incr()
            column_1 = column.incr()
            indent_column_1 = indent_column.incr()
            partial_tab_offset_1 = partial_tab_offset.incr()
            partial_tab_width_1 = partial_tab_width.incr()
            steps.extend((
                f"if not ({column} == 0 and len({indent_column}) == 1):",
                f"    {offset} = -1",
                f"    break",
                f"{offset_0} = {offset}",
                f"{column_1} = {column}",
                f"{indent_column_1} = list({indent_column})",
                f"{partial_tab_offset_1} = {partial_tab_offset}",
                f"{partial_tab_width_1} = {partial_tab_width}",
                f"", # offet = start, offset_0 = current pos, offset_1 = next pos
                f"for indent, dedent in {prefix}:",
                f"    # print(indent)",
                f"    _children, _prefix = [], []",
                f"    {offset_1} = {offset_0}",
                f"    {offset_1}, {column_1}, {indent_column_1}, {partial_tab_offset_1}, {partial_tab_width_1} = indent(buf, buf_start, buf_eof, {offset_1}, {column_1}, {indent_column_1}, _prefix, _children, {partial_tab_offset_1}, {partial_tab_width_1})",
                f"    if _prefix or _children:",
                f"       raise Exception('bar')",
                f"    if {offset_1} == -1:",
                f"        if dedent is None:",
                f"            {offset_0} = -1",
                f"            break",
                f"        _children, _prefix = [], []",
                f"        {offset_1} = {offset_0}",
                f"        {offset_1}, _column, _indent_column, _partial_tab_offset, _partial_tab_width = dedent(buf, buf_start, buf_eof, {offset_1}, {column_1}, {indent_column_1}, _prefix, _children, {partial_tab_offset_1}, {partial_tab_width_1})",
                f"        if {offset_1} != -1:",
                f"            {offset_0} = -1", 
                f"            break",
                f"        else:",
                f"            {offset_1} = {offset_0}",
                f"    {offset_0} = {offset_1}",
                f"    {indent_column}.append({column})",
                f"if {offset_0} != -1:",
                f"    {offset} = 0; break",
            ))

        elif rule.kind == RULE:
            steps.extend((
                f"{offset}, {column}, {partial_tab_offset}, {partial_tab_width} = self.parse_{rule.args['name']}(buf, buf_start, buf_eof, {offset}, {column}, {indent_column}, {prefix}, {children}, {partial_tab_offset}, {partial_tab_width})",
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
                f"codepoint = {_ord}(buf[{offset}])",
                f"",
            ))

            literals = rule.args['range']

            idx = 0
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
                            f"{_if} {start}codepoint <= {end}:",
                            f"    {offset} = -1",
                            f"    break",
                        ))
                    else:
                        steps.extend((
                            f"{_if} {start}codepoint <= {end}:",
                            f"    {offset} += 1",
                            f"    {column} += 1",
                        ))

                elif len(literal) == 1:
                    literal = repr(ord(literal))
                    if invert:
                        steps.extend((
                            f"{_if} codepoint == {literal}:",
                            f"    {offset} = -1",
                            f"    break",
                        ))
                    else:
                        steps.extend((
                            f"{_if} codepoint == {literal}:",
                            f"    {offset} += 1",
                            f"    {column} += 1",
                        ))
                else:
                    raise BadGrammar('bad range', repr(literal))

            _chr = "" if cython else "chr"
            for name, active in rule.args['named_ranges'].items():
                if not active: continue
                _if = {0:"if"}.get(idx, "elif")
                idx +=1 
                if name == "unicode_punctuation":
                    steps.extend((
                        f"{_if} unicodedata.category({_chr}(codepoint)).startswith('P'):",
                    ))
                    if invert: steps.extend ((
                        f"    {offset} = -1",
                        f"    break",
                    ))
                    else: steps.extend((
                        f"    {offset} += 1",
                        f"    {column} += 1",
                    ))
                elif name == "unicode_whitespace":
                    steps.extend((
                        f"{_if} unicodedata.category({_chr}(codepoint)) == 'Zs':",
                    ))
                    if invert: steps.extend ((
                        f"    {offset} = -1",
                        f"    break",
                    ))
                    else: steps.extend((
                        f"    {offset} += 1",
                        f"    {column} += 1",
                    ))
                elif name == "unicode_newline": # crlf ugh
                    steps.extend((
                        f"{_if} unicodedata.category({_chr}(codepoint)) in ('Zl', 'Zp', 'Cc'):",
                    ))
                    if invert: steps.extend ((
                        f"    {offset} = -1",
                        f"    break",
                    ))
                    else: steps.extend((
                        f"    {offset} += 1",
                        f"    {column} += 1",
                    ))
                else:
                    raise Exception(name)

            # if idx == 0: raise Exception("empty range", rule.args)
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
                    if rule.args['transform'] is not None:
                        if rule.args['transform'] == "lower":
                            cond = f"buf[{offset}:{offset}+{length}].lower() == {(vliteral)}"
                        else:
                            raise Exception('bad')

                    elif cython:
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

            cond2 =f"codepoint in {repr(''.join(grammar.whitespace))}"
            cond3 =f"codepoint in {repr(''.join(grammar_newline))}"

            steps.extend((
                        f"{count} = 0",
                        f"while {' and '.join(cond)}:",
                        f"    codepoint = buf[{offset}]",
            ))

            if _newline:
                if newline_rn:
                    steps.extend((
                        f"    if codepoint == '\\r' and {offset} + 1 < buf_eof and buf[{offset}+1] == '\\n':", 
                        f"        {offset} +=2",
                        f"        {column} = 0",
                        f"        {indent_column}[:] = (0, )",
                        f"    elif {cond3}:", # in newline
                    ))
                else:
                    steps.extend((
                        f"    if {cond3}:", # in newlne
                    ))
                steps.extend((
                        f"        {offset} +=1",
                        f"        {column} = 0",
                        f"        {indent_column}[:] = (0, )",
                        f"        {count} +=1",
                        f"    elif {cond2}:",
                ))
            else:
                steps.extend((
                        f"    if {cond2}:",
                ))

            steps.extend((
                        f"        if codepoint == '\\t':",
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
            cond =f"codepoint in {repr(''.join(grammar_newline))}"
            steps.extend((
                f"if {offset} < buf_eof:",
                f"    codepoint = buf[{offset}]",
            ))
            if newline_rn:
                steps.extend((
                    f"    if codepoint == '\\r' and {offset} + 1 < buf_eof and buf[{offset}+1] == '\\n':", 
                    f"        {offset} +=2",
                    f"        {column} = 0",
                    f"        {indent_column}[:] = (0, )",
                    f"    elif {cond}:",
                ))
            else:
                steps.extend((
                    f"    if {cond}:",
            ))
            steps.extend((
                    f"        {offset} +=1",
                    f"        {column} = 0",
                    f"        {indent_column}[:] = (0, )",
                    f"    else:",
                    f"        {offset} = -1",
                    f"        break",
                    f"else:",
                    f"    {offset} = -1",
                    f"    break",
            ))

        elif rule.kind == END_OF_LINE:
            cond =f"codepoint in {repr(''.join(grammar_newline))}"

            steps.extend((
                f"if {offset} < buf_eof:",
                f"    codepoint = buf[{offset}]",
            ))
            if newline_rn:
                steps.extend((
                    f"    if codepoint == '\\r' and {offset} + 1 < buf_eof and buf[{offset}+1] == '\\n':", 
                    f"        {offset} +=2",
                    f"        {column} = 0",
                    f"        {indent_column}[:] = (0, )",
                    f"    elif {cond}:",
                ))
            else:
                steps.extend((
                    f"    if {cond}:",
            ))
            steps.extend((
                    f"        {offset} +=1",
                    f"        {column} = 0",
                    f"        {indent_column}[:] = (0, ) ",
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
            args = [str(values.get(a, repr(a))) for a in rule.args['args']]
            steps.append(f"print('print', {', '.join(args)}, 'at' ,{offset},'col', {column}, repr(buf[{offset}:min({offset}+16, buf_eof)]), buf_eof, {prefix})")
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

    def _build_regex(rule):
        if rule.kind == LITERAL:
            return f'(?:{"|".join(re.escape(l) for l in rule.args["literals"])})'
        if rule.kind == RANGE:
            out = []
            def _f(x):
                if 32 < ord(x)< 127 :return re.escape(x)
                return repr(x)[1:-1]
            for r in rule.args['range']:
                if len(r) == 1:
                    out.append(_f(r))
                else:
                    out.append(f"{_f(r[0])}-{_f(r[2])}")
            if rule.args['invert']:
                return f"[^{''.join(out)}]"
            return f"[{''.join(out)}]"
        if rule.kind == SEQUENCE:
            return "".join(_build_regex(r) for r in rule.rules)
        if rule.kind == CHOICE:
            return f'(?:(?:{")|(?:".join(_build_regex(r) for r in rule.rules)}))'
        if rule.kind == REPEAT:
            _min, _max = rule.args['min'], rule.args['max']
            if not _min  and _max == 1:
                num = "?"
            elif not _min and not _max:
                num = "*"
            elif _min ==1 and _max == None:
                num = "+"
            elif _min == _max:
                num = "{" + str(_max) + "}"
            else:
                num = "{" +f"{_min or ''}"+","+f"{_max or ''}"+ "}"
            return f'(?:{"".join(_build_regex(r) for r in rule.rules)}){num}'
    def _visit(node):
        if node.kind ==REGULAR:
            regex = _build_regex(node.args['rule'])
            if regex not in regexes:
                name = node.args.get('name')
                if not name:
                    name = VarBuilder('regex', n=len(regexes))
                else:
                    name = f"regex_{name}"
                regexes[regex] = name
            else:
                name = regexes[regex]
            node.args['regex'] = regex
            node.args['name'] = name
    for rule in grammar.rules.values():
        rule.visit_tail(_visit)
            

    output = ParserBuilder([], 0, {})
    grammar_newline = tuple(n for n in grammar.newline if n!='\r\n') if grammar.newline else ()
    newline = repr(tuple(grammar.newline)) if grammar.newline else '()'
    newline_rn = bool(grammar.newline) and '\r\n' in grammar.newline
    whitespace = repr(tuple(grammar.whitespace)) if grammar.whitespace else '()'
    whitespace_tab = bool(grammar.whitespace) and '\t' in grammar.whitespace

    if wrap:
        output.append("def _build():")
        output = output.add_indent()
    if cython:
        output.append('#cython: language_level=3, bounds_check=False')

    old_output = output

    output.extend((
        f"import unicodedata, re",
        f"",
        f"class Node:",
        f"    def __init__(self, name, start, end, start_column, end_column, children, value):",
        f"        self.name = name",
        f"        self.start = start",
        f"        self.end = end",
        f"        self.start_column = start_column",
        f"        self.end_column = end_column",
        f"        self.children = children if children is not None else ()",
        f"        self.value = value",
        f"    def __str__(self):",
        "        return '{}[{}:{}]'.format(self.name, self.start, self.end)",
        f'    def build(self, buf, builder):',
        f'        children = [child.build(buf, builder) for child in self.children]',
        f'        if callable(builder): return builder(buf, self, children)',
        f'        if self.name == "value": return self.value',
        f'        return builder[self.name](buf, self, children)',
        f'',
    ))

    if use_regexes:
        for regex, value in regexes.items():
            output.append(f"{value} = re.compile(r'''{(regex)}''')")
        if regexes:
            output.append("")
    if cython:
        output.extend((
            f"cdef class Parser:",
            f"    cdef dict cache",
            f"    cdef int tabstop",
            f"    cdef int allow_mixed_indent ",
            f"",
            f"    def __init__(self, tabstop=None, allow_mixed_indent=True):",
            f"         self.tabstop = tabstop or {grammar.tabstop}",
            f"         self.cache = None",
            f"         self.allow_mixed_indent = allow_mixed_indent",
            "",
        ))
        output = output.add_indent(4)

    else:
        output.extend((
            f"class Parser:",
            f"    def __init__(self, tabstop=None, allow_mixed_indent=False):",
            f"         self.tabstop = tabstop or {grammar.tabstop}",
            f"         self.cache = None",
            f"         self.allow_mixed_indent = allow_mixed_indent",
            "",
        ))

        output = output.add_indent(4)

    start_rule = grammar.start
    output.extend((
        f"def parse(self, buf, offset=0, end=None, err=None, builder=None):",
        f"    self.cache = dict()",
        f"    end = len(buf) if end is None else end",
        f"    start, eof = offset, end",
        f"    column, indent_column = 0, [0]",
        f"    prefix, children = [], []",
        f"    new_offset, column, partial_tab_offset, partial_tab_width = self.parse_{start_rule}(buf, start, end, offset, column, indent_column, prefix, children, 0, 0)",
        f"    if children and new_offset == end:",
        f"         if builder is None: return {node}({repr(grammar.capture)}, offset, new_offset, 0, column, children, None)",
        f"         return children[-1].build(buf, builder)",
        f"#     print('no', offset, new_offset, end)",
        f"    if err is not None: raise err(buf, new_offset, 'no')",
        f"",
    ))

    varnames = {
            "offset":"cdef int", "column":"cdef int", 
            "prefix":"cdef list", "children":"cdef list", "count":"cdef int", "indent_column":"cdef list",
            "partial_tab_offset":"cdef int", "partial_tab_width": "cdef int"}
    for name, rule in grammar.rules.items():
        cdefs = {}
        if cython:
            output.append(f"cdef (int, int, int, int) parse_{name}(self, str buf, int buf_start, int buf_eof, int offset_0,  int column_0, list indent_column_0,  list prefix_0, list children_0, int partial_tab_offset_0, int partial_tab_width_0):")
            output.append(f"    cdef Py_UCS4 codepoint")
            
            for v in varnames:
                cdefs[v] = output.add_indent(4).append_placeholder()
        else:
            output.append(f"def parse_{name}(self, buf, buf_start, buf_eof, offset_0, column_0, indent_column_0, prefix_0, children_0, partial_tab_offset_0, partial_tab_width_0):")
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
        output.append(f"    return offset_0, column_0, partial_tab_offset_0, partial_tab_width_0")
        output.append("")
    if wrap:
        old_output.append("return Parser")
    #for lineno, line in enumerate(output.output):
    #  print(lineno, '\t', line)
    return output.as_string()






def parser(grammar):
    output = compile_python(grammar, wrap=True)
    glob, loc = {}, {}
    exec(output, glob, loc)
    return loc['_build']()()

class Grammar(metaclass=Metaclass):
    pass

Grammar.parser = classmethod(parser)
