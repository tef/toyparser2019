from grammar import Grammar, compile_python

import codecs

def walk(node, indent="- "):
    print(indent, node, node.value)
    for child in node.children:
        walk(child, indent+ "  ")

def unescape(string):
    return codecs.decode(string, 'unicode_escape')

builder = {
    'number': (lambda buf, start, end, children: int(buf[start:end])),
    'string': (lambda buf, start, end, children: unescape(buf[start:end])),
    'list': (lambda buf, start, end, children: children),
    'object': (lambda buf, start, end, children: dict(children)),
    'pair': (lambda buf, start, end, children: children),
    'document': (lambda buf, start, end, children: children[0]),
    'identifier': (lambda buf, start, end, children: str(buf[start:end])),
    'bool': (lambda buf, start, end, children: bool(buf)),
    'null': (lambda buf, start, end, children: None),
}

class YAML(Grammar, start="document", whitespace=[" ", "\t"], newline=["\n", "\r", "\r\n"]):
    literal = rule( 
        list_literal | object_literal |
        string_literal | number_literal |
        true_literal | false_literal | 
        null_literal
    )

    true_literal = rule(accept("true"), capture="bool")
    false_literal = rule(accept("false"), capture="bool")
    null_literal = rule(accept("null"), capture="null")

    @rule()
    def identifier(self):
        with self.choice():
            with self.case(), self.capture('identifier'), self.repeat(min=1):
                self.range("a-z","A-Z","_")
            with self.case():
                self.string_literal()

    @rule()
    def number_literal(self):
        with self.capture("number"):
            with self.optional():
                self.range("-", "+")
            with self.repeat(min=1):
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
    def string_literal(self):
        self.accept("\"")
        with self.capture("string"), self.repeat(), self.choice():
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
    def list_literal(self):
        self.accept("[")
        self.whitespace(newline=True)
        with self.capture("list"), self.repeat(max=1):
            self.literal()
            with self.repeat(min=0):
                self.whitespace(newline=True)
                self.accept(",")
                self.whitespace(newline=True)
                self.literal()
            self.whitespace(newline=True)
            with self.optional():
                self.accept(",")
                self.whitespace(newline=True)
        self.accept("]")

    @rule()
    def object_literal(self):
        self.accept("{")
        self.whitespace(newline=True)
        with self.capture("object"), self.optional():
            self.string_literal()
            self.whitespace() # must be on same line as :
            self.accept(":")
            self.whitespace(newline=True)
            self.literal()
            with self.repeat(min=0):
                self.whitespace(newline=True)
                self.accept(",")
                self.whitespace(newline=True)
                self.string_literal()
                self.whitespace() # must be on same line as #
                self.accept(":")
                self.whitespace(newline=True)
                self.literal()
            self.whitespace(newline=True)
            with self.optional():
                self.accept(",")
                self.whitespace(newline=True)
        self.accept("}")

    @rule()
    def yaml_eol(self):
        with self.repeat(), self.choice():
            with self.case():
                self.whitespace()
                self.newline()
            with self.case():
                self.whitespace()
                self.accept('#')
                with self.repeat():
                    self.range("\n", invert=True)
                self.newline()

    
    @rule()
    def indented_list(self):
        with self.indented(), self.capture('list'):
            self.accept("-")
            with self.choice():
                with self.case():
                    self.whitespace()
                    self.indented_value()
                with self.case():
                    self.yaml_eol()
                    self.start_of_line()
                    self.whitespace(min=1)
                    self.indented_value()

            with self.repeat():
                self.yaml_eol()
                self.start_of_line()
                self.accept("-")
                self.whitespace(min=1)
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.indented_value()
                    with self.case():
                        self.yaml_eol()
                        self.start_of_line()
                        self.whitespace()
                        self.indented_value()

    @rule()
    def indented_object(self):
        with self.indented(), self.capture('object'):
            with self.capture("pair"):
                self.identifier()
                self.whitespace()
                self.accept(":")
                with self.choice():
                    with self.case():
                        self.yaml_eol()
                        self.start_of_line()
                        self.whitespace(min=1)
                        self.indented_value()
                    with self.case():
                        self.whitespace()
                        self.indented_value()

            with self.repeat(), self.capture("pair"):
                self.yaml_eol()
                self.start_of_line()
                self.identifier()
                self.whitespace()
                self.accept(":")
                self.capture_value("a")
                with self.choice():
                    with self.case():
                        self.whitespace()
                        self.indented_value()
                    with self.case():
                        self.yaml_eol()
                        self.start_of_line()
                        self.whitespace(min=1)
                        self.indented_value()

    @rule()
    def indented_value(self):
        with self.choice():
            with self.case():
                self.indented_object()
            with self.case():
                self.indented_list()
            with self.case():
                self.literal()

    @rule()
    def document(self):
        with self.repeat():
            self.whitespace()
            self.yaml_eol()
        with self.capture("document"), self.choice():
            with self.case():
                self.indented_object()
            with self.case():
                self.indented_list()
            with self.case():
                self.list_literal()
            with self.case():
                self.object_literal()
        self.whitespace()
        with self.repeat():
            self.yaml_eol()
            self.whitespace()
        with self.repeat():
            self.end_of_line()
            self.whitespace()


if __name__ == '__main__':
    import subprocess, sys
    if not sys.argv[1:] or sys.argv[1] != "--skip":
        code = compile_python(YAML, builder, cython=True)
        with open("YAMLParser.pyx", "w") as fh:
            fh.write(code)

        subprocess.run(["python3", "setup.py", "build_ext", "--inplace"]).check_returncode()

        from YAMLParser import Parser as YAMLParser
        parser2 = YAMLParser(None)
    else:
        parser2 = YAML.parser()
    from old_grammar import compile, Parser

    parser = Parser(YAML, None)
    import time

    def yaml(buf):
        print(len(buf))
        print(buf)
        t1 = time.time()
        node = parser.parse(buf)
        t1 = time.time() - t1
        t2 = time.time()
        node2 = parser2.parse(buf)
        t2 = time.time() - t2
        if node:
            walk(node)
        else:
            print('parser1failed')
        print(parser2)
        if node2:
            walk(node2)
        else:
            raise Exception('no')
            print('parser2failed')
   #     print(t1, t2, t2/t1*100)
        print()

    # yaml = lambda x:x
    yaml("""\
- 1
- 2
- 
  - 3
  - 4
- 5
- 6
- - 7
  - 8
  - - 9
  - 
    - 10
    - 11
- 12
- 
 13
    """)

    yaml("""\
    servers:
        alpha: { "a": 1 }
    example: 
        a: 1
        b: 2
    """)
    yaml("""\
    servers:
      alpha: {
        "ip": "10.0.0.1",
        "names": [
          "alpha",
          "alpha.server",
        ],
      }
      beta: {
        "ip": "10.0.0.2",
        "names": ["beta"],
      }
    """)

    yaml("""\
    title: "SafeYAML Example"

    database:
      server: "192.168.1.1"

      ports:
        - 8000
        - 8001
        - 8002

      enabled: true

    servers:
      alpha: {
        "ip": "10.0.0.1",
        "names": [
          "alpha",
          "alpha.server",
        ],
      }
      beta: {
        "ip": "10.0.0.2",
        "names": ["beta"],
      }
    """)

    yaml("""\
example: 
\ta: 1
        b: 2
""")
