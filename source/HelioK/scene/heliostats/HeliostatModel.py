from .HeliostatDrive import *
from .HeliostatFacet import *
from .HeliostatAiming import * 



class HeliostatModelCache:
    """
    HeliostatModelCache stores the cached values of various parameters
    """
    
    def __init__(self, a, b): 
        self.k = a.cross(b)
        self.k2 = (self.k).dot(self.k)  
        self.ab = a.dot(b)
        self.det = 1. - self.ab*self.ab 

        
        
class HeliostatModel:
    """
    HeliostatModel solves rotations in local (heliostat) frame
    """ 
    name: str
    primary: HeliostatDrive # primary drive
    secondary: HeliostatDrive # secondary drive
    tracking: Vertex # tracking vertex on heliostat (for zero angles)
    facets: List[HeliostatFacet]
    # angles: default angles
    # aiming: default aiming
    cache: HeliostatModelCache
        
    def __init__(self, name,
                 primary, secondary, tracking,
                 facets,
                 angles = (0.*degree, 0.*degree),
                 aiming = HeliostatAiming([0., 0., 1.], True)
        ):
        self.name = name
        self.primary = primary
        self.secondary = secondary
        self.facets = facets 
        # if not tracking:
        #     if not facets:
        #         tracking = Vertex()
        #     else:
        #         tracking = facets[0].getVertex()
        self.tracking = tracking
        self.angles = angles
        self.aiming = aiming
        self.cache = HeliostatModelCache(primary.rotationAxis, secondary.rotationAxis)             
        
    def selectTrackingAngles(self, angles):
        # select angles in tracking range
        # angles = [(alpha, beta),]
        # returns [(alpha, beta),]         
        ans = []
        pd = self.primary   
        sd = self.secondary   
        for (alpha, beta) in angles:
            alpha = pd.rotationAngles.normalizeAngle(alpha)  
            if not pd.rotationAngles.isInside(alpha): continue
            beta = sd.rotationAngles.normalizeAngle(beta)  
            if not sd.rotationAngles.isInside(beta): continue   
            ans.append((alpha, beta))
        return ans        
      
    def writeTrackingAngles(self, angles):
        # prints angles in degrees        
        (alpha, beta) = angles
        valid = True if self.selectTrackingAngles([(alpha, beta)]) else False
        return "α = {:.4f}°, β = {:.4f}°, trackable = {:}".format(alpha/degree, beta/degree, valid)   
        
    def findTrackingVertex(self, angles):
        # returns tracking vertex
        return self.tracking.transformed(self.findTransformFacets(angles))
    
    def findTrackingPoint(self, angles):
        # returns point of tracking vertex
        r = self.tracking.point
        r = self.secondary.getTransform(angles[1])@r
        r = self.primary.getTransform(angles[0])@r           
        return r

    def findTrackingNormal(self, angles):
        # returns normal of tracking vertex
        # angles = (alpha, beta)
        n = self.tracking.normal
        n = self.secondary.getTransform(angles[1]).to_3x3()@n     
        n = self.primary.getTransform(angles[0]).to_3x3()@n   
        return n  
    
    def findTransformFacets(self, angles):
        # returns mirror transform 
        t = self.secondary.getTransform(angles[1])
        t = self.primary.getTransform(angles[0])@t        
        return t
    
    def solveRotation(self, v0, v):
        # find the angles which rotate vector v0 (for zero angles) to v
        # returns [(alpha, beta),]  
        
        a = self.primary.rotationAxis
        b = self.secondary.rotationAxis
        cd = self.cache
        
        av = a.dot(v)
        bv0 = b.dot(v0)
        ma = (av - cd.ab*bv0)/cd.det
        mb = (bv0 - cd.ab*av)/cd.det             
        mk = 1. - ma*ma - mb*mb - 2.*ma*mb*cd.ab
        
        if mk < 0.: return []
        
        ans = []
        mk = mt.sqrt(mk/cd.k2)
        m0 = ma*a + mb*b
        for m in (m0 - mk*cd.k, m0 + mk*cd.k):
            alpha = mt.atan2(a.dot(m.cross(v)), m.dot(v) - av*av)      
            beta = mt.atan2(b.dot(v0.cross(m)), v0.dot(m) - bv0*bv0)  
            ans.append((alpha, beta))
            
        return ans
    
    def solveTrackingNormal(self, vNormal):
        # find tracking angles for a mirror normal
        # returns [(alpha, beta),]         
        return self.solveRotation(self.tracking.normal, vNormal)
    
    def solveReflectionRelative(self, vSun, rAim):
        # reflect sun to aiming point
        # aiming for zero angles
        # returns [(alpha, beta),]         
        vTarget0 = (rAim - self.tracking.point).normalized() # reflector frame
        vSun0 = -vTarget0.reflect(self.tracking.normal) # default, heliostat frame
        return self.solveRotation(vSun0, vSun) 
        
    def solveReflectionAbsolute(self, vSun, rAim, debug = False):
        # reflect sun to aiming point     
        # returns [(alpha, beta),]         
        ans = []
        iterationsMax = 5 # max iterations
        deltaMin = 0.01 # accuracy in meters
        
        for s in (0, 1):
            if debug: print('Solution {}:'.format(s))
            rMirror = self.findTrackingPoint(self.angles)
            for iteration in range(0, iterationsMax): 
                vTarget = (rAim - rMirror).normalized()
                vNormal = (vSun + vTarget).normalized() 
                angles = self.solveTrackingNormal(vNormal)
                if not angles: break 
                angles = angles[s]  
                rMirror = self.findTrackingPoint(angles)
                delta = (rAim - rMirror).cross(vTarget).length
                if debug:
                    out = self.writeTrackingAngles(angles)
                    out += ', accuracy = {:.4f} m'.format(delta)
                    print(out)
                if delta < deltaMin:
                    ans.append(angles) 
                    break
            #if debug: print()
        
        return ans
    