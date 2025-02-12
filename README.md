# Splines
![teaser](./spline.jpg)

## Abstract

This Curve Editor, written by Jehee Lee in 2015, is freeware.
You are free to use, modify, and redistribute the code without any restrictions.
This software requires python3, numpy, scipy, and glfw.
I primarily use this code for teaching computer graphics and computer animation courses.

## Run

GLFW version

```python spline.py```

GLUT version

```python spline_glut.py```

## Usage

**[c]** Toggle open/closed

**[v]** Toggle show/hide latent points

**[d]** Delete a point

**[x]** Delete all points

**[q]** Exit

**[up/down arrow]** in subdivision mode: level up/down

**[up/down arrow]** in Lagrange mode: add/remove control points

**[left/right arrow]** rotate control points


**[1]** B-spline

**[2]** Natural spline

**[3]** Catmull-Rom spline

**[4]** Lagrange polynomial

**[5]** Bezier spline

**[6]** Cubic B-spline subdivision

**[7]** Corner cutting subdivision

**[8]** Interpolatory subdivision
