# Se pintará el contorno de un objeto filtrándolo por color con la librería de opencv
import cv2 as cv
import numpy as np

# Se abre la webcan para detectar los colores
cap = cv.VideoCapture(0)
while True:
	_,frame = cap.read()
	# se difumina la imagen para eliminar más ruido
	frame_blur = cv.GaussianBlur(frame,(5,5),0)
	hsv = cv.cvtColor(frame_blur,cv.COLOR_BGR2HSV)
	# Se detecta el color azul en un rango
	lower_blue = np.array([38, 86, 0])
	upper_blue = np.array([121, 255, 255])
	# Se crea una máscara
	mask = cv.inRange(hsv, lower_blue, upper_blue)

	# Se dibuja el contorno
	# cv2.findContours(image, contours, hierarchy, mode, method, offset = Point())
		# image = Fuente, una imagen de un solo canal de 8 bits. 
			# Los píxeles distintos de cero se tratan como 1.
			# Cero píxeles siguen siendo 0, por lo que la imagen se trata como binaria.
			# Puede usar compare , inRange , threshold , adaptiveThreshold , 
			# Canny y otros para crear una imagen binaria a partir de una en escala de grises o en color.
			# Si el modo es igual a RETR_CCOMP o RETR_FLOODFILL , la entrada también puede ser una imagen de etiquetas de enteros de 32 bits (CV_32SC1).
		# contours = Contornos detectados. Cada contorno se almacena como un vector de puntos (por ejemplo, std::vector<std::vector<cv::Point> >).
		# hierarchy = Vector de salida opcional (p. ej., std::vector<cv::Vec4i>), 
			# que contiene información sobre la topología de la imagen. 
			# Tiene tantos elementos como número de contornos. 
			# Para cada i-ésimo contorno contornos[i], los elementos jerarquía[i][0], jerarquía[i][1],
			# jerarquía[i][2] y jerarquía[i][3] se establecen en 0- índices basados ​​en contornos del contorno siguiente y anterior en el mismo nivel jerárquico, el primer contorno hijo y el contorno padre, respectivamente.
			# Si para el contorno i no hay contornos siguiente, anterior, principal o anidado, los elementos correspondientes de la jerarquía[i] serán negativos.
		# mode = Modo de recuperación de contorno, consulte RetrievalModes.
		# method = Método de aproximación de contorno, consulte ContourApproximationModes.
		# offset = Desplazamiento opcional por el cual se desplaza cada punto del contorno. Esto es útil si los contornos se extraen del ROI de la imagen y luego deben analizarse en el contexto de la imagen completa.
	contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

	# Una vez encontrado los contornos hay que dibujarlos
	for contour in contours:
		cv.drawContours(frame, contour,-1,(0,0,255),3)
		# cv2.drawContours(image, contours, contourIdx, color, thickness = 1,
			# lineType = LINE_8, hierarchy = noArray(), maxLevel = INT_MAX,
			# offset = Point()))

			# image = Imagen de destino.
			# contours = Todos los contornos de entrada. Cada contorno se almacena como un vector de puntos.
			# contourIdx = Parámetro que indica un contorno a dibujar. Si es negativo, se dibujan todos los contornos. 
			# color = 	Color de los contornos. 
			# thickness = 	Grosor de las líneas con las que se dibujan los contornos. Si es negativo (por ejemplo, thick= FILLED ), se dibujan los interiores del contorno.
			# lineType = Conectividad de línea. Ver tipos de línea.
			# hierarchy = Información opcional sobre la jerarquía. Solo es necesario si desea dibujar solo algunos de los contornos (consulte maxLevel).
			# maxLevel = Nivel máximo para contornos dibujados. Si es 0, solo se dibuja el contorno especificado. 
				# Si es 1, la función dibuja el(los) contorno(s) y todos los contornos anidados. 
				# Si es 2, la función dibuja los contornos, todos los contornos anidados, todos los contornos anidados, etc. 
				# Este parámetro solo se tiene en cuenta cuando hay jerarquía disponible.
			# offset = Parámetro de cambio de contorno opcional. Desplazar todos los contornos dibujados por el especificadocompensación =(rex , rey)
	cv.imshow("Frame",frame)
	cv.imshow("Mask",mask)
	key = cv.waitKey(1)
	if key==27: break
cap.release()
cv.destroyAllWindows()