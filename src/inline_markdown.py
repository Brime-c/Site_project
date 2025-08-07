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
            raise Exception("unmatched delimiter found")
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