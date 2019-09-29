"""
# Remarkable, a restructured markup format.

## The summary

The syntax sugar is very similar to markdown

- Words seperated by whitespace, empty line is paragraph break
- `# Header`, `## Subheader` 
- *\*strong\**, _\_emphasis\__
- `---` Horizonal Rule
- `- indented list item`, `> indented quote item`, with at most one empty line between items
- ``` `raw text` ```, ` ```raw text``` `
- `\*`, `\_`, `\#`, `\>`, ```\```` to get those characters, even `\\`
- `\` at the end of a line forces a line break

Every piece of ascii-art has a more canonical longer form, called a directive:

- `\heading[1]{text}`, or `\h[2]{text}`
- `\emphasis{text}`, `\strong{text}`
- `\hr`, `\br` 
- `\list{\item{text}}`, 

For example, `# My heading` can be expressed in several different ways:

- `\heading[1]: My Heading`
- `\heading[1]{My Heading}`
- `\heading[level:1]{My Heading}`,
- `\heading[level:1]{{{My Heading}}}`
- ```
  @heading {
      level: 1,
      text: ["My Heading", ],
  }
  ```

Directives can take parameters, alongside text:

- `\foo[key: "value", "key": "value"]{text}`
- `\foo[bare_key, "value with no key"]{text}`
- `\foo[a,b,c]` is `\foo["a": null, "b":null, "c":null]`

Keys can be quoted strings, or identifier like bare words. Values can take numerous JSON like forms:

- `0x123`, `0b111`, `0o123`, `123` 
- `123.456`, `123e45`,floats
- `"strings"`, `'or single quoted'`
- `[lists]`, `{key:value}`

Directives also have an 'argument only form', somewhat like JSON:

```
@metadata {
    author: "tef",
    date: 2019-09-30T12:00Z,
}
```

Finally, directives can take list, quote, or code blocks as arguments, along with text:

```
\code``` ... ```

\list:
- 1 
- 2

\quote:
> para

\para: Until the next paragraph break,
which includes trailing lines

\section:
    This text is indented
```

## Example Document

Putting it all together, here's a larger example:

```
@metadata {
    author: "tef",
    version: "123",
}

# A title

A paragraph is split
over  multiple lines

Although this one \
Contains a line break

- here is a list item with `raw text`

- here is the next list item


- this is a new list

  > this is a quoted paragraph inside the list

  > this is a new paragraph inside the blockquote


  > this is a new blockquote

This paragraph contains _emphasis_ and *strong text*. As well as ___emphasis over
multiple lines___ and `inline code`, too.

\list[start: 1]:
- a final list
- that starts at 1
  - with an unnumbered
  - sublist inside, that has text that
continues on the next line.

This is the last paragraph, which contains a non-breaking\ space.
```

"""

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

def builder(buf, node, children):
    kind = node.kind

    if kind == 'number': 
        return eval(buf[node.start:node.end])
    if kind == 'string': 
        return unescape(buf[node.start:node.end])
    if kind == 'list': 
        return children
    if kind == 'object': 
        return dict(children)
    if kind == 'pair':
        return children
    if kind == 'document': 
        return children[0]
    if kind =='bool': 
        return bools[buf[node.start:node.end]]
    if kind == 'null': 
        return None
    if kind == 'identifier':
        return buf[node.start:node.end]
    if kind == "tagged":
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
    return {node.kind: node.children}


