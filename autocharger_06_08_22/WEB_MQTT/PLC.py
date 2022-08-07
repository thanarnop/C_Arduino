from glob import glob
import re
import paho.mqtt.client as mqtt
from threading import Thread
import json
import time
import signal
import sys

client = mqtt.Client()
subTopic1 = "PLC/ChargeRS/"  # Topic to subscribe
subTopic2 = "PLC/ChargeRS2/"  # Topic to subscribe

host = "192.168.250.3"
port = 1800


def signal_handler(sig, frame1e):
    global _break
    print('You pressed Ctrl+C!')
    _break = 1
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)



def on_connect(self, cliend, userdata, rc):
    global subTopic
    print("Connected to Broker")
    self.subscribe(subTopic1)  # Topic1
    self.subscribe(subTopic2)  # Topic2


def on_message(cliend, userdata, msg):
    data = msg.payload.decode("utf-8", "strict")
    print(data)
    
client.on_connect = on_connect
client.on_message = on_message
client.connect(host, port)
client.loop_forever()