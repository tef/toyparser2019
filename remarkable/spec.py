from . import dom, parser, rson

def run_tests(doc):
    tests = list(doc.select(dom.TestCase.name))
    results = []
    success = []
    total = 0
    working = 0
    skipped = 0
    for n, test_case in enumerate(tests):
        total += 1
        raw_text = test_case.get_arg('input_text')
        output_dom = test_case.get_arg('output_dom')
        if raw_text is not None:
            if hasattr(raw_text, 'text'):
                raw_text = "\n".join(raw_text.text)
        elif len(test_case.text) >= 2:
            # todo: select codeblock, etc
            raw_text, output_dom = test_case.text[:2]
            if getattr(raw_text, "name", "") != dom.CodeBlock.name or raw_text.get_arg('language') != 'remark':
                test_case.args.append(('state', 'skipped'))
                skipped+=1
                continue
            raw_text = "".join(raw_text.text)
            test_case.text = test_case.text[2:]
            if getattr(output_dom, "name", "") == dom.CodeBlock.name:
                if output_dom.get_arg('language') == 'rson':
                    output_dom = "".join(output_dom.text)
                    try:
                        output_dom = dom.parse(output_dom)
                    except:
                        print(output_dom)
                        raise
                if output_dom.get_arg('language') == 'remark':
                    output_dom = "".join(output_dom.text)
                    output_dom = parser.parse(output_dom)
        if raw_text is None: 
            test_case.args.append(('state', 'skipped'))
            skipped+=1
            continue

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
                            dom.ItemBlock((), [dom.Paragraph((), [dom.Strong((), ["Test", " ", "Case", " ",  "#", str(n), " ", "is", " ", state]) ]) ]),
                            dom.ItemBlock((), [dom.CodeBlock((), [repr(raw_text)]) ]),
                            dom.ItemBlock((), [dom.CodeBlock((), brk(dom.dump(output_dom)))]),
                        ])
                    ])
                ]),
        ]
        if test_case.text:
            rows.append(
                dom.Row((), [
                    dom.CellBlock((), test_case.text)
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

