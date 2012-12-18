#!/usr/bin/env python
# -*- encoding: utf-8 -*-

def shift(arg, a, b):
    return (b - a) / 2.0 * float(arg) + (a + b) / 2.0

def quad(function, a, b):
    """Two point gauss quadrature"""
    rightPoint = 0.5773502691896
    leftPoint = -rightPoint
    f1 = function(shift(leftPoint, a, b))
    f2 = function(shift(rightPoint, a, b))
    return (b - a) / 2.0 * (f1 + f2)

