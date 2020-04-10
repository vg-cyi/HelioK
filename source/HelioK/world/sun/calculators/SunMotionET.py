from ..SunMotion import *

from datetime import datetime, timedelta


class SunMotionET(SunMotion):
    """
    SunMotion based on equation of time
    """
    sinDeltaMax = mt.sin(obliquity) # obliquity of ecliptic

    def __init__(self):
        SunMotion.__init(self)
        
    def setTime(self, udt):       
        # time from spring equinox
        m = udt.month - 2
        if m <= 0: m += 12
        d = (367*m)//12 + udt.day - 51 # 21 March = 0 
        t = (udt.hour + (udt.minute + udt.second/60)/60)/24       
        b = twopi*(d + t)/365.24 
        cb = mt.cos(b)
        sb = mt.sin(b)
        
        # equatorial coordinates
        delta = mt.asin(self.sinDeltaMax*sb) # declination
        eot = (19.74*sb*cb - 7.53*cb - 1.5*sb)/(24*60) # equation of time
        omega = twopi*(t + eot - 0.5) + self.location.longitude # hour angle
        
        self.setHD(omega, delta)
        
    def findAboveT(self, udt, elevation = 0., solution = -1):       
        # time from spring equinox
        m = udt.month - 2
        if m <= 0: m += 12
        d = (367*m)//12 + udt.day - 51 # 21 March = 0 
        t = (udt.hour + (udt.minute + udt.second/60)/60)/24       
        b = twopi*(d + t)/365.24 
        cb = mt.cos(b)
        sb = mt.sin(b)
        
        # equatorial coordinates
        delta = mt.asin(self.sinDeltaMax*sb) # declination
        eot = (19.74*sb*cb - 7.53*cb - 1.5*sb)/(24*60) # equation of time
        omega = twopi*(t + eot - 0.5) + self.location.longitude # hour angle
        
        if solution == 0:
            omegaX = 0.
        else:
            omegas = self.findAboveH(delta, elevation)        
            if len(omegas) == 0: 
                return False    
            if omegas[1] == mt.pi:
                return False
            if solution == -1:
                omegaX = omegas[0]
            elif solution == 1:
                omegaX = omegas[1]
        
        dt = -(omega - omegaX)/twopi        
#         sdt = 24*mt.fabs(dt)        
#         dh = int(sdt)
#         sdt = 60*(sdt - dh)
#         dm = int(sdt)
#         sdt = 60*(sdt - dm)
#         ds = int(sdt)        
        udt += timedelta(seconds = int(dt*24*60*60)) 
        return True
          
