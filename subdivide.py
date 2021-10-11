
import sys, math

Polygons = [[], [], [], [], [], [], [], [], []]

def numLatentPoints( num, level, closed ):
    yield 0   # No latent control points

    if num>3:
        n = num
        if closed:
            n = num + 3

        for i in range(level):
            n = 2*n - 3
        yield n
    else:
        yield 0


def subdivision2D( num, points, curve, level, closed ):
    global Polygons

    if ( num<4 ):
        return

    n = num
    if closed:
        n = num + 3

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
        Polygons[0][num+2][0] = points[2][0]
        Polygons[0][num+2][1] = points[2][1]

    for i in range(level):
        while len(Polygons[i+1])<2*n-3:
            Polygons[i+1].append([0,0])

        for j in range(n-1):
            Polygons[i+1][2*j][0] = (Polygons[i][j][0] + Polygons[i][j+1][0])/2
            Polygons[i+1][2*j][1] = (Polygons[i][j][1] + Polygons[i][j+1][1])/2

        for j in range(1,n-1):
            Polygons[i+1][2*j-1][0] = (Polygons[i][j-1][0] + 6*Polygons[i][j][0] + Polygons[i][j+1][0])/8
            Polygons[i+1][2*j-1][1] = (Polygons[i][j-1][1] + 6*Polygons[i][j][1] + Polygons[i][j+1][1])/8

        n = 2*n-3

    while len(curve)<n:
        curve.append([0,0])

    for i in range(len(Polygons[level])):
        curve[i][0] = Polygons[level][i][0]
        curve[i][1] = Polygons[level][i][1]
