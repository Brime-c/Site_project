import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes_list =  []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes_list.append(old_node)
            continue
        
        text_split = old_node.text.split(delimiter)
        if len(text_split) % 2 == 0:
            raise ValueError("unmatched delimiter found")
        for idx, chunk in enumerate(text_split):
            if chunk == "":
                continue
            elif idx % 2 == 0:
                new_nodes_list.append(TextNode(chunk, TextType.TEXT))
            elif idx % 2 == 1:
                new_nodes_list.append(TextNode(chunk, text_type))
    return new_nodes_list

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes_list =  []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes_list.append(old_node)
            continue
        if old_node.text == "":
            continue

        images = extract_markdown_images(old_node.text)
        original_text = old_node.text

        for image_alt,image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"
            text_split = original_text.split(image_markdown,1)
            original_text = text_split[1]

            if text_split[0] != "":
                new_nodes_list.append(TextNode(text_split[0], TextType.TEXT))
            new_nodes_list.append(TextNode(image_alt, TextType.IMAGE, image_url))

        if original_text !="":
            new_nodes_list.append(TextNode(original_text, TextType.TEXT))

    return new_nodes_list

def split_nodes_link(old_nodes):
    new_nodes_list =  []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes_list.append(old_node)
            continue
        if old_node.text == "":
            continue

        links = extract_markdown_links(old_node.text)
        original_text = old_node.text

        for link_text,link_url in links:
            link_markdown = f"[{link_text}]({link_url})"
            text_split = original_text.split(link_markdown,1)
            original_text = text_split[1]

            if text_split[0] != "":
                new_nodes_list.append(TextNode(text_split[0], TextType.TEXT))
            new_nodes_list.append(TextNode(link_text, TextType.LINK, link_url))

        if original_text !="":
            new_nodes_list.append(TextNode(original_text, TextType.TEXT))

    return new_nodes_list

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes,"**",TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes