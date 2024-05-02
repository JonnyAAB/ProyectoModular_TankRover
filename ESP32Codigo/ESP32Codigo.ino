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
*/

const int En = 32;
const int RPWM1 = 33;
const int LPWM1 = 25;
const int LPWM2 = 26;
const int RPWM2 = 27;

void setMotor(int u, int RPWM, int LPWM, int direccion)
  {
    // Limitamos el control para que no haya problemas
    if(u >= 140)
      u=140;
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
    // Esperar hasta que se reciba un mensaje completo
    String jsonData = Serial.readStringUntil('\n');

    // Procesar el mensaje JSON
    if (jsonData.length() > 0) {
        // Habilitar motores
        digitalWrite(En, HIGH);
        // Parsea la cadena JSON
        StaticJsonDocument<200> jsonDoc;
        DeserializationError error = deserializeJson(jsonDoc, jsonData);
        if (error) {
            Serial.print("Error al analizar JSON: ");
            Serial.println(error.c_str());
            setMotor(0, RPWM2, LPWM2, 1);
            setMotor(0, RPWM1, LPWM1, 1);
        } else {
            if (!jsonDoc.containsKey("u1") || !jsonDoc.containsKey("u2") ||
                !jsonDoc.containsKey("direccion1") || !jsonDoc.containsKey("direccion2")) {
                Serial.println("Error: Datos faltantes en el documento JSON. Estableciendo valores en 0.");
                // Procesa los datos JSON
                setMotor(0, RPWM2, LPWM2, 1);
                setMotor(0, RPWM1, LPWM1, 1);
            } else {
                // Procesa los datos JSON
                float u1 = jsonDoc["u1"];
                float u2 = jsonDoc["u2"];
                int direccion1 = jsonDoc["direccion1"];
                int direccion2 = jsonDoc["direccion2"];
                // Imprimir el JSON recibido
                Serial.println("JSON recibido:");
                serializeJson(jsonDoc, Serial);
                // Llamamos a la funcion que realiza el control de los motores
                setMotor(u1, RPWM1, LPWM1, direccion1);
                setMotor(u2, LPWM2, RPWM2, direccion2);
            }
        }
    } else {
        // Si no se recibió ningún dato
        Serial.println("Error: No se recibieron datos.");
        // Deshabilitar motores para ahorrar energía
        // digitalWrite(En, LOW);
    }
}
