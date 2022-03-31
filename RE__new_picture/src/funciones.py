# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 10:07:48 2022

@author: cxdso
"""

import numpy as np

def getImgFrom1DArray (array, j_size):
    lenArray = len(array)
    numSegments = int( lenArray / j_size)
    resto = lenArray % j_size
    img = np.zeros((numSegments, j_size),dtype=np.ndarray)
    for i in range(0,numSegments):
        for j in range(j_size):
            img[i][j] = array[i*j_size+j]
    return img


def npImgResta (img1, img2):
    '''Resta img2 a img1 sin overflow'''
    shape=(len(img1), len(img1[0]))
    resta = np.zeros(shape, np.uint8)
    
    for i in range(len(resta)):
        for j in range(len(resta[0])):
            if (img1[i][j] > img2[i][j]):
                sub = img1[i][j] - img2[i][j]
            else:
                sub = 0
            resta[i][j]= sub
    return resta;

def UmbralizadoYErosion(binImg, umbral, radio):
    result = np.copy(binImg)
    for i in range (len(result)):
        for j in range (len(result[0])):
            
            for k in range (-radio, radio+1):
                for w in range  (-radio, radio+1):
                    if i+k>=0 and j+w>=0 and i+k<len(result) and j+w<len(result[0]):
                        if binImg[i+k][j+w] > umbral and result[i][j] > 0:
                            result[i][j] = 255
                        else:
                            result[i][j] = 0
                            break
                    else:
                        result[i][j] = 0    #Si está en el borde lo pongo siempre a 0 para simplificar
                        break
                if result[i][j] == 0:
                    break
    return result



def segmentacion(binImg):
    '''Recibe una imagen (numpy array). Devielve la imagen segmentada (fondo a 0) y el número de regiones encontradas (sin contar el fondo)'''
    imgEtiquetada = np.copy(binImg)
    numRegiones = 0
    for i in range(len(binImg)):
        for j in range(len(binImg[0])):
            if (binImg[i][j] != 0):
                nuevoValor, numRegiones = nuevoValorSegunVecinosArrIzq (imgEtiquetada,i,j,numRegiones)
                if imgEtiquetada[i][j] != nuevoValor:
                    imgEtiquetada[i][j] = nuevoValor

    for i in range(len(binImg)-1, -1, -1 ):
            for j in range(len(binImg[0])-1, -1, -1 ):
                nuevoValor, numRegiones = nuevoValorSegunVecinosAbaDer (imgEtiquetada,i,j,numRegiones)
                if imgEtiquetada[i][j] != nuevoValor:
                    imgEtiquetada[i][j] = nuevoValor

    for i in range(10):
        imgEtiquetada = LimpiarRegiones ( imgEtiquetada)
    
    listaRegiones = ListarRegiones (imgEtiquetada)
    SimplificaRegiones(imgEtiquetada, listaRegiones)

    return np.copy(imgEtiquetada), len(listaRegiones)


def nuevoValorSegunVecinosArrIzq (ImgEt, x, y, numRegiones):
    izq = 0
    arr = 0
    diag = 0
    
    if ImgEt[x][y] == 0:
        return 0, numRegiones
    
    if x-1 >= 0:
        izq = ImgEt[x-1][y]
    else:
        izq = 0
        
    # if x-1 >= 0 and y-1 >= 0:
    #     diag = ImgEt[x-1][y-1]
    # else:
    #     diag = 0    
    
    if y-1 >= 0:
        arr = ImgEt[x][y-1]
    else:
        arr = 0

        
    if arr > 0 :
        return arr, numRegiones
    if izq > 0:
        return izq, numRegiones
    
    # if arr == 255 or izq == 255:
    #     return numRegiones + 1, numRegiones + 1
    return numRegiones + 1, numRegiones + 1





def nuevoValorSegunVecinosAbaDer (ImgEt, x, y, numRegiones):
    der = 0
    aba = 0
    diag = 0
    
    if ImgEt[x][y] == 0:
        return 0, numRegiones
    
    if x+1 < len(ImgEt):
        der = ImgEt[x+1][y]
    else:
        izq = 0
        
    # if x+1 < len(ImgEt) and y+1 < len(ImgEt[0]):
    #     diag = ImgEt[x+1][y+1]
    # else:
    #     diag = 0
        
    if y+1 < len(ImgEt[0]):
        aba = ImgEt[x][y+1]
    else:
        aba = 0
        
    if aba > 0 :
        return aba, numRegiones
    if der > 0:
        return der, numRegiones
    
    # if arr == 255 or izq == 255:
    #     return numRegiones + 1, numRegiones + 1
    return ImgEt[x][y], numRegiones #tercera pasada



    
def UnRegMascara (ImgEt, x, y):
    menorValor = 255
    if (ImgEt[x][y] == 0):
        return 0
    
    for i in range(-1,2):
        for j in range(-1,2):
            if x+i < 0 or y+j < 0 or x+i >= len(ImgEt) or y+j >= len(ImgEt[0]):
                continue
            if(menorValor > ImgEt[x+i][y+j] and ImgEt[x+i][y+j] > 0):
                menorValor = ImgEt[x+i][y+j]
    return menorValor


def LimpiarRegiones (Img):
    for i in range(len(Img)-1, -1, -1 ):
        for j in range(len(Img[0])-1, -1, -1 ):
            nuevoValor = UnRegMascara (Img,i,j)
            Img[i][j]= nuevoValor
            
    return (Img)


def ListarRegiones (Img):
    regiones = []
    for i in range(len(Img)):
        for j in range(len(Img[0])):
            if Img[i][j] > 0 and not Img[i][j] in regiones:
                regiones.append(Img[i][j]);
    return regiones
    

def SimplificaRegiones (Img, listaRegiones):
    '''Recibe la imagen segmentada (como numpy array) y la lista con las regiones.
    Se usan los indices de las n regiones de la lista para etiquetarlas de 1 a n+1'''
    for i in range(len(Img)):
        for j in range(len(Img[0])):
            if Img[i][j] == 0:
                continue
            Img[i][j] = listaRegiones.index(Img[i][j]) + 1

def CalcularMasasYCentros (imgSeg, numReg):
    '''Recibe la imagen segmentada y el numero de regiones sin contar el fondo.
    Devuelve tres listas de longitud numero de regiones + 1: masas, centros_x, centros_y.
    Los resultados incluyen el fondo, aunque sus valores se devuelven a 0.'''
    masas = nuevaLista(numReg+1, 0) #Primer valor es fondo. Segundo es region 1
    centros_x = nuevaLista(numReg+1, 0)
    centros_y = nuevaLista(numReg+1, 0)
    
    for i in range(len(imgSeg)):
        for j in range(len(imgSeg[0])):
            if imgSeg[i][j] == 0:
                continue
            masas[imgSeg[i][j]] += 1
            centros_x [imgSeg[i][j]] += j
            centros_y [imgSeg[i][j]] += i
    for i in range(1, len(masas)):
        
        centros_x[i] = centros_x[i]/masas[i]
        centros_y[i] = centros_y[i]/masas[i]
    return masas, centros_x, centros_y

def nuevaLista (long, valor):
    lista = []
    for i in range(long):
        lista.append(valor)
    return lista

def crearMensajeError (string, reqId):
    return  '{"RequestId":"' + reqId + '","xy":[],"error":"' + string +'"}'


def getHardCodedTablePoses ():
    return [[212, 46], #Izquierda de la imagen
            [177,102],[244,102],
            [142,163],[213,160],[281,159],
            [107,222],[176, 221],[246,219],[317,219],
            [110,415],[178,415],[247,414],[317,414],
            [147,474],[217,473],[284,472],
            [181,532],[249,530],
            [217,588]]#Derechaa de la imagen. Se ignorará la última posicion en las pruebas

def checkPosesHardcoded (img, th):
    offset = 10
    # th = 153 #threshold
    poses = getHardCodedTablePoses()
    for pose in poses:
        p1 = [pose[0]+offset, pose[1]+offset]
        p2 = [pose[0]-offset, pose[1]+offset]
        p3 = [pose[0]-offset, pose[1]-offset]
        p4 = [pose[0]+offset, pose[1]-offset]
        if img[p1[0]] [p1[1]] >= th and img[p2[0]] [p2[1]] >= th and  img[p3[0]] [p3[1]] >= th and img[p4[0]] [p4[1]] >= th:
            return pose
    return []

# def bindingHolesAndbackground (picture):
#     imgBackground = np.copy(picture)
    
#     shape=(len(picture), len(picture[0]))
#     imgHoles = np.zeros(shape, np.uint8)
    
    
#     radiousHoles = 15
#     radiousBack = 20
#     poses = getHardCodedTablePoses()
#     for pose in poses:
#         for i in range (pose[0] + -radiousHoles, pose[0] + radiousHoles):
#             for j in range (pose[1] - radiousHoles, pose[1] + radiousHoles):
#                     imgHoles[i][j] = picture[i][j]
                
#         for i in range (pose[0] + -radiousBack, pose[0] + radiousBack):
#             for j in range (pose[1] - radiousBack, pose[1] + radiousBack):
#                 imgBackground[i][j] = 0
            
#     return imgHoles, imgBackground 

def bindingHoles (picture, radiousBack):
    imgBackground = np.copy(picture)
    # radiousBack = 20
    poses = getHardCodedTablePoses()
    for pose in poses:  
        for i in range (pose[0] + -radiousBack, pose[0] + radiousBack):
            for j in range (pose[1] - radiousBack, pose[1] + radiousBack):
                imgBackground[i][j] = 0
            
    return imgBackground 


# import cv2 as cv

# test1 = cv.imread(r'C:/Users/cxdso/Desktop/AI_analytics_Script/testImg/test1.png', cv.IMREAD_GRAYSCALE)
# test2 = cv.imread(r'C:/Users/cxdso/Desktop/AI_analytics_Script/testImg/test2.png', cv.IMREAD_GRAYSCALE)
# test3 = cv.imread(r'C:/Users/cxdso/Desktop/AI_analytics_Script/testImg/test3.png', cv.IMREAD_GRAYSCALE)
# test4 = cv.imread(r'C:/Users/cxdso/Desktop/AI_analytics_Script/testImg/test4.png', cv.IMREAD_GRAYSCALE)


# test1_et, test1_numReg = segmentacion (test1)
# test2_et, test2_numReg = segmentacion (test2)
# test3_et, test3_numReg = segmentacion (test3)
# test4_et, test4_numReg = segmentacion (test4)

# test1_masas, test1_centros_x, test1_centros_y = CalcularMasasYCentros (test1_et, test1_numReg)
# test2_masas, test2_centros_x, test2_centros_y = CalcularMasasYCentros (test2_et, test2_numReg)
# test3_masas, test3_centros_x, test3_centros_y = CalcularMasasYCentros (test3_et, test3_numReg)









