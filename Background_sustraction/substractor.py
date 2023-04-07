# Usando la librería de Opencv se puede sustraer el fondo de un vídeo en una cámara fija
import cv2 as cv
import numpy as np

# Se lee el vídeo
# cap = cv.VideoCapture("video/highway.mp4")
cap = cv.VideoCapture(0)
# Se usa la funció cv2.createBackgroundSubtractorMOG2()
# cv2.createBackgroundSubtractorMOG2(history = 500, 
	# varThreshold = 16, detectShadows = true)

	# history = Longitud de la historia.
	# varThreshold = Umbral de la distancia de Mahalanobis al cuadrado entre el píxel
		# y el modelo para decidir si el modelo de fondo describe bien un píxel.
		# Este parámetro no afecta la actualización en segundo plano.
	# detectShadows = Si es verdadero, el algoritmo detectará las sombras y las marcará.
		# Disminuye un poco la velocidad, por lo que si no necesita esta función,
		# establezca el parámetro en falso.
subtractor = cv.createBackgroundSubtractorMOG2(history=100, 
    varThreshold=10, detectShadows=True)
# Se entra en el bucle para mostrar el vídeo
while True:
	ret,frame = cap.read()
	# se crea una máscara aplicando como método subtractor
	mask = subtractor.apply(frame)
	# una condición para cuando termine el vídeo
	if ret==False:break
	# Se muestra por panlla el resultado
	cv.imshow("frame",cv.pyrDown(frame))
	cv.imshow("mask",cv.pyrDown(mask))
	key = cv.waitKey(30)
	if key == 27: break
# Se aplica try en caso de que el vídeo se termine solo
try:
	cap.release()
except Exception:
	pass
cv.destroyAllWindows()