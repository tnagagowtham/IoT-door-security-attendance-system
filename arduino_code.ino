#include <Servo.h>

Servo doorServo;

void setup() {
  Serial.begin(9600);
  doorServo.attach(9);
  doorServo.write(0);
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();
    if (command == 'o') {
      for (int pos = 0; pos <= 90; pos++) {
        doorServo.write(pos);
        delay(20);
      }
      delay(2000);
    } 
    else if (command == 'c') {
      for (int pos = 90; pos >= 0; pos--) {
        doorServo.write(pos);
        delay(20);
      }
      delay(2000);
    }
  }
}