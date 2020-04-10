import math
import numpy as np
import numba

paramsType = np.dtype([
    ('xA', np.float32),
    ('xB', np.float32),
    ('xSize', np.int32),
    ('xStep', np.float32),
    ('yA', np.float32),
    ('yB', np.float32),
    ('ySize', np.int32),
    ('yStep', np.float32)
], align = True)


@numba.njit(numba.float32(numba.typeof(paramsType)[:], numba.float32[:, :], numba.float32, numba.float32))
def interpolate(params, data, x, y):
    # bilinear interpolation
    
    for p in params:
        # bounding
        if x < p.xA: xb = p.xA
        elif x > p.xB: xb = p.xB
        else: xb = x
        
        if y < p.yA: yb = p.yA
        elif y > p.yB: yb = p.yB
        else: yb = y
        
        # unit square
        xs = (xb - p.xA)/p.xStep # scaled       
        xn = math.floor(xs) # integer  
        xf = xs - xn # fractional
        if xn >= p.xSize - 1: 
            xn = p.xSize - 2
            xf = 1.
        xfc = 1. - xf
        
        ys = (yb - p.yA)/p.yStep
        yn = math.floor(ys)
        yf = ys - yn
        if yn >= p.ySize - 1: 
            yn = p.ySize - 2
            xf = 1.        
        yfc = 1. - yf
        
        # corners
        f11 = data[xn][yn]
        f12 = data[xn][yn + 1]
        f21 = data[xn + 1][yn]
        f22 = data[xn + 1][yn + 1]

        # bilinear
        ans1 = xfc*f11 + xf*f21
        ans2 = xfc*f12 + xf*f22
        return yfc*ans1 + yf*ans2
    return 0.

"""
params = np.array([
(0., 1., 11, 0.1, 0., 1., 11, 0.1)
], dtype = paramsType)   

data = np.array(
    np.arange(11*11).reshape(11,11),
dtype = np.float32)

interpolationGrid(params, data, np.float32(0.), np.float32(0.))
"""