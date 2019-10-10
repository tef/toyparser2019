class Response:
    pass

class Plaintext(Response):
    def __init__(self, lines):
        self.lines = []
        if isinstance(lines, str):
            lines = (lines,)
        for line in lines:
            self.lines.extend(line.splitlines())
    def render(self, width, height):
        return self.lines

class Document(Response):
    def __init__(self, obj):
        self.obj = obj
    def render(self, width, height):
        return self.obj.to_ansi(width=width, height=height)

