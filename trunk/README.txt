
=Sole Scion=

http://code.google.com/p/sole-scion/

A game with retro 2D vector graphics and rigid body physics, with a vision to exploit the scaling, toppling, sliding and rolling of vector shapes in a game
with 'Roguelike' sensibilities.

Currently at a very early stage of development. Only of interest to the geekiest of my enthusiastic programmer friends.

Works on Windows and Linux. Also worked on Macs relatively recently, thanks to
an assist from William Reade, but is not tested regularly there. Last I heard,
also worked under [http://codespeak.net/pypy/dist/pypy/doc/home.html PyPy] too,
with functools installed.)

If you have problems, please let me know so I can fix them, thanks. See contact
details at the bottom.


==Screenshots==

http://sole-scion.googlecode.com/svn/trunk/docs/screenshots/SoleScion-screenshot-v0.2.4.png

More are [http://code.google.com/p/sole-scion/wiki/Screenshots here].


==To Play==

You will need to install [http://python.org/download/ Python] v2.5 or v2.6.

Then, install the following Python packages:

  * pyglet
  * pymunk
  * shapely

You do not need to install 'libgeos' for shapely - Sole-Scion includes a
copy of it.

Use subversion to check out Sole Scion from:

{{{
    svn checkout http://sole-scion.googlecode.com/svn/trunk/ sole-scion
}}}

and execute {{{SoleScion.bat}}} (Windows) or {{{SoleScion.sh}}} (Linux)


==Known Problems==

  * There isn't a game there yet. It's still very early days. Lower your expectations.
  * See the [http://code.google.com/p/sole-scion/issues/list issues page].


==Thanks==

Many thanks to the creators of the following excellent libraries, without
which this project could not have been built.

  * [http://code.google.com/p/pymunk Pymunk], Excellent Python bindings to the magnificent  [http://code.google.com/p/chipmunk-physics/ Chipmunk] physics library, which provides 2D rigid body dynamics.
 
  * [http://www.pyglet.org Pyglet] game library, providing fantastic facilities for creating windows, OpenGL graphics, keyboard and mouse input, sound, etc.

  * [http://pypi.python.org/pypi/Shapely/ Shapely], superb Python wrapper of [http://trac.osgeo.org/geos/ GEOS] (Geometry Engine Open Souce), which provides 2D geometry operations.

  * Martin O'Leary's Squirtle project, from which inspiration for loading from
    SVG was gleaned, and his polygon tessellation code was lifted wholesale
    under the terms of the BSD.


==Contact==

Jonathan Hartley, tartley at tartley dot com, http://tartley.com

