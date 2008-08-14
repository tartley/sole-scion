#!/usr/bin/python -O
"Runs the program"

from controller.gameloop import Gameloop

def main():
    "Call this to run the program"
    Gameloop("Sole Scion").run()

if __name__ == "__main__":
    main()
