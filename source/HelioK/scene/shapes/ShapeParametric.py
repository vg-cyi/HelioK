from .ShapeXY import *



class ShapeParametric:
    """
    Combines shape function and aperture
    """
    # function # parabola, sphere
    # aperture
    
    def __init__(self,
             functions=ShapeFlat(),
             aperture=None
        ):
        self.functions = functions
        if aperture:
            self.aperture = aperture
        else:
            self.aperture = functions.defaultAperture()
        