from .CommonMark import CommonMark, parse, builder
from ..grammar import sibling

def walk(node, indent="- "):
    if (node.value is not None):
        print(indent, node, node.value)
    else:
        print(indent, node)
    for child in node.children:
        walk(child, indent+ "  ")


def test_spec():
    print('grammar version', CommonMark.version)

    import json
    import os.path

    with open(sibling(__file__, "commonmark_0_29.json")) as fh:
        tests = json.load(fh)

    failed = 0
    worked = 0
    count =0

    for t in tests:
        markd = t['markdown']
        out1 = parse(markd)

        out = out1.build(markd, builder)
        count +=1
        if out == t['html']: 
            worked +=1
            #print(repr(markd))
            #print(repr(out))
        else:
            failed +=1
            print("example", t['example'])
            print(repr(markd))
            print('=', repr(t['html']))
            print('X', repr(out))
            print()
            #walk(out1)
            print()
    print(count, worked, failed)


if __name__ == "__main__":
    import time 
    test_spec()

    with open(sibling(__file__, "syntax.md")) as readme:
        test_case = readme.read()

    t = time.time()
    times = 10
    for i in range(times):
        out = parse(test_case).build(test_case,builder)
    t = time.time() -t 

    print(t, t/times)

    # from .CommonMarkParser import CommonMarkParser
    #t = time.time()
    #for i in range(times):
    #    out = CommonMarkParser().parse(test_case).build(test_case,builder)
    #t = time.time() -t 

    print(t, t/times)
    import commonmark

    t = time.time()
    for i in range(times):
        out = commonmark.commonmark(test_case)
    t = time.time() -t 

    print(t, t/times)

    #for name, value in CommonMark.rules.items():
    #    print(name, '<--', value,'.')
    #def markup(buf):
    #    parser = CommonMark.parser()
    #    node = parser.parse(buf)
    #    if node:
    #        print("test")
    #        for b in buf.splitlines():
    #            print(b)
    #        print()
    #        walk(node)
    #        print()
    #        print(node.build(buf, builder))



