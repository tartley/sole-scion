from __future__ import division
from math import pi
from random import uniform

from pymunk import \
    Body, Circle, init_pymunk, moment_for_circle, Segment, Space, \
    version as pymunk_version
from pymunk.vec2d import Vec2d
print "Loaded Pymunk %s" % (pymunk_version,)


class Colors(object):
    White = (1,1,1)
    Black = (0,0,0)


FPS_LIMIT = 30

class World(object):

    def __init__(self):
        init_pymunk()
        self.space = Space()
        self.space.gravity = Vec2d(0.0, -900.0)
        self.segments = self.spawn_slope()
        self.balls = []
        self.stars = [
            (
                0.5 + random.random()/2,
                -1500+3000*random.random(),
                1600*random.random(),
            ) for _ in range(200)
        ]
        self.next_ball_in = 1
        self.tick_times = []


    def spawn_slope(self):
        # spawn the slope
        body = Body(1e100, 1e100)
        heights = [300+cos(x-10.5)*400*1/(1+abs(x-10.5)) for x in range(21)]
        old_height = 0
        slopes = []
        for i in range(0, len(heights)-1):
            l1 = Vec2d(-1280 + i*128, heights[i])
            l2 = Vec2d(-1280 + (i+1)*128, heights[i+1])
            shape = Segment(body, l1, l2, 0.0)
            shape.friction = 0.8
            shape.elasticity = 0.8
            self.space.add_static(shape)
            slopes.append(shape)

        return slopes


    def free(self):
        # print "Ticks:", ", ".join("%.1f" % (dt*1000) for dt in self.tick_times)
        for index in range(len(self.balls)):
            ball = self.balls.pop()
            del ball
        del self.segments[0]
        del self.space


    def tick(self, dt):
        if controller.paused:
            return

        self.tick_times.append(dt)

        # spawn new balls every so often
        self.next_ball_in -= 1
        if self.next_ball_in <= 0:
            self.next_ball_in = 15
            self.balls.append(self.spawn_ball())

        self.space.step(1/FPS_LIMIT)

        # remove balls that have fallen offscreen
        for i in range(len(self.balls) - 1, -1, -1):
            ball = self.balls[i]
            if ball.body.position.y + ball.radius < 0:
                self.space.remove(ball, ball.body)
                self.balls.remove(ball)


    def spawn_ball(self):
        radius = 50 + random.expovariate(1/50.0)
        mass = radius * radius
        inertia = moment_for_circle(mass, 0, radius, Vec2d(0,0))
        body = Body(mass, inertia)
        body.position = -1000, 1800
        body.angle = uniform(0.0, 2*pi)
        body.velocity = uniform(100.0, 800.0), 0
        body.angular_velocity = uniform(-1.0, +1.0)
        shape = Circle(body, radius, Vec2d(0,0))
        shape.friction = 0.8
        shape.elasticity = 0.8
        shape.color = (random.random(), random.random(), random.random())
        self.space.add(body, shape)
        return shape


# View -----------------------------------------------------

from math import cos, pi, sin

from pyglet import clock, window
from pyglet.gl import *


class Camera(object):

    def __init__(self, window):
        self.window = window
        self.x = 0.0
        self.y = 800.0
        self.rot = 0.0
        self.zoom = 800
        self.worldProjection()


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


class Renderer(object):

    def __init__(self, world, window):
        self.world = world
        self.window = window
        self.window.on_draw = lambda: self.draw()
        self.camera = Camera(self.window)
        self.clockDisplay = clock.ClockDisplay()

        glEnable(GL_BLEND)
        glClearColor(0.5, 0.2, 0.4, 0.0)


    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        self.camera.worldProjection()

        self.draw_world(self.world)

        for ball in self.world.balls:
            self.draw_ball(ball)

        self.clockDisplay.draw()


    def draw_world(self, world):

        # sky
        glColor3f(0, 0.0, 1)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(-1300, -000)
        glVertex2f(+1300, -000)
        glColor3f(0, 0, 0.2)
        glVertex2f(+1300, +1600)
        glVertex2f(-1300, +1600)
        glEnd()

        # stars
        glBegin(GL_POINTS)
        for star in world.stars:
            glColor3f(star[0], star[0], star[0])
            glVertex2f(star[1], star[2])
        glEnd()

        # ground
        origcolor = [0.3, 0.2, 0.1]
        colorheight = 400
        for slope in world.segments:
            glBegin(GL_TRIANGLES)
            if slope.a[1] > slope.b[1]:
                glColor3f(*(c * slope.b[1]/colorheight for c in origcolor))
                glVertex2f(slope.a[0], slope.b[1])
            else:
                glColor3f(*(c * slope.a[1]/colorheight for c in origcolor))
                glVertex2f(slope.b[0], slope.a[1])
            glColor3f(*(c * slope.b[1]/colorheight for c in origcolor))
            glVertex2f(slope.b[0], slope.b[1])
            glColor3f(*(c * slope.a[1]/colorheight for c in origcolor))
            glVertex2f(slope.a[0], slope.a[1])

            glColor3f(*(c * min(slope.a[1], slope.b[1])/colorheight for c in origcolor))
            glVertex2f(slope.a[0], min(slope.a[1], slope.b[1]))
            glColor3f(0,0,0)
            glVertex2f(slope.a[0], 0)
            glVertex2f(slope.b[0], 0)

            glColor3f(0,0,0)
            glVertex2f(slope.b[0], 0)
            glColor3f(*(c * min(slope.a[1], slope.b[1])/colorheight for c in origcolor))
            glVertex2f(slope.a[0], min(slope.a[1], slope.b[1]))
            glVertex2f(slope.b[0], min(slope.a[1], slope.b[1]))

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
        colors = [
            (0.1, 0.1, 0.1),
            (0.0, 0.0, 0.0),
        ]
        colorIdx = 0
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(*ball.color)
        glVertex2f(0, 0)
        glColor3f(*Colors.Black)
        for n in range(segs + 1):
            rads = n * coef
            if n % 4 == 0:
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

from pyglet import app, clock, version as pyglet_version, window
from pyglet.window import key
print "Loaded Pyglet %s" % (pyglet_version,)

controller = None

class Controller(object):

    def __init__(self):
        global controller
        self.paused = False
        controller = self
        self.world = World()
        self.window = window.Window(
            fullscreen=True,
            vsync=True,
            resizable=True,
            caption="Sole Scion",
            visible=False,
        )
        self.window.on_key_press = lambda *a: self.on_key_press(*a)
        self.window.set_exclusive_mouse(True)
        clock.schedule_interval(self.world.tick, 1/FPS_LIMIT)
        self.renderer = Renderer(self.world, self.window)


    def run(self):
        self.window.set_visible(True)
        app.run()
        self.world.free()


    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.window.close()
        elif symbol == key.RETURN or symbol == key.ENTER:
            if modifiers & (key.LALT | key.RALT):
                self.window.set_fullscreen(not self.window.fullscreen)
        elif symbol == key.SPACE:
            self.paused = not self.paused


def main():
    myapp = Controller()
    return myapp.run()


if __name__ == '__main__':
    sys.exit(main())



