#main render script

import numpy as np
from Object import Object
from Scene import Scene
import matplotlib.pyplot as plt
from multiprocessing import Pool


cameraPos = np.array([0,0,-1])
screenPos = np.array([0,0,0])
lightPos = np.array([-1,0,2])
Scene = Scene(cameraPos,screenPos,np.array([1,1]),np.array([800,800]))

#add sphere to scene
green = np.array([0,0.9,0])
fadedgreen = np.array([0,0.1,0])
Scene.addSphere(np.array([0,0,3]),0.8,shinyness=100,reflection=1.0)
Scene.addSphere(np.array([0.5,0.5,2]),0.4,shinyness=50,diffuseColor=green,ambientColor=fadedgreen,reflection=1.0)

blue = np.array([0,0,0.9])
fadedblue = np.array([0,0,0.2])
Scene.addSphere(np.array([0.5,-0.5,2]),0.3,shinyness=50,diffuseColor=blue,ambientColor=fadedblue,reflection=1.0)

gray = np.array([0.2,0.2,0.2])
Scene.addPlane(np.array([0.9,0,5]),np.array([1,0,0.4]),shinyness=100,diffuseColor=gray,ambientColor=gray,reflection=0.0)
Scene.addPlane(np.array([0,0,5]),np.array([0,0,1]),shinyness=100,diffuseColor=gray,ambientColor=gray,reflection=0.0)
Scene.addLight(lightPos)

# Scene.sortObjectsByDistance()


lightPositions = Scene.lights[0].spinLight(2,60)
frameNames = np.arange(0,len(lightPositions),1)

#render multiple processes within loop
# for i in range(lightPositions.shape[0]):
#     if __name__ == "__main__":
#         print(i)
#         Scene.lights[0].center = lightPositions[i,:]
#         pixelColors = Scene.renderMulti()
#         plt.imshow(pixelColors)
#         plt.savefig(str(i)+'.png',dpi=800)

#render multiple processes outside loop


if __name__ == "__main__":

        with Pool(8) as p:
            p.starmap(Scene.renderSingle,zip(lightPositions,frameNames))

# if __name__ == "__main__":
#     plt.show()
    