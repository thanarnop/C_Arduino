from glob import glob
import paho.mqtt.client as mqtt
from threading import Thread
import serial
import json
import time
import signal
import sys

charger1_state = ["",""]
charger2_state = ["",""]

client = mqtt.Client()
subTopic = "Charger/"  # Topic to sen
pubTopic = "PLC/ChargeRS/"
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

relay2 = ""
ready2 = ""
text2 = ""

relay1 = ""
ready1 = ""
text1 = ""

check1 = ""
check2 = ""
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
        global relay1 , amp1 , volt1 
        global relay2 , amp2 , volt2 ,charger1_state ,charger2_state
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
                    amp1 = data1[7]
                    volt1 = data1[8]
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
                    #print(data2)
                    amp2 = data2[7]
                    volt2 = data2[8]
                    amp2 = int(amp2,16)
                    volt2 = int(volt2,16)
                    amp2 = amp2 / 256
                    volt2 = volt2 / 1024
                    amp2 = str(amp2)
                    volt2 = str(volt2)
                    if charger2_state[0] != "48A":
                            charger2_state[0] = "48A"

            if frame2 == "38A" :
                    relay2 = data2[1]
                    relay2 = str(relay2)
                    if relay2 == "255" :
                        relay2 = "0"
                    else :
                        relay2 = "1"
                    if charger2_state[1] != "38A":
                            charger2_state[1] = "38A"

            all1 = ("unit1"+","+amp1 +","+volt1+","+relay1) 
            all2 = ("unit2"+","+amp2 +","+volt2+","+relay2)
            #print(all1)
            #print(all2) 
        
            client.publish(pubTopic,all1)
            client.publish(pubTopic,all2)        
            if full == 1 :
                ser1.write(text1.encode('utf-8'))
                ser2.write(text1.encode('utf-8'))
                print(text1)
                full = 0
        except Exception as e :
            pass

def check_charger2_state():
    global charger2_state
    print(charger2_state)
    try:
        if  charger2_state[0] == '48A' and charger2_state[1] == '38A':
            print("charger2 ready")
        else:
            print("charger2 not ready")
    except Exception as e:
        pass

def main():
    while _break == 0:
        global i , last_millis
        milliseconds = int(round(time.time() * 1000))
        if milliseconds - last_millis > 250:
            Port()
            last_millis = milliseconds
            check_charger2_state()

        #s1()


def on_connect(self, cliend, userdata, rc):
    global subTopic
    self.subscribe(subTopic)  # Topic#
    th = Thread(target=main)
    th.start()


def on_message(cliend, userdata, msg):
    global jsonData , full , text1
    sh = msg.payload.decode("utf-8", "strict")
    jsonData = json.loads(sh)
    unit1 = jsonData["Charger"][0]["Name"]
    unit2 = jsonData["Charger"][1]["Name"]

    ReadCMD1 = jsonData["Charger"][0]["ReadCMD"]
    ReadCMD2 = jsonData["Charger"][1]["ReadCMD"]

    VoltCMD1 = jsonData["Charger"][0]["VoltCMD"]
    VoltCMD2 = jsonData["Charger"][1]["VoltCMD"]

    AmpCMD1 = jsonData["Charger"][0]["AmpCMD"]
    AmpCMD2 = jsonData["Charger"][1]["AmpCMD"]

    ChargerCMD1 = jsonData["Charger"][0]["ChargeCMD"]
    ChargerCMD2 = jsonData["Charger"][1]["ChargeCMD"]

    ChargerReset1 = jsonData["Charger"][0]["ChargerReset"]
    ChargerReset2 = jsonData["Charger"][1]["ChargerReset"]
    
    #print(unit1, ReadCMD1, VoltCMD1, AmpCMD1, ChargerCMD1, ChargerReset1)
    #print(unit2, ReadCMD2, VoltCMD2, AmpCMD2, ChargerCMD2, ChargerReset2)


    Ready = ReadCMD1
    datavolt = int(VoltCMD1)
    dataamp = int(AmpCMD1)

    voltc = datavolt
    ampc = dataamp
    
    enable = ChargerCMD1
    voltc = (voltc * 1024)
    ampc = (ampc * 256)
    
    voltc = hex(voltc)
    ampc = hex(ampc)
    
    voltc = str(voltc)
    ampc = str(ampc)        
    
    x = {
    "data1": 0,
    "data2": voltc,
    "data3": ampc,
    "data4": enable
    }
    x = json.dumps(x)
    
    text1 = x
    text1 = text1 + "*"
    text1 = str(text1)
    
    full = 1
client.on_connect = on_connect
client.on_message = on_message
client.connect(host, port)
client.loop_forever()