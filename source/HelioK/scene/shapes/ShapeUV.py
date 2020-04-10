from HelioK.common.math import *
from .Aperture import *



class ShapeUV:
    # ShapeUV describes a paramteric surface 
    # p.x, p.y in the range [0, 1]
    
    def __init__(self):
        pass
    
    def findPoint(self, p):
        #return point on surface  
        return mu.Vector([p.x, p.y, 0.]) 
    
    def findJacobian(self, v):
        #return Jacobian vector
        return mu.Vector([0., 0., 1.])  
    
    def findNormal(self, p):
        # return normal vector
        return self.findJacobian(p).normalized()
    
    def findVertex(self, p):
        return Vertex(self.findPoint(p), self.findNormal(p))
    
    def findCenter(self):
        return mu.Vector([0., 0., 0.])
    
    def findBox(self):
        pass
    
    def defaultAperture(self):
        return ApertureRectangular((0., 1.), (0., 1.))
    
    
    
class ShapeRectangle(ShapeUV):
    # ShapeRectangle describes a rectangle
    # p = x, y
    widthX = None
    widthY = None
    
    def __init__(self, widthX = 1., widthY = 1):
        ShapeUV.__init__(self)
        self.widthX = widthX
        self.widthY = widthY
        
    def findPoint(self, p):  
        x = self.widthX*(p.x - 0.5)
        y = self.widthY*(p.y - 0.5)
        return mu.Vector([x, y, 0.]) 
    
    def findNormal(self, p):
        return mu.Vector([0., 0., 1.])  
    
    

class ShapeSphere(ShapeUV):
    # ShapeSphere describes a sphere
    # p = phi, alpha
    radius = None
    
    def __init__(self, radius = 1.):
        ShapeUV.__init__(self)
        self.radius = radius
    
    def findPoint(self, p):  
        phi = 2.*mt.pi*p.x
        alpha = mt.pi*(p.y - 0.5)
        x = mt.cos(phi)*mt.cos(alpha)
        y = mt.sin(phi)*mt.cos(alpha)
        z = mt.sin(alpha)
        return self.radius*mu.Vector([x, y, z]) 
    
    def findNormal(self, p):
        phi = 2.*mt.pi*p.x
        alpha = mt.pi*(p.y - 0.5)
        x = mt.cos(phi)*mt.cos(alpha)
        y = mt.sin(phi)*mt.cos(alpha)
        z = mt.sin(alpha)
        return mu.Vector([x, y, z])   
    
    
    
class ShapeCylinder(ShapeUV):
    # ShapeCylinder describes a cylinder
    # p = phi, z
    radius = None # radius
    height = None # height
    
    def __init__(self, radius = 1., height = 1.):
        ShapeUV.__init__(self)
        self.radius = radius
        self.height = height
        
    def findPoint(self, p):
        phi = 2.*mt.pi*p.x
        x = self.radius*mt.cos(phi)
        y = self.radius*mt.sin(phi)
        z = self.height*(p.y - 0.5)  
        return mu.Vector([x, y, z]) 
    
    def findNormal(self, p):
        phi = 2.*mt.pi*p.x
        x = mt.cos(phi)
        y = mt.sin(phi)
        return mu.Vector([x, y, 0.]) 