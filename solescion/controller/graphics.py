
from os import listdir
from os.path import join

from solescion.geom.svgload.svgparser import SvgParser

def load_graphics():
    graphics = {}
    for file in listdir('data'):
        if file.endswith('.svg'):
            svg = SvgParser(join('data', file))
            svg.parse_svg()
            graphics[file[:-4]] = svg
    return graphics

