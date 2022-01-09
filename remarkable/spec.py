from . import dom, parser, rson

class TestCase:
    def __init__(self, n, section, name, input_text, output_dom, description):
        self.n = n
        self.section = section
        self.name = name
        self.input_text = input_text
        self.output_dom = output_dom
        self.description = description
        self.result_dom = None
        self.expected_dom = None

    def skip(self):
        return self.input_text is None or self.output_dom is None

    def test(self):
        try:
            self.result_dom = parser.parse(self.input_text)
        except:
            print('parse error on input {!r}'.format(self.input_text))
            raise
        try:
            self.expected_dom = dom.parse(self.output_dom)
        except:
            print('parse error on input {!r}'.format(self.output_dom))
            raise

        return (self.result_dom == self.expected_dom)

def find_tests(doc):
    tests = list(doc.select(dom.TestCase.name))

    count = 0

    for test_case in tests:
        n = test_case.get_arg('n')
        section = test_case.get_arg('section')
        name = test_case.get_arg('name')
        input_text = test_case.get_arg('input_text')
        output_dom = test_case.get_arg('output_dom')
        description = test_case.get_arg('description')
        
        if n is None:
            n = count
        if input_text is not None:
            if hasattr(input_text, 'text'):
                input_text = "\n".join(input_text.text)
        elif len(test_case.text) >= 2:
            # todo: select codeblock, etc
            input_text, output_dom = test_case.text[:2]
            description = test_case.text[2:]

            if getattr(input_text, "name", "") == dom.CodeBlock.name and input_text.get_arg('language') == 'remark':
                input_text = "".join(input_text.text)
            else:
                input_text = None

            if getattr(output_dom, "name", "") == dom.CodeBlock.name and output_dom.get_arg('language') == 'rson':
                output_dom = "".join(output_dom.text)
            else:
                output_dom = None

        yield test_case, TestCase(n, section, name, input_text, output_dom, description)
        count = max(count, n) + 1

def run_tests(doc):
    tests = list(find_tests(doc))
    results = []
    success = []
    total = 0
    working = 0
    skipped = 0
    for element, test_case in tests:
        total += 1
        if test_case.skip():
            skipped+=1
            element.args.append(('state', 'skipped'))
            continue

        try:
            result = test_case.test()
        except:
            print(f"skipped {test_case.n}, {test_case.description}, {test_case.output_dom}")
            skipped+=1
            element.args.append(('state', 'skipped'))
            continue

        element.args.append(('result_dom', test_case.result_dom))
        element.args.append(('number', test_case.n))

        if result:
            state = "working"
            working +=1
        else:
            state = "failed"

        element.args.append(('state', state))
        state = dom.Strong((), state)

        def brk(s):
            o = []
            while True:
                x = s.split(' ', 1)
                if len(x) <2:
                    o.append(x[0])
                    break
                else:
                    if x[0]:
                        o.append(x[0])
                    o.append(' ')
                    s= x[1]
            return o

        rows = [
                dom.Row((), [
                    dom.CellBlock((), [
                        dom.BulletList( [('bullet', '')], [
                            dom.ItemBlock((), [dom.Paragraph((), [dom.Strong((), ["Test", " ", "Case", " ",  "#", str(test_case.n), " ", "is", " ", state]) ]) ]),
                            dom.ItemBlock((), [dom.CodeBlock((), [repr(test_case.input_text)]) ]),
                            dom.ItemBlock((), [dom.CodeBlock((), brk(test_case.output_dom))]),
                        ])
                    ])
                ]),
        ]
        if test_case.description:
            rows.append(
                dom.Row((), [
                    dom.CellBlock((), test_case.description)
                ])
            )
        table = dom.Table( [ ('column_align', ['left']), ], rows)
        test_case.text = [table]
    for r in doc.select(dom.TestReport.name):
        r.args.append(('total', total))
        r.args.append(('working', working))
        r.args.append(('skipped', skipped))
        r.text += [ 
            dom.Table( [ ('align', ()), ], [
                dom.Row((), [
                    dom.CellSpan((), [ dom.Strong((), ["Test", " ", "Report:"]), ]),
                    dom.CellSpan((), ["Working:", " ", str(working)]),
                    dom.CellSpan((), ["Skipped:", " ", str(skipped)]),
                    dom.CellSpan((), ["Total:", " ", str(total)]),
                ]),
            ])
        ]

