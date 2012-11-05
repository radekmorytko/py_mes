#!/usr/bin/env python

from scipy.integrate import quadrature as quad

from functions import shift_me_baby, df_dx, df_dy, functions

class Element:
    def __init__(self, mes, i, j):
        self.i, self.j = i, j
        self.mes = mes
        self.a, self.b, self.c, self.d = mes.ij_to_abcd(i,j)
        self.coeff = [ None ]*9
    
    def calculate_a(self):
        a,b,c,d = self.a, self.b, self.c, self.d
        
        self.coeff[0] = self.mes.bitmap_value(a,c)
        self.coeff[1] = self.mes.bitmap_value(b,c)
        self.coeff[2] = self.mes.bitmap_value(c,d)
        self.coeff[3] = self.mes.bitmap_value(a,d)
        
    
    def calculate_b(self):
        a,b,c,d = self.a, self.b, self.c, self.d
        f5 = lambda x: (self.mes.bitmap_derivative_x(x, c) - (self.coeff[0] * shift_me_baby(df_dx[0], a, b, c, d)(x, c) + self.coeff[1] * shift_me_baby(df_dx[1], a, b, c, d)(x, c) + self.coeff[2] * shift_me_baby(df_dx[2], a, b, c, d)(x, c) + self.coeff[3] * shift_me_baby(df_dx[3], a, b, c, d)(x, c))*shift_me_baby(functions[4], a, b, c, d)(x, c))
        f6 = lambda y: (self.mes.bitmap_derivative_y(b, y) - (self.coeff[0] * shift_me_baby(df_dy[0], a, b, c ,d)(b, y) + self.coeff[1] * shift_me_baby(df_dy[1], a, b, c, d)(b, y) + self.coeff[2] * shift_me_baby(df_dy[2], a, b, c, d)(b, y) + self.coeff[3] * shift_me_baby(df_dy[3], a, b, c, d)(b, y)) * shift_me_baby(functions[5], a, b, c, d)(b, y))
        f7 = lambda x: (self.mes.bitmap_derivative_x(x, d) - (self.coeff[0] * shift_me_baby(df_dx[0], a, b, c, d)(x, d) + self.coeff[1] * shift_me_baby(df_dx[1], a, b, c, d)(x, d) + self.coeff[2] * shift_me_baby(df_dx[2], a, b, c, d)(x, d) + self.coeff[3] * shift_me_baby(df_dx[3], a, b, c, d)(x, d))*shift_me_baby(functions[6], a, b, c, d)(x, d))
        f8 = lambda y: (self.mes.bitmap_derivative_y(a, y) - (self.coeff[0] * shift_me_baby(df_dy[0], a, b, c ,d)(a, y) + self.coeff[1] * shift_me_baby(df_dy[1], a, b, c, d)(a, y) + self.coeff[2] * shift_me_baby(df_dy[2], a, b, c, d)(a, y) + self.coeff[3] * shift_me_baby(df_dy[3], a, b, c, d)(a, y)) * shift_me_baby(functions[7], a, b, c, d)(a, y))

        g5 = lambda x: shift_me_baby(df_dx[4], a, b, c, d)(x, c)
        g6 = lambda y: shift_me_baby(df_dy[5], a, b, c, d)(b, y)
        g7 = lambda x: shift_me_baby(df_dx[6], a, b, c, d)(x, d)
        g8 = lambda y: shift_me_baby(df_dy[7], a, b, c, d)(a, y)


        self.coeff[4] = quad(f5, a, b, vec_func=False, maxiter=100)[0]/quad(g5, a, b, vec_func=False, maxiter=100)[0]
        self.coeff[5] = quad(f6, c, d, vec_func=False, maxiter=100)[0]/quad(g6, c, d, vec_func=False, maxiter=100)[0]
        self.coeff[6] = quad(f7, a, b, vec_func=False, maxiter=100)[0]/quad(g7, a, b, vec_func=False, maxiter=100)[0]
        self.coeff[7] = quad(f8, c, d, vec_func=False, maxiter=100)[0]/quad(g8, c, d, vec_func=False, maxiter=100)[0]

    
    def calculate_c(self):
        pass

