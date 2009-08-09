
from os import listdir
from os.path import join

from solescion.geom.svgload.svg_parser import SvgParser

def load_graphics():
    graphics = {}
    parser = SvgParser()
    for file in listdir('data'):
        if file.endswith('.svg'):
            print 'file', file
            svg = parser.parse(join('data', file))
            graphics[file[:-4]] = svg
    return graphics

