import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("Hello", TextType.TEXT)
        other = TextNode("Hello", TextType.TEXT)

        self.assertEqual(node, other)

    def test_eq_different_text_type_or_url(self):
        node = TextNode("Hello", TextType.TEXT, "url")

        self.assertNotEqual(node, TextNode("World", TextType.TEXT, "url"))
        self.assertNotEqual(node, TextNode("Hello", TextType.BOLD, "url"))
        self.assertNotEqual(node, TextNode("Hello", TextType.TEXT, "other-url"))

    def test_eq_with_non_textnode(self):
        node = TextNode("Hello", TextType.TEXT)

        self.assertNotEqual(node, None)
        self.assertNotEqual(node, "Hello")
        self.assertNotEqual(node, 123)

    def test_eq_default_url(self):
        node = TextNode("Hello", TextType.TEXT)
        other = TextNode("Hello", TextType.TEXT)

        self.assertEqual(node, other)

    def test_repr(self):
        node = TextNode("Hello", TextType.BOLD, "https://example.com")

        self.assertEqual(
            repr(node),
            "TextNode(Hello,bold,https://example.com)",
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("Hello", TextType.TEXT)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node, LeafNode(None, "Hello"))

    def test_bold(self):
        node = TextNode("Hello", TextType.BOLD)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node, LeafNode("b", "Hello"))

    def test_italic(self):
        node = TextNode("Hello", TextType.ITALIC)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node, LeafNode("i", "Hello"))

    def test_code(self):
        node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node, LeafNode("code", "print('Hello')"))

    def test_link(self):
        node = TextNode(
            "Click here",
            TextType.LINK,
            "https://example.com",
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(
            html_node,
            LeafNode(
                "a",
                "Click here",
                {"href": "https://example.com"},
            ),
        )

    def test_image(self):
        node = TextNode(
            "An image",
            TextType.IMAGE,
            "https://example.com/image.png",
        )

        html_node = text_node_to_html_node(node)

        self.assertEqual(
            html_node,
            LeafNode(
                "img",
                None,
                {
                    "src": "https://example.com/image.png",
                    "alt": "An image",
                },
            ),
        )


if __name__ == "__main__":
    unittest.main()
