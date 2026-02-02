// Encoder pins
const int pinA = 2;  // Encoder output A
const int pinB = 3;  // Encoder output B
const int pinP = A0;  // Pression meter

volatile long encoderPosition = 0;
volatile bool lastAState;
volatile int pressure;

void setup() {
  pinMode(pinA, INPUT);
  pinMode(pinB, INPUT);
  
  // Read initial state
  lastAState = digitalRead(pinA);
  pressure = analogRead(pinP);

  // Attach interrupt for pin A
  attachInterrupt(digitalPinToInterrupt(pinA), updateEncoder, CHANGE);

  Serial.begin(9600);
}

void loop() {
  // Print the encoder position
  Serial.print(pressure);
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