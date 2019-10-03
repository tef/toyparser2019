"""
# Remarkable, a restructured markup format.

Remarkable has three different ways to specify data. You only care about one, maybe two, 
but there's a third, too. 

The first is markdown like ascii art: `*like this*`

The second is LaTeX like directives: `\like{this}`

The third?, JSON like raw nodes: `@like {text: "this"}`

You can't always get what you want with the ascii-art, but you can use the directives.
You can use the directives, but it isn't always easy to embed data, or be horrifyingly exact, 
so you can embed raw nodes too. 

You are very unlikely to need raw nodes, but if you ever dump the AST, you'll see it.

## The Markdown like Ascii-Art

The syntax sugar is very similar to markdown, github's especially.

- Words are seperated by whitespace, and empty line is paragraph break. 

- `#` marked headers: `# Header`, `## Subheader` and continue on till the end of the paragraph.

- *\*strong\**, _\_emphasis\__ ~\~strike through\~~, \code{\`code\`}, and `:emoij:`

- `---` for a horizonal rule

- use `\*`, `\_`, `\#`, `\>`, \code{\`} to get those characters, even `\\`

- `\` at the end of a line forces a line break, `\ ` is a non breaking space.

- Starting a new list, quote, code block, header, or horizontal rule is also a paragraph break.

Everything else is a bit different. Doubling or tripling markers doesn't change
their meaning:

```
_emphasis_ __emphasis__ ___emphasis___
*strong* **strong** ***strong***
~strike~ ~~strike~~ ~~~strike~~~
```

Code blocks can be tagged with a language identifier, like in markdown:

````
```foo
example
```
````

Lists can have one empty line, or no empty lines between items. Like markdown, if there
is only one item or no empty line between items, the block is considered 'tight'. 
Two empty lines between list items means two lists with one item each.

````
- A list with one element
that spans two lines


- A new List
  
  - A sublist
````

Unlike markdown, `>` works under the same rules as `-`. In other words, only the start of a paragraph gets a `>`, 
and anything indented underneath is included. Using a `>` starts a new paragraph.

```
> A block quote
that spans lines
> And a second paragraph


> A new block quote

> A second Paragraph
```

Arguments can be passed to horizontal rules, lists, quotes, and code blocks too:

````
--- [a:1]

- [b:2] foo
> [c:3] foo

``` [d:4
foo
```
````

## Tables

## The LaTeX-like Directives

Unlike markdown, every piece of ascii-art has a more canonical longer form, called a directive.
A directive has a name, optional parameters, and an argument, usually text:

- `\heading[1]{text}`, or `\h[2]{text}`
- `\emphasis{text}`, `\strong{text}`
- `\hr`, `\br` 
- `\list[spacing: "loose"]{\item{text}}`, 

For example, `# My heading` can be expressed in several different ways:

- `\heading[level: 1]: My Heading`
- `\heading[level: 1]{My Heading}`,
- `\heading[level: 1]{{{My Heading}}}`

Like the block forms above, directives can take parameters, alongside text:

- `\foo[key: "value", "key": "value"]{text}`
- `\foo[bare_key, "value with no key"]{text}`
- `\foo[a,b,c]` is `\foo["a": null, "b":null, "c":null]`. 

Parameters are lists of (key,value) pairs, where one or both are given. non null keys must be unique. 
Keys can be quoted strings, or identifier like bare words. Values can take numerous JSON like forms:

- `0x123`, `0b111`, `0o123`, `123` 
- `123.456`, `123e45`,floats
- `"strings"`, `'or single quoted'`
- `[lists]`, `{key:value}`

Finally, directives can take list, quote, or code blocks as arguments, or a paragraph:

````
\para: This will include all text on this line
and this line too.

\heading:
It can start on the next line and continues
until the end of the paragraph

You can use \code{text} or \code`raw text`, but text in \code{\`} is escaped. 

\code```
a raw block
```

\list:
- 1 
- 2

\quote:
> para

````

## Raw Nodes

If you want to skip the text processing and just dump data inside, you can. A header
can be specified as a raw node, instead of using a directive, or `#` shorthand.

```
  @heading {
      level: 1,
      text: ["My Heading", ],
  }
```

Raw nodes can also be used to specify metadata, although `\metadata[author:"tef", date:"..."]` works just as well.

```
@metadata {
    author: "tef",
    date: "2019-09-30T12:00Z",
    example: \para{...},
}
```

Really they're so things can emit dom nodes in a simpler, canonical form, and you can still paste it midway into another
document. Yes, that's a terrible idea, but stopping it happening doesn't prevent the need.

The subset of Remarkable that's only `@foo{}` with no directives or markup or bare identifiers, is called RSON.

## An Example Document

Putting it all together, here's a larger example:

````````
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
 
  ```` [language: "python"]
  and a code block inside
  ````


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

This is the last paragraph, which contains a non-breaking\ space, and :emoji:.
````````



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

class Raw(Directive):
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
        return Block("document", [], [c for c in children if c is not None])

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
        return Block("hr", children[0], [])
    if kind == "hr_args":
        return children
    if kind == 'atx_heading':
        return Block("heading", [("level", node.value)], [c for c in children if c is not None])

    if kind == "para":
        return Block("para", [], [c for c in children if c is not None])
    if kind == "span":
        return Inline("span", [("marker", node.value)],[c for c in children if c is not None])
    if kind == 'code_span':
        return Inline("code", [], [c for c in children if c is not None])

    if kind == 'code_block':
        arg = children[0] if children[0] is not None else []
        return Block("code", arg, [c for c in children[1:] if c is not None])
    if kind == "code_args":
        return children
    if kind == "code_string":
        return [("language", children)]

    if kind == 'group':
        marker = children[0]
        spacing = children[1]
        return Block("group", [("marker", marker), ("spacing", spacing)], [c for c in children[2:] if c is not None])
    if kind == 'group_marker':
        return buf[node.start:node.end]
    if kind == 'group_spacing':
        return node.value
    if kind == 'item':
        return Block("item", children[0] , [c for c in children[1:] if c is not None])
    if kind == 'item_args':
        return children 

    if kind == "block_directive":
        args = children[1]
        text = [children[2]] if children[2] is not None else []
        if text and text[0].name in ('directive_group', 'directive_para'):
            if text[0].name == "directive_group":
                args = args + text[0].args
            text = text[0].text
        return Block(children[0], args, text)
    if kind == "inline_directive":
        args = children[1]
        text = [children[2]] if children[2:] and children[2] is not None else []
        if text and text[0].name == 'directive_span':
            text = text[0].text
        return Inline(children[0], args, text)
    if kind == "arg":
        return children
    if kind == "directive_args":
        return children
    if kind == "directive_name":
        return buf[node.start:node.end]

    if kind == "directive_span":
        return Inline('directive_span',[],[c for c in children if c is not None])

    if kind == "directive_para":
        return Block('directive_para',[],[c for c in children if c is not None])
    if kind == "directive_group":
        marker = children[0]
        spacing = children[1]
        return Block("directive_group", [("marker", marker), ("spacing", spacing)], [c for c in children[2:] if c is not None])


    if kind == 'block_rson':
        text = []
        args = children[1]
        if isinstance(args, dict) and 'text' in args:
            text = args.pop('text')
        args = list(args.items())
        return Raw(children[0], args, text)

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
                        with self.case(): self.para()
                        with self.case(): self.empty_lines()
                        with self.case(): self.end_of_file()
                self.whitespace()
                self.end_of_file()

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
        with self.reject():
            self.paragraph_breaks()
        self.whitespace()
        with self.reject(): 
            self.newline()

    @rule()
    def paragraph_breaks(self):
        with self.choice():
            with self.case(): self.horizontal_rule()
            with self.case(): self.atx_heading()
            with self.case(): self.start_code_block()
            with self.case(): self.start_group()


    @rule()
    def para(self):
        with self.capture_node("para"):
            self.inner_para()

    @rule()
    def inner_para(self):
        self.whitespace()
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
    def horizontal_rule(self):
        with self.capture_node('horizontal_rule'):
            with self.repeat(min=3):
                self.literal("-")
            with self.capture_node("hr_args"), self.optional():
                self.whitespace(min=1)
                self.literal("[")
                self.directive_args()
                self.literal("]")
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
                    self.inner_para()

    @rule()
    def start_code_block(self):
        self.literal("```")

    @rule()
    def code_block(self):
        with self.capture_node('code_block'):
            fence = "`"
            with self.count(char=fence) as c, self.repeat(min=3):
                self.literal(fence)
            with self.choice():
                with self.case(), self.capture_node("code_args"):
                    self.whitespace(min=1)
                    self.literal("[")
                    self.directive_args()
                    self.literal("]")
                with self.case(), self.capture_node("code_info"):
                    self.whitespace()
                    self.identifier()
                with self.case():
                    self.capture_value(None)

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

        with self.choice():
            with self.case(): self.block_element()
            with self.case(): self.inner_para()


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
            with self.choice():
                with self.case(): self.block_element()
                with self.case(): self.inner_para()

    @rule()
    def block_group(self):
        with self.capture_node('group'):
            self.inner_group()

    @rule()
    def inner_group(self):
        with self.variable('tight') as spacing:
            with self.count(columns=True) as w:
                with self.count(columns=True) as i:
                    self.whitespace(max=8)
                with self.capture_node('group_marker'), self.backref() as marker:
                    self.range("-", ">")
            with self.capture_node('group_spacing', value=spacing):
                pass


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
                        with self.indented(count=1, dedent=self.paragraph_breaks), self.indented(count=w, dedent=self.paragraph_breaks):
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
                        self.literal(marker)
                    self.set_variable(spacing, 'loose')

                self.whitespace(min=i, max=i)
                self.literal(marker)
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
                            with self.indented(count=1, dedent=self.paragraph_breaks):
                                with self.indented(count=w, dedent=self.paragraph_breaks):
                                    self.group_item()
                        with self.case():
                            with self.capture_node("item"):
                                self.whitespace()
                            self.end_of_line()


    @rule()
    def block_directive(self):
        self.literal("\\")
        with self.capture_node("block_directive"):
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
                                self.whitespace()
                                self.newline()
                            with self.capture_node("directive_para"):
                                self.print('inner')
                                self.inner_para()
                        with self.case():
                            self.whitespace()
                            self.newline()
                            self.indent()
                            with self.choice():
                                with self.case():
                                    with self.capture_node("directive_group"):
                                        self.inner_group()
                                with self.case():
                                    with self.capture_node("directive_para"):
                                        self.inner_para()
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
    def inline_directive(self):
        self.literal("\\")
        with self.capture_node("inline_directive"):
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

                    with self.capture_node("directive_span"):
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

    @rule()
    def block_rson(self):
        with self.capture_node('block_rson'):
            self.literal('@')
            self.identifier()
            self.literal(' ')
            self.rson_literal()
            self.line_end()

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
            with self.case(): self.inline_directive()

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
