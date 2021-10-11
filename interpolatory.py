
import sys, math

Polygons = [[], [], [], [], [], [], [], [], []]

def numLatentPoints( num, level, closed ):
    yield 0   # No latent control points

    if num>3:
        n = num
        for i in range(level):
            if closed:
                n = 2*n
            else:
                n = 2*n - 1
        yield n
    else:
        yield 0


def subdivision2D( num, points, curve, level, closed ):
    global Polygons

    if ( num<4 ):
        return

    n = num
    while len(Polygons[0])<n:
        Polygons[0].append([0,0])

    for i in range(num):
        if i<len(Polygons[0]):
            Polygons[0][i][0] = points[i][0]
            Polygons[0][i][1] = points[i][1]

    def increment_open(n):
        return 2*n - 1

    def increment_closed(n):
        return 2*n 

    inc = increment_open
    if closed:
        inc = increment_closed

    for i in range(level):
        while len(Polygons[i+1])<inc(n):
            Polygons[i+1].append([0,0])

        for j in range(n):
            Polygons[i+1][2*j][0] = Polygons[i][j][0]
            Polygons[i+1][2*j][1] = Polygons[i][j][1]

        for j in range(n-1):
            if j==0 and not closed:
                Polygons[i+1][2*j+1][0] = (5*Polygons[i][j][0] + 15*Polygons[i][j+1][0] - 5*Polygons[i][j+2][0] + Polygons[i][j+3][0])/16
                Polygons[i+1][2*j+1][1] = (5*Polygons[i][j][1] + 15*Polygons[i][j+1][1] - 5*Polygons[i][j+2][1] + Polygons[i][j+3][1])/16
            elif j==n-2 and not closed:
                Polygons[i+1][2*j+1][0] = (Polygons[i][j-2][0] - 5*Polygons[i][j-1][0] + 15*Polygons[i][j][0] + 5*Polygons[i][j+1][0])/16
                Polygons[i+1][2*j+1][1] = (Polygons[i][j-2][1] - 5*Polygons[i][j-1][1] + 15*Polygons[i][j][1] + 5*Polygons[i][j+1][1])/16
            elif j==0 and closed:
                Polygons[i+1][2*j+1][0] = (-Polygons[i][n-1][0] + 9*Polygons[i][j][0] + 9*Polygons[i][j+1][0] - Polygons[i][j+2][0])/16
                Polygons[i+1][2*j+1][1] = (-Polygons[i][n-1][1] + 9*Polygons[i][j][1] + 9*Polygons[i][j+1][1] - Polygons[i][j+2][1])/16
            elif j==n-2 and closed:
                Polygons[i+1][2*j+1][0] = (-Polygons[i][j-1][0] + 9*Polygons[i][j][0] + 9*Polygons[i][j+1][0] - Polygons[i][0][0])/16
                Polygons[i+1][2*j+1][1] = (-Polygons[i][j-1][1] + 9*Polygons[i][j][1] + 9*Polygons[i][j+1][1] - Polygons[i][0][1])/16
            else:
                Polygons[i+1][2*j+1][0] = (-Polygons[i][j-1][0] + 9*Polygons[i][j][0] + 9*Polygons[i][j+1][0] - Polygons[i][j+2][0])/16
                Polygons[i+1][2*j+1][1] = (-Polygons[i][j-1][1] + 9*Polygons[i][j][1] + 9*Polygons[i][j+1][1] - Polygons[i][j+2][1])/16

        if closed:
            Polygons[i+1][2*n-1][0] = (-Polygons[i][1][0] + 9*Polygons[i][0][0] + 9*Polygons[i][n-1][0] - Polygons[i][n-2][0])/16
            Polygons[i+1][2*n-1][1] = (-Polygons[i][1][1] + 9*Polygons[i][0][1] + 9*Polygons[i][n-1][1] - Polygons[i][n-2][1])/16

        n = inc(n)

    while len(curve)<n:
        curve.append([0,0])

    for i in range(len(Polygons[level])):
        curve[i][0] = Polygons[level][i][0]
        curve[i][1] = Polygons[level][i][1]
