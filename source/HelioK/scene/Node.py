# from __future__ import annotations 
from HelioK.common.math import *
from .Kit import *
from typing import List



class Node:
    """
    Node for scene
    """
    name : str
    transform : mu.Matrix
    parent : "Node"
    kits : List[Kit] 
    nodes: List["Node"]    
    
    def __init__(self, name : str = "", transform : mu.Matrix = mu.Matrix.Identity(4)):
        self.name = name
        self.transform = transform # from this to parent (transform@r)
        self.parent = None
        self.kits = []
        self.nodes = []
        
    def addKit(self, kit : Kit):
        kit.node = self
        self.kits.append(kit)
        return kit
    
    def getKit(self, instance = None):
        # if not instance and self.kits: return self.kits[0]
        for k in self.kits:
            if isinstance(k, instance): return k
        return None
   
    def addNode(self, name : str = ""):
        node = Node(name)
        node.parent = self
        self.nodes.append(node)
        return node

    def findNode(self, name : str, recursive : bool = True):
        # find node by name recursively
        for n in self.nodes:
            if n.name == name: return n
            if (recursive): 
                nn = n.findNode(name, recursive)
                if nn: return nn
        return None                
            
    def printTree(self, level : int = 0, recursive : bool = True):
        # print tree recursively
        pad = '  '*level
        for k in self.kits:
            print( pad + type(k).__name__ )

        for n in self.nodes:
            if n.name:
                print( pad + n.name )
            else:
                print( pad + '_')
            if (recursive):
                n.printTree(level + 1, recursive)  

    def findTransformGlobal(self):
        # return global transform
        node = self
        transform = node.transform.copy()
        while True:
            node = node.parent
            if not node: return transform
            transform = node.transform@transform                                                                  
        