=Sole Scion=

http://code.google.com/p/sole-scion/

A game with 2D vector graphics and rigid body physics, and a vision to exploit the scaling, toppling, sliding and rolling of vector shapes.

Works on Windows and Macs and Linux (and under [http://codespeak.net/pypy/dist/pypy/doc/home.html PyPy], with functools installed.)

Currently at a very early stage of development. Only of interest to the geekiest of my friends and to enthusiastic programmers.


==Screenshots==

Are [http://code.google.com/p/sole-scion/wiki/Screenshots here].


==To Play on Windows==

Download the [http://code.google.com/p/sole-scion/downloads/list?can=3&q=binary featured Windows binary download], unzip and double-click 'run.bat'.


==To Play on Linux or Mac==

Proper binary and source installs to make this trivially easy will be coming soon. Until then:

First install Python 2.5 or 2.6 from [http://python.org python.org]. You probably already have this installed. To check, start a command-line prompt, type 'python', and check the version number displayed is 2.5.x or 2.6.x.

Download the [http://code.google.com/p/sole-scion/downloads/list?can=3&q=source featured source code download].

Untar it and run the game from the command line with something like:

{{{
  tar -xzf SoleScion-X.X.X.tar.gz
  cd SoleScion-X.X.X
  python -O run.py
}}}


==Known Problems==

  * It's still very early days. There isn't a game there yet. Lower your expectations.
  * See the [http://code.google.com/p/sole-scion/issues/list issues page].


==Dependencies==

Many thanks to the creators of the following invaluable libraries, upon which this project is built:

  * [http://code.google.com/p/pymunk Pymunk], Python bindings to the [http://code.google.com/p/chipmunk-physics/ Chipmunk] physics library, which provides brilliant 2D rigid body dynamics.
 
  * [http://www.pyglet.org Pyglet] game library, providing fantastic facilities for creating windows, OpenGL graphics, keyboard and mouse input, sound, etc.

  * [http://trac.gispython.org/lab/wiki/Shapely Shapely], Python bindings
to the [http://trac.osgeo.org/geos GEOS] 2D geometry library.


==Contact==

Jonathan Hartley, http://tartley.com, tartley at tartley dot com, twitter:tartley


