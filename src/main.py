from textnode import *

def main():
    dummy = TextNode("This is a text node", TextType.BOLD, 'https://www.google.com')

    print(dummy)

if __name__ == '__main__':
    main()