import base64, codecs
from datetime import datetime, timedelta, timezone

from ..grammar import Grammar, compile_python, sibling

def unescape(string):
    return codecs.decode(string.replace('\\/', '/'), 'unicode_escape')

def parse_datetime(v):
    if v[-1] == 'Z':
        if '.' in v:
            return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        else:
            return datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    else:
        raise NotImplementedError()

bools = {'false': False, 'true':True}
builder = {
    'number': (lambda buf, node, children: eval(buf[node.start:node.end])),
    'string': (lambda buf, node, children: unescape(buf[node.start:node.end])),
    'list': (lambda buf, node, children: children),
    'object': (lambda buf, node, children: dict(children)),
    'pair': (lambda buf, node, children: children),
    'document': (lambda buf, node, children: children[0]),
    'bool': (lambda buf, node, children: bools[buf[node.start:node.end]]),
    'null': (lambda buf, node, children: None),
    'identifier': (lambda buf, node, children: buf[node.start:node.end]),
}

def untag(buf, node, children):
    identifier, literal = children
    if identifier == "object":
       return literal
    if identifier == "record" or identifier == "dict":
        if not isinstance(literal, dict): raise Exception('bad')
        return literal
    elif identifier == "list":
        if not isinstance(literal, list): raise Exception('bad')
        return literal
    elif identifier == "string":
        if not isinstance(literal, str): raise Exception('bad')
        return literal
    elif identifier == "bool":
        if not isinstance(literal, bool): raise Exception('bad')
        return literal
    elif identifier == "int":
        if not isinstance(literal, int): raise Exception('bad')
        return literal
    elif identifier == "float":
        if isinstance(literal, float): return literal
        if not isinstance(literal, str): raise Exception('bad')
        return float.fromhex(literal)
    elif identifier == "set":
        if not isinstance(literal, list): raise Exception('bad')
        return set(literal)
    elif identifier == "complex":
        if not isinstance(literal, list): raise Exception('bad')
        return complex(*literal)
    elif identifier == "bytestring":
        if not isinstance(literal, str): raise Exception('bad')
        return literal.encode('ascii')
    elif identifier == "base64":
        if not isinstance(literal, str): raise Exception('bad')
        return base64.standard_b64decode(literal)
    elif identifier == "datetime":
        if not isinstance(literal, str): raise Exception('bad')
        return parse_datetime(literal)
    elif identifier == "duration":
        if not isinstance(literal, (int, float)): raise Exception('bad')
        return timedelta(seconds=literal)
    elif identifier == "unknown":
        raise Exception('bad')
    return {identifier: literal}

builder['tagged'] = untag

