from .math import *
import numpy as np


class Interval:
    """
    Interval stores interval x in [a, b]
    """

    def __init__(self, ab=(0., 1.)):
        assert ab[0] < ab[1]
        self.a = ab[0]
        self.b = ab[1]

    @classmethod
    def limits(cls, a, b):
        return cls((a, b))

    def isInside(self, x):
        return self.a <= x <= self.b

    def length(self):
        return self.b - self.a

    def middle(self):
        return (self.b + self.a) / 2.

    def toNormalized(self, x):
        return (x - self.a) / (self.b - self.a)

    def fromNormalized(self, u):
        return (1. - u) * self.a + u * self.b

    def sampleDivisions(self, divisions):
        if divisions <= 1: return [self.a, self.b]
        step = (self.b - self.a) / divisions
        return [self.a + n * step for n in range(divisions + 1)]

    def sampleResolution(self, resolution):
        assert resolution > 0.
        divisions = round((self.b - self.a) / resolution)
        return self.sampleDivisions(divisions)


class IntervalAngular(Interval):
    """
    Interval stores angular interval x in [a, b]
    """

    def __init__(self, ab):
        Interval.__init__(self, ab)

    def normalizeAngle(self, alpha):
        # normalize angle with respect to the lower limit        
        return normalizeAngle(alpha, self.a)


class Interval2D:
    """
    Two intervals
    """

    def __init__(self, X=(0., 1.), Y=(0., 1.)):
        self.X = Interval(X)
        self.Y = Interval(Y)

    @classmethod
    def sides(cls, xWidth, yWidth):
        w = xWidth / 2
        h = yWidth / 2
        return cls((-w, w), (-h, h))

    @classmethod
    def limits(cls, xMin, xMax, yMin, yMax):
        return cls((xMin, xMax), (yMin, yMax))

    def isCentered(self):
        return self.X.a == -self.X.b and self.Y.a == -self.Y.b

    def isInside(self, xy):
        x, y = xy
        return self.X.isInside(x) and self.Y.isInside(y)

    def area(self):
        return self.X.length() * self.Y.length()

    def toNormalized(self, xy):
        x, y = xy
        u = self.X.toNormalized(x)
        v = self.Y.toNormalized(y)
        return mu.Vector([u, v])

    def fromNormalized(self, uv):
        u, v = uv
        x = self.X.fromNormalized(u)
        y = self.Y.fromNormalized(v)
        return mu.Vector([x, y])
