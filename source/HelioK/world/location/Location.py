from HelioK.common.math import *



class Location:
    """
    Location on Earth
    """
    
    def __init__(self, longitude = 0., latitude = 0., name = ""):        
        self.setCoordinates(longitude, latitude)
        self.setName(name)
        
    def setCoordinates(self, longitude = 0., latitude = 0.):
        # set coordinates in radians       
        assert mt.fabs(longitude) <= mt.pi  
        assert mt.fabs(latitude) <= mt.pi/2      
        self.longitude = longitude
        self.latitude = latitude    
        
    def setName(self, name):
        self.name = name