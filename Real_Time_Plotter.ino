// max30100
#include <Wire.h>
#include "MAX30100_PulseOximeter.h"
#define REPORTING_PERIOD_MS     1000
#pragma pack(pop)

PulseOximeter pox;
uint32_t tsLastReport = 0;
 
void onBeatDetected()
{
//    Serial.println("Beat!");
}




void setup() 
{
   
  Serial.begin(9600);
 

  // max30100
//    Serial.print("Initializing pulse oximeter..");

    if (!pox.begin()) {
//        Serial.println("FAILED");
        for(;;);
    } else {
//        Serial.println("SUCCESS");
    }
     pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);
 
    // Register a callback for the beat detection
    pox.setOnBeatDetectedCallback(onBeatDetected);
  
}





void loop() 
{

 // max30100    
    pox.update();
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) { 

//        Serial.print("Heart rate:");
        Serial.println(pox.getHeartRate());
//        Serial.println("  bpm");

//        Serial.print("SpO2:  ");
//        Serial.print(pox.getSpO2());
//        Serial.println("  %");
        
        tsLastReport = millis();
    }



////////////////////////////////////////////////////////////////////////////////////////////////////////




 

  
///////////////////////////////////////////////////////////////////////////////////////////////////

 


   
   
/*
 Serial.print("age  ");
 Serial.println(ageInt);
 Serial.println("");
 delay(500);
 Serial.print("wieght ");
 Serial.println(weightInt);
  delay(500);
Serial.print("gender ");
Serial.println(gender);
Serial.println("");
  delay(500);
 Serial.print("Time ");
 Serial.println(timed);
 delay(500);
 delay(1000);
 

  */ 

 // Serial.print("Time ");
  //Serial.println(timed);
 
 
}
