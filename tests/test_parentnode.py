import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        child = LeafNode("p", "Hello, world!")
        node = ParentNode("div", [child])

        self.assertEqual(
            node.to_html(),
            "<div><p>Hello, world!</p></div>",
        )

    def test_parent_to_html_with_multiple_children(self):
        children = [
            LeafNode("p", "Hello"),
            LeafNode("p", "World"),
        ]
        node = ParentNode("div", children)

        self.assertEqual(
            node.to_html(),
            "<div><p>Hello</p><p>World</p></div>",
        )

    def test_parent_to_html_nested(self):
        child = ParentNode(
            "div",
            [LeafNode("p", "Hello")],
        )
        node = ParentNode("main", [child])

        self.assertEqual(
            node.to_html(),
            "<main><div><p>Hello</p></div></main>",
        )

    def test_parent_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("p", "Hello")],
            {"class": "container"},
        )

        self.assertEqual(
            node.to_html(),
            '<div class="container"><p>Hello</p></div>',
        )

    def test_parent_to_html_without_tag(self):
        node = ParentNode(None, [])

        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_without_children(self):
        node = ParentNode("div", None)

        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
