from OpenGL.GL import *
import glfw
import sys, math
from enum import Enum

import Bspline
import natural
import Lagrange
import Bezier
import CatmullRom
import subdivide
import cornercut
import interpolatory

#variables
winWidth,  winHeight  = 700, 700
halfWidth, halfHeight = winWidth/2, winHeight/2
mouse_x = 0
mouse_y = 0
double_buf_flag = 2

points  = []
curve   = []
bpoints = []

picked = -1
left_drag   = False
right_drag  = False
left_press  = False
right_press = False

resolution  = 20
numCurve    = 0
numBpoints  = 0
div_level   = 5
closed      = False
show_bpoints= False

class Mode(Enum):
    BSPLINE=1
    NATURAL=2
    LAGRANGE=3
    BEZIER=4
    CATMULLROM=5
    CUBIC_SUB=6
    CORNER_CUT=7
    INTERPOLATORY=8
curveMode = Mode.NATURAL


def windowReshape( window, newWidth, newHeight ):
    global winWidth, winHeight
    global halfWidth, halfHeight

    ratio = newWidth / float(newHeight)
    glViewport(0, 0, newWidth, newHeight)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-ratio, ratio, -1.0, 1.0, 1.0, -1.0)

    winWidth, winHeight = newWidth, newHeight
    halfWidth, halfHeight = winWidth/2, winHeight/2

    redraw(2)


def screen2coord( x, y ):
    return (x-halfWidth)/halfHeight, (y-halfHeight)/halfHeight


def coord2screen( x, y ):
    return (x*halfHeight)+halfWidth, (y*halfHeight)+halfHeight


def drawPoints( x, y ):
    glBegin(GL_LINE_LOOP)
    glVertex2f(x+0.01, y+0.01)
    glVertex2f(x-0.01, y+0.01)
    glVertex2f(x-0.01, y-0.01)
    glVertex2f(x+0.01, y-0.01)
    glEnd()


def drawLatentPoints( x, y ):
    glBegin(GL_LINE_LOOP)
    glVertex2f(x+0.007, y+0.007)
    glVertex2f(x-0.007, y+0.007)
    glVertex2f(x-0.007, y-0.007)
    glVertex2f(x+0.007, y-0.007)
    glEnd()


def redraw( flag ):
    global double_buf_flag

    if flag==0 and double_buf_flag==0:
        return
    elif flag>0:
        double_buf_flag = flag
    elif double_buf_flag>0:
        double_buf_flag = double_buf_flag-1

    glClearColor( 0.8, 0.8, 0.8, 0.0 )
    glClear(GL_COLOR_BUFFER_BIT)
    glLineWidth( 2.0 )

    # draw latent control polygon
    if show_bpoints and numBpoints>1:
        glColor3f(0.1,0.5,0.1)
        glLineWidth( 2.0 )
        for i in range(numBpoints-1):
            glBegin(GL_LINES)
            glVertex2f(*bpoints[i])
            glVertex2f(*bpoints[i+1])
            glEnd()

        for i in range(numBpoints):
            drawLatentPoints(*bpoints[i])

    # draw control polygon
    for i in range(len(points)):
        if picked==i:
            glColor3f(1.0,0.0,0.0)
            glLineWidth( 2.0 )
        else:
            glColor3f(0.3,0.3,0.3)
            glLineWidth( 2.0 )
        drawPoints(*points[i])

    glColor3f(0.3,0.3,0.3)
    glLineWidth( 2.0 )
    for i in range(len(points)-1):
        glBegin(GL_LINES)
        glVertex2f(*points[i])
        glVertex2f(*points[i+1])
        glEnd()
    if closed and len(points)>2:
        glBegin(GL_LINES)
        glVertex2f(*points[0])
        glVertex2f(*points[len(points)-1])
        glEnd()

    # Draw Curve
    if numCurve>1:
        glColor3f(0.0,0.0,1.0)
        glLineWidth( 2.0 )
        for i in range(numCurve-1):
            glBegin(GL_LINES)
            glVertex2f(*curve[i])
            glVertex2f(*curve[i+1])
            glEnd()

    glFlush()


