# Barra de desplazamiento con la librería Opencv
import cv2 as cv

# Se crea una función llamada nothing que no haga nada
def nothing(x):
	pass

# Se pone un cero para que se active la cámara con la función VideoCapture
cap = cv.VideoCapture(0)

# Se crea una ventana con el nombre frame
cv.namedWindow("frame")
# Se crea una barra de desplazamiento
cv.createTrackbar("test","frame",50,500,nothing)
cv.createTrackbar("color/gray","frame",0,1,nothing)

while True:
	# Se lee la imagen de la cámara
	_,frame = cap.read()
	test = cv.getTrackbarPos("test", "frame")
	font = cv.FONT_HERSHEY_COMPLEX
	cv.putText(frame, str(test), (50, 150), font, 4, (0, 0, 255))

	# Se lee el dato de la barra si es 0 se muestra en color y si es uno en escala de grises
	s = cv.getTrackbarPos("color/gray","frame")

	if s == 0:
		pass
	else:
		# Si el valor es uno, se cambia la imagen a escala de grises
		frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

	# Se muestra la imagen de la cámara
	cv.imshow("frame",frame)
	key = cv.waitKey(1)
	if key==27: break # Si se pulsa escape se cierra la pantalla

# Cuando se pulsa esc se cierra la ventana
cap.release()
cv.destroyAllWindows()