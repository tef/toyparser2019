#!/usr/bin/env python3 

import os
import sys
import os.path

old = set(sys.modules.keys())

from clgi.errors import Bug, Error
from clgi.app import App, Router, command, Plaintext, Document

from remarkable import dom
from remarkable.parser import parse
from remarkable.render_ansi import to_ansi, RenderBox
from remarkable.render_html import to_html

new = sys.modules.keys() - old

path = os.path.dirname(os.path.abspath(__file__))
files = [os.path.abspath(__file__)]

for module in new:
    m = sys.modules[module]
    file = getattr(m, "__file__", "")
    if file and os.path.commonprefix([file, path]) == path:
        files.append(file)

modified = []

for file in files:
    dir, p = os.path.split(file)
    swapfile = os.path.join(dir, f".{p}.swp")
    if os.path.exists(swapfile):
        with open(swapfile,'rb') as fh:
            contents = fh.read()
            if contents[:5] != b"b0VIM": continue
            fn = contents[108:1008].rsplit(b"\x00",1)[-1]
            if fn.endswith(b"U"):
                modified.append(file)

for m in modified:
    print("modified!", os.path.relpath(m), file=sys.stderr)

class AppError(Error):
    pass

router = Router()

@router.on_error(AppError)
def app_error(request, code):
    args = request.args
    error_args, original_request = args['args'], args['request']
    code(-1)
    filename = error_args
    if filename:
        return ["app error: {}".format(filename)]

@router.on("convert", "convert:html") 
@command(args=dict(file="path"))
def ConvertHtml(ctx, file):
    app = ctx['app']
    name = ctx['name']
    filename = os.path.relpath(file)
    with open(filename) as fh:
        doc = parse(fh.read())
        text = to_html(doc) 
    return Plaintext(text)

@router.on("convert:rson") 
@command(args=dict(file="path"))
def ConvertHtml(ctx, file):
    app = ctx['app']
    name = ctx['name']
    filename = os.path.relpath(file)
    with open(filename) as fh:
        doc = parse(fh.read())
        text = dom.dump(doc)
    return Plaintext(text)

@router.on("convert:ansi") 
@command(args=dict(heading="--str?", width="--int?", height="--int?", file="path"))
def ConvertAnsi(ctx, file, width, height, heading):
    app = ctx['app']
    name = ctx['name']
    width = width or 80
    height = height or 24
    filename = os.path.relpath(file)
    with open(filename) as fh:
        doc = parse(fh.read())
        box = RenderBox(indent=0, width=width, height=height)
        settings = {'double': (heading == 'double'), 'width': width, 'height': height}
        mapping, text = to_ansi(doc, box, settings)
    return Plaintext(text)

@router.on("test") 
@command(args=dict(heading="--str?", width="--int?", height="--int?", file="path"))
def View(ctx, file, width, height, heading):
    app = ctx['app']
    name = ctx['name']
    filename = os.path.relpath(file)
    settings = {}
    settings['double']=(heading!="single")
    if width: settings['width']=width

    with open(filename) as fh:
        text = fh.read()
        doc = parse(text)

    fragments = []
    dom.run_tests(doc, parse)

    tests = list(doc.select('TestCase'))

    for t in tests:
        fragments.append(t)
        if t.get_arg('state') == 'working':
            fragments.append(dom.Paragraph((), ["worked"]))
        else:
            fragments.append(dom.Paragraph((), ["failed"]))
            result_dom = t.get_arg('result_dom')
            if result_dom:
                fragments.append(dom.Paragraph((), ["raw ast: ",dom.dump(results[i])]))
            else:
                fragments.append(dom.Paragraph((), ["raw ast: null"]))
        fragments.append(dom.HorizontalRule((), ()))


    return Document(dom.Document((), fragments), settings)

@router.on("view") 
@command(args=dict(heading="--str?", width="--int?", height="--int?", file="path"))
def View(ctx, file, width, height, heading):
    app = ctx['app']
    name = ctx['name']
    filename = os.path.relpath(file)
    with open(filename) as fh:
        doc = parse(fh.read())
    settings = {}
    settings['double']=(heading!="single")
    if width: settings['width']=width
    dom.run_tests(doc, parse)

    return Document(doc, settings)
app = App(
    name="remark", 
    version="0.0.1",
    command=router,
    args={ },
)



app.main(__name__)
