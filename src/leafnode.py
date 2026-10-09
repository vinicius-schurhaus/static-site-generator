from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value

        props = self.props_to_html()

        if props:
            return f"<{self.tag} {props}>{self.value}</{self.tag}>"

        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False

        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )
