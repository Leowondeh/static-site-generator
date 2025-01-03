import unittest
from textnode import TextNode, TextType
from markdown_parser import split_nodes_with_delimiter, regex_markdown_images, regex_markdown_links

class TestSplitNodesWithDelimiter(unittest.TestCase):
    def test_delimiter_bold(self):
        node = TextNode('example text with **bold** word', TextType.NORMAL)
        result = split_nodes_with_delimiter([node], '**', TextType.BOLD)

        self.assertListEqual(
            [
                TextNode('example text with ', TextType.NORMAL, None),
                TextNode('bold', TextType.BOLD, None),
                TextNode(' word', TextType.NORMAL, None)
            ],
            result
        )
    
    def test_delimiter_italic(self):
        node = TextNode('example text with *italic* word', TextType.NORMAL)
        result = split_nodes_with_delimiter([node], '*', TextType.ITALIC)

        self.assertListEqual(
            [
                TextNode('example text with ', TextType.NORMAL, None),
                TextNode('italic', TextType.ITALIC, None),
                TextNode(' word', TextType.NORMAL, None)
            ],
            result
        )
    
    def test_delimiter_code(self):
        node = TextNode("example text with 'code' text", TextType.NORMAL)
        result = split_nodes_with_delimiter([node], "'", TextType.CODE)

        self.assertListEqual(
            [
                TextNode('example text with ', TextType.NORMAL, None),
                TextNode('code', TextType.CODE, None),
                TextNode(' text', TextType.NORMAL, None)
            ],
            result
        )
    def test_delimiter_double_bold(self):
        node = TextNode('example text with **bold** and **another** word', TextType.NORMAL)
        result = split_nodes_with_delimiter([node], '**', TextType.BOLD)

        self.assertListEqual(
            [
                TextNode('example text with ', TextType.NORMAL, None),
                TextNode('bold', TextType.BOLD, None),
                TextNode(' and ', TextType.NORMAL, None),
                TextNode('another', TextType.BOLD, None),
                TextNode(' word', TextType.NORMAL, None)
            ],
            result
        )

    def test_delimiter_multiword_bold(self):
        node = TextNode('example text with **bold** and **another bold** word', TextType.NORMAL)
        result = split_nodes_with_delimiter([node], '**', TextType.BOLD)

        self.assertListEqual(
            [
                TextNode('example text with ', TextType.NORMAL, None),
                TextNode('bold', TextType.BOLD, None),
                TextNode(' and ', TextType.NORMAL, None),
                TextNode('another bold', TextType.BOLD, None),
                TextNode(' word', TextType.NORMAL, None)
            ],
            result
        )

    def test_delimiter_multiple_delimiters(self):
        node = TextNode('example text with **bold** and *italic*', TextType.NORMAL)
        result_part1 = split_nodes_with_delimiter([node], '**', TextType.BOLD)
        result_finished = split_nodes_with_delimiter(result_part1, '*', TextType.ITALIC)

        self.assertListEqual(
            [
                TextNode('example text with ', TextType.NORMAL, None),
                TextNode('bold', TextType.BOLD, None),
                TextNode(' and ', TextType.NORMAL, None),
                TextNode('italic', TextType.ITALIC, None)
            ],
            result_finished
        )

class TestRegexMarkdownImages(unittest.TestCase):
    def test_text_image(self):
        text = 'This is text with a ![linked image](https://i.imgur.com/aKaOqIh.gif).'
        result = regex_markdown_images(text)

        self.assertListEqual(
            [
                ('linked image', 'https://i.imgur.com/aKaOqIh.gif')
            ],
            result
        )
    
    def test_text_multiple_images(self):
        text = 'This is text with a ![linked image](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)'
        result = regex_markdown_images(text)

        self.assertListEqual(
            [
                ('linked image', 'https://i.imgur.com/aKaOqIh.gif'),
                ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')
            ],
            result
        )

class TestRegexMarkdownLinks(unittest.TestCase):
    def test_text_link(self):
        text = 'This is text with a [link to example](https://www.example.com).'
        result = regex_markdown_links(text)

        self.assertListEqual(
            [
                ('link to example', 'https://www.example.com')
            ],
            result
        )
    
    def test_text_multiple_links(self):
        text = 'This is text with a [link to example](https://www.example.com) and a [link to github](https://www.github.com)'
        result = regex_markdown_links(text)
        
        self.assertListEqual(
            [
                ('link to example', 'https://www.example.com'),
                ('link to github', 'https://www.github.com')
            ],
            result
        )
