import cv2,json
from pprint import pprint
with open("fromFANUC.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    img_array=cv2.imread('IMG1.png')
    jsonObject[0].get("ImageData")["Picture"]= img_array.tolist()
    with open('fromFANUC.json', 'w') as outfile:
        json.dump(jsonObject, outfile,
                   indent=4)
    pprint(img_array.tolist())