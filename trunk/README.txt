
=Sole Scion=

http://code.google.com/p/sole-scion/

A game with 2D vector graphics and rigid body physics, and a vision to exploit the scaling, toppling, sliding and rolling of vector shapes.

Currently at a very early stage of development. Only of interest to the geekiest of my enthusiastic programmer friends.

Works on Windows and Linux (and last I heard, under
[http://codespeak.net/pypy/dist/pypy/doc/home.html PyPy] too, with functools
installed.)

Could easily work on Macs too, but I need a little assist from someone with a
Mac. Can you help? See contact details below.


==Screenshots==

http://sole-scion.googlecode.com/svn/trunk/docs/screenshots/SoleScion-screenshot-v0.2.4.png

More are [http://code.google.com/p/sole-scion/wiki/Screenshots here].


==To Play==

Use subversion to check out souce from:

{{{
    svn checkout http://sole-scion.googlecode.com/svn/trunk/ sole-scion
}}}

and execute {{{SoleScion.bat}}} (Windows) or {{{SoleScion.sh}}} (Linux)

You will need [http://python.org/download/ Python] v2.5 or v2.6 installed. To check your installed version, type 'python' at a command-prompt and note the displayed version number.

All other dependencies are included in the project.

There is no installer as yet.


==Known Problems==

  * There isn't a game there yet. It's still very early days. Lower your expectations.
  * See the [http://code.google.com/p/sole-scion/issues/list issues page].


==Thanks==

Many thanks to the creators of the following excellent libraries, without
which this project could not have been built.

  * [http://code.google.com/p/pymunk Pymunk], Excellent Python bindings to the magnificent  [http://code.google.com/p/chipmunk-physics/ Chipmunk] physics library, which provides 2D rigid body dynamics.
 
  * [http://www.pyglet.org Pyglet] game library, providing fantastic facilities for creating windows, OpenGL graphics, keyboard and mouse input, sound, etc.

  * [http://pypi.python.org/pypi/Shapely/ Shapely], superb Python wrapper of [http://trac.osgeo.org/geos/ GEOS] (Geometry Engine Open Souce), which provides 2D geometry operations.


==Contact==

Jonathan Hartley, tartley at tartley dot com, http://tartley.com

