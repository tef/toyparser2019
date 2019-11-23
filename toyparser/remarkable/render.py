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
       "document": template,
       "code_block": "<pre><code>{text}</code></pre>\n",
       "code_span": "<code>{text}</code>",
       "thead": "<thead><tr>{text}</tr></thead>\n",
       "para": "<p>{text}</p>\n",
       "paragraph": "<p>{text}</p>\n",
       "prose": '<p style="white-space: pre-wrap">{text}</p>\n',
       "division": "<div>{text}</div>\n",
       "section": "<section>{text}</section>\n",
       "hardbreak": "<br/>",
       "softbreak": "\n",
       "emoji":"<span class='emoji'>{text}</span>",
       "n": "\n",
       "table": "<table>\n{text}</table>\n",
       "row": "<tr>{text}</tr>\n",
       "cell": "<td>{text}</td>",
       "cell_block": "<td>{text}</td>",
       "nbsp": "&nbsp;",
       "strike": "<del>{text}</del>",
       "strong": "<strong>{text}</strong>",
       "emph": "<em>{text}</em>",
       "block_item": "<li>{text}</li>",
       "item_span": "<li>{text}</li>",
       "block_raw": "{text}",
       "raw_span": "{text}",
       "span": "<span>{text}</span>\n",
}

def to_html(obj):
    if isinstance(obj, str): return html.escape(obj)

    args = dict(obj.args)
    name = obj.name
    text = obj.text 
    if 'text' in args:
        text = args.pop('text')
    if name in ('block_raw', 'raw_span'):
        text = "".join(obj.text)
    else:
        text = "".join(to_html(x) for x in obj.text if x is not None) if obj.text else ""

    if name == "heading":
        name = f"h{args.get('level',1)}"
        if 'level' in args: args.pop('level')

    if name =="blocklist":
        if 'start' in args:
            name = "ol"
        else:
            name = "ul"
        if 'marker' in args: args.pop('marker')


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

