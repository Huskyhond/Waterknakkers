////http://kingtidesailing.blogspot.nl/2015/09/how-to-connect-any-nmea-0183-device-to.html
//Receive
//DPT = Depth
//DBT = Depth below Transducer
//Transmit
//SDBPT = Depth
//SDDBT = Depth below Transducer
//TX = Blue
//RX = Brown

//#include <PString.h>
#include <SoftwareSerial.h>  
#include <nmea.h>  
   
 SoftwareSerial nmeaSerial(19,18,true); // RX pin, TX pin (not used), and true means we invert the signal  
 NMEA nmeaDecoder(ALL);   
   
 void setup()  
 {  
    Serial.begin(4800);
    nmeaSerial.begin(4800);
 }  
   
 void loop()  
 {  
    if (nmeaSerial.available() > 0 ) {  
      if (nmeaDecoder.decode(nmeaSerial.read())) {  
        Serial.println(nmeaDecoder.sentence());  
      }  
    }

//  if (Serial2.available()) {  
//    if (nmeaDecoder.decode(Serial2.read())) {
//      char* title = nmeaDecoder.term(0);  
//      if (strcmp(title,"SDDBT") == 0) {            // only run the following code if the incoming sentence is MTW  
//        Serial.println(nmeaDecoder.sentence());     // prints the original in Celsius  
//        float depth = atof(nmeaDecoder.term(1));     // declares a float from a string   
//   
//        // Time to assemble the sentence  
//        char mtwSentence [18];                      // the MTW sentence can be up to 18 characters long  
//        byte cst;  
//        PString strt(mtwSentence, sizeof(mtwSentence));  
//        strt.print("SDDBT,");  
//        strt.print(depth);  
//        strt.print(",M");  
//        cst = checksum(mtwSentence);  
//        if (cst < 0x10) strt.print('0');            // Arduino prints 0x007 as 7, 0x02B as 2B, so we add it now  
//          strt.print(cst, HEX);  
//          Serial.println(mtwSentence);  
//        }  
//    }  
//  }
 }

// calculate checksum function (thanks to https://mechinations.wordpress.com)  
byte checksum(char* str)   
{  
  byte cs = 0;   
  for (unsigned int n = 1; n < strlen(str) - 1; n++)   
  {  
    cs ^= str[n];  
  }  
  return cs;  
} 
