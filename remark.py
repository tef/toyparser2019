#!/usr/bin/env python3 

import os

from clgi.errors import Bug, Error
from clgi.app import App, Router, command, Plaintext, Document
from clgi.render import to_ansi
from toyparser.remarkable.Remarkable import parse, to_html

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
        dom = parse(fh.read())
        text = to_html(dom) 
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
        dom = parse(fh.read())
        mapping, text = to_ansi(dom, indent=0, width=width, height=height, double=(heading=="double"))
    return Plaintext(text)

@router.on("view") 
@command(args=dict(file="path"))
def View(ctx, file):
    app = ctx['app']
    name = ctx['name']
    filename = os.path.relpath(file)
    with open(filename) as fh:
        dom = parse(fh.read())
    return dom
app = App(
    name="remark", 
    version="0.0.1",
    command=router,
    args={ },
)



app.main(__name__)
