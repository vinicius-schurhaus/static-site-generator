import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        delimiter_count = node.text.count(delimiter)

        if delimiter_count % 2:
            raise ValueError("Open and closing delimiter not matching")

        parts = node.text.split(delimiter)

        for index, part in enumerate(parts):
            if part == "":
                continue

            node_type = text_type if index % 2 else TextType.TEXT
            result.append(TextNode(part, node_type))

    return result


def extract_markdown_images(text) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        images = extract_markdown_images(node.text)
        text = node.text

        for alt, url in images:
            image_markdown = f"![{alt}]({url})"
            parts = text.split(image_markdown)

            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
            result.append(TextNode(alt, TextType.IMAGE, url))

            text = parts[1]

        if text:
            result.append(TextNode(text, TextType.TEXT))

    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        links = extract_markdown_links(node.text)
        text = node.text

        for desc, url in links:
            link_markdown = f"[{desc}]({url})"
            parts = text.split(link_markdown)

            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))
            result.append(TextNode(desc, TextType.LINK, url))

            text = parts[1]

        if text:
            result.append(TextNode(text, TextType.TEXT))

    return result


def text_to_textnodes(text) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
