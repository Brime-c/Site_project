import re
from enum import Enum
from textnode import TextNode, TextType
from htmlnode import HTMLNode
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
    block_type = block_to_block(markdown)
    for block in blocks:
        if block_type == BlockType.HEADING:
            pass