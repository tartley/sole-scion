http://code.google.com/p/sole-scion/

STATUS: Unfinished. On hold. Only of interest to the geekiest of my enthusiastic programmer friends.

The vision of Sole Scion is to be a slow-paced but real-time 2D vector graphic RPG, styled somewhat on Nethack, but with smoothly moving and rotating vector shapes. I hope to supplement the limited amount of content I can produce with some emergent behaviours based on the shape of objects and a rigid-body physics system. (eg. imagine the player stacking boulders to block a corridor before the monsters arrive.)

Currently complete are:
  * SVG objects loaded
  * conversion of SVG into vertex arrays for OpenGL rendering
  * conversion of SVG into shapes for the Chipmunk rigid-body engine
  * A basic random procedural level generation
  * The player can zoom a small shape around within the level
  * Camera pans around to follow the player, (with added subtle zooming and rolling for comedy vertiginous disorientation.)
  * Player can push and shove a bunch of randomly generated objects in the level, derived from loaded SVG, and they tumble and roll around in appropriate response.

I am pleased with the work to date, but progress has been very slow. I plan to postpone completion of this for the time being, and work on a few very small, less ambitious games, before hopefully returning to this vision when I have a little more experience.


## Screenshots ##

![http://sole-scion.googlecode.com/svn/trunk/docs/screenshots/SoleScion-screenshot-v0.2.6.png](http://sole-scion.googlecode.com/svn/trunk/docs/screenshots/SoleScion-screenshot-v0.2.6.png)

More screenshots are [here](http://code.google.com/p/sole-scion/wiki/Screenshots).


## To Play ##

**Windows:** Download the latest Windows binaries from the [downloads page](http://code.google.com/p/sole-scion/downloads/list?can=3). Run `SoleScion.bat`


**Linux, Mac, PyPy:** A simple way to download and play does not yet exist. The complicated way is:

  * Install [Python](http://python.org/download/) v2.5 or v2.6.
  * Install Python packages: [pyglet](http://www.pyglet.org), [Pymunk](http://code.google.com/p/pymunk), [Shapely](http://pypi.python.org/pypi/Shapely/).
  * Install the C library [GEOS](http://trac.osgeo.org/geos/).
  * Download the [source distribution](http://code.google.com/p/sole-scion/downloads/list?can=3).
  * Run `bin\run.sh`


## To examine or modify the source code ##

See the [Subversion repository](http://code.google.com/p/sole-scion/source/checkout). You will need to install the above dependencies.


## Known Problems ##

  * There isn't a game there yet. It's still very early days. Lower your expectations.
  * See the [issues page](http://code.google.com/p/sole-scion/issues/list).


## Thanks ##

Many thanks to the creators of the following excellent libraries, without
which this project could not exist.
  * [Pymunk](http://code.google.com/p/pymunk), Excellent Python bindings to the magnificent  [Chipmunk](http://code.google.com/p/chipmunk-physics/) physics library, which provides 2D rigid body dynamics.
  * [pyglet](http://www.pyglet.org) game library, providing fantastic facilities for creating windows, OpenGL graphics, keyboard and mouse input, sound, etc.
  * [Shapely](http://pypi.python.org/pypi/Shapely/), superb Python wrapper of [GEOS](http://trac.osgeo.org/geos/) (Geometry Engine Open Souce), which provides 2D geometry operations.
  * Many thanks to Martin O'Leary of http://supereffective.org, whose Squirtle module inspired the SVG data loading for this project, and in particular his sublime tessellation code, which I have copied wholesale under the terms of the BSD.


## Contact ##

Jonathan Hartley, tartley at tartley dot com, http://tartley.com, @tartley
