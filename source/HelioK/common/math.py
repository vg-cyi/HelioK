import math as mt
import mathutils as mu



twopi = 2*mt.pi # 2*pi
degree = twopi/360 # 1 degree in radians
hour = twopi/24 # 1 hour in radians



def normalizeAngle(phi, phi0=-mt.pi):
    """
    normalize angle phi to the range [phi0, phi0 + pi)
    """
    return phi - twopi*mt.floor((phi - phi0)/twopi)


def clamp(x, a, b):
    """
    clip x between a and b
    """
    if x <= a: return a
    if x >= b: return b 
    return x


rotationENZ = [(1., 0., 0.), (0., 1., 0.), (0., 0., 1.)] # identity
rotationWZN = [(-1., 0., 0.), (0., 0., 1.), (0., 1., 0.)] # (x, y, z) -> (-x, z, y)


def makeTransform(translation=[0., 0., 0.], rotation=mu.Matrix.Identity(3)):
    transform = mu.Matrix(rotation).to_4x4()
    transform.translation = translation 
    return transform


class Vertex:
    # point and normal
    point: mu.Vector
    normal: mu.Vector
        
    def __init__(self, point = [0., 0., 0.], normal = [0., 0., 1.]):
        self.point = mu.Vector(point)
        self.normal = mu.Vector(normal)
      
    @classmethod
    def copy(cls, v):  
        return cls(v.point, v.normal)
    
    def transform(self, t):
        self.point = t@self.point
        self.normal = t.to_3x3()@self.normal

    def transformed(self, t):
        return Vertex(t@self.point, t.to_3x3()@self.normal)
    
    def transformed2(self, t, t2):
        # slightly faster
        return Vertex(t@self.point, t2@self.normal)
    
    def __repr__(self):
        return 'Vertex(point = {}, normal = {})'.format(
            list(self.point),
            list(self.normal)
        )