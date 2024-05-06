#En primer lugar obtenemos la velocidad angular de las ruedas
import time
import math

x_robot = 0
y_robot = 0
theta_robot = 0

# Función para calcular la velocidad angular de un motor
def pose(encoder_count1, encoder_count2, tiempo_muestreo):
    # radio de la rueda dentada en metros
    radio_rueda = 2.3

    # Velocidad angular del motor en radianes por segundo
    velocidad_angular1 = (encoder_count1/16) * ((2*math.pi)/tiempo_muestreo)
    velocidad_angular2 = (encoder_count2/16) * ((2*math.pi)/tiempo_muestreo)

    # Velocidad lineal
    velocidad_lineal1 = velocidad_angular1 * radio_rueda
    velocidad_lineal2 = velocidad_angular2 * radio_rueda

    #Se obtiene la velocidad angular y lineal del robot
    velocidad_angular_robot = velocidad_angular2 - velocidad_angular1
    velocidad_lineal_robot = (velocidad_lineal1 + velocidad_lineal2)/2

    global x_robot, y_robot, theta_robot
    # Integrar las velocidades para obtener el cambio en la posición y la orientación del robot
    cambio_x = velocidad_lineal_robot * tiempo_muestreo * math.cos(theta_robot)
    cambio_y = velocidad_lineal_robot * tiempo_muestreo * math.sin(theta_robot)
    cambio_theta = velocidad_angular_robot * tiempo_muestreo

    # Actualizar la posición y la orientación del robot
    x_robot += cambio_x
    y_robot += cambio_y
    theta_robot += cambio_theta

