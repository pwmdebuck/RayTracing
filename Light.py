#Light class
import numpy as np
white = np.array([1,1,1])

def parametric_circle(t,xc,yc,R):
    x = xc + R*np.cos(t)
    y = yc + R*np.sin(t)
    return x,y

class Light:
    def __init__(self,center,ambientColor=white,diffuseColor=white,specularColor=white):
        self.center = center
        self.ambientColor = ambientColor
        self.diffuseColor = diffuseColor
        self.specularColor = specularColor

    def spinLight(self,radius,number):
        #assuming fixed y position
        center = self.center
        lightPositions = np.zeros((number,3))
        t = np.linspace(0,2*np.pi,number)
        x,y = parametric_circle(t,center[1],center[2],radius)

        lightPositions[:,0] = center[0]
        lightPositions[:,1] = x
        lightPositions[:,2] = y

        return lightPositions
    

