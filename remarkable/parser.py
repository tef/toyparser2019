import base64, codecs
from datetime import datetime, timedelta, timezone

from toyparser.remarkable.Remarkable import Remarkable
from toyparser.commonmark.CommonMark import parse as commonmark_parser
from . import dom

parser = Remarkable().parser()

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

def trim_whitespace(children):
    out = []
    for node in children:
        if node is None:
            pass
        elif isinstance(node, str):
            out.append(node)
        elif node.name == dom.Whitespace.name:
            out.append(" ")
        else:
            node.text = trim_whitespace(node.text)
            out.append(node)
    if len(out) > 1 and out[0] == " ":
        out.pop(0)
    if len(out) > 1 and out[-1] == " ":
        out.pop()
    return out

def builder(buf, node, children):
    kind = node.name
    if kind == "value":
        return node.value

    if kind == "remark_document":
        if len(children) == 1 and getattr(children[0], "name", "") in (dom.Document.name, dom.Fragment.name):
            return children[0]
        if len(children) == 1 and getattr(children[0], "name", "") in (dom.NamedInlineDirective.name, dom.NamedBlockDirective.name):
            if children[0].get_arg("name") == "document":
                return dom.Document(children[0].args[1:], children[0].text)
            if children[0].get_arg("name") == "fragment":
                return dom.Fragment(children[0].args[1:], children[0].text)

        text = []
        metadata = None
        for c in children:
            if c is None: continue
            if metadata is None and getattr(c, "name", "") == dom.Metadata.name:
                if c.text:
                    if c.text[0] and getattr(c.text[0], "name", "") == dom.BulletList.name:
                        out = []
                        for item in c.text[0].text:
                            out.append((
                                        " ".join(item.get_arg('label')),
                                        " ".join(item.text)
                            ))
                        metadata = out
                        continue
                    else:
                        raise NotImplementedError('unhandled metadata block')
                else:
                    metadata = c.args
                    continue
            text.append(c)

        if metadata is None:
            if len(children) == 1 and isinstance(children[0], dom.Node):
                return children[0]
            return dom.Fragment([], text)
        else:
            return dom.Document(metadata, text)
    if kind == 'remark_codepoint':
        return dom.Codepoint([('n', int(buf[node.start:node.end]))], [])
    if kind == 'remark_hex_codepoint':
        return dom.Codepoint([('n', int(buf[node.start:node.end], 16))], [])

    if kind == 'remark_identifier':
        return buf[node.start:node.end]
    if kind == "code_text":
        return buf[node.start:node.end]
    if kind == "code_whitespace":
        return " "*(node.end_column-node.start_column)
    if kind == "remark_text":
        return buf[node.start:node.end]
    if kind == "remark_nbsp":
        return dom.Nbsp([],[ buf[node.start:node.end]])
    if kind == "remark_whitespace":
        if node.end == node.start:
            return None
        text = buf[node.start:node.end]
        if text == " ": return text
        text = " "*(node.end_column-node.start_column)
        return dom.Whitespace((), [text])

    if kind == "remark_softbreak":
        return dom.Softbreak([], [buf[node.start:node.end]])
    if kind in ("remark_prose_hardbreak", "remark_hardbreak"):
        return dom.Hardbreak([],[buf[node.start:node.end]])

    if kind in ('remark_empty_line',):
        return None

    if kind == "remark_emoji":
        name = "".join(c for c in children if c is not None)
        return dom.Emoji([('name', name),], [])


    if kind == 'remark_horizontal_rule':
        return dom.HorizontalRule(children[0], ())
    if kind == 'remark_heading':
        args = [('level', node.value)] + children[0]
        return dom.Heading(args, trim_whitespace(children[1:]))

    if kind == "remark_paragraph":
        return dom.Paragraph([], trim_whitespace(children))
    if kind == "remark_prose_paragraph":
        return dom.Prose(children[0], [c for c in children[1:] if c is not None])
    if kind == "remark_inline_span":
        return dom.Span(children[-1], trim_whitespace(children[:-1]))
    if kind == "remark_paragraph_span":
        marker = node.value
        if marker == "*":
            return dom.Strong(children[-1], trim_whitespace(children[:-1]))
        if marker == "_":
            return dom.Emphasis(children[-1], trim_whitespace(children[:-1]))
            return dom.Emphasis(args,[c for c in children[:-1] if c is not None])
        if marker == "~":
            return dom.Strikethrough(children[-1], trim_whitespace(children[:-1]))
        if marker:
            return dom.Span( [("marker", node.value)] + children[-1], trim_whitespace(children[:-1]))
        return dom.Span(children[-1], trim_whitespace(children[:-1]))
    if kind == 'remark_code_span':
        args = children[-1]
        return dom.CodeSpan(args, [c for c in children[:-1] if c is not None])

    if kind == 'remark_code_block':
        arg = children[0] if children[0] is not None else []
        return dom.CodeBlock(arg, [c for c in children[1:] if c is not None])
    if kind == "code_string":
        return [("language", children[0])]
    if kind == 'remark_blockquote':
        return dom.Blockquote(children[0], children[1:])
        
    if kind == 'remark_definition_list':
        return dom.DefinitionList([], children)
    if kind == 'remark_definition_label':
        return dom.ItemLabel(children[-1], trim_whitespace(children[:-1]))
    if kind == 'remark_definition_block':
        return dom.ItemBlock([], children)

    if kind == 'remark_label_span':
        return children
    if kind == 'remark_item_label':
        return dom.ItemLabel(children[1], trim_whitespace(children[0]))
    if kind == 'remark_list':
        marker = children[0]
        spacing = children[1]
        items = children[2:] # don't remove labels
        args = [("marker", marker)]

        if spacing == "tight":
            if all(c and c.name == dom.ItemSpan.name for c in items):
                return dom.BulletList([], [c for c in items if c is not None])

        new_children = []
        for c in children[2:]:
            if c is None: continue
            if c.name == dom.ItemSpan.name:
                text = [dom.Paragraph([], c.text)] if c.text else []
                c = dom.ItemBlock(c.args, text)
            new_children.append(c)
        return dom.BulletList([], new_children)

    if kind == 'item_marker':
        return buf[node.start:node.end]
    if kind == 'list_spacing':
        return node.value
    if kind == 'item_spacing':
        return node.value
    if kind == 'remark_item':
        args = children[0].args + [("label", children[0].text,)]
        spacing = children[1]
        text = children[2:]
        if spacing == "tight":
            if not text:
                return dom.ItemSpan(args, [])
            elif len(text) == 1 and text[0].name == dom.Paragraph.name and not text[0].args:
                return dom.ItemSpan(args, trim_whitespace(text[0].text))
            else:
                return dom.ItemBlock(args, [c for c in text if c is not None])

        return dom.ItemBlock(args, [c for c in text if c is not None])

    if kind == "directive_fragment":
        if not children[1].text:
            return children[0]
        child = children[0]
        text = []

        if child.name == 'directive_list':
            spacing = child.get_arg('spacing')
            if spacing == "tight" and all(c and c.name == dom.ItemSpan.name for c in child.text):
                    text.append(dom.BulletList([], child.text))
            else:
                new_children = []
                for c in child.text:
                    if c is None: continue
                    if c.name == dom.ItemSpan.name:
                        text = [dom.Paragraph([], c.text)] if c.text else []
                        c = dom.ItemBlock(c.args, text)
                    new_children.append(c)
                text.append(dom.BulletList([], new_children))
        elif child.name == 'directive_table':
            text.append(dom.Table(child.args, child.text))
        elif child.name == 'directive_quote':
            text.append(dom.Blockquote([], text.text))
        elif child.name == 'directive_para': 
            text.append(dom.Paragraph([], child.text))
        elif child.name == 'directive_prose': 
            text.append(dom.Prose([], child.text))
        elif child.name == 'directive_block':
            text.extend(child.text)
        text.extend(children[1].text)
        return dom.DirectiveNode('directive_block',[], text)

    if kind == "block_directive":
        name = children[0]
        args = children[1]
        text = children[2] 
        if text:
            if name == 'todo' and text.name == "directive_list":
                spacing = text.get_arg('spacing')
                if spacing == "tight":
                    if all(c and c.name == dom.ItemSpan.name for c in text.text):
                        new_children = []
                        for c in text.text:
                            done = False
                            args = []
                            for k,v in c.args:
                                if k == "label":
                                    if v == ["x"]:
                                        done = True
                                else:
                                    args.append((k,v))
                            args.append(("done", done))
                            new_children.append(dom.ItemSpan(args, c.text))
                        return dom.TodoList(args, new_children)

                new_children = []
                for c in text.text:
                    if c is None: continue
                    if c.name == dom.ItemSpan.name:
                        t = [dom.Paragraph([], c.text)] if c.text else []
                        args = []
                        done = False
                        for k,v in c.args:
                            if k == "label":
                                if v == ["x"]:
                                    done = True
                            else:
                                args.append((k,v))
                        args.append(("done", done))
                        c = dom.ItemBlock(args, t)
                    else:
                        args = []
                        done = False
                        for k,v in c.args:
                            if k == "label":
                                if v == ["x"]:
                                    done = True
                            else:
                                args.append((k,v))
                        args.append(("done", done))
                        c = dom.ItemBlock(args, c.text)
                    new_children.append(c)
                return dom.TodoList(args, new_children)

            if name == 'list' and text.name == "directive_definition_list":
                return dom.DefinitionList(args, text.text)
            if name == 'list' and text.name == "directive_list":
                spacing = text.get_arg('spacing')
                if spacing == "tight":
                    if all(c and c.name == dom.ItemSpan.name for c in text.text):
                        return dom.list_directive(args, text.text)

                new_children = []
                for c in text.text:
                    if c is None: continue
                    if c.name == dom.ItemSpan.name:
                        t = [dom.Paragraph([], c.text)] if c.text else []
                        c = dom.ItemBlock(c.args, t)
                    new_children.append(c)
                return dom.list_directive(args, new_children)
            if name == 'blockquote' and text.name == "directive_quote":
                return dom.Blockquote(args, text.text)
            if name == 'blockquote' and text.name == "directive_list":
                new_children = []
                for c in children[2:]:
                    if c is None:
                        continue
                    elif c.name == dom.ItemSpan.name:
                        new_children.append(dom.Paragraph(c.args, c.text))
                    elif c.name == dom.ItemBlock.name:
                        new_children.extend(c.text)
                    else:
                        new_children.append(c)
                return dom.Blockquote(args, new_children)

            if name == 'table' and text.name == "directive_list":
                new_text = []
                def transform_row(r):
                    if r.name == dom.ItemSpan.name:
                        return transform_cols(r, r.text)
                    if r.name == dom.ItemBlock.name:
                        return transform_cols(r, r.text)
                    else:
                        return r

                def transform_cols(name, d):
                    if len(d) == 1 and d[0].name == dom.BulletList.name:
                        if all( len(e.text) == 1 and getattr(e.text[0],'name', '') == dom.Heading.name for e in d[0].text):
                            return dom.TableHeader([], [dom.CellSpan([], t.text[0].text) for t in d[0].text])

                        return dom.Row([], [(dom.CellBlock([], t.text) if t.name == dom.ItemBlock.name else dom.CellSpan([], t.text)) for t in d[0].text])
                    elif all(getattr(t,'name', '') == dom.Heading.name for t in d):
                        return dom.TableHeader([], [dom.CellSpan([], t.text) for t in d])

                    return name
                    
                text = [transform_row(r) for r in text.text]
                return dom.Table(args, text)
            if name == 'table' and text.name == "directive_table":
                return dom.Table(args, text.text)

            if text.name == 'directive_list':
                text = [dom.BulletList(text.args, text.text)]
            elif text.name == 'directive_table':
                text = [dom.Table(text.args, text.text)]
            elif text.name == 'directive_quote':
                text = text.text
            elif text.name == 'directive_block':
                text = text.text
            elif text.name == 'directive_para': 
                text = text.text if name in dom.para_directives else [dom.Paragraph([], text.text)]
            elif text.name == 'directive_prose': 
                text = text.text if name in dom.para_directives else [dom.Prose(args, text.text)]
            elif text.name == 'directive_code':
                text = text.text if name in dom.para_directives else [dom.CodeBlock([], text.text)]
            elif text.name == 'directive_definition_list':
                text = [dom.DefinitionList(text.args, text.text)]
            else:
                raise Exception('no')
        else:
            text = []

        return dom.named_block_directive(name, args, text)
    if kind == "raw_block_directive":
        name = children[0]
        args = children[1] if len(children) > 2 else []
        text = children[2] if len(children) > 1 else []
        args = [('name', name)] + args

        return dom.RawBlock(args, text.text)
    if kind == "raw_inline_directive":
        name = children[0]
        text = children[1] if len(children) > 1 else []
        args = children[2] if len(children) > 2 else []
        if text is not None:
            text = text.text
        args = [('name', name)] + args

        return dom.RawSpan(args, text)

    if kind == "inline_directive":
        name = children[0]
        text = children[1] if len(children) > 1 else []
        args = children[2] if len(children) > 2 else []
        if text is not None:
            text = text.text

        return dom.named_inline_directive(name, args, text)
    if kind == "arg":
        return children
    if kind == "directive_args":
        return children
    if kind == "directive_name":
        return buf[node.start:node.end]

    if kind == "directive_span":
        return dom.DirectiveNode('directive_span',[],[c for c in children if c is not None])

    if kind == "directive_para":
        return dom.DirectiveNode('directive_para',[],trim_whitespace(children))
    if kind == "directive_code":
        return dom.DirectiveNode('directive_code',[],[c for c in children if c is not None])
    if kind == "directive_code_span":
        return dom.DirectiveNode('directive_code',[],[c for c in children if c is not None])
    if kind == "directive_table":
        return dom.DirectiveNode('directive_table',[],[c for c in children if c is not None])
    if kind == "directive_block":
        return dom.DirectiveNode('directive_block',[],[c for c in children if c is not None])
    if kind == "directive_quote":
        return dom.DirectiveNode('directive_quote',children[0],[c for c in children[1:] if c is not None])
    if kind == "directive_definition_list":
        return dom.DirectiveNode('directive_definition_list',[],[c for c in children if c is not None])
    if kind == "directive_list":
        marker = children[0]
        spacing = children[1]
        items = children[2:] # don't remove labels
        return dom.DirectiveNode("directive_list", [("marker", marker), ("spacing", spacing)], [c for c in items if c is not None])

    if kind == "table":
        text = []
        args = []
        for c in children:
            if c is None: continue
            if getattr(c, 'name', '') ==  dom.TableRule.name:
                args.append(('column_align', c.text))
            else:
                text.append(c)
        return dom.Table(args,text)
        
    if kind == "table_cell":
        return dom.CellSpan([], trim_whitespace(children))
    if kind == "column_align":
        left = buf[node.start] == ":"
        right = buf[node.end-1] == ":"
        if left and right: return "center"
        if right: return "right"
        if left: return "left"
        return "default"
    if kind == "table_row":
        return dom.Row([], children)
    if kind == "table_header":
        return dom.TableHeader([], children)
    if kind == "table_header_rule":
        return dom.TableRule([], children)

    if kind == 'block_rson':
        # can't take raw rson, must be a data node!
        name = children[0]
        args = children[1]
        return dom.named_rson_block(name, args)
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

