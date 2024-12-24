#include "Adafruit_Sensor.h"
#include "DHT.h"
#include "DHT_U.h"

#define DHTPIN 5
#define DHTTYPE DHT11

DHT_Unified dht(DHTPIN, DHTTYPE);

#define greenLight 2
#define redLight 3
#define pumpRelay 4


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(greenLight, OUTPUT);
  pinMode(redLight, OUTPUT);
  pinMode(pumpRelay, OUTPUT);
  dht.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  int soilMoisture = analogRead(A0);
  int photoResistor = analogRead(A2);

  // Read temperature
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  float temp = event.temperature;

  // Read humidity
  dht.humidity().getEvent(&event);
  float humidity = event.relative_humidity;
  // Serial.print("Soil Moisture:");
  Serial.print(soilMoisture);
  Serial.print(",");
  Serial.print(photoResistor);
  Serial.print(",");
  
  Serial.print(temp);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  // Pump relay triggers have been inverted
  // due to the hardware wiring of the relay
  if(soilMoisture > 400){
    digitalWrite(redLight, HIGH);
    digitalWrite(greenLight, LOW);
    digitalWrite(pumpRelay, HIGH); //OFF
    Serial.println("OFF");
  }
  else if(soilMoisture < 50){    
    digitalWrite(redLight, HIGH);
    digitalWrite(greenLight, LOW);
    digitalWrite(pumpRelay, LOW); //ON
    Serial.println("ON");
  }
  else{
    digitalWrite(greenLight, HIGH);
    digitalWrite(redLight, LOW);
    digitalWrite(pumpRelay, HIGH); //OFF
    Serial.println("OFF"); 
  }
  delay(10000);
}
