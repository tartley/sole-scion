
import xml.dom.minidom

from path_parser import PathParser


class SvgParser(object):
    '''
    Maintains an ordered list of paths, each one corresponding to a path tag
    from an SVG file. Creates a pylget Batch containing all these paths, for
    rendering as a single OpenGL GL_TRIANGLES indexed vert primitive.
    '''
    def __init__(self, filename=None):
        '''
        filename: string, absolute or relative filename of an SVG file
        '''
        self.filename = filename
        self.paths = {}
        self.path_order = []


    def parse_svg(self):
        '''
        Populates self.paths from the <path> tags in the svg file.
        '''
        doc = xml.dom.minidom.parse(self.filename)       
        path_tags = doc.getElementsByTagName('path')
        parser = PathParser()
        for path_tag in path_tags:
            id, path = parser.parse(path_tag)
            self.paths[id] = path
            self.path_order.append(id)

        boundary = self.paths['boundary']
        x, y = boundary.get_centroid()
        for path in self.paths.values():
            path.offset(-x, -y)


    def add_to_batch(self, batch):
        '''
        Adds paths to the given batch object. They are all added as
        GL_TRIANGLES, so the batch will aggregate them all into a single OpenGL
        primitive.
        '''
        for name in self.path_order:
            path = self.paths[name]
            path.add_to_batch(batch)

