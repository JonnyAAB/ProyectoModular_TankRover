// Programa de muestra para la ESP32 - Parpadeo de LED

// Incluye la biblioteca necesaria
#include <Arduino.h>
#include <ArduinoJson.h>

// Define el pin del LED incorporado en la placa ESP32
const int ledPin = 2; // Pin 2 en la mayoría de las placas ESP32

void setup() {
  // Inicializa el pin del LED como una salida
  Serial.begin(9600);  // Inicia la comunicación serial a 9600 baudios
  Serial.println("Hola, mundo!");  // Envía la cadena de texto a la computadora

  pinMode(ledPin, OUTPUT);
}

void loop() {
  // Enciende el LED
if (Serial.available() > 0) {
    // Lee los datos disponibles en el puerto serial
    String jsonData = Serial.readStringUntil('\n');

    // Parsea la cadena JSON
    StaticJsonDocument<200> jsonDoc;
    DeserializationError error = deserializeJson(jsonDoc, jsonData);

    if (error) {
      Serial.print("Error al analizar JSON: ");
      Serial.println(error.c_str());
    } else {
      // Procesa los datos JSON
      float u1 = jsonDoc["u1"];
      float u2 = jsonDoc["u2"];
      float direccion1 = jsonDoc["direccion1"];
      float direccion2 = jsonDoc["direccion2"];

      // Realiza acciones con los datos recibidos, por ejemplo, imprimirlos
      Serial.print("Dato del sensor 1: ");
      Serial.println(u1);
      Serial.print("Dato del sensor 2: ");
      Serial.println(u2);
      Serial.print("Dato de la direccion 1: ");
      Serial.println(direccion1);
      Serial.print("Dato de la direccion 2: ");
      Serial.println(direccion2);
    }
  }
}