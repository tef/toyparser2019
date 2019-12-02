from . import dom, parser

def run_tests(doc):
    tests = list(doc.select(dom.TestCase.name))
    results = []
    success = []
    total = 0
    working = 0
    for n, test_case in enumerate(tests):
        total += 1
        raw_text = test_case.get_arg('input_text')
        output_dom = test_case.get_arg('output_dom')
        result_dom = parser.parse(raw_text)

        if result_dom == output_dom:
            state = "working"
            working+=1
        else:
            state = "failed"
        test_case.args.append( ('state', state))
        test_case.args.append(('number', n))
        test_case.text = [ 
            dom.Table( [ ('align', ()), ], [
                dom.Row((), [
                    dom.CellSpan((), [dom.Strong((), ["Test", " ", "Case", " ",  "#", str(n)]) ]),
                    dom.CellSpan((), [dom.CodeSpan((), raw_text)]),
                    dom.CellSpan((), [dom.CodeSpan((), dom.dump(output_dom))]),
                    dom.CellSpan((), [state,]),
                ]),
            ])
        ]
    for r in doc.select(dom.TestReport.name):
        r.args.append(('total', total))
        r.args.append(('working', working))
        r.text = [ 
            dom.Table( [ ('align', ()), ], [
                dom.Row((), [
                    dom.CellSpan((), [ dom.Strong((), ["Test", " ", "Report:"]), ]),
                    dom.CellSpan((), ["Working:", " ", str(working)]),
                    dom.CellSpan((), ["Total:", " ", str(total)]),
                ]),
            ])
        ]

