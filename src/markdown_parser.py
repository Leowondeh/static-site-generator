from textnode import TextType, TextNode
import re

def split_nodes_with_delimiter(nodes: list[TextNode], delimiter: str, type: TextType) -> list:
    split_nodes = []

    for node in nodes:
        if node.text_type != TextType.NORMAL:
            split_nodes.append(node)
            continue
            
        split_node_text = node.text.split(delimiter)
        
        # if number of splits is even, there is no delimited text
        if len(split_node_text) % 2 == 0:
            raise Exception('Invalid Markdown syntax - a delimiter does not have a matching closing parameter')
        
        # if split the uneven parts will always be the ones that contain the delimiter text
        for i in range(len(split_node_text)):
            if split_node_text[i] == '':
                continue
            if i % 2 == 1:
                split_nodes.append(TextNode(split_node_text[i], type, node.url))
            else:
                split_nodes.append(TextNode(split_node_text[i], TextType.NORMAL, node.url))
    
    return split_nodes

def regex_markdown_images(text: str) -> list[tuple]:
    pattern = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
    matches = re.findall(pattern, text)
    
    return matches

def regex_markdown_links(text: str) -> list[tuple]:
    pattern = r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)'
    #          ~~~~~~ = negative lookbehind: expression cannot start with "!" (because it would be an image)
    matches = re.findall(pattern, text)
    
    return matches
