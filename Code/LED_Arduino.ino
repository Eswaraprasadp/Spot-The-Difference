
char serialData;
int pin1 = 2;   
int pin2 = 3;
int pin3 = 4;
int pin4 = 5;
int pin5 = 6;
int pin6 = 7;
int pin7 = 8;
int pin8 = 9;
int pin9 = 10;
int pin10 = 11;
int pin11 = 12;
int pin12 = 13;


void setup() {
  
  Serial.begin(9600);
  pinMode(pin1, OUTPUT);  
  pinMode(pin2, OUTPUT);
  pinMode(pin3, OUTPUT);
  pinMode(pin4, OUTPUT);
  pinMode(pin5, OUTPUT);
  pinMode(pin6, OUTPUT);
  pinMode(pin7, OUTPUT);
  pinMode(pin8, OUTPUT);
  pinMode(pin9, OUTPUT);
  pinMode(pin10, OUTPUT);
  pinMode(pin11, OUTPUT);
  pinMode(pin12, OUTPUT);
  digitalWrite(pin1,LOW); //Off the LEDs initially if they were glowing
  digitalWrite(pin2, HIGH);
  digitalWrite(pin3, HIGH);
  digitalWrite(pin4, HIGH);
  digitalWrite(pin5, LOW);
  digitalWrite(pin6, HIGH);
  digitalWrite(pin7, HIGH);
  digitalWrite(pin8, HIGH);
  digitalWrite(pin9, HIGH);
  digitalWrite(pin10, LOW);
  digitalWrite(pin11, HIGH);
  digitalWrite(pin12, LOW);
  // make the pushbutton's pin an input:
  
}

// the loop routine runs over and over again forever:
void loop() {
      
  if(Serial.available()>0)
  {
    delay(30);
      serialData = Serial.read(); //Read the data freom python in Serial

      //LED 1: Anode: connected to pin1, Cathode: connected to pin2
      //LED 2: Anode: connected to pin1, Cathode: connected to pin3
      //LED 3: Anode: connected to pin1, Cathode: connected to pin4
      //LED 4: Anode: connected to pin5, Cathode: connected to pin6
      //LED 5: Anode: connected to pin5, Cathode: connected to pin7
      //LED 6: Anode: connected to pin5, Cathode: connected to pin8
      //LED 7: Anode: connected to 5V, Cathode: connected to pin9
      //LED 8: Anode: connected to pin10, Cathode: connected to pin11 
      //LED 9: Anode: connected to pin12, Cathode: connected to ground
     // Note: Both LEDs 8 and 9 were connected to arduino itself as there were not enough jumper wires
     
      if(serialData == '1'){  //If else statement to match the serialData ie. the data sent from python with the corresponding LED number
      digitalWrite(pin1,HIGH);
      digitalWrite(pin2, LOW);
      }
      else if (serialData == '2'){
        digitalWrite(pin1,HIGH);
        digitalWrite(pin3, LOW);
      }
      else if (serialData == '3'){
        digitalWrite(pin1,HIGH);
        digitalWrite(pin4, LOW);
      }
      else if (serialData == '4'){
        digitalWrite(pin5, HIGH);
        digitalWrite(pin6, LOW);
      }
      else if (serialData == '5'){
        digitalWrite(pin5, HIGH);
        digitalWrite(pin7, LOW);
      }
      else if (serialData == '6'){
        digitalWrite(pin5, HIGH);
        digitalWrite(pin8, LOW);
      }
      else if (serialData == '7'){
        digitalWrite(pin9, LOW);
      }
      else if (serialData == '8'){
        digitalWrite(pin12, HIGH);
      }
      else if (serialData == '9'){
        digitalWrite(pin10, HIGH);
        digitalWrite(pin11, LOW);
      }
      
  }
    
}
