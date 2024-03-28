from yosemite.tools.text import Text
import threading
import time
import sys

class Loader:
    """Displays a simple animated loading placeholder. Now depreciated. Use 'alive-progress' instead.

    ```bash
    pip install alive-progress
    ```
    
    Attributes:
        message (str): The message to be displayed while loading.
        color (str): The color of the loading animation.
        animation (str): The animation to be displayed while loading.
        styles (str): The style of the animation to be displayed while loading.
    """

    def __init__(self, message: str = "Loading...", color: str = "white", animation: str = "|/-\\", styles: str = None):
        """
        Generates a simple animated loading placeholder.

        Example:
            ```python
            from yosemite.tools.load import Loader

            loader = Loader()
            with loader:
                time.sleep(2)
                loader.checkpoint("Checkpoint 1")
                time.sleep(2)
            ```

        Args:
            message (str, optional): The message to be displayed while loading. Defaults to "Loading...".
            color (str, optional): The color of the loading animation. Defaults to "white".
            animation (str, optional): The animation to be displayed while loading. Defaults to "|/-\\".
            styles (str, optional): The style of the animation to be displayed while loading. Defaults to None.
        """
        self.say = Text()
        self.timer = Timer()
        self.message = message
        self.color = color
        self.animation = animation
        self.is_running = False
        self.index = 0

        self.say.say("The yosemite.core.modules.loaders module will no longer be updated. I have personally started using the 'alive-progress' module for this purpose.", color="yellow")
        self.say.say("You can install it using 'pip install alive-progress'.", color="yellow", bold=True)

        animations = {
            "blocks": "█▉▊▋▌▍▎▏ ",
            "emoji": "🌑🌒🌓🌔🌕🌖🌗🌘",
            "hourglass": "⏳⌛",
            "dots": "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
            "arrows": "←↖↑↗→↘↓↙",
            "lines": "┤┘┴└├┌┬┐",
            "pipes": "┃┃┃┃┃┃┃┃┃",
            "dots2": "⣾⣽⣻⢿⡿⣟⣯⣷",
            "dots3": "⢄⢂⢁⡁⡈⡐⡠",
            "stars": "✶✸✹✺✹✷",
            "ping": "⚫⚪",
            "hearts": "💗💓💕💖💞💘💝💟",
            "weather": "🌤️🌥️🌦️🌧️⛈️🌩️🌨️☃️",
            "moons": "🌑🌒🌓🌔🌕🌖🌗🌘🌑"
        }

        if styles in animations:
            self.animation = animations[styles]

    def __enter__(self):
        self.timer.enter()
        self.is_running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()
        return self

    def _animate(self):
        while self.is_running:
            sys.stdout.write(f"\r{self.message} {self.animation[self.index]}")
            sys.stdout.flush()
            time.sleep(0.1)
            self.index = (self.index + 1) % len(self.animation)

    def __exit__(self, exc_type, exc_value, traceback):
        self.is_running = False
        self.thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\n")
        self.timer.exit()

    def checkpoint(self, message: str):
        """Displays a checkpoint message while the loader is running.
        
        Example:
            ```python
            loader = Loader()
            with loader:
                time.sleep(2)
                loader.checkpoint("Checkpoint 1")
                time.sleep(2)
            ```

        Args:
            message (str): The checkpoint message to be displayed.
        """
        self.is_running = False
        self.thread.join()
        checkpoint_message = f"\r{self.message} {message}\n"
        sys.stdout.write(checkpoint_message)
        sys.stdout.flush()
        time.sleep(1)
        self.is_running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()

class Timer:
    """Measures and prints the execution time of a task.
    
    Example:
        ```python
        from yosemite.tools.load import Timer

        timer = Timer()
        with timer.enter():
            time.sleep(2)
        ```
        
        ```bash
        Task completed in 2.00 seconds.
        ```
        
    Attributes:
        message (str): The message to be displayed while timing.
        """

    def __init__(self, message: str = "Task"):
        self.say = Text()
        self.message = message

    def enter(self):
        self.start_time = time.time()
        return self

    def exit(self):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        message = f"{self.message} completed in {elapsed_time:.2f} seconds."
        self.say.say(message, color="green", bold=True)

if __name__ == "__main__":
    loader = Loader(styles="blocks")
    timer = Timer()

    with loader:
        time.sleep(2)
        loader.checkpoint("Checkpoint 1")
        time.sleep(2)