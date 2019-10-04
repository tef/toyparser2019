#!/usr/bin/env python3 

import os

from clgi import App, Bug, Error, Routes, command
from toyparser.remarkable.Remarkable import parse

class AppError(Error):
    pass

class cli:
    routes = Routes()
    errors = Routes()

    @errors.on(AppError)
    def app_error(request, code):
        args = request.args
        error_args, original_request = args['args'], args['request']
        code(-1)
        filename = error_args
        if filename:
            return ["app error: {}".format(filename)]

    @routes.on("convert") # no path given
    @command(args=dict(file="path"))
    def Remark(ctx, file):
        app = ctx['app']
        name = ctx['name']
        filename = os.path.relpath(file)
        with open(filename) as fh:
            dom = parse(fh.read())
            text = dom.to_html() 
        return [text]

    app = App(
        name="remark", 
        version="0.0.1",
        routes=routes,
        errors=errors,
        args={
        },
    )


# Generic exception handler here
cli.app.main(__name__)
