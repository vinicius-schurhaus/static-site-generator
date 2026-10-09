import unittest

from block import *


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = (
            "# This is a heading\n\n"
            "This is a paragraph of text. It has some **bold** "
            "and _italic_ words inside of it.\n\n"
            "- This is the first list item in a list block\n"
            "- This is a list item\n"
            "- This is another list item"
        )

        result = markdown_to_blocks(markdown)

        self.assertEqual(
            result,
            [
                "# This is a heading",
                (
                    "This is a paragraph of text. It has some **bold** "
                    "and _italic_ words inside of it."
                ),
                (
                    "- This is the first list item in a list block\n"
                    "- This is a list item\n"
                    "- This is another list item"
                ),
            ],
        )

    def test_markdown_to_blocks_strips_whitespace(self):
        markdown = (
            "  # Heading  \n\n"
            "  This is a paragraph.  \n\n"
            "  - Item 1\n"
            "  - Item 2  "
        )

        result = markdown_to_blocks(markdown)

        self.assertEqual(
            result,
            [
                "# Heading",
                "This is a paragraph.",
                "- Item 1\n  - Item 2",
            ],
        )

    def test_markdown_to_blocks_removes_empty_blocks(self):
        markdown = "# Heading\n\n\n\n" "Paragraph\n\n\n" "Another paragraph"

        result = markdown_to_blocks(markdown)

        self.assertEqual(
            result,
            [
                "# Heading",
                "Paragraph",
                "Another paragraph",
            ],
        )

    def test_markdown_to_blocks_empty_markdown(self):
        markdown = ""

        result = markdown_to_blocks(markdown)

        self.assertEqual(result, [])


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING,
        )

    def test_heading_levels(self):
        self.assertEqual(
            block_to_block_type("## Heading"),
            BlockType.HEADING,
        )

        self.assertEqual(
            block_to_block_type("###### Heading"),
            BlockType.HEADING,
        )

    def test_invalid_heading_too_many_hashes(self):
        self.assertEqual(
            block_to_block_type("####### Heading"),
            BlockType.PARAGRAPH,
        )

    def test_invalid_heading_without_space(self):
        self.assertEqual(
            block_to_block_type("#Heading"),
            BlockType.PARAGRAPH,
        )

    def test_code_block(self):
        block = "```\nprint('hello')\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_invalid_code_block_without_newline(self):
        block = "```print('hello')```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_quote_block(self):
        block = "> First line\n> Second line\n> Third line"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_quote_block_without_space(self):
        block = ">First line\n>Second line"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_invalid_quote_block(self):
        block = "> First line\nSecond line"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list(self):
        block = "- First item\n- Second item\n- Third item"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_invalid_unordered_list_without_space(self):
        block = "- First item\n-Second item"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_must_start_at_one(self):
        block = "2. First item\n3. Second item\n4. Third item"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_must_increment(self):
        block = "1. First item\n3. Third item\n4. Fourth item"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_requires_space(self):
        block = "1. First item\n2.Second item\n3. Third item"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_paragraph(self):
        block = "This is a normal paragraph."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        markdown = "This is a paragraph."

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><p>This is a paragraph.</p></div>",
        )

    def test_heading(self):
        markdown = "# This is a heading"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><h1>This is a heading</h1></div>",
        )

    def test_heading_with_inline_markdown(self):
        markdown = "## This is **bold** and _italic_"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><h2>This is <b>bold</b> and <i>italic</i></h2></div>",
        )

    def test_image(self):
        markdown = "![Tolkien](images/tolkien.png)"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            '<div><p><img src="images/tolkien.png" alt="Tolkien"></p></div>',
        )

    def test_unordered_list(self):
        markdown = "- First item\n- Second item"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            (
                "<div>"
                "<ul>"
                "<li>First item</li>"
                "<li>Second item</li>"
                "</ul>"
                "</div>"
            ),
        )

    def test_ordered_list(self):
        markdown = "1. First item\n2. Second item"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            (
                "<div>"
                "<ol>"
                "<li>First item</li>"
                "<li>Second item</li>"
                "</ol>"
                "</div>"
            ),
        )

    def test_quote(self):
        markdown = "> This is a quote"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote</blockquote></div>",
        )

    def test_code(self):
        markdown = "```\nprint('hello')\n```"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><pre><code>print('hello')\n</code></pre></div>",
        )

    def test_multiple_blocks(self):
        markdown = (
            "# Heading\n\n" "This is a paragraph.\n\n" "- First item\n" "- Second item"
        )

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            (
                "<div>"
                "<h1>Heading</h1>"
                "<p>This is a paragraph.</p>"
                "<ul>"
                "<li>First item</li>"
                "<li>Second item</li>"
                "</ul>"
                "</div>"
            ),
        )


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_with_whitespace(self):
        markdown = "#   Hello World   "
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_with_multiple_blocks(self):
        markdown = "# Hello\n\nThis is a paragraph."
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_missing(self):
        markdown = "This has no title."
        with self.assertRaises(ValueError):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
