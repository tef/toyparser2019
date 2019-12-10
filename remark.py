#!/usr/bin/env python3 

import os
import sys
import os.path

old = set(sys.modules.keys())

from clgi.errors import Bug, Error
from clgi.app import App, Router, command, Plaintext, Document

from remarkable import dom
from remarkable.parser import parse, parse_commonmark
from remarkable.spec import run_tests
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

def is_modified(file):
    dir, p = os.path.split(file)
    swapfile = os.path.join(dir, f".{p}.swp")
    if os.path.exists(swapfile):
        with open(swapfile,'rb') as fh:
            contents = fh.read()
            if contents[:5] != b"b0VIM": return
            fn = contents[108:1008].rsplit(b"\x00",1)[-1]
            if fn.endswith(b"U"):
                return True

modified = []

for file in files:
    if is_modified(file):
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
        run_tests(doc)
        text = to_html(doc) 
    return Plaintext(text)

@router.on("convert:rson") 
@command(args=dict(file="path"))
def ConvertRson(ctx, file):
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
def Test(ctx, file, width, height, heading):
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
    run_tests(doc)


    if is_modified(filename):
        fragments.append(dom.HorizontalRule((), ()))
        fragments.append(dom.Paragraph((), ["unsaved", " ", "changes", " ", "in", " ", filename]))
        fragments.append(dom.HorizontalRule((), ()))

    for r in doc.select('TestReport'):
        fragments.append(r)
        fragments.append(dom.HorizontalRule((), ()))

    skipped = []
    for t in doc.select('TestCase'):
        if t.get_arg('state') == 'working':
            pass # fragments.append(dom.Paragraph((), ["worked"]))
        elif t.get_arg('state') == 'skipped':
            skipped.append(t)
            skipped.append(dom.Paragraph((), ["skipped"]))
            skipped.append(dom.HorizontalRule((), ()))
        else:
            fragments.append(t)
            fragments.append(dom.Paragraph((), ["failed"]))
            result_dom = t.get_arg('result_dom')
            if result_dom:
                fragments.append(dom.Paragraph((), ["raw ast: ",dom.dump(result_dom)]))
            else:
                fragments.append(dom.Paragraph((), ["raw ast: null"]))
            fragments.append(dom.HorizontalRule((), ()))
    fragments.extend(skipped)

    return Document(dom.Document((), fragments), settings)

@router.on("view") 
@command(args=dict(heading="--str?", width="--int?", height="--int?", file="path"))
def View(ctx, file, width, height, heading):
    app = ctx['app']
    name = ctx['name']
    filename = os.path.relpath(file)
    if is_modified(file):
        print("modified!", file, file=sys.stderr)
    with open(filename) as fh:
        doc = parse(fh.read())
    settings = {}
    settings['double']=(heading!="single")
    if width: settings['width']=width
    run_tests(doc)

    return Document(doc, settings)
@router.on("view:commonmark") 
@command(args=dict(heading="--str?", width="--int?", height="--int?", file="path"))
def View(ctx, file, width, height, heading):
    app = ctx['app']
    name = ctx['name']
    filename = os.path.relpath(file)
    if is_modified(file):
        print("modified!", file, file=sys.stderr)
    with open(filename) as fh:
        doc = parse_commonmark(fh.read())
    settings = {}
    settings['double']=(heading!="single")
    if width: settings['width']=width
    run_tests(doc)

    return Document(doc, settings)
app = App(
    name="remark", 
    version="0.0.1",
    command=router,
    args={ },
)



app.main(__name__)
