# Archivo para comparar si dos imágenes son iguales
import cv2 as cv
import numpy as np

# Se cargan las imágenes a comparar
original = cv.imread("photos/estatua1.jpg")
# Se escala la imagen para mostrarla en pantalla
scale_percent = 140 # percent of original size
width = int(original.shape[1] * scale_percent / 100)
height = int(original.shape[0] * scale_percent / 100)
dim = (width, height)
# Se ajusta la imagen
original = cv.resize(original, dim, interpolation = cv.INTER_AREA)
duplicate = cv.imread("photos/estatua2.jpg")
# Se escala la imagen para mostrarla en pantalla
scale_percent = 140 # percent of duplicate size
width = int(duplicate.shape[1] * scale_percent / 100)
height = int(duplicate.shape[0] * scale_percent / 100)
dim = (width, height)
# Se ajusta la imagen
duplicate = cv.resize(duplicate, dim, interpolation = cv.INTER_AREA)

# 1) Se compara si dos imágenes son iguales
# Se comprueba primero si las dimensiones son las mismas
if original.shape == duplicate.shape:
	print("#################################################################")
	print("Las dimensiones de alto, ancho y canales de color son iguales")
	print("#################################################################")
	# Se obtiene la diferencia entre las dos imágnes y si son iguales el resultado es negro
	difference = cv.subtract(original, duplicate)
	# Se separa los tres canales de color con la función split
	b ,g, r = cv.split(difference)

	# En caso de ser todos los valores 0 (que todos los píxeles sean iguales) se etiqueta la imágen como igua
	if cv.countNonZero(b) == 0 and cv.countNonZero(g) == 0 and cv.countNonZero(r) == 0:
		print("#################################################################")
		print('Las dos imágenes son iguales')
		print("#################################################################")
	else:
		print("#################################################################")
		print('Las dos imágenes NO son iguales')
		print("#################################################################")

# Se muestra tanto la copia como el original
cv.imshow("Original",original)
cv.imshow("Duplicate",duplicate)
# cv.imshow("Difference",difference)
cv.waitKey(0)
cv.destroyAllWindows()

# 2) Se comprueba si dos imágenes son iguales
sift = cv.xfeatures2d.SIFT_create()
# Se extraen los key points y los descriptores de ambas imágenes
kp_1, desc_1 = sift.detectAndCompute(original, None)
kp_2, desc_2 = sift.detectAndCompute(duplicate, None)
print("#################################################################")
print("Keypoints de la primera imagen: {}".format(len(kp_1)))
print("Keypoints de la segunda imagen: {}".format(len(kp_2)))
print("#################################################################")

# Se carga el método FlannBasedMatcher que es un método para encontrar coincidencias
index_param = dict(algorithm=0, trees=5)
search_params = dict()
flann = cv.FlannBasedMatcher(index_param, search_params)
# Se almacenan las coincidencias en una matriz llamada matches
matches = flann.knnMatch(desc_1,desc_2,k=2)

# Para evitar mucho ruido en el resultado, se reduce el valor del ratio para mostrar solo los resultados destacados
ratio = 0.6
good_points = [m for m, n in matches if (m.distance < ratio*n.distance)]
# Se pretende saber el número de keypoints para determinar que tan simil es una imagen
number_keypoints = 0
if len(kp_1) <= len(kp_2):
	number_keypoints = len(kp_1)
else:
	number_keypoints = len(kp_2)

print("#################################################################")
print("La cantidad de good_points es de {}".format(len(good_points)))
print("#################################################################")
# Se dibujan los resultados en la imagen
result = cv.drawMatches(original, kp_1, duplicate, kp_2, good_points, None)

# Se puede conocer la proporcion de la similitud de la imagen original con respecto a las dos
print("#################################################################")
print("La proporcion de similitid de las imágnes es de: ",len(good_points)/number_keypoints*100)
print("#################################################################")

# Finalmente se muestran los resultados por pantalla
cv.imshow("Result", result)
cv.imshow("Original",original)
cv.imshow("Duplicate",duplicate)
cv.waitKey(0)
cv.destroyAllWindows()