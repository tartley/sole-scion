#!/usr/bin/python -O

from sys import argv, exit

from application import name, version
desc = "%s version %s" % (name, version)

if '-v' in argv or '--version' in argv:
    print desc
    exit(0)

from controller.gameloop import Gameloop

def main():
    Gameloop(desc).run()

if __name__ == "__main__":
    main()