def commonmark_builder(buf, node, children):
    kind = node.name
    if kind == "value":
        return node.value

    if kind == "document":
        # todo: yaml metadata promotes to document
        text = []
        metadata = None
        for c in children:
            if c is None: continue
            if metadata is None and getattr(c, "name", "").lower() == "metadata":
                # todo, parse yaml
                metadata = c.args
                continue
            text.append(c)

        if metadata is None:
            return dom.Fragment([], text)
        else:
            return dom.Document(metadata, text)

    if kind == 'yaml_metadata_block':
        return dom.Metadata((), [buf[node.start:node.end]])

    if kind == "operator":
        return buf[node.start:node.end]
    if kind == "text":
        return buf[node.start:node.end]
    if kind == "raw":
        return buf[node.start:node.end]
    if kind == "html_comment":
        return ""
    if kind == "whitespace":
        if node.end == node.start:
            return None
        text = buf[node.start:node.end]
        if text == " ": return text
        return dom.Whitespace((), [text])

    if kind == "softbreak":
        return dom.Softbreak([], [buf[node.start:node.end]])
    if kind == "hardbreak":
        return dom.Hardbreak([], [buf[node.start:node.end]])


    if kind in ('empty', 'empty_line',):
        return None

    # emoji
    if kind == "emoji":
        name = "".join(c for c in children if c is not None)
        return dom.Emoji([('name', name),], [])


    if kind == 'thematic_break':
        return dom.HorizontalRule((), ())
    def trim_whitespace(node):
        if isinstance(node, str):
            return node
        if node.name == dom.Whitespace.name:
            return " "
        node.text = [trim_whitespace(n) for n in node.text if n is not None]
        return node
    if kind == 'atx_heading' or kind == 'setext':
        args = [('level', node.value)] 
        return dom.Heading(args, [trim_whitespace(c) for c in children if c is not None])

    if kind == "para":
        return dom.Paragraph([], [trim_whitespace(c) for c in children if c is not None])

    if kind == "indented_code":
        return dom.CodeBlock([], [c for c in children if c is not None])
    if kind == "partial_indent":
        return " "*(node.end_column-node.start_column)
    if kind == "indented_code_line":
        return buf[node.start:node.end] +"\n"
    if kind == "fenced_code":
        args =  [("language", children[0])]
        return dom.CodeBlock(args, [c for c in children[1:] if c is not None])
    if kind == "info":
        text = "".join(children)
        text = text.lstrip().split(' ',1)
        if text: return text[0]
        return None

    if kind == 'code_span':
        args = []
        return dom.CodeSpan(args, [c for c in children[:-1] if c is not None])


    if kind == 'blockquote':
        return dom.Blockquote([], [c for c in children if c is not None])
    if kind == 'unordered_list':
        if node.value == "loose":
            pass
        else:
            pass
        return None

    if kind == 'ordered_list':
        return None

    if kind == 'ordered_list_start':
        return int(buf[node.start:node.end])
    if kind == 'list_item':
        return None

    if kind == 'html_block':
        args = [('language', 'html')]
        return dom.RawBlock(args, buf[node.start:node.end])

    if kind == 'link_def' or kind == 'link_name':
        return None # todo

    if kind == 'image':
        return None

    if kind == 'link':
        return None

    if kind == 'link_para':
        return None
    if kind == 'link_label':
        return None
    if kind == 'link_url':
        return None
    if kind == 'link_title':
        return None

    if kind == 'raw_entity': #inside links
        if node.value == 'named':
            return None
        elif node.value == 'hex':
            return None
        elif node.value == 'decimal':
            return None

    if kind == 'html_entity': 
        if node.value == 'named':
            return None
        elif node.value == 'hex':
            return None
        elif node.value == 'decimal':
            return None

    if kind in ('left_flank', 'right_flank', 'dual_flank'):
        return node.value
    
    if kind == 'auto_link':
        return None
    if kind == 'mailto_auto_link':
        return None

    if kind == "table":
        text = []
        args = []
        for c in children:
            if c is None: continue
            if getattr(c, 'name', '') ==  dom.TableRule.name:
                args.append(('column_align', c.text))
            else:
                text.append(c)
        return dom.Table(args,text)
        
    if kind == "table_cell":
        return dom.CellSpan([], [trim_whitespace(c) for c in children if c is not None])
    if kind == "column_align":
        left = buf[node.start] == ":"
        right = buf[node.end-1] == ":"
        if left and right: return "center"
        if right: return "right"
        if left: return "left"
        return "default"
    if kind == "table_row":
        return dom.Row([], children)
    if kind == "table_header":
        return dom.TableHeader([], children)
    if kind == "table_header_rule":
        return dom.TableRule([], children)

    # cruft

    if kind == "remark_paragraph_span":
        args = children[-1]
        marker = node.value
        if marker == "*":
            return dom.Strong(args,[c for c in children[:-1] if c is not None])
        if marker == "_":
            return dom.Emphasis(args,[c for c in children[:-1] if c is not None])
        if marker == "~":
            return dom.Strikethrough(args,[c for c in children[:-1] if c is not None])
        if marker:
            return dom.Span([("marker", node.value)] +args,[c for c in children[:-1] if c is not None])
        return dom.Span(args,[c for c in children[:-1] if c is not None])

        
    if kind == 'remark_list':
        marker = children[0]
        spacing = children[1]
        args = [("marker", marker)]

        if spacing == "tight":
            if all(c and c.name == dom.ItemSpan.name for c in children[2:]):
                return dom.BulletList([], [c for c in children[2:] if c is not None])

        new_children = []
        for c in children[2:]:
            if c is None: continue
            if c.name == dom.ItemSpan.name:
                text = [dom.Paragraph([], c.text)] if c.text else []
                c = dom.ItemBlock(c.args, text)
            new_children.append(c)
        return dom.BulletList([], new_children)

    if kind == 'item_marker':
        return buf[node.start:node.end]
    if kind == 'list_spacing':
        return node.value
    if kind == 'item_spacing':
        return node.value
    if kind == 'remark_item':
        spacing = children[0]
        text = children[1:]
        args = []
        if spacing == "tight":
            if not children[1:]:
                return dom.ItemSpan(children[0], [])
            elif len(children) == 3 and children[2].name == dom.Paragraph and not children[2].args:
                return dom.ItemSpan(children[0], [trim_whitepace(t) for t in children[2].text if t is not None])
            else:
                return dom.ItemBlock(children[0], [c for c in children[2:] if c is not None])

        return dom.ItemBlock(children[0], [c for c in children[2:] if c is not None])

    raise Exception(node.name)

def parse(buf):
    node = parser.parse(buf)
    if node:
        tree = node.build(buf, builder)
        return tree

def parse_commonmark(buf):
    node = commonmark_parser(buf)
    if node:
        return node.build(buf, commonmark_builder)
