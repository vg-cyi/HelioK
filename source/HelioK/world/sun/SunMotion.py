from ..location.Location import *



class SunMotion:
    """
    SunMotion is used for sun motion    
    vector # unit vector to the sun
    location # location
    cosPhi # cos(latitude)
    sinPhi # sin(latitude)    
    """    
    obliquity = 23.438*degree # obliquity

    def __init__(self):
        self.setLocation(Location())
        self.vector = mu.Vector([0., 0., 1.])

    def setLocation(self, location):
        # set location
        self.location = location
        self.cosPhi = mt.cos(location.latitude)
        self.sinPhi = mt.sin(location.latitude)

    def setAE(self, azimuth, elevation):
        # set azimuth and elevation
#         v = mu.Vector([0., 1., 0.])
#         v = mu.Matrix.Rotation(elevation, 3, 'X')@v
#         v = mu.Matrix.Rotation(-azimuth, 3, 'Z')@v
#         self.vector = v

        cosAlpha = mt.cos(elevation)
        self.vector = mu.Vector([
            mt.sin(azimuth)*cosAlpha,
            mt.cos(azimuth)*cosAlpha,
            mt.sin(elevation)
        ])

    def findAE(self):
        # find azimuth and elevation
        alpha = mt.asin(self.vector.z)
        gamma = mt.atan2(self.vector.x, self.vector.y)
        return (gamma, alpha)

    def printAE(self):
        # print azimuth and elevation
        (az, el) = self.findAE()
        return print('azimuth = {:.3f}°, elevation = {:.3f}°'.format(az/degree, el/degree))
        
    def setHD(self, hourAngle, declination):
        # set hour angle and declination
#         v = mu.Vector([0., 0., 1.])
#         v = mu.Matrix.Rotation(-declination, 3, 'X')@v
#         v = mu.Matrix.Rotation(-hourAngle, 3, 'Y')@v
#         v = mu.Matrix.Rotation(self.latitude, 3, 'X')@v
#         self.vector = v

        cosDelta = mt.cos(declination)
        sinDelta = mt.sin(declination)
        cosOmegaDelta = mt.cos(hourAngle)*cosDelta
        self.vector = mu.Vector([
            -mt.sin(hourAngle)*cosDelta,
            self.cosPhi*sinDelta - self.sinPhi*cosOmegaDelta,
            self.sinPhi*sinDelta + self.cosPhi*cosOmegaDelta
        ])

    def findHD(self):
        # find hour angle and declination
        delta = mt.asin(self.vector.y*self.cosPhi + self.vector.z*self.sinPhi)
        omega = mt.atan2(-self.vector.x, -self.vector.y*self.sinPhi + self.vector.z*self.cosPhi)
        return (omega, delta)

    def findAboveH(self, declination = 0., elevation = 0.):
        # find hour angles when sun is above elevation
        a = mt.sin(elevation) - self.sinPhi*mt.sin(declination)
        b = self.cosPhi*mt.cos(declination)
        
        if a >= b: # cosOmega = 1
            return () # always below 
        elif a <= -b: # cosOmega = -1 
            return (-mt.pi, mt.pi) # always above
        
        hSet = mt.acos(a/b)
        return (-hSet, hSet) # rise and set
        
    def findAboveD(self, omega = 0., elevation = 0.):
        # find declinations when sun is above elevation
        # A cos(delta - delta0) > sin(elevation)   
        S = self.sinPhi
        C = mt.cos(omega)*self.cosPhi
        A = mt.sqrt(S*S + C*C)
        if A <= 1e-6:
            if elevation <= 1e-6: 
                return (-self.obliquity, self.obliquity)
            else:
                return ()   
            
        delta0 = mt.atan2(S, C) # decliantion at zenith
        D = mt.sin(elevation)/A
        deltaX = mt.acos(D)
        
        deltaA = max(-self.obliquity, delta0 - deltaX)
        deltaB = min(delta0 + deltaX, self.obliquity)
        if deltaA < deltaB: 
            return (deltaA, deltaB)
        else: 
            return ()
    
    def setTime(self, udt):
        # set UTC time
        pass
    
    def findAboveT(self, udt, elevation = 0., solution = -1):
        # find UTC time when sun is above elevation 
        # solutions for rise (-1), noon transit (0), set (1)    
        # returns modified udt 
        pass