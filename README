# untitled parser toy

this is a parsing expression library for python 3

the big idea is that you should be able to express Python, Markdown, or similar
without resorting to lexer hacks, or inlining code into the parser

## example

it uses a builder/dsl like thingy to describe and build rules

```

from grammar import Grammar # here we go

class MyGrammar(Grammar, whitespace=[" "], newline=["\n"], start="main"):
    
    @rule()                              # must be decorated
    def main(self): 			 # called, given a builder 
        with self.capture("name"):       # scoped rules
            self.accept("yes")           # built in operators
            self.newline()

a = MyGrammar.parser()

out = a.parse("yes\n")  # returns a Node("name", offset=0, end=4, children=())

builder = {"name": (lambda buf, offset, end, children: buf[offset: end])}

# instead of inline code, pass in a dict of callbacks

print(out.build(builder))

a = MyGrammar.parser(builder)

print(a.parse("yes\n")) # and get "yes\n"

```

## features

 - opt-in memoizaton (as opposed to packrat)
 - explict named captures (as opposed to returning entire parse tree)
 - currently cython output, but no python specific operations are involved
 - handle annoying grammars (indents, prefixes, etc)


## annoying grammar handling

      - indentaton
	- lines must be {n} whitespace chars in from start
        - or empty
        - passing in a tabstop and if allowing mixed space/tabs, at parse time

      - prefixed
        - blockquote/markdown '>' prefixed lines

      - data depedennt
        - counting chars in string and passing it as a value to other rules


## wishlist:

- codegen for other languages
- .peg file parsing

## operators

### terminal operators

`self.whitespace()`, `self.whitespace(min=..., max=..., newline=True)`, `self.newline()`, `self.accept("string")`, `self.range("1", "a-b", invert=True)`,
`self.end_of_line()` newline or eof, `self.end_of_file`, `self.start_of_line()`,


### non terminal/group operators

```
with self.capture("name"): # capture start, end, name and children
	...

with self.lookahead():
	self.accept("+")

with self.repeat(min=1, max=2):
	self.accept(".")

with self.reject():
	self.accept("123")

with self.memoize():
	self.awful_rule()
```

### data dependent operators:

```
with self.count(".") as c:
    with self.repeat(): self.accept(".")

with self.repeat(min=c, max=c):
    self.accept("+")

self.capture_value(c)
```

### intendation operators:

```
self.whitespace()
with self.indented(): # use offset from line start
	self.accept("1")
	with self.repeat():
	    self.newline()
	    self.start_of_line() # include indent
	    self.accept("1')
	self.end_of_line()
```

```
@rule()
def line(self):
    with self.repeat(): self.range("\n", invert=True)

@rule()
def quote(self):
    self.accept(">")
    self.whitespace(max=1)

@rule()
def blockquote(self):
    self.quote()
    with self.quote.as_prefix():
        self.line()
	with self.repeat():
	    self.newline()
	    self.start_of_line() # include indent
	    self.line()
        self.end_of_line()
```


### debugging operators:

```

self.print("string")

with self.trace():
	....
```


