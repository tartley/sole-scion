import re
from sys import stdout

from solescion.testutils.TerminalController import TerminalController


class ColoredStream(object):

    def __init__(self, highlights, stream=stdout):
        self.highlights = highlights
        self.stream = stream
        for item in highlights:
            item[0] = re.compile('(' + item[0] + ')')
        self.term = TerminalController()

    def write(self, text, *args):
        for regex, highlight in self.highlights:
            text = regex.sub(highlight + '\g<1>' + self.term.NORMAL, text)
        self.stream.write(text, *args)

    def flush(self):
        pass

