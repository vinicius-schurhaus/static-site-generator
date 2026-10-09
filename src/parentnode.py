from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props=None):
        super().__init__(tag, None, children, props)


    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if self.children is None:
            raise ValueError("ParentNode must have children")

        children_html = ""

        for child in self.children:
            children_html += child.to_html()

        props = self.props_to_html()

        if props:
            return f"<{self.tag} {props}>{children_html}</{self.tag}>"

        return f"<{self.tag}>{children_html}</{self.tag}>"

