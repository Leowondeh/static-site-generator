import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_values(self):
        node = TextNode('Lorem ipsum dolor sit amet', TextType.NORMAL, 'https://www.example.com')
        self.assertEqual(node.text, 'Lorem ipsum dolor sit amet')
        self.assertEqual(node.text_type.value, 'normal')
        self.assertEqual(node.url, 'https://www.example.com')
    
    def test_repr(self):
        node = TextNode('Lorem ipsum dolor sit amet', TextType.NORMAL, 'https://www.example.com')
        self.assertEqual(node.__repr__(), 'TextNode(Lorem ipsum dolor sit amet, normal, https://www.example.com)')

    def test_two_nodes(self):
        node1 = TextNode('Lorem ipsum dolor sit amet', TextType.NORMAL, 'https://www.example.com')
        node2 = TextNode('Lorem ipsum dolor sit amet', TextType.NORMAL, 'https://www.example.com')

        self.assertEqual(node1, node2)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode('test text', TextType.NORMAL)
        converted_node = text_node_to_html_node(node)

        self.assertEqual(converted_node.tag, None)
        self.assertEqual(converted_node.value, 'test text')

    def test_image(self):
        node = TextNode('test image', TextType.IMAGE, 'https://www.example.com')
        converted_node = text_node_to_html_node(node)

        self.assertEqual(converted_node.tag, 'img')
        self.assertEqual(converted_node.value, '')
        self.assertEqual(
            converted_node.properties,
            {'src': 'https://www.example.com', 'alt': 'test image'},
        )

    def test_bold(self):
        node = TextNode('bold text', TextType.BOLD)
        converted_node = text_node_to_html_node(node)

        self.assertEqual(converted_node.tag, 'b')
        self.assertEqual(converted_node.value, 'bold text')
    
    def test_italic(self):
        node = TextNode('italic text', TextType.ITALIC)
        converted_node = text_node_to_html_node(node)

        self.assertEqual(converted_node.tag, 'i')
        self.assertEqual(converted_node.value, 'italic text')
    
    def test_code(self):
        node = TextNode('code text', TextType.CODE)
        converted_node = text_node_to_html_node(node)

        self.assertEqual(converted_node.tag, 'code')
        self.assertEqual(converted_node.value, 'code text')

    def test_link(self):
        node = TextNode('link text', TextType.LINK, 'https://www.example.com')
        converted_node = text_node_to_html_node(node)

        self.assertEqual(converted_node.tag, 'a')
        self.assertEqual(converted_node.value, 'link text')
        self.assertEqual(
            converted_node.properties,
            {'href': 'https://www.example.com'},
        )

if __name__ == '__main__':

    unittest.main()