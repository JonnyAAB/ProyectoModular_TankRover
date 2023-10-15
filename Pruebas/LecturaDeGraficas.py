import matplotlib.pyplot as plt

with open("posicion.txt", "r") as archivo:
    posicion = archivo.readlines()

with open("tiempo.txt", "r") as archivo:
    tiempo = archivo.readlines()

pos = [float(linea.strip()) for linea in posicion]
t = [float(linea.strip()) for linea in tiempo]

plt.plot(tiempo,pos)
plt.xlabel("tiempo")
plt.ylabel("posicion")
plt.title("Gráfico de Valores")
plt.grid(True)
plt.show()