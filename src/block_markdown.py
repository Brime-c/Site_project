import re
from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_textnodes, extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_link, split_nodes_image

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")
    final_block_list = []
    for block in block_list:
        block = block.strip()
        if block != "":
            final_block_list.append(block)
            
    return final_block_list

def block_to_block(block):
    if "\n" not in block and re.match(r'^#{1,6} ', block):
       return BlockType.HEADING
    
    lines = block.split("\n")
    if lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    counter = 1
    for line in lines:
        if line.startswith(f"{counter}. "):
            counter += 1
        else:
            break
    else:
        if counter == len(lines)+1:
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_list = []
    for block in blocks:
        block_type = block_to_block(block)
        
        if block_type == BlockType.HEADING:
            match = re.match(r"^(#{1,6})\s+(.*)", block)
            if match:
                heading_level = f"h{len(match.group(1))}"
                heading_text = match.group(2)
                html_list.append(ParentNode(heading_level, children=text_to_children(heading_text)))
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            quote_content = " ".join(line.lstrip("> ").strip() for line in lines)
            html_list.append(ParentNode("blockquote", children=text_to_children(quote_content)))
        elif block_type == BlockType.PARAGRAPH:
            para_text = block.replace('\n', ' ')
            html_list.append(ParentNode("p", children=text_to_children(para_text)))
        elif block_type == BlockType.CODE:
            lines = block.split('\n')
            code_text = '\n'.join(lines[1:-1]) + '\n'
            html_list.append(
                ParentNode("pre", [
                    ParentNode("code", [LeafNode(None, code_text)])
                ])
            )
        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            lines = block.split("\n")
            for line in lines:
                striped_line = line[2:].strip()
                items.append(ParentNode("li", text_to_children(striped_line)))
            html_list.append(ParentNode("ul", children=items))
        elif block_type == BlockType.ORDERED_LIST:
            items = []
            lines = block.split("\n")
            for line in lines:
                item_text = re.sub(r"^\d+\.\s*", "", line).strip()
                items.append(ParentNode("li", text_to_children(item_text)))
            html_list.append(ParentNode("ol", children=items))

    return ParentNode("div", children=html_list)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = [text_node_to_html_node(tn) for tn in text_nodes]
    return children
