from HelioK.common.math import *



class HeliostatAiming:
    point = None # point
    relative = None # relative (reflector frame) or absolute (global frame)
        
    def __init__(self, point, relative = False):
        self.point = mu.Vector(point)
        self.relative = relative