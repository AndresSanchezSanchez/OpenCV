# Usando la librería de opencv se va a detectar las caras de las personas
import cv2 as cv
import numpy as np

# Se necesita crea una función para usar TrackBar y poder variar parámetros
# del detector de rostros
def nothing(x):
	pass
# Se abre la webcam para leer las caras de las personas que estén en frente
cap = cv.VideoCapture(0)

# Se crea el modelo con la función cv2.CascadeClassifier()
# cv2.CascadeClassifier()
# Existen varios modelos entrenados para este proposito, para encontrar donde están almacenada,
# busca en la consola (de anaconda o el cmd) python (where python)
# Se propocionará una ruta y se tiene que entrar en diferentes carpetas que son las siguientes
# C:\ProgramData\Anaconda3\Lib\site-packages\cv2\data (para windows)
# Nota: se debe haber instalado previamente la librería de opencv
# Los distintos clasificadores son los siguientes:
	# haarcascade_eye.xml
	# haarcascade_eye_tree_eyeglasses.xml
	# haarcascade_frontalcatface.xml
	# haarcascade_frontalcatface_extended.xml
	# haarcascade_frontalface_alt.xml
	# haarcascade_frontalface_alt_tree.xml
	# haarcascade_frontalface_alt2.xml
	# haarcascade_frontalface_default.xml
	# haarcascade_fullbody.xml
	# haarcascade_lefteye_2splits.xml
	# haarcascade_licence_plate_rus_16stages.xml
	# haarcascade_lowerbody.xml
	# haarcascade_profileface.xml
	# haarcascade_righteye_2splits.xml
	# haarcascade_russian_plate_number.xml
	# haarcascade_smile.xml
	# haarcascade_upperbody.xml
# Nota: en caso de no funcionar, se escribe la ruta completa en el modelo
face_cascade = cv.CascadeClassifier(cv.data.haarcascades +
	"haarcascade_frontalface_default.xml")

# Se crea barras de desplazamientos para variar algunos parametros del detector
cv.namedWindow("frame")
cv.createTrackbar("Neighbours","frame",5,20,nothing)

# Se muestra por pantalla
while True:
	ret, frame = cap.read()
	if ret == None: break
	# Es necesario pasar la imagen a escala de grises
	gray = cv.cvtColor(frame.copy(),cv.COLOR_BGR2GRAY)
	# Se lee el dato que hay en la barra de desplazamiento
	neighbours = cv.getTrackbarPos("Neighbours","frame")

	# Se aplica el modelo de detector de escala con la función cv2::CascadeClassifier::detectMultiScale()
	# cv2::CascadeClassifier::detectMultiScale(image, objects, scaleFactor = 1.1, minNeighbors = 3,
		# flags = 0, minSize = Size(), maxSize = Size())

		# image = Matriz del tipo CV_8U que contiene una imagen donde se detectan objetos.
		# objects = Vector de rectángulos donde cada rectángulo contiene el objeto detectado, 
			# los rectángulos pueden estar parcialmente fuera de la imagen original.
		# scaleFactor = Parámetro que especifica cuánto se reduce el tamaño de la imagen en 
			# cada escala de imagen.
		# minNeighbors = Parámetro que especifica cuántos vecinos debe tener cada rectángulo 
			# candidato para conservarlo.
		# flags = Parámetro con el mismo significado para una cascada antigua que en la función 
			# cvHaarDetectObjects. No se utiliza para una nueva cascada.
		# minSize = Tamaño mínimo posible del objeto. Los objetos más pequeños que eso se ignoran.
		# maxSize = Tamaño máximo posible del objeto. Los objetos más grandes que eso se ignoran. 
			# Si maxSize == minSizeel modelo se evalúa en una sola escala.
	faces = face_cascade.detectMultiScale(image=gray,scaleFactor=1.3,
		minNeighbors=neighbours)
	# Se muestra el resultado
	for points in faces:
		(x,y,w,h) = points
		frame = cv.rectangle(frame,(x,y),(x+w,y+h),(255,75,255),2)
	cv.imshow("frame",frame)
	key = cv.waitKey(1)
	if key == 27: break

cap.release()
cv.destroyAllWindows()
