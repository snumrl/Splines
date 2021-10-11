import sys, math
import numpy as np
import scipy.linalg

A, Au, X, Y, Bx, By = [], [], [], [], [], []

def numLatentPoints( num, resolution, closed ):
    if num>3:
        if closed:
            yield num
            yield num*resolution
        else:
            yield num+2
            yield (num-1)*resolution
    else:
        yield 0
        yield 0


def matrixSetupNaturalSpline( n, closed ):
    global A, Au, X, Y, Bx, By

    if n<4:
        return

    if closed:
        A  = np.zeros( (n, n), dtype=float )
        X  = np.zeros( n, dtype=float )
        Y  = np.zeros( n, dtype=float )
        Bx = np.zeros( n, dtype=float )
        By = np.zeros( n, dtype=float )

        A[  0][n-1], A[  0][  0], A[  0][1] = 1.0/6.0, 4.0/6.0, 1.0/6.0
        A[n-1][n-2], A[n-1][n-1], A[n-1][0] = 1.0/6.0, 4.0/6.0, 1.0/6.0

        for i in range(n-2):
            A[i+1][i], A[i+1][i+1], A[i+1][i+2] = 1.0/6.0, 4.0/6.0, 1.0/6.0

        Au = scipy.linalg.lu_factor(A)

    else:
        A  = np.zeros( (n+2, n+2), dtype=float )
        X  = np.zeros( n+2, dtype=float )
        Y  = np.zeros( n+2, dtype=float )
        Bx = np.zeros( n+2, dtype=float )
        By = np.zeros( n+2, dtype=float )

        A[  0][  0], A[  0][1], A[  0][  2] = 1.0/6.0, -2.0/6.0, 1.0/6.0
        A[n+1][n-1], A[n+1][n], A[n+1][n+1] = 1.0/6.0, -2.0/6.0, 1.0/6.0

        for i in range(n):
            A[i+1][i], A[i+1][i+1], A[i+1][i+2] = 1.0/6.0, 4.0/6.0, 1.0/6.0

        Au = scipy.linalg.lu_factor(A)


def evaluateNaturalSpline( n, points, Bpoints, closed ):
    global Au, X, Y, Bx, By

    if n<4:
        return

    if closed:
        for i in range(n):
            Bx[i] = points[i][0]
            By[i] = points[i][1]

        X = scipy.linalg.lu_solve( Au, Bx )
        Y = scipy.linalg.lu_solve( Au, By )

        for i in range(n):
            if i<len(Bpoints):
                Bpoints[i][0] = X[i]
                Bpoints[i][1] = Y[i]
            else:
                Bpoints.append([X[i],Y[i]])

    else:
        Bx[0], Bx[n+1], By[0], By[n+1] = 0, 0, 0, 0
        for i in range(n):
            Bx[i+1] = points[i][0]
            By[i+1] = points[i][1]

        X = scipy.linalg.lu_solve( Au, Bx )
        Y = scipy.linalg.lu_solve( Au, By )

        for i in range(n+2):
            if i<len(Bpoints):
                Bpoints[i][0] = X[i]
                Bpoints[i][1] = Y[i]
            else:
                Bpoints.append([X[i],Y[i]])

