#include <Arduino.h>

void setup() {
  Serial.begin(9600); // Inicia la comunicación serial a 9600 baudios
}

void loop() {
  // Envía variables a la Raspberry Pi
  int variable1 = 42;
  float variable2 = 3.14;
  // Envía las variables como texto
  Serial.print("Variable1: ");
  Serial.println(variable1);
  Serial.print("Variable2: ");
  Serial.println(variable2);
  delay(1000);
}