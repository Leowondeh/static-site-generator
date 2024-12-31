import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            'div',
            'Hello, world!',
            None,
            {'class': 'greeting', 'href': 'https://github.com'},
        )
        self.assertEqual(
            node.properties_to_html(),
            ' class="greeting" href="https://github.com"',
        )

    def test_values(self):
        node = HTMLNode(
            'div',
            'lorem ipsum',
        )
        self.assertEqual(
            node.tag,
            'div',
        )
        self.assertEqual(
            node.value,
            'lorem ipsum',
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.properties,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            'p',
            'test text',
            None,
            {'class': 'primary'},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, test text, children: None, {'class': 'primary'})",
        )

    # LeafNode tests
    def test_to_html_no_children(self):
        node = LeafNode('p', 'hello world')
        self.assertEqual(node.to_html(), '<p>hello world</p>')

    def test_to_html_no_tag(self):
        node = LeafNode(None, 'hello world')
        self.assertEqual(node.to_html(), 'hello world')

if __name__ == '__main__':
    unittest.main()