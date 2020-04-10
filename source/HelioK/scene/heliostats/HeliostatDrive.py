from HelioK.common.Interval import *



class HeliostatDrive:
    """
    HeliostatDrive describes a heliostat drive for rotation around fixed axis
    """
    # translation # the position of pivot (in parent frame)
    # rotationAxis # the direction of rotation axis (in parent frame)
    # rotationAngles # the interval of trackable angles
    
    def __init__(self,
                 translation = [0., 0., 0.],
                 rotationAxis = [1., 0., 0.],
                 rotationAngles = [-90.*degree, 90.*degree]
                ):
        self.translation = mu.Vector(translation)
        self.rotationAxis = mu.Vector(rotationAxis).normalized()
        self.rotationAngles = IntervalAngular(rotationAngles)

    def getTransform(self, angle):
        # get transform for angle
        transform = mu.Matrix.Rotation(angle, 4, self.rotationAxis)
        transform.translation = self.translation
        return transform
