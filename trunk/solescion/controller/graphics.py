
from os import listdir
from os.path import join

from svgbatch.svgbatch import SvgBatch

def load_graphics():
    graphics = {}
    for file in listdir('data'):
        if file.endswith('.svg'):
            print file
            svg = SvgBatch(join('data', file))
            svg.parse_svg()
            graphics[file[:-4]] = svg
    return graphics

