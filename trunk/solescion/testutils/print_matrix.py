#!/usr/bin/env python

from TerminalController import TerminalController


def print_matrix():
    t = TerminalController()
    t.render('This is ${GREEN}GREEN${NORMAL}')
    backcolors = [
        '', t.BG_BLACK, t.BG_BLUE, t.BG_GREEN, t.BG_CYAN,
        t.BG_RED, t.BG_MAGENTA, t.BG_YELLOW, t.BG_WHITE,
    ]
    forecolors = [
        t.BLACK, t.BLUE, t.GREEN, t.CYAN, t.RED, t.MAGENTA, t.YELLOW, t.WHITE,
    ]
    for back in backcolors:
        for fore in forecolors:
            print back + fore + 'Hey',
            print t.BOLD + 'Hey' + t.NORMAL,
        print


if __name__ == '__main__':
    print_matrix()

