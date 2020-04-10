from HelioK.common.Interval import *

    
    
class ApertureRectangular(Interval2D):
    # ApertureRectangular describes rectangular aperture
    
    def __init__(self, us = (-1., 1.) , vs = (-1., 1.)):
        # identity mapping by default
        Interval2D.__init__(self, us, vs)
        
    @classmethod
    def sides(cls, xWidth, yWidth):    
        w = xWidth/2
        h = yWidth/2     
        return cls((-w, w), (-h, h)) 
        

# class ApertureDisk