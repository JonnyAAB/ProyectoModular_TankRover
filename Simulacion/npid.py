import numpy as np

class nPID:
	def __init__(self, n=3, beta=0.3):
		# Inicialización de la clase con parámetros
		self.w = np.random.rand(n, 1)  # Pesos aleatorios
		self.beta = beta  # Parámetro beta
		self.y = 0  # Salida inicial

		# Inicialización de matrices de ganancia P, Q y R
		self.P = np.diag(np.ones(n)) * 10 	#Matriz de estimación del error de los pesos
		self.Q = np.diag(np.ones(n))		#Matriz de estimación del ruido
		self.R = 0.1						#Ruido del error

	def control_u(self, x, alpha=0.05):
		#Método para calcular la salida del controlador
		self.alpha = alpha  # Parámetro alpha
		self.v = np.dot(self.w.T, x)  # Producto punto entre w y x
		self.y = np.tanh(self.v * self.alpha)  # Función tangente hiperbólica
		return self.y * self.beta  # Salida multiplicada por beta

	def fit(self, error, x, eta=0.01):
		# Método para ajustar los pesos del controlador
		H = self.get_H(x)  # Cálculo de la matriz H
		H = H.reshape((3, 1))  # Redimensionamiento de H
		PH = np.dot(self.P, H)  # Producto punto entre P y H
		matriz = self.R + np.dot(H.T, PH)  # Cálculo de matriz
		inv = np.linalg.inv(matriz)  # Inversa de la matriz
		k = np.dot(PH, inv)  # Producto punto entre PH y la inversa

		delta_w = eta * np.dot(k, error)  # Cálculo del cambio en los pesos
		self.w = self.w + delta_w  # Actualización de los pesos
		self.P = self.P - np.dot(k, np.dot(H.T, self.P)) + self.Q  # Actualización de P

	def get_H(self, x):
		# Método para calcular la matriz H
		del_phi = (1 - self.y * self.y) * x * self.beta * self.alpha  # Cálculo de del_phi
		return del_phi  # Retorna H
