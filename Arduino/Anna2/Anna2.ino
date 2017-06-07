//code running on the arduino microprocessor in the "Anna"
 
#include <Servo.h>

#define INPUT_SIZE 17
#define debug = false

Servo LinkerRoer;
Servo RechterRoer;
Servo LinkerMotor;
Servo RechterMotor;

int threshold = 1400;
int LR=0; //LR=Left Rudder
int RR=0; //rr=Right Rudder
int LM=0; //LM=Left Motor
int LMR=0; 
int RM=0; //RM=Right Motor
int TW=0; 
int takeOverLED = 12;
unsigned long time = 0;
unsigned long time2 = 0;
char input[INPUT_SIZE];
int size=0;
int totaal=0;

bool takeOver = false;

// Kanalen van de ontvanger
// Arduino pins
const int Ch1=A3, // Aileron | Rudder, sturen
          Ch2=A4, // Rudder | Zorgt voor een draai motion
          Ch3=A2, // Throttle | Motor kracht
          Ch5=A1; // Trigger kanaal |  

void setup() 
{
  delay(2000);
  // put your setup code here, to run once:

  pinMode(Ch1,INPUT);
  pinMode(Ch2,INPUT);
  pinMode(Ch3,INPUT);
  pinMode(Ch5,INPUT);
  pinMode(12,OUTPUT);

  Serial.begin(115200);

  LinkerRoer.attach(8);
  RechterRoer.attach(9);
  LinkerMotor.attach(10);
  RechterMotor.attach(11);
  LinkerRoer.write(90); //90 is halfway, or rest position
  RechterRoer.write(90);
  LinkerMotor.write(90);
  RechterMotor.write(90);
  Serial.setTimeout(50);
}
 
void loop() 
{
  RC();
  rpi();
}

void RC()
{
  while(analogRead(A1)>50)
    {  
      takeOver=true;  
      digitalWrite(takeOverLED,HIGH);

      //Rudder
      LR=pulseIn(Ch1,HIGH);    
      LR=map(LR,1000,1850,40,140);
      if (LR>135)
        LR=140;
      if (LR<45)
        LR=40;
      if (LR>80&&LR<100)
        LR=90;      


      //Throttle
      LMR=pulseIn(Ch3,HIGH);
      if (LMR<1000)
        LM=90;
      if(LMR>=1000)
        LM=map(LMR,1000,1850,40,140);
      if (LM>130)
        LM=140;
      if (LM<50 && LM >40) 
        LM=40;
      if (LM>80&&LM<100)
        LM=90;  

      //Turn throttle
      RM=LM;
      TW=pulseIn(Ch2,HIGH);
      TW=map(TW,1000,1850,40,140);
      if (TW>100 && LMR>=1000)
      {
        RM=RM-TW+90;
        LM=LM+TW-90;
      }
      if (TW<80&& LMR>=1000)
      {
        LM=LM+TW-90;
        RM=RM-TW+90;
      }

      LinkerRoer.write(LR);
      RechterRoer.write(LR);
      LinkerMotor.write(RM);
      RechterMotor.write(LM);
 
      while (Serial.available()>0)
        Serial.read();

    } 
    
    digitalWrite(takeOverLED,LOW);
 
    if(takeOver==true)
      {
        LinkerRoer.write(90);
        RechterRoer.write(90);
        LinkerMotor.write(90);
        RechterMotor.write(90); 
        takeOver=false;
      }
}

void rpi()
{
  if (Serial.available()>0) //if there is something in the serial buffer
  { 
    if (Serial.peek()=='a') //if this something starts with "a"
    {
      Serial.read(); //remove first byte ("a") from the serial buffer
      size=Serial.readBytesUntil('z',input,INPUT_SIZE); //read bytes untill "z"
      input[size]='z'; //make the last char in the string a "z"

      //The following code parses a string of the following format to 4 values:
      //"a(int)b(int)c(int)d(int)z" eg. "a90b100c110d120z" becomes 90, 100, 110, 120

      char* command = strtok(input,"b"); 
      LR=atoi(command);
      LR=constrain(LR,40,140);
      command=strtok(0,"c");
      RR=atoi(command);
      RR=constrain(RR,40,140);
      command=strtok(0,"d");
      LM=atoi(command);
      LM=constrain(LM,40,140);
      command=strtok(0,"z");
      RM=atoi(command);
      RM=constrain(RM,40,140);

      //the received values are then written to the 4 outputs
      LinkerRoer.write(LR);
      RechterRoer.write(RR);
      LinkerMotor.write(LM);
      RechterMotor.write(RM);

      //the program then echoes the received commands back to the sender over serial interface
      if(debug)
      {
        Serial.print('a');
        Serial.print(LR);
        Serial.print('b');
        Serial.print(RR);
        Serial.print('c');  
        Serial.print(LM);
        Serial.print('d');  
        Serial.print(RM);
        Serial.print('z');   
      }
      
    }
    else
    {
      //if there is something not starting with an "a" in the buffer, discard it
      while((Serial.available()>0)&&(Serial.peek()!='a'))
        Serial.read();
    }
  }
}

