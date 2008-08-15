==Sole Scion==

A three month project to write a 2D vector graphic adventure game with
Newtonian rigid-body dynamics, and a vision to exploit the scaling, toppling,
sliding and rolling of vector shapes. 

Currently at a very early stage of development. Only of interest to enthusiastic
programmers.

Works on Linux and Windows. Also works under PyPy, with functools installed.
Anyone tried it on a Mac?

http://code.google.com/p/sole-scion/


===Screenshot===

A spike of v0.2, circles rain down on a polygonal surface. Note the current
HEAD features arbitrary polygon shapes as well as circles, but does not look as
cutesy as this, since it's missing some superficial features like the gradient
fills, and stars in the background.

http://sole-scion.googlecode.com/svn/trunk/screenshots/Screenshot-Sole-Scion-spike2.png


===Dependencies===

You must install these manually.

  * Python 2.5, (or a lower version with the ctypes module.)

  * Pymunk 0.8, Python bindings to Chipmunk physics library, which provides 2D collision detection and rigid body dynamics. Includes a binary of Chipmunk 4.0.2. http://code.google.com/p/pymunk.
 
  * Pyglet 1.1, game library, providing output window, OpenGL graphics, keyboard and mouse input, sound, etc. http://www.pyglet.org


===Install / Running===

There is no install. To run::

    python -O run.py

Note that the -O flag can increase framerate by double or more on Linux. It disables some Pyglet error checking.


===Current Status===

v0.2, 6 Aug 08, week 10 of 12
  * A handful of circular and polygonal entities bounce around inside a single polygonal room.
  * Arbitary polygons are supported by composing one or more convex polys and/or circles.
  * Each component part of a poly has a material, which determines its physical properties: density, friction, elasticity and color.
  * Rendering is very plain indeed.
  * Is now unit tested, and has a basic acceptance test.
  * Internal architecture now defined (v0.1 spike was just one big script)


===Known Problems===

  * It is possible for a fast-moving object to make it through a Room wall from one frame to the next. Possible solution is to use fat line segments (ie. width>0) for wall collision shapes to help prevent this.



