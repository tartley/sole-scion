from pyglet.gl import GLfloat, glGetFloatv, GL_COLOR_CLEAR_VALUE

import fix_pythonpath

from testutils.testcase import MyTestCase, run_test

from view.renderer import Renderer


class Renderer_test(MyTestCase):

    def testSemantics(self):
        one = (GLfloat * 4)(*[1, 2, 3, 4])
        two = (GLfloat * 4)(*[1, 2, 3, 4])


    def testConstructor(self):
        window = object()
        renderer = Renderer(window)
        self.assertTrue(renderer.window is window, "should store window")

        clearColor = (GLfloat * 4)(*[0, 0, 0, 0])
        glGetFloatv(GL_COLOR_CLEAR_VALUE, clearColor)
        expected = (GLfloat * 4)(*[0.0, 0.0, 1.0, 1.0])
        self.assertEquals(clearColor, expected, "should set clear color")


    def testDraw(self):
        self.fail("not done")


if __name__ == "__main__":
    run_test()

