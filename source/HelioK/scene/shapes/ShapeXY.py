from .ShapeUV import *



class ShapeXY(ShapeUV):
    # ShapeXY describes a parameteric surface extrudable in z-direction
    # p.x, p.y in the range [-inf, inf]
    # for sphere check limits
    
    def __init__(self):
        ShapeUV.__init__(self)
    
    def defaultAperture(self):
        return ApertureRectangular((-1., 1.), (-1., 1.))    
    
    
    
class ShapeFlat(ShapeXY):
    # ShapeFlat describes a flat surface
    
    def __init__(self):
        ShapeXY.__init__(self)
       
    def findNormal(self, p):
        return mu.Vector([0., 0., 1.])  
    
    

class ShapeParabolic(ShapeXY):
    # ShapeParabolic describes parabolic shape 
    f = None # focus
    
    def __init__(self, focus = 1.):
        ShapeXY.__init__(self)
        self.f = focus
    
    def findPoint(self, p):
        z = (p.x**2 + p.y**2)/(4.*self.f)
        return mu.Vector([p.x, p.y, z]) 
    
    def findJacobian(self, p):
        k = -1./(2.*self.f)
        return mu.Vector([k*p.x, k*p.y, 1.])  
    
    
    
class ShapeParabolicXY(ShapeXY):
    # ShapeParabolic describes parabolic shape   
    fX = None # focus X
    fY = None
    
    def __init__(self, focusX = 1., focusY = 1.):
        ShapeXY.__init__(self)
        self.fX = focusX
        self.fY = focusY
    
    def findPoint(self, p):
        z = p.x**2/(4.*self.fX) + p.y**2/(4.*self.fY)
        return mu.Vector([p.x, p.y, z]) 
    
    def findJacobian(self, p):
        return mu.Vector([-p.x/(2.*self.fX), -p.y/(2.*self.fY), 1.])    
    
    
    
class ShapeSpherical(ShapeXY):
    # ShapeSpherical describes spherical shape (half)
    r = None # radius 
    
    def __init__(self, radius = 1.):
        ShapeXY.__init__(self)
        self.r = radius
    
    def findPoint(self, p):  
        z = self.r - mt.sqrt(self.r**2 - p.x**2 - p.y**2)
        return mu.Vector([p.x, p.y, z]) 
    
    def findJacobian(self, p):     
        s = -1./mt.sqrt(self.r**2 - p.x**2 - p.y**2)
        return mu.Vector([s*p.x, s*p.y, 1.])
    
    
    
class ShapeSphericalXY(ShapeXY):
    # ShapeSphericalXY describes spherical shape (half) 
    rX = None # radius X
    rY = None 
    rZ = None 
    
    def __init__(self, radiusX = 1., radiusY = 1., radiusZ = 1.):
        ShapeXY.__init__(self)
        self.rX = radiusX
        self.rY = radiusY
        self.rZ = radiusZ
    
    def findPoint(self, p):  
        s = mt.sqrt(1. - (p.x/self.rX)**2 - (p.y/self.rY)**2)
        z = self.rZ*(1. - s)
        return mu.Vector([p.x, p.y, z]) 
    
    def findJacobian(self, v): 
        k = -self.rZ/mt.sqrt(1. - (p.x/self.rX)**2 - (p.y/self.rY)**2)
        return mu.Vector([k*p.x/self.rX**2, k*p.y/self.rY**2, 1.])  
        