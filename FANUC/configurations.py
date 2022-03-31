#########################Middleware CONSTS-Global VARS#########################

#related to middleware app only

LocIP = '0.0.0.0'#'192.168.1.2'
LocPort = 3000
FlaskPort = 3001
#ZDMP DAQ and M&S BUS
tokenURL="https://keycloak-zdmp.platform.zdmp.eu/auth/realms/testcompany/protocol/openid-connect/token"
ROBOT_ID = 'E122350'
ROBOT_NAME = 'LR-Mate-200iD-4S-'+ROBOT_ID
zMSG_PORT_VPN = 30204
zMSG_TLS_PORT = 8883
z_MSG_URL_VPN = '192.168.100.100'
z_MSG_URL = 'msgbus-zdmp.platform.zdmp.eu'
USER = 'tau'
PASSWORD =  'ZDMP-tau2020!'
TOPIC_TYPE= 'multi'

#Roki
results=["reachable","not reachable","","error"]
rokiMsg=[]
#Robot-KAREL URLS
ORCHESTRATOR_URL = 'http://192.168.1.1/KAREL/z_Orchstrate'
#ORCHESTRATOR_URL = 'http://192.168.1.1/KAREL/z_Orc_v1_1'
UPDATE_POS_REG = 'http://192.168.1.1/KAREL/'

#FANUC Socket and FTP  Server
socket_ServerIP = '192.168.1.1'
socket_PORT = 1162      # The port used by the server
FTP_ServerIP = '192.168.1.1'
BASE_TOPIC = 'LR-Mate/'
BASE_TOPIC_DAQ = 'LR-Mate/'#T5_1-Data-Acquisition/Datasource ID: {} - MultiTopic/LR-Mate/
VIS_LOG_BASE_DIR = 'ud1:/vision/logs/'
#DAQ URLs
ADMIN_URL = f'http://apigw-zdmp.platform.zdmp.eu/gateway/data-acquisition-admin-service/v0'#f'http://192.168.100.100:30025'
ASYNCH_URL = f'http://apigw-zdmp.platform.zdmp.eu/gateway/data-acquisition-asynch-service/v0' #f'http://192.168.100.100:30026'
SYNCH_URL =  f'http://apigw-zdmp.platform.zdmp.eu/gateway/data-acquisition-synch-service/v0' #f'http://192.168.100.100:30027'
TOPIC_TYPE= 'multi'

# ZDMP-Cumulocity IoT tenant credentials
# domain = "https://zdmp-da.eu-latest.cumulocity.com"
# TenantID = "t59849255/mahboob.elahi@tuni.fi"
# passward = "mahboobelahi93"

##############################MQTT-Settings###########################################
Conn_ALIVE = 60
NAME = ROBOT_NAME
MQTT_CLIENT_ID = 'E122350-LRMate200iD-4S'
MQTT_BROKER_URL = z_MSG_URL #z_MSG_URL  # use the free broker from HIVEMQ
MQTT_BROKER_PORT = zMSG_TLS_PORT# zMSG_PORT  # default port for non-tls connection
MQTT_USERNAME = USER  # set the username here if you need authentication for the broker
MQTT_PASSWORD = PASSWORD # set the password here if the broker demands authentication
MQTT_KEEPALIVE = Conn_ALIVE  # set the time interval for sending a ping to the broker to 5 seconds
MQTT_TLS_ENABLED = True  # set TLS to disabled for testing purposes
MQTT_TLS_CA_CERTS = './files/ca_certificate.pem'
MQTT_REFRESH_TIME = 1.0  # refresh time in seconds