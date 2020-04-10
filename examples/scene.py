app = hk.Application()

# World
location = app.world.location
location.setCoordinates(longitude = 33.261*hk.degree, latitude = 34.707*hk.degree)
location.setName("Pentakomo")

sun = app.world.sun
sun.motion.setAE(azimuth = 120.*hk.degree, elevation = 45.*hk.degree)
sun.shape = hk.SunShapePillbox()
sun.irradiance = 1000.
    

# Factory
factory = app.factory

material = hk.MaterialSpecular(name = "mirror", reflectivity = 1., roughness = 0.001)
factory.addMaterial(material)

material = hk.MaterialSpecular(name = "absorber", reflectivity = 0., roughness = 0.001)
factory.addMaterial(material)

facet = hk.HeliostatFacet(
    hk.makeTransform([0., 0., 0.], hk.rotationWZN),
    hk.ShapeKit(
        hk.ShapeParametric(hk.ShapeParabolic(focus = 70.), hk.ApertureRectangular.sides(xWidth = 2., yWidth = 2.)),
        factory.materials["mirror"]
    )
)

heliostatAzEl = hk.HeliostatModel(
    name = "AzEl",
    primary = hk.HeliostatDrive(
        translation = [0., 0., 1.5], rotationAxis = [0., 0., -1.], rotationAngles = [-90.*hk.degree, 90.*hk.degree] 
    ),
    secondary = hk.HeliostatDrive(
        translation = [0., 0.1, 0.], rotationAxis = [1., 0., 0.], rotationAngles = [0.*hk.degree, 90.*hk.degree]
    ),
    tracking = facet.getVertex(),
    facets = [facet],
    angles = (0.*hk.degree, 0.*hk.degree),
    aiming = hk.HeliostatAiming([0., 0., 20.], False)
)
factory.addHeliostat(heliostatAzEl)  
    

# Scene    
nodeReceiver = app.scene.addNode("Receiver")
nodeReceiver.transform = hk.makeTransform([0., 0., 20.], hk.rotationWZN)
receiver = hk.ShapeKit(
    hk.ShapeParametric(hk.ShapeFlat(), hk.ApertureRectangular.sides(2., 2.)),
    factory.materials["absorber"]
)
nodeReceiver.addKit(receiver)

def makeTransformRadial(position):
    # look at origin
    position = hk.mu.Vector(position)
    azimuth = hk.mt.atan2(-position.x, -position.y) 
    rotation = hk.mu.Matrix.Rotation(-azimuth, 3, 'Z') 
    return hk.makeTransform(position, rotation) 

nodeHeliostats = app.scene.addNode("Heliostats")
heliostatAzEl = app.factory.heliostats['AzEl']

# heliostatA
nodeA = nodeHeliostats.addNode("HeliostatA")
nodeA.transform = makeTransformRadial([30., 50., 0.]) 
heliostatA = nodeA.addKit(hk.HeliostatKit())
heliostatA.setModel(heliostatAzEl)

# heliostatB
nodeB = nodeHeliostats.addNode("HeliostatB") 
nodeB.transform = makeTransformRadial([-30., 50., 0.]) 
heliostatB = nodeB.addKit(hk.HeliostatKit())
heliostatB.setModel(heliostatAzEl)

# aiming
aiming = hk.HeliostatAiming([0., 0., 20.])
heliostatA.setAiming(aiming)
heliostatB.setAiming(aiming)
