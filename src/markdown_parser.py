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

def split_nodes_with_image(nodes: list[TextNode]) -> list:
    split_nodes = []
    
    for node in nodes:
        if node.text_type != TextType.NORMAL:
            split_nodes.append(node)
            continue
            
        image_matches = regex_markdown_images(node.text)
        
        if len(image_matches) == 0:
            split_nodes.append(node)
            continue
        
        start_len = 0
        for match in image_matches:
            # find the index of all the text before the match
            match_end_len = node.text.find(f'![{match[0]}]({match[1]})', start_len)
            
            before_image = node.text[start_len:match_end_len]
            
            # append the found text and link
            if before_image:
                split_nodes.append(TextNode(before_image, TextType.NORMAL))
            split_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            
            # set the new start length to after what we just appended ended
            start_len = node.text.index(f'![{match[0]}]({match[1]})') + len(f'![{match[0]}]({match[1]})')
            
        # if there is some text after we add it
        text_after = node.text[start_len:]
        if text_after:
            split_nodes.append(TextNode(text_after, TextType.NORMAL))
    
    return split_nodes

def split_nodes_with_link(nodes: list[TextNode]) -> list:
    split_nodes = []
    
    for node in nodes:
        if node.text_type != TextType.NORMAL:
            split_nodes.append(node)
            continue
            
        link_matches = regex_markdown_links(node.text)
        
        if len(link_matches) == 0:
            split_nodes.append(node)
            continue

        start_len = 0
        for match in link_matches:
            # find the index of all the text before the match
            match_end_len = node.text.find(f'[{match[0]}]({match[1]})', start_len)
            
            before_image = node.text[start_len:match_end_len]
            # append the found text and link
            if before_image:
                split_nodes.append(TextNode(before_image, TextType.NORMAL))
            split_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
             
            # set the new start length to after what we just appended ended
            start_len = match_end_len + len(f'[{match[0]}]({match[1]})')

        # if there is some text after we add it
        text_after = node.text[start_len:]
        if text_after:
            split_nodes.append(TextNode(text_after, TextType.NORMAL))
    
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
