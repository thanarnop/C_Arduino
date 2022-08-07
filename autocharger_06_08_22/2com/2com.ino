
#include "convert.h" 
String data1 = "078F";
char databuf[16];
void setup() {
  Serial.begin(115200);

}



void loop(){
   Serial.println(two_complement("078F",databuf));
   delay(500);
}
