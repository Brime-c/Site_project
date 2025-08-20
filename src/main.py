import os
import shutil
from textnode import TextType, TextNode

def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")

    return path_creator("./static", "./public")

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
if __name__ == "__main__":
    main()