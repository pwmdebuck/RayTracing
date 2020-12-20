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
    def __init__(self,center,radius,ambientColor,diffuseColor,specularColor,shinyness,reflection):
        super().__init__(center,'sphere',ambientColor,diffuseColor,specularColor,shinyness,reflection)
        self.radius = radius

    def intersect(self,rayOrigin,rayDirection):
        OminC = rayOrigin-self.center
        b = 2*np.dot(rayDirection,OminC)
        c = np.linalg.norm(OminC)**2 - self.radius**2
        delta = b**2-4*c
        sqrtdelta = np.sqrt(delta)
        if delta>0:
            d1 = 0.5*(-b+sqrtdelta)
            d2 = 0.5*(-b-sqrtdelta)
            if d1 > 0 and d2 > 0:
                return np.minimum(d1,d2)
        return None

class Plane(Object):
    def __init__(self,center,normal,ambientColor=fadedred,diffuseColor=red,specularColor=white,shinyness=0.0,reflection=0.0)):
        super().__init__(center,ambientColor,diffuseColor,specularColor,shinyness,reflection)
        self.radius = radius

    def intersect(self,rayOrigin,rayDirection):
        OminC = rayOrigin-self.center
        b = 2*np.dot(rayDirection,OminC)
        c = np.linalg.norm(OminC)**2 - self.radius**2
        delta = b**2-4*c
        sqrtdelta = np.sqrt(delta)
        if delta>0:
            d1 = 0.5*(-b+sqrtdelta)
            d2 = 0.5*(-b-sqrtdelta)
            if d1 > 0 and d2 > 0:
                return np.minimum(d1,d2)
        return None
