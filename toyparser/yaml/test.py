from ..grammar import Grammar, compile_python
from ..old_grammar import compile, Parser
from .YAML import YAML, builder
from .YAMLParser import Parser as YAMLParser

def walk(node, indent="- "):
    print(indent, node, node.value)
    for child in node.children:
        walk(child, indent+ "  ")

if __name__ == '__main__':

    parser = Parser(YAML)
    parser2 = YAMLParser(None)
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
