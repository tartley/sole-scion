# Model ---------------------------------------------------

from __future__ import division
from random import uniform

import pymunk
from pymunk.vec2d import Vec2d


class World(object):

    def __init__(self):
        pymunk.init_pymunk()
        self.space = pymunk.Space()
        self.space.gravity = Vec2d(0.0, -500.0)
        self.segments = [self.spawn_slope()]
        self.balls = []
        self.next_ball_in = 10


    def spawn_slope(self):
        # spawn the slope
        body = pymunk.Body(1e100, 1e100)
        l1 = Vec2d(-500, 300)
        l2 = Vec2d(+500, 500)
        shape = pymunk.Segment(body, l1, l2, 0.0)
        shape.friction = 0.99
        shape.elasticity = 0.5
        self.space.add_static(shape)
        return shape


    def free(self):
        for index in range(len(self.balls)):
            ball = self.balls.pop()
            del ball
        del self.segments[0]
        del self.space


    def tick(self, dt):
        # spawn new balls every so often
        self.next_ball_in -= 1
        if self.next_ball_in <= 0:
            self.next_ball_in = 10
            self.balls.append(self.spawn_ball())

        self.space.step(1.0/30.0)

        # remove balls that have fallen offscreen
        for i in range(len(self.balls) - 1, -1, -1):
            ball = self.balls[i]
            if ball.body.position.y + ball.radius < 0:
                self.space.remove(ball, ball.body)
                self.balls.remove(ball)


    def spawn_ball(self):
        radius = 20.0 + random.expovariate(1/50.0)
        mass = radius * radius
        inertia = pymunk.moment_for_circle(mass, 0, radius, Vec2d(0,0))
        body = pymunk.Body(mass, inertia)
        body.position = -1000, 1400
        body.angle = uniform(0.0, 2*pi)
        body.velocity = uniform(100.0, 800.0), 0
        body.angular_velocity = uniform(-1.0, +1.0)
        shape = pymunk.Circle(body, radius, Vec2d(0,0))
        shape.friction = 0.99
        shape.elasticity = 0.5
        self.space.add(body, shape)
        return shape


# View -----------------------------------------------------

from math import cos, pi, sin

import pyglet
from pyglet.gl import *


class Camera(object):

    def __init__(self, window):
        self.window = window
        self.x = 0.0
        self.y = 800.0
        self.rot = 0.0
        self.zoom = 800


    def worldProjection(self):
        widthRatio = self.window.width / self.window.height
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(
            -self.zoom * widthRatio,
            self.zoom * widthRatio,
            -self.zoom,
            self.zoom)
        self.focus()

    def focus(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(
            self.x, self.y, +1.0,
            self.x, self.y, -1.0,
            sin(self.rot), cos(self.rot), 0.0)


renderer = None

def on_draw():
    renderer.draw()


class Renderer(object):

    def __init__(self, world):
        global renderer
        renderer = self

        self.world = world

        self.window = pyglet.window.Window(
            resizable=True, fullscreen=False, vsync=True)
        self.window.on_draw = on_draw

        self.camera = Camera(self.window)
        self.camera.worldProjection()

        glEnable(GL_BLEND)
        glClearColor(0.0, 0.0, 0.5, 0.0)


    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.camera.worldProjection()

        self.draw_slope(self.world.segments[0])

        for ball in self.world.balls:
            self.draw_ball(ball)


    def draw_slope(self, slope):
        glColor3f(0.3, 0.2, 0.1)
        glBegin(GL_TRIANGLES)
        glVertex2f(slope.a[0], slope.a[1])
        glVertex2f(slope.b[0], slope.b[1])
        glVertex2f(slope.b[0], slope.a[1])
        glVertex2f(self.window.width, self.window.height)
        glEnd()


    def draw_ball(self, ball):
        x = ball.body.position.x
        y = ball.body.position.y
        a = ball.body.angle

        glPushMatrix()
        glTranslatef(x, y, 0)
        glRotatef(a*180.0/pi, 0, 0, 1)

        segs = 32
        coef = 2.0 * pi / segs
        colors = [(1.0, 1.0, 0.0), (0, 0, 0)]
        colorIdx = 0
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(*colors[0])
        glVertex2f(0, 0)
        for n in range(segs + 1):
            rads = n * coef
            if n % 8 == 0:
                colorIdx += 1
                color = colors[colorIdx % 2]
                glColor3f(*color)
            glVertex2f(ball.radius * cos(rads),
                       ball.radius * sin(rads))
        glVertex2f(0, 0)
        glEnd()

        glPopMatrix()


# Controller ----------------------------------------------

import sys, random

from pyglet import app, clock


class Application(object):

    def __init__(self):
        self.world = World()
        self.renderer = Renderer(self.world)
        print "Loaded Pyglet %s" % (pyglet.version,)
        print "Loaded Pymunk %s" % (pymunk.version,)


    def run(self):
        clock.schedule(self.world.tick)
        clock.set_fps_limit(30)
        app.run()
        self.world.free()


def main():
    app = Application()
    exitVal = app.run()
    return exitVal


if __name__ == '__main__':
    sys.exit(main())



