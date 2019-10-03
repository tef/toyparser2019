"""
# Remarkable, a restructured markup format.

## The summary

The syntax sugar is very similar to markdown

- Words seperated by whitespace, empty line is paragraph break
- `# Header`, `## Subheader` 
- *\*strong\**, _\_emphasis\__ ~\~strike through\~~
- `---` Horizonal Rule
- ``` `raw text` ```, ` ```raw text``` `
- `\*`, `\_`, `\#`, `\>`, ```\```` to get those characters, even `\\`
- `\` at the end of a line forces a line break, `\ ` is a non breaking space.

Lists work like markdown, with at most one empty line between items.

```
- A list with one element
that spans two lines


- Another List
  - and a sublist
```

Unlike markdown, `>` works under the same rules as `-`:

```
> A block quote
that spans lines
> And a second paragraph
> and a third


> A new block quote

> A second Paragraph

> A third
```

Like markdown, if there is only one item or no empty lines between items, the block is considered 'tight'. This means
entries are not wrapped in paragraphs. This applies to blockquotes, and lists.

## Directives

Unlike markdown, every piece of ascii-art has a more canonical longer form, called a directive:

- `\heading[1]{text}`, or `\h[2]{text}`
- `\emphasis{text}`, `\strong{text}`
- `\hr`, `\br` 
- `\list[spacing: "loose"]{\item{text}}`, 

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
    date: "2019-09-30T12:00Z",
}
```

Finally, directives can take list, quote, or code blocks as arguments, along with text:

````
\code{text}
\code`raw text` 

\code```
block
```

\list:
- 1 
- 2

\quote:
> para

\para: Until the next paragraph break,
which includes trailing lines

\heading:
This text is not indented
````

## Example Document

Putting it all together, here's a larger example:

````
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
````
"""

import base64, codecs
from datetime import datetime, timedelta, timezone

from ..grammar import Grammar, compile_python, sibling


class Directive:
    def __init__(self, name, args, text):
        self.name = name
        self.args = args
        self.text = text

    def to_text(self):
        return to_text(self)

class Block(Directive):
    pass

class Inline(Directive):
    pass

def to_text(obj):
    if isinstance(obj, str): return obj

    end = "\n" if isinstance(obj, Block) else ""
    args = ", ".join(f"{key}: {repr(value)}" for key, value in obj.args)
    args = f"[{args}]" if args else ""
    text = "".join(to_text(x) for x in obj.text) if obj.text else ""
    text = "{" f"{text}" "}" if text else ";"
    return f"\\{obj.name}{args}{text}"

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
    kind = node.name
    if kind == "value":
        return node.value

    if kind == "document":
        return Directive("document", [], [c for c in children if c is not None])

    if kind == 'identifier':
        return buf[node.start:node.end]
    if kind == "text":
        return buf[node.start:node.end]
    if kind == "whitespace":
        if node.end == node.start:
            return None
        return " "

    if kind == "softbreak":
        return " "
    if kind == "hardbreak":
        return Inline("br", [], [])

    if kind in ('empty', 'empty_line'):
        return None

    if kind == "emoji":
        return Inline("emoij", [],[c for c in children if c is not None])


    if kind == 'horizontal_rule':
        return Block("hr", [], [])

    if kind == "para":
        return Block("para", [], [c for c in children if c is not None])
    if kind == "span":
        if node.value == "_":
            return Inline("span", [("style", "emphasis")],[c for c in children if c is not None])
        if node.value == "*":
            return Inline("span", [("style", "strong")],[c for c in children if c is not None])
        if node.value == "~":
            return Inline("span", [("style","strikethrough")],[c for c in children if c is not None])

    if kind == 'code_block':
        return Block("code", [], [c for c in children if c is not None])
    if kind == 'code_span':
        return Inline("code", [], [c for c in children if c is not None])
    if kind == 'atx_heading':
        return Block("heading", [("level", node.value)], [c for c in children if c is not None])

    if kind == 'group':
        delimiter = children[0]
        if delimiter == '>':
            return Block("quote", [("spacing", node.value)], [c for c in children[1:] if c is not None])
        elif delimiter == '-':
            return Block("list", [("spacing", node.value)], [c for c in children[1:] if c is not None])
    if kind == 'item':
        return Block("item", [], [c for c in children if c is not None])
    if kind == 'group_delimiter':
        return buf[node.start:node.end]

    if kind == 'block_rson':
        text = []
        args = children[1]
        if isinstance(args, dict) and 'text' in args:
            text = args.pop('text')
        args = list(args.items())
        return Block(children[0], args, text)

    if kind == "directive":
        text = [children[2]] if children[2:] and children[2] is not None else []
        if text and text[0].name in ('directive_span', 'quote', 'list'):
            text = text[0].text
        return Directive(children[0], children[1], text)
    if kind == "arg":
        return children
    if kind == "directive_args":
        return children
    if kind == "directive_name":
        return buf[node.start:node.end]
    if kind == "directive_text":
        return Directive('directive_span',[],[c for c in children if c is not None])


    if kind == 'rson_number': 
        return eval(buf[node.start:node.end])
    if kind == 'rson_string': 
        return unescape(buf[node.start:node.end])
    if kind == 'rson_list': 
        return children
    if kind == 'rson_object': 
        return dict(children)
    if kind == 'rson_pair':
        return children
    if kind =='rson_bool': 
        return bools[buf[node.start:node.end]]
    if kind == 'rson_null': 
        return None
    if kind == "rson_tagged":
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
    raise Exception(node.name)
    return {node.name: children}


