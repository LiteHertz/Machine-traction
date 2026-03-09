// ===== Encoder Pins =====
const int pinA = 2; // Encoder output A (White wire on board (encoder section))
const int pinB = 3; // Encoder output B (Green wire on board (encoder section))

// ===== Analog Pin =====
const int pressurePin = A0; // Pressure meter (Green wire on board (pressure section))

// ===== Encoder Variables =====
volatile long encoderPosition = 0;
volatile bool lastAState;

// ===== Sampling =====
const unsigned long sampleInterval = 2; // milliseconds (500 Hz)
unsigned long lastSampleTime = 0;

// ===== Filtering =====
// float filteredPressure = 0;
// const float alpha = 0.1;  // 0 < alpha < 1 (lower = smoother)

// ===== Setup =====
void setup() {
  pinMode(pinA, INPUT);
  pinMode(pinB, INPUT);

  lastAState = digitalRead(pinA);
  attachInterrupt(digitalPinToInterrupt(pinA), updateEncoder, CHANGE);

  Serial.begin(115200);
}

// ===== Main Loop =====
void loop() {

  unsigned long now = millis();

  if (now - lastSampleTime >= sampleInterval) {
    lastSampleTime += sampleInterval;  // avoids drift

    uint16_t rawPressure = analogRead(pressurePin);

    // IIR Low-pass filter
    // filteredPressure = alpha * rawPressure + (1 - alpha) * filteredPressure;
    // Commented out for testing, can be re-enabled if needed
    // To renable the filter, uncomment the above lines and change the sendPacket line to use filteredPressure instead of rawPressure
    // The line should look like this: sendPacket(encoderPosition, now, (uint16_t)filteredPressure);

    sendPacket(now, rawPressure, encoderPosition);
    // Ordre des packets: timestamp, pressure, encoder position
  }
}

// ===== Send Binary Packet =====
void sendPacket(unsigned long timestamp, uint16_t pressure, long encoder) {

  uint8_t startByte = 0xAA;

  Serial.write(startByte);
  Serial.write((uint8_t*)&timestamp, sizeof(timestamp));
  Serial.write((uint8_t*)&pressure, sizeof(pressure));
  Serial.write((uint8_t*)&encoder, sizeof(encoder));

}

// ===== Encoder ISR =====
void updateEncoder() {
  bool A = digitalRead(pinA);
  bool B = digitalRead(pinB);

  if (A != lastAState) {
    if (A == B) {
      encoderPosition++;
    } else {
      encoderPosition--;
    }
  }

  lastAState = A;
}