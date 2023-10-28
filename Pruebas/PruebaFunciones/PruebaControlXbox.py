import pygame
import os
import time

# Inicializa Pygame
pygame.init()

# Inicializa los joysticks
pygame.joystick.init()

# Comprueba si hay joysticks disponibles
if pygame.joystick.get_count() > 0:
    # Obtiene el primer joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    # Loop principal
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 4:  # Gatillo izquierdo
                    left_trigger = event.value
                    print(f"Gatillo Izquierdo: {left_trigger}")
                elif event.axis == 5:  # Gatillo derecho
                    right_trigger = event.value
                    print(f"Gatillo Derecho: {right_trigger}")
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             quit()

    #     # Lectura de los valores de los sticks analógicos
    #     left_stick_x = joystick.get_axis(0)  # Stick izquierdo, eje X, -1 izquierdo 1 derecho
    #     left_stick_y = joystick.get_axis(1)  # Stick izquierdo, eje Y, -1 arriba 1 abajo
    #     right_stick_x = joystick.get_axis(2)  # Stick derecho, eje Y, -1 arriba 1 abajo
    #     right_stick_y = joystick.get_axis(3)  # Stick derecho, eje X, -1 izquierdo 1 derecho

    #     # Read D-pad input
    #     crosspad_x = joystick.get_hat(0)[0]  # D-pad X input (-1, 0, or 1)
    #     crosspad_y = joystick.get_hat(0)[1]  # D-pad Y input (-1, 0, or 1)

    #     # Check D-pad input
    #     if crosspad_x == -1:
    #         print("Left pressed")
    #     elif crosspad_x == 1:
    #         print("Right pressed")
        
    #     if crosspad_y == -1:
    #         print("Down pressed")
    #     elif crosspad_y == 1:
    #         print("Up pressed")

        

    #     # Imprime los valores
    #     if right_stick_x >= .9:        
    #         print(f"Izquierdo X: {left_stick_x}, Izquierdo Y: {left_stick_y}")
    #     elif right_stick_y >= .91:
    #         print(f"Derecho X: {right_stick_x}, Derecho Y: {right_stick_y}")
    #     # print(f"Derecho X: {right_stick_x}, Derecho Y: {right_stick_y}")

    #     # time.sleep(3)
        # os.system('cls')    # Limpia la consola


# # Inicializa pygame
# pygame.init()

# # Inicializa el controlador
# controller = pygame.joystick.Joystick(0)
# controller.init()

# Bucle principal
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.JOYAXISMOTION:
#             a=1
#             # Maneja el movimiento de los ejes del controlador
#             # event.axis contiene el número del eje (0 para el izquierdo, 1 para el derecho)
#             # event.value contiene el valor del eje (-1 a 1)
#             # if event.axis == 0:
#                 # Maneja el eje izquierdo
#                 # print(f"Eje izquierdo: {event.value}")
#             # elif event.axis == 1:
#                 # Maneja el eje derecho
#                 # print(f"Eje derecho: {event.value}")

#         elif event.type == pygame.JOYBUTTONDOWN:
#             # Maneja los botones presionados
#             # event.button contiene el número del botón
#             if event.button == 0:
#                 print("Botón A presionado")
#             if event.button == 1:
#                 print("Botón B presionado")
#             if event.button == 2:
#                 print("Botón X presionado")
#             if event.button == 3:
#                 print("Botón Y presionado")
#             if event.button == 4:
#                 print("Botón LB presionado")
#             if event.button == 5:
#                 print("Botón RB presionado")
#             if event.button == 6:
#                 print("Botón Back presionado")
#             if event.button == 7:
#                 print("Botón Start presionado")
#             if event.button == 8:
#                 print("Botón RS presionado")
#             if event.button == 9:
#                 print("Botón LS presionado")
#             if event.button == 10:
#                 print("Botón Home presionado")

#         elif event.type == pygame.JOYBUTTONUP:
#             # Maneja los botones liberados
#             # event.button contiene el número del botón
#             if event.button == 0:
#                 print("Botón A liberado")
