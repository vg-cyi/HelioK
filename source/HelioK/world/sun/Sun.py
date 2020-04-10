from .SunMotion import *
from .SunShape import *



class Sun:
    """
    Sun combines position and shape
    """    
    motion = None # direction to the sun
    shape = None
    irradiance = None # direct normal irradiance

    def __init__(self, motion = SunMotion(), shape = SunShapePillbox(), irradiance = 1000.):        
        self.motion = motion
        self.shape = shape
        self.irradiance = irradiance
                
    def findRadianceV(self, v):
        # radiance going in the direction of vector (global)
        a = self.irradiance/self.shape.irradiance
        return a*self.shape.findRadianceV(self.motion.vector, v)
    
    def findRadiance0(self):
        # coefficent for irradience
        return self.irradiance/self.shape.irradiance   
        