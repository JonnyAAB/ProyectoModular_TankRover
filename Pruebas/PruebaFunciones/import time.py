import time
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Registra el tiempo inicial
tiempo_inicial = time.time()

# Realiza alguna operación o espera
time.sleep(3)  # Espera durante 3 segundos como ejemplo

# Registra el tiempo final
tiempo_final = time.time()
print(tiempo_final)

# # Calcula la diferencia en segundos
diferencia = tiempo_final - tiempo_inicial
print(diferencia)
# # Crear una función de formato personalizado para el eje x
# def formato_segundos(x, pos):
#     return f"{x:.1f} s"

# # Crear una figura y un eje
# fig, ax = plt.subplots()

# # Crear una gráfica de ejemplo (puedes reemplazar esto con tus datos)
# valores_x = [0, diferencia]  # Usamos 0 como inicio y diferencia como final
# valores_y = [0, 1]

# # Dibuja la gráfica
# ax.plot(valores_x, valores_y)

# # Aplica el formato personalizado al eje x
# ax.xaxis.set_major_formatter(FuncFormatter(formato_segundos))

# # Etiquetas de ejes
# plt.xlabel("Tiempo")
# plt.ylabel("Valor")

# # Muestra el gráfico
# plt.show()