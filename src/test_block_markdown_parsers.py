from block_markdown_parsers import markdown_to_blocks, block_to_block_type
import unittest

from block_markdown_parsers import (
    block_type_paragraph,
    block_type_heading, 
    block_type_code, 
    block_type_quote, 
    block_type_olist, 
    block_type_ulist
)

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

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_type_heading, block_to_block_type('###### a small heading'))
        self.assertEqual(block_type_heading, block_to_block_type('##### a small heading'))
        self.assertEqual(block_type_heading, block_to_block_type('#### a medium heading'))
        self.assertEqual(block_type_heading, block_to_block_type('#### a medium heading'))
        self.assertEqual(block_type_heading, block_to_block_type('### a big heading'))
        self.assertEqual(block_type_heading, block_to_block_type('## a big heading'))
        self.assertEqual(block_type_heading, block_to_block_type('# a huge heading'))

        self.assertEqual(block_type_paragraph, block_to_block_type('#.# an interrupted heading'))
        self.assertEqual(block_type_paragraph, block_to_block_type('####### a heading with too many #'))
    
    def test_code(self):
        self.assertEqual(block_type_code, block_to_block_type('```a code block```'))
        self.assertEqual(block_type_code, block_to_block_type('``````'))
        self.assertEqual(block_type_paragraph, block_to_block_type('````'))
    
    def test_quote(self):
        quote_text = """
> a quote
> another quote
"""
        self.assertEqual(block_type_quote, block_to_block_type(quote_text))
    
    def test_unordered_list(self):
        unordered_list_asterisk_text = """
* element one
* element two
* element three
"""
        unordered_list_dash_text = """
- element one
- element two
- element three
"""
        unordered_list_mixed_text = """
* element one
- element two
* element three
- element four
"""
        self.assertEqual(block_type_ulist, block_to_block_type(unordered_list_asterisk_text))
        self.assertEqual(block_type_ulist, block_to_block_type(unordered_list_dash_text))
        self.assertEqual(block_type_ulist, block_to_block_type(unordered_list_mixed_text))

    def test_ordered_list(self):
        ordered_list_correct_order = """
1. something
2. something else
3. something something
"""
        ordered_list_wrong_order = """
1. first element
3. third element
2. second element
4. oopsie daisy i ordered it wrong!
"""
        self.assertEqual(block_type_olist, block_to_block_type(ordered_list_correct_order))
        self.assertEqual(block_type_paragraph, block_to_block_type(ordered_list_wrong_order))
        
if __name__ == '__main__':
    unittest.main()