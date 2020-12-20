#main render script

import numpy as np
from Object import Object
from Scene import Scene
import matplotlib.pyplot as plt


cameraPos = np.array([0,0,-1])
screenPos = np.array([0,0,0])
lightPos = np.array([-1,0,2])
Scene = Scene(cameraPos,screenPos,np.array([1,1]),np.array([400,400]))

#add sphere to scene
green = np.array([0,0.9,0])
fadedgreen = np.array([0,0.1,0])
Scene.addObject(np.array([0,0,3]),0.8,shinyness=100)
Scene.addObject(np.array([0.5,0.5,2]),0.4,shinyness=50,diffuseColor=green,ambientColor=fadedgreen)

blue = np.array([0,0,0.9])
fadedblue = np.array([0,0,0.2])
Scene.addObject(np.array([0.5,-0.5,2]),0.3,shinyness=50,diffuseColor=blue,ambientColor=fadedblue)

gray = np.array([0.2,0.2,0.2])
Scene.addObject(np.array([1001,0,0]),1000,shinyness=100,diffuseColor=gray,ambientColor=gray)
Scene.addLight(lightPos)

Scene.sortObjectsByDistance()

lightPositions = Scene.lights[0].spinLight(1,30)
for i in range(lightPositions.shape[0]):
    if __name__ == "__main__":
        print(i)
        Scene.lights[0].center = lightPositions[i,:]
        pixelColors = Scene.render()
        plt.imshow(pixelColors)
        plt.savefig(str(i)+'.png')

#plt.show()