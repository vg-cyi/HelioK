from lxml import etree as ET


from ..Application import *



class ImportXML:
    # import project from xml-file
    
    def __init__(self):
        pass
            
    def read(self, app, filename = "scene.xml"): 
#         self.app = Application()
        self.app = app

        with open(filename, 'rt') as f:
            tree = ET.parse(f)
            xmlRoot = tree.getroot()

        if xmlRoot.attrib['unitAngle'] == 'deg':   
            self.unitAngle = degree
        else:
            self.unitAngle = 1.
        
        for xmlElement in xmlRoot:
            if xmlElement.tag == "World":
                self.readWorld(xmlElement) 
            elif xmlElement.tag == "Factory":
                self.readFactory(xmlElement)
            elif xmlElement.tag == "Scene":
                self.readScene(xmlElement)
            else:
                print(xmlElement.tag)
                
        return self.app
    
    
    
    def readWorld(self, xmlWorld):
        # read "World"
        for xmlElement in xmlWorld:
            if xmlElement.tag == "Location":
                self.readLocation(xmlElement)
            elif xmlElement.tag == "Sun":
                self.readSun(xmlElement)   
            else:
                print(xmlElement.tag)
       
    def readLocation(self, xmlLocation):
        location = self.app.world.location
        longitude = float(xmlLocation.attrib['longitude'])*self.unitAngle
        latitude = float(xmlLocation.attrib['latitude'])*self.unitAngle
        location.setCoordinates(longitude, latitude)
        location.setName(xmlLocation.attrib['name'])
                
    def readSun(self, xmlSun):
        sun = self.app.world.sun                
        azimuth = float(xmlSun.attrib['azimuth'])*self.unitAngle
        elevation = float(xmlSun.attrib['elevation'])*self.unitAngle                
        sun.motion.setAE(azimuth, elevation) 
        for xmlElement in xmlSun:
            if xmlElement.tag == "SunShapePillbox":
                sun.shape = SunShapePillbox()  
            elif xmlElement.tag == "SunShapeGaussian":
                sun.shape = SunShapeGaussian()    
            elif xmlElement.tag == "SunShapeLimbDarkened":
                sun.shape = SunShapeLimbDarkened()    
            elif xmlElement.tag == "SunShapeBuieRational":
                sun.shape = SunShapeBuieRational()  
            else:
                print(xmlElement.tag)                        
        sun.irradiance = float(xmlSun.attrib['irradiance']) 

    
    def readFactory(self, xmlFactory):
        for xmlElement in xmlFactory:
            if xmlElement.tag == "HeliostatKit":
                self.readHeliostatKit(xmlElement)
            elif xmlElement.tag == "Material":
                self.readMaterial(xmlElement)
            else:
                print(xmlElement.tag)  

    def readMaterial(self, xmlMaterial):
        name = xmlMaterial.attrib['name']
        if name:
            reflectivity = float(xmlMaterial.attrib['reflectivity'])
            roughness = self.readValueUnit(xmlMaterial.attrib['roughness'])
            material = MaterialSpecular(name, reflectivity, roughness)
            self.app.factory.addMaterial(material)

    def readHeliostatKit(self, xmlHeliostat):
        facets = []
        for xmlElement in xmlHeliostat:
            if xmlElement.tag == "Primary":
                primary = self.readHeliostatDrive(xmlElement)  
            elif xmlElement.tag == "Secondary":
                secondary = self.readHeliostatDrive(xmlElement)  
            elif xmlElement.tag == "Tracking":
                tracking = Vertex(
                    self.readVector(xmlElement.attrib['point']),
                    self.readVector(xmlElement.attrib['normal']),
                )
            elif xmlElement.tag == "Facet":
                facet = self.readHeliostatFacet(xmlElement)
                facets.append(facet)
            elif xmlElement.tag == "Angles":
                alpha = self.readValueUnit(xmlElement.attrib['primary'])
                beta = self.readValueUnit(xmlElement.attrib['secondary'])
            elif xmlElement.tag == "Aiming":
                target = self.readVector(xmlElement.attrib['point'])
            else:
                print(xmlElement.tag)                  
                
        heliostatModel = HeliostatModel(
            xmlHeliostat.attrib['name'],
            primary,
            secondary,
            tracking,
            facets,
            (alpha, beta),
            HeliostatAiming(target, False)
        )
        self.app.factory.addHeliostat(heliostatModel)
    
    def readHeliostatDrive(self, xmlDrive):
        rotationAngles = self.readInterval(xmlDrive.attrib['rotationAngles'])
        rotationAngles = [q*self.unitAngle for q in rotationAngles]
        return HeliostatDrive(
            self.readVector(xmlDrive.attrib['translation']),
            self.readVector(xmlDrive.attrib['rotationAxis']), 
            rotationAngles
        )
        
    def readHeliostatFacet(self, xmlFacet):
        transform = self.readTransform(xmlFacet)
        for xmlElement in xmlFacet:
            if xmlElement.tag == "ShapeKit":
                shapeKit = self.readShapeKit(xmlElement)
            else:
                print(xmlElement.tag) 
        return HeliostatFacet(transform, shapeKit)
    
    def readShapeKit(self, xmlShapeKit):
        for xmlElement in xmlShapeKit:
            if xmlElement.tag == "ShapeParabolic":
                focus = float(xmlElement.attrib['focus'])
                func = ShapeParabolic(focus)
            elif xmlElement.tag == "ShapeFlat":
                func = ShapeFlat()
            elif xmlElement.tag == "ApertureRectangular":
                xWidth = float(xmlElement.attrib['xWidth'])
                yWidth = float(xmlElement.attrib['yWidth'])
                aperture = ApertureRectangular.sides(xWidth, yWidth)
            elif xmlElement.tag == "Material":
                ref = xmlElement.attrib['ref']
                material = self.app.factory.materials[ref]
            else:
                print(xmlElement.tag)
        if func:
            shape = ShapeParametric(func, aperture)
        return ShapeKit(shape, material)
    
    # def readShapeParametric(self, xmlShapeParametric):
    #     for xmlElement in xmlShapeParametric:
    #         if xmlElement.tag == "ShapeParabolic":
    #             focus = float(xmlElement.attrib['focus'])
    #             func = ShapeParabolic(focus)
    #         elif xmlElement.tag == "ShapeFlat":
    #             func = ShapeFlat()
    #         elif xmlElement.tag == "ApertureRectangular":
    #             xWidth = float(xmlElement.attrib['xWidth'])
    #             yWidth = float(xmlElement.attrib['yWidth'])
    #             aperture = ApertureRectangular.sides(xWidth, yWidth)
    #         else:
    #             print(xmlElement.tag)
    #     return ShapeParametric(func, aperture)
    
    def readScene(self, xmlScene):
        # read "Scene"   
        parent = self.app.scene
        self.readNode(parent, xmlScene)
        
    def readNode(self, node, xmlNode):
        for xmlElement in xmlNode:
            if xmlElement.tag == 'Node':
                name = xmlElement.attrib['name']
                subnode = node.addNode(name)
                subnode.transform = self.readTransform(xmlElement)
                self.readNode(subnode, xmlElement)
            elif xmlElement.tag == 'HeliostatKit':
                model = xmlElement.attrib['ref']
                heliostatModel = self.app.factory.heliostats[model]
                heliostat = node.addKit(HeliostatKit())
                heliostat.setModel(heliostatModel)  
                # t = self.readVector(xmlElement.attrib['target'])
                # aiming = HeliostatAiming(t)
                # heliostat.setAiming(aiming)
            elif xmlElement.tag == 'ShapeKit':
                shapeKit = self.readShapeKit(xmlElement)
                node.addKit(shapeKit)
            else:
                print(xmlElement.tag)  
    
    
    
    def readTransform(self, xmlNode):
        if 'translation' in xmlNode.attrib:
            translation = self.readVector(xmlNode.attrib['translation'])
        else:
            translation = mu.Vector([0., 0., 0.])
            
        if 'rotation' in xmlNode.attrib:
            rotation = self.readVector(xmlNode.attrib['rotation'])
            rotation *= self.unitAngle
        else:
            rotation = mu.Vector([0., 0., 0.])  
            
        transform = mu.Euler(rotation).to_matrix().to_4x4()
        transform.translation = translation 
        return transform            
    
    def readVector(self, s):
        vs = s.split(',')
        v = [float(q) for q in vs]
        return mu.Vector((v[0], v[1], v[2]))
        
    def readInterval(self, s):
        vs = s.split(',')
        v = [float(q) for q in vs]
        return v  
    
    def readValueUnit(self, text, unitDefault=1.):
        pos = text.find(' ')
        value = float(text[:pos])
        if pos > 0:
            unitName = text[pos + 1:]
            if unitName == 'deg': unit = degree
            elif unitName == 'rad': unit = 1.
            elif unitName == 'mrad': unit = 0.001
            else: print(unitName)
        else:
            unit = unitDefault
        
        return value*unit