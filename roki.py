import cv2,json
import base64 as b64
from pprint import pprint

with open("fromFANUC.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    img_array=cv2.imread('IMG00.png', cv2.IMREAD_GRAYSCALE)
    #jsonObject.get("ImageData")["Picture"]= img_array.tolist()
    jsonObject.get("ImageData")["txtPicture"] = str(b64.standard_b64encode(img_array),'utf-8')
    jsonObject.get("ImageData")["Picture"]= img_array.tolist()
    with open('fromFANUC.json', 'w') as outfile:
        json.dump(jsonObject, outfile,
                indent=4
                )#separators=(',',': ')
    #pprint(img_array.tolist())

# with open("fromFANUC.json") as jsonFile:
#     jsonObject = json.load(jsonFile)
#     img_array=cv2.imread('IMG1.png', cv2.IMREAD_GRAYSCALE)
#     cv2.imshow('ss',img_array)
#     cv2.waitKey(0) # waits until a key is pressed
#     cv2.destroyAllWindows() # destroys the window showing image