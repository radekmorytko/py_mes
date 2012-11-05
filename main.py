#!/usr/bin/env python

from mes import Mes
from bmp_loader import Bitmap
from element import Element
from functions import functions
import sys
import numpy
import matplotlib.pyplot as plt

if __name__ == '__main__':
    assert len(sys.argv) == 3, 'Usage: {0} <n> <path to bitmap>'.format(sys.argv[0])     
    n = int(sys.argv[1])
    bmp_file = sys.argv[2]
    bitmap = Bitmap(bmp_file)

    new_bitmap = numpy.matrix(numpy.zeros((n*64,n*64)))

    mes = Mes(bitmap, n)
    elements = [ [ Element(mes,i,j,10) for i in xrange(0,n) ] for j in xrange(0,n) ]
    i = 0
    for row in elements:
        for element in row:
            i += 1
            print i
            element.calculate_a()
            element.calculate_b()
            element.calculate_c()
#            print element.u(0.5, 0.5)
#            print mes.bitmap_value(element.i*mes.pixels_per_x, element.j*mes.pixels_per_y)
            for x in xrange(0,64):
                for y in xrange(0, 64):
                    new_bitmap[element.j*64+y, element.i*64+x] = element.u(x/64.0, y/64.0)
    plt.axis('off')
    plt.imshow(new_bitmap, cmap=plt.cm.gray)
    plt.show()
#    raw_input()
