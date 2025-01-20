from htmlnode import ParentNode
from textnode import text_node_to_html_node
from inline_markdown_parsers import text_to_text_nodes

block_type_paragraph = 'paragraph'
block_type_heading = 'heading'
block_type_code = 'code'
block_type_quote = 'quote'
block_type_ulist = 'unordered_list'
block_type_olist = 'ordered_list'

def block_to_block_type(markdown_text: str) -> str:
    # if the line starts with 1-6 continuous hashtags it's a heading
    if markdown_text.split()[0] in ['#', '##', '###', '####', '#####', '######']:
        return block_type_heading
    
    # if the line starts and ends with 3x ``` and is longer than 6 (so the conditions don't count eachothers backticks) it's a code block
    elif markdown_text[:3] == '```' and markdown_text[-3:] == '```' and len(markdown_text) >= 6:
        return block_type_code
    
    # if all lines except empty ones (newlines) start with > it's a quote
    elif all([line[0] == '>' for line in markdown_text.split('\n') if line != '']):
        return block_type_quote
    
    # if all lines except empty ones (newlines) start with either '* ' or '- ' (with a space) it's an unordered list
    elif all([line.startswith(('* ', '- ')) for line in markdown_text.split('\n') if line != '']):
        return block_type_ulist
    
    # if all lines except empty ones (newlines) start with a number followed by a . and a space, and the numbers increment by 1 it's an ordered list
    elif all([line.split('.')[0].isdigit() and line.split('.')[1].startswith(' ') for line in markdown_text.split('\n') if line != '']):
        # get the first char of every line start and check if it matches an incrementing list
        line_indexes = []
        for line in markdown_text.split('\n'):
            if len(line.split()) > 0:
                line_indexes.append(line.split()[0][0])

        incrementing_list = []
        for i in range(1, len(line_indexes) + 1):
            incrementing_list.append(str(i))
        
        if line_indexes == incrementing_list:
            return block_type_olist
    
    return block_type_paragraph

def markdown_to_blocks(markdown_text: str) -> list:
    if markdown_text in ['', ' '] or markdown_text is None:
        return []
    
    # split the text on multiple newlines after eachother
    split_text = markdown_text.split('\n\n')
    converted_blocks = []
    for block in split_text:
        if block == '':
            continue
        converted_blocks.append(block.strip())
    return converted_blocks

def markdown_to_html_node(markdown_text: str) -> ParentNode:
    split_blocks = markdown_to_blocks(markdown_text)
    parent_children = []

    for block in split_blocks:
        html_node = block_to_html_node(block)
        parent_children.append(html_node)

    return ParentNode('div', parent_children)

def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)

    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    elif block_type == block_type_heading:
        return heading_to_html_node(block)
    elif block_type == block_type_code:
        return code_to_html_node(block)
    elif block_type == block_type_quote:
        return quote_to_html_node(block)
    elif block_type == block_type_ulist:
        return ulist_to_html_node(block)
    elif block_type == block_type_olist:
        return olist_to_html_node(block)

    raise ValueError('Invalid block type!')

def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    children = []

    for node in text_nodes:
        children.append(text_node_to_html_node(node))

    return children

def paragraph_to_html_node(block: str) -> ParentNode:
    # split at newlines
    split_lines = block.split('\n')
    joined_lines = ' '.join(split_lines)

    return ParentNode('p', text_to_children(joined_lines))

def heading_to_html_node(block: str) -> ParentNode:
    count = 0

    # count number of #
    for char in block:
        if char == '#':
            count += 1
        else:
            break
    
    # handle edge case of '###### ' or something like that
    if count + 1 >= len(block):
        raise ValueError('Invalid heading!')
    
    after_heading_text = block[count + 1:]

    return ParentNode(f'h{count}', text_to_children(after_heading_text))

def code_to_html_node(block):
    # Error if the code block is not valid
    if not block.startswith('```') or not block.endswith('```'):
        raise ValueError('Invalid code block!')
    
    # take the text between the code block
    text = block[4:-3]

    return ParentNode('pre', [ParentNode('code', text_to_children(text))])


def olist_to_html_node(block):
    # split at newlines
    items = block.split('\n')
    converted_items = []

    for item in items:
        # get text after the '1. ' so after the 3rd
        text = item[3:]
        children = text_to_children(text)
        converted_items.append(ParentNode('li', children))

    return ParentNode('ol', converted_items)


def ulist_to_html_node(block):
    # split at newlines
    items = block.split('\n')
    converted_items = []

    for item in items:
        # get the text after '- ' or '* '
        text = item[2:]
        children = text_to_children(text)
        converted_items.append(ParentNode('li', children))

    return ParentNode('ul', converted_items)


def quote_to_html_node(block):
    # split at newlines
    lines = block.split('\n')
    new_lines = []

    for line in lines:
        if not line.startswith('>'):
            raise ValueError('Invalid quote block!')
        
        # get text after '> ' without whitespace
        new_lines.append(line.lstrip('>').strip())
    
    joined_text = ' '.join(new_lines)

    return ParentNode('blockquote', text_to_children(joined_text))
