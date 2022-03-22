import requests,threading,json,urllib.parse,time
from base64 import b64encode
from datetime import datetime

from FANUC.configurations import (ROBOT_ID,BASE_TOPIC,
                            ORCHESTRATOR_URL,
                            UPDATE_POS_REG,
                            SYNCH_URL)

#utility Function(S)
#send Data to zRoki
def IMG_bytes_to_JSON(image,JSON_DATA):
                # reading newly downloaded file as bytes
                # first: reading the binary stuff
                # note the 'rb' flag
                # result: bytes
                with open(image, 'rb') as file:
                    pub_img = file.read()
                    # second: base64 encode read data
                    # result: bytes (again)
                    base64_bytes = b64encode(pub_img)
                    # third: decode these bytes to text
                    # result: string (in utf-8)
                    base64_string = base64_bytes.decode('utf-8')
                    JSON_DATA.get("ImageData")[0].update({"Picture":base64_string})
                    JSON_DATA.update({"timeStamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S')})
                    return JSON_DATA
       
#Robot information cycle 1
def start_camera_cycle(obj):
    try:
        req = requests.get(f'{ORCHESTRATOR_URL}', params={"CMD":199})
        obj.sendEvent(f'CameraCycle',f'CameraCycle_{obj.get_IMG_Count()} has started.')
        print(f'[X-UH-CamCycle] Status Code: {req.status_code}') 
        #start_camera_cycle(self)
        req= requests.get(f'{ORCHESTRATOR_URL}',params={"CMD":199})
        print(f'[X-UH] {req.status_code}')
        time.sleep(1)
    except requests.exceptions.RequestException as err:
        print ("[X-W-SUD] OOps: Something Else",err)
 

def parsed_Roki_Msg(Roki_Msg,self):
    #de-serialize incomming JSON string to python dictionary
    #Msg_dict = json.loads(Roki_Msg)
    IK_solutions = Roki_Msg.get("InverseKinematicSolutions")
    id =100 #for jPOS
    if IK_solutions:
        for j in IK_solutions:
            key,j_angles = list(j.items())[0]
            payload = dict([
                ("id",id),
                ("J1_angel_str",j_angles[0]),
                ("J2_angel_str",j_angles[1]),
                ("J3_angel_str",j_angles[2]),
                ("J4_angel_str",j_angles[3]),
                ("J5_angel_str",j_angles[4]),
                ("J6_angel_str",j_angles[5])])
            print(f'[X-UH] {payload}')
            try:
                req= requests.get(f'{UPDATE_POS_REG}z_getRokiPOS',params=payload)
                print(f'[X-UH] {req.text}')
                if int(req.text) == 200:
                    print("[X-UH] Reachable POS....")
                    time.sleep(0.1)
                    self.sendEvent('POS',f'POS-Reg is updated with IK Solution {j_angles}')
                    self.sendEvent('RobotCycle', 'Robot cycle is initiatiated.')
                    # req= requests.get(f'{ORCHESTRATOR_URL}',params={"CMD":198})
                    # print(f'[X-UH] Updating POS... {req.status_code}')
                else:
                    print("[X-UH] Not-Reachable POS....")
                    self.sendEvent('RobotCycle', 'Robot cycle not initiatiated.')
                    self.sendEvent('POS',f'POS-Reg not updated for IK Solution {j_angles} coz, Not Reachable!')
                    
                    try:
                        
                        #start_camera_cycle(self)
                        req= requests.get(f'{ORCHESTRATOR_URL}',params={"CMD":199})
                        print(f'[X-UH-Cam] {req.status_code}')
                        #time.sleep(1)
                    except requests.exceptions.RequestException as err:
                        print ("[X-W-SUD] OOps: Something Else",err)
            except requests.exceptions.RequestException as err:
                print ("[X-W-SUD] OOps: Something Else",err)
    else:
        try:
            print("[X-UH-NK] No IK Solutions....")
            print("[X-UH-NK] Now starting camera cycle...")
            
            #start_camera_cycle(self)
            req= requests.get(f'{ORCHESTRATOR_URL}',params={"CMD":199})
            print(f'[X-UH] {req.status_code}')
            time.sleep(1)
        except requests.exceptions.RequestException as err:
            print ("[X-W-SUD] OOps: Something Else",err)


#update robot position
def update_POS(Roki_Msg,self):

    #error checking must be implemented
    if (Roki_Msg.get("errors") !=None) and (len(Roki_Msg.get("errors"))):
        print(f'[X-uPOS] {Roki_Msg.get("errors")}')
        #start camera cycle
        #threading.Thread(target=start_camera_cycle,args=(self,)).start()
        self.sendEvent('POS',f'POS-Reg is not updated: {Roki_Msg.get("errors")}')
        return

    Pose = Roki_Msg.get("Pose")
    id =94 # cartPos
    if Pose:
            payload = dict([
                ("id",id),
                ("XX",Pose.get("xyz")[0]),
                ("YY",Pose.get("xyz")[1]),
                ("ZZ",Pose.get("xyz")[2]),
                ("WW",Pose.get("wpr")[0]),
                ("PP",Pose.get("wpr")[1]),
                ("RR",Pose.get("wpr")[2])])
            print(f'[X-UH-uPOS]>>> {payload}')
            try:
                req= requests.get(f'{UPDATE_POS_REG}z_CART_POS',params=payload)
                print(f'[X-UH-uPOS] {req.text}')
                if int(req.text) == 200:
                    print("[X-UH-uPOS] Reachable POS....")
                    time.sleep(0.1)
                    self.sendEvent('POS',f'POS-Reg is updated with IK Solution {Pose}')
                    self.sendEvent('RobotCycle', 'Robot cycle is initiatiated.')
                    req= requests.get(f'{ORCHESTRATOR_URL}',params={"CMD":198})
                    print(f'[X-UH--uPOS] Updating POS... {req.status_code}')
                else:
                    print("[X-UH-uPOS] Not-Reachable POS....")
                    self.sendEvent('RobotCycle', 'Robot cycle not initiatiated.')
                    self.sendEvent('POS',f'POS-Reg not updated for IK Solution {Pose} coz, Not Reachable!')
                    
                    try:
                        
                        #start_camera_cycle(self)
                        req= requests.get(f'{ORCHESTRATOR_URL}',params={"CMD":199})
                        print(f'[X-UH-Cam] {req.status_code}')
                        #time.sleep(1)
                    except requests.exceptions.RequestException as err:
                        print ("[X-UH-uPOS] OOps: Something Else",err)
            except requests.exceptions.RequestException as err:
                print ("[X-UH-uPOS] OOps: Something Else",err)
    else:
        try:
            print("[X-UH-uPOS] No IK Solutions....")
            print("[X-UH-uPOS] Now starting camera cycle...")
            
            #start_camera_cycle(self)
            threading.Thread(target=start_camera_cycle,args=(self,)).start()
            # req= requests.get(f'{ORCHESTRATOR_URL}',params={"CMD":199})
            print(f'[X-UH] {req.status_code}')
            time.sleep(1)
        except requests.exceptions.RequestException as err:
            print ("[X-W-SUD] OOps: Something Else",err)
    #[float(val) for val in json.loads(POS).values()]
    # id= 100
    # (XX,YY,ZZ,WW,PP,RR) = ([float(val) for val in json.loads(POS).values()])
    # payload =dict([ ("id",id),
    #                 ("XX",XX),("YY",YY),("ZZ",ZZ),
    #                 ("WW",WW),("PP",PP),("RR",RR)
    #                 ])
    
    # req= requests.get(f'{UPDATE_POS_REG}',params=payload)
    # print(f'[X-UH] {req.url}')
    # time.sleep(0.1)
    # req= requests.get(f'{ORCHESTRATOR_URL}',params={"CMD":198})
    # print(f'[X-UH] {req.url}')

  

#SYNCHRONOUSLY sending measurements on custom endpoint
def send_Measurements(JSON_DATA,ID,count,headers):
    
    
    # for k, v in JSON_DATA.items():
    # print(k)
    # setting query string
    JSON_DATA.get("ImageData")[0]["Picture"]=count
    payload = {"externalId": ID,
                "fragment": f'LR-Mate/fromFANUC'}
    payload = urllib.parse.urlencode(payload, safe='/')
    print(type(JSON_DATA),JSON_DATA)
    req = requests.post(f'{SYNCH_URL}/sendCustomMeasurement',
                        params=payload,
                        json=JSON_DATA,headers=headers)
    print('[X-UF]',req.url)
    print('[X-UF]',req.status_code,req.reason)


