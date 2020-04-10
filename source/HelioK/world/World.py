from .sun.Sun import *



class LocationNode(Location):
    
    def __init__(self, parent):
        self.parent = None
        Location.__init__(self)
        self.parent = parent
        
    def setCoordinates(self, longitude = 0., latitude = 0.):        
        super().setCoordinates(longitude, latitude)
        if self.parent: self.parent.updateLocation()
        
    def sub(self):
        return Location(self.longitude, self.latitude)
        

        
class World:
    """
    World includes sun, location, air
    """
    location = None
    sun = None
        
    def __init__(self):
        self.location = LocationNode(self)
        self.sun = Sun()
    
    def updateLocation(self):
        self.sun.motion.setLocation(self.location.sub()) 
        