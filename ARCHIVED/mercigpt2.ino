// Encoder pins
const int pinA = 2;  // Encoder output A
const int pinB = 3;  // Encoder output B

volatile long encoderPosition = 0;
volatile bool lastAState;

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