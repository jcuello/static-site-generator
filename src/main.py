import textnode
from textnode import TextType

def main():
  text_node = textnode.TextNode(
    "This is some anchor text", 
    TextType.LINK, 
    "https://www.boot.dev"
  )
  print(text_node)

if __name__ == "__main__":
  main()