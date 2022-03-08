from flask import Flask
import FANUC.configurations as CONFIG


app = Flask(__name__) #"FASTory-EM-Data-Collection"

########using flask-mqtt for message bus connection##########
app.config['MQTT_CLIENT_ID'] = CONFIG.MQTT_CLIENT_ID
app.config['MQTT_USERNAME'] = CONFIG.NAME
app.config['MQTT_BROKER_URL'] = CONFIG.MQTT_BROKER_URL  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = CONFIG.zMSG_TLS_PORT#zMSG_PORT_VPN # default port for non-tls connection
app.config['MQTT_USERNAME'] = CONFIG.MQTT_USERNAME  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = CONFIG.MQTT_PASSWORD  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = CONFIG.Conn_ALIVE  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = CONFIG.MQTT_TLS_ENABLED # set TLS to disabled for testing purposes
#app.config['MQTT_TLS_CA_CERTS'] = CONFIG.MQTT_TLS_CERTFILE
#app.config['MQTT_TLS_INSECURE'] = True-'MQTT_TLS_CERTFILE'