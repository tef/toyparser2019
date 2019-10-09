#!/usr/bin/env python3 

import os

from clgi import App, Bug, Error, Router, command
from clgi.tty import Plaintext, Document
from toyparser.remarkable.Remarkable import parse

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

@router.on("convert") # no path given
@command(args=dict(file="path"))
def Remark(ctx, file):
    app = ctx['app']
    name = ctx['name']
    filename = os.path.relpath(file)
    with open(filename) as fh:
        dom = parse(fh.read())
        text = dom.to_html() 
    return Plaintext(text)

@router.on("view") # no path given
@command(args=dict(file="path"))
def Remark(ctx, file):
    app = ctx['app']
    name = ctx['name']
    filename = os.path.relpath(file)
    with open(filename) as fh:
        dom = parse(fh.read())
    return Document(dom)
app = App(
    name="remark", 
    version="0.0.1",
    command=router,
    args={ },
)



app.main(__name__)
