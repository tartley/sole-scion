from model.entity import Entity

class Room(Entity):

    def __init__(self, color, verts):
        if len(color) != 3:
            raise TypeError("bad color: %s" % (color,))
        self.color = color

        if len(verts) < 3:
            raise TypeError("need 3 or more verts")
        self.verts = verts

