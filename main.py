#!/usr/bin/env python

from mes import Mes
from bmp_loader import Bitmap
from element import Element
from functions import functions
import sys
import numpy
import matplotlib.pyplot as plt
import math

import Image

if __name__ == '__main__':
    assert len(sys.argv) == 3, 'Usage: {0} <n> <path to bitmap>'.format(sys.argv[0])     
    n = int(sys.argv[1])
    bmp_file = sys.argv[2]
    bitmap = Bitmap(bmp_file)

    ratio = float(bitmap.height)/bitmap.width;
    print ratio
    new_bitmap = numpy.matrix(numpy.zeros((64*n,int(64*ratio)*n)))

    mes = Mes(bitmap, n)
    elements = [ [ Element(mes,i,j,2) for i in xrange(0,n) ] for j in xrange(0,n) ]
    i = 0
    
    im = Image.new('L',(64*n,int(64*ratio*n)))
    pix = im.load()
    
    
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
                for y in xrange(0, int(64*ratio)):
                    pix[element.i*64+x, element.j*int(64*ratio)+y] = element.u(x/64.0, y/(64.0*ratio))
    # plt.axis('off')
    # plt.imshow(new_bitmap, cmap=plt.cm.gray)
    # plt.show()
    im.save('output.png')
#    raw_input()