def selectPoint( x, y ):
    for i in range(len(points)):
        px, py = coord2screen( *points[i] )
        if abs(px-x)<7.0 and abs(py-y)<7.0:
            return i

    return -1


def updateCurves():
    global numCurve, numBpoints

    if curveMode==Mode.BSPLINE:
        Bspline.cubicBspline2D( len(points), points, curve, resolution, closed )

    elif curveMode==Mode.NATURAL:
        natural.evaluateNaturalSpline( len(points), points, bpoints, closed )
        Bspline.cubicBspline2D( numBpoints, bpoints, curve, resolution, closed )

    elif curveMode==Mode.LAGRANGE:
        Lagrange.lagrange2D( points, curve, resolution )

    elif curveMode==Mode.BEZIER:
        Bezier.cubicBezier2D( len(points), points, curve, resolution )

    elif curveMode==Mode.CATMULLROM:
        CatmullRom.CatmullRom2D( len(points), points, bpoints, closed )
        Bezier.cubicBezier2D( len(bpoints), bpoints, curve, resolution )

    elif curveMode==Mode.CUBIC_SUB:
        subdivide.subdivision2D( len(points), points, curve, div_level, closed )

    elif curveMode==Mode.CORNER_CUT:
        cornercut.subdivision2D( len(points), points, curve, div_level, closed )

    elif curveMode==Mode.INTERPOLATORY:
        interpolatory.subdivision2D( len(points), points, curve, div_level, closed )


def setupCurves():
    global numCurve, numBpoints

    if curveMode==Mode.BSPLINE:
        numBpoints, numCurve = Bspline.numLatentPoints( len(points), resolution, closed)

    elif curveMode==Mode.NATURAL:
        natural.matrixSetupNaturalSpline( len(points), closed )
        numBpoints, numCurve = natural.numLatentPoints( len(points), resolution, closed)

    elif curveMode==Mode.LAGRANGE:
        numBpoints, numCurve = Lagrange.numLatentPoints( len(points), resolution, closed)

    elif curveMode==Mode.BEZIER:
        numBpoints, numCurve = Bezier.numLatentPoints( len(points), resolution, closed)

    elif curveMode==Mode.CATMULLROM:
        numBpoints, numCurve = CatmullRom.numLatentPoints( len(points), resolution, closed)

    elif curveMode==Mode.CUBIC_SUB:
        numBpoints, numCurve = subdivide.numLatentPoints( len(points), div_level, closed)

    elif curveMode==Mode.CORNER_CUT:
        numBpoints, numCurve = cornercut.numLatentPoints( len(points), div_level, closed)

    elif curveMode==Mode.INTERPOLATORY:
        numBpoints, numCurve = interpolatory.numLatentPoints( len(points), div_level, closed)

    updateCurves()


def mouseCallback( window, button, action, mods ):
    global picked, left_press, left_drag

    if button==glfw.MOUSE_BUTTON_LEFT:

        if action==glfw.PRESS: # add a new point or pick a point
            left_press = True
            left_drag  = False

            picked = selectPoint( mouse_x, winHeight-mouse_y )
            if picked<0:
                px, py = screen2coord( mouse_x, winHeight-mouse_y )

                points.append([px,py])
                setupCurves()
            else:
                left_drag = True

        if action==glfw.RELEASE:
            left_press = False
            left_drag = False

    redraw(2)


def motionCallback( window, x, y ):
    global picked, left_press, left_drag
    global mouse_x, mouse_y

    mouse_x = x
    mouse_y = y

    if left_press and left_drag:
        points[picked][0], points[picked][1] = screen2coord( x, winHeight-y )
        updateCurves()

    redraw(2)


