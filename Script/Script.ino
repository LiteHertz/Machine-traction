// Encoder pins
const int pinA = 2;  // Encoder output A
const int pinB = 3;  // Encoder output B
const int pinP = A0;  // Pression meter

volatile long encoderPosition = 0;
volatile bool lastAState;
volatile int pressureVolts;
volatile int pressureKPa;
volatile unsigned long time;

void setup() {
  pinMode(pinA, INPUT);
  pinMode(pinB, INPUT);
  
  // Read initial state
  lastAState = digitalRead(pinA);


  // Attach interrupt for pin A
  attachInterrupt(digitalPinToInterrupt(pinA), updateEncoder, CHANGE);

  Serial.begin(9600);
}

void loop() {
  // Print the encoder position
  time = millis();
  
  pressureVolts = map(analogRead(pinP), 0, 1023, 0, 5000);
  pressureKPa = map(pressureVolts, 500, 4500, 0, 15000);
  
  Serial.print(time);
  Serial.print(";");
  Serial.print(pressureVolts);
  Serial.print(";");
  Serial.print(pressureKPa);
  Serial.print(";");
  Serial.println(encoderPosition);
  delay(100);
}

void updateEncoder() {
  bool A = digitalRead(pinA);
  bool B = digitalRead(pinB);

  // Determine direction
  if (A != lastAState) {
    if (A == B) {
      encoderPosition++;
    } else {
      encoderPosition--;
    }
  }
  lastAState = A;
}