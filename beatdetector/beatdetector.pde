
// These constants won't change.  They're used to give names
// to the pins used:
const int analogInPin1 = A0; 
const int analogInPin2 = A1; 
const int analogInPin3 = A2; 
const int analogInPin4 = A3; 

const int analogInPin5 = A4; 
const int analogInPin6 = A5; 
const int analogInPin7 = A6; 
const int analogInPin8 = A7; 

int sensorValue1 = 0;
int sensorValue2 = 0;      
int sensorValue3 = 0;      
int sensorValue4 = 0;      
int sensorValue5 = 0;      
int sensorValue6 = 0;      
int sensorValue7 = 0;      
int sensorValue8 = 0;      

int outputValue = 0;        // value output to the PWM (analog out)

int pin1 = 2;
int pin2 = 3;
int pin3 = 4;
int pin4 = 5;
int pin5 = 6;
int pin6 = 7;
int pin7 = 8;
int pin8 = 9;

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(115200);//19200);
  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
  pinMode(pin3, OUTPUT);
  pinMode(pin4, OUTPUT);
  pinMode(pin5, OUTPUT);
  pinMode(pin6, OUTPUT);
  pinMode(pin7, OUTPUT);
  pinMode(pin8, OUTPUT);


}
void setPin(int val,int pin){
  if(val < 10){
    digitalWrite(pin,LOW);
  }
  else{
    digitalWrite(pin,HIGH);
  } 
}

const int numSamples = 48*4;
void loop(){
  
  int samples[numSamples];
  for(int i = 0; i< numSamples; i++){
    // delay(1);
    delayMicroseconds(10);
    samples[i] = analogRead(analogInPin1);
    //sensorValue1 = analogRead(analogInPin1);         
  }
  //Serial.print("a ");
  for(int i = 0; i< numSamples; i++){

    Serial.print(samples[i]);
    Serial.print(' ');
  }
  Serial.println();

  

}

void loop1() {
  // read the analog in value:
  sensorValue1 = analogRead(analogInPin1);         
  sensorValue2 = analogRead(analogInPin2);            
  sensorValue3 = analogRead(analogInPin3);            
  sensorValue4 = analogRead(analogInPin4);            
  sensorValue5 = analogRead(analogInPin5);            
  sensorValue6 = analogRead(analogInPin6);            
  sensorValue7 = analogRead(analogInPin7);            
  sensorValue8 = analogRead(analogInPin8);            

  setPin(sensorValue1, pin1);
  setPin(sensorValue2, pin2);
  setPin(sensorValue3, pin3);
  setPin(sensorValue4, pin4);
  setPin(sensorValue5, pin5);
  setPin(sensorValue6, pin6);
  setPin(sensorValue7, pin7);
  setPin(sensorValue8, pin8);

  // print the results to the serial monitor:
  Serial.print(sensorValue1);
  Serial.print(" ");
  Serial.print(sensorValue2);      
  Serial.print(" ");
  Serial.print(sensorValue3);      
  Serial.print(" ");
  Serial.print(sensorValue4);      
  Serial.print(" ");
  Serial.print(sensorValue5);      
  Serial.print(" ");
  Serial.print(sensorValue6);      
  Serial.print(" ");
  Serial.print(sensorValue7);      
  Serial.print(" ");
  Serial.println(sensorValue8);      


  // wait 10 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(10);                     
}