def keyboardCallback( window, key, scancode, action, mods ):
    global curveMode, picked, closed, show_bpoints
    global div_level

    if action == glfw.PRESS:
        if key==glfw.KEY_Q:
            glfw.set_window_should_close( window, GL_TRUE )

        elif key==glfw.KEY_X:
            del points[:]
            del curve[:]
            numCurve = 0
            numBpoints = 0
            picked = -1

        elif key==glfw.KEY_D:
            if picked>-1:
                del points[picked]

                if picked>=len(points):
                    if len(points)>0:
                        picked = len(points)-1
                    else:
                        picked = -1

        elif key==glfw.KEY_C:
            closed = not closed

        elif key==glfw.KEY_V:
            show_bpoints = not show_bpoints

        elif key==glfw.KEY_1:
            curveMode = Mode.BSPLINE
        elif key==glfw.KEY_2:
            curveMode = Mode.NATURAL
        elif key==glfw.KEY_3:
            curveMode = Mode.CATMULLROM
        elif key==glfw.KEY_4:
            curveMode = Mode.LAGRANGE
        elif key==glfw.KEY_5:
            curveMode = Mode.BEZIER
        elif key==glfw.KEY_6:
            curveMode = Mode.CUBIC_SUB
        elif key==glfw.KEY_7:
            curveMode = Mode.CORNER_CUT
        elif key==glfw.KEY_8:
            curveMode = Mode.INTERPOLATORY

        if key==glfw.KEY_DOWN:
            if curveMode==Mode.LAGRANGE:
                if len(points)>3:
                    del points[0]

                while len(points)<3:
                    points.append( [0.0,0.0] )

                for i in range(len(points)):
                    points[i][0] = 1.8*i/(len(points)-1) - 0.9
                    points[i][1] = 0.0
            else:
                div_level = div_level-1
                if div_level < 1:
                    div_level = 1

        elif key==glfw.KEY_UP:
            if curveMode==Mode.LAGRANGE:
                points.append( [0.0, 0.0] )

                while len(points)<3:
                    points.append( [0.0,0.0] )

                for i in range(len(points)):
                    points[i][0] = 1.8*i/(len(points)-1) - 0.9
                    points[i][1] = 0.0
            else:
                div_level = div_level+1
                if div_level > 7:
                    div_level = 7

        elif key==glfw.KEY_LEFT:
       	    for i in range(len(points)):
                c = math.cos(.2)
       	        s = math.sin(.2)
       	        x = c*points[i][0] - s*points[i][1]
       	        y = s*points[i][0] + c*points[i][1]
       	        points[i][0] = x
                points[i][1] = y

        elif key==glfw.KEY_RIGHT:
       	    for i in range(len(points)):
                c = math.cos(.2)
       	        s = math.sin(.2)
       	        x =   c*points[i][0] + s*points[i][1]
       	        y = - s*points[i][0] + c*points[i][1]
       	        points[i][0] = x
                points[i][1] = y

        setupCurves()
        redraw(2)


def main():
    if not glfw.init():
        return

    window = glfw.create_window( winWidth, winHeight, "Spline Demo", None, None )
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    #glfw.swap_interval(1);
    glfw.set_key_callback(window, keyboardCallback)
    glfw.set_mouse_button_callback(window, mouseCallback)
    glfw.set_cursor_pos_callback(window, motionCallback)
    glfw.set_window_size_callback(window, windowReshape)

    # Help
    print()
    print( "-------------------------------------------------------------------" )
    print( "  This Curve Editor, written by Jehee Lee in 2015, is a freeware.    " )
    print( "  You can use, modify, redistribute the code without restriction.  " )
    print( "  This software requires python3, numpy, and glfw to be installed. " )
    print( "-------------------------------------------------------------------" )
    print( "[c] Toggle open/closed" )
    print( "[v] Toggle show/hide latent points" )
    print( "[d] Delete a point" )
    print( "[x] Delete all points" )
    print( "[q] Exit" )
    print( "[up/down arrow] in subdivision mode: level up/down" )
    print( "[up/down arrow] in Lagrange mode: add/remove control points" )
    print( "[left/right arrow] rotate control points" )
    print( "---" )
    print( "[1] B-spline" )
    print( "[2] Natural spline" )
    print( "[3] Catmull-Rom spline" )
    print( "[4] Lagrange polynomial" )
    print( "[5] Bezier spline" )
    print( "[6] Cubic B-spline subdivision" )
    print( "[7] Corner cutting subdivision" )
    print( "[8] Interpolatory subdivision" )
    print()


    width, height = glfw.get_framebuffer_size(window)
    ratio = width / float(height)
    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-ratio, ratio, -1.0, 1.0, 1.0, -1.0)

    while not glfw.window_should_close(window):
        redraw(0)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
