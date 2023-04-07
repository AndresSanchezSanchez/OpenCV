# Usando la librería de opencv se buscan y comparan los puntos clacves
import cv2 as cv
import numpy as np

# Se leen las dos imágenes y en la de libro se hace una pyramide para reducir
# la resolución
img1 = cv.imread("Image_Photos/Andres_Libro.jpg", cv.IMREAD_GRAYSCALE)
img2 = cv.pyrDown(cv.imread("Image_Photos/libro.jpg", cv.IMREAD_GRAYSCALE))


# ORB Detector Se usa el detector OBR que es el que funciona en esta versión
orb = cv.ORB_create()
# detectAndCompute(image, mask, keypoints, descriptors, 
	# useProvidedKeypoints = false)
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# Brute Force Matching
# Se trata de crear el modelo de predictor de fuerza bruta
# Se crea un modelo con el constructor de cv2.BFMatcher()
# cv2.BFMatcher(normType = NORM_L2, crossCheck = false)
bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
# Te saca tods los puntos comunes la función mathc
matches = bf.match(des1, des2)
# Usando una función lambda se ordenana de mayor a menor
matches = sorted(matches, key = lambda x:x.distance)

# EL resultado se punta con la función cv2.drawMatches()
# cv2.drawMatches(image, keypoints, outImage, color = Scalar::all(-1),
	# flags = DrawMatchesFlags::DEFAULT)

	# image = Imagen de origen.
	# keypoints = Puntos clave de la imagen de origen.
	# outImage = Imagen de salida. Su contenido depende del valor de las banderas que definen lo que se dibuja en la imagen de salida.
		# Consulte los posibles valores de bits de las banderas a continuación.
	# color = Color de los puntos clave.
	# flags = Banderas que configuran características de dibujo. 
		# Los posibles valores de bits de banderas están definidos por DrawMatchesFlags. Ver detalles arriba en drawMatches.
matching_result = cv.drawMatches(img1, kp1, img2, kp2, matches[:50], 
	None, flags=2)

# Se muestran los resultados obtenidos
cv.imshow("Img1", img1)
cv.imshow("Img2", img2)
cv.imshow("Matching result", matching_result)
cv.waitKey(0)
cv.destroyAllWindows()
