// Incluye la biblioteca necesaria
#include <Arduino.h>
#include <ArduinoJson.h>

// Definicion de pines en la ESP32
/*
  - 32 -- se encarga de activar R_EN y L_EN en ambos IBT
  - 33 -- controla el RPWM del motor 1
  - 25 -- controla el LPWM del motor 1
  - 26 -- controla el LPWM del motor 2
  - 27 -- controla el RPWM del motor 2

  Recibe json

  {
    "direccion1": 1,
    "direccion2":1,
    "u1":50,
    "u2":50
  }
  
*/

const int En = 32;
const int RPWM1 = 33;
const int LPWM1 = 25;
const int LPWM2 = 26;
const int RPWM2 = 27;

void setMotor(int u, int RPWM, int LPWM, int direccion)
  {
    digitalWrite(En, HIGH);
    // Limitamos el control para que no haya problemas
    if(u >= 120)
      u=120;
    if(direccion == 1)
      {
        analogWrite(RPWM,u);
        analogWrite(LPWM,0);
        //Serial.println("Se va pa'delante");
      }
     else
      {
        analogWrite(LPWM,u);
        analogWrite(RPWM,0);
        //Serial.println("Se va pa'tras");
      }
  }

void setup() {
  // Inicializamos conexion serial
  Serial.begin(9600);  // Inicia la comunicación serial a 9600 baudios
  // Configuramos los pines como salida
  pinMode(En, OUTPUT);
  pinMode(RPWM1, OUTPUT);
  pinMode(LPWM1, OUTPUT);
  pinMode(RPWM2, OUTPUT);
  pinMode(LPWM2, OUTPUT);
}

void loop() {
if (Serial.available() > 0) {
    // Lee los datos disponibles en el puerto serial
    String jsonData = Serial.readStringUntil('\n');

    // Delay para asegurar la recepción completa del mensaje
    delay(50);

    // Parsea la cadena JSON
    StaticJsonDocument<200> jsonDoc;
    DeserializationError error = deserializeJson(jsonDoc, jsonData);
    
    if (error) {
      Serial.print("Error al analizar JSON: ");
      Serial.println(error.c_str());
      setMotor(0,RPWM2,LPWM2,1);
      setMotor(0,RPWM1,LPWM1,1);
    } else {
      // Procesa los datos JSON
      float u1 = jsonDoc["u1"];
      float u2 = jsonDoc["u2"];
      int direccion1 = jsonDoc["direccion1"];
      int direccion2 = jsonDoc["direccion2"];
      
      // Llamamos a la funcion que realiza el control de los motores
      setMotor(u1,RPWM1,LPWM1,direccion1);
      setMotor(u2,LPWM2,RPWM2,direccion2);
    }
  }
}
