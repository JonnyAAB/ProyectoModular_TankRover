import serial
import json

# Configura el puerto serie
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Reemplaza con el nombre correcto de tu puerto serie

# Datos a enviar
datos_a_enviar = {
    "comando": "Graficas",
    "parametros": {
        "tiempo": [1, 2, 3, 4, 5],
        "pos": [10, 20, 30, 40, 50],
        "pdPlot": [5, 15, 25, 35, 45],
        "control": [1, 2, 3, 4, 5],
        "errorPlot": [0, 0, 0, 0, 0]
    }
}

# Convierte los datos a JSON
datos_json = json.dumps(datos_a_enviar)

# Envía los datos por el puerto serie
ser.write(datos_json.encode())
