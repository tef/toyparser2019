#!/usr/bin/env python3 

import os

from clgi.errors import Bug, Error
from clgi.app import App, Router, command, Plaintext, Document
from toyparser.remarkable.Remarkable import parse, to_html, to_ansi

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

@router.on("convert", "convert:html") # no path given
@command(args=dict(file="path"))
def Remark(ctx, file):
    app = ctx['app']
    name = ctx['name']
    filename = os.path.relpath(file)
    with open(filename) as fh:
        dom = parse(fh.read())
        text = to_html(dom) 
    return Plaintext(text)

@router.on("convert:ansi") # no path given
@command(args=dict(file="path"))
def Remark(ctx, file):
    app = ctx['app']
    name = ctx['name']
    filename = os.path.relpath(file)
    with open(filename) as fh:
        dom = parse(fh.read())
        text = dom.to_ansi(indent=0, width=80, height=24) 
    return Plaintext(text)

@router.on("view") # no path given
@command(args=dict(file="path"))
def Remark(ctx, file):
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
