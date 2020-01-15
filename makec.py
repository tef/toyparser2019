
class Metaclass(type):
    @classmethod
    def __prepare__(metacls, name, bases, **args):
        return {}

    def __new__(metacls, name, bases, attrs, **args):
        attrs["__args__"] = args
        return super().__new__(metacls, name, bases, attrs)


class Base(metaclass=Metaclass):
    pass


class Unit(Base):
    "A Translation unit"
    pass

class Function(Base):
    "A Function"

    def __call__(self, fn):
        return fn

class Static(Base):
    "A Static variable"

class Library(Base):
    "A external translation unit"

class Header(Base):
    "For icluding in other projects"

class Binary(Base):
    "An executable with an entry point"

class Project(Base):
    "A Collection of Units, that include Headers, that provides Libraries, Binaries"

    
class Stdio(Library):
    pass


from clgi.errors import Bug, Error
from clgi.app import App, Router, command, Plaintext, Document

class Build:
    router = Router()

    @router.on("make")
    @command(args={"target":"str*"})
    def Make(ctx, target):
        return Plaintext(f"targets: {','.join(target)}")

    app = App(name="makec", version="0", command=router, args={})

    @classmethod
    def run(self, name):
        self.app.main(name)
