import pygame

# Inicializa pygame
pygame.init()

# Inicializa el controlador
controller = pygame.joystick.Joystick(0)
controller.init()

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            # Maneja el movimiento de los ejes del controlador
            # event.axis contiene el número del eje (0 para el izquierdo, 1 para el derecho)
            # event.value contiene el valor del eje (-1 a 1)
            if event.axis == 0:
                # Maneja el eje izquierdo
                print(f"Eje izquierdo: {event.value}")
            elif event.axis == 1:
                # Maneja el eje derecho
                print(f"Eje derecho: {event.value}")

        elif event.type == pygame.JOYBUTTONDOWN:
            # Maneja los botones presionados
            # event.button contiene el número del botón
            if event.button == 0:
                print("Botón A presionado")

        elif event.type == pygame.JOYBUTTONUP:
            # Maneja los botones liberados
            # event.button contiene el número del botón
            if event.button == 0:
                print("Botón A liberado")
