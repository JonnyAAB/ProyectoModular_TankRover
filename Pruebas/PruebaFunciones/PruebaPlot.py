import matplotlib.pyplot as plt

# Datos de ejemplo
x = [0, 1, 2, 3, 4, 5]
y1 = [0, 1, 4, 9, 16, 25]
y2 = [0, 1, 8, 27, 64, 125]

# Crear la gráfica
plt.plot(x, y1, label='Función y = x^2', color='blue', linestyle='-', marker='o')
plt.plot(x, y2, label='Función y = x^3', color='red', linestyle='--', marker='x')

# Etiquetas de los ejes
plt.xlabel("Eje X")
plt.ylabel("Eje Y")

# Título de la gráfica
plt.title("Gráfica de Funciones")

# Leyenda
plt.legend()

# Mostrar la gráfica
plt.show()