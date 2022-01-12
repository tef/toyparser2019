import html
from remarkable import dom

# --- Parse Tree Builder
template = """\
<html>
<head>
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
<style type="text/css">
* {{
    -webkit-box-sizing: border-box; 
    -moz-box-sizing: border-box;  
    box-sizing: border-box;   
}}

body, td {{
    background: white;
    font-family: "Lucida Sans Unicode", "Lucida Grande", Verdana, Arial, Helvetica, sans-serif;
    /*color: #000000;*/
    font-size: 0.9rem;
}}
i, em {{
    font-family: Georgia, serif;
}}

h1.title {{font-weight: normal; margin-top: 0; font-size: 1.8rem;}}
h1 {{font-weight: normal; margin-top: 0; font-size: 1.3rem;}}
h2 {{font-weight: normal; margin-top: 0; font-size: 1.1rem; }}

section {{
    margin-bottom: 2em;
}}

blockquote {{
    font-style: italic;
}}

blockquote em {{
    font-style: normal; 
}}

a {{ color: #0000ff; text-decoration: none; }} 
a:hover {{ color: #ff0000; text-decoration: underline; }}
a img {{ outline: 0; border: none; }}

hr {{
    height: 0;
    border: solid 1px;
    color: #cccccc;
    width: 100%;
    max-width: 36rem;
}}

footer {{
    text-align: center;

}}
footer ul {{
    padding-left: 0;
}}
footer li {{
    display: inline-block;
    list-style-type: none;
}}
footer li:after {{
    content: "&mdash;";
}}
footer li:last-child:after {{
    content: "";
}}


@media all and (max-width: 600px)  {{
  article {{
      padding-top: 1rem;
    }}
    nav {{
        border-top: solid 1px;
        width: 100%;
    }}
    body {{
        padding-left:3px;
        padding-right:3px;
    }}
    blockquote, pre, ul, ol {{
        padding-left:1rem;
        margin-left: 0;
        padding-right: 0;
        margin-right: 0;
    }}

}}

@media all and (min-width: 600px)  {{
    pre {{ 
        margin-left: 0rem; 
        padding-left: 1rem; 
        margin-top: 0; 
    }}
    blockquote {{
        margin-left: 0rem; 
        padding-left: 1rem; 
        margin-top: 0; 
        border-left: dotted 1px ;
    }}
    blockquote blockquote {{ 
        margin-left: 0; 
    }}

    blockquote ul, blockquote ol {{
        padding-left: 1rem;
    }}

    ul, ol {{
        padding-left: 1rem;
    }}
    
    body {{
        padding-left:5rem;
        max-width:37rem;
    }}
}}


h1,h2,h3 {{  padding-top:1rem;}}

p {{padding-bottom: 0.2rem;}}

p {{ -webkit-hyphens: none; -moz-hyphens: none; hyphens: none; }}

table {{
    border-spacing: 0;
    border-collapse: collapse;
}}
td {{

          border: 1px solid black;
          padding: 6px 13px;
}}

code {{
        white-space: pre;
}}
.emoji {{
    border: 1px dotted red
}}

</style>
</head>
<body>
{text}
</html>"""


html_tags = {
       dom.Document.name: template,
       dom.Fragment.name: "{text}",
       dom.CommentBlock.name: "<!-- {text} -->\n",
       dom.CommentSpan.name: "<!-- {text} -->\n",
       dom.CodeBlock.name: "<pre><code>{text}</code></pre>\n",
       dom.CodeSpan.name: "<code>{text}</code>",
       dom.Blockquote.name: "<blockquote>{text}</blockquote>",
       dom.TableHeader.name: "<thead><tr>{text}</tr></thead>\n",
       dom.Paragraph.name: "<p>{text}</p>\n",
       dom.Prose.name: '<p style="white-space: pre-wrap">{text}</p>\n',
       dom.Division.name: "<div>{text}</div>\n",
       dom.Section.name: "<section>{text}</section>\n",
       dom.TestCase.name: '<section class="testcase">{text}</section>\n',
       dom.Hardbreak.name: "<br/>",
       dom.Softbreak.name: "\n",
       dom.Emoji.name: "<span class='emoji'>{text}</span>",
       dom.Newline.name: "\n",
       dom.Table.name: "<table>\n{text}</table>\n",
       dom.Row.name: "<tr>{text}</tr>\n",
       dom.CellSpan.name: "<td>{text}</td>",
       dom.CellBlock.name: "<td>{text}</td>",
       dom.Nbsp.name: "&nbsp;",
       dom.Strikethrough.name: "<del>{text}</del>",
       dom.Strong.name: "<strong>{text}</strong>",
       dom.Emphasis.name: "<em>{text}</em>",
       dom.BulletList.name: "<ul>{text}</ul>",
       dom.NumberedList.name: "<ol>{text}</ol>",
       dom.ItemBlock.name: "<li>{text}</li>",
       dom.ItemSpan.name: "<li>{text}</li>",
       dom.RawBlock.name: "{text}",
       dom.RawSpan.name: "{text}",
       dom.Span.name: "<span>{text}</span>\n",
}

def to_html(obj):
    if isinstance(obj, str): return html.escape(obj)

    args = dict(obj.args)
    name = obj.name
    text = obj.text 
    if 'text' in args:
        text = args.pop('text')
    if name in (dom.RawBlock.name, dom.RawSpan.name):
            if args['name'].lower() == 'html':
                text = "".join(obj.text)
            else:
                return "<!-- raw block omitted -->"
    else:
        text = "".join(to_html(x) for x in obj.text if x is not None) if obj.text else ""

    if name == dom.Emoji.name:
        text = args.pop('name')

    if name == dom.Heading.name:
        name = f"h{args.get('level',1)}"
        if 'level' in args: args.pop('level')

    if name in html_tags:
        return html_tags[name].format(name=name, text=text, **args)
    args = " ".join(f"{key}={repr(value)}" for key, value in args.items())
    end = "" if isinstance(obj, dom.Inline) else "\n"
    if text:
        args = f" {args}" if args else ""
        return f"<{name}{args}>{text}</{name}>{end}"
    else:
        args = f" {args}" if args else ""
        return f"<{name}{args}/>{end}"


def to_text(obj):
    if obj is None: return ""
    if isinstance(obj, str): 
        escape = "~_*\\-#`{}[]|@<>"
        return "".join(('\\'+t if t in escape else t) for t in obj).replace("\n", "\\n;")
    if isinstance(obj, dom.Data):
        args = ", ".join(f"{key}: {repr(value)}" for key, value in obj.args)
        return f"@{obj.name}" "{" f"{args}" "}\n"


    end = "\n" if isinstance(obj, dom.Block) else ""
    args = ", ".join(f"{key}: {repr(value)}" for key, value in obj.args) if obj.args else ""
    #if obj.name in ('code', 'code_span') and obj.text:
    #    text = repr("".join(obj.text))
    #    args = f"text: {text}, {args}"
    #    text = ""
    #else:
    text = "".join(to_text(x) for x in obj.text) if obj.text else ""

    args = f"[{args}]" if args else ""
    text = "{" f"{text}" "}" if text else ";"
    return f"\\{obj.name}{args}{text}{end}"