class Remarkable(Grammar, start="document", whitespace=[" ", "\t"], newline=["\r", "\n", "\r\n"], tabstop=8):
    # block
    @rule(start="document")
    def document(self):
        with self.repeat(min=0):
            self.indent()
            with self.choice():
                with self.case(): self.block_element()
                with self.case(): self.empty_lines()
                with self.case(): self.end_of_file()
        self.whitespace()
        self.end_of_file()
        self.print(3)

    @rule(inline=True)
    def empty_lines(self):
        self.whitespace()
        self.newline()
        with self.repeat():
            self.indent()
            self.whitespace()
            self.newline()
        with self.capture_node("empty_line"):
            pass

    @rule(inline=True) # 2.1 line ends by newline or end_of_file
    def line_end(self):
        self.whitespace()
        self.end_of_line()


    # blocks
    @rule()
    def block_element(self):
        with self.choice():
            with self.case():
                self.tagged_rson_value()
                self.line_end()
            with self.case():
                self.backtick_code_block()
            #with self.case():
            #    self.blockquote()
            with self.case():
                self.atx_heading()
            with self.case():
                self.thematic_break()
            with self.case():
                self.block_group()
            with self.case():
                self.para()

    @rule() # 4.1
    def thematic_break(self):
        with self.capture_node('thematic_break'):
            with self.repeat(min=3):
                self.literal("-")
        self.line_end()

    @rule()
    def atx_heading(self):
        with self.variable(0) as num, self.capture_node("atx_heading", value=num):
            with self.count(char='#') as level:
                with self.repeat(min=1, max=9):
                    self.literal("#")
            self.set_variable(num, level)
            with self.choice():
                with self.case():
                    self.line_end()
                with self.case():
                    self.whitespace(min=1)
                    self.inline_element()
                    with self.repeat():
                        with self.reject():
                            self.line_end()
                        with self.capture_node("whitespace"):
                            self.whitespace()
                        self.inline_element()
                    with self.optional():
                        self.literal("\\")
                        self.capture_value("\\")
                    self.line_end()



    @rule()
    def start_fenced_block(self):
        self.literal("```")

    @rule()
    def backtick_code_block(self):
        with self.capture_node('fenced_code'):
            fence = "`"
            with self.count(char=fence) as c, self.repeat(min=3):
                self.literal(fence)
            with self.capture_node('info'), self.repeat(min=0):
                with self.reject(): # Example 115
                    self.literal(fence)
                with self.choice():
                    with self.case(): self.escaped_text()
                    with self.case(): self.html_entity()
                    with self.case():
                        with self.capture_node('text'):
                            self.range("\n", invert=True)
                            with self.repeat(min=0):
                                self.range("\n", "\\", "&", "`", invert=True)
            self.line_end()
            with self.repeat():
                self.indent()
                with self.reject():
                    with self.repeat(min=c):
                        self.literal(fence)
                    self.end_of_line()
                with self.capture_node('text'), self.repeat(min=0):
                    self.range("\n", invert=True)
                self.line_end()
            self.indent()
            with self.repeat(min=c):
                self.literal(fence)
            self.whitespace()
            self.line_end()

    @rule()
    def start_group(self):
        self.whitespace(max=8)
        self.literal("-")
        with self.choice():
            with self.case(), self.lookahead():
                self.whitespace()
                self.end_of_line()
            with self.case():
                self.whitespace(min=1, max=1, newline=True)

    @rule()
    def list_interrupts(self):
        with self.choice():
            with self.case(): self.thematic_break()
            with self.case(): self.atx_heading()
            with self.case(): self.start_fenced_block()
            with self.case(): self.start_group()
            # with self.case(): self.start_blockquote()


    @rule()
    def group_item(self):
            with self.choice():
                with self.case():
                    self.whitespace()
                    with self.reject(): 
                        self.newline()
                with self.case():
                    with self.lookahead():
                        self.whitespace()
                        self.newline()

                    with self.indented():
                        self.whitespace()
                        self.newline()
                        self.indent()
                    self.whitespace(min=1, max=1)

            self.block_element()
            with self.repeat():
                self.indent()
                with self.optional():
                    with self.repeat(max=2):
                        self.whitespace()
                        with self.capture_node("empty"):
                            self.newline()
                        self.indent()
                    with self.lookahead():
                        self.whitespace()
                        self.range("\n", invert=True)
                self.whitespace(min=1, max=1)
                self.block_element()

    @rule()
    def block_group(self):
        with self.variable('group') as kind, self.capture_node(kind):
            with self.count(columns=True) as w:
                with self.count(columns=True) as i:
                    self.whitespace(max=8)
                with self.backref() as delimiter, self.choice():
                    with self.case():
                        self.literal("-")
                        self.set_variable(kind, "list")
                    with self.case():
                        self.literal(">")
                        self.set_variable(kind, "quote")

            with self.choice():
                with self.case(), self.lookahead():
                    self.whitespace()
                    self.end_of_line()
                with self.case():
                    self.whitespace(min=1, max=1, newline=True)

            with self.choice():
                with self.case():
                    with self.capture_node("item"):
                        with self.indented(count=w, dedent=self.list_interrupts):
                            self.group_item()
                with self.case():
                    with self.capture_node("item"):
                        self.whitespace()
                    self.end_of_line()

            with self.repeat():
                self.indent()
                with self.optional():
                    with self.capture_node('emptylist'):
                        self.whitespace()
                        self.newline()
                    self.indent()
                    with self.lookahead():
                        self.whitespace(min=i, max=i)
                        self.literal(delimiter)

                self.whitespace(min=i, max=i)
                self.literal(delimiter)
                with self.choice():
                    with self.case(), self.lookahead():
                        self.whitespace()
                        self.end_of_line()
                    with self.case():
                        self.whitespace(min=1, max=1, newline=True)

                with self.choice():
                    with self.case():
                        with self.capture_node("item"):
                            with self.indented(count=w, dedent=self.list_interrupts):
                                self.group_item()
                    with self.case():
                        with self.capture_node("item"):
                            self.whitespace()
                        self.end_of_line()



    # inlines

    @rule()
    def para_interrupt(self):
        with self.choice():
            with self.case(): self.thematic_break()
            with self.case(): self.atx_heading()
            with self.case(): self.start_group()
            with self.case(): self.start_fenced_block()
            # with self.case(): self.start_blockquote()
            
    @rule(inline=True)
    def linebreak(self):
        with self.choice():
            with self.case():
                with self.choice():
                    with self.case(): self.whitespace(min=2)
                    with self.case(): self.literal("\\")
                with self.capture_node("hardbreak"):
                    self.newline()
            with self.case():
                self.whitespace()
                with self.capture_node("softbreak"):
                    self.newline()

        self.indent(partial=True)
        with self.reject(): 
            self.para_interrupt()
        self.whitespace()
        with self.reject(): 
            self.newline()

    @rule()
    def para(self):
        self.whitespace()
        with self.capture_node("para"):
            self.inline_element()

            with self.repeat():
                with self.choice():
                    with self.case():
                        self.linebreak()
                    with self.case():
                        with self.capture_node("whitespace"):
                            self.whitespace()

                # 4.1 Ex 27, 28. Thematic Breaks can interrupt a paragraph
                self.inline_element()

            self.whitespace()
            with self.optional():
                self.literal("\\")
                self.capture_value("\\")
            self.end_of_line()

    @rule()
    def inline_element(self):
        with self.choice():
            with self.case():
                self.code_span()

            with self.case():
                self.escaped_text()

            with self.case():
                with self.capture_node('text'):
                    self.range(" ", "\n", "\\", invert=True)
                    with self.repeat(min=0):
                        with self.choice():
                            with self.case():
                                self.range(" ", "\n", "`", invert=True)
                            with self.case():
                                with self.reject(offset=-1):
                                    self.range(unicode_punctuation=True)
                                with self.repeat(min=1): 
                                    self.literal("_") 

    @rule(inline=True)
    def escaped_text(self):
        with self.choice():
            with self.case():
                self.literal("\\")
                with self.capture_node("text"):
                    self.range("!-/",":-@","[-`","{-~")

            with self.case(), self.capture_node("text"):
                self.literal("\\")
                with self.reject(): # hardbreaks
                    self.newline()
                    self.whitespace()
                    self.range('\n', invert=True)

    @rule(inline=True)
    def html_entity(self):
        self.literal("&");
        with self.choice():
            with self.case():
                self.literal("#")
                with self.capture_node("html_entity", value="decimal"), self.repeat(min=1, max=7):
                    self.range("0-9")
                self.literal(";")
            with self.case():
                self.literal("#")
                self.range("x","X")
                with self.capture_node("html_entity", value="hex"):
                    self.range("0-9", "a-f","A-F")
                    with self.repeat(min=0, max=6):
                        self.range("0-9", "a-f","A-F")
                self.literal(";")
            with self.case():
                with self.capture_node("html_entity", value="named"):
                    self.range("a-z","A-Z")
                    with self.repeat(min=1):
                        self.range("0-9","a-z","A-Z")
                self.literal(";")

    @rule()
    def code_span(self):
        with self.choice():
            with self.case():
                with self.count(char="`") as c, self.repeat(min=1):
                    self.literal("`")
                with self.capture_node('code_span') as span, self.repeat(min=1), self.choice():
                    with self.case():
                        with self.capture_node('text'):
                            self.range("\n", "`", invert=True)
                            with self.repeat(min=0):
                                self.range("\n", "`", invert=True)
                    with self.case():
                        with self.capture_node("text"):
                            self.newline()
                        self.indent(partial=True)
                    with self.case():
                        with self.reject():
                            with self.repeat(min=c, max=c):
                                self.literal("`")
                            with self.choice():
                                with self.case(): self.range('`', invert=True)
                                with self.case(): self.end_of_file()
                        with self.capture_node("text"), self.repeat():
                            self.literal("`")
                with self.repeat(min=c, max=c):
                    self.literal("`")
                with self.reject():
                    self.literal("`")
            with self.case():
                with self.capture_node('text'), self.repeat(min=1):
                    self.literal("`")

    # rson

    @rule()
    def rson_value(self):
        with self.choice():
            with self.case():
                self.tagged_rson_value.inline()
            with self.case():
                self.rson_literal.inline()
    @rule()
    def tagged_rson_value(self):
        with self.capture_node('tagged'):
            self.literal('@')
            with self.capture_node('identifier', nested=False):
                self.range("a-z", "A-Z")
                with self.repeat():
                    self.range("0-9", "a-z","A-Z","_")
            self.literal(' ')
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

    @rule(inline=True)
    def rson_comment(self):
        self.whitespace()
        with self.repeat(min=0):
            self.literal("#")
            with self.repeat(min=0):
                self.range("\n", invert=True)
            self.whitespace()
        self.whitespace()

    @rule()
    def rson_list(self):
        self.literal("[")
        self.rson_comment.inline()
        with self.capture_node("list"), self.repeat(max=1):
            self.rson_value()
            with self.repeat(min=0):
                self.rson_comment.inline()
                self.literal(",")
                self.rson_comment.inline()
                self.rson_value()
            self.rson_comment.inline()
            with self.optional():
                self.literal(",")
                self.rson_comment.inline()
        self.literal("]")

    @rule()
    def rson_object(self):
        self.literal("{")
        self.rson_comment.inline()
        with self.capture_node("object"), self.optional():
            with self.capture_node("pair"):
                self.rson_string()
                self.rson_comment.inline()
                self.literal(":")
                self.rson_comment.inline()
                self.rson_value()
            self.rson_comment.inline()
            with self.repeat(min=0):
                self.literal(",")
                self.rson_comment.inline()
                with self.capture_node("pair"):
                    self.rson_string()
                    self.rson_comment.inline()
                    self.literal(":")
                    self.rson_comment.inline()
                    self.rson_value()
                self.rson_comment.inline()
            with self.optional():
                self.literal(",")
                self.rson_comment.inline()
        self.literal("}")
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
                # hexfloat?
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


