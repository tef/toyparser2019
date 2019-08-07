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
        args['key'] =  self.key
        args['args'] = self.args
        return ParserRule(CAPTURE, args=args, rules=[r.make_rule() for r in self.rules])

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
            def callback(*, rule=rule):
                    self.rule(rule)
            def _repeat(min=0, max=None, *, rule=rule):
                    self.rule(RepeatNode([rule], min=min, max=max))
            callback.repeat = _repeat
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
    def indented(self, prefix=None):
        if self.block_mode: raise SyntaxError()
        rules, self.rules = self.rules, []
        yield
        rules.append(GrammarNode(SET_INDENT, args=dict(prefix=prefix), rules=self.rules))
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
        rules.append(CaptureNode(name, {}, self.rules))
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
                return CaptureNode(capture, {}, rules)
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
        return CaptureNode(name, {}, args)
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
        return f"{self.name}_{self.n}" # if self.n else self.name

    def incr(self):
        return VarBuilder(self.name, self.n+1)


def compile_python(grammar, builder=None, cython=False):

    def build_subrules(rules, steps, offset, line_start, prefix, children, count, values):
        for subrule in rules:
            build_steps(subrule, steps, offset, line_start, prefix, children, count, values)

    def build_steps(rule, steps, offset, line_start, prefix, children, count, values):
        # steps.append(f"print('start', {repr(str(rule))})")
        if rule.kind == SEQUENCE:
            build_subrules(rule.rules, steps, offset, line_start, prefix, children, count, values)

        elif rule.kind == CAPTURE:
            name = repr(rule.args['name'])
            children_0 = children.incr()
            offset_0 = offset.incr()
            steps.append(f"{offset_0} = {offset}")
            steps.append(f"{children_0} = []")
            steps.append(f"while True: # start capture")
            build_subrules(rule.rules, steps.add_indent(), offset_0, line_start, prefix, children_0, count, values)
            steps.append(f"    break")
            steps.append(f"if {offset_0} == -1:")
            steps.append(f"    {offset} = -1")
            steps.append(f"    break")
            if cython:
                node = "Node"
            else:
                node = "self.Node"

            value = VarBuilder('value', len(values))
            values[rule.args['key']] = value

            steps.extend((
                # f"print(len(buf), {offset}, {offset_0}, {children})",
                f"if self.builder is not None:",
                f"    {value} = self.builder[{name}](buf, {offset}, {offset_0}, {children_0})",
                f"else:",
                f"    {value} = {node}({name}, {offset}, {offset_0}, list({children_0}), None)",
                f"{children}.append({value})",
            ))
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
                build_steps(subrule, steps_0.add_indent(), offset_0, line_start_0, prefix, children_0, count, values)
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

            _minv = values.get(_min)
            _maxv = values.get(_max)

            cond = "True"
            if _maxv:
                cond = f"{count} < {_maxv}"
            elif _max is not None and _max > 0:
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


            steps_0.append("while True:")
            for subrule in rule.rules:
                    build_steps(subrule, steps_0.add_indent(), offset_0, line_start_0, prefix, children, new_count, values)
            steps_0.append("    break")
            steps_0.append(f"if {offset_0} == -1:")
            steps_0.append(f"    break")

            steps_0.append(f"if {offset} == {offset_0}: break")
            steps_0.append(f"{offset} = {offset_0}")
            steps_0.append(f"{line_start} = {line_start_0}")
            steps_0.append(f"{count} += 1")
            if _max == 1:
                steps_0.append(f"break")

            if _minv or (_min is not None and _min > 0):
                _minv = _minv or repr(_min)
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
            line_start_0 = line_start.incr()
            steps.append(f"while True: # start reject")
            steps_0.append(f"{children_0} = []")
            steps_0.append(f"{offset_0}, {line_start_0} = {offset}, {line_start}")
            build_subrules(rule.rules, steps_0, offset_0, line_start_0, prefix, children_0, count, values)
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
            build_subrules(rule.rules, steps_0, offset_0, line_start_0, prefix, children_0, count, values)
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
            steps.append(f"{offset_0} = {offset}")
            steps.append(f"while True: # start count")
            build_subrules(rule.rules, steps.add_indent(), offset_0, line_start, prefix, children, count, values)
            steps.append("    break")
            steps.append(f"if {offset_0} == -1:")
            steps.append(f"    {offset} = -1; break")
            # find var name
            value = VarBuilder('value', len(values))
            values[rule.args['key']] = value
            steps.append(f"{value} = buf[{offset}:{offset_0}].count({repr(rule.args['char'])})")
            steps.append(f"{offset} = {offset_0}")


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

        elif rule.kind == SET_INDENT:
            cond = f"chr in self.WHITESPACE"
            if cython: cond = " or ".join(f"chr == {repr(ord(chr))}" for chr in grammar.whitespace)


            if rule.args['prefix'] is None:
                steps.extend((
                    f"{count} = {offset} - {line_start}+  ((self.tabstop -1) * buf[{line_start}:{offset}].count('\t'))",
                    f"def _indent(buf, offset, line_start, prefix, buf_eof, children, count={count}):",
                    f"    while count > 0 and offset < buf_eof:",
                    f"        chr = ord(buf[offset])",
                    f"        if {cond}:",
                    f"            offset +=1",
                    f"            count -= self.tabstop if chr == 9 else 1",
                    f"        else:",
                    f"            offset = -1",
                    f"            break",
                    f"    return offset, line_start",
                    f'{prefix}.append(_indent)',
                ))
            else:
                prule = rule.args['prefix']
                steps.append(f'{prefix}.append(self.parse_{prule})')

            steps.append('while True:')
            build_subrules(rule.rules, steps.add_indent(), offset, line_start, prefix, children, count, values)
            steps.append('    break')

            steps.append(f'{prefix}.pop()')
            steps.append(f'if {offset} == -1: break')

        elif rule.kind == MATCH_INDENT or rule.kind == START_OF_LINE:
            cond = f"chr in self.WHITESPACE"
            if cython: cond = " or ".join(f"chr == {repr(ord(chr))}" for chr in grammar.whitespace)

            offset_0 = offset.incr()

            steps.extend((
                f"if {offset} != {line_start}:",
                f"    {offset} = -1",
                f"    break",
                f"for indent in {prefix}:",
                f"    _children, _prefix = [], []",
                f"    {offset}, {line_start} = indent(buf, {offset}, {line_start}, _prefix, buf_eof, _children)",
                f"    if {offset} == -1 or _prefix or _children:",
                f"        break",
                f"    {line_start} = {offset}",
                f"if {offset} == -1:",
                f"    break",
            ))

        elif rule.kind == RULE:
            steps.extend((
                f"{offset}, {line_start} = self.parse_{rule.args['name']}(buf, {offset}, {line_start}, {prefix}, buf_eof, {children})",
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
                f"chr = ord(buf[{offset}])",
                f"",
            ))

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

            # steps.append(f"_buf = buf[{offset}:]")

            for idx, literal in enumerate(rule.args['literals']):
                _if = {0:"if"}.get(idx, "elif")

                length = len(literal)

                cond = f"buf[{offset}:{offset}+{length}] == {repr(literal)}"

                # cond = [f"{offset} + {length} <= buf_eof"]
                # for i, c in enumerate(literal):
                #     cond.append(f"buf[{offset}+{i}] == {repr(c)}")
                # cond = " and ".join(cond)

                # cond = f"_buf.startswith({repr(literal)})"

                steps.extend((
                    f"{_if} {cond}:",
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

            _minv = values.get(_min)
            _maxv = values.get(_max)

            _newline = rule.args['newline']

            cond = [f"{offset} < buf_eof"]
            if _maxv:
                cond.append(f"{count} < {repr(_maxv)}")
            elif _max is not None:
                cond.append(f"{count} < {repr(_max)}")

            cond2 =f"chr in self.WHITESPACE"
            if cython: cond2 = " or ".join(f"chr == {repr(ord(chr))}" for chr in grammar.whitespace)

            if _newline:
                cond3 =f"chr in self.NEWLINE"
                if cython: cond3 = " or ".join(f"chr == {repr(ord(chr))}" for chr in grammar.newline)
                steps.extend((
                    f"{count} = 0",
                    f"while {' and '.join(cond)}:",
                    f"    chr = ord(buf[{offset}])",
                    f"    if {cond3}:",
                    f"        {offset} +=1",
                    f"        {line_start} = {offset}",
                    f"        {count} +=1",
                    f"    elif {cond2}:",
                    f"        {offset} +=1",
                    f"        {count} +=1",
                    f"    else:",
                    # f"        print(repr(buf[{offset}:{offset}+5]))",
                    f"        break",

                ))

            else:
                steps.extend((
                    f"{count} = 0",
                    f"while {' and '.join(cond)}:",
                    f"    chr = ord(buf[{offset}])",
                    f"    if {cond2}:",
                    f"        {offset} +=1",
                    f"        {count} +=1",
                    f"    else:",
                    f"        break",
                ))
            if _minv:
                steps.extend((
                    f"if {count} < {_minv}:",
                    f"    {offset} = -1",
                    f"    break",
                ))
            elif _min is not None and _min > 0:
                steps.extend((
                    f"if {count} < {repr(_min)}:",
                    f"    {offset} = -1",
                    f"    break",
                ))

        elif rule.kind == NEWLINE:
            cond =f"chr in self.NEWLINE"

            if cython: cond = " or ".join(f"chr == {repr(ord(chr))}" for chr in grammar.newline)
            steps.extend((
                f"if {offset} < buf_eof:",
                f"    chr = ord(buf[{offset}])",
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
        elif rule.kind == END_OF_LINE:
            cond =f"chr in self.NEWLINE"
            if cython: cond = " or ".join(f"chr == {repr(ord(chr))}" for chr in grammar.newline)

            steps.extend((
                f"if {offset} < buf_eof:",
                f"    chr = ord(buf[{offset}])",
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
    newline = repr(tuple(ord(n) for n in grammar.newline)) if grammar.newline else '()'
    whitespace = repr(tuple(ord(w) for w in grammar.whitespace)) if grammar.whitespace else '()'



    parse_node = (
        f"class Node:",
        f"    def __init__(self, name, start, end, children, value):",
        f"        self.name = name",
        f"        self.start = start",
        f"        self.end = end",
        f"        self.children = children",
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
            f"    cpdef object builder, tabstop",
            f"",
            f"    def __init__(self, builder=None):",
            f"         self.builder = builder",
            f"         self.tabstop = self.TABSTOP",
            f"",
            f"    NEWLINE = {newline}",
            f"    WHITESPACE = {whitespace}",
            f"    TABSTOP = {grammar.tabstop}",
            "",
        ))
        output = output.add_indent(4)

    else:
        output.extend((
            f"class Parser:",
            f"    def __init__(self, builder=None):",
            f"         self.builder = builder",
            f"         self.tabstop = self.TABSTOP",
            "",
            f"    NEWLINE = {newline}",
            f"    WHITESPACE = {whitespace}",
            f"    TABSTOP = {grammar.tabstop}",
            "",
        ))

        output = output.add_indent(4)
        output.extend(parse_node)

    start_rule = grammar.start
    output.extend((
        f"def parse(self, buf, offset=0, end=None, err=None):",
        f"    end = len(buf) if end is None else end",
        f"    line_start, prefix, eof, children = offset, [], end, []",
        f"    new_offset, line_start = self.parse_{start_rule}(buf, offset, line_start, prefix, eof, children)",
        f"    if children and new_offset == end: return children[-1]",
        f"    print('no', offset, new_offset, end, buf[new_offset:])",
        f"    if err is not None: raise err(buf, new_offset, 'no')",
        f"",
    ))

    for name, rule in grammar.rules.items():
        if cython:
            output.append(f"cdef (int, int) parse_{name}(self, str buf, int offset_0, int line_start_0, list prefix_0, int buf_eof, list children_0):")
            output.append(f"    cdef int count_0")
            output.append(f"    cpdef Py_UCS4 chr")
        else:
            output.append(f"def parse_{name}(self, buf, offset_0, line_start_0, prefix_0, buf_eof, children_0):")
   #     output.append(f"    print('enter {name},',offset_0,line_start_0,prefix_0, repr(buf[offset_0:offset_0+10]))")
        output.append(f"    while True: # note: return at end of loop")

        values = {}
        build_steps(rule,
                output.add_indent(8),
                VarBuilder("offset"),
                VarBuilder('line_start'),
                VarBuilder('prefix'),
                VarBuilder('children'),
                VarBuilder("count"), values)
        output.append(f"        break")
    #     output.append(f"    print(('exit' if offset_0 != -1 else 'fail'), '{name}', offset_0, line_start_0, repr(buf[offset_0: offset_0+10]))")
        output.append(f"    return offset_0, line_start_0")
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
