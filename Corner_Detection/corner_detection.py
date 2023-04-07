# Con la librería de opencv se detectan esquinas y puntos finales
import cv2 as cv
import numpy as np
# Se hará esto con una imagen y con la cámara web y una barra de desplazamiento
# Se usa una bandera para decidir si se usa la webcam o no
flag = 2
# Se crea una función nothing para crear la barra de desplazamiento
def nothing(x):
	pass
if flag == 1:
	# Se lee la imagen con varias esquinas para ver como funciona la función
	img = cv.imread("image/squares.jpg")
	# Se cambia a escala de grises
	gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
	# cv2.goodFeaturesToTrack(image, corners, maxCorners, qualityLevel,
		# minDistance, mask = noArray(), blockSize = 3, 
		# useHarrisDetector = false, k = 0.04)

		# image = Entrada de imagen de un solo canal de 8 bits o punto flotante de 32 bits.
		# corners = Vector de salida de esquinas detectadas.
		# maxCorners = Número máximo de córners a devolver. 
			# Si hay más esquinas de las que se encuentran, se devuelve la más fuerte de ellas. 
			# maxCorners <= 0 implica que no se establece ningún límite en el máximo y se devuelven todas las esquinas detectadas.
		# qualityLevel = Parámetro que caracteriza la calidad mínima aceptada de las esquinas de la imagen.
			# El valor del parámetro se multiplica por la mejor medida de calidad de esquina, 
			# que es el valor propio mínimo (ver cornerMinEigenVal) o la respuesta de la función de Harris (ver cornerHarris).
			# Las esquinas con la medida de calidad inferior al producto son rechazadas.
			# Por ejemplo, si la mejor esquina tiene la medida de calidad = 1500 y qualityLevel=0.01 ,
			# todas las esquinas con la medida de calidad inferior a 15 se rechazan.
		# minDistance = Distancia euclidiana mínima posible entre las esquinas devueltas.
		# mask = Región de interés opcional. Si la imagen no está vacía (debe tener el tipo CV_8UC1 y el mismo tamaño que la imagen), 
			# especifica la región en la que se detectan las esquinas.
		# blockSize = Tamaño de un bloque promedio para calcular una matriz de covariación derivada sobre cada vecindario de píxeles. 
			# Consulte cornerEigenValsAndVecs .
		# useHarrisDetector = Parámetro que indica si usar un detector Harris (ver cornerHarris ) o cornerMinEigenVal.
		# k = Parámetro libre del detector de Harris.
	corners = cv.goodFeaturesToTrack(image=gray,maxCorners=150,
		qualityLevel=0.8,minDistance=10)
	# Se convierte en interos los datos almacenados en la variable corners
	corners = np.int0(corners)
	# Hay que meter en un bucle para mostrar los puntos
	for corner in corners:
		# Las funciones numpy.ravel() devuelven una matriz plana contigua
		x,y = corner.ravel()
		# Se colocan círculos en las esquinas
		cv.circle(img,(x,y),5,(75,150,255),-1)
	cv.imshow('image',img)
	cv.waitKey()
	cv.destroyAllWindows()
else:
	# Se crea una barra de desplazamiento en la ventana de windows
	cv.namedWindow("Frame")
	cv.createTrackbar("quality","Frame",1,100,nothing)
	# Se lee la imagen de la cámara con la función VideoCapture
	cap = cv.VideoCapture(0)
	while True:
		# Se lee la imagen de la cámara
		_, frame = cap.read()
		# Se cambia a escala de grises para poder usar la función necesaria para detectar objetos
		gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
		# Se lee el dato de la barra de desplazamiento
		quality = cv.getTrackbarPos("quality","Frame")
		quality = quality / 100 
		# Se necesita que el valor de quality esté entre 0.01 y 1 y se divide por 100
		# Y en caso de que sea cero o 1, se le asigna el valor 0.01
		if (quality == 0 or quality==1):
			quality = 0.01 
		# Se aplica la función de detección de esquinas
		corners = cv.goodFeaturesToTrack(image=gray, maxCorners=100,
			qualityLevel=quality, minDistance=20)
		# Se mira si hay valores en corners y después se convierte en entero
		if corners is not None: corners=np.int0(corners)
		# Se pasa por un bucle todos los puntos para pintarlos
		for corner in corners:
			x,y = corner.ravel()
			cv.circle(frame,(x,y),3,(123,147,210),-1)
		cv.imshow("Frame",frame)
		if cv.waitKey(1)==27: break
	# Se cierra la webcam
	cap.release()
	# Se cierran todas las ventanas
	cv.destroyAllWindows()