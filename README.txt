=Sole Scion=

http://code.google.com/p/sole-scion/

A three month project to write a 2D vector graphic adventure game with
Newtonian rigid-body dynamics, and a vision to exploit the scaling, toppling,
sliding and rolling of vector shapes. 

Currently at a very early stage of development. Only of interest to enthusiastic
programmers. If it doesn't work for you or you have problems, please let me know - see the 'Contact' section.

Works on Linux and on Windows. Also works under PyPy, with functools installed. Has anyone tried it on a Mac?


==Screenshots==

Version 0.2. Arbitary polygons made up from collections of circles and convex
chunks. Each chunk has a material, which determines its physical properties
(density, friction, elasticity, color.)

http://sole-scion.googlecode.com/svn/trunk/screenshots/SoleScion-screenshot-v0.2.png


A spike of v0.2, circles rain down on a polygonal surface. Note the current
HEAD features arbitrary polygon shapes as well as circles, but does not look as
cutesy as this, since it's missing some superficial features like the gradient
fills, and stars in the background.

http://sole-scion.googlecode.com/svn/trunk/screenshots/SoleScion-screenshot-v0.1.1.spike.png


==Dependencies==

You must install these manually.

  * Python 2.5, (or a lower version with the ctypes module.) http://python.org

  * Pymunk 0.8, Python bindings to Chipmunk physics library, which provides 2D collision detection and rigid body dynamics. Includes a binary of Chipmunk 4.0.2. http://code.google.com/p/pymunk.
 
  * Pyglet 1.1, game library, providing output window, OpenGL graphics, keyboard and mouse input, sound, etc. http://www.pyglet.org


==Install / Running==

There is no install. To run, you must be in the SoleScion directory, then:

    bin/run        (Linux)

    bin\run.bat    (Windows)


==Current Status==

v0.2, 6 Aug 08, week 10 of 12
  * A handful of circular and polygonal entities bounce around inside a single polygonal room.
  * Arbitary polygons are supported by composing one or more convex polys and/or circles.
  * Each component part of a poly has a material, which determines its physical properties: density, friction, elasticity and color.
  * Rendering is very plain indeed.
  * Is now unit tested, and has a basic acceptance test.
  * Internal architecture now defined (v0.1 spike was just one big script)


==Known Problems==

  * It is possible for a fast-moving object to make it through a Room wall from one frame to the next. Possible solution is to use fat line segments (ie. width>0) for wall collision shapes to help prevent this. This would have the amusing side-effect that walls at the intersection between rooms would have rounded corners, which is fine, but might be slightly troublesome to render.


==Contact==

Jonathan Hartley, http://tartley.com, tartley at tartley dot com

