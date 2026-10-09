import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://example.com",
                "target": "_blank",
            }
        )

        self.assertEqual(
            node.props_to_html(),
            'href="https://example.com" target="_blank"',
        )

    def test_props_to_html_empty(self):
        node = HTMLNode(props={})

        self.assertEqual(node.props_to_html(), "")

    def test_to_html(self):
        node = HTMLNode()

        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode(
            tag="p",
            value="Hello",
            children=[],
            props={"class": "text"},
        )

        self.assertEqual(
            repr(node),
            "HTMLNode(p, Hello, [], {'class': 'text'})",
        )


if __name__ == "__main__":
    unittest.main()
