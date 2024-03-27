from yosemite.tools.text import Text

def main():
    text = Text()
    text.say("Yosemite", color="rgb(255, 165, 0)", bold=True)
    text.say("Hammad Saeed", color="rgb('128', '128', '128')", italic=True)
    text.say("0.1.xxx - Half Dome", color="rgb('128', '128', '128')", italic=True)
        
if __name__ == "__main__":
    main()