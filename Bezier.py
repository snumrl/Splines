
import sys, math

index = 0

def numLatentPoints( num, resolution, closed ):
    yield 0   # No latent control points

    if num>3:
        yield int((num-1)/3) * resolution
    else:
        yield 0


def discretize( p0, p1, p2, p3, curve, resolution ):
    global index

    for j in range(resolution):
        t = 1.0/(resolution-1)*j
        b0 = (1.0-t)**3.0
        b1 = 3.0*t*(1.0-t)**2.0
        b2 = 3.0*t*t*(1.0-t)
        b3 = t*t*t

        x  = b0*p0[0] + b1*p1[0] + b2*p2[0] + b3*p3[0]
        y  = b0*p0[1] + b1*p1[1] + b2*p2[1] + b3*p3[1]

        if index<len(curve):
            curve[index][0] = x
            curve[index][1] = y
        else:
            curve.append([x,y])

        index = index+1


def cubicBezier2D( num, points, curve, resolution ):
    global index

    if ( num<4 ):
        return

    index = 0
    for i in range(0,num-3,3):
        discretize( points[i], points[i+1], points[i+2], points[i+3], curve, resolution )

