from textnode import TextType, TextNode

if (__name__ == "__main__"):
    #HERE
    text1 = TextNode("Here's a link", TextType.LINK, "https://nothing_is_here.com")
    print(text1)
