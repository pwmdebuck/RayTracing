#Scene class
#camera, canvas, objects, lighting

import numpy as np
import matplotlib.pyplot as plt
from Object import Object,Sphere,Plane
from Light import Light
from multiprocessing import Pool
from itertools import repeat

white = np.array([1,1,1])
black = np.array([0,0,0])

def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)




class Scene:
    def __init__(self,cameraPos,screenPos,screenSize,screenRes,lightColor=white):
        self.cameraPos = cameraPos
        self.screenPos = screenPos
        self.screenSize = screenSize
        self.screenRes = screenRes
        self.lightColor = lightColor
        self.bounceLimit = 4

        self.pixelColors = np.zeros((screenRes[0],screenRes[1],3))

        self.cameraDir = screenPos-cameraPos
        #assume screen is on x-y plane
        self.screenBounds = np.array([-screenSize[0]/2,screenSize[0]/2,screenSize[1]/2,-screenSize[1]/2]) #x_left,x_right,y_top,y_bottom

        #compute grid of pixel x/y positions
        x = np.linspace(self.screenBounds[0],self.screenBounds[1],screenRes[0]+1)
        y = np.linspace(self.screenBounds[2],self.screenBounds[3],screenRes[1]+1)
        self.pixel_xx,self.pixel_yy = np.meshgrid(x,y,sparse=True)

        #compute grid of pixel centers
        dx = screenSize[0]/screenRes[0]
        dy = screenSize[1]/screenRes[1]
        x = np.arange(self.screenBounds[0]+dx/2,self.screenBounds[1],dx)
        y = np.arange(self.screenBounds[2]-dy/2,self.screenBounds[3],-dy)
       
        self.pixelCenter_xx,self.pixelCenter_yy = np.meshgrid(x,y,sparse=True)

        #compute directions of the rays from camera to scene
        self.rays = np.zeros((screenRes[0],screenRes[1],2))

        #object storage
        self.objects = []

        #light storage
        self.lights = []

    def plotGrid(self):
        plt.figure()
        plt.plot(self.pixel_xx,self.pixel_yy,'ko',markersize=1)
        plt.plot(self.pixelCenter_xx,self.pixelCenter_yy,'ro',markersize=1)
        plt.grid()

    def getNearestIntersectingObject(self,rayOrigin,rayDirection):
        #check if the ray collided with any objects
        nearestObjectDist = np.inf
        nearestObject = None
        for k in range(len(self.objects)):
            obj = self.objects[k]
            d = obj.intersect(rayOrigin,rayDirection)

            if d is not None and d<nearestObjectDist:
                nearestObjectDist = d
                nearestObject = obj
                #return nearestObjectDist,nearestObject

        return nearestObjectDist,nearestObject

    def renderMulti(self):
        #black canvas
        self.pixelColors = np.zeros((self.screenRes[0],self.screenRes[1],3))

        #compute directions of the rays from camera to scene
        #self.rays = np.zeros((screenRes[0],screenRes[1],2))
        index = 0
        maxIndex = self.screenRes[0]*self.screenRes[1]
        indexVector = np.arange(0,maxIndex)
        p = Pool(16)
        out = p.starmap(Scene.getPixelColor,zip(repeat(self),indexVector))
        p.close()
        p.join()
        
        for index in range(len(out)):
            i = index%self.screenRes[0]
            j = np.floor_divide(index,self.screenRes[0])
            self.pixelColors[i,j,:] = out[index]

        # plt.figure()
        # plt.imshow(self.pixelColors)
        return self.pixelColors

    def renderSingle(self,lightPos,index):
        print(lightPos,index)
        fig = plt.figure(figsize=(8,8))
        self.lights[0].center = lightPos
        #black canvas
        self.pixelColors = np.zeros((self.screenRes[0],self.screenRes[1],3))

        #compute directions of the rays from camera to scene
        #self.rays = np.zeros((screenRes[0],screenRes[1],2))
        
        for i in range(self.screenRes[0]):
            for j in range(self.screenRes[1]):
                self.pixelColors[i,j,:] = self.getPixelColor(j*self.screenRes[0]+i)

        # plt.figure()
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        plt.imshow(self.pixelColors)
        #plt.tight_layout()
        plt.savefig(str(index)+'.png',dpi=800)
        return self.pixelColors
    

                
    def getPixelColor(self,index):
        #get pixel center location
        i = index%self.screenRes[0]
        j = np.floor_divide(index,self.screenRes[0])

        color = np.zeros(3)

        px = self.pixelCenter_xx[0][i]
        py = self.pixelCenter_yy[j][0]
        pixelCenter = np.array([px,py,self.screenPos[2]])

        #compute direction of the ray from camera to scene
        rayDirection = normalized(pixelCenter-self.cameraPos)[0]

        #check if the ray collided with any objects
        startPoint = self.cameraPos

        reflection = 1

        for k in range(self.bounceLimit):
            nearestObjectDist,nearestObject =  self.getNearestIntersectingObject(startPoint,rayDirection)

            if nearestObject is not None:
                for l in range(len(self.lights)):
                    light = self.lights[l]
                    interSectionPoint = startPoint+nearestObjectDist*rayDirection

                    #offset intersectionpoint from surface slightly
                    normal = normalized(interSectionPoint-nearestObject.center)[0]
                    interSectionPoint = interSectionPoint + 1e-5*normal

                    #check if there are any objects in between the bounce point and the light
                    interSectionToLightVector = light.center-interSectionPoint
                    bounceDirection = normalized(interSectionToLightVector)[0]

                    #print(i,j,interSectionPoint,bounceDirection)

                    nearestBounceObjectDist,_ = self.getNearestIntersectingObject(interSectionPoint,bounceDirection)
                    bounceToLightDist = np.linalg.norm(interSectionToLightVector)

                    #if there is an object in between we are in shade
                    #the pixel is already black so we dont do anything

                    #if there is no object, the pixel will be the color of the object
                    # print(nearestBounceObjectDist,)
                    if nearestBounceObjectDist > bounceToLightDist:
                        #self.pixelColors[i,j,:] = nearestObject.diffuseColor

                        L = bounceDirection
                        N = normal
                        V = -rayDirection

                        illumination = np.zeros(3)
                        
                        illumination += nearestObject.ambientColor*light.ambientColor
                        illumination += nearestObject.diffuseColor*light.diffuseColor*np.dot(L,N)
                        temp = normalized(L+V)[0]
                        illumination += nearestObject.specularColor*light.specularColor*(np.dot(N,temp)**(nearestObject.shinyness/4))
                        illumination = np.clip(illumination,0,1)
                        # print(color)
                        # self.pixelColors[i,j,:] = color
                        
                        color += reflection*illumination
                        reflection = reflection*nearestObject.reflection
                        if reflection<=0.01:
                            return np.clip(color,0,1)

                        startPoint = interSectionPoint
                        rayDirection = self.reflection(rayDirection,normal)
            else:
                return np.clip(color,0,1)
        return np.clip(color,0,1)

    def reflection(self,rayDirection,normal):
        return rayDirection - 2 *np.dot(rayDirection, normal)*normal
    
    def addSphere(self,center,radius,**kwargs):
        self.objects.append(Sphere(center,radius,**kwargs))

    def addPlane(self,center,normal,**kwargs):
        self.objects.append(Plane(center,normal,**kwargs))

    def addLight(self,center,**kwargs):
        self.lights.append(Light(center,**kwargs))

    def sortObjectsByDistance(self):
        for obj in self.objects:
            obj.minDistFromCamera = np.linalg.norm(obj.center-self.cameraPos)-obj.radius

        self.objects.sort(key=lambda x: x.minDistFromCamera)

