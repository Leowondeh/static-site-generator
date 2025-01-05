block_type_paragraph = 'paragraph'
block_type_heading = 'heading'
block_type_code = 'code'
block_type_quote = 'quote'
block_type_ulist = 'unordered_list'
block_type_olist = 'ordered_list'

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
        line_indexes = [line.split()[0][0] for line in markdown_text.split('\n') if len(line.split()) > 0]
        if line_indexes == [str(i) for i in range(1, len(line_indexes) + 1)]:
            return block_type_olist
    
    return block_type_paragraph