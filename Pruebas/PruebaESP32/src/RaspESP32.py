import serial

# Configura la comunicación serial
ser = serial.Serial('/dev/tty/USB0', 9600)  # Asegúrate de especificar el puerto correcto

while True:
    # Lee los datos de la ESP32
    data = ser.readline().decode('utf-8').strip()
    print("Datos recibidos:", data)
    # Lee datos del usuario o de alguna fuente de datos en Python
    enviarTexto = "Texto enviado desde la rasp"
    # Envía los datos a la ESP32
    ser.write(enviarTexto.encode() + b'\n')

    # Aquí puedes procesar los datos según tus necesidades
