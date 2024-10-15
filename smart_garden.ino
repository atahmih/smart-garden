int greenLight = 2;
int redLight = 3;
int pumpRelay = 4;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(greenLight, OUTPUT);
  pinMode(redLight, OUTPUT);
  pinMode(pumpRelay, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int soilMoisture = analogRead(A0);
  int photoResistor = analogRead(A2);
  Serial.print("Soil Moisture:");
  Serial.println(soilMoisture);
  Serial.print("Light Intensity: ");
  Serial.println(photoResistor);
  if(soilMoisture > 430){
    digitalWrite(redLight, HIGH);
    digitalWrite(greenLight, LOW);
    digitalWrite(pumpRelay, LOW);
  }
  else if(soilMoisture < 100){    
    digitalWrite(redLight, HIGH);
    digitalWrite(greenLight, LOW);
    digitalWrite(pumpRelay, HIGH);
  }
  else{
    digitalWrite(greenLight, HIGH);
    digitalWrite(redLight, LOW);
    digitalWrite(pumpRelay, LOW);
  }
  delay(1000);
  
}
