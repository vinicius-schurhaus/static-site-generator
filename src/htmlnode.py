class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list[HTMLNode] = None,
        props: dict[str, str] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None:
            return ""

        props_list = []

        for prop in self.props:
            props_list.append(f'{prop}="{self.props[prop]}"')

        return " ".join(props_list)

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
