from yosemite_tiny.tools.text import Text
from yosemite_tiny.tools.load import Loader, Timer
from yosemite_tiny.tools.input import Input, Dialog

class Yosemite:
    """
    The core entrypoint for Yosemite tools.

    Example:
        ```python
        # Import Yosemite
        from yosemite import Yosemite

        # Initialize Yosemite
        core = Yosemite()

        # Styled Text
        core.say("Hello, Yosemite!" color="blue", bg="white", bold=True, italic=True, underline=True)

        # List
        list_items = ["This is a list", "With some items", "And some colors"]
        core.list(list_items, color="blue", bg="white", bold=True)

        # ASCII Art
        core.art("yosemite", art="random", color="rgb(255, 0, 0)")

        # Loaders
        with core.loader("Loading..."):
            time.sleep(2)

        # Inputs
        name = core.input.ask("What is your name?")

        # Dialogs
        if core.dialog.confirm("Do you want to continue?"):
            core.say(f"Hello, {name}!")
        else:
            core.say("Goodbye!")
        ```

    Methods:
        art: A method to display ASCII art. 
        say: A method to display styled text.
        list: A method to display a list of items.
        loader: A class to display loading animations. (Depreciated)
        timer: A context manager to time code execution. 
        inputs: A class to handle user inputs.
        dialog: A class to display dialogs.

    API Reference:
        [Art Styles](./api/tools/yosemite.tools.text.md) <br>
        [Text Styles](./api/tools/yosemite.tools.text.md) <br>
        [Loaders](./api/tools/yosemite.tools.load.md) <br>
        [Timer](./api/tools/yosemite.tools.load.md) <br>
        [Inputs](./api/tools/yosemite.tools.input.md) <br>
        [Dialogs](./api/tools/yosemite.tools.input.md) <br>
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
    with core.loader(message="Loading...") as status:
        time.sleep(2)
        pass

    with core.loader(styles="emoji", color="yellow") as status:
        time.sleep(2)
        pass

    
    # Inputs
    core.input.pause()
    core.input.confirm("Do you want to continue?")
