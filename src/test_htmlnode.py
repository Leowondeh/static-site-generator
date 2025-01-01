import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    # HTMLNode tests
    def test_to_html_props(self):
        node = HTMLNode('div', 'Hello, world!', None, {'class': 'greeting', 'href': 'https://www.example.com'})
        self.assertEqual(node.properties_to_html(), ' class="greeting" href="https://www.example.com"')

    def test_values(self):
        node = HTMLNode('div', 'lorem ipsum')
        self.assertEqual(node.tag, 'div')
        self.assertEqual(node.value, 'lorem ipsum')
        self.assertEqual(node.children, None)
        self.assertEqual(node.properties, None)

    def test_repr(self):
        node = HTMLNode('p', 'test text', None, {'class': 'primary'})
        self.assertEqual(node.__repr__(), "HTMLNode(p, test text, children: None, {'class': 'primary'})")

    # LeafNode tests
    def test_to_html_no_children(self):
        node = LeafNode('p', 'hello world')
        self.assertEqual(node.to_html(), '<p>hello world</p>')

    def test_to_html_no_tag(self):
        node = LeafNode(None, 'hello world')
        self.assertEqual(node.to_html(), 'hello world')

    # ParentNode tests
    def test_parent_to_html_standard(self):
        node = ParentNode('p',
                          [
                              LeafNode('b', 'example bold text'),
                              LeafNode('i', 'example italic text'),
                              LeafNode(None, 'example normal text'),
                              LeafNode('b', 'another example bold text')
                          ]
        )
        self.assertEqual(node.to_html(), '<p><b>example bold text</b><i>example italic text</i>example normal text<b>another example bold text</b></p>')
    
    def test_parent_to_html_no_children(self):
        node = ParentNode('p', [])
        
        # Test specifically for the min. 1 child error
        with self.assertRaises(ValueError) as error:
            node.to_html()
        self.assertEqual(str(error.exception), 'ParentNode requires at least one child')
    
    def test_parent_to_html_no_tag(self):
        node = ParentNode('', [LeafNode('b', 'example bold text'), LeafNode('i', 'example italic text')])

        # Test specifically for the missing tag error
        with self.assertRaises(ValueError) as error:
            node.to_html()
        self.assertEqual(str(error.exception), 'ParentNode requires a tag')

    def test_parent_to_html_nested(self):
        node = ParentNode('p',
                          [
                              ParentNode('p', [LeafNode('b', 'example bold text'), LeafNode('i', 'example italic text')]),
                              LeafNode(None, 'example normal text'),
                              ParentNode('p', [LeafNode(None, 'example normal text'), LeafNode('b', 'another example bold text')]),
                              LeafNode('b', 'example bold text')
                          ])
        self.assertEqual(node.to_html(), '<p><p><b>example bold text</b><i>example italic text</i></p>example normal text<p>example normal text<b>another example bold text</b></p><b>example bold text</b></p>')
if __name__ == '__main__':
    unittest.main()
