#!/usr/bin/env python

from mes import Mes
from bmp_loader import Bitmap
from element import Element
from functions import functions
import sys

if __name__ == '__main__':
    assert len(sys.argv) == 3, 'Usage: {0} <n> <path to bitmap>'.format(sys.argv[0])     
    n = int(sys.argv[1])
    bmp_file = sys.argv[2]
    bitmap = Bitmap(bmp_file)
    
    mes = Mes(bitmap, n)
    elements = [ [ Element(mes,i,j) for i in xrange(0,n) ] for j in xrange(0,n) ]
    
    for row in elements:
        for element in row:
            element.calculate_a()
            element.calculate_b()
            element.calculate_c()
            print element.u(0.5, 0.5)
            print mes.bitmap_value(element.i*mes.pixels_per_x, element.j*mes.pixels_per_y)
