/*
 Interface to Shinyei Model PPD42NS Particle Sensor
 Program by Christopher Nafis 
 Written April 2012
 
 http://www.seeedstudio.com/depot/grove-dust-sensor-p-1050.html
 http://www.sca-shinyei.com/pdf/PPD42NS.pdf
 
 JST Pin 1 (Black Wire)  => Arduino GND
 JST Pin 3 (Red wire)    => Arduino 5VDC
 JST Pin 4 (Yellow wire) => Arduino Digital Pin 8
 */
#include <FileIO.h>

int pin = 8;
unsigned long duration;
unsigned long starttime;
unsigned long sampletime_ms = 30000;
unsigned long lowpulseoccupancy = 0;
float ratio = 0;
float concentration = 0;

void setup() {
  Bridge.begin();
  Serial.begin(9600);
  FileSystem.begin();
  pinMode(8,INPUT);
  starttime = millis();
}

void loop() {
 
    duration = pulseIn(pin, LOW);
    lowpulseoccupancy = lowpulseoccupancy+duration;
  
    if ((millis()-starttime) > sampletime_ms)
    {
      File dataFile = FileSystem.open("/mnt/sda1/script_py/shinyei_PM10", FILE_WRITE);
      if(dataFile)
      {
        ratio = lowpulseoccupancy/(sampletime_ms*10.0);  // Integer percentage 0=>100
        concentration = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62; // using spec sheet curve
        Serial.print(lowpulseoccupancy);
        Serial.print(",");
        Serial.print(ratio);
        Serial.print(",");
        Serial.println(concentration);
        Serial.flush();
        
        //dataFile.print(lowpulseoccupancy);
        //dataFile.print(",");
        //dataFile.print(ratio);
        //dataFile.print(",");
        //dataFile.println("sdfad");
        dataFile.print(concentration);
        //dataFile.println(count);
        //dataFile.println("sdfad");
        dataFile.flush();
        dataFile.close();
        //dataFile.print("\n");
        //dataFileLog.print("\n");
        
        lowpulseoccupancy = 0;
        starttime = millis();
      }
      else
      {
         Serial.println("Error opening file!!");
         Serial.flush();
         delay(3000); 
      }
    }
   
}
