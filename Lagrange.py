
import sys, math

def numLatentPoints( num, resolution, closed):
    yield 0   # No latent control points

    if num>1:
        yield (num-1)*resolution+1
    else:
        yield 0


def lagrange2D( points, curve, resolution ):
    num = len( points )
    if num<2:
        return

    if 0<len(curve):
        curve[0][0] = points[0][0]
        curve[0][1] = points[0][1]
    else:
        curve.append( [points[0][0], points[0][1]] )

    for i in range(resolution*(num-1)):
        t = (float)(i)/resolution + 1.0/resolution

        Lx, Ly = 0, 0
        for j in range(num):
            l = 1
            for k in range(num):
                if j!=k:
                    l *= (t-k)/(j-k)

            Lx += l*points[j][0]
            Ly += l*points[j][1]

        if i+1<len(curve):
            curve[i+1][0] = Lx
            curve[i+1][1] = Ly
        else:
            curve.append([Lx, Ly])
        
