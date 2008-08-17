#!/usr/bin/python -O

from sys import argv, exit

from application import title

if '-v' in argv or '--version' in argv:
    print title
    exit(0)

from controller.gameloop import Gameloop

def main():
    Gameloop(title).run()

if __name__ == "__main__":
    main()

