import builtins
import os
from colorama import init

init() 

class BeautifulTerminal:
    COLORS = {
        "reset": "\033[0m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "green": "\033[92m",
        "white": "\033[97m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "magenta": "\033[95m",
        "black": "\033[90m",
        "light_red": "\033[91m",
        "light_green": "\033[92m",
        "light_yellow": "\033[93m",
        "light_blue": "\033[94m",
        "light_cyan": "\033[96m",
        "light_magenta": "\033[95m",
        "dark_gray": "\033[90m",
        "light_gray": "\033[37m",
        "orange": "\033[38;5;208m",
        "purple": "\033[38;5;128m",
        "teal": "\033[38;5;38m",
        "pink": "\033[38;5;206m",
        "brown": "\033[38;5;94m",
        "gold": "\033[38;5;226m",
        "navy": "\033[38;5;17m",
        "dark_green": "\033[38;5;22m",
    }

    def __init__(self):
        self.original_print = builtins.print
        self.is_ise = "powershell_ise" in os.getenv("TERM", "").lower()
        self.enable()

    def enable(self):
        builtins.print = self.custom_print

    def disable(self):
        builtins.print = self.original_print

    def custom_print(self, *args, color=None, **kwargs):
        message = " ".join(map(str, args))
        
        color_code = ""
        if color and not self.is_ise:
            color_code = self.COLORS.get(color.lower(), self.COLORS['reset'])


        if "error" in message.lower() and not self.is_ise or "fehler" in message.lower() and not self.is_ise:
            color_code = self.COLORS['red']
        elif "warn" in message.lower() and not self.is_ise or "warnung" in message.lower() and not self.is_ise:
            color_code = self.COLORS['yellow']
        elif "success" in message.lower() and not self.is_ise or "erfolgreich" in message.lower() and not self.is_ise:
            color_code = self.COLORS['green']

        self.original_print(f"{color_code}{message}{self.COLORS['reset'] if not self.is_ise else ''}", **kwargs)

if __name__ == "__main__":
    BeautifulTerminal()
    print("Das ist ein normaler text.")
    print("Das", "ist", "ein", "blauer", "text" + ".", color="blue")
    print("This is an error message!")
    print("This is a warning message!")
    print("This is a success message!")