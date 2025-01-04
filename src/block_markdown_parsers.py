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