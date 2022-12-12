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
        self.state = None

    @classmethod
    def from_element(cls, element, count):
        n = element.get_arg('n')
        section = element.get_arg('section')
        name = element.get_arg('name')
        input_text = element.get_arg('input_text')
        output_dom = element.get_arg('output_dom')
        description = element.get_arg('description')
        
        if n is None:
            n = count
        if input_text is not None:
            if hasattr(input_text, 'text'):
                input_text = "\n".join(input_text.text)
        elif len(element.text) == 1 and getattr(element.text[0],'name', '') == dom.BulletList.name:
            for item in element.text[0].text:
                if getattr(item, 'name', '') in (dom.ItemSpan.name , dom.ItemBlock.name):
                    label = "".join(item.get_arg('label'))
                    if label == 'description':
                        if item.name == dom.ItemBlock.name:
                            description = item.text
                        elif item.name == dom.ItemSpan.name:
                            description = [dom.Paragraph([], item.text)]
                    elif label == 'input_text':
                        for codeblock in item.select(dom.CodeBlock.name):
                            if codeblock.get_arg('language') == 'remark':
                                input_text = "".join(codeblock.text)
                                break
                        else:
                            input_text = None
                    elif label == 'output_dom':
                        for codeblock in item.select(dom.CodeBlock.name):
                            if codeblock.get_arg('language') == 'rson':
                                output_dom = "".join(codeblock.text)
                                break
                        else:
                            output_dom = None

        elif len(element.text) >= 2:
            # todo: select codeblock, etc
            input_text, output_dom = element.text[:2]
            description = element.text[2:]

            if getattr(input_text, "name", "") == dom.CodeBlock.name and input_text.get_arg('language') == 'remark':
                input_text = "".join(input_text.text)
            else:
                input_text = None

            if getattr(output_dom, "name", "") == dom.CodeBlock.name and output_dom.get_arg('language') == 'rson':
                output_dom = "".join(output_dom.text)
            else:
                output_dom = None

        return cls(n, section, name, input_text, output_dom, description)

    def update_element(self, element):
        element.args.append(('state', self.state))
        element.args.append(('result_dom', self.result_dom))
        element.args.append(('number', self.n))

        state = dom.Strong((), self.state)

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
                            dom.ItemBlock((), [dom.Paragraph((), [dom.Strong((), ["Test", " ", "Case", " ",  "#", str(self.n), " ", "is", " ", state]) ]) ]),
                            dom.ItemBlock((), [dom.CodeBlock((), [repr(self.input_text)]) ]),
                            dom.ItemBlock((), [dom.CodeBlock((), brk(self.output_dom))]),
                        ])
                    ])
                ]),
        ]
        if self.description:
            rows.append(
                dom.Row((), [
                    dom.CellBlock((), self.description)
                ])
            )
        table = dom.Table( [ ('column_align', ['left']), ], rows)
        element.text = [table]

    def run(self):
        if self.skip():
            self.state = "skipped"
            return None

        try:
            result = self.test()
        except:
            raise
            self.state = "skipped"
            return None
        else:
            if result:
                self.state = "working"
            else:
                self.state = "failed"
            return self.state

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
    return doc.select(dom.TestCase.name)

def run_tests(doc):
    count = 1
    total = 0
    working = 0
    skipped = 0

    tests = list(find_tests(doc))

    for element in tests:
        test_case = TestCase.from_element(element, count)
        count = max(count, test_case.n) + 1
        total += 1

        if test_case.run():
            working +=1

        test_case.update_element(element)

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

