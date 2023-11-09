// Programa de muestra para la ESP32 - Parpadeo de LED

// Incluye la biblioteca necesaria
#include <Arduino.h>
#include <ArduinoJson.h>

// Define el pin del LED incorporado en la placa ESP32
// Definicion de pines en la ESP32, configurandolo 
const int LPWM1 = 15;    //Cambiar el numero por el numero de pin del ESP32 para el 
const int RPWM1 = 2;    //Cambiar el numero por el numero de pin del ESP32
const int LPWM2 = 4;    //Cambiar el numero por el numero de pin del ESP32
const int RPWM2 = 16;    //Cambiar el numero por el numero de pin del ESP32
const int En = 17;

void setup() {
  // Inicializamos conexion serial
  Serial.begin(9600);  // Inicia la comunicación serial a 9600 baudios

  // Configuramos los pines como salida
  pinMode(RPWM1, OUTPUT);
  pinMode(LPWM1, OUTPUT);
  pinMode(RPWM2, OUTPUT);
  pinMode(LPWM2, OUTPUT);
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

      Serial.print("u1: ");
      Serial.println(u1);
      Serial.print("u2: ");
      Serial.println(u2);

      // Llamamos a la funcion que realiza el control de los motores
      setMotor(u1,RPWM1,LPWM1);
      setMotor(u2,LPWM2,RPWM2);
    }
  }
}
void setMotor(float u, int RPWM, int LPWM)
  {
     analogWrite(RPWM,u);
     analogWrite(LPWM,0);
  }
