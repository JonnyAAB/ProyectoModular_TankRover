import msvcrt

try:
    while True:
        tecla = msvcrt.getch()  # Espera hasta que se presione una tecla
        if tecla == b'\x1b':  # Verifica si se presionó la tecla "Esc" (valor ASCII '\x1b')
            print("Saliendo del programa.")
            break
        else:
            print("Continuando después de presionar una tecla.")


except KeyboardInterrupt:
    pass