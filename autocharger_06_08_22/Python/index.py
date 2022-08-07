from glob import glob
import re
import paho.mqtt.client as mqtt
from threading import Thread
import serial
import json
import time
import signal
import sys

client = mqtt.Client()
subTopic = "Charger/"  # Topic to sen
pubTopic1 = "PLC/ChargeRS/1"
pubTopic2 = "PLC/ChargeRS/2"
host = "192.168.1.81"
port = 1800

unit1 = ""
unit2 = ""

ReadCMD1 = ""
ReadCMD2 = ""

VoltCMD1 = ""
VoltCMD2 = ""

AmpCMD1 = ""
AmpCMD2 = ""

ChargerCMD1 = ""
ChargerCMD2 = ""

ChargerReset1 = ""
ChargerReset2 = ""

amp1 = ""
volt1 = ""

amp2 = ""
volt2 = ""
alerm1 = ""
alerm2 = ""
relay2 = ""
ready2 = ""
text2 = ""

relay1 = ""
ready1 = ""
text1 = ""

rd1 = ""
rd2 = ""
full = 0
last_millis = 0
_break = 0
i = 0

def signal_handler(sig, frame1e):
    global _break
    print('You pressed Ctrl+C!')
    _break = 1
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def s1():
    global i
    time.sleep(1)
    i = i + 1


def Port():
        global unit1, unit2, ReadCMD1, ReadCMD2, VoltCMD1, VoltCMD2, AmpCMD1, AmpCMD2 , text1 , full
        global relay1 , amp1 , volt1 , rd1,rd2
        global relay2 , amp2 , volt2 ,alerm1, alerm2
        try:
            ser1 = serial.Serial("/dev/ttyACM1",baudrate=115200, write_timeout=None)
            ser2 = serial.Serial("/dev/ttyACM0",baudrate=115200, write_timeout=None)
            
           
            data1 = ser1.readline()
            data1 = data1.decode()
            data1 = data1.split()

            data2 = ser2.readline()
            data2 = data2.decode()
            data2 = data2.split()
            frame1 = data1[0]
            frame2 = data2[0]
            if frame1 == "48A" :
                    #print(data)
                    amp1 = data1[2]
                    volt1 = data1[3]
                    alerm1 = data1[4]
                    amp1 = int(amp1,16)
                    volt1 = int(volt1,16)
                    amp1 = amp1 / 256
                    volt1 = volt1 / 1024
                    amp1 = str(amp1)
                    volt1 = str(volt1)
                    
            if frame1 == "38A" :
                    relay1 = data1[1]
                    relay1 = str(relay1)
                    if relay1 == "255" :
                        relay1 = "0"
                    else :
                        relay1 = "1"

            if frame2 == "48A" :
                    #print(data)
                    amp2 = data2[2]
                    volt2 = data2[3]
                    alerm2 = data2[4]
                    amp2 = int(amp2,16)
                    volt2 = int(volt2,16)
                    amp2 = amp2 / 256
                    volt2 = volt2 / 1024
                    amp2 = str(amp2)
                    volt2 = str(volt2)
                    
            if frame2 == "38A" :
                    relay2 = data2[1]
                    relay2 = str(relay2)
                    if relay2 == "255" :
                        relay2 = "0"
                    else :
                        relay2 = "1"

            if frame1 == "On":
                rd1 = "0"
            else:
                rd1 = "1"
            if frame2 == "On":
                rd2 = "0"
            else:
                rd2 = "1"

            #all1 = ("CHG1"+","+amp1 +","+volt1+","+relay1+","+rd1) 
            #all2 = ("CHG2"+","+amp2 +","+volt2+","+relay2+","+rd2)
            all1 = ("CHG1"+","+rd1 +","+amp1+","+volt1+","+relay1+","+alerm1) 
            all2 = ("CHG2"+","+rd2 +","+amp2+","+volt2+","+relay2+","+alerm2)       
            print(all1)
            print(all2) 
            client.publish(pubTopic1,all1)
            client.publish(pubTopic2,all2)        
            if full == 1 :
                ser1.write(text1.encode('utf-8'))# Send command to Serial port
                ser2.write(text1.encode('utf-8'))# Send command to Serial port
                full = 0
        except Exception as e :
            pass#print(e)

def main():
    while _break == 0:
        global i , last_millis
        milliseconds = int(round(time.time() * 1000))
        if milliseconds - last_millis > 250:
            Port()
            last_millis = milliseconds

def on_connect(self, cliend, userdata, rc):
    global subTopic
    self.subscribe(subTopic)  # Topic
    th = Thread(target=main)
    th.start()


def on_message(cliend, userdata, msg):
    global jsonData , full , text1
    sh = msg.payload.decode("utf-8", "strict")
    jsonData = json.loads(sh)

    unit1 = jsonData["Charger"][0]["Name"]
    ReadCMD1_1 = jsonData["Charger"][0]["ReadCMD"]

    Volt2CMD_1 = jsonData["Charger"][0]["Volt1CMD"]
    Volt1CMD_1 = jsonData["Charger"][0]["Volt2CMD"]

    Amp2CMD_1 = jsonData["Charger"][0]["Amp1CMD"]
    Amp1CMD_1 = jsonData["Charger"][0]["Amp2CMD"]

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

    #print(jsonData)
    #print(unit1,ReadCMD1_1 ,Volt1CMD_1,Volt2CMD_1,Amp1CMD_1,Amp2CMD_1,ChargerCMD_1,ChargerReset_1)
    #print(unit2,ReadCMD1_2 ,Volt1CMD_2,Volt2CMD_2,Amp1CMD_2,Amp2CMD_2,ChargerCMD_2,ChargerReset_2)

    x = {
    "data1":ReadCMD1_1,
    "volt1":Volt1CMD_1,
    "volt2":Volt2CMD_1,
    "amp1":Amp2CMD_1,
    "amp2":Amp1CMD_1,
    "reset":ChargerReset_1,
    "data4":ChargerCMD_1,
    }
    x = json.dumps(x)
    text1 = x
    text1 = text1 + "*"
    text1 = str(text1)
    print(text1)

    
    full = full + 1
    
client.on_connect = on_connect
client.on_message = on_message
client.connect(host, port)
client.loop_forever()