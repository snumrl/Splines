import sys, math

def numLatentPoints( num, resolution, closed ):
    if num>2:
        n = 3*num - 2
        if closed:
            n = 3*num + 1

        yield n
        yield int((n-1)/3) * resolution
    else:
        yield 0, 0


def CatmullRom2D( num, points, Bpoints, closed ):
    if num<3:
        return

    # set Bpoints size
    if not closed:
        while len(Bpoints)<3*num-2:
            Bpoints.append([0,0])
    else:
        while len(Bpoints)<3*num+1:
            Bpoints.append([0,0])

    # set control points at keypoints
    for i in range(num):
        Bpoints[3*i][0] = points[i][0]
        Bpoints[3*i][1] = points[i][1]

    if closed:
        Bpoints[3*num][0] = points[0][0]
        Bpoints[3*num][1] = points[0][1]

    # set internal control points
    for i in range(num-1):
        if i>0:
            Bpoints[3*i+1][0] = points[i][0] + (points[i+1][0]-points[i-1][0])/6.0
            Bpoints[3*i+1][1] = points[i][1] + (points[i+1][1]-points[i-1][1])/6.0
        else:
            if closed:
                Bpoints[1][0] = points[0][0] + (points[1][0]-points[num-1][0])/6.0
                Bpoints[1][1] = points[0][1] + (points[1][1]-points[num-1][1])/6.0
            else:
                Bpoints[1][0] = points[0][0]
                Bpoints[1][1] = points[0][1]

        if i<num-2:
            Bpoints[3*i+2][0] = points[i+1][0] - (points[i+2][0]-points[i][0])/6.0
            Bpoints[3*i+2][1] = points[i+1][1] - (points[i+2][1]-points[i][1])/6.0
        else:
            if closed:
                Bpoints[3*i+2][0] = points[num-1][0] + (points[num-2][0]-points[0][0])/6.0
                Bpoints[3*i+2][1] = points[num-1][1] + (points[num-2][1]-points[0][1])/6.0

                Bpoints[3*i+4][0] = points[num-1][0] - (points[num-2][0]-points[0][0])/6.0
                Bpoints[3*i+4][1] = points[num-1][1] - (points[num-2][1]-points[0][1])/6.0

                Bpoints[3*i+5][0] = points[0][0] - (points[1][0]-points[num-1][0])/6.0
                Bpoints[3*i+5][1] = points[0][1] - (points[1][1]-points[num-1][1])/6.0
            else:
                Bpoints[3*num-4][0] = points[num-1][0]
                Bpoints[3*num-4][1] = points[num-1][1]
