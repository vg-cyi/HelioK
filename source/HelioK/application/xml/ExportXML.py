from lxml import etree as ET

from ..Application import *


class ExportXML:
    # export project to xml-file
    degrees: bool # unit for degrees

    def __init__(self):
        # settings
        self.unitLength = "m"
        self.unitAngle = "deg" # or "rad"
        self.app = None

    def write(self, app, filename: str = "scene.xml"):
        # export
        self.app = app
        self.factory = Factory()
        # header        
        xmlParent = ET.Element('HelioK')
        xmlParent.set('version', '2020.2')
        xmlParent.set('unitLength', self.unitLength)
        xmlParent.set('unitAngle', self.unitAngle)

        # main
        self.writeWorld(xmlParent, app.world)
        self.writeFactory(xmlParent, app.factory)
        xmlScene = ET.SubElement(xmlParent, 'Scene')
        for n in app.scene.nodes:
            self.writeNode(xmlScene, n)

        # print
        if ET.LXML_VERSION >= (4, 5):
            ET.indent(xmlParent, space="\t")
        xmlString = ET.tostring(xmlParent, xml_declaration=True, encoding='UTF-8')

        with open(filename, "wb") as f:
            f.write(xmlString)

    def writeWorld(self, xmlParent, world):
        xmlWorld = ET.SubElement(xmlParent, 'World')
        self.writeLocation(xmlWorld, world.location)
        self.writeSun(xmlWorld, world.sun)

    def writeLocation(self, xmlParent, location):
        xmlLocation = ET.SubElement(xmlParent, 'Location')
        xmlLocation.set('name', location.name)
        xmlLocation.set('longitude', self.writeAngle(location.longitude))
        xmlLocation.set('latitude', self.writeAngle(location.latitude))

    def writeSun(self, xmlParent, sun):
        xmlSun = ET.SubElement(xmlParent, 'Sun')
        (gamma, alpha) = sun.motion.findAE()
        xmlSun.set('azimuth', self.writeAngle(gamma))
        xmlSun.set('elevation', self.writeAngle(alpha))
        xmlSun.set('irradiance', self.floatString(sun.irradiance))

        xmlSunShape = ET.SubElement(xmlSun, type(sun.shape).__name__)
        if isinstance(sun.shape, SunShapeBuieRational):
            xmlSun.set('csr', self.floatString(sun.shape.csr))

    def writeFactory(self, xmlParent, factory):
        xmlFactory = ET.SubElement(xmlParent, 'Factory')
        for material in factory.materials.values():
            self.writeMaterial(xmlFactory, material)
        for model in factory.heliostats.values():
            xmlModel = ET.SubElement(xmlFactory, 'HeliostatKit')
            xmlModel.set('name', model.name)
            xmlPrimary = ET.SubElement(xmlModel, 'Primary')
            self.writeHeliostatDrive(xmlPrimary, model.primary)
            xmlSecondary = ET.SubElement(xmlModel, 'Secondary')
            self.writeHeliostatDrive(xmlSecondary, model.secondary)
            for f in model.facets:
                self.writeHeliostatFacet(xmlModel, f)
            xmlAngles = ET.SubElement(xmlModel, 'Angles')
            xmlAngles.set('primary', self.writeAngle(model.angles[0]))
            xmlAngles.set('secondary', self.writeAngle(model.angles[1]))
            xmlTracking = ET.SubElement(xmlModel, 'Tracking')
            xmlTracking.set('point', self.vectorString(model.tracking.point))
            xmlTracking.set('normal', self.vectorString(model.tracking.normal))
            xmlAiming = ET.SubElement(xmlModel, 'Aiming')
            xmlAiming.set('point', self.vectorString(model.aiming.point))

    def writeHeliostatDrive(self, xmlParent, drive):
        xmlParent.set('translation', self.vectorString(drive.translation))
        xmlParent.set('rotationAxis', self.vectorString(drive.rotationAxis))
        a = drive.rotationAngles.a
        b = drive.rotationAngles.b
        xmlParent.set('rotationAngles', self.writeAngle(a) + ', ' + self.writeAngle(b))

    def writeHeliostatFacet(self, xmlParent, facet):
        xmlFacet = ET.SubElement(xmlParent, 'Facet')
        self.makeTransform(xmlFacet, facet.transform)
        self.writeShapeKit(xmlFacet, facet.shapeKit)

    def writeShapeKit(self, xmlParent, shapeKit):
        xmlShapeKit = ET.SubElement(xmlParent, 'ShapeKit')

        s = shapeKit.shape
        #xmlShape = ET.SubElement(xmlShapeKit, type(s).__name__)
        if isinstance(s, ShapeParametric):
            xmlFunctions = ET.SubElement(xmlShapeKit, type(s.functions).__name__)
            if isinstance(s.functions, ShapeParabolic):
                xmlFunctions.set('focus', self.floatString(s.functions.f))

            xmlAperture = ET.SubElement(xmlShapeKit, type(s.aperture).__name__)
            if isinstance(s.aperture, ApertureRectangular):
                if s.aperture.isCentered():
                    xmlAperture.set('xWidth', self.floatString(s.aperture.X.length()))
                    xmlAperture.set('yWidth', self.floatString(s.aperture.Y.length()))
                else:
                    xmlAperture.set('x', self.intervalString(s.aperture.X.a, s.aperture.X.b))
                    xmlAperture.set('y', self.intervalString(s.aperture.Y.a, s.aperture.Y.b))

        self.writeMaterial(xmlShapeKit, shapeKit.material)

    def writeMaterial(self, xmlParent, material):
        xmlMaterial = ET.SubElement(xmlParent, 'Material')
        if material.name in self.factory.materials:
            xmlMaterial.set("ref", material.name)
        elif material.name:
            xmlMaterial.set('name', material.name)
            xmlMaterial.set('reflectivity', self.floatString(material.reflectivity))
            xmlMaterial.set('roughness', self.writeAngle(material.roughness, 'mrad'))
            self.factory.addMaterial(material)

    def writeNode(self, xmlParent, node):
        # node
        xmlNode = ET.SubElement(xmlParent, 'Node')
        xmlNode.set('name', node.name)
        self.makeTransform(xmlNode, node.transform)

        # kits
        skip = False
        for c in node.kits:
            if isinstance(c, HeliostatKit):
                xmlKit = ET.SubElement(xmlNode, type(c).__name__)
                skip = True
                xmlKit.set('ref', c.model.name)
                # xmlKit.set('target', self.vectorString(c.aiming.point))
                # if c.aiming.relative: xmlKit.set('relative', True)
            elif isinstance(c, ShapeKit):
                self.writeShapeKit(xmlNode, c)
            else:
                xmlKit = ET.SubElement(xmlNode, type(c).__name__)

        # subnodes
        if skip: return
        for n in node.nodes:
            self.writeNode(xmlNode, n)

    def makeTransform(self, xmlParent, transform):
        p = transform.translation
        if p.length_squared > 0.:
            xmlParent.set('translation', self.vectorString(p))

        p = mu.Vector(transform.to_euler())
        if p.length_squared > 0.:
            if self.unitAngle == 'deg': p /= degree
            xmlParent.set('rotation', self.vectorString(p))

    def floatString(self, f, eps=1e-6):
        x = f if mt.fabs(f) > eps else 0.
        return '{:.3f}'.format(x)

    def intervalString(self, a, b):
        return '{:}, {:}'.format(
        self.floatString(a), self.floatString(b)
        )

    def vectorString(self, v):
        return '{:}, {:}, {:}'.format(
            self.floatString(v.x), self.floatString(v.y), self.floatString(v.z)
        )

    def writeAngle(self, value, unitName=''):
        if unitName == '':
            unitName = self.unitAngle

        if unitName == 'deg':
            unit = degree
        elif unitName == 'rad':
            unit = 1.
        elif unitName == 'mrad':
            unit = 0.001

        if unit != 1.:
            value /= unit

        ans = '{:.3f}'.format(value)
        if unitName == self.unitAngle:
            return ans
        return ans + ' ' + unitName
