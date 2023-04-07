# Se muestran todos los distintos tipos de umbralización de la librería opencv
import cv2 as cv
import numpy as np

# Se pone una bandera para elegir la imagen con degradado dicdactica o una real
option = 2

if option == 1:
	# Se lee una imagen para explicar los tipos de umbralización
	img = cv.imread("image/black_to_white.jpg", cv.IMREAD_GRAYSCALE)
	img = cv.resize(img, (300,150),1,1,cv.INTER_CUBIC)

	# Umbralización binaria, si supera el valor intermedio se asigna 255 y si no 0
	_, threshold_binary = cv.threshold(img, 128, 255, cv.THRESH_BINARY)
	# Umbralización binaria inversa, se contrapone lo anterior
	_, threshold_binary_inv = cv.threshold(img, 128, 255, cv.THRESH_BINARY_INV)
	# Umbralización truncada consiste en que si los valores están por encima del valor umbral,
	# todos los píxeles toman el valor umbral
	_, threshold_trunc = cv.threshold(img, 128, 255, cv.THRESH_TRUNC)
	# Umbralización to zero consiste en que todo lo que está por encima del umbral se mantiene,
	# en cambio, lo que está por debajo se cae a cero
	_, threshold_to_zero = cv.threshold(img, 128, 255, cv.THRESH_TOZERO)

	cv.imshow("Image", img)
	cv.imshow("th binary", threshold_binary)
	cv.imshow("th binary inv", threshold_binary_inv)
	cv.imshow("th trunc", threshold_trunc)
	cv.imshow("th to zero", threshold_to_zero)

	cv.waitKey(0)
	cv.destroyAllWindows()

else:

	def nothing(x):
		pass

	img = cv.imread("fotos/Blue_Spider-Man.jpg", cv.IMREAD_GRAYSCALE)
	cv.namedWindow("Image")
	cv.createTrackbar("Threshold value", "Image", 128, 255, nothing)

	while True:
		value_threshold = cv.getTrackbarPos("Threshold value", "Image")
		_, threshold_binary = cv.threshold(img, value_threshold, 255, cv.THRESH_BINARY)
		_, threshold_binary_inv = cv.threshold(img, value_threshold, 255, cv.THRESH_BINARY_INV)
		_, threshold_trunc = cv.threshold(img, value_threshold, 255, cv.THRESH_TRUNC)
		_, threshold_to_zero = cv.threshold(img, value_threshold, 255, cv.THRESH_TOZERO)
		_, threshold_to_zero_inv = cv.threshold(img, value_threshold, 255, cv.THRESH_TOZERO_INV)

		cv.imshow("Image", img)
		cv.imshow("th binary", threshold_binary)
		cv.imshow("th binary inv", threshold_binary_inv)
		cv.imshow("th trunc", threshold_trunc)
		cv.imshow("th to zero", threshold_to_zero)
		cv.imshow("th to zero inv", threshold_to_zero_inv)

		key = cv.waitKey(100)
		if key == 27:
			break

	cv.destroyAllWindows()