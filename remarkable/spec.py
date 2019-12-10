from . import dom, parser

def run_tests(doc):
    tests = list(doc.select(dom.TestCase.name))
    results = []
    success = []
    total = 0
    working = 0
    for n, test_case in enumerate(tests):
        total += 1
        if not test_case.text:
            raw_text = test_case.get_arg('input_text')
            if hasattr(raw_text, 'text'):
                raw_text = "\n".join(raw_text.text)
            output_dom = test_case.get_arg('output_dom')
        else:
            raw_text, output_dom = test_case.text[:2]
            test_case.text = test_case.text[2:]
            raw_text = "".join(raw_text.text)
        result_dom = parser.parse(raw_text)
        test_case.args.append(('result_dom', result_dom))
        test_case.args.append(('number', n))

        if result_dom == output_dom:
            state = "working"
            test_case.args.append( ('state', state))
            working+=1
        else:
            state = "failed"
            test_case.args.append( ('state', state))
            state = dom.Strong((), state)
        test_case.text = [ 
            dom.Table( [ ('align', ()), ], [
                dom.Row((), [
                    dom.CellSpan((), [dom.Strong((), ["Test", " ", "Case", " ",  "#", str(n)]) ]),
                    dom.CellSpan((), [dom.CodeSpan((), raw_text)]),
                    dom.CellSpan((), [dom.CodeSpan((), dom.dump(output_dom))]),
                    dom.CellSpan((), [state,]),
                ]),
            ])
        ] + test_case.text
    for r in doc.select(dom.TestReport.name):
        r.args.append(('total', total))
        r.args.append(('working', working))
        r.text += [ 
            dom.Table( [ ('align', ()), ], [
                dom.Row((), [
                    dom.CellSpan((), [ dom.Strong((), ["Test", " ", "Report:"]), ]),
                    dom.CellSpan((), ["Working:", " ", str(working)]),
                    dom.CellSpan((), ["Total:", " ", str(total)]),
                ]),
            ])
        ]

