import base64, codecs
from datetime import datetime, timedelta, timezone

from ..grammar import Grammar, compile_python, sibling
from .RemarkableParser import Parser as RemarkableParser
from .Remarkable import Remarkable
from remarkable.parser import builder
from remarkable.render_ansi import to_ansi, RenderBox

def to_text(t):
    settings = {'width':80, 'height':24}
    box = RenderBox(0, 80, 24, encoding=None)

    return to_ansi(t, box, settings)



def walk(node, indent="- "):
    text = ""
    print(indent, node, node.value, text)
    for child in node.children:
        walk(child, indent+ "  ")

if __name__ == "__main__":
    cython_parser = RemarkableParser()
    python_parser = Remarkable.parser()

    import time

    def timeit(name, parser, buf):
        t = time.time()
        o = parser(buf)
        t = time.time() - t
        print(name, t)
        return o, t

    tests = [
        "\n".join([
            "@Tag [1,2,3]",
            ""
        ]),
        "\n".join([
            "# header",
            "para1",
            "",
            "para2",
            "- 1",
            "  - 2",
            "- 3",
            "",
            "",
            "- 4",
            "",
            "",
            "- 5",
            "four",
        ]),
"""\
- 1
  - 2
    - 3
    - 4
  - 4
- 5


- 6

- 7

- 8


- 9
""",
"""\
- 1

  2

  a

  3

  
  4

- 1

- 2


- 3

""",
"""\
# Heading

Para

## Subheading

Para
""",
"""
> quote

> new para


> new quote
""",
"""
*strong*, _emph_

**strong
still**

__emph 

still__

~strike~

:emoji:

\emoji: what
""",
"""
- [a: 1] foo

> [b: 2] foo

``` [c: 2]
foo
```

```butt
nice
```

--- [a:3]

@foo {
        name: \para{butt},
}

*foo*[v:4] `foo`[c:3]

### [but:1] foo

""", """

| a | b |
| - | - |
| 1 | 2 |
| 3 | 4 |
""",
"""
- 
    a 
    b
- 
    c
    d

    e
    f

-
-

-
""","""
\\begin::section
Foo

\end::section
""",
"""
- ```
   fooo
    fofofo
  ```
""",
"""\
- [a: 1]
  foo
- boo
""", """
\\table:
-   
  # X
  # Y
- 
  - a
  - b
-
  - 1
  - 2


""",r"""
\begin::table
\row: \cell{1}\cell{2}
\end::table

\foo`foo`

\foo```
foo
```
"""
    ]

    for testcase in tests:
        for line in testcase.splitlines():
            print("> ", line)

        o1, python_t = timeit("python-compiled", (lambda b: python_parser.parse(b)), testcase)
        #o2, cython_t = timeit("cython", (lambda b: cython_parser.parse(b)), testcase)

        # if not o1 or not o2 or o1.end != o2.end: raise Exception(o1,o2)

        walk(o1)
        print()

    print()

    with open(sibling(__file__, "../../README.remark")) as readme:
        Readme = readme.read()

    out = python_parser.parse(Readme).build(Readme, builder)
    import pprint
    #pprint.pprint(out)
    txt = to_text(out)
    #print(txt)
    #print()





    raw= r"""
@metadata {
    author: "tef",
    version: 23,
}

# A title

A paragraph is split
over  multiple lines

Although this one \
Contains a line break

- here 1

- here 2

  > 2.1

  > 2.2

  > 2.3

This paragraph contains _emphasis_ and *strong text*. As well as ___emphasis over
multiple lines___ and `inline code`, too.

\list[start: 1]:
- a final list
- that starts at 1
  - with an unnumbered
  - sublist inside, that has text that
continues on the next line.

This is the last paragraph, which contains a non-breaking\ space.

---

- 1

  - 2

  - 3


  - 4

- :butt:

\foo: what

- [a: 1] foo

> [b: 2] foo

``` [c: 2]
foo
```

```butt
nice
```

"""
    out = python_parser.parse(raw).build(raw, builder)
    txt = to_text(out)
    print(txt)




