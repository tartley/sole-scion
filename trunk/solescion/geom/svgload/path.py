
from solescion.geom.loop import Loop
from solescion.geom.path import ColoredPath


class ParseError(Exception):
    pass


class PathDataParser(object):

    def __init__(self):
        self.data = None
        self.pos = 0

    def get_char(self, allowed):
        if self.pos < len(self.data) and self.data[self.pos] in allowed:
            self.pos += 1
            return self.data[self.pos - 1]

    def get_chars(self, allowed):
        start = self.pos
        while self.get_char(allowed):
            pass
        return self.data[start:self.pos]

    def get_number(self):
        number = None
        start = self.get_char('0123456789.-')
        if start:
            number = start
            finish = self.get_chars('0123456789.')
            if finish:
                number += finish
        if '.' in number:
            return float(number)
        else:
            return int(number)

    def to_tuples(self, data):
        '''
        path_data : string, from an svg path tag's 'd' attribute, eg:
            'M 46,74 L 35,12 l 53,-13 z'
        returns the same data collected in a list of tuples, eg:
            [ ('M', 46, 74), ('L', 35, 12), ('l', 53, -13), ('z') ],
        The input data may have floats instead of ints, this will be reflected
        in the output. The input may have its whitespace stripped out, or its
        commas replaced by whitespace.
        '''
        self.data = data
        self.pos = 0
        parsed = []
        command = []

        while self.pos < len(self.data):
            indicator = self.data[self.pos]
            if indicator == ' ':
                self.pos += 1
            elif indicator == ',':
                if len(command) >= 2:
                    self.pos += 1
                else:
                    msg = 'unexpected comma at %d in %r' % (self.pos, self.data)
                    raise ParseError(msg)
            elif indicator in '0123456789.-':
                if command:
                    command.append(self.get_number())
                else:
                    msg = 'missing command at %d in %r' % (self.pos, self.data)
                    raise ParseError(msg)
            else:
                if command:
                    parsed.append(tuple(command))
                command = [indicator]
                self.pos += 1

        if command:
            parsed.append(tuple(command))
        return parsed


class LoopTracer(object):

    def __init__(self):
        self.loops = []

    def get_point(self, command):
        x = command[1]
        y = -command[2]
        return x, y

    def onMove(self, command):
        x, y = self.get_point(command)
        self.current_loop = [(x, y)]

    def onLine(self, command):
        x, y = self.get_point(command)
        self.current_loop.append((x, y))

    def onClose(self, command):
        if self.current_loop[0] == self.current_loop[-1]:
            self.current_loop = self.current_loop[:-1]
        if len(self.current_loop) < 3:
            raise ParseError('loop needs 3 or more verts')
        loop = Loop(self.current_loop)
        if not loop.is_clockwise():
            loop.verts.reverse()
        self.loops.append(loop)
        self.current_loop = None

    def onBadCommand(self, action):
        msg = 'unsupported svg path command: %s' % (action,)
        raise ParseError(msg) 

    def to_loops(self, commands):
        '''
        commands : list of tuples, as output from to_tuples() method, eg:
            [('M', 1, 2), ('L', 3, 4), ('L', 5, 6), ('z')]
        Interprets the command characters at the start of each tuple to return
        a list of loops, where each loop is a closed list of verts, and each
        vert is a pair of ints or floats, eg:
            [[1, 2, 3, 4, 5, 6]]
        Note that the final point of each loop is eliminated if it is equal to
        the first.
        SVG defines commands:
            M x,y: move, start a new loop
            L x,y: line, draw boundary
            H x: move horizontal
            V y: move vertical
            Z: close current loop - join to start point
        Lower-case command letters (eg 'm') indicate a relative offset.
        See http://www.w3.org/TR/SVG11/paths.html
        '''
        lookup = {
            'M': self.onMove,
            'L': self.onLine,
            'Z': self.onClose,
            'z': self.onClose,
        }
        self.loops = []
        self.current_loop = None

        for command in commands:
            action = command[0]
            if action in lookup:
                lookup[action](command)
            else:
                self.onBadCommand(action)
        return self.loops



class PathParser(object):
    '''
    parse(path_tag) returns an SvgPath object()
    '''
    next_id = 1


    def get_id(self, attributes):
        if 'id' in attributes.keys():
            return attributes['id'].value
        else:
            self.next_id += 1
            return self.next_id - 1


    def parse_color(self, color):
        '''
        color : string, eg: '#rrggbb' or 'none'
        (where rr, gg, bb are hex digits from 00 to ff)
        returns a triple of unsigned bytes, eg: (0, 128, 255)
        '''
        if color == 'none':
            return None
        return (
            int(color[1:3], 16),
            int(color[3:5], 16),
            int(color[5:7], 16))


    def parse_style(self, style):
        '''
        style : string, eg:
            fill:#ff2a2a;fill-rule:evenodd;stroke:none;stroke-width:1px;
            stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1
        returns color as a triple of unsigned bytes: (r, g, b), or None
        '''
        style_elements = style.split(';')
        while style_elements:
            element = style_elements.pop()
            if element.startswith('fill:'):
                return self.parse_color(element[5:])
        return None


    def parse(self, tag):
        '''
        returns (id, path)
        where:  'id' is the path tag's id attribute
                'path' is a populated instance of SvgPath
        '''
        path = ColoredPath()
        id = self.get_id(tag.attributes)

        if 'style' in tag.attributes.keys():
            style_data = tag.attributes['style'].value
            path.color = self.parse_style(style_data)
        
        parser = PathDataParser()
        path_data = tag.attributes['d'].value
        path_tuple = parser.to_tuples(path_data)

        tracer = LoopTracer()
        path.loops = tracer.to_loops(path_tuple)

        return id, path

