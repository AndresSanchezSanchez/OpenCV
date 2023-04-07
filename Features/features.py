# Se usa la librería de opencv para buscar los keypoint
import cv2 as cv
import numpy as np

# Solo se puede usar con opencv 3.4.9 bajo python 3.6.9 
# (Funciona bien para SIFT y SURF)

# Se leen los datos del libro de la carpeta de Image_Photos
img = cv.imread("Image_Photos/libro.jpg",cv.IMREAD_GRAYSCALE)
# Se reduce la resolución con la función 
	# cv2.pyrDown(src, dst, dstsize = Size(), borderType = BORDER_DEFAULT)
img = cv.pyrDown(img)
"""
# Clase para extraer puntos clave y calcular descriptores utilizando el algoritmo Scale Invariant Feature Transform ( SIFT ) de D. Lowe
# cv2.xfeatures2d.SIFT_create(nfeatures = 0, nOctaveLayers = 3, 
	# contrastThreshold = 0.04, edgeThreshold = 10, sigma = 1.6)
		# nfeatures = El número de mejores características para retener. 
			# Las características se clasifican por sus puntuaciones 
			#(medidas en el algoritmo SIFT como el contraste local) 
		# nOctaveLayers = El número de capas en cada octava. 3 es el valor utilizado en el papel de D. 
			# Lowe. El número de octavas se calcula automáticamente a partir de la resolución de la imagen.
		# contrastThreshold = 	El umbral de contraste utilizado para filtrar 
			# características débiles en regiones semiuniformes (de bajo contraste).
			# Cuanto mayor sea el umbral, menos características producirá el detector.
		# edgeThreshold = El umbral utilizado para filtrar entidades similares a bordes. 
			# Tenga en cuenta que su significado es diferente del contrastThreshold, 
			# es decir, cuanto mayor sea edgeThreshold, menos características se filtran 
			# (se retienen más características).
		# sigma = La sigma de la Gaussiana aplicada a la imagen de entrada en la octava #0. 
			# Si su imagen se captura con una cámara débil con lentes suaves, es posible que desee reducir el número.
sift = cv.xfeatures2d.SIFT_create()
# Clase para extraer características robustas aceleradas de una imagen.
# cv2.xfeatures2d.SURF_create(hessianThreshold = 100, nOctaves = 4,
	# nOctaveLayers = 3, extended = false, upright = false)
		# hessianThreshold = Umbral para el detector de punto clave de arpillera utilizado en SURF.
		# nOctaves = Número de octavas piramidales que utilizará el detector de punto clave.
		# nOctaveLayers = Número de capas de octava dentro de cada octava.
		# extended = 	Indicador de descriptor extendido (verdadero: use descriptores de 128 elementos extendidos; 
			# falso: use descriptores de 64 elementos).
		# upright = Indicador de entidades giradas o hacia arriba a la derecha 
			# (verdadero: no calcula la orientación de las entidades; falso: calcula la orientación).
surf = cv.xfeatures2d.SURF_create()
# Clase que implementa el extractor de descriptores y detector de puntos clave ORB ( BRIEF orientado ).
# cv2.ORB_create(nfeatures = 500, scaleFactor = 1.2f, nlevels = 8,
	# edgeThreshold = 31, firstLevel = 0, WTA_K = 2, 
	# scoreType = ORB::HARRIS_SCORE, patchSize = 31, fastThreshold = 20)
		# nfeatures = El número máximo de entidades a conservar.
		# scaleFactor = Relación de diezmado de la pirámide, mayor que 1. scaleFactor==2 significa la pirámide clásica, 
			# donde cada siguiente nivel tiene 4 veces menos píxeles que el anterior,
			# pero un factor de escala tan grande degradará drásticamente las puntuaciones de coincidencia de características. 
			# Por otro lado, demasiado cerca de 1 factor de escala significará que para cubrir cierto rango 
			# de escala necesitarás más niveles de pirámide y, 
			# por lo tanto, la velocidad se verá afectada.
		# nlevels = El número de niveles de la pirámide. 
			# El nivel más pequeño tendrá un tamaño lineal igual a input_image_linear_size/pow(scaleFactor, nlevels - firstLevel).
		# edgeThreshold = Este es el tamaño del borde donde no se detectan las características. 
			# Debe coincidir aproximadamente con el parámetro patchSize.
		# firstLevel = 	El nivel de la pirámide para colocar la imagen de origen. 
			# Las capas anteriores se rellenan con la imagen de origen mejorada. 
		# WTA_K = 	El número de puntos que produce cada elemento del descriptor BREVE orientado.
			# El valor predeterminado 2 significa BREVE donde tomamos un par de puntos aleatorios y comparamos sus brillos,
			# por lo que obtenemos una respuesta de 0/1. Otros valores posibles son 3 y 4. Por ejemplo, 
			# 3 significa que tomamos 3 puntos aleatorios (por supuesto, esas coordenadas de puntos son aleatorias,
			# pero se generan a partir de la semilla predefinida, por lo que cada elemento del descriptor BREVE se calcula 
			# de forma determinista a partir de el rectángulo de píxeles), encuentre el punto de brillo máximo y el índice de 
			# salida del ganador (0, 1 o 2). Tal salida ocupará 2 bits y, por lo tanto, necesitará una variante especial de Hammingdistancia,
			# indicada como NORM_HAMMING2 (2 bits por contenedor). Cuando WTA_K=4, tomamos 4 puntos aleatorios para calcular cada contenedor 
			# (que también ocupará 2 bits con valores posibles 0, 1, 2 o 3).
		# scoreType = El HARRIS_SCORE predeterminado significa que el algoritmo de Harris se usa para clasificar 
			# las características (la puntuación se escribe en KeyPoint::score y se usa para conservar las mejores características); 
			# FAST_SCORE es un valor alternativo del parámetro que produce puntos clave ligeramente menos estables, pero es un poco más rápido de calcular.
		# patchSize = 	tamaño del parche utilizado por el descriptor BREVE orientado. Por supuesto, en capas piramidales más pequeñas, 
			# el área de imagen percibida cubierta por una característica será mayor.
		# fastThreshold = el umbral rápido"""
orb = cv.ORB_create(nfeatures=1500)
# detectAndCompute(image, mask, keypoints, descriptors, 
	# useProvidedKeypoints = false)

"""keypoints_sift, descriptors = sift.detectAndCompute(img, None)
keypoints_surf, descriptors = surf.detectAndCompute(img, None)"""
keypoints_orb, descriptors = orb.detectAndCompute(img, None)
# Se pintan todos los keypoints
"""img_sift = cv.drawKeypoints(img.copy(), keypoints_sift, None)
img_surf = cv.drawKeypoints(img.copy(), keypoints_surf, None)"""
img_orb = cv.drawKeypoints(img.copy(), keypoints_orb, None)

cv.imshow("Original",img)
"""cv.imshow("img_sift",img_sift)
cv.imshow("img_surf",img_surf)"""
cv.imshow("img_orb",img_orb)
cv.waitKey()
cv.destroyAllWindows()