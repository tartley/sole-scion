SOLE SCION

A three month project to write a 2D vector graphic adventure game with Newtonian dynamics.

http://code.google.com/p/sole-scion/


CURRENT STATUS

v0.1, 17 Jun 08, week 2 of 12.
A very rudimentary integration of our major dependencies. Linux only.
Chipmunk controls some circles raining down the screen, which are rendered using Pyglet.


KNOWN PROBLEMS

- Haven't tried to run it on Windows (no known incompatabilities though)
- mouse/keyboard input accelerates gameloop, which later sleeps a big chunk to compensate
- No user input / no point to the game
- Still seem to be seeing tearing, although vsync is requested.


FUTURE PLANS

- Handle moving polygon entities (rocks) as well as circles.
- Put the rocks inside a room with impenetrable walls.
- Render faster, using Vertex Object Buffers instead of glVertex() calls.
- Windows compatibility.
- Windows binary distributable.
- Handle multiple connected room polygons to form a maze of sorts.
- Other objects in the maze to form a narrative / quest structure.


DEPENDENCIES

Chipmunk 4.0.2
Collision detection, Newtonian rigid body dynamics.
http://wiki.slembcke.net/main/published/Chipmunk

Pymunk 0.7.1
Python bindings to Chipmunk.
http://code.google.com/p/pymunk

Pyglet 1.1beta2
Graphics, key/mouse input, sound, etc.
http://www.pyglet.org

