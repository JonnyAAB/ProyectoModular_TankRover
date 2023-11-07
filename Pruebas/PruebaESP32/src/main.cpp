#include <Arduino.h>

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String receivedData = Serial.readStringUntil('\n'); // Lee los datos hasta encontrar una nueva línea
    Serial.println("Datos recibidos: " + receivedData);

    // Analiza los datos JSON
    // Asegúrate de incluir la biblioteca JSON adecuada
    // (puedes usar la biblioteca "ArduinoJson" para analizar datos JSON)
  }
}
