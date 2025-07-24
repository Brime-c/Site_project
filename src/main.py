from textnode import TextType, TextNode

def main():
    node =  TextNode("hello", TextType.BOLD, "https://boot.dev")
    print(node)

if __name__ == "__main__":
    main()