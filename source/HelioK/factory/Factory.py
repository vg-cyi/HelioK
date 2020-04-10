

class Factory:
    # Factory stores heliostat templates
    
    def __init__(self):
        self.heliostats = {}
        self.materials = {}
        
    def addHeliostat(self, model):
        self.heliostats[model.name] = model

    def addMaterial(self, material):
        self.materials[material.name] = material