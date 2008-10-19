import re
from sys import stdout

from TerminalController import TerminalController
term = TerminalController()

class ColoredStream(object):

    def __init__(self, highlights, stream=stdout):
        self.highlights = highlights
        self.stream = stream
        for item in highlights:
            item[0] = re.compile('(' + item[0] + ')')

    def write(self, text, *args):
        for regex, highlight in self.highlights:
            text = regex.sub(highlight + '\g<1>' + term.NORMAL, text)
        self.stream.write(text, *args)
