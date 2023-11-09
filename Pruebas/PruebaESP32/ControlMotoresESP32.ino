// Programa de muestra para la ESP32 - Parpadeo de LED

// Incluye la biblioteca necesaria
#include <Arduino.h>
#include <ArduinoJson.h>

// Definicion de pines en la ESP32, configurandolo 
const int RPWM1 = 2    //Cambiar el numero por el numero de pin del ESP32 para el 
const int LPWM1 = 2    //Cambiar el numero por el numero de pin del ESP32
const int RPWM2 = 2    //Cambiar el numero por el numero de pin del ESP32
const int LPWM2 = 2    //Cambiar el numero por el numero de pin del ESP32
const int En = 2

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
      setMotor(RPWM1,LPWM1,0,0);
      setMotor(LPWM2,RPWM2,0,0);
    } else {
      // Procesa los datos JSON
      int u1 = jsonDoc["u1"];
      int u2 = jsonDoc["u2"];
      int direccion1 = jsonDoc["direccion1"];
      int direccion2 = jsonDoc["direccion2"];

      // Llama a la funcion para controlar los motores, los argumentos inversos son por el espejo en los motores
      setMotor(RPWM1,LPWM1,u1,direccion1);
      setMotor(LPWM2,RPWM2,u2,direccion2);
    }
  }
}

void setMotor(RPWM,LPWM,u,direccion)
  {
    if(direccion==1)
      {
        analogWrite(RPWM,u);  # ajusta según el control
        analogWrite(LPWM,0);  # Si se mueve para adelante, entonces el lpwm es 0
      }
	else  
    {
        analogWrite(LPWM,u);  # ajusta según el control
        analogWrite(RPWM,0);  # Si se mueve para adelante, entonces el lpwm es 0
    }		
  }
  
  