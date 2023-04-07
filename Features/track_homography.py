# Se usa la librería de opencv para rasterar con la webcam objetos
import cv2 as cv
import numpy as np

# Se lee la imagen a procesar y se abre la cámara para porcesar el objeto a 
	# seguir
img = cv.pyrDown(cv.imread("Image_Photos/Digimon.jpg"))
cap = cv.VideoCapture(0)
# Se utiliza la función cv2xfeatures2d.SIFT_create para crear un modelo que 
	# busque los puntos característicos
# Clase para extraer puntos clave y calcular descriptores utilizando el 
	# algoritmo Scale Invariant Feature Transform ( SIFT ) de D. Lowe
# cv2.xfeatures2d.SIFT_create(nfeatures = 0, nOctaveLayers = 3, 
	# contrastThreshold = 0.04, edgeThreshold = 10, sigma = 1.6)
		# nfeatures = El número de mejores características para retener. 
			# Las características se clasifican por sus puntuaciones 
			#(medidas en el algoritmo SIFT como el contraste local) 
		# nOctaveLayers = El número de capas en cada octava. 3 es el valor 
			# utilizado en el papel de D. 
			# Lowe. El número de octavas se calcula automáticamente a partir 
			# de la resolución de la imagen.
		# contrastThreshold = 	El umbral de contraste utilizado para filtrar 
			# características débiles en regiones semiuniformes 
				# (de bajo contraste).
			# Cuanto mayor sea el umbral, menos características producirá 
				# el detector.
		# edgeThreshold = El umbral utilizado para filtrar entidades 
			# similares a bordes. Tenga en cuenta que su significado es 
			# diferente del contrastThreshold, es decir, cuanto mayor 
			# sea edgeThreshold, menos características se filtran 
			# (se retienen más características).
		# sigma = La sigma de la Gaussiana aplicada a la imagen de entrada 
			# en la octava #0. Si su imagen se captura con una cámara 
			# débil con lentes suaves, es posible que desee reducir el número.
# Nota SIFT es una algoritmo patentado, así que solo duncionaría en 
	# pip install opencv-python==3.3.0.10 opencv-contrib-python==3.3.0.10
sift = cv.xfeatures2d.SIFT_create()
# Se almacenan los datos de los puntos característicos y los descriptores 
	# con la función detectAndCompute()
# detectAndCompute(image, mask, keypoints, descriptors, 
	# useProvidedKeypoints = false)
kp_img, desc_img = sift.detectAndCompute(image=img,mask=None)
# Se crean diccionarios con los parámetros que serán explicados posteriormente
index_params = dict(algorithm=0, trees=5)
search_params = dict()
# Se carga el método FlannBasedMatcher que es un método para encontrar 
	# coincidencias
# cv2FlannBasedMatcher(indexParams = makePtr< flann::KDTreeIndexParams >(), 
	# searchParams = makePtr< flann::SearchParams >())
flann = cv.FlannBasedMatcher(index_params,search_params)
# Se crea un bucle para mostrar los resultados y cargar la solución frame 
	# to frame
