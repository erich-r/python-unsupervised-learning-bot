#per modificare la schermata in input presa dal gioco
import cv2
#per prendere la schermata dal gioco
from PIL import ImageGrab
#per trasformare l'immagine in un array
import numpy as np
#per visualizzare i frame
import time

import json


import key_controller as key

import Species as s

from scipy import misc

import utils

import conv_model as cm


#def processImg(imgToProcess):
#    processedImg = cv2.cvtColor(imgToProcess,cv2.COLOR_RGB2GRAY)
#    return processedImg

model = cm.getModel()

#cm.trainModel(model,
#              'C:/Users/Erich/Documents/Giovani Ricercatori/dataTrex/validation',
#              'C:/Users/Erich/Documents/Giovani Ricercatori/dataTrex/training',
#              'C:/Users/Erich/Documents/Tensorboard/GiovaniRicercatori/7',
#              'C:/Users/Erich/Documents/Giovani Ricercatori/weights/pesi_trex.h5')

#cm.loadWeights(model,'C:/Users/Erich/Documents/Giovani Ricercatori/weights/pesi_trex.h5')

X = 12
Y = 10

#IA param
macsGenomes = 50
currentGenome = 0
currentIteration = 0
fitness = 0
 
#IA Init
specie = s.Species(macsGenomes,-1,12,3,[40,5,2])

batch_size = 32

totalGenomes = 0

cm.loadWeights(model,'C:/Users/Erich/Documents/Giovani Ricercatori/weights/pesi_finale.h5') 


isGameOver = True
ultimoFrame = time.time()
while(True):
    screen = ImageGrab.grab(bbox=(59,129,800,600))
    screen = misc.imresize(screen,(60,80))
    screen = np.array(screen)
    screen = utils.swapArray(screen)
    #print(screen)
    #cv2.imshow('eiiii',screen)
    np.moveaxis(screen,0,-1).shape
    screen = np.expand_dims(screen,axis=0)
    #print(model.predict(screen,batch_size=batch_size)[0][0])
    if(cm.predictInput(model,screen)[0][0] < 0.5):
        fitness = 0
        key.PressKey(0x39)
        key.ReleaseKey(0x39)
        #print("HOPERSOOOOOO")
        if(not isGameOver):
            isGameOver = True
            specie.setFitness(currentGenome,fitness)
            specie.nextGeneration()
            if(currentGenome >= macsGenomes - 1):
                currentGenome = 0
            else:
                currentGenome = currentGenome + 1
                totalGenomes = totalGenomes + 1

    else:
        isGameOver = False
        #print(specie.toString())
        specie.feedGenome(currentGenome,utils.genInput(X,Y,screen))                 
        output = specie.getOutputs(currentGenome)
        #print(currentGenome)
        #print(specie.toString())


        if(output[0] > 0.5):
            #key.PressKey(0xC8) #up
            key.PressKey(0xCB) #left
            #key.ReleaseKey(0xCB)
        else:
            key.ReleaseKey(0xCB)
            #key.ReleaseKey(0xC8) #u     p

        if(output[1] > 0.5):
            #key.PressKey(0xD0) #down
            key.PressKey(0xCD) #right
            #key.ReleaseKey(0xCD)
        else:
            key.ReleaseKey(0xCD)
            #key.ReleaseKey(0xD0) #up

        fitness = fitness + 1
    #print(time.time()-ultimoFrame)
    ultimoFrame = time.time()

    if(totalGenomes == 6000):
        utils.saveWeights(specie,0,'C:/Users/Erich/Documents/Giovani Ricercatori/pesiNN/pesi.json')
        break;
    