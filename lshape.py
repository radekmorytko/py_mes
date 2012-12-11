#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from mes import Mes
from functions import functions, shift_me_baby
from scipy.integrate import quadrature as quad

import sys
import numpy

import matplotlib.pyplot as plt
import math

import Image


class Element:
    def __init__(self, _xrange, yrange):
        self.xrange = _xrange
        self.yrange = yrange
        self.coeff = [0] * 9
        print "%s %s" % (_xrange, yrange)
        self.functions = map(lambda f: shift_me_baby(f, _xrange[0], _xrange[1], yrange[0], yrange[1]), functions)

    def u(self, i, j):
        assert self.xrange[0] <= i <= self.xrange[1], "Out of x range!"
        assert self.yrange[0] <= j <= self.yrange[1], "Out of y range!"

        if i < 0.5 and j < 0.5:
            return 0

        return reduce(lambda x,y: x+y[0](i,j)*y[1], 
                      zip(self.functions, self.coeff), 0.0)

    def f(self, i, j):
        if i == 0.0 and j >= 0.5:
            return 1.0-self.u(i,j)
        elif j == 1.0 and i >= 0.5:
            return -1.0 - self.u(i,j)
        else:
            return 0.0

def global_u(elements, i, j):
    if i < 0.0:
        i = 0.0
    if j < 0.0:
        j = 0.0
    if i > 1.0:
        i = 1.0
    if j > 1.0:
        j = 1.0
    for row in elements:
        for element in row:
            if element.xrange[0] <= i <= element.xrange[1] and \
               element.yrange[0] <= j <= element.yrange[1]:
                return element.u(i,j)
    
    raise  Exception("Kurwa nie znaleziono! %f %f" % (i, j) )

def laplacian(elements, i, j, dn):
    return (4*global_u(elements, i,j)-global_u(elements,i-dn,j)-global_u(elements,i+dn,j)-global_u(elements,i,j-dn)-global_u(elements,i,j+dn))/dn

def bitmap(elements, i, j, delta, dn):
    for row in elements:
        for element in row:
            if element.xrange[0] <= i <= element.xrange[1] and \
               element.yrange[0] <= j <= element.yrange[1]:
                return element.u(i,j)+delta*laplacian(elements,i,j,dn)+delta*element.f(i,j)

if __name__ == '__main__':
    if len(sys.argv)  != 5:
        print ('[!] Invalid number of arguments.')
        print ('[i] Usage: %s <n> <time steps> <delta> <dn>')
        sys.exit(1)
    
    n = int(sys.argv[1])
    steps = int(sys.argv[2])
    delta = float(sys.argv[3])
    dn = float(sys.argv[4])

    # bitmap = numpy.zeros((n,n))

    # tworzymy grid elementów:    

    elements = [[Element((1.0*i/n,(i+1.0)/n), (1.0*j/n,(j+1.0)/n)) for i in xrange(n)] for j in xrange(n)]
                
    for t in xrange(steps):
        print t
        for row in elements:
            for element in row:
                element.coeff[0] = bitmap(elements, 
                                          element.xrange[0], 
                                          element.yrange[0], 
                                          delta,
                                          1.0/n)

                f5 = lambda x: bitmap(elements, x, element.yrange[0], delta, dn) - element.coeff[0] * element.functions[0](x, element.yrange[0])  - element.coeff[1] * element.functions[1](x, element.yrange[0]) - element.coeff[2] * element.functions[2](x, element.yrange[0]) - element.coeff[3] * element.functions[3](x, element.yrange[0])                
                g5 = lambda x: elemet.functions[5]**2

                f6 = lambda x: bitmap(elements, element.xrange[1], x, delta, dn) - element.coeff[0] * element.functions[0](element.xrange[1], x)  - element.coeff[1] * element.functions[1](element.xrange[1], x)  - element.coeff[2] * element.functions[2](element.xrange[1], x)  - element.coeff[3] * element.functions[3](element.xrange[1], x) 
                g6 = lambda x: elemet.functions[6]**2

                f7 = lambda x: bitmap(elements, x, element.yrange[1], delta, dn) - element.coeff[0] * element.functions[0](x, element.yrange[1])  - element.coeff[1] * element.functions[1](x, element.yrange[0]) - element.coeff[2] * element.functions[2](x, element.yrange[0]) - element.coeff[3] * element.functions[3](x, element.yrange[0])                
                g7 = lambda x: elemet.functions[7]**2

                f8 = lambda x: bitmap(elements, element.xrange[0], x, delta, dn) - element.coeff[0] * element.functions[0](element.xrange[0], x)  - element.coeff[1] * element.functions[1](element.xrange[0], x)  - element.coeff[2] * element.functions[2](element.xrange[0], x)  - element.coeff[3] * element.functions[3](element.xrange[0], x) 
                g8 = lambda x: elemet.functions[8]**2

                q5u = quad(f5, element.xrange[0], element.xrange[1], vec_func=False, maxiter=10)[0]
                q5l = quad(f5, element.xrange[0], element.xrange[1], vec_func=False, maxiter=10)[0]
                                                                                             
                q6u = quad(f6, element.yrange[0], element.yrange[1], vec_func=False, maxiter=10)[0]
                q6l = quad(f6, element.yrange[0], element.yrange[1], vec_func=False, maxiter=10)[0]
                                                                                             
                q7u = quad(f7, element.xrange[0], element.xrange[1], vec_func=False, maxiter=10)[0]
                q7l = quad(f7, element.xrange[0], element.xrange[1], vec_func=False, maxiter=10)[0]
                                                                                             
                q8u = quad(f8, element.yrange[0], element.yrange[1], vec_func=False, maxiter=10)[0]
                q8l = quad(f8, element.yrange[0], element.yrange[1], vec_func=False, maxiter=10)[0]

    im = Image.new('L',(512,512))
    pix = im.load()
    
    for x in xrange(512):
        for y in xrange(512):
            u = global_u(elements, x/511.0, y/511.0)*1000
            pix[x, y] = u+128.0
    im.save('output.png')
        

