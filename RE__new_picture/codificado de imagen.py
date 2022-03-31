# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 13:37:05 2022

Image encoding with different outputs


@author: cxdso
"""

import cv2 as cv
import numpy as np
import base64 as b64

target = 1  #choose a target

target_txt = 0  #save the string in txt. Use this one
target_py = 1   
target_json = 2     
target_txt_open = 3
target_json_open = 4

encodetarget = 'utf-8'
#encodetarget = 'ascii'


limitePagina = 25

imgDirectory = input("\nImage address:\n")
txtDirectory = input("\nOutput file address:\n")

imagen = cv.imread(imgDirectory, cv.IMREAD_GRAYSCALE)

txtString = ""

if target == target_py:
    txtString = 'import numpy as np\ndef referenceImagen ():\n\treturn np.array(['
    for i in range(len(imagen)):
        txtString += '['
        for j in range(len (imagen[0])):
            txtString += "%d"%imagen[i][j]
            if(j<len (imagen[0])-1):
                txtString += ","
                if((j+1)%limitePagina == 0):
                    txtString += "\n"
        txtString += "]"
        if(i<len (imagen)-1):
            txtString += ","
    
    txtString += '])'
elif target == target_txt:
    txtString += str(b64.standard_b64encode(imagen),encodetarget)
elif target == target_json:
    txtString += '{"RequestId":"007", "Picture":"'
    txtString += str(b64.standard_b64encode(imagen),encodetarget)
    txtString += '"}'
# elif target == target_txt_open :
#     with open(imgDirectory,"rb") as img: 
#         imagen = img.read()
#     bbb=imagen
#     aaa=b64.standard_b64encode(bbb)
#     txtString += str(aaa,encodetarget)
# elif target == target_json_open:
#     with open(imgDirectory,"rb") as img: 
#         imag = img.read()
#     bbb=imag
#     txtString += '{"RequestId":"007", "Picture":"'
#     txtString += str(b64.standard_b64encode(bbb),encodetarget)
#     txtString += '"}'
    
txtFile = open(txtDirectory, "w")
txtFile.write(txtString)
txtFile.close()


# cv.imshow(imgDirectory , imagen)
# cv.waitKey(0)