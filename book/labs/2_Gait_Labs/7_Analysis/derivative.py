import numpy as np

def symmetric_difference(x, y):
    #write a function here!
    xm = np.full_like(x, np.nan)
    xm[1:] = x[:-1]
    xp = np.full_like(x, np.nan)
    xp[:-1] = x[1:]
    ym = np.full_like(y, np.nan)
    ym[1:] = y[:-1]
    yp = np.full_like(y, np.nan)
    yp[:-1] = y[1:]
    
    h = xp - x
    k = x - xm
    
    d = (1/k) - (1/h)
    dm = -h/( k*(k+h) )
    dp = k/( h*(k+h) )
    
    derivative = dm*ym + d*y + dp*yp
    derivative[0] = (y[1]-y[0])/(x[1]-x[0])
    derivative[-1] = (y[-1] - y[-2])/(x[-1] -x[-2])
    
    return derivative