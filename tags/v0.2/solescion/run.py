#!/usr/bin/python -O

from application import name, version
desc = "%s v%s" % (name, version)
print desc

from controller.gameloop import Gameloop

def main():
    Gameloop(desc).run()

if __name__ == "__main__":
    main()

