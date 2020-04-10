from ..SunMotion import *

from datetime import datetime, timedelta


class SunMotionPSA(SunMotion):
    """
    SunMotion based on PSA algorithm 2001
    """
    parallaxCoeff = 6371.01/149597890.
    
    def __init__(self):
        SunMotion.__init(self)
        
    def setTime(self, udt):       
        # elapsed days
        dy = 0 if udt.month > 2 else -1 # start year from March
        jd = (1461*(4800 + udt.year + dy))//4 # leap years 4
        jd -= (3*((4900 + udt.year + dy)//100))//4 # leap years 100 and 400
        jd += (367*(udt.month - 2 - 12*dy))//12 # days since March
        jd += udt.day - 32075 # Julian day number
        hours = udt.hour + (udt.minute + udt.second/60)/60 
        days = jd + hours/24 - 2451545.5 # days since noon 1 January 2000
        
        # ecliptic coordinates
        meanLongitude = 4.8950630 + 0.017202791698*days # from spring equinox, tropical year
        meanAnomaly = 6.2400600 + 0.0172019699*days # from perihelion, orbital year
        omega = 2.1429 - 0.0010394594*days # precession 26000 years 
        eclipticLongitude = meanLongitude + 0.03341607*mt.sin(meanAnomaly) + 0.00034894*mt.sin(2.*meanAnomaly)
        eclipticLongitude -= 0.0001134 + 0.0000203*mt.sin(omega)
        eclipticObliquity = 0.4090928 - 6.2140e-9*days + 0.0000396*mt.cos(omega)
        
        # celestial coordinates
        (rightAscension, declination) = self.findRD(self, eclipticLongitude, eclipticObliquity)
        
        # equatorial coordinates
        GreenwichMeanSiderealTime = 6.6974243242 + 0.0657098283*days + hours # 24/365.24
        localMeanSiderealTime = GreenwichMeanSiderealTime*twopi/24 + self.location.longitude 
        hourAngle = localMeanSiderealTime - rightAscension
        
        # horizontal coordiantes
        self.setHD(hourAngle, declination)
        (azimuth, elevation) = self.findAE()
        # parallax correction
        elevation -= self.parallaxCoeff*mt.cos(elevation)
        self.setAE(azimuth, elevation)
        
    def findAboveT(self, udt, elevation = 0., solution = -1):  
        pass
    
    def findRD(self, eclipticLongitude, eclipticObliquity):
        sinEclipticLongitude = mt.sin(eclipticLongitude)
        y = mt.cos(eclipticObliquity)*sinEclipticLongitude
        x = mt.cos(eclipticLongitude)
        rightAscension = mt.atan2(y, x)
        if rightAscension < 0.: rightAscension += twopi
        declination = mt.asin(sinEclipticLongitude*mt.sin(eclipticObliquity))
        return (rightAscension, declination)