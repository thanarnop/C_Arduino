#include <SPI.h>
#include "convert.h"
#include "mcp_can.h"
#include <ArduinoJson.h>

StaticJsonDocument<300> doc;
const int SPI_CS_PIN = 17;

MCP_CAN CAN(SPI_CS_PIN);

void setup()
{
  Serial.begin(115200);
  delay(5000);
  while (CAN_OK != CAN.begin(CAN_125KBPS))
  {
    Serial.print("CAN BUS FAILL");
    delay(100);
  }
}

bool heart;
String com;
String show;
String text1;
String text2;
String text3;
String text4;
int data1;

byte volt1;
byte volt2;
byte amp1;
byte amp2;

int data4 = 1;
String command = "0";
char json[] = "";
String relay = "";
String input = "";
String jsonon = "";
unsigned char buf[8];
unsigned char len = 0;
long unsigned int rxId;
unsigned long prev_millis = 0;
unsigned long prev_millis2 = 200;
byte mmt[8] = {0x01, 0x0A , 0, 0, 0, 0, 0, 0};

void loop() {
  while (Serial.available()) {
    char str = Serial.read();

    if (str != '*') {
      input += String(str);
    }
    if (str == '*') {
      //Serial.println(input);
      jsonon = "on";
      command = "0";
      delay(500);
    }
  }

  unsigned long current_millis = millis();
  if (current_millis - prev_millis >= 1000) {
    prev_millis = current_millis;
    if (heart) {
      CAN.sendMsgBuf(0x701, 0x00 , 1, 0x05);
      CAN.sendMsgBuf(0x00, 0, 2 , mmt);
      Serial.println("On" );
      show = "on";
    }

    else {
      Serial.println("off");
      heart = !heart;
      show = "off";
    }
  }

  unsigned long current_millis2 = millis();
  if (current_millis2 - prev_millis2 >= 500) {
    prev_millis2 = current_millis2;
      }
      if (jsonon == "on") {
      DeserializationError error = deserializeJson(doc, input);
      if (error) {
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.f_str());
        return;
      }

      data1 = doc["data1"];
      String _volt1 = doc["volt1"].as<String>();
      String _volt2 = doc["volt2"].as<String>();
      
      byte _v1 = hexToDec(_volt1);
      byte _v2 = hexToDec(_volt2);
      
      volt1 = dectohex(_v1);
      volt2 = dectohex(_v2);
      String _amp1 = doc["amp1"].as<String>();
      String _amp2 = doc["amp2"].as<String>();
      byte _a1 = hexToDec(_amp1);
      byte _a2 = hexToDec(_amp2);
      amp1 = dectohexAmp(_a1);
      amp2 = dectohexAmp(_a2);
      data4 = doc["data4"].as<long>();
      jsonon = "";
      input = "";
      }
      
  if (data4 == 1 && command == "0") {
    //t_volt
    byte enable[8] = {0x2F, 0x00, 0x60, 0x00, 1, 0, 0, 0};
    CAN.sendMsgBuf(0x60A, 0, 8 , enable);
    Serial.println("Enable");
     //    {"data1": 0, "volt1": "14", "volt2": "00", "amp1": "A0", "amp2": "00", "reset": 0, "data4": 0}*
     //    5v 10A
     //    {"data1": 0, "volt1": "6C", "volt2": "00", "amp1": "50", "amp2": "00", "reset": 0, "data4": 1}*
     //    27 V 5A    
    
    byte v[8] = {0x23, 0x71 , 0x22,  0x00,  volt2, volt1, 0x00, 0x00};
    byte a[8] = {0x2B, 0x70 , 0x60,  0x00,  amp1,  amp2,  0x00 , 0x00};
    
    Serial.println("");
    CAN.sendMsgBuf(0x60A, 0, 8 , v);
    CAN.sendMsgBuf(0x60A, 0, 8, a);
    command = "1";
    
  }
  
  if (data4 == 0 && command == "0") {
    byte disible[8] = {0x2F, 0x00, 0x60, 0, 0, 0, 0, 0};
    CAN.sendMsgBuf(0x60A, 0, 8 , disible);
    byte stemp1[8] = {0x23, 0x71, 0x22, 00, 00, 00, 0, 0};
    CAN.sendMsgBuf(0x60A, 0, 8 , stemp1);
    Serial.println("Disible");
    command = "1";
  }


    if (CAN_MSGAVAIL == CAN.checkReceive())
    {
      
      CAN.readMsgBuf(&len, buf);
      unsigned long canId = CAN.getCanId();
      unsigned long total;
      com = String(canId, HEX);
      if (com == "48a") {
        Serial.print(canId, HEX);
        Serial.print(" ");
        Serial.print(len);
        Serial.print(" ");
        text1 = (String(buf[1], HEX)) + (String(buf[0], HEX));
        text2 = (String(buf[3], HEX)) + (String(buf[2], HEX));
        text3 = (String(buf[5], HEX)) + (String(buf[4], HEX));
        Serial.print(text1);
        Serial.print(" ");
        Serial.print(text2);
        Serial.print(" ");
        Serial.println(text3);     
      }
      if (com == "18a") {
       /* Serial.print(canId, HEX);
        Serial.print(" ");
        Serial.print(len);
        Serial.print(" ");
        for (int i = 0; i < len; i++) {
          Serial.print(buf[i], HEX);
          Serial.print("\t");
        }
        text1 = (String(buf[1], HEX)) + (String(buf[0], HEX));
        text2 = (String(buf[2], HEX)) + (String(buf[3], HEX));
        Serial.print(text1);
        Serial.print(" ");
        Serial.println(text2);*/
      }
    }
}
