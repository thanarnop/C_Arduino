import paho.mqtt.client as mqtt

client = mqtt.Client()

Receiver = "PLC/ChargeRS2/"
#Receiver = "Charger/"
host = "192.168.250.3"
port = 1800

def on_connect(self, cliend, userdata , rc):
    global Receiver
    self.subscribe(Receiver)
    print("wait")

def on_message(cliend, userdata,msg):
    sh = msg.payload.decode("utf-8", "strict")
    print(sh)

client.on_connect = on_connect
client.on_message = on_message
client.connect(host, port)
client.loop_forever()
