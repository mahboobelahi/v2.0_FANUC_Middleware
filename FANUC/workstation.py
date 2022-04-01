import threading,time,requests,json,socket
from pprint import pprint as P
from FANUC import app
from flask import request,jsonify
from FANUC.configurations import*
from  flask_mqtt import Mqtt
from FANUC.UtilityFunction import* 

# Anonymous FTP login
from ftplib import FTP
#mqtt = Mqtt(app)

class RobotCell():
    def __init__(self,id,name):

        self.ID = id
        self.NAME = name
        self.source_ID = 0
        #token
        self.token=''
        self.access_token_time=0
        self.expire_time = 0
        self.headers={}
        #for zRoki
        self.IMG_Count=1
        self.VIS_LOG_BASE_DIR = 'ud1:/vision/'
        self.JSON_DATA={"ImageData":{"pix/mm":0.623,"format":"PNG",
                        "Width":640,"Height":480,
                        "Part_Z_dimention":-269.974,
                        "Picture":""},
                        "RobotData":{}
                        }
        
        self.toJson = []
        

    # getters 
    def get_ID(self):
        return self.ID
    def get_IMG_Count(self):
        return self.IMG_Count

    def get_JSON_DATA(self):
        return self.JSON_DATA
    def set_JSON_DATA(self,data):
        self.JSON_DATA=data
    
    def get_headers(self):
        return self.headers 

    # setters
    def set_source_ID(self, srID):
        self.source_ID = srID

    def inc_IMG_Count(self):
        self.IMG_Count = self.IMG_Count+1
 
    def toJsonFile(self):
        #self.toJson.append(self.get_JSON_DATA().copy())
        with open('fromFANUC.json', 'w') as outfile:
            json.dump(self.get_JSON_DATA(), outfile,
                        indent=4)#,  separators=(',',': ')


    # *******************************************
    #   Class Methods
    # *******************************************  
    def getAccessToken(self):
        try:
            ACCESS_URL = tokenURL 
            headers = { 'accept': "application/json", 'content-type': "application/x-www-form-urlencoded" }
            payload = "grant_type=password&client_id=ZDMP_API_MGMT_CLIENT&username=zdmp_api_mgmt_test_user&password=ZDMP2020!"
            response = requests.post(ACCESS_URL, data=payload, headers=headers)
            if response.status_code ==200:
                self.token = response.json().get('access_token')
                self.access_token_time = int(time.time())
                self.expire_time = response.json().get('expires_in')
                self.headers={"Authorization": f"Bearer {self.token}"}
                print(f'[X-W-Tk] ({response.status_code})')
                self.sendEvent('Token','Accessing Token......')
            else:
                print(f"[X-W-Tk] {response.status_code}")
        except requests.exceptions.RequestException as err:
            print ("[X-W-Tk] OOps: Something Else",err)

    def refreshToken(self):
        while True:
            time.sleep(1)
            print(f'[X-W-rT] ({self.access_token_time}, {self.expire_time}, {int(time.time()-self.access_token_time)})')
            if int(time.time()-self.access_token_time)>=(self.expire_time-50):
                                    #self.sendEvent('Token','Refreshing Token......')
                                    print(f'[X-W-sm] Accessing New Token.......')
                                    self.getAccessToken()
    # *******************************************
    #   DAQ-Related
    # *******************************************
    #events/alarms/deviceControl etc
    def sendAlarm(self):
        pass

    def sendEvent(self,type,text):
        payload = {"externalId": self.get_ID(),
                    "type": type,
                    "text": text}
        try:
            req = requests.post(f'{SYNCH_URL}/sendEvent',
                            params=payload,
                            headers=self.get_headers(),timeout=3)
            print(f'[X-W-SnDE] {req.status_code}')
        except requests.exceptions.HTTPError as errh:
            print ("[X-W-RD] Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("[X-W-RD] Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("[X-W-RD] Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("[X-W-RD] OOps: Something Else",err)

    def deviceControl(self):
        pass

    # registration to ZDMP-DAQ component
    def register_device(self):
        # need to set some guard condition to avoid re-registration of device
        # each device registared against a unique external ID
        try:
            req = requests.get(
                url=f'{ADMIN_URL}/deviceInfo?externalId={self.ID}',
                headers=self.headers)
            if req.status_code == 200:
                self.set_source_ID(req.json().get('id'))
                print('[X-W-RD] Device already Registered. Device details are:\n')
                #P(req.json())
            else:
                print('[X-W-RD] Registering the device')
                req_R = requests.post(
                    url=f'{ADMIN_URL}/registerDevice?externalId={self.ID}&name={self.NAME}&type=c8y_Serial',
                    headers=self.headers)
                print(f'Http Status Code: {req_R.status_code}')
                # setting souece ID of device
                self.set_source_ID(req_R.json().get('id'))
                self.sendEvent('DAQ-ADMIN','Robot info accessed.')
                print('[X-W-RD] Device Registered Successfully.\n')
                # pprint(req_R.json())
        except requests.exceptions.HTTPError as errh:
            print ("[X-W-RD] Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("[X-W-RD] Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("[X-W-RD] Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("[X-W-RD] OOps: Something Else",err)

    # register data source to ASYNC-DAQ service
    def sub_or_Unsubscribe_DataSource(self, subs=False):
        
        payload = {"externalId": self.ID, "topicType": 'multi'}
        try:
            if subs:
                req = requests.get(f'{ASYNCH_URL}/unsubscribe',
                                params=payload,headers=self.headers)
                self.sendEvent('DAQ-ASYNC','Data source have unsubscribed to previous subscriptions.....')
                print(f'[X-W-SUDU] Subscribing to Data Source: {self.ID}....{req.status_code}')
                req = requests.get(f'{ASYNCH_URL}/subscribe',
                                params=payload,headers=self.headers)
                if req.status_code == 200:
                    self.sendEvent('DAQ-ASYNC','Data source have subscribed to ASYNC data access...')
                    print(f'[X-W-SUD] Subscrption Status: {req.status_code} {req.reason}')

                elif req.status_code == 500:
                    time.sleep(1)
                    req = requests.get(f'{ASYNCH_URL}/subscribe',
                                params=payload,headers=self.headers)
                    if req.status_code == 200:
                        self.sendEvent('DAQ-ASYNC','Data source have subscribed to ASYNC data access...')
                        print(f'[X-W-SUD] Subscrption Status: {req.status_code} {req.reason}')

                else:
                    print(f'[X-W-SUD] Subscrption Status: {req.status_code} {req.reason}')
                    
                    
            else:
                req = requests.get(f'{ASYNCH_URL}/unsubscribe',
                                params=payload,headers=self.headers)

                if req.status_code == 200:
                    print(f'[X-W-SUD] Unsubscrption Status: {req.status_code} {req.reason}')
                else:
                    print(f'[X-W-SUD] Unsubscrption Status: {req.status_code} {req.reason}')
        except requests.exceptions.HTTPError as errh:
            print ("[X-W-SUD] Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("[X-W-SUD] Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("[X-W-SUD] Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("[X-W-SUD] OOps: Something Else",err)

    # *******************************************
    #   FTP-Client---->FANUC FTP-Server
    # *******************************************
 
    def download_and_publish_pic(self,mqtt):
        
        
 
        #VIS_LOG_BASE_DIR = 'ud1:/vision/'
        with FTP(FTP_ServerIP) as ftp:
            print(f'[X-FTP] Welcome Msg from Robot: {ftp.getwelcome()}')

            # changing to image log dir
            ftp.cwd(self.VIS_LOG_BASE_DIR)
            print(f'[X-FTP] Current_Dir: {ftp.pwd()}')

            """
                FANUC FTP server supports minimal commands that's why 
                in pervious version old dir method were used for listing
                all directories.
                With the modification of z_Take_IMG KAREL source file, navigation in
                robot FTP server much simplified.
            """

            #downloading file from FTP-Server

            with open(f'IMG{self.get_IMG_Count()}.png', 'wb') as local_file:
                        ftp.retrbinary(f'RETR IMG.png', local_file.write)
                        self.sendEvent('FTP','Workspace image downloaded from FANUC FTP server')
                        self.sendEvent('CameraCycle',f'CameraCycle_{self.get_IMG_Count()} has ended.')
                        print('[X-FTP] Image downloaded successfully....')
    
                # now: encoding the data to json
                # result: string          

            JSON_STR=json.dumps(IMGtob64Str(f'IMG{self.get_IMG_Count()}.png',self),
                                indent=4,separators=(',',': '))
            #print(BASE_TOPIC_DAQ.format(self.ID))
            mqtt.publish(BASE_TOPIC+"fromFANUC",JSON_STR,retain=False)
            self.inc_IMG_Count()
            #time.sleep(1)
            threading.Thread(target=self.toJsonFile).start()
            print('[X-FTP] Data published successfully....')

            #to DAQ
            # send_Measurements(  self.JSON_DATA,self.get_ID(),
            #                     self.get_IMG_Count(),
            #                     self.get_headers())
    
    # ************************************************
    #   connect to FANUC Socket Client and ZDMP MsgBus
    # ************************************************
    def start_socket_server(self):
        mqtt = Mqtt(app)
        #####MQTT Endpoints################
        @mqtt.on_connect()
        def handle_connect(client, userdata, flags, rc):
            if rc==0:
                self.sendEvent('MsgBus',f'FANUC connected to public instance of ZDMP-MsgBus.')
                print("[X-W-MQTT] connected, OK Returned code=",rc)
                #subscribe to tpoics
                time.sleep(0.1)
                mqtt.unsubscribe_all()
                #mqtt.unsubscribe(BASE_TOPIC)
                time.sleep(1)
                mqtt.subscribe(BASE_TOPIC_DAQ.format(self.ID)+"fromRoki")
                print(f'[X-W-MQTT] Subscribed to: {BASE_TOPIC_DAQ.format(self.ID)+"fromRoki"}')    
            else:
                print("[X-W-MQTT] Bad connection Returned code=",rc)

        @mqtt.on_subscribe()
        def handle_subscribe(client, userdata, mid, granted_qos):
            print('[X-W-MQTT] Subscription id {} granted with qos {}.'
                .format(mid, granted_qos))   

        # @mqtt.unsubscribe()
        # def handle_unsubscribe(client, userdata, mid):
        #     print('Unsubscribed from topic (id: {})'.format(mid))

        @mqtt.on_disconnect()
        def handle_disconnect():
            self.sendEvent('MsgBus',f'FANUC disconnected from ZDMP-MsgBus.')
            mqtt.unsubscribe_all()
            # mqtt.unsubscribe(BASE_TOPIC)
            mqtt.unsubscribe_all()
            print("[X-W-MQTT] CLIENT DISCONNECTED")

        @mqtt.on_message()
        def handle_mqtt_message(client, userdata, message):
            try:
                self.sendEvent('MsgBus',f'FANUC connected to public instance of ZDMP-MsgBus.')
                payload=json.loads(message.payload)
                rokiMsg.append(payload.copy())
                with open('fromRoki.json', 'w') as outfile:
                    json.dump(rokiMsg, outfile,
                                indent=4,  
                                separators=(',',': '))
                print(f"[X-W-MQTT] {type(payload)},'??',{payload}")
                # threading.Thread(target=parsed_Roki_Msg,
                #             args=(payload,self),
                #             daemon=True).start()
                threading.Thread(target=update_POS,
                            args=(payload,self),
                            daemon=True).start()
            except ValueError:
                print('[X-W-MQTT] Decoding JSON has failed')
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((LocIP,LocPort))
        sock.listen(1)
        
        while True:
            print("[X-SC] Waiting for connection...")
            conn, client_address = sock.accept()

            print("[X-SC] Connection from ", client_address)
            
            while True:
                
                data = conn.recv(1024)
                #print(f'[X-SC] {data}')
                dat = self.get_JSON_DATA()
                if data != b'':
                    #self.sendEvent('FANUC-Socket',f'FANUC socket client connected to middleware Socket Server.')
                    
                    data = data.decode().strip().split()
                    #print(f'[X-SC] {data}')
                    if len(data)>1:
                       
                        
                        #during debugging comment all before else
                        
                        if dat.get("RobotData").get(data[0]) == None:
                            #print("data_0 ",data[0])
                            dat["RobotData"][data[0]]=dict(
                                                            [("XYZ",[float(i) for i in data[1:4] ]),
                                                            ("WPR",[float(i) for i in data[4:] ]),
                                                            ("CONFIG","NUT000")]
                                                            )
                        else:  
                            dat["RobotData"][data[0]]= dict(
                                                            [("XYZ",[float(i) for i in data[1:4] ]),
                                                            ("WPR",[float(i) for i in data[4:] ]),
                                                            ("CONFIG","NUT000")]
                                                            )
                    self.set_JSON_DATA(dat)
                    #print(dat)
                    #self.sendEvent('FANUC-Socket',f'Data received and closing socket.')
                else:
                    print('[X-SC] BREAK LOOP')
                    break


            #print('[X-SC] IN LOOP')
            self.sendEvent('FANUC-FTP',f'Middleware FTP-client downloading image from FANUC FTP server.')
            #print(f'[X-SC] {self.get_JSON_DATA()}')
            threading.Timer(0.5, self.download_and_publish_pic,args=(mqtt,)).start()
            
            #self.get_JSON_DATA().get("RobotData").clear()
            #P(self.get_JSON_DATA())
            time.sleep(1)
        
        #conn.sendall(data)

    # *******************************************
    #   Flask Application
    # *******************************************
    
    def runApp(self):

        ########Flask Application Endpoints################

        @app.route('/', methods=['GET'])
        def index():

            return "<h1>welcom from zFANUC Middleware App!</h1>"
        
        app.run(host='0.0.0.0', port=FlaskPort)