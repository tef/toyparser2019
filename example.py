from textexpressions import *

class JSON(Grammar, start="document"):
    document = json_list 
    document = json_object

    json_value = rule( 
        json_list | json_object |
        json_string | json_number |
        json_true | json_false | 
        json_null
    )
    
    json_true = accept("true")
    json_false = accept("false")
    json_null = accept("null")

    @rule()
    def json_number(self):
        with self.optional():
            self.accept("-")
        with self.choice():
            with self.case():
                self.accept("0")
            with self.case():
                self.range("1-9")
                with self.repeat():
                    self.range("0-9")
        with self.optional():
            self.accept(".")
            with self.repeat():
                self.range("0-9")
        with self.optional():
            self.accept("e", "E")
            with self.optional():
                self.accept("+", "-")
                with self.repeat():
                    self.range("0-9")

    @rule()
    def json_string(self):
        self.accept("\"")
        with self.repeat(), self.choice():
            with self.case():
                self.accept("\\u")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
                self.range("0-9", "a-f", "A-F")
            with self.case():
                self.accept("\\")
                self.range(
                    "\"", "\\", "/", "b", 
                    "f", "n", "r", "t",
                )
            with self.case():
                self.range("\\", "\"", invert=True)
        self.accept("\"")

    @rule()
    def json_list(self):
        self.accept("[")
        with self.repeat(max=1):
            self.json_value()
            with self.repeat(min=0):
                self.accept(",")
                self.json_value()
        self.accept("]")

    @rule()
    def json_object(self):
        self.accept("{")
        with self.optional():
            self.json_string()
            self.accept(":")
            self.json_value()
            with self.repeat(min=0):
                self.accept(",")
                self.json_string()
                self.accept(":")
                self.json_value()
        self.accept("}")

for name, value in JSON.rules.items():
    print(name, '<--', value,'.')
    print()


def parse_rule(rule, buf, offset):
    if isinstance(rule, NamedRule):
        end = parse_rule(JSON.rules[rule.name], buf, offset)
        if end:
            print(rule.name, buf[offset:end])
        return end

    if isinstance(rule, ChoiceRule):
        for option in rule.rules:
            o = parse_rule(option, buf, offset)
            if o is not None:
                return o
    if isinstance(rule, RepeatRule):
        start, end = rule.min, rule.max
        c= 0
        while c < start:
            for step in rule.rules:
                offset = parse_rule(step, buf, offset)
                if offset is None:
                    return None
            c+=1
        while end is None or c < end:
            for step in rule.rules:
                new_offset = parse_rule(step, buf, offset)
                if new_offset is None:
                    return offset
                offset = new_offset
            c+=1
        return offset

    if isinstance(rule, SequenceRule):
        for step in rule.rules:
            offset = parse_rule(step, buf, offset)
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




    


rule = JSON.rules[JSON.start]
print(parse_rule(rule, "[1,2,3]", 0))


# build a recogniser, give it captures
# get back tree of (start, end, children) nodes, well something which exposes start,end and children 
