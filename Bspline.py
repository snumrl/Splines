
import sys, math

index = 0

def numLatentPoints( num, resolution, closed ):
    yield 0   # No latent control points

    if num>3:
        if closed:
            yield num*resolution
        else:
            yield (num-3)*resolution
    else:
        yield 0


def discretize( p0, p1, p2, p3, curve, resolution ):
    global index

    for j in range(resolution):
        t = 1.0/(resolution-1)*j
        b0 = (1.0-t)**3.0/6.0
        b1 = (3.0*t*t*t - 6.0*t*t + 4.0)/6.0
        b2 = (-3.0*t*t*t + 3*t*t + 3*t + 1)/6.0
        b3 = t**3/6.0

        x  = b0*p0[0] + b1*p1[0] + b2*p2[0] + b3*p3[0]
        y  = b0*p0[1] + b1*p1[1] + b2*p2[1] + b3*p3[1]

        if index<len(curve):
            curve[index][0] = x 
            curve[index][1] = y
        else:
            curve.append([x,y])

        index = index+1


def cubicBspline2D( num, points, curve, resolution, closed ):
    global index
    index = 0

    if ( num<4 ):
        return

    if closed:
        for i in range(num-3):
            discretize( points[i], points[i+1], points[i+2], points[i+3], curve, resolution )

        discretize( points[num-3], points[num-2], points[num-1], points[0], curve, resolution)
        discretize( points[num-2], points[num-1], points[0], points[1], curve, resolution)
        discretize( points[num-1], points[0], points[1], points[2], curve, resolution)

    else:
        for i in range(num-3):
            discretize( points[i], points[i+1], points[i+2], points[i+3], curve, resolution )
