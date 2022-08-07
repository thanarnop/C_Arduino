#include <SPI.h>
#define CAN_2515
#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#if defined(SEEED_WIO_TERMINAL) && defined(CAN_2518FD)
const int SPI_CS_PIN  = BCM8;
const int CAN_INT_PIN = BCM25;
#else
const int SPI_CS_PIN = 9;
const int CAN_INT_PIN = 2;
#endif

#ifdef CAN_2518FD
#include "mcp2518fd_can.h"
mcp2518fd CAN(SPI_CS_PIN); // Set CS pin
#endif

#ifdef CAN_2515
#include "mcp2515_can.h"
mcp2515_can CAN(SPI_CS_PIN); // Set CS pin
#endif

String Status;
String com;
String data;
String temp1 = "00";
String temp2 = "00";
String soc = "00";
String soh = "00";

String volt = "00"; // use
String voltlow = "00";
String volthigh = "00";

String amp = "00" ;
String amplow = "00";
String amphigh = "00";
String all = "00";

unsigned char stmp[8] = {0, 0, 0, 0, 0, 0, 0, 0};

char start[] = {0xA1,0xF1};
void setup(){
  Serial.begin(115200);
  Serial3.begin(9600);
  //Serial2.begin(9600);
    
  while(!Serial);
  while (CAN_OK != CAN.begin(CAN_250KBPS))    // init can bus : baudrate = 300k
  {
    Serial.println("CAN BUS FAIL!");
    delay(100);
  }
    canbusReadCMD();
    delay(100);   
}

unsigned long prev_millis = 0;
void canbus_send(){
  unsigned long current_millis = millis();
  if(current_millis - prev_millis > 1000){
    prev_millis = current_millis;
    stmp[7] = stmp[7]+1;
    if(stmp[7] == 100){
      stmp[7] = 0;
      stmp[6] = stmp[6] + 1; 
      if(stmp[6] == 100){
        stmp[6] = 0;
        stmp[5] = stmp[6] + 1;
      }
    }
    CAN.sendMsgBuf(0x00, 0, 8, stmp);
  }
}

void canbusReadCMD(){
    stmp[7] = stmp[7]+1;
    if(stmp[7] == 100){
      stmp[7] = 0;
      stmp[6] = stmp[6] + 1; 
      if(stmp[6] == 100){
        stmp[6] = 0;
        stmp[5] = stmp[6] + 1;
      }
    CAN.sendMsgBuf(0x00, 0, 8, stmp);
  }
}

unsigned char len = 0;
unsigned char buf[8];
void loop() {
    //canbus_send();
    if(CAN_MSGAVAIL == CAN.checkReceive()){
        CAN.readMsgBuf(&len, buf);
        unsigned long canId = CAN.getCanId();
        
        com = String(buf[0],HEX);
        if (com == "20"){
          Status = (buf[6]);   
          //Serial.println(String(buf[6],HEX));      
        }        
        if (com == "30"){
          soc = String(buf[2],HEX);
          if(soc.length() == 1){
            soc = "0"+soc;
          }
          soh = String(buf[3],HEX);
  
        }
        
        if (com == "31"){
          volt = String(buf[3],HEX) + String(buf[2],HEX);
          voltlow = String(buf[2],HEX);
          volthigh = String(buf[3],HEX);
          if(voltlow.length()==1){
            voltlow = "0"+voltlow;
          }
          if(volthigh.length()==1){
            volthigh = "0"+volthigh;
          }
          }
          
        if (com == "32"){
          temp1 = String(buf[3],HEX);
          temp2 = String(buf[2],HEX);
          
          if(temp1.length()==1){
          temp1 = "0"+temp1;
          }else{
            temp1 = String(buf[3],HEX);
          }
          
          if(temp2.length()==1){
          temp2 = "0"+temp2;
          }else{
            temp2 = String(buf[2],HEX);
          }
       
        }
        if (com == "33"){ 
         amplow = String(buf[3],HEX);
         amphigh = String(buf[2],HEX);
         if(amplow.length()==1){
          amplow = "0"+amplow;
         }
         if(amphigh.length() == 1){
          amphigh = "0"+amphigh;
         }
         amp  = amplow;
         Serial.println("Amp :"+amp);
        }
        if(all.length() >= 22){
         Serial3.write(start,2);
         Serial3.println(soc+"/");
         delay(300);
          
         Serial3.write(start,2);
         Serial3.println(soh+"/");
         delay(300);

         Serial3.write(start,2);
         Serial3.println(amplow+"/");
         delay(300);
         
         Serial3.write(start,2);
         Serial3.println(amphigh+"/");
         delay(300);
          
         Serial3.write(start,2);
         Serial3.println(volthigh+"/");
         delay(300);
          
         Serial3.write(start,2);
         Serial3.println(voltlow+"/");
         delay(300);
          
         Serial3.write(start,2);
         Serial3.println(temp1+"/");
         delay(300);

         Serial3.write(start,2);
         Serial3.println(temp2+"/");
         delay(300);
         
         Serial3.write(start,2);
         Serial3.println("*");
         delay(300);
         Serial.println(all);
         }
        all = (soc+"/"+soh+"/"+amplow+"/"+amphigh+"/"+voltlow+"/"+volthigh+"/"+temp1+"/"+temp2+"/");

     }
}
