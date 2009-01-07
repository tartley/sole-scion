
class Material(object):

    def __init__(self, density, elast, frict, color):
        self.density = density
        self.elasticity = elast
        self.friction = frict
        self.color = color

__crazyWeight = 0.5

# name             density               elasti fricti  color
air     = Material( 0.0013 * __crazyWeight, 0.0,    0.1,   (  0,  50, 100))
bamboo  = Material( 0.35 * __crazyWeight,   0.2,    0.4,   (150, 130,  50))
flesh   = Material( 1.5 * __crazyWeight,    0.3,    1.0,   (  0, 127,   0))
gold    = Material(19.0 * __crazyWeight,    0.5,    0.5,   (255, 255,   0))
granite = Material( 2.7 * __crazyWeight,    0.5,    2.0,   (100,  80,  70))
ice     = Material( 0.92 * __crazyWeight,   0.5,    0.1,   (200, 210, 255))
rubber  = Material( 1.5 * __crazyWeight,    1.0,   10.0,   ( 20, 130, 200))
steel   = Material( 7.7 * __crazyWeight,    0.5,    1.0,   ( 90, 150, 200))

