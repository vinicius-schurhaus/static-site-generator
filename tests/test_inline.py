import unittest

from textnode import TextNode, TextType
from inline import *


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_bold(self):
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
        ]

        result = split_nodes_delimiter(
            nodes,
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_italic(self):
        nodes = [
            TextNode("This is _italic_ text", TextType.TEXT),
        ]

        result = split_nodes_delimiter(
            nodes,
            "_",
            TextType.ITALIC,
        )

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_code(self):
        nodes = [
            TextNode("This is `code` text", TextType.TEXT),
        ]

        result = split_nodes_delimiter(
            nodes,
            "`",
            TextType.CODE,
        )

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_multiple_delimiters(self):
        nodes = [
            TextNode(
                "This is **bold** and **more bold** text",
                TextType.TEXT,
            ),
        ]

        result = split_nodes_delimiter(
            nodes,
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("more bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_preserves_non_text_nodes(self):
        nodes = [
            TextNode("This is **bold**", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]

        result = split_nodes_delimiter(
            nodes,
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("already bold", TextType.BOLD),
            ],
        )

    def test_split_without_delimiter(self):
        nodes = [
            TextNode("This is plain text", TextType.TEXT),
        ]

        result = split_nodes_delimiter(
            nodes,
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            result,
            [
                TextNode("This is plain text", TextType.TEXT),
            ],
        )

    def test_split_with_unmatched_delimiter(self):
        nodes = [
            TextNode("This is **bold text", TextType.TEXT),
        ]

        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                nodes,
                "**",
                TextType.BOLD,
            )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_single_image(self):
        text = "This is an ![image](https://example.com/image.png)"

        result = extract_markdown_images(text)

        self.assertEqual(
            result,
            [
                ("image", "https://example.com/image.png"),
            ],
        )

    def test_extract_multiple_images(self):
        text = "![cat](cat.png) and " "![dog](dog.png)"

        result = extract_markdown_images(text)

        self.assertEqual(
            result,
            [
                ("cat", "cat.png"),
                ("dog", "dog.png"),
            ],
        )

    def test_extract_images_without_matches(self):
        text = "This text has no images."

        result = extract_markdown_images(text)

        self.assertEqual(result, [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_single_link(self):
        text = "This is a [link](https://example.com)"

        result = extract_markdown_links(text)

        self.assertEqual(
            result,
            [
                ("link", "https://example.com"),
            ],
        )

    def test_extract_multiple_links(self):
        text = "[Google](https://google.com) and " "[GitHub](https://github.com)"

        result = extract_markdown_links(text)

        self.assertEqual(
            result,
            [
                ("Google", "https://google.com"),
                ("GitHub", "https://github.com"),
            ],
        )

    def test_extract_links_without_matches(self):
        text = "This text has no links."

        result = extract_markdown_links(text)

        self.assertEqual(result, [])

    def test_extract_links_ignores_images(self):
        text = "![cat](cat.png) and [Google](https://google.com)"

        result = extract_markdown_links(text)

        self.assertEqual(
            result,
            [
                ("Google", "https://google.com"),
            ],
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_split_single_image(self):
        nodes = [
            TextNode(
                "This is an ![image](image.png)",
                TextType.TEXT,
            ),
        ]

        result = split_nodes_image(nodes)

        self.assertEqual(
            result,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "image.png"),
            ],
        )

    def test_split_image_with_text_after(self):
        nodes = [
            TextNode(
                "This is an ![image](image.png) in the text",
                TextType.TEXT,
            ),
        ]

        result = split_nodes_image(nodes)

        self.assertEqual(
            result,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "image.png"),
                TextNode(" in the text", TextType.TEXT),
            ],
        )

    def test_split_multiple_images(self):
        nodes = [
            TextNode(
                "![cat](cat.png) and ![dog](dog.png)",
                TextType.TEXT,
            ),
        ]

        result = split_nodes_image(nodes)

        self.assertEqual(
            result,
            [
                TextNode("cat", TextType.IMAGE, "cat.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("dog", TextType.IMAGE, "dog.png"),
            ],
        )

    def test_split_preserves_non_text_nodes(self):
        nodes = [
            TextNode(
                "This is an ![image](image.png)",
                TextType.TEXT,
            ),
            TextNode("already bold", TextType.BOLD),
        ]

        result = split_nodes_image(nodes)

        self.assertEqual(
            result,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "image.png"),
                TextNode("already bold", TextType.BOLD),
            ],
        )

    def test_split_without_images(self):
        nodes = [
            TextNode("This is plain text", TextType.TEXT),
        ]

        result = split_nodes_image(nodes)

        self.assertEqual(
            result,
            [
                TextNode("This is plain text", TextType.TEXT),
            ],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_single_link(self):
        nodes = [
            TextNode(
                "This is a [link](https://example.com)",
                TextType.TEXT,
            ),
        ]

        result = split_nodes_link(nodes)

        self.assertEqual(
            result,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://example.com",
                ),
            ],
        )

    def test_split_link_with_text_after(self):
        nodes = [
            TextNode(
                "This is a [link](https://example.com) in the text",
                TextType.TEXT,
            ),
        ]

        result = split_nodes_link(nodes)

        self.assertEqual(
            result,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://example.com",
                ),
                TextNode(" in the text", TextType.TEXT),
            ],
        )

    def test_split_multiple_links(self):
        nodes = [
            TextNode(
                "[Google](https://google.com) and " "[GitHub](https://github.com)",
                TextType.TEXT,
            ),
        ]

        result = split_nodes_link(nodes)

        self.assertEqual(
            result,
            [
                TextNode(
                    "Google",
                    TextType.LINK,
                    "https://google.com",
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "GitHub",
                    TextType.LINK,
                    "https://github.com",
                ),
            ],
        )

    def test_split_preserves_non_text_nodes(self):
        nodes = [
            TextNode(
                "This is a [link](https://example.com)",
                TextType.TEXT,
            ),
            TextNode("already bold", TextType.BOLD),
        ]

        result = split_nodes_link(nodes)

        self.assertEqual(
            result,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://example.com",
                ),
                TextNode("already bold", TextType.BOLD),
            ],
        )

    def test_split_without_links(self):
        nodes = [
            TextNode("This is plain text", TextType.TEXT),
        ]

        result = split_nodes_link(nodes)

        self.assertEqual(
            result,
            [
                TextNode("This is plain text", TextType.TEXT),
            ],
        )

    def test_split_link_does_not_match_image(self):
        nodes = [
            TextNode(
                "![image](image.png)",
                TextType.TEXT,
            ),
        ]

        result = split_nodes_link(nodes)

        self.assertEqual(
            result,
            [
                TextNode("![image](image.png)", TextType.TEXT),
            ],
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        result = text_to_textnodes(text)

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text."

        result = text_to_textnodes(text)

        self.assertEqual(
            result,
            [
                TextNode("This is just plain text.", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_bold(self):
        text = "This is **bold** text."

        result = text_to_textnodes(text)

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text.", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_italic(self):
        text = "This is _italic_ text."

        result = text_to_textnodes(text)

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text.", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_code(self):
        text = "This is `code` text."

        result = text_to_textnodes(text)

        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text.", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_image(self):
        text = "Here is ![an image](image.png)."

        result = text_to_textnodes(text)

        self.assertEqual(
            result,
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("an image", TextType.IMAGE, "image.png"),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_link(self):
        text = "Here is [a link](https://example.com)."

        result = text_to_textnodes(text)

        self.assertEqual(
            result,
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://example.com"),
                TextNode(".", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
