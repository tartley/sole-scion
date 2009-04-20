
all_materials = set()

class Material(object):

    def __init__(self, name, density, elast, frict, color):
        self.name = name
        self.density = density
        self.elasticity = elast
        self.friction = frict
        self.color = color
        all_materials.add(self)
        globals()[name] = self

#        name      density  elastic fricti color
Material('air',     0.0013, 0.0,    0.1,   (  0,  50, 100))
Material('bamboo',  0.35,   0.2,    0.4,   (150, 130,  50))
Material('flesh',   1.5,    0.3,    1.0,   (  0, 127,   0))
Material('gold',   19.0,    0.2,    0.5,   (255, 255,   0))
Material('granite', 2.7,    0.6,    1.0,   (100,  80,  70))
Material('ice',     0.92,   0.2,    0.1,   (200, 210, 255))
Material('rubber',  1.5,    1.6,   10.0,   ( 20, 130, 200))
Material('steel',   7.7,    0.3,    1.0,   ( 90, 150, 200))

