#!/usr/bin/env python

import Image
import numpy

def YCbCr(point):
    """
    Returns point value converted to YCbCr. Currently only 'Y' part is returned.
    """

    return 0.299 * point[0] + 0.587 * point[1] + 0.114 * point[2]

class Bitmap:
    def __init__(self, filename):
        self.img = Image.open(filename)
        self.img.load()
        self.width, self.height = self.img.size
    
    def as_matrix(self, convert_func = YCbCr):
        matrix = numpy.zeros((self.width, self.height))
        print self.width, self.height
        for i in xrange(0, self.width):
            for j in xrange(0, self.height):
                matrix[i,j] = convert_func(self.img.getpixel((i,j)))
        return numpy.matrix(matrix)


if __name__ == '__main__':
    b = Bitmap('./bitmaps/test.png')
    mat = b.as_matrix()
    print mat*(2+1j)
    
