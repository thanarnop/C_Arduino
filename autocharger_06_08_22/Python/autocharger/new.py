import serial
import paho.mqtt.client as mqtt
from threading import Thread
import json
import time
import signal
import sys

client = mqtt.Client()
host = "192.168.250.3"
port = 1800

subTopic = "Charger/"  # Topic to sen
pubTopic1 = "PLC/ChargeRS/"
pubTopic2 = "PLC/ChargeRS2/"
serTopic1 = "serial1"
serTopic2 = "serial2"


charger1 = serial.Serial(port="/dev/ttyACM1",baudrate=115200,timeout=.1)
charger2 = serial.Serial(port="/dev/ttyACM0",baudrate=115200,timeout=.1)


def read1():
    data = charger1.readline()
    data = data.decode()
    data = data.split()    
    rd1 = "0"       
    try:
        rd1 = "0"       
        if data[0] == "On":
            rd1 = "1"  
        else:
            rd1 = "0"

        if data[0] == "48A" :
                print("Charger1:",data) 
                amp1 = data[2]
                volt1 = data[3]
                alarm1 = data[4]
                amp1 = int(amp1,16)
                volt1 = int(volt1,16)
                amp1 = amp1 / 256
                volt1 = volt1 / 1024
                amp1 = str(amp1)
                volt1 = str(volt1)
                all1 = ("CHG1"+","+rd1 +","+amp1+","+volt1+","+alarm1) 
                client.publish(pubTopic1,all1)

    except Exception as e:
        print(e)

def read2():
    data = charger2.readline()
    data = data.decode()
    data = data.split()
    try:
        rd1 = "0"       
        if data[0] == "On":
            rd1 = "1"  
        else:
            rd1 = "0"

        if data[0] == "48A" :
                print("Charger2:",data) 
                amp1 = data[2]
                volt1 = data[3]
                alarm1 = data[4]
                amp1 = int(amp1,16)
                volt1 = int(volt1,16)
                amp1 = amp1 / 256
                volt1 = volt1 / 1024
                amp1 = str(amp1)
                volt1 = str(volt1)
                all1 = ("CHG1"+","+rd1 +","+amp1+","+volt1+","+alarm1) 
                client.publish(pubTopic2,all1)
                
    except Exception as e:
        print(e)

def serialRead():
    while True:
        value1 = read1()
        value2 = read2()

def signal_handler(sig, frame1e):
    global _break
    print('You pressed Ctrl+C!')
    _break = 1
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
th = Thread(target=serialRead)

def on_connect(self, cliend, userdata, rc):
    global subTopic
    print("Connected to Broker")
    self.subscribe(subTopic) 
    th.start()


def on_message(cliend, userdata, msg):
    sh = msg.payload.decode("utf-8", "strict")
    jsonData = json.loads(sh)

    unit1 = jsonData["Charger"][0]["Name"]
    ReadCMD1_1 = jsonData["Charger"][0]["ReadCMD"]

    Volt2CMD_1 = jsonData["Charger"][0]["Volt1CMD"]
    Volt1CMD_1 = jsonData["Charger"][0]["Volt2CMD"]

    Amp1CMD_1 = jsonData["Charger"][0]["Amp1CMD"]
    Amp2CMD_1 = jsonData["Charger"][0]["Amp2CMD"]

    ChargerCMD_1 = jsonData["Charger"][0]["ChargeCMD"]
    ChargerReset_1 = jsonData["Charger"][0]["ChargerReset"]

    unit2 = jsonData["Charger"][1]["Name"]
    ReadCMD1_2 = jsonData["Charger"][1]["ReadCMD"]

    Volt1CMD_2 = jsonData["Charger"][1]["Volt1CMD"]
    Volt2CMD_2 = jsonData["Charger"][1]["Volt2CMD"]

    Amp1CMD_2 = jsonData["Charger"][1]["Amp1CMD"]
    Amp2CMD_2 = jsonData["Charger"][1]["Amp2CMD"]

    ChargerCMD_2 = jsonData["Charger"][1]["ChargeCMD"]
    ChargerReset_2 = jsonData["Charger"][1]["ChargerReset"]

    x = {
    "data1":ReadCMD1_1,
    "volt1":Volt1CMD_1,
    "volt2":Volt2CMD_1,
    "amp1":Amp1CMD_1,
    "amp2":Amp2CMD_1,
    "reset":ChargerReset_1,
    "data4":ChargerCMD_1,
    }

    x = json.dumps(x)
    text1 = x
    text1 = text1 + "*"
    text1 = str(text1)
    charger1.write(text1.encode('utf-8'))# Send command to Serial port
    charger2.write(text1.encode('utf-8'))# Send command to Serial port

client.on_connect = on_connect
client.on_message = on_message
client.connect(host, port)
client.loop_forever()