class RSON(Grammar, start="document", whitespace=[" ", "\t", "\r", "\n", "\uFEFF"]):
    @rule()
    def document(self):
        self.comment.inline()
        self.rson_value()
        self.comment.inline()

    @rule()
    def comment(self):
        self.whitespace()
        with self.repeat(min=0):
            self.literal("#")
            with self.repeat(min=0):
                self.range("\n", invert=True)
            self.whitespace()
        self.whitespace()

    @rule()
    def rson_value(self):
        with self.choice():
            with self.case(), self.capture_node('tagged'):
                self.literal('@')
                with self.capture_node('identifier', nested=False):
                    self.range("a-z", "A-Z")
                    with self.repeat():
                        self.range("0-9", "a-z","A-Z","_")
                self.literal(' ')
                self.rson_literal()
            with self.case():
                self.rson_literal()
    @rule()
    def rson_literal(self):
        with self.choice():
            with self.case(): self.rson_list.inline()
            with self.case(): self.rson_object.inline()
            with self.case(): self.rson_string.inline()
            with self.case(): self.rson_number.inline()
            with self.case(): self.rson_true.inline()
            with self.case(): self.rson_false.inline()
            with self.case(): self.rson_null.inline()

    rson_true = rule(literal("true"), capture="bool")
    rson_false = rule(literal("false"), capture="bool")
    rson_null = rule(literal("null"), capture="null")

    @rule()
    def rson_number(self):
        with self.capture_node("number", nested=False), self.choice():
            with self.case():
                with self.optional():
                    self.range("-", "+")
                self.literal("0x")
                self.range("0-9", "A-F", "a-f")
                with self.repeat():
                    self.range("0-9","A-F","a-f","_")
            with self.case():
                with self.optional():
                    self.range("-", "+")
                self.literal("0o")
                self.range("0-8",)
                with self.repeat():
                    self.range("0-8","_")
            with self.case():
                with self.optional():
                    self.range("-", "+")
                self.literal("0b")
                self.range("0-1",)
                with self.repeat():
                    self.range("0-1","_")
            with self.case():
                with self.optional():
                    self.range("-", "+")
                with self.choice():
                    with self.case():
                        self.literal("0")
                    with self.case():
                        self.range("1-9")
                        with self.repeat():
                            self.range("0-9")
                with self.optional():
                    self.literal(".")
                    with self.repeat():
                        self.range("0-9")
                with self.optional():
                    self.literal("e", "E")
                    with self.optional():
                        self.literal("+", "-")
                        with self.repeat():
                            self.range("0-9")

    @rule()
    def rson_string(self):
        with self.choice():
            with self.case():
                self.literal("\"")
                with self.capture_node("string", nested=False), self.repeat(), self.choice():
                    with self.case():
                        self.range("\x00-\x1f", "\\", "\"", "\uD800-\uDFFF", invert=True)
                    with self.case():
                        self.literal("\\x")
                        with self.reject():
                            self.range('0-1')
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                    with self.case():
                        self.literal("\\u")
                        with self.reject():
                            self.literal("000")
                            self.range('0-1')
                        with self.reject():
                            self.literal("D", "d")
                            self.range("8-9", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                    with self.case():
                        self.literal("\\U")
                        with self.reject():
                            self.literal("0000000")
                            self.range('0-1')
                        with self.reject():
                            self.literal("0000")
                            self.literal("D", "d")
                            self.range("8-9", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                    with self.case():
                        self.literal("\\")
                        self.range(
                            "\"", "\\", "/", "b", 
                            "f", "n", "r", "t", "'", "\n",
                        )
                self.literal("\"")
            with self.case():
                self.literal("\'")
                with self.capture_node("string", nested=False), self.repeat(), self.choice():
                    with self.case():
                        self.range("\x00-\x1f", "\\", "\'", "\uD800-\uDFFF", invert=True)
                    with self.case():
                        self.literal("\\x")
                        with self.reject():
                            self.range('0-1')
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                    with self.case():
                        self.literal("\\u")
                        with self.reject():
                            self.literal("00")
                            self.range('0-1')
                        with self.reject():
                            self.literal("D", "d")
                            self.range("8-9", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                    with self.case():
                        self.literal("\\U")
                        with self.reject():
                            self.literal("000000")
                            self.range('0-1')
                        with self.reject():
                            self.literal("0000")
                            self.literal("D", "d")
                            self.range("8-9", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                        self.range("0-9", "a-f", "A-F")
                    with self.case():
                        self.literal("\\")
                        self.range(
                            "\"", "\\", "/", "b", 
                            "f", "n", "r", "t", "'", "\n",
                        )
                self.literal("\'")

    @rule()
    def rson_list(self):
        self.literal("[")
        self.comment.inline()
        with self.capture_node("list"), self.repeat(max=1):
            self.rson_value()
            with self.repeat(min=0):
                self.comment.inline()
                self.literal(",")
                self.comment.inline()
                self.rson_value()
            self.comment.inline()
            with self.optional():
                self.literal(",")
                self.comment.inline()
        self.literal("]")

    @rule()
    def rson_object(self):
        self.literal("{")
        self.comment.inline()
        with self.capture_node("object"), self.optional():
            with self.capture_node("pair"):
                self.rson_string()
                self.comment.inline()
                self.literal(":")
                self.comment.inline()
                self.rson_value()
            self.comment.inline()
            with self.repeat(min=0):
                self.literal(",")
                self.comment.inline()
                with self.capture_node("pair"):
                    self.rson_string()
                    self.comment.inline()
                    self.literal(":")
                    self.comment.inline()
                    self.rson_value()
                self.comment.inline()
            with self.optional():
                self.literal(",")
                self.comment.inline()
        self.literal("}")

if __name__ == "__main__":
    import subprocess
    import os.path


    filename = sibling(__file__, "RSONParser.py")
    code = compile_python(RSON, cython=False)

    with open(filename, "w") as fh:
        fh.write(code)

    filename = sibling(__file__, "RSONParser.pyx")
    code = compile_python(RSON, cython=True)

    with open(filename, "w") as fh:
        fh.write(code)

    subprocess.run(f"python3 `which cythonize` -i {filename}", shell=True).check_returncode()
