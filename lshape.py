#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from mes import Mes
from functions import functions, shift_me_baby, d2f_dx, d2f_dy
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
        self.functions = map(lambda f: shift_me_baby(f, _xrange[0], _xrange[1], yrange[0], yrange[1]), functions)
        self.functions2x = map(lambda f: shift_me_baby(f, _xrange[0], _xrange[1], yrange[0], yrange[1]), d2f_dx)
        self.functions2y = map(lambda f: shift_me_baby(f, _xrange[0], _xrange[1], yrange[0], yrange[1]), d2f_dy)

    def u(self, i, j):
        assert self.xrange[0] <= i <= self.xrange[1], "Out of x range!"
        assert self.yrange[0] <= j <= self.yrange[1], "Out of y range!"
        # 
        if i < 0.5 and j < 0.5:
            return 0

        return reduce(lambda x,y: x+y[0](i,j)*y[1], 
                      zip(self.functions, self.coeff), 0.0)

    def lap(self, i, j):
        assert self.xrange[0] <= i <= self.xrange[1], "Out of x range!"
        assert self.yrange[0] <= j <= self.yrange[1], "Out of y range!"
        # 
        if i < 0.5 and j < 0.5:
            return 0

        return reduce(lambda x,y: x+y[0](i,j)*y[1], zip(self.functions2x, self.coeff), 0.0)+ reduce(lambda x,y: x+y[0](i,j)*y[1], zip(self.functions2y, self.coeff), 0.0)

    def f(self, i, j):
        if i == 0.0 and j >= 0.5:
            return 1.0-self.u(i,j)
        elif j == 0.0 and i >= 0.5:
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

# def laplacian(elements, i, j, dn):
#     for row in elements:
#         for element in row:
#             if element.xrange[0] <= i <= element.xrange[1] and \
#                element.yrange[0] <= j <= element.yrange[1]:
#                 return element.lap(i,j)/float(len(elements)**2)
#         
#     # return (4*global_u(elements, i,j)-global_u(elements,i-dn,j)-global_u(elements,i+dn,j)-global_u(elements,i,j-dn)-global_u(elements,i,j+dn))/dn

def bitmap(elements, i, j, delta, dn):
    # ii = int(math.floor(i*len(elements)))
    # jj = int(math.floor(j*len(elements)))
    # if(ii == len(elements)):
    #     ii -= 1
    # if(jj == len(elements)):
    #     jj -= 1
    # element = elements[jj][ii]
    
    for row in elements:
        for element in row:
            if element.xrange[0] <= i <= element.xrange[1] and \
               element.yrange[0] <= j <= element.yrange[1]:
                return element.u(i,j)+delta*element.lap(i,j)/float(len(elements)**2)+delta*element.f(i,j)

if __name__ == '__main__':
    if len(sys.argv)  != 5:
        print ('[!] Invalid number of arguments.')
        print ('[i] Usage: %s <n> <time steps> <delta> <dn>')
        sys.exit(1)
    
    n = int(sys.argv[1])
    steps = int(sys.argv[2])
    delta = float(sys.argv[3])
    dn = float(sys.argv[4])

    elements = [[Element((1.0*i/n,(i+1.0)/n), (1.0*j/n,(j+1.0)/n)) for i in xrange(n)] for j in xrange(n)]

    g5 = lambda x: functions[4](x, 0.0)**2
    q5l = q6l = q7l = q8l = quad(g5, 0.0, 1.0, vec_func=False, maxiter = 10)[0]/float(n)
    
    print [q5l, q6l, q7l, q8l]
    #             
    for t in xrange(steps):
          print t
          for row in elements:
              for element in row:
                  element.coeff[0] = bitmap(elements, element.xrange[0], element.yrange[0], delta, 1.0/n)
                  element.coeff[1] = bitmap(elements, element.xrange[0], element.yrange[1], delta, 1.0/n)
                  element.coeff[2] = bitmap(elements, element.xrange[1], element.yrange[1], delta, 1.0/n)
                  element.coeff[3] = bitmap(elements, element.xrange[1], element.yrange[0], delta, 1.0/n)
                                        
                  f5 = lambda x: (bitmap(elements, x, element.yrange[0], delta, dn) - element.coeff[0] * element.functions[0](x, element.yrange[0])  - element.coeff[1] * element.functions[1](x, element.yrange[0]) - element.coeff[2] * element.functions[2](x, element.yrange[0]) - element.coeff[3] * element.functions[3](x, element.yrange[0]))*element.functions[4](x, element.yrange[0])
                  f6 = lambda x: (bitmap(elements, element.xrange[1], x, delta, dn) - element.coeff[0] * element.functions[0](element.xrange[1], x)  - element.coeff[1] * element.functions[1](element.xrange[1], x) - element.coeff[2] * element.functions[2](element.xrange[1], x) - element.coeff[3] * element.functions[3](element.xrange[1], x))*element.functions[5](element.xrange[1], x)
                  f7 = lambda x: (bitmap(elements, x, element.yrange[1], delta, dn) - element.coeff[0] * element.functions[0](x, element.yrange[1])  - element.coeff[1] * element.functions[1](x, element.yrange[1]) - element.coeff[2] * element.functions[2](x, element.yrange[1]) - element.coeff[3] * element.functions[3](x, element.yrange[1]))*element.functions[6](x, element.yrange[1])
                  f8 = lambda x: (bitmap(elements, element.xrange[0], x, delta, dn) - element.coeff[0] * element.functions[0](element.xrange[0], x)  - element.coeff[1] * element.functions[1](element.xrange[0], x) - element.coeff[2] * element.functions[2](element.xrange[0], x) - element.coeff[3] * element.functions[3](element.xrange[0], x))*element.functions[7](element.xrange[0], x)
                  
                  q5u = quad(f5, element.xrange[0], element.xrange[1], vec_func=False, maxiter=2)[0]
                  q7u = quad(f7, element.xrange[0], element.xrange[1], vec_func=False, maxiter=2)[0]

                  q6u = quad(f6, element.yrange[0], element.yrange[1], vec_func=False, maxiter=2)[0]
                  q8u = quad(f8, element.yrange[0], element.yrange[1], vec_func=False, maxiter=2)[0]
                  
                  element.coeff[4] = q5u/q5l 
                  element.coeff[5] = q6u/q6l 
                  element.coeff[6] = q7u/q7l 
                  element.coeff[7] = q8u/q8l 

    im = Image.new('L',(512,512))
    pix = im.load()
    
    print "Rendering"
    
    max_u = -float('inf')
    
    for x in xrange(512):
        for y in xrange(512):
            u = abs(global_u(elements, x/511.0, y/511.0))
            if u > max_u:
              max_u = u

    for x in xrange(512):
        for y in xrange(512):
            u = global_u(elements, x/511.0, y/511.0)/max_u * 127.0
            pix[x, y] = u+127.0    

    im.save('output.png')
        

