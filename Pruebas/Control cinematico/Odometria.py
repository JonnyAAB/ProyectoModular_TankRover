import math

class OdometryCalculator:
    def __init__(self, wheel_distance):
        self.wheel_distance = wheel_distance
        self.x = 0  # Posición x del robot
        self.y = 0  # Posición y del robot
        self.theta = 0  # Orientación del robot
        self.last_time = None

    def update(self, vr, vl, current_time):
        if self.last_time is None:
            self.last_time = current_time
            return

        # Calcular el cambio en el tiempo
        dt = current_time - self.last_time

        # Calcular la velocidad lineal y angular
        v = (vr + vl) / 2
        w = (vr - vl) / self.wheel_distance

        # Calcular los cambios en la posición y orientación
        dx = v * dt * math.cos(self.theta)
        dy = v * dt * math.sin(self.theta)
        dtheta = w * dt

        # Actualizar la posición y orientación
        self.x += dx
        self.y += dy
        self.theta += dtheta

        # Mantener la orientación en el rango de [0, 2*pi)
        self.theta = self.theta % (2 * math.pi)

        # Actualizar el tiempo
        self.last_time = current_time

# Ejemplo de uso
if __name__ == "__main__":
    # Distancia entre las ruedas del robot (en metros)
    Distancia = 40  # La distancia es de 40 pulsos por metro

    # Crear un objeto de calculadora de odometría
    odometry_calculator = OdometryCalculator(wheel_distance)



    # Velocidades de las ruedas derecha e izquierda (en metros por segundo)
    vr = 0.2  # Velocidad de la rueda derecha (ejemplo: 20 cm/s)
    vl = 0.3  # Velocidad de la rueda izquierda (ejemplo: 30 cm/s)

    # Tiempo actual (en segundos)
    current_time = 1.0

    # Actualizar la odometría con las velocidades de las ruedas y el tiempo actual
    odometry_calculator.update(vr, vl, current_time)

    # Mostrar la posición y orientación del robot después de la actualización
    print("Posición x:", odometry_calculator.x)
    print("Posición y:", odometry_calculator.y)
    print("Orientación (theta):", odometry_calculator.theta)
