from HelioK.common.math import *


class MaterialSpecular:
    #     albedo = None # Lambertian reflectivity
    #     reflectivity = None # specular reflectivity
    #     roughness = None # surface roughness (sigma slope in radians)

    def __init__(self,
                 name: str = "",
                 reflectivity: float = 1.,
                 roughness: float = 0.001
                 ):
        assert 0. <= reflectivity <= 1.
        assert roughness > 0.
        self.name = name
        self.reflectivity = reflectivity
        self.roughness = roughness
