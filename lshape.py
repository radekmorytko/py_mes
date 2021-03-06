#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from mes import Mes
from functions import functions, shift_me_baby, d2f_dx, d2f_dy
from gauss import quad

import sys
import numpy

import math

import Image

gridNodes = []
horizontalEdges = []
verticalEdges = []
centers = []
n = 0

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

        return sum([fun(i, j) * coeff for fun, coeff in zip(self.functions, self.coeff)])

    def only_vertex_u(self, i, j):
        assert self.xrange[0] <= i <= self.xrange[1], "Out of x range!"
        assert self.yrange[0] <= j <= self.yrange[1], "Out of y range!"
        if i < 0.5 and j < 0.5:
            return 0

        return sum([fun(i, j) * coeff for fun, coeff in zip(self.functions[:4], self.coeff[:4])])

    def lap(self, i, j):
        assert self.xrange[0] <= i <= self.xrange[1], "Out of x range!"
        assert self.yrange[0] <= j <= self.yrange[1], "Out of y range!"
        #
        if i < 0.5 and j < 0.5:
            return 0

        return sum([fun(i, j) * coeff for fun, coeff in zip(self.functions2x, self.coeff)]) + sum([fun(i, j) * coeff for fun, coeff in zip(self.functions2y, self.coeff)])

    def f(self, i, j):
        if i == 0.0 and j >= 0.5:
            return 1.0-self.u(i,j)
        elif j == 0.0 and i >= 0.5:
            return -1.0 - self.u(i,j)
        else:
            return 0.0

    def setCoeffs(self, coeffs, i, j):
        global gridNodes
        global horizontalEdges
        global verticalEdges
        global centers
        self.coeff = coeffs
        gridNodes[i][j] = coeffs[0]
        gridNodes[i+1][j] = coeffs[1]
        gridNodes[i+1][j+1] = coeffs[2]
        gridNodes[i][j+1] = coeffs[3]
        horizontalEdges[i][j] = coeffs[4]
        verticalEdges[i+1][j] = coeffs[5]
        horizontalEdges[i][j+1] = coeffs[6]
        verticalEdges[i][j] = coeffs[7]
        centers[i][j] = coeffs[8]

def global_u(elements, x, y):
    if x < 0.0:
        x = 0.0
    if y < 0.0:
        y = 0.0
    if x > 1.0:
        x = 1.0
    if y > 1.0:
        y = 1.0

    i = int(math.floor(x*n))
    j = int(math.floor(y*n))

    if i == n:
        i = n-1
    if j == n:
        j = n-1

    #print i, j

    for row in elements:
        for element in row:
            if element.xrange[0] <= x <= element.xrange[1] and \
               element.yrange[0] <= y <= element.yrange[1]:
                #element.coeff = [gridNodes[i][j], gridNodes[i+1][j], gridNodes[i+1][j+1], gridNodes[i][j+1], \
                #                 horizontalEdges[i][j], verticalEdges[i+1][j], horizontalEdges[i][j+1], verticalEdges[i][j], \
                #                 centers[i][j]]
                element.coeff = [gridNodes[i][j], gridNodes[i+1][j], gridNodes[i+1][j+1], gridNodes[i][j+1], \
                                 0, 0, 0, 0, 0]
                return element.u(x,y)

    raise  Exception("nie znaleziono! %f %f" % (i, j) )

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

def initialize():
    global n
    global elements
    global gridNodes
    global horizontalEdges
    global verticalEdges
    global centers
    n = int(sys.argv[1])
    gridNodes = [[0 for i in xrange(n + 1)] for j in xrange(n + 1)]
    horizontalEdges = [[0 for i in xrange(n + 1)] for j in xrange(n)]
    verticalEdges = [[0 for i in xrange(n)] for j in xrange(n + 1)]
    centers = [[0 for i in xrange(n)] for j in xrange(n)]

def render():
    global n
    global elements
    global gridNodes
    global horizontalEdges
    global verticalEdges
    global centers
    im = Image.new('L',(512,512))
    pix = im.load()

    print "Rendering"
    print gridNodes
    print horizontalEdges
    print verticalEdges
    print centers

    max_u = -float('inf')

    for x in xrange(512):
        for y in xrange(512):
            u = abs(global_u(elements, x/511.0, y/511.0))
            if u > max_u:
              max_u = u

    if max_u == 0:
      max_u = 0.0001

    for x in xrange(512):
        for y in xrange(512):
            u = global_u(elements, x/511.0, y/511.0)/max_u * 127.0
            pix[x, y] = u+127.0

    im.save('output.png')


if __name__ == '__main__':
    if len(sys.argv)  != 5:
        print ('[!] Invalid number of arguments.')
        print ('[i] Usage: %s <n> <time steps> <delta> <dn>')
        sys.exit(1)

    steps = int(sys.argv[2])
    delta = float(sys.argv[3])
    dn = float(sys.argv[4])

    initialize()
    elements = [[Element((1.0*i/n,(i+1.0)/n), (1.0*j/n,(j+1.0)/n)) for i in xrange(n)] for j in xrange(n)]

    g5 = lambda x: functions[4](x, 0.0)**2
    q5l = q6l = q7l = q8l = quad(g5, 0.0, 1.0)/float(n)

    print [q5l, q6l, q7l, q8l]

    #
    for t in xrange(steps):
          print t
          for i in xrange(n):
              for j in xrange(n):
                  element = elements[i][j]
                  coeffs = [0] * 9
                  coeffs[0] = bitmap(elements, element.xrange[0], element.yrange[0], delta, 1.0/n)
                  coeffs[1] = bitmap(elements, element.xrange[0], element.yrange[1], delta, 1.0/n)
                  coeffs[2] = bitmap(elements, element.xrange[1], element.yrange[1], delta, 1.0/n)
                  coeffs[3] = bitmap(elements, element.xrange[1], element.yrange[0], delta, 1.0/n)
                  #element.setCoeffs(coeffs, i, j)

                  f5 = lambda x: (bitmap(elements, x, element.yrange[0], delta, dn) - element.only_vertex_u(x, element.yrange[0]))*element.functions[4](x, element.yrange[0])
                  f6 = lambda x: (bitmap(elements, element.xrange[1], x, delta, dn) - element.only_vertex_u(element.xrange[1], x))*element.functions[5](element.xrange[1], x)
                  f7 = lambda x: (bitmap(elements, x, element.yrange[1], delta, dn) - element.only_vertex_u(x, element.yrange[1]))*element.functions[6](x, element.yrange[1])
                  f8 = lambda x: (bitmap(elements, element.xrange[0], x, delta, dn) - element.only_vertex_u(element.xrange[0], x))*element.functions[7](element.xrange[0], x)

                  q5u = quad(f5, element.xrange[0], element.xrange[1])
                  q7u = quad(f7, element.xrange[0], element.xrange[1])

                  q6u = quad(f6, element.yrange[0], element.yrange[1])
                  q8u = quad(f8, element.yrange[0], element.yrange[1])

                  coeffs[4] = q5u/q5l
                  coeffs[5] = q6u/q6l
                  coeffs[6] = q7u/q7l
                  coeffs[7] = q8u/q8l
                  element.setCoeffs(coeffs, i, j)

    render()
