#!/usr/bin/env python3 

import os

from clgi.errors import Bug, Error
from clgi.app import App, Router, command, Plaintext, Document

from remarkable import dom
from remarkable.parser import parse
from remarkable.render_ansi import to_ansi, RenderBox
from remarkable.render_html import to_html

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
        tests = list(doc.select('TestCase'))
        results = []
        success = []
        for test_case in tests:
            raw_text = test_case.get_arg('input_text')
            output_dom = test_case.get_arg('output_dom')
            result_dom = parse(raw_text)
            results.append(result_dom)
            success.append(result_dom == output_dom)

        fragments = []
        for i, t in enumerate(tests):
            fragments.append(t)
            if success[i]:
                fragments.append(dom.Paragraph((), ["worked"]))
            else:
                fragments.append(dom.Paragraph((), ["failed"]))
                if result_dom:
                    fragments.append(result_dom)

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

    return Document(doc, settings)
app = App(
    name="remark", 
    version="0.0.1",
    command=router,
    args={ },
)



app.main(__name__)
