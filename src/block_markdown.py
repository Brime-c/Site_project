from textnode import TextNode, TextType

def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")
    final_block_list = []
    for block in block_list:
        block = block.strip()
        if block != "":
            final_block_list.append(block)
            
    return final_block_list

