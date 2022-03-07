import threading,time,requests,json
from pprint import pprint as P
from FANUC import app
from flask import request,jsonify
from FANUC.configurations import*
from  flask_mqtt import Mqtt



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

    # accessors and setters
    def get_ID(self):
        return self.ID
    def set_source_ID(self, srID):
        self.source_ID = srID

    #####Methods#######  
    def getAccessToken(self):
        ACCESS_URL = tokenURL 
        headers = { 'accept': "application/json", 'content-type': "application/x-www-form-urlencoded" }
        payload = "grant_type=password&client_id=ZDMP_API_MGMT_CLIENT&username=zdmp_api_mgmt_test_user&password=ZDMP2020!"
        response = requests.post(ACCESS_URL, data=payload, headers=headers)
        self.token = response.json().get('access_token')
        self.access_token_time = int(time.time())
        self.expire_time = response.json().get('expires_in')
        self.headers={"Authorization": f"Bearer {self.token}"}
        print(f'[X-W-Tk] ({response.status_code})')

    def refreshToken(self):
        while True:
            time.sleep(1)
            print(f'[X-W-rT] ({self.access_token_time}, {self.expire_time}, {int(time.time()-self.access_token_time)})')
            if int(time.time()-self.access_token_time)>=(self.expire_time-50):
                                    print(f'[X-W-sm] Accessing New Token.......')
                                    self.getAccessToken()
    ####DAQ related#####
    #events/alarms/deviceControl etc
    def handleAlarms(self):
        pass

    def handleEvents(self):
        pass

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
                P(req.json())
            else:
                print('[X-W-RD] Registering the device')
                req_R = requests.post(
                    url=f'{ADMIN_URL}/registerDevice?externalId={self.ID}&name={self.NAME}&type=c8y_Serial',
                    headers=self.headers)
                print(f'Http Status Code: {req_R.status_code}')
                # setting souece ID of device
                self.set_source_ID(req_R.json().get('id'))
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
                print(f'[X-W-SUD] Subscribing to Data Source: {self.external_ID}....{req.status_code}')
                req = requests.get(f'{ASYNCH_URL}/subscribe',
                                params=payload,headers=self.headers)
                if req.status_code == 200:
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
    #   Flask Application
    # *******************************************

    def runApp(self):
        mqtt = Mqtt(app)
        #####MQTT Endpoints################
        @mqtt.on_connect()
        def handle_connect(client, userdata, flags, rc):
            if rc==0:

                print("[X-W-MQTT] connected, OK Returned code=",rc)
                #subscribe to tpoics
                time.sleep(0.1)
                mqtt.unsubscribe_all()
                #mqtt.unsubscribe(BASE_TOPIC)
                time.sleep(1)
                mqtt.subscribe(BASE_TOPIC.format(self.ID)+"IKsolution")
                # IKsolution = BASE_TOPIC.format(self.ID)
                # IKsolution=IKsolution+"IKsolution"
                # mqtt.subscribe(IKsolution)
                print(f'[X-W-MQTT] Subscribed to: {BASE_TOPIC.format(self.ID)+"IKsolution"}')  
                #print(f'[X-W-MQTT] Subscribed to: {IKsolution}')    
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
            mqtt.unsubscribe_all()
            # mqtt.unsubscribe(BASE_TOPIC)
            mqtt.unsubscribe_all()
            print("[X-W-MQTT] CLIENT DISCONNECTED")

        @mqtt.on_message()
        def handle_mqtt_message(client, userdata, message):
            try:
                payload=json.loads(message.payload)
                print(f"{type(payload)},'??',{payload}")
                
                        
            except ValueError:
                print('[X-W-MQTT] Decoding JSON has failed')

        ########Flask Application Endpoints################


        @app.route('/', methods=['GET'])
        def index():

            return "<h1>welcom from zFANUC Middleware App!</h1>"
        
        app.run(host='0.0.0.0', port=FlaskPort)