const int redLight = 2;
const int intLight = 13;

void setup() {
  Serial.begin(9600);
  pinMode(redLight, OUTPUT);
  pinMode(intLight, OUTPUT);
}

void loop() {
  if (Serial.available() > 0){        //  Regarde s'il y a un message dans le serial
    String msg = Serial.readString(); //  Lit le message

    if (msg == "ON" or "On" or "on"){
      digitalWrite(intLight, HIGH);
    }
    else if (msg == "OFF" or "Off" or "off")
      digitalWrite(intLight, LOW);
    }
    else {
      for (int i = 0; i < 5; i++){
        digitalWrite(redLight, HIGH);
        delay(100);
        digitalWrite(redLight, LOW);
        delay(100);
      }
    }
  }
}