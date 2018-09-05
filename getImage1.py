#conding=utf-8
from naoqi import ALProxy
import os
import vision_definitions
import cv2
import sys
import random
import numpy as np
from PIL import Image

save_dir = './image/'
IP = "192.168.0.114"
PORT = 9559

#create_dir(save_dir)

try:
    camProxy = ALProxy("ALVideoDevice", IP, PORT)
except Exception, e:
    print("Error when create ALphotoCapture proxy:")
    print(str(e))
    exit(1)
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
def relight(imgsrc, alpha=1, bias=0):
    imgsrc = imgsrc.astype(float)
    imgsrc = imgsrc * alpha + bias
    imgsrc[imgsrc < 0] = 0
    imgsrc[imgsrc > 255] = 255
    imgsrc=imgsrc.astype(np.uint8)
    return imgsrc
f = open('in.txt', 'r')
index = int(f.read())
print(index)
f.close()
while index <= 4000:
    resolution = 1
    colorSpace = 11
    fps = 30
    camProxy.setActiveCamera(1)
    nameId = camProxy.subscribe("python_GVM", resolution, colorSpace, fps)
    naoImage = camProxy.getImageRemote(nameId)
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]

    im = Image.frombytes("RGB", (imageWidth, imageHeight), array)
    im.save(save_dir+"redball"+str(index)+".png", "png")
    im=cv2.imread(save_dir+"redball"+str(index)+".png")
    #im = cv2.cvtColor(im,cv2.COLOR_RGB2GRAY)
    im=relight(im, random.uniform(0.5, 1.5), random.randint(-50, 50))
    cv2.imwrite(save_dir+"redball"+str(index)+".png",im)
    #im.show()
    camProxy.unsubscribe(nameId)
    print(index)
    index += 1

f = open('in.txt','w')
f.write(str(index))
f.close()