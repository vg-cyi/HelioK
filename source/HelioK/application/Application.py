from ..world.World import *
from ..factory.Factory import *
# from ..scene.Node import *
from ..scene.heliostats.HeliostatKit import *

from .xml.ExportXML import *
from .xml.ImportXML import *


class Application:
    """
    Combines world, factory and scene
    """
    world: World
    factory: Factory
    scene: Node

    def __init__(self):
        self.reset()

    @classmethod
    def file(cls, filename: str, gv=None):
        ext = filename.split(".")[-1]
        if ext == 'xml':
            temp = cls()
            temp.read(filename)
            return temp
        elif ext == 'py':
            with open(filename) as f:
                exec(f.read(), gv)

    def reset(self):
        self.world = World()
        self.factory = Factory()
        self.scene = Node("Scene")

    def updateTracking(self, node=None, debug=False):
        # set sun for node recursively
        if not node: node = self.scene
        self.updateTrackingPrivate(node, self.world.sun.motion.vector, debug)

    def updateTrackingPrivate(self, node, sun, debug):
        h = node.getKit(HeliostatKit)
        if h:
            if debug: print(node.name)
            h.setTrackingSun(sun, debug)
            if debug: print()
            return

        for n in node.nodes:
            self.updateTrackingPrivate(n, sun, debug)

    def write(self, filename):
        w = ExportXML()
        w.write(self, filename)

    def read(self, filename):
        self.reset()
        r = ImportXML()
        r.read(self, filename)
