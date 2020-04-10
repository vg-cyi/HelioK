from HelioK.common.math import *



class SunShape:
    """
    SunShape gives irradiance going in direction
    """
#     irradiance = None # integrated radiance for L0 = 1
#     thetaMax = None
    
    def findRadiance(self, theta):
        return 0.
    
    def findRadianceV(self, vSun, vRay):
        cosTheta = -vSun.dot(vRay)
        theta = mt.acos(cosTheta)        
        return self.findRadiance(theta)



class SunShapePillbox(SunShape):
#     cosThetaMax = None # for fast check
    
    def __init__(self, thetaMax = 4.65/1000):
        assert thetaMax > 0.
        self.thetaMax = thetaMax
        self.cosThetaMax = mt.cos(thetaMax)
        sin2ThetaMax = 1. - self.cosThetaMax**2
        self.irradiance = mt.pi*sin2ThetaMax
    
    def findRadiance(self, theta):
        if mt.fabs(theta) > self.thetaMax: return 0.
        return 1.
    
    def findRadianceV(self, vRay, vSun):
        cosTheta = -vSun.dot(vRay)        
        if cosTheta < self.cosThetaMax: return 0.
        return 1.


    
class SunShapeGaussian(SunShape):
#     thetaG = None
    
    def __init__(self, thetaG = 2.51/1000, thetaMax = None):
        assert thetaG > 0.
        self.thetaG = thetaG
        if not thetaMax: thetaMax = 5.*thetaG
        self.thetaMax = thetaMax        
        self.irradiance = 2.*mt.pi*thetaG**2
    
    def findRadiance(self, theta):
        if mt.fabs(theta) > self.thetaMax: return 0.
        temp = theta/self.thetaG
        return mt.exp(-temp**2/2.) 
    


class SunShapeLimbDarkened(SunShape):   
#     thetaZ = None
    
    def __init__(self, thetaZ = 5.49/1000, thetaMax = 4.65/1000): 
        assert thetaZ > 0.        
        self.thetaZ = thetaZ
        self.thetaMax = thetaMax         
        temp = 1. - (thetaMax/thetaZ)**4/3.
        self.irradiance = mt.pi*thetaMax**2*temp
        
    def findRadiance(self, theta):
        if mt.fabs(theta) > self.thetaMax: return 0.
        return 1. - (theta/self.thetaZ)**4
    

    
class SunShapeBuieRational(SunShape):  
#     csr circumsolar ratio    
#     thetaZ = None
#     thetaP = None
#     thetaS = None # sun disk
#     gamma = None
#     zeta = None
    
    def __init__(self, csr = 0.02): 
        self.thetaZ = 4.84/1000 # zero
        self.thetaP = 5.17/1000 # pole
        self.thetaS = 4.65/1000 # sun disk
        self.thetaMax = 43.6/1000 # sun aureole
        self.setCSR(csr)    
        
    def setCSR(self, csr):
        # set circumsolar ratio
        assert csr > 0. and csr < 1. 
        self.csr = csr
        self.gamma = 1.6333*(csr + 0.021)/(csr + 0.048)*(csr - 1.975)
        s = 0.426
        g = self.gamma + 2.
        temp = self.thetaMax/self.thetaS
        self.zeta = csr/(1. - csr)*s*g/(temp**g - 1.)
        self.irradiance = 2.*mt.pi*s*self.thetaS**2/(1. - csr)        
        
    def findRadiance(self, theta):
        theta = mt.fabs(theta)
        if theta > self.thetaMax: return 0.
        if theta < self.thetaS: 
            temp = 1. - (theta/self.thetaZ)**2
            temp /= 1. - (theta/self.thetaP)**2
            return temp
        else:
            return self.zeta*(theta/self.thetaS)**self.gamma
        