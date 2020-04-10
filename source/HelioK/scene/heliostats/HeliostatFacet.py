from ..materials.Material import *
from ..shapes.ShapeKit import *



class HeliostatFacet:
    """
    HeliostatFacet describes a heliostat mirror
    """
    transform = None # transform from mirror to heliostat frame (parent)

#     shape = None 
#     material = None # reflectivity and roughness (possible front/back material)
    
    def __init__(self,
                 transform = mu.Matrix.Translation([0., 0., 0.]),
                 shapeKit = ShapeKit()
                ):
        self.transform = transform        
        self.shapeKit = shapeKit       
        
    def getVertex(self, uv = (0.5, 0.5)):
        shape = self.shapeKit.shape
        xy = shape.aperture.fromNormalized(uv)
        r = mu.Vector(xy).to_3d()
        ans = Vertex(
            shape.functions.findPoint(r),
            shape.functions.findNormal(r)
        )  
        ans.transform(self.transform)
        return ans
