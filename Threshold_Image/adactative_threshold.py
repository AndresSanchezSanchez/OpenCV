# Usando la librería de Opencv se usa la umbralización adactativa
import cv2 as cv
import numpy as np

# Se lee la imagen a umbralizar con técnicas de umbralización adactativa
img = cv.imread("image/book_page.jpg")
img = cv.imread("fotos/Andrés.jpg")
# En caso de necesitarlo se aplica una reducción de escala
img = cv.resize(img,(0,0),fx=0.45,fy=0.45)

# Se aplica una umbralización normal para mostrar las diferencias
_,threshold_normal = cv.threshold(img, 150,255,cv.THRESH_BINARY)


# La umbralización adactativa se tiene que realizar en escala de grises
img_gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# Se aplica dos umbralizaciones adactativas, una mean y otra gaussiana
#cv2.adaptiveThreshold(src, dst, maxValue, adaptiveMethod, thresholdType, 
	# blockSize, C)
#######################################################################
	# src = Fuente de imagen de un solo canal de 8 bits.
	# dst = Imagen de destino del mismo tamaño y del mismo tipo que src.
	# maxValue = Valor distinto de cero asignado a los píxeles para los que se cumple la condición
	# adaptiveMethod = Algoritmo de umbral adaptable para usar, consulte AdaptiveThresholdTypes . 
		# El BORDER_REPLICATE | BORDER_ISOLATED se utiliza para procesar límites.
	# thresholdType = Tipo de umbral que debe ser THRESH_BINARY o THRESH_BINARY_INV , consulte ThresholdTypes. 
	# blockSize = Tamaño de una vecindad de píxeles que se utiliza para calcular un valor de umbral para el píxel: 3, 5, 7, etc. 
	# C = Constante sustraída de la media o media ponderada. Normalmente, es positivo, pero también puede ser cero o negativo.

# Tipos de umbrales adactativos 
	# cv2.ADAPTIVE_THRESH_MEAN_C
	# cv2.ADAPTIVE_THRESH_GAUSSIAN_C 

# Se crea una función llamada nothing que no haga nada
def nothing(x):
	pass
# Se crea una barra de desplazamiento para manipular los valores constantes
cv.namedWindow("Trackbars")
cv.createTrackbar("C","Trackbars",12,40,nothing)
cv.createTrackbar("blockSize_mean","Trackbars",15,90,nothing)
cv.createTrackbar("blockSize_gauss","Trackbars",91,300,nothing)
while True:
	C = cv.getTrackbarPos("C","Trackbars")
	blockSize_mean = cv.getTrackbarPos("blockSize_mean","Trackbars")
	blockSize_gauss = cv.getTrackbarPos("blockSize_gauss","Trackbars")
	# Los balores de blockSize deben ser mayor a uno y un número impar
	# Las condiciones es para que siempre tenga valores impares y mayor de 1
	if blockSize_mean<3: blockSize_mean=3
	if blockSize_mean%2==0: blockSize_mean+=1
	if blockSize_gauss<3: blockSize_gauss=3
	if blockSize_gauss%2==0: blockSize_gauss+=1

	mean_c = cv.adaptiveThreshold(img_gray, 255,
		cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, blockSize_mean, C)
	gaus = cv.adaptiveThreshold(img_gray, 255,
		cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, blockSize_gauss, C)

	cv.imshow('Imagen',img)
	cv.imshow('Normal threshold',threshold_normal)
	cv.imshow("Mean C", mean_c)
	cv.imshow("Gaussian", gaus)
	if cv.waitKey(1)==27: break
cv.destroyAllWindows()