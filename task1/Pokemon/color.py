RESET   = "\033[0m"
OPPONENT     = "\033[91m"
PLAYER    = "\033[94m"

POSITION = {
    "player":"player",
    "opponent":"computer"
}

def color(text, color):
    return f"{color}{text}\033[0m"
