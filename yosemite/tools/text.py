import libhammadpy_text
from art import text2art
import sys
import random

class Text:
    """
    Dynamic, interchangable text styling for the terminal. Compatible with RGB, background colors, bold, italic, and underline text.
    
    Attributes:
        say: A method to style and print a single line of text.
        list: A method to style and print a list of items.
        splash: A method to create an ASCII art styled Splash 'Logo' in the terminal.
    """
    def say(self, message, color="white", bg=None, bold=False, italic=False, underline=False):
        """
        Style and print a single line of text.

        Example:
            ```python
            from yosemite.tools.text import Text

            text = Text()
            text.say("Hello, World!", color="red", bg="white", bold=True)
            ```

            ```bash
            Hello, World!
            ```

        Args:
            message (str): The message to be styled and printed.
            color (str, optional): The color of the text. Defaults to "white".
            bg (str, optional): The background color of the text. Defaults to None.
            bold (bool, optional): Whether the text should be bold. Defaults to False.
            italic (bool, optional): Whether the text should be italic. Defaults to False.
            underline (bool, optional): Whether the text should be underlined. Defaults to False.
        """
        styled_message = libhammadpy_text.format_text(message, color, bg, bold, italic, underline)
        print(styled_message)

    def list(self, items, color="white", bg=None, bold=False, italic=False, underline=False):
        """
        Style and print a list of items.

        Example:
            ```python
            from yosemite.tools.text import Text

            text = Text()
            text.list(["apple", "banana", "cherry"], color="green", bg="black", bold=True)
            ```

            ```bash
            apple
            banana
            cherry
            ```

        Args:
            items (list): The items to be styled and printed.
            color (str, optional): The color of the text. Defaults to "white".
            bg (str, optional): The background color of the text. Defaults to None.
            bold (bool, optional): Whether the text should be bold. Defaults to False.
            italic (bool, optional): Whether the text should be italic. Defaults to False.
            underline (bool, optional): Whether the text should be underlined. Defaults to False.
        """
        styled_items = libhammadpy_text.format_list(items, color, bg, bold, italic, underline)
        for item in styled_items:
            print(item)

    def splash(self, message: str = "hammadpy", art: str = "random", color: str = "white", bg: str = None, bold: bool = False, italic: bool = False, underline: bool = False):
        """
        Creates an ASCII art styled Splash 'Logo' in the terminal.

        Example:
            ```python
            from yosemite.tools.text import Text
            
            text = Text()
            text.splash("hammadpy", art="random", color="white", bg="black", bold=True)
            ```

        Args:
            message (str): The message to display in the splash.
            art (str): The ASCII art style to use.
            color (str): Text color (e.g., 'red', 'blue').
            bg (str): Background color (e.g., 'red', 'blue').
            bold (bool): Whether the text should be bold.
            italic (bool): Whether the text should be italic.
            underline (bool): Whether the text should be underlined.
        """
        if art == "random":
            fonts = ["block", "caligraphy", "doh", "dohc", "doom", "epic", "fender", "graffiti", "isometric1", "isometric2", "isometric3", "isometric4", "letters", "alligator", "dotmatrix", "bubble", "bulbhead", "digital", "ivrit", "lean", "mini", "script", "shadow", "slant", "speed", "starwars", "stop", "thin", "3-d", "3x5", "5lineoblique", "acrobatic", "alligator2", "alligator3", "alphabet", "banner", "banner3-D", "banner3", "banner4", "barbwire", "basic", "bell", "big", "bigchief", "binary", "block", "broadway", "bubble", "caligraphy", "doh", "dohc", "doom", "dotmatrix", "drpepper", "epic", "fender", "graffiti", "isometric1", "isometric2", "isometric3", "isometric4", "letters", "alligator", "dotmatrix", "bubble", "bulbhead", "digital", "ivrit", "lean", "mini", "script", "shadow", "slant", "speed", "starwars", "stop", "thin"]
            art = random.choice(fonts)

        art_message = text2art(message, font=art)
        self.say(art_message, color=color, bg=bg, bold=bold, italic=italic, underline=underline)

def main():
    text = Text()
    text.say("Yosemite", color="rgb(255, 165, 0)", bold=True)
    text.say("Hammad Saeed", color="rgb('128', '128', '128')", italic=True)
    text.say("0.1.x - Half Dome", color="rgb('128', '128', '128')", italic=True)
    text.say("The Yosemite CLI Interface is still being developed :)", color="rgb(255, 165, 0)", bold=True)

if __name__ == "__main__":
    main()
