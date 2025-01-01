import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_values(self):
        node = TextNode('Lorem ipsum dolor sit amet', TextType.NORMAL, 'https://www.example.com')
        self.assertEqual(node.text, 'Lorem ipsum dolor sit amet')
        self.assertEqual(node.text_type.value, 'normal')
        self.assertEqual(node.url, 'https://www.example.com')
    
    def test_repr(self):
        node = TextNode('Lorem ipsum dolor sit amet', TextType.NORMAL, 'https://www.example.com')
        self.assertEqual(node.__repr__(), 'HTMLNode(Lorem ipsum dolor sit amet, normal, https://www.example.com)')

    def test_two_nodes(self):
        node1 = TextNode('Lorem ipsum dolor sit amet', TextType.NORMAL, 'https://www.example.com')
        node2 = TextNode('Lorem ipsum dolor sit amet', TextType.NORMAL, 'https://www.example.com')

        self.assertEqual(node1, node2)

if __name__ == '__main__':

    unittest.main()