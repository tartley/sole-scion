=Sole Scion=

http://code.google.com/p/sole-scion/

A game with 2D vector graphics and rigid body physics, and a vision to exploit the scaling, toppling, sliding and rolling of vector shapes.

Currently at a very early stage of development. Only of interest to the geekiest of my friends and to enthusiastic programmers.

Works on Windows and Macs and Linux (and under [http://codespeak.net/pypy/dist/pypy/doc/home.html PyPy], with functools installed.)

Screenshots are [http://code.google.com/p/sole-scion/wiki/Screenshots here].


==To play==

If the following doesn't work for you, please let me know about it - see the 'Contact' section.


===On Windows===

Download the [http://code.google.com/p/sole-scion/downloads/list?can=3&q=binary featured Windows binary download], unzip and double-click 'run.bat'.

===On Linux or Mac==

Install Python 2.5 or 2.6 from [http://python.org python.org].

Download the [http://code.google.com/p/sole-scion/downloads/list?can=3&q=source featured source code download].

Untar it and run the game by opening a command-line terminal and typing something like:

{{{
  tar -xzf SoleScion-X.X.X.tar.gz
  cd SoleScion-X.X.X
  python -O run.py
}}}


==Known Problems==

  * It's still very early days. Lower your expectations.
  * It is possible for a very fast-moving object to make it through a Room wall from one frame to the next. One possible solution is to use fat line segments (ie. width>0) to define the outline of rooms.


==Dependencies==

Many thanks to the creators of the following invaluable libraries, upon which
this project is built:

  * [http://code.google.com/p/pymunk Pymunk], Python bindings to the [http://code.google.com/p/chipmunk-physics/ Chipmunk] physics library, which provides brilliant 2D rigid body dynamics.
 
  * [http://www.pyglet.org Pyglet] game library, providing fantastic facilities for creating windows, OpenGL graphics, keyboard and mouse input, sound, etc.


==Contact==

Jonathan Hartley, http://tartley.com, tartley at tartley dot com, twitter:tartley


