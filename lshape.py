#!/usr/bin/env python

from mes import Mes
from functions import functions, shift_me_baby

import sys
import numpy as np

class Element:
    def __init__(self, xrange, yrange):
        self.xrange = xrange
        self.yrange = yrange
        self.coeff = [0] * 9

    def u(self, i, j):
        assert xrange[0] <= i <= xrange[1], "Out of x range!"
        assert yrange[0] <= j <= yrange[1], "Out of y range!"

        if i < 0.5 and j < 0.5:
            return 0

        return reduce(lambda x,y: x+shift_me_baby(y[0], xrange[0], 
                                                  xrange[1], yrange[0], 
                                                  yrange[1])(i,j)*y[1], 
                      zip(functions, self.coeff), 0.0)

    def f(self, i, j):
        if i == 0 and j >= 0.5:
            return 1-self.u(i,j)
        elif j == 1.0 and i >= 0.5:
            return -1 - self.u(i,j)
        else:
            return 0

def global_u(elements, i, j):
    for row in elements:
        for element in row:
            if element.xrange[0] <= i <= element.xrange[1] and
               element.yrange[0] <= j <= element.yrange[1]:
                return element.u
    
    raise "Kurwa nie znaleziono!"

def laplacian(elements, i, j, dn):
    return (4*global_u(i,j)-global_u(i-dn,j)-global_u(i+dn,j)-global_u(i,j-dn)-global_u(i,j+dn))/dn

def bitmap(elements, i, j, delta, dn):
    for row in elements:
        for element in row:
            if element.xrange[0] <= i <= element.xrange[1] and
               element.yrange[0] <= j <= element.yrange[1]:
                return element.u(i,j)+delta*laplacian(elements,i,j,dn)+delta*element.f(i,j)

if __name__ == '__main__':
    if len(sys.argv != 5):
        print ('[!] Invalid number of arguments.')
        print ('[i] Usage: %s <n> <time steps> <delta> <dn>')
        sys.exit(1)
    
    n = int(sys.argv[1])
    steps = int(sys.argv[2])
    delta = float(sys.argv[3])
    dn = float(sys.argv[4])

    bitmap = numpy.zeros((n,n))

    # tworzymy grid elementów:

    elements = [Element((1.0*i/n,(i+1.0)/n), (1.0*j/n,(j+1.0)/n)) for i in xrange(n) for j in xrange(n)]
                
    for t in xrange(steps):
        for row in elements:
            for element in row:
                element.coeff[0] = bitmap(elements, 
                                          element.xrange[0], 
                                          element.yrange[0], 
                                          delta,
                                          1.0/n
