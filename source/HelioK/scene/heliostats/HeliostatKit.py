from ..Node import *
from .HeliostatModel import *


class HeliostatKit(Kit):
    """
    Heliostat describes a heliostat with two rotational drives
    """
    model: HeliostatModel
    nodePrimary: Node
    nodeSecondary: Node
    #     angles = None # tracking angles (alpha, beta)
    aiming: HeliostatAiming

    def __init__(self):
        Kit.__init__(self)

    def setModel(self, model, createNodes=True):
        self.model = model
        if createNodes:
            self.nodePrimary = Node()
            self.nodeSecondary = Node()
            self.node.nodes = [self.nodePrimary]
            self.nodePrimary.nodes = [self.nodeSecondary]
        else:
            self.nodePrimary = self.node.nodes[0]
            self.nodeSecondary = self.nodePrimary.nodes[0]
        self.setTrackingAnglesList([model.angles])
        self.aiming = model.aiming

    def setTrackingAngles(self, alpha, beta):
        # set tracking angles
        return self.setTrackingAnglesList([(alpha, beta)])

    def setTrackingAnglesList(self, angles):
        # set tracking angles
        # the first valid solution is selected
        # returns True if tracking is possible
        angles = self.model.selectTrackingAngles(angles)
        if not angles: return False
        self.angles = angles[0]
        self.nodePrimary.transform = self.model.primary.getTransform(self.angles[0])
        self.nodeSecondary.transform = self.model.secondary.getTransform(self.angles[1])
        return True

    def printTrackingAngles(self, angles=None):
        # prints angles in degrees
        # by default prints current angles
        if not angles: angles = [self.angles]
        for ab in angles:
            print(self.model.writeTrackingAngles(ab))

    def findTrackingVertex(self):
        # returns tracking vertex
        return self.model.tracking.transformed(self.findTransformFacets())

    def findTrackingPoint(self):
        # returns position of reflector in heliostat frame
        r = self.model.tracking.point
        r = self.nodeSecondary.transform @ r
        r = self.nodePrimary.transform @ r
        return r

    def findTrackingNormal(self):
        # returns normal of reflector in heliostat frame
        n = self.model.tracking.normal
        n = self.nodeSecondary.transform.to_3x3() @ n
        n = self.nodePrimary.transform.to_3x3() @ n
        return n

    def getFacets(self):
        return self.nodeSecondary.nodes

    def findTransformFacets(self):
        # returns mirror transform 
        t = self.nodeSecondary.transform
        t = self.nodePrimary.transform @ t
        return t

    def setTrackingNormal(self, vNormal, debug=False):
        # set mirror normal in heliostat frame
        # returns True if tracking is possible
        n = vNormal
        angles = self.model.solveTrackingNormal(n)
        ans = self.setTrackingAnglesList(angles)
        if debug:
            print("Solutions:")
            self.printTrackingAngles(angles)
            print("Selected:")
            self.printTrackingAngles()
        return ans

    def setAiming(self, aiming):
        # set aiming
        self.aiming = aiming

    def setTrackingSun(self, vSun, debug=False):
        # reflect sun to aiming point
        # vSun (in global frame)
        # returns True if tracking is possible                
        angles = None
        toLocal = self.node.findTransformGlobal().inverted()
        vSunL = toLocal.to_3x3() @ vSun
        rAimL = self.aiming.point
        if self.aiming.relative:
            angles = self.model.solveReflectionRelative(vSunL, rAimL)
        else:
            rAimL = toLocal @ rAimL  # rAimL@self.node.transform
            angles = self.model.solveReflectionAbsolute(vSunL, rAimL, debug)
        ans = self.setTrackingAnglesList(angles)
        if debug:
            print("Selected:")
            self.printTrackingAngles()
        return ans

    def checkAiming(self, vSun):
        # check aiming
        # sunVector (in global frame) to the sun
        # lateral displacement from aiming point in meters 
        tR = self.node.findTransformGlobal() @ self.findTransformFacets()
        vSunR = vSun @ tR.to_3x3()  # to sun
        vTargetR = -vSunR.reflect(self.model.tracking.normal)  # to target
        rAimR = self.aiming.point
        if not self.aiming.relative:
            rAimR = tR.inverted() @ rAimR  # rAimR@tR
        return (rAimR - self.model.tracking.point).cross(vTargetR).length
