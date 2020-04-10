from ..Node import *
from .ShapeParametric import *
from ..materials.Material import *


class ShapeKit(Kit):
    """
    ShapeKit holds shape and material
    """

    # shape
    # material

    def __init__(self, shape=ShapeParametric(), material=MaterialSpecular()):
        self.shape = shape
        self.material = material
