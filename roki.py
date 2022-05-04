import cv2,json
import base64 as b64
from pprint import pprint
import numpy as np

# with open("fromFANUC.json") as jsonFile:
#     jsonObject = json.load(jsonFile)
#     img_array=cv2.imread('IMG00.png', cv2.IMREAD_GRAYSCALE)
#     #jsonObject.get("ImageData")["Picture"]= img_array.tolist()
#     jsonObject.get("ImageData")["txtPicture"] = str(b64.standard_b64encode(img_array),'utf-8')
#     jsonObject.get("ImageData")["Picture"]= img_array.tolist()
#     with open('fromFANUC.json', 'w') as outfile:
#         json.dump(jsonObject, outfile,
#                 indent=4
               #separators=(',',': ') )
    #pprint(img_array.tolist())

# with open("fromFANUC.json","r") as jsonFile:
#     jsonObject = json.load(jsonFile)
#     print(type(jsonObject.get("ImageData").get("Picture")))
#     #img_array=cv2.imread('IMG1.png', cv2.IMREAD_GRAYSCALE)
#     decodedImg = b64.b64decode(jsonObject.get("ImageData").get("Picture"))
#     print(type(decodedImg))
#     jpg_as_np = np.asarray(bytearray(decodedImg), dtype=np.uint8)
#     print(type(jpg_as_np))
#     img = cv2.imdecode(jpg_as_np, cv2.IMREAD_GRAYSCALE)
#     print(type(img))
#     cv2.imwrite('test.png', img)
    # cv2.imshow('ss',decodedImg)
    # cv2.waitKey(0) # waits until a key is pressed
    # cv2.destroyAllWindows() # destroys the window showing image


    # decodedImg = b64.b64decode(JSON_DATA.get("ImageData")["Picture"])
    # print(type(decodedImg))
    # jpg_as_np = np.asarray(bytearray(decodedImg), dtype=np.uint8)
    # print(type(jpg_as_np))
    # img = cv2.imdecode(jpg_as_np, cv2.IMREAD_GRAYSCALE)
    # print(type(img))
    # #cv2.imwrite('test.png', img)
    # cv2.imshow('ss',decodedImg)
    # cv2.waitKey(0) # waits until a key is pressed
    # cv2.destroyAllWindows() # destroys the window showing image
# img_array=cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    # img_base64 = to_base64(img_array)#bytes
    # print(type(img_base64))
    # img_decoded = from_base64(img_base64)
    # JSON_DATA.get("ImageData")["Picture"] = img_base64
    # print(img_decoded.shape,type(img_decoded))#numpyarray
    # cv2.imwrite('test.png', img_decoded)
    # cv2.imshow('ss',img_decoded)
    # cv2.waitKey(0) # waits until a key is pressed
    # cv2.destroyAllWindows() # destroys the window showing image
    # height,width=img_array.shape
    # print(height,width)
    #imgen64=b64.standard_b64encode(img_array)
    # #########################################################################
    # #JSON_DATA.get("ImageData")["Picture"]=img_array.tolist()
    #JSON_DATA.get("ImageData")["Picture"] = str(b64.standard_b64encode(imgen64),'utf-8')
    # # json.dump(JSON_DATA,indent=4,separators=(',',': '))
    # decodedImg = b64.b64decode(JSON_DATA.get("ImageData")["Picture"])
    # print(type(decodedImg),decodedImg.flatten()[0:10])
    # jpg_as_np = np.asarray(bytearray(decodedImg), dtype=np.uint8)
    # print(type(jpg_as_np),jpg_as_np.shape)
    # img = cv2.imdecode(jpg_as_np, cv2.IMREAD_GRAYSCALE)
    # print(type(img))

    #########################################################################
import numpy as np
import base64 as b64
import cv2 as cv

# def getImgFrom1DArray (array, j_size):
#     lenArray = len(array)
#     numSegments = int( lenArray / j_size)
#     resto = lenArray % j_size
#     img = np.zeros((numSegments, j_size),dtype=np.ndarray)
#     for i in range(0,numSegments):
#         for j in range(j_size):
#             img[i][j] = array[i*j_size+j]
#     return img


# adrees = r'C:\Users\cxdso\Desktop\TEMP\IMG02.txt'
# f = open(adrees,'r')
# txtString = f.read()

# full64deco = b64.standard_b