class Remarkable(Grammar, start="document", whitespace=[" ", "\t"], newline=["\r", "\n", "\r\n"], tabstop=8):
    # block
    @rule(start="document")
    def document(self):
        with self.choice():
            with self.case():
                self.print("2233")
                self.literal("\\document{")
                with self.repeat():
                    self.whitespace()
                    self.inline_directive()
                    self.whitespace()
                self.literal("}")
                self.whitespace(newline=True)
                self.end_of_file()
            with self.case():
                with self.repeat(min=0):
                    self.indent()
                    with self.choice():
                        with self.case(): self.block_element()
                        with self.case(): self.empty_lines()
                        with self.case(): self.end_of_file()
                self.whitespace()
                self.end_of_file()

    @rule()
    def identifier(self):
        with self.capture_node('identifier', nested=False):
            self.range("a-z", "A-Z")
            with self.repeat():
                self.range("0-9", "a-z","A-Z","_")

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
                self.block_rson()
            with self.case():
                self.code_block()
            with self.case():
                self.atx_heading()
            with self.case():
                self.horizontal_rule()
            with self.case():
                self.block_directive()
            with self.case():
                self.block_group()
            with self.case():
                self.para()

    @rule()
    def block_rson(self):
        with self.capture_node('block_rson'):
            self.literal('@')
            self.identifier()
            self.literal(' ')
            self.rson_literal()
            self.line_end()

    @rule() 
    def horizontal_rule(self):
        with self.capture_node('horizontal_rule'):
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
                        with self.capture_node("text"):
                            self.literal("\\")
                    self.line_end()

    @rule()
    def start_code_block(self):
        self.literal("```")

    @rule()
    def code_block(self):
        with self.capture_node('code_block'):
            fence = "`"
            with self.count(char=fence) as c, self.repeat(min=3):
                self.literal(fence)
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
    def group_interrupts(self):
        with self.choice():
            with self.case(): self.horizontal_rule()
            with self.case(): self.atx_heading()
            with self.case(): self.start_code_block()
            with self.case(): self.start_group()


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

        self.block_element()
        with self.repeat():
            self.indent()
            with self.optional():
                with self.repeat(min=1):
                    self.whitespace()
                    with self.capture_node("empty"):
                        self.newline()
                    self.indent()
                with self.lookahead():
                    self.whitespace()
                    self.range("\n", invert=True)
            self.block_element()

    @rule()
    def block_group(self):
        with self.variable('tight') as spacing, self.capture_node('group', value=spacing):
            with self.count(columns=True) as w:
                with self.count(columns=True) as i:
                    self.whitespace(max=8)
                with self.capture_node('group_delimiter'), self.backref() as delimiter:
                    self.range("-", ">")

            with self.choice():
                with self.case(), self.lookahead():
                    self.whitespace()
                    self.end_of_line()
                with self.case():
                    self.whitespace(min=1, max=1, newline=True)

            with self.capture_node("item"):
                with self.capture_node("item_args"):
                    with self.optional():
                        self.literal("[")
                        self.directive_args()
                        self.literal("] ")
                with self.choice():
                    with self.case():
                        with self.indented(count=1, dedent=self.group_interrupts), self.indented(count=w, dedent=self.group_interrupts):
                            self.group_item()
                    with self.case():
                        self.whitespace()
                        self.end_of_line()

            with self.repeat():
                self.indent()
                with self.optional():
                    with self.capture_node('empty'):
                        self.whitespace()
                        self.newline()
                    self.indent()
                    with self.lookahead():
                        self.whitespace(min=i, max=i)
                        self.literal(delimiter)
                    self.set_variable(spacing, 'loose')

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
                            with self.indented(count=1, dedent=self.group_interrupts):
                                with self.indented(count=w, dedent=self.group_interrupts):
                                    self.group_item()
                    with self.case():
                        with self.capture_node("item"):
                            self.whitespace()
                        self.end_of_line()


    @rule()
    def block_directive(self):
        self.literal("\\")
        with self.capture_node("directive"):
            with self.capture_node("directive_name"):
                self.identifier()
            with self.capture_node("directive_args"), self.optional():
                self.literal("[")
                self.directive_args()
                self.literal("]")
            with self.choice():
                with self.case():
                    self.literal(";")
                    self.capture_value(None)
                    self.newline()
                with self.case():
                    self.code_block()
                with self.case():
                    self.literal(":")
                    with self.choice():
                        with self.case():
                            with self.reject():
                                self.whitespace
                                self.newline()
                            self.para()
                        with self.case():
                            self.whitespace()
                            self.newline()
                            self.indent()
                            with self.choice():
                                with self.case():
                                    self.block_group()
                                with self.case():
                                    self.para()
                        with self.case():
                            self.empty_lines()
                with self.case():
                    self.line_end()
                    self.capture_value(None)

    @rule()
    def directive_args(self):
        self.whitespace(newline=True)
        with self.optional():
            self.directive_arg()
            self.whitespace()
            with self.repeat(min=0):
                self.literal(",")
                self.whitespace(newline=True)
                self.directive_arg()
                self.whitespace()
            with self.optional():
                self.literal(",")
            self.whitespace(newline=True)

    @rule(inline=True)
    def directive_arg(self):
        with self.capture_node("arg"), self.choice():
            with self.case():
                self.identifier()
                with self.optional():
                    self.whitespace()
                    self.literal(":")
                    self.whitespace(newline=True)
                    self.rson_value()
            with self.case():
                self.rson_string()
                self.whitespace()
                self.literal(":")
                self.whitespace(newline=True)
                self.rson_value()
            with self.case():
                self.rson_value()

    # inlines/paras
            
    @rule(inline=True)
    def linebreak(self):
        with self.choice():
            with self.case():
                self.whitespace()
                self.literal("\\")
                with self.capture_node("hardbreak"):
                    self.newline()
            with self.case():
                self.whitespace()
                with self.capture_node("softbreak"):
                    self.newline()

        self.indent(partial=True)
        # allow missing indents if no interrupts
        with self.reject(), self.choice(): 
            with self.case(): self.horizontal_rule()
            with self.case(): self.atx_heading()
            with self.case(): self.start_group()
            with self.case(): self.start_code_block()
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
                self.literal("\\")
                with self.capture_node("text"):
                    self.range("*", "_","!-/",":-@","[-`","{-~")
            with self.case():
                self.literal("\\")
                with self.capture_node("text"):
                    self.whitespace(min=1)
            with self.case():
                self.literal(":")
                with self.capture_node("emoji"):
                    self.identifier()
                self.literal(":")
            with self.case():
                self.inline_directive()
            with self.case():
                self.inline_span()
            with self.case():
                self.code_span()
            with self.case():
                with self.capture_node('text'):
                    self.range(" ", "\n", "\\", invert=True)
                    with self.repeat(min=0):
                        with self.choice():
                            with self.case():
                                self.range(" ", "\n", "`", "_", "*", "~", "\\", "}",invert=True)
                            with self.case():
                                with self.repeat(min=1): 
                                    self.literal("_") 
                                with self.reject():
                                    self.whitespace(newline=True)

    @rule(inline=True)
    def inline_directive(self):
        self.literal("\\")
        with self.capture_node("directive"):
            with self.capture_node("directive_name"):
                self.identifier()
            with self.capture_node("directive_args"), self.optional():
                self.literal("[")
                self.directive_args()
                self.literal("]")
            with self.optional(), self.choice():
                with self.case():
                    self.literal(";")
                    self.capture_value(None)
                with self.case():
                    with self.count(columns=True) as n, self.repeat(min=1):
                        self.literal("{")

                    with self.capture_node("directive_text"):
                        with self.optional():
                            with self.reject():
                                with self.repeat(min=n, max=n):
                                    self.literal("}")
                            self.inline_element()

                            with self.repeat(min=0):
                                with self.choice():
                                    with self.case():
                                        self.linebreak()
                                    with self.case():
                                        with self.capture_node("whitespace"):
                                            self.whitespace()

                                with self.reject():
                                    with self.repeat(min=n, max=n):
                                        self.literal("}")
                                self.inline_element()
                        with self.choice():
                            with self.case():
                                self.linebreak()
                            with self.case():
                                with self.capture_node("whitespace"):
                                    self.whitespace()

                    with self.repeat(min=n, max=n):
                        self.literal("}")
                with self.case():
                    self.code_span()

    @rule()
    def inline_span(self):
        with self.count(columns=True) as n, self.variable('') as fence:
            with self.backref() as chr:
                self.range("_", "*", "~")
            with self.repeat(min=0):
                self.literal(chr)
            with self.reject():
                self.whitespace(newline=True, min=1)
            self.set_variable(fence, chr)


        with self.capture_node('span', value=fence):
            self.inline_element()

            with self.repeat(min=0):
                with self.choice():
                    with self.case():
                        self.linebreak()
                    with self.case():
                        with self.capture_node("whitespace"):
                            self.whitespace()

                with self.reject():
                    with self.repeat(min=n, max=n):
                        self.literal(fence)
                self.inline_element()

            with self.choice():
                with self.case():
                    self.linebreak()
                with self.case():
                    with self.capture_node("whitespace"):
                        self.whitespace()
        with self.repeat(min=n, max=n):
            self.literal(fence)
                
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
                with self.capture_node('rson_tagged'):
                    self.literal('@')
                    self.identifier()
                    self.literal(' ')
                    self.rson_literal()
            with self.case():
                self.rson_literal.inline()

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
        with self.repeat(min=0):
            self.whitespace()
            self.literal("#")
            with self.repeat(min=0):
                self.range("\n", invert=True)
            self.newline()
        self.whitespace(newline=True)

    @rule()
    def rson_list(self):
        self.literal("[")
        self.rson_comment.inline()
        with self.capture_node("rson_list"), self.repeat(max=1):
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
    def rson_key(self):
        with self.choice():
            with self.case(): self.rson_string()
            with self.case(): self.identifier()
    @rule()
    def rson_pair(self):
        with self.capture_node("rson_pair"):
            self.rson_key()
            self.rson_comment.inline()
            self.literal(":")
            self.rson_comment.inline()
            self.rson_value()

    @rule()
    def rson_object(self):
        self.literal("{")
        self.rson_comment.inline()
        with self.capture_node("rson_object"), self.optional():
            self.rson_pair()
            self.rson_comment.inline()
            with self.repeat(min=0):
                self.literal(",")
                self.rson_comment.inline()
                self.rson_pair()
                self.rson_comment.inline()
            with self.optional():
                self.literal(",")
                self.rson_comment.inline()
        self.literal("}")

    rson_true = rule(literal("true"), capture="rson_bool")
    rson_false = rule(literal("false"), capture="rson_bool")
    rson_null = rule(literal("null"), capture="rson_null")

    @rule()
    def rson_number(self):
        with self.capture_node("rson_number", nested=False), self.choice():
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
                with self.capture_node("rson_string", nested=False), self.repeat(), self.choice():
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
                with self.capture_node("rson_string", nested=False), self.repeat(), self.choice():
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
