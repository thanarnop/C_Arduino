void setup() {
  //Port 11
  pinMode(LED_BUILTIN,OUTPUT);
  pinMode(7,INPUT);
  Serial.begin(115200);
  Serial3.begin(9600);
  Serial2.begin(9600,SERIAL_7E2);
}

String sendData = "";
bool perfect = false;
unsigned long prev_mill = 0;
void loop() {
  if(digitalRead(7)==LOW){
    sendData = "12345";
  }
  if(Serial3.available()){
     byte c = Serial3.read();
     if(c != '\n' && c != '*' && c != 0x0A){
      sendData = sendData + String(c,HEX);
      if(perfect){
      Serial2.write(char(c));
      Serial.print(c,HEX);
      }
      }
    if(c == '*'){
      Serial.println("");
      //Serial2.print(sendData);
      Serial.println("send data lengt:"+String(sendData.length()));
      if(sendData.length() == 49){
        perfect = true;
      }else{
        perfect = false;
      }
      sendData = "";
      //delay(200);
    }
  }
}
