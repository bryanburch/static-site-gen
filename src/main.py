import re
from textnode import TextNode
from leafnode import LeafNode


def main():
    node = TextNode(
        "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
        "text",
    )
    new_nodes = split_nodes_image([node])
    print(new_nodes)


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(value=text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case "image":
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Unknown text type for TextNode.")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], "text"))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue

        split_nodes = []
        images = extract_markdown_images(old_node.text)

        if len(images) == 0:
            new_nodes.append(old_node)
            new_nodes.extend(split_nodes)
            continue

        text = old_node.text
        for i in range(len(images)):
            split = text.split(f"![{images[i][0]}]({images[i][1]})", 1)

            # don't create nodes for empty string
            if len(split[0]):
                split_nodes.append(TextNode(split[0], "text"))
            split_nodes.append(TextNode(images[i][0], "image", url=images[i][1]))
            text = split[1]

        if text:
            split_nodes.append(TextNode(text, "text"))

        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue

        split_nodes = []
        links = extract_markdown_links(old_node.text)

        if len(links) == 0:
            new_nodes.append(old_node)
            new_nodes.extend(split_nodes)
            continue

        text = old_node.text
        for i in range(len(links)):
            split = text.split(f"[{links[i][0]}]({links[i][1]})", 1)

            # don't create nodes for empty string
            if len(split[0]):
                split_nodes.append(TextNode(split[0], "text"))
            split_nodes.append(TextNode(links[i][0], "link", url=links[i][1]))
            text = split[1]

        if text:
            split_nodes.append(TextNode(text, "text"))

        new_nodes.extend(split_nodes)
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, text_type="text")
    nodes = split_nodes_delimiter([node], delimiter="**", text_type="bold")
    nodes = split_nodes_delimiter(nodes, delimiter="*", text_type="italic")
    nodes = split_nodes_delimiter(nodes, delimiter="`", text_type="code")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


if __name__ == "__main__":
    main()