if __name__ == "__main__":
    import subprocess
    import os.path


    filename = sibling(__file__, "RemarkableParser.py")
    code = compile_python(Remarkable, cython=False)

    with open(filename, "w") as fh:
        fh.write(code)

    filename = sibling(__file__, "RemarkableParser.pyx")
    code = compile_python(Remarkable, cython=True)

    with open(filename, "w") as fh:
        fh.write(code)

    subprocess.run(f"python3 `which cythonize` -i {filename}", shell=True).check_returncode()



'''
class CommonMark(Grammar, capture="document", whitespace=[" ", "\t"], newline=["\n"], tabstop=4):

    @rule()
    def left_flank(self):
        with self.capture_node("left_flank"), self.choice():
            with self.case():
                with self.lookahead(offset=-1):
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range("_", "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                with self.reject():
                    self.range(unicode_whitespace=True, unicode_newline=True)
                self.capture_value("left")
                self.capture_value(chr)
                self.capture_value(n)

            with self.case():
                with self.reject(offset=-1):
                    self.range(unicode_punctuation=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range("_", "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                with self.reject():
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                self.capture_value('left')
                self.capture_value(chr)
                self.capture_value(n)
                    
    @rule()
    def right_flank(self):
        with self.capture_node("right_flank"), self.choice():
            with self.case():
                with self.reject(offset=-1):
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range("_", "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                self.capture_value("right")
                self.capture_value(chr)
                self.capture_value(n)

            with self.case():
                with self.reject(offset=-1):
                    self.range(unicode_whitespace=True, unicode_newline=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range("_", "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                with self.lookahead():
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                self.capture_value("right")
                self.capture_value(chr)
                self.capture_value(n)
                
    @rule()
    def dual_flank(self):
        with self.capture_node("dual_flank"), self.choice():
            with self.case():
                with self.lookahead(offset=-1):
                    self.range(unicode_punctuation=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range("_", "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                with self.lookahead():
                    self.range(unicode_punctuation=True)
                self.capture_value("dual")
                self.capture_value(chr)
                self.capture_value(n)

            with self.case():
                with self.reject(offset=-1):
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                with self.count(columns=True) as n:
                    with self.backref() as chr:
                        self.range( "*")
                    with self.repeat(min=0):
                        self.literal(chr)
                with self.reject():
                    self.range(unicode_whitespace=True, unicode_newline=True, unicode_punctuation=True)
                self.capture_value('dual')
                self.capture_value(chr)
                self.capture_value(n)
'''
