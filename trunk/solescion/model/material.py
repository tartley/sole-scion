
class Material(object):

    _crazyWeight = 0.5

    def __init__(self, density, elast, frict, color):
        self.density = density
        self.elasticity = elast
        self.friction = frict
        self.color = color

# name                       density elasti fricti  color
Material.air     = Material( 0.0013, 0.0,    0.1,   (  0,  50, 100))
Material.bamboo  = Material( 0.35,   0.2,    0.4,   (150, 130,  50))
Material.flesh   = Material( 1.5,    0.3,    1.0,   (  0, 127,   0))
Material.gold    = Material(19.0,    0.5,    0.5,   (255, 255,   0))
Material.granite = Material( 2.7,    0.5,    2.0,   (100,  80,  70))
Material.ice     = Material( 0.92,   0.5,    0.1,   (200, 210, 255))
Material.rubber  = Material( 1.5,    1.0,   10.0,   ( 20, 130, 200))
Material.steel   = Material( 7.7,    0.5,    1.0,   ( 90, 150, 200))

