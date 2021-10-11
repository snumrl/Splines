
import sys, math

Polygons = [[], [], [], [], [], [], [], [], []]

def numLatentPoints( num, level, closed ):
    yield 0   # No latent control points

    if num>2:
        n = num
        if closed:
            n = num + 2

        for i in range(level):
            n = 2*n - 2
        yield n
    else:
        yield 0


def subdivision2D( num, points, curve, level, closed ):
    global Polygons

    if ( num<3 ):
        return

    n = num
    if closed:
        n = num + 2

    while len(Polygons[0])<n:
        Polygons[0].append([0,0])

    for i in range(num):
        if i<len(Polygons[0]):
            Polygons[0][i][0] = points[i][0]
            Polygons[0][i][1] = points[i][1]
    if closed:
        Polygons[0][num  ][0] = points[0][0]
        Polygons[0][num  ][1] = points[0][1]
        Polygons[0][num+1][0] = points[1][0]
        Polygons[0][num+1][1] = points[1][1]

    for i in range(level):
        while len(Polygons[i+1])<2*n-2:
            Polygons[i+1].append([0,0])

        for j in range(n-1):
            Polygons[i+1][2*j][0] = (3*Polygons[i][j][0] + Polygons[i][j+1][0])/4
            Polygons[i+1][2*j][1] = (3*Polygons[i][j][1] + Polygons[i][j+1][1])/4

            Polygons[i+1][2*j+1][0] = (Polygons[i][j][0] + 3*Polygons[i][j+1][0])/4
            Polygons[i+1][2*j+1][1] = (Polygons[i][j][1] + 3*Polygons[i][j+1][1])/4

        n = 2*n-2

    while len(curve)<n:
        curve.append([0,0])

    for i in range(len(Polygons[level])):
        curve[i][0] = Polygons[level][i][0]
        curve[i][1] = Polygons[level][i][1]
