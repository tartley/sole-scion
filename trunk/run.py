#!/usr/bin/python -O

from sys import argv, exit, path

from solescion.application import title
print title

if '-v' in argv or '--version' in argv:
    exit(0)

from solescion.controller.gameloop import Gameloop

def main():
    gameloop = Gameloop()
    gameloop.init(title)
    try:
        gameloop.run()
    finally:
        gameloop.dispose()


if __name__ == "__main__":
    main()

