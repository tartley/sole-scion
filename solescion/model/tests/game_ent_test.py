from pymunk.vec2d import Vec2d

from solescion.model.game_ent import GameEnt
from solescion.testutils.testcase import MyTestCase, run


class GameEnt_test(MyTestCase):

    def testInit(self):
        ent = GameEnt()
        self.assertEquals(ent.position, Vec2d(0, 0))
        self.assertEquals(ent.angle, 0.0)
        self.assertNone(ent.batch)


if __name__ == "__main__":
    run(GameEnt_test)

