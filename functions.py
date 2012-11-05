#!/usr/bin/env python

functions = [ lambda x,y: (1.0-x)*(1.0-y),  # fi1
              lambda x,y: x*(1.0-y),        # fi2
              lambda x,y: x*y,              # fi3
              lambda x,y: (1.0-x)*y,        # fi4
              lambda x,y: (1.0-x)*x*(1.0-y),    # fi5
              lambda x,y: x*(1.0-y)*y,        # fi6
              lambda x,y: y*(1.0-x)*x,        # fi7
              lambda x,y: (1.0-y)*(1.0-x)*y,    # fi8
              lambda x,y: (1.0-x)*x*y*(1.0-y) ] # fi9

df_dx = [ lambda x,y: y-1.0,
          lambda x,y: 1.0-y,
          lambda x,y: y,
          lambda x,y: -y,
          lambda x,y: 1.0-y-2*x*(1.0-y),
          lambda x,y: y-y*y,
          lambda x,y: y-2*x*y,
          lambda x,y: y*y-y,
          lambda x,y: y-y*y-2*x*(y-y*y) ]

df_dy = [ lambda x,y: x-1.0,
          lambda x,y: -x,
          lambda x,y: x,
          lambda x,y: 1.0-x,
          lambda x,y: x*x-x,
          lambda x,y: x-2*x*y,
          lambda x,y: x-x*x,
          lambda x,y: 1.0-x-2.0*y*(1.0-x),
          lambda x,y: x-x*x-2.0*y*(x-x*x) ]

def shift_me_baby(f, a, b, c, d):
    return lambda x,y: f((x-a)/(b-a), (y-c)/(d-c))
        
    
              
