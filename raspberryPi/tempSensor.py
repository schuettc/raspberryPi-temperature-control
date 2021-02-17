from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import os
import glob
import time

ENDPOINT = "a1dpf39ivechwj-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERT = "certs/device.pem.crt"
PATH_TO_KEY = "certs/private.pem.key"
PATH_TO_ROOT = "certs/AmazonRootCA1.pem"
TOPIC = "iot/temperature"
path="/sys/bus/w1/devices" 
sensors=["28-01204f79c6d6"]
suffix="w1_slave"

event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERT,
            pri_key_filepath=PATH_TO_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_ROOT,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )

def hexbin(h):
    h=str(h)
    b=str(bin(int(h,16)))[2:].rjust(16,"0")
    return b

def convert(t):
    lsb=t[:2]
    msb=t[3:5]
    h=msb+lsb
    b=hexbin(h)
    if b[:5]=="11111":
        sign="-"
    else:
        sign="+"
    out=0
    b2=b[5:]
    for a,n in enumerate(range(6,-5,-1)):
        p=int(b2[a])*pow(2,n)
        out+=p
    if sign=="-":
        out=out-128
    else:
        out=out

    temp_f = out * 9.0 / 5.0 + 32.0
    return temp_f

def read_temp():
    for s in sensors:
        input_file=path+"/"+s+"/"+suffix
        f = open(input_file, "r")
        data=f.readlines()
        t=data[1][:5]
        f_temp = convert(t)
        return f_temp

while True:
	print("Connecting to {} with client ID '{}'...".format(
        	ENDPOINT, CLIENT_ID))
	connect_future = mqtt_connection.connect()
	connect_future.result()
	print("Connected!")
	print('Begin Publish')
	epoch_time = int(time.time())
	data = round(read_temp(),2)
	print(data)	
	message = {"temperature" : data, "time" : epoch_time }
	print(json.dumps(message))	
	mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_MOST_ONCE)
	print("Published: '" + json.dumps(message) + "' to the topic: " + "'test/testing'")

	print('Publish End')
	disconnect_future = mqtt_connection.disconnect()
	disconnect_future.result()

	time.sleep(60)
