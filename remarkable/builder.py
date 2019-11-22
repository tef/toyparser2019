import base64, codecs
from datetime import datetime, timedelta, timezone
from . import dom

def unescape(string):
    return codecs.decode(string.replace('\\/', '/'), 'unicode_escape')

def parse_datetime(v):
    if v[-1] == 'Z':
        if '.' in v:
            return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        else:
            return datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    else:
        raise NotImplementedError()

bools = {'false': False, 'true':True}

def builder(buf, node, children):
    kind = node.name
    if kind == "value":
        return node.value

    if kind == "document":
        text = []
        metadata = None
        for c in children:
            if c is None: continue
            if metadata is None and getattr(c, "name", "") == "metadata":
                metadata = c.args
                continue
            text.append(c)

        metadata = metadata or [('title', '')]

        if len(text) == 1 and getattr(text[0], "name", "") == "document":
            return text[0]
        return dom.Document(metadata, text)

    if kind == 'identifier':
        return buf[node.start:node.end]
    if kind == "text":
        return buf[node.start:node.end]
    if kind == "nbsp":
        return dom.Nbsp()
    if kind == "whitespace":
        if node.end == node.start:
            return None
        return " "

    if kind == "softbreak":
        return dom.Softbreak()
    if kind == "hardbreak":
        return dom.Hardbreak()

    if kind in ('empty', 'empty_line'):
        return None

    if kind == "emoji":
        return dom.Emoji((), [c for c in children if c is not None])


    if kind == 'horizontal_rule':
        return dom.HorizontalRule(children[0], ())
    if kind == 'atx_heading':
        args = [('level', node.value)] + children[0]
        return dom.Heading(args, [c for c in children[1:] if c is not None])

    if kind == "paragraph":
        return dom.Paragraph([], [c for c in children if c is not None])
    if kind == "span":
        args = children[-1]
        marker = node.value
        if marker == "*":
            return dom.Strong(args,[c for c in children[:-1] if c is not None])
        if marker == "_":
            return dom.Emphasis(args,[c for c in children[:-1] if c is not None])
        if marker == "~":
            return dom.Strike(args,[c for c in children[:-1] if c is not None])
        if marker:
            return dom.Span([("marker", node.value)] +args,[c for c in children[:-1] if c is not None])
        return dom.Span(args,[c for c in children[:-1] if c is not None])
    if kind == 'code_span':
        args = children[-1]
        return dom.CodeSpan(args, [c for c in children[:-1] if c is not None])

    if kind == 'code_block':
        arg = children[0] if children[0] is not None else []
        return dom.CodeBlock(arg, [c for c in children[1:] if c is not None])
    if kind == "code_string":
        return [("language", children)]
    if kind == 'blockquote':
        return dom.QuoteBlock(children[0], children[1:])
        
    if kind == 'group':
        marker = children[0]
        spacing = children[1]
        name = 'group'
        args = [("marker", marker)]

        block = dom.GroupBlock

        if spacing == "tight":
            if all(c and c.name == "item_span" for c in children[2:]):
                return dom.ListBlock([], [c for c in children[2:] if c is not None])

        new_children = []
        for c in children[2:]:
            if c is None: continue
            if c.name == 'item_span':
                text = [dom.Paragraph([], c.text)] if c.text else []
                c = dom.ItemBlock(c.args, text)
            new_children.append(c)
        return dom.ListBlock([], new_children)

        return dom.GroupBlock(args, new_children)
    if kind == 'group_marker':
        return buf[node.start:node.end]
    if kind == 'group_spacing':
        return node.value
    if kind == 'item':
        spacing = children[1]
        if spacing == "tight":
            if not children[2:]:
                return dom.ItemSpan(children[0], [])
            elif len(children) == 3 and children[2].name == "para" and not children[2].args:
                return dom.ItemSpan(children[0], children[2].text)
            else:
                return dom.ItemBlock(children[0], [c for c in children[2:] if c is not None])

        return dom.ItemBlock(children[0], [c for c in children[2:] if c is not None])
    if kind == 'item_spacing':
        return node.value

    if kind == "block_directive":
        name = children[0]
        args = children[1]
        text = children[2] 
        if text:
            if name == 'list' and text.name == "directive_group":
                args = args + text.args # pull up spacing
                return dom.ListBlock(args, text.text)
            if name == 'blockquote' and text.name == "directive_quote":
                return dom.QuoteBlock(args, text.text)
            if name == 'blockquote' and text.name == "directive_group":
                new_children = []
                for c in children[2:]:
                    if c is None:
                        continue
                    elif c.name == 'item_span':
                        new_children.append(dom.Paragraph(c.args, c.text))
                    elif c.name == "block_item":
                        new_children.extend(c.text)
                    else:
                        new_children.append(c)
                return dom.QuoteBlock(args, new_children)

            if name == 'table' and text.name == "directive_group":
                new_text = []
                def transform_row(r):
                    if r.name == 'item_span':
                        return transform_cols(r, r.text)
                    if r.name == 'block_item':
                        return transform_cols(r, r.text)
                    else:
                        return r

                def transform_cols(name, d):
                    if len(d) == 1 and d[0].name in ('para_group', 'group', 'blocklist', 'blockquote'):
                        if all( len(e.text) == 1 and getattr(e.text[0],'name', '') == 'heading' for e in d[0].text):
                            return dom.HeaderRow([], [dom.Cell([], t.text[0].text) for t in d[0].text])

                        return dom.Row([], [(dom.CellBlock([], t.text) if t.name =='block_item' else dom.Cell([], t.text)) for t in d[0].text])
                    elif all(getattr(t,'name', '') == 'heading' for t in d):
                        return dom.HeaderRow([], [Cell([], t.text) for t in d])

                    return name
                    
                text = [transform_row(r) for r in text.text]
                return dom.Table(args, text)
            if name == 'table' and text.name == "directive_table":
                return dom.Table(args, text.text)

            if text.name == 'directive_group':
                text = [dom.GroupBlock(text.args, text.text)]
            elif text.name == 'directive_table':
                text = [dom.Table(text.args, text.text)]
            elif text.name == 'directive_quote':
                text = text.text
            elif text.name == 'directive_block':
                text = text.text
            elif text.name == 'directive_para': 
                text = text.text if name in dom.para_directives else [dom.Paragraph([], text.text)]
            elif text.name == 'directive_code':
                text = text.text if name in dom.para_directives else [dom.CodeBlock([], text.text)]
            else:
                raise Exception('no')
        else:
            text = []

        if name in dom.para_directives:
            return dom.para_directives[name](args, text)
        elif name in dom.block_directives:
            return dom.block_directives[name](args, text)
        else:
            return dom.NamedBlockDirective([('name', name)] + args, text)

    if kind == "inline_directive":
        name = children[0]
        if name == 'code':
            name == 'code_span'
        args = children[1]
        text = [children[2]] if children[2:] and children[2] is not None else []
        if text:
            text = text[0].text
        if name in dom.inline_directives:
            return dom.inline_directives[name](args, text)
        return dom.NamedInlineDirective([('name', name)]+ args, text)
    if kind == "arg":
        return children
    if kind == "directive_args":
        return children
    if kind == "directive_name":
        return buf[node.start:node.end]

    if kind == "directive_span":
        return dom.Inline('directive_span',[],[c for c in children if c is not None])

    if kind == "directive_para":
        return dom.Block('directive_para',[],[c for c in children if c is not None])
    if kind == "directive_code":
        return dom.Block('directive_code',[],[c for c in children if c is not None])
    if kind == "directive_code_span":
        return dom.Block('directive_code',[],[c for c in children if c is not None])
    if kind == "directive_table":
        return dom.Block('directive_table',[],[c for c in children if c is not None])
    if kind == "directive_block":
        return dom.Block('directive_block',[],[c for c in children if c is not None])
    if kind == "directive_quote":
        return dom.Block('directive_quote',children[0],[c for c in children[1:] if c is not None])
    if kind == "directive_group":
        marker = children[0]
        spacing = children[1]
        return dom.Block("directive_group", [("marker", marker), ("spacing", spacing)], [c for c in children[2:] if c is not None])

    if kind == "table":
        text = []
        args = []
        for c in children:
            if c is None: continue
            if getattr(c, 'name', '') == "table_heading_rule":
                args.append(('column_align', c.text))
            else:
                text.append(c)
        return dom.Table(args,text)
        
    if kind == "table_cell":
        return dom.Cell([], children)
    if kind == "column_align":
        left = buf[node.start] == ":"
        right = buf[node.end-1] == ":"
        if left and right: return "center"
        if right: return "right"
        if left: return "left"
        return "default"
    if kind == "table_row":
        return dom.Row([], children)
    if kind == "table_heading":
        return dom.HeaderRow([], children)
    if kind == "table_heading_rule":
        return dom.Block('table_heading_rule', [], children)

    if kind == 'block_rson':
        # can't take raw rson, must be a data node!
        args = children[1]
        text = args.pop('text') if 'text' in args else []
        args = list(args.items())
        return dom.Data(children[0], args, text)

    if kind == 'rson_number': 
        return eval(buf[node.start:node.end])
    if kind == 'rson_string': 
        return unescape(buf[node.start:node.end])
    if kind == 'rson_list': 
        return children
    if kind == 'rson_object': 
        return dict(children)
    if kind == 'rson_pair':
        return children
    if kind =='rson_bool': 
        return bools[buf[node.start:node.end]]
    if kind == 'rson_null': 
        return None
    if kind == "rson_tagged":
        identifier, literal = children
        if identifier == "object":
           return literal
        if identifier == "record" or identifier == "dict":
            if not isinstance(literal, dict): raise Exception('bad')
            return literal
        elif identifier == "list":
            if not isinstance(literal, list): raise Exception('bad')
            return literal
        elif identifier == "string":
            if not isinstance(literal, str): raise Exception('bad')
            return literal
        elif identifier == "bool":
            if not isinstance(literal, bool): raise Exception('bad')
            return literal
        elif identifier == "int":
            if not isinstance(literal, int): raise Exception('bad')
            return literal
        elif identifier == "float":
            if isinstance(literal, float): return literal
            if not isinstance(literal, str): raise Exception('bad')
            return float.fromhex(literal)
        elif identifier == "set":
            if not isinstance(literal, list): raise Exception('bad')
            return set(literal)
        elif identifier == "complex":
            if not isinstance(literal, list): raise Exception('bad')
            return complex(*literal)
        elif identifier == "bytestring":
            if not isinstance(literal, str): raise Exception('bad')
            return literal.encode('ascii')
        elif identifier == "base64":
            if not isinstance(literal, str): raise Exception('bad')
            return base64.standard_b64decode(literal)
        elif identifier == "datetime":
            if not isinstance(literal, str): raise Exception('bad')
            return parse_datetime(literal)
        elif identifier == "duration":
            if not isinstance(literal, (int, float)): raise Exception('bad')
            return timedelta(seconds=literal)
        elif identifier == "unknown":
            raise Exception('bad')
        return dom.tagged_to_object(identifier, literal)
    raise Exception(node.name)
    return {node.name: children}

