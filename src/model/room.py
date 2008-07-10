from model.entity import Entity

class Room(Entity):

    color = (0.3, 0.2, 0.0)

    def __init__(self, verts):
        if len(verts) < 3:
            raise TypeError("need 3 or more verts")
        self.verts = verts

