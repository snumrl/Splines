from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
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
winWidth, winHeight = 700, 700
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


def windowReshape( newWidth, newHeight ):
    glViewport( 0, 0, newWidth, newHeight )
    glMatrixMode( GL_PROJECTION )
    glLoadIdentity()
    gluOrtho2D( 0.0, float(newWidth), 0.0, float(newHeight) )

    winWidth, winHeight = newWidth, newHeight


def drawPoints( x, y ):
    glBegin(GL_LINE_LOOP)
    glVertex2f(x+4.0, y+4.0)
    glVertex2f(x-4.0, y+4.0)
    glVertex2f(x-4.0, y-4.0)
    glVertex2f(x+4.0, y-4.0)
    glEnd()


def drawLatentPoints( x, y ):
    glBegin(GL_LINE_LOOP)
    glVertex2f(x+1.0, y+1.0)
    glVertex2f(x-1.0, y+1.0)
    glVertex2f(x-1.0, y-1.0)
    glVertex2f(x+1.0, y-1.0)
    glEnd()


def redraw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLineWidth( 1.0 )

    # draw latent control polygon
    if show_bpoints and numBpoints>1:
        glColor3f(1.0,0.5,0.0)
        glLineWidth( 1.0 )
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
        else:
            glColor3f(0.6,0.6,0.6)
        drawPoints(*points[i])
    
    glColor3f(0.6,0.6,0.6)
    glLineWidth( 1.0 )
    for i in range(len(points)-1):
        glBegin(GL_LINES)
        glVertex2f(*points[i])
        glVertex2f(*points[i+1])
        glEnd()
    if closed:
        glBegin(GL_LINES)
        glVertex2f(*points[0])
        glVertex2f(*points[len(points)-1])
        glEnd()
    
    # Draw Curve
    if numCurve>1:
        glColor3f(0.0,0.0,1.0)
        glLineWidth( 1.0 )
        for i in range(numCurve-1):
            glBegin(GL_LINES)
            glVertex2f(*curve[i])
            glVertex2f(*curve[i+1])
            glEnd()

    glFlush()


def selectPoint( x, y ):
    for i in range(len(points)):
        if abs(points[i][0]-x)<7.0 and abs(points[i][1]-y)<7.0:
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


def mouseCallback( button, action, x, y ):
    global picked, left_press, left_drag
    
    if button==GLUT_LEFT_BUTTON:
        
        if action==GLUT_DOWN: # add a new point or pick a point
            left_press = True
            left_drag  = False
            
            picked = selectPoint( float(x), float(winHeight-y) )
            if picked<0:
                points.append([float(x), float(winHeight-y)])
                setupCurves()
                
            else:
                left_drag = True
                
            glutPostRedisplay()

        if action==GLUT_UP:
            left_press = False
            left_drag = False
        

def motionCallback( x, y ):
    global picked, left_press, left_drag
    
    if left_press and left_drag:
        points[picked][0] = float(x)
        points[picked][1] = float(winHeight-y)
        updateCurves()

        glutPostRedisplay()


def keyboardCallback( key, x, y ):
    global curveMode, picked, closed, show_bpoints

    if key==b'x' or key==b'X':
        del points[:]
        numCurve = 0
        numBpoints = 0
        picked = -1

    elif key==b'q' or key==b'Q':
        sys.exit()

    elif key==b'd' or key==b'D':
        if picked>-1:
            del points[picked]

            if picked>=len(points):
                if len(points)>0:
                    picked = len(points)-1
                else:
                    picked = -1

    elif key==b'c' or key==b'C':
        closed = not closed

    elif key==b'v' or key==b'V':
        show_bpoints = not show_bpoints

    elif key==b'1':
        curveMode = Mode.BSPLINE
    elif key==b'2':
        curveMode = Mode.NATURAL
    elif key==b'3':
        curveMode = Mode.CATMULLROM
    elif key==b'4':
        curveMode = Mode.LAGRANGE
    elif key==b'5':
        curveMode = Mode.BEZIER
    elif key==b'6':
        curveMode = Mode.CUBIC_SUB
    elif key==b'7':
        curveMode = Mode.CORNER_CUT
    elif key==b'8':
        curveMode = Mode.INTERPOLATORY

    setupCurves()
    glutPostRedisplay()


def SpecialInput(key, x, y):
    global div_level

    if key==GLUT_KEY_DOWN:
        div_level = div_level-1
        if div_level < 1:
            div_level = 1
            
    elif key==GLUT_KEY_UP:
        div_level = div_level+1
        if div_level > 5:
            div_level = 5

    setupCurves()
    glutPostRedisplay()
            

if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(winWidth,winHeight)
    glutCreateWindow('Spline Demo')
    
    glClearColor(0.8,0.8,0.8,0.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0.0,1000.0,0.0,1000.0)
    
    glutDisplayFunc(redraw)
    glutReshapeFunc(windowReshape)
    glutMouseFunc( mouseCallback )
    glutMotionFunc( motionCallback )
    glutKeyboardFunc( keyboardCallback )
    glutSpecialFunc(SpecialInput);

    # Help
    print()
    print( "---------------------------------------------------" )
    print( "  The Curve Editor, written by Jehee Lee in 2015," )
    print( "  is a freeware software. You can use and modify" )
    print( "  the code for whatever purpose freely." )
    print( "---------------------------------------------------" )
    print( "[c] Toggle open/closed" )
    print( "[v] Toggle show/hide latent points" )
    print( "[d] Delete a point" )
    print( "[x] Delete all points" )
    print( "[q] Exit" )
    print( "[up/down arrow] Subdivision level" )
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

    glutMainLoop()
