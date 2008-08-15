"Module for class 'Materials'"

class Material(object):
    "Define physical properties"
    def __init__(self, density, elast, frict, color):
        self.density = density
        self.elasticity = elast
        self.friction = frict
        self.color = color

class Materials(object):
    "Provide a list of predefined materials"
#   name               density  elasti fricti  color
    Gold    = Material(19.0,    0.4,    0.5,   (255, 255,   0))
    Granite = Material( 2.7,    0.6,    2.0,   (100,  80,  70))
    Rubber  = Material( 1.5,    1.0,   10.0,   ( 20, 130, 200))
    Ice     = Material( 0.92,   0.5,    0.0,   (200, 210, 255))
    Bamboo  = Material( 0.35,   0.5,    0.4,   (150, 130,  50))
    Air     = Material( 0.0013, 0.0,    0.1,   (  0,  50, 100))

