import unittest
from textnode import TextNode, TextType
from markdown_parser import (
                                split_nodes_with_delimiter,
                                regex_markdown_images,
                                regex_markdown_links,
                                split_nodes_with_image,
                                split_nodes_with_link,
                                text_to_text_nodes
                            )

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
        node = TextNode("example text with `code` text", TextType.NORMAL)
        result = split_nodes_with_delimiter([node], "`", TextType.CODE)

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

class TestSplitNodesWithImage(unittest.TestCase):
    def test_only_image(self):
        node = TextNode('![image link](https://www.example.com)', TextType.NORMAL)
        
        self.assertEqual(
            [
                TextNode('image link', TextType.IMAGE, 'https://www.example.com')
            ],
            split_nodes_with_image([node])
        )
    
    def test_single_image(self):
        node = TextNode('text with a ![image link](https://www.example.com)', TextType.NORMAL)
        
        self.assertEqual(
            [
                TextNode('text with a ', TextType.NORMAL, None),
                TextNode('image link', TextType.IMAGE, 'https://www.example.com')
            ],
            split_nodes_with_image([node])
        )
    
    def test_single_image_and_text_after(self):
        node = TextNode('text with a ![image link](https://www.example.com) and some text after', TextType.NORMAL)
        self.assertEqual(
            [
                TextNode('text with a ', TextType.NORMAL, None),
                TextNode('image link', TextType.IMAGE, 'https://www.example.com'),
                TextNode(' and some text after', TextType.NORMAL, None)
            ],
            split_nodes_with_image([node])
        )

class TestSplitNodesWithLink(unittest.TestCase):
    def test_only_link(self):
        node = TextNode('[link](https://www.example.com)', TextType.NORMAL)
        
        self.assertEqual(
            [
                TextNode('link', TextType.LINK, 'https://www.example.com')
            ],
            split_nodes_with_link([node])
        )

    def test_single_link(self):
        node = TextNode('text with a [link](https://www.example.com)', TextType.NORMAL)
        
        self.assertEqual(
            [
                TextNode('text with a ', TextType.NORMAL, None),
                TextNode('link', TextType.LINK, 'https://www.example.com')
            ],
            split_nodes_with_link([node])
        )
    
    def test_single_link_and_text_after(self):
        node = TextNode('text with a [link](https://www.example.com) and some text after', TextType.NORMAL)
        self.assertEqual(
            [
                TextNode('text with a ', TextType.NORMAL, None),
                TextNode('link', TextType.LINK, 'https://www.example.com'),
                TextNode(' and some text after', TextType.NORMAL, None)
            ],
            split_nodes_with_link([node])
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

class TestTextToTextNodes(unittest.TestCase):
    def test(self):
        text = 'This is **bold text** with an *italic* word, a `code block`, an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://example.com)'

        self.assertEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("bold text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word, a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(", an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            text_to_text_nodes(text)
        )

    
