import cv2,json
import base64 as b64
from pprint import pprint

# with open("fromFANUC.json") as jsonFile:
#     jsonObject = json.load(jsonFile)
#     img_array=cv2.imread('IMG1.png')
#     jsonObject[0].get("ImageData")["Picture"]= img_array.tolist()
#     jsonObject[0].get("ImageData")["txtPicture"] = str(b64.standard_b64encode(img_array),'utf-8')
#     with open('fromFANUC.json', 'w') as outfile:
#         json.dump(jsonObject, outfile,)
    #pprint(img_array.tolist())

with open("fromFANUC.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    img_array=cv2.imread('IMG1.png')
    cv2.imshow('ss',img_array)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys the window showing image