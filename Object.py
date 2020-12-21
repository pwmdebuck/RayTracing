#Object class
import numpy as np
red = np.array([1,0,0])
fadedred = np.array([0.2,0,0])
white = np.array([1,1,1])

class Object:
    def __init__(self,center,objectType='sphere',ambientColor=fadedred,diffuseColor=red,specularColor=white,shinyness=0.0,reflection=0.0):
        self.center = center
        self.objectType = objectType
        # self.radius = radius
        self.ambientColor = ambientColor
        self.diffuseColor = diffuseColor
        self.specularColor = specularColor
        self.shinyness = shinyness
        self.reflection = reflection

class Sphere(Object):
    def __init__(self,center,radius,**kwargs):
        super().__init__(center,'sphere',**kwargs)
        self.radius = radius

    def intersect(self,rayOrigin,rayDirection):
        OminC = rayOrigin-self.center
        b = 2*np.dot(rayDirection,OminC)
        c = np.linalg.norm(OminC)**2 - self.radius**2
        delta = b**2-4*c
        if delta>0:
            sqrtdelta = np.sqrt(delta)
            d1 = 0.5*(-b+sqrtdelta)
            d2 = 0.5*(-b-sqrtdelta)
            if d1 > 0 and d2 > 0:
                return np.minimum(d1,d2)
        return None

class Plane(Object):
    def __init__(self,center,normal,**kwargs):
        super().__init__(center,'sphere',**kwargs)
        self.normal = normal

    def intersect(self,rayOrigin,rayDirection):
        denom = np.dot(self.normal,rayDirection)
        if denom > 1e-6:
            CminO = self.center-rayOrigin
            t= np.dot(CminO,self.normal)/denom
            if t>0:
                return t
        return None
