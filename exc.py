from makec import Unit, Function, Static, Binary, Project
from makec import Stdio
from makec import Build


class Hello(Unit, include=[Stdio]):
    @Function()
    def main(self, args, locals, heap):
        self.printf("Hello, World\n")


class HelloWorld(Binary):
    include = [Hello]
    main = Hello.main
    name = "hello"

class Example(Project):
    export = [HelloWorld]

Build.run(__name__)


