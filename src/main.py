import os
import shutil
from textnode import TextType, TextNode
from block_markdown import markdown_to_html_node
from htmlnode import HTMLNode

def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")

    path_creator("./static", "./public")
    generate_page(
        "content/index.md",
        "template.html",
        "public/index.html"
    )

def path_creator(source_path, destination_path):
    source_list = os.listdir(source_path)
    for item in source_list:
        full_source_path = os.path.join(source_path, item)
        full_destination_path = os.path.join(destination_path, item)
        if os.path.isfile(full_source_path):
            print(full_source_path)
            shutil.copy(full_source_path, full_destination_path)
        else:
            if not os.path.exists(full_destination_path):
                os.mkdir(full_destination_path)
            path_creator(full_source_path, full_destination_path)

def extract_title(markdown):
    md_lines = markdown.split("\n")
    for line in md_lines:
        if line.strip().startswith("# "):
            return line.strip().replace("# ","",1).strip()
    raise Exception("no title found")
        
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()

    html_content = markdown_to_html_node(md_content).to_html()
    
    title = extract_title(md_content)

    page_html = template_content.replace("{{ Title }}", title)
    page_html = page_html.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page_html)

if __name__ == "__main__":
    main()