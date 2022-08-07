
from turtle import pu
import paho.mqtt.client as mqtt
import json
import time

Receiver = "Charger/"
host = "192.168.1.81"
port = 1800


client = mqtt.Client()
client.connect(host,port)

def s1() :
    time.sleep(3)

box = '{"Charger":[{"Name":"CHG1",'+\
                    '"ReadCMD":0,'+\
                    '"Volt1CMD":"00",'\
                    '"Volt2CMD":"60",'\
                    '"Amp1CMD":"00",'\
                    '"Amp2CMD":"f0",'\
                    '"ChargeCMD":0,'\
                    '"ChargerReset":1}'\
                    ',{"Name":"CHG2","ReadCMD":0,"Volt1CMD":"00","Volt2CMD":"3C","Amp1CMD":"00","Amp2CMD":"05","ChargeCMD":1,"ChargerReset":0}]}'

while True :
    client.publish(Receiver,box)
    print("sending : ",box)
    s1()