while True:
	# Se carga la imagen de cada frame
	ret, frame = cap.read()
	# Se pasa a escala de grises la imagen obtenida de la webcam
	gray_frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
	# Al igual que se hace fuera del bucle se buscan los puntos característicos 
		# y los descriptores
	kp_gray_frame, desc_gray_frame = sift.detectAndCompute(image=gray_frame,
		mask=None)
	# Con esta función de FlannBasedMatcher() llamda knnMatch() se encuentra 
		# las k mejores coincidencias para cada descriptor de un conjunto 
		# de consultas.
	#  cv::DescriptorMatcher::knnMatch(queryDescriptors, trainDescriptors,
		# matches, k, mask = noArray(), compactResult = false)

		# queryDescriptors = Conjunto de consultas de descriptores.
		# trainDescriptor = Conjunto de entrenamoentode descriptores. 
			# Este conjunto no se agrega a la colección de descriptores 
			# del entrenamiento almacenada en el objeto de clase.
		# matches = Coincidencias. Cada coincidencia[i] es k o menos 
			# coincidencias para el mismo descriptor de consulta.
		# k = Recuento de las mejores coincidencias encontradas por cada 
			# descriptor de consulta o menos si un descriptor de consulta 
			# tiene menos de k posibles coincidencias en total.
		# mask = Máscara que especifica coincidencias permitidas entre una 
			# consulta de entrada y matrices de descriptores de tren.
		# compactResult = Parámetro utilizado cuando la máscara (o máscaras) 
			# no está vacía. Si compactResult es falso, el vector de 
			# coincidencias tiene el mismo tamaño que las filas de queryDescriptors.
			# Si compactResult es verdadero, el vector de coincidencias no 
			# contiene coincidencias para descriptores de consulta 
			# completamente enmascarados.
	# Para mostrar la img3 se muestran primero los descriptores de la imagen 
		# original y luelo los de las escala de grises
	matches = flann.knnMatch(desc_img,desc_gray_frame,k=2)
	good_points = []
	good_points_distance = []
	# Se crea un bucle for para decidir si son puntos buenos o malos
	for m,n in matches:
		if m.distance < 0.6*n.distance:
			good_points.append(m)
	# Se puede alamcenar este resultado y pintado en la varaible img3
	# img3 = cv.drawMatches(img,kp_img, gray_frame, kp_gray_frame,
	# 	good_points, gray_frame)

	# cv.imshow("frame",img3)
	# key = cv.waitKey(1)
	# if key==27: break

	# Homografy
	# Se existen más de 10 puntos buenos para hacer el seguimiento, 
		# se aplica la condición
	if len(good_points) > 10:
		# Para el atributo item.queryIdx da el índice del descriptor en la lista 
			# de descriptores de consulta 
			# (en nuestro caso, es la lista de descriptores en el img).
		query_pts = np.float32([kp_img[m.queryIdx].pt for m in good_points]).reshape(-1,1,2)
		# Para el atributo item.trainIdx da el índice del descriptor en la 
			# lista de descriptores del tren (en nuestro caso, es la lista de 
			# descriptores en el gray_frame).
		train_pts = np.float32([kp_gray_frame[m.trainIdx].pt for m in good_points]).reshape(-1,1,2)
		# Se aplica la función cv2.findHomography() para encontrar una 
			# transformación de perspectiva entre dos planos.
		# cv2.findHomography(srcPoints, dstPoints, method = 0, 
			# ransacReprojThreshold = 3, mask = noArray(), 
			# maxIters = 2000, confidence = 0.995)

			# srcPoints = Coordenadas de los puntos en el plano original, 
				# una matriz del tipo CV_32FC2 o vector<Point2f> .
			# dstPoints = Coordenadas de los puntos en el plano objetivo, 
				# una matriz del tipo CV_32FC2 o un vector<Point2f> .
			# method = 	Método utilizado para calcular una matriz homográfica.
				# Los siguientes métodos son posibles:
				# 0 - un método regular que utiliza todos los puntos, es decir, 
					# el método de mínimos cuadrados
				# RANSAC : método robusto basado en RANSAC
				# LMEDS : método robusto de mediana mínima
				# RHO - Método robusto basado en PROSAC
			# ransacReprojThreshold = Máximo error de reproyección permitido 
				# para tratar un par de puntos como un valor 
				# interior (utilizado solo en los métodos RANSAC y RHO). es decir, si
				# ||dstPoints_i - convertPointsHomogeneous(H*srcPoints_i)||_2 > 
				# ransacReprojThreshold 
				# entonces el punto i se considera un caso atípico. Si srcPoints y 
				# dstPoints se miden en píxeles, 
				# generalmente tiene sentido establecer este parámetro en algún 
				# lugar en el rango de 1 a 10.
			# mask = Máscara de salida opcional establecida por un método robusto 
				# (RANSAC o LMeDS).
				# Tenga en cuenta que los valores de la máscara de entrada se ignoran.
			# maxIters = El número máximo de iteraciones de RANSAC.
			# confidence = Nivel de confianza, entre 0 y 1.
		matrix, mask = cv.findHomography(srcPoints=query_pts, dstPoints=train_pts, 
			method = cv.RANSAC, ransacReprojThreshold = 5.0)
		# Se convierten las coincidencias en una lista
		matches_mask = mask.ravel().tolist()
		# Se pintan las coincidencias encontradas si es que se han encontrado
		# Trasndormación de la perspectiva
		h,w,c = img.shape
		pts = np.float32([[0,0],[0,h],[h,w],[w,0]]).reshape(-1,1,2)
		# Se obtiene la transformación de la perspectiva que devuelve un array
		# cv2.perspectiveTransform(src, dst, m)
			# src = matriz de coma flotante de dos o tres canales de entrada; 
				# cada elemento es un vector 2D/3D a transformar.
			# dst = matriz de salida del mismo tamaño y tipo que src.
			# m = Matriz de transformación de punto flotante de 3x3 o 4x4.
		dts = cv.perspectiveTransform(pts,matrix)
		# Se pinta el resultado en cada uno de los frames
		homography = cv.polylines(frame,[np.int32(dts)],True,(255,75,255),3)
		cv.imshow("Homography",homography)
	else:
		# En caso de no cumplirse la condición de no tener suficientes puntos, 
			# se muestra la imagen en gris
		cv.imshow("Homography",gray_frame)
	# Se muestra por pantalla
	key = cv.waitKey(1)
	if key==27: break
# Se cierra la cámara y destrulle la ventana
cap.release()
cv.destroyAllWindows()