# Se va a explicar como funciona los istogramas con la librería Opencv y matplotlib
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

# Se hacen dos pruebas explicativas usando una bandera
position = 2
# La primer muestra un cuadro negro y blanco con un círculo y representa el histograma
if position ==1:
	# Se crea una pequeña imagen de ceros
	img = np.zeros((100,100), np.uint8)
	# Se crea un rectángulo blanco
	cv.rectangle(img, (0,50), (100,100), (255), -1)
	# Se crea un círculo gris de radio 25 en las coordenadas 50,50
	cv.circle(img,(50,50),25,127,thickness=-1)
	# Se muestra por pantalla
	cv.imshow("img",img)

	# Se muestra el histograma en un rango de 256
	# La función img.ravel() devuelve una matriz de 1D con todos los elementos del mismo tipo
	# bins = 256 es el número entero que representa los datos del eje de abcisas
	# El rango [0,256] muestra el rango del histograma
	plt.hist(img.ravel(),256,[0,256])
	plt.show()
else:
	# Se lee la imagen de tres dimensiones
	# img = cv.imread("photos/beach_1.jpg")
	img = cv.imread("photos/beach_2.jpg")
	b, g, r = cv.split(img)

	# Se lee la imagen con color y se separan en azul, verde y rojo
	cv.imshow("img", img)
	cv.imshow("b", b)
	cv.imshow("g", g)
	cv.imshow("r", r)

	# Se muestra el histograma de los tres colores
	plt.hist(b.ravel(), 256, [0, 256],color='b')
	plt.hist(g.ravel(), 256, [0, 256],color='g')
	plt.hist(r.ravel(), 256, [0, 256],color='r')
	plt.show()