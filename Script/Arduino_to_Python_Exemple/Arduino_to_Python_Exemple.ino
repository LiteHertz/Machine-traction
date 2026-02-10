const int redLight = 2;
const int intLight = 13;
const int button = 6;
int cnt = 0;

void setup() {
  Serial.begin(115200);
  pinMode(redLight, OUTPUT);
  pinMode(intLight, OUTPUT);
  pinMode(button, INPUT_PULLUP);
}

void loop() {
  if (Serial.available() > 0){        //  Regarde s'il y a un message dans le serial
    String msg = Serial.readString(); //  Lit le message
    if (msg == "ON"){
      digitalWrite(intLight, HIGH);
    }
    else if (msg == "OFF"){
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
  int toggle = digitalRead(button);
  if (toggle < 1){
    Serial.println("toggle");
  }
  else{
    Serial.println("not toggle");
  }
  delay(100);
}