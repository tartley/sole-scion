import xml.dom.minidom

from pyglet.graphics import Batch

from bounds import Bounds
from path import PathParser



def svg2batch(filename):
    '''
    filename: string, absolute or relative filename of an SVG file
    return a pyglet Batch made from all the paths in the file
    '''
    loader = SvgBatch(filename)
    return loader.create_batch()



class SvgBatch(object):
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
        self.bounds = Bounds()
        self.batch = None

    @property
    def width(self):
        return self.bounds.width

    @property
    def height(self):
        return self.bounds.height


    def parse_svg(self):
        '''
        Populates self.paths from the <path> tags in the svg file.
        '''
        doc = xml.dom.minidom.parse(self.filename)       
        path_tags = doc.getElementsByTagName('path')
        for path_tag in path_tags:
            parser = PathParser()
            id, path = parser.parse(path_tag)
            self.paths[id] = path
            self.path_order.append(id)


    def create_batch(self):
        '''
        Returns a new pyglet Batch object populated with indexed GL_TRIANGLES
        '''
        if self.batch is None:
            self.batch = Batch()
            self.parse_svg()
            for name in self.path_order:
                path = self.paths[name]
                path.add_to_batch(self.batch)
        return self.batch    

