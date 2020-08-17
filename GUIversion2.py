import paho.mqtt.client as paho
import os
import socket
import ssl
import boto3
import json
import time
import numpy as np
    
global total_data_dict
total_data_dict= {}
connflag = False
start_time = True


def on_connect(client, userdata, flags, rc):
    global connflag
    client.subscribe("EdgeComputingForAbnormalDetection/Subscribe/"+sys["cert"], 1 )
    print("AWS IoT連線完成")
    connflag = True
def on_message(client, userdata, msg):
    global total_data_dict
    message = json.loads(msg.payload.decode('utf-8'))
    print(message)
    print(total_data_dict[str(message["timestamp"])])


vendor = "SiMSlab"
device = "RaspberryPi_32G"
cert = "b9c38f898c"
sys = {"vendor":vendor,"device":device,"cert":cert}

mqttc = paho.Client()                      
mqttc.on_connect = on_connect
mqttc.on_message = on_message
awshost = "azzt8jgouxwto-ats.iot.us-east-2.amazonaws.com"
awsport = 8883                                             
clientId = sys["vendor"]                                   
thingName = sys["vendor"]+"_"+sys["device"]
caPath = "/home/pi/Edge_Computing_For_Abnormal_Detection/certs/AmazonRootCA1.pem"                           
certPath = "/home/pi/Edge_Computing_For_Abnormal_Detection/certs/"+sys["cert"]+"-certificate.pem.crt"                           
keyPath = "/home/pi/Edge_Computing_For_Abnormal_Detection/certs/"+sys["cert"]+"-private.pem.key" 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
mqttc.connect(awshost, awsport, keepalive=60)
mqttc.loop_start()

start_time = True
while True:
    if connflag == True:
        timestamp = float(time.time())
        if start_time == True:
            start_time = False
            start_timestamp = timestamp
            f = open("0ad9398983ae9cf82a6dca3afb905ab7_0001.ecg","r")
            a = np.fromfile(f,dtype=np.int16)
            a = list(a)
            data = []
            for i in a:
                data.append(str(i))
            TOPIC_Value = json.dumps({"timestamp":timestamp,"startstamp":start_timestamp,"cert":sys["cert"],"sensor":"Arduino","data":data})
            total_data_dict.setdefault(str(timestamp),data)
            mqttc.publish("EdgeComputingForAbnormalDetection/Publish",TOPIC_Value, qos=1)
            print("ok")
    else:
        pass