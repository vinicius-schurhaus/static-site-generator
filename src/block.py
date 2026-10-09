from enum import Enum

from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []

    for block in markdown.split("\n\n"):
        block = block.strip()

        if block:
            blocks.append(block)

    return blocks


def block_to_block_type(markdown: str) -> BlockType:
    lines = markdown.split("\n")

    # Heading
    first_line = lines[0]
    parts = first_line.split(" ", 1)

    if len(parts) == 2:
        hashes = parts[0]

        if 1 <= len(hashes) <= 6 and all(char == "#" for char in hashes):
            return BlockType.HEADING

    # Code block
    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE

    # Quote block
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list
    if all(line.startswith(f"{index}. ") for index, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)

    children = []

    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))

    return children


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            parts = block.split(" ", 1)
            level = len(parts[0])
            text = parts[1]

            children = text_to_children(text)
            block_node = ParentNode(f"h{level}", children)

        elif block_type == BlockType.PARAGRAPH:
            text = " ".join(block.split("\n"))
            children = text_to_children(text)
            block_node = ParentNode("p", children)

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            text = "\n".join(line[1:].lstrip() for line in lines)

            children = text_to_children(text)
            block_node = ParentNode("blockquote", children)

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            children = []

            for line in lines:
                text = line[2:]
                li_children = text_to_children(text)
                children.append(ParentNode("li", li_children))

            block_node = ParentNode("ul", children)

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            children = []

            for line in lines:
                text = line.split(". ", 1)[1]
                li_children = text_to_children(text)
                children.append(ParentNode("li", li_children))

            block_node = ParentNode("ol", children)

        elif block_type == BlockType.CODE:
            code = block[4:-3]
            text_node = TextNode(code, TextType.TEXT)
            code_node = text_node_to_html_node(text_node)

            block_node = ParentNode(
                "pre",
                [ParentNode("code", [code_node])],
            )

        else:
            raise ValueError(f"Unsupported block type: {block_type}")

        block_nodes.append(block_node)

    return ParentNode("div", block_nodes)


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()

    raise ValueError("No h1 header found")
