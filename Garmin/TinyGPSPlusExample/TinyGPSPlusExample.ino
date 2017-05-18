#include <TinyGPS++.h>
#include <SoftwareSerial.h>

// The RX Pin and TXPin
static const int RXPin = 4, TXPin = 3;

// The Serial Baudrate
static const uint32_t GPSBaud = 4800;

// The TinyGPS++ object
TinyGPSPlus gps;

// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);

// Garmin NMEA0183-information from Manual
/*
 * Sending:
 * SDDPT = Depth
 * SDDBT = Depth under Transducer
 * Receiving:
 * DPT = Depth
 * DBT = Depth under Transducer
 */
TinyGPSCustom depth(gps, "SDDPT", 18); // $GPGSA sentence, 18th element

void setup() 
{
  Serial.begin(115200);
  ss.begin(GPSBaud);

  Serial.println(F("TinyGPSPlusExample.ino"));
  Serial.println(F("Testing Garmin Device to read Depth"));
  Serial.print(F("Testing TinyGPS++ library v. ")); Serial.println(TinyGPSPlus::libraryVersion());
  Serial.println(F("by Boris van Norren"));
  Serial.println();
}

void loop() 
{
  // Every time anything is updated, print everything.
  if (gps.altitude.isUpdated() || gps.satellites.isUpdated() ||
    pdop.isUpdated() || hdop.isUpdated() || vdop.isUpdated())
  {
    //ALT = Test value
    Serial.print(F("testALT="));   Serial.print(gps.altitude.meters()); 
    //DEPTH = Wanted value
    Serial.print(F("DEPTH=")); Serial.print(depth.value());
    //SATS = Test value
    Serial.print(F("testSATS=")); Serial.println(gps.satellites.value());
  }

  while (ss.available() > 0)
    gps.encode(ss.read());
}

