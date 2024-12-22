import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_equals_1(self):
        test_type = 'equals'
        test_node1 = TextNode("This is a text node", TextType.BOLD)
        test_node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(test_node1, test_node2, f"\n>> FAIL: {__name__} with {test_node1} {test_type} {test_node2}")
    def test_equals_2(self):
        test_type = 'equals'
        test_node1 = TextNode("", TextType.NORMAL, "")
        test_node2 = TextNode("", TextType.NORMAL, "")

        self.assertEqual(test_node1, test_node2, f"\n>> FAIL: {__name__} with {test_node1} {test_type} {test_node2}")

    def test_equals_3(self):
        test_type = 'equals'
        test_node1 = TextNode("<h1>Hello world</h1>", TextType.CODE)
        test_node2 = TextNode("<h1>Hello world</h1>", TextType.CODE)

        self.assertEqual(test_node1, test_node2, f"\n>> FAIL: {__name__} with {test_node1} {test_type} {test_node2}")

    def test_not_equals_1(self):
        test_type = 'not equal to'
        test_node1 = TextNode("This is a text node", TextType.NORMAL, 'github.com')
        test_node2 = TextNode("This is a different text node", TextType.ITALIC)

        self.assertNotEqual(test_node1, test_node2, f"\n>> FAIL: {__name__} with {test_node1} {test_type} {test_node2}")
    
    def test_not_equals_2(self):
        test_type = 'not equal to'
        test_node1 = TextNode("", TextType.BOLD)
        test_node2 = TextNode("", TextType.ITALIC)

        self.assertNotEqual(test_node1, test_node2, f"\n>> FAIL: {__name__} with {test_node1} {test_type} {test_node2}")

    def test_not_equals_3(self):
        test_type = 'not equal to'
        test_node1 = TextNode("", TextType.NORMAL, None)
        test_node2 = TextNode("", TextType.CODE, None)

        self.assertNotEqual(test_node1, test_node2, f"\n>> FAIL: {__name__} with {test_node1} {test_type} {test_node2}")



if __name__ == "__main__":

    unittest.main()