from block_markdown_parsers import markdown_to_blocks
import unittest

class TestMarkdownToBlocks(unittest.TestCase):
    def test_standard(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        self.assertEqual(
                        [
                            '# This is a heading',
                            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                            '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
                        ],
                        markdown_to_blocks(markdown)
        )
    
    def test_lots_of_newlines(self):
        markdown = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
            markdown_to_blocks(markdown)
        )
    
    def test_edge_cases(self):
        self.assertEqual(markdown_to_blocks(''), [])
        self.assertEqual(markdown_to_blocks(' '), [])
        self.assertEqual(markdown_to_blocks('only one line of text'), ['only one line of text'])

if __name__ == '__main__':
    unittest.main()