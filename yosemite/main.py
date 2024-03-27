from yosemite.tools.text import Text
from yosemite.tools.load import Loader, Timer
from yosemite.tools.input import Input, Dialog

class Yosemite:
    """
    The core entrypoint for Yosemite tools.

    Example:
        ```python
        core = Yosemite()
        core.say("Hello, Yosemite!")
        core.say("Hello, Yosemite!", bold=True)
        ```

    Attributes:
        art: A method to display ASCII art.
        say: A method to display styled text.
        list: A method to display a list of items.
        loader: A class to display loading animations. (Depreciated)
        timer: A context manager to time code execution. 
        inputs: A class to handle user inputs.
        dialog: A class to display dialogs.
    """
    def __init__(self):

        # Text Styling
        text = Text()
        self.art = text.splash
        self.say = text.say
        self.list = text.list

        # Loaders
        self.loader = Loader
        self.timer = Timer

        # Inputs
        self.input = Input()

        # Dialogs
        self.dialog = Dialog

        pass

if __name__ == "__main__":
    import time
    import random

    rgb = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    rgb2 = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    rgb = f"rgb{rgb}"
    rgb2 = f"rgb{rgb2}"

    core = Yosemite()
    # Text Styling
    core.art(message="yosemite", art="random", color=rgb)
    time.sleep(1)
    core.say("This has an underline!", underline=True)
    core.say("This is ITALIC!", italic=True)
    list_items = ["This is a list", "With some items", "And some colors"]
    core.list(list_items, color="blue", bg="white", bold=True)
    time.sleep(0.5)

    # Loaders
    with core.status(message="Loading...") as status:
        time.sleep(2)
        pass

    with core.status(styles="emoji", color="yellow") as status:
        time.sleep(2)
        pass

    
    # Inputs
    core.inputs.pause()
    core.inputs.confirm("Do you want to continue?")
