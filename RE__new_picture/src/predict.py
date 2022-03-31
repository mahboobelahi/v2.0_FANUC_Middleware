import numpy as np
from funciones import *
import imageReference as ref
import base64

#Version 20220208001

# Input:
# {
#      "RequestId":  unique_identifier
#      "Picture": Image_encoded_as_String (UTF-8)
# }
# Output:
# {
#      "RequestId":  unique_identifier
#      "xy": [x_coordinate_in_pixels, y_coordinate_in_pixels]
# }

# https://www.codegrepper.com/code-examples/javascript/python+base64+string+json
# https://www.youtube.com/watch?v=dW-b5S7cOTw

def predict (**input):

    try:

    #Parameters
        imgSize_i = 480
        imgSize_j = 640
        tt = 102 #Thresholding Threshold 
        erosionR = 7
        minMass = 100 #Masa media durante pruebas: 170-250 pxls 
        maxMass = 320
        thHoles = 153
        #Data feeding
        id = ""
 
        messageIdentifier = input['RequestId']
        rawStrImg = input ['Picture']
        
        decodedImg = base64.standard_b64decode(rawStrImg)
        arrayImg= np.frombuffer(decodedImg,np.uint8)
    
        receivedImg = getImgFrom1DArray (arrayImg, 640)
        
        #Image analysis
            
            #Background
        ImgVoidTable = ref.referenceImagen()
        substractedImg = npImgResta(receivedImg, ImgVoidTable)
        backgroundImg = bindingHoles (substractedImg, 17)
        
        # #----------------------------------------
        # import cv2 as cv
        
        # cv.imshow("resta", substractedImg)
    
        # #----------------------------------------
        
        erodedImg = UmbralizadoYErosion(backgroundImg, tt, erosionR)
        ImgSegmented, numReg = segmentacion(erodedImg)
        
        #     #----------------------------------------
        # cv.imshow("segmented", ImgSegmented)
        # cv.waitKey(0)
        # #----------------------------------------
        
        
        if numReg == 0:
            output = crearMensajeError("0 regions found in segmentation", messageIdentifier)
            return output
        
        #Region analysis
        masas, centres_x, centres_y = CalcularMasasYCentros(ImgSegmented, numReg)
        def chekMasas (masas, i):
            return masas[i]>maxMass and masas[i]<minMass
        i=1
        while i < len(masas) and chekMasas (masas, i):
            i += 1
        if (i>=len(masas)):
            output = crearMensajeError("No valid region found (criterio masa). Mass found: %d"%len(masas)-1,messageIdentifier)
            return output
        regInteres = i
        
        output = '{"RequestId":"%s", "xy":[%.2f,%.2f] }'%(messageIdentifier,centres_x[i],centres_y[i] )
        return output
    except:
        return crearMensajeError("An unnidentified exception was throught on AI prediction model" , "????")
