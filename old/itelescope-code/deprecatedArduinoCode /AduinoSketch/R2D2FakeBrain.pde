/*
  This is a modification of the "Analog input, analog output, serial output"
  sketch for telescope RA, Dec control using two potentiometers measuring 
  ALT/AZ.
 
 created 23 Jan. 2011
 by Simon Box
  
 */
 
//includes
#include <LiquidCrystal.h>
#include "Observer.h";
#include "Angle.h";
#include "Coordinates.h";
#include "DateTime.h";
#include "Time.h";
#include "MeanCutFilter.h";
#include <Time.h>

#define TIME_MSG_LEN  11   // time sync to PC is HEADER followed by Unix time_t as ten ASCII digits
#define TIME_HEADER  'T'   // Header tag for serial time sync message
#define TIME_REQUEST  7    // ASCII bell character requests a time sync message 

// These constants won't change.  They're used to give names
// to the pins used:
const int AzPin = A3;  // Analog input pin that AZ potentiometer is attached to
const int AltPin = A4;  // Analog input pin that ALT potentiometer is attached to

Observer Me;
Angle RA;
Angle DE;
Angle ALT;
Angle AZ;

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  pinMode(A0,OUTPUT);
  pinMode(A1,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(10,OUTPUT);
  
  //inputs
  pinMode(AzPin,INPUT);
  pinMode(AltPin,INPUT);
  
  //set Az + Alt resistor voltage
  digitalWrite(8,LOW);
  digitalWrite(7,LOW);
  digitalWrite(9,LOW);
  digitalWrite(10,LOW);
  
  //turn on lcd backlight
  digitalWrite(A0,LOW);
  digitalWrite(A1,HIGH);
  
  //analog reference
  analogReference(EXTERNAL);
  
  // set up the LCD's number of columns and rows: 
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("Starting...");
  
  //set telescope location and time.
  Angle Lat = AngleDegs(48,51,36);//hardcode location to Noss May
  Angle Long = AngleDegs(-2,-20,-24);
  Me = Observer(Lat,Long);
  //Coordinates Nav;
  setTime(18,32,22,24,9,2011);
  
  // initialize serial communications at 9600 bps:
  Serial.begin(9600); 
  delay(100);// allow analog pins to settle after being set.
}

void loop() {
  
  if(Serial.available() ) 
  {
    processSyncMessage();
  }
  
  DateTime Tnow = DateTime(year(),month(),day(),hour(),minute(),second());
  Me.UpdateTime(Tnow);
  Coordinates Nav = Coordinates(Me); 
  
  int sen0List[10];
  int sen1List[10];
  
  for(int i=0;i<6;i++)
  {
  delay(10);
  sen0List[i] = analogRead(AzPin);
  sen1List[i] = analogRead(AltPin);
  }
  
  MeanCutFilter MCF(5001);
  int sensor0Value = MCF.Filter(sen0List,10);
  int sensor1Value = MCF.Filter(sen1List,10);
  
  double Normer =2*M_PI/1023;
  AZ = AngleRads(sensor0Value*Normer);
  ALT = AngleRads(sensor1Value*Normer);
  
  Nav.SetAzAlt(AZ,ALT);
  
  
  
  // print the results to the serial monitor:
  Serial.print("[RA_int,DE_int] =[ " );                       
  Serial.print(Nav.Ra.radians,5);
  lcd.setCursor(0, 0);
  lcd.print("Ra:");
  lcd.print(Nav.Ra.HrsMinsSecs.Hours);lcd.print("h");
  lcd.print(Nav.Ra.HrsMinsSecs.Minutes);lcd.print("m");
  lcd.print(Nav.Ra.HrsMinsSecs.Seconds,2);lcd.print("s");
  lcd.setCursor(0, 1);
  lcd.print("De:");
  //lcd.print(Tnow.Hour);lcd.print("h");
  //lcd.print(Tnow.Minute);lcd.print("m");
  //lcd.print(Nav.TimeAndLoc.Time.Seconds);lcd.print("s");
  lcd.print(sensor0Value);
  //lcd.print(Nav.Dec.DegsMinsSecs.Degrees);lcd.print("d");
  //lcd.print(Nav.Dec.DegsMinsSecs.Minutes);lcd.print("m");
  //lcd.print(Nav.Dec.DegsMinsSecs.Seconds,2);lcd.print("s");
  Serial.print(", ");      
  Serial.print(Nav.Dec.radians,5);
  Serial.println("];;;");
  /*Serial.print("Time: ");
  Serial.print(Tnow.Hour);
  Serial.print(", ");
  Serial.print(Tnow.Minute);
  Serial.print(", ");
  Serial.print(Tnow.Seconds);
  Serial.print(", ");
  Serial.println(";");*/

  // wait 10 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(10);                     
}

void processSyncMessage() {
  // if time sync available from serial port, update time and return true
  while(Serial.available() >=  TIME_MSG_LEN ){  // time message consists of header & 10 ASCII digits
    char c = Serial.read() ; 
    Serial.print(c);  
    if( c == TIME_HEADER ) {       
      time_t pctime = 0;
      for(int i=0; i < TIME_MSG_LEN -1; i++){   
        c = Serial.read();          
        if( c >= '0' && c <= '9'){   
          pctime = (10 * pctime) + (c - '0') ; // convert digits to a number    
        }
      }   
      setTime(pctime);   // Sync Arduino clock to the time received on the serial port
    }  
  }
}
