# Con las librería de Opencv se van a explicar las trasformaciones morfológicas
import cv2 as cv
import numpy as np

# Se va a mostrar con la cámara del ordenador y con imágenes

flag = 2
# Se crea una función de apoyo para las barras de desplazamiento
def nothing(x):
    pass

if flag ==1:
	# Se carga la imagen en escala de grises y se muestran
	# img = cv.imread("image/orange.jpg", cv.IMREAD_GRAYSCALE)
	img = cv.imread("image/balls.jpg", cv.IMREAD_GRAYSCALE)
	# Se umbraliza la imagen y se crea una máscara con binarización inversa
	_,mask = cv.threshold(img,250,255,cv.THRESH_BINARY_INV)
	# Para reducir el ruedo se usan dos técnicas, o bien una erosión o una dilatación
	# La erosión calcula un mínimo local sobre el área del núcleo dado.
	# Esto significa que la parte blanca disminuye (se erosiona)
	kernel = np.ones((5,5),np.uint8)
	dilation = cv.dilate(mask,kernel)
	# La dilatación consiste en convolucionar una imagen A con algún núcleo (B), 
	# que puede tener cualquier forma o tamaño, generalmente un cuadrado o un círculo.
	# La dilatación amplia la parte blanca de la imagen
	erosion = cv.erode(mask,kernel, iterations=6)

	cv.imshow('imagen',img)
	cv.imshow('mask',mask)
	cv.imshow('dilation',dilation)
	cv.imshow('erosion',erosion)
	cv.waitKey(0)
	cv.destroyAllWindows()
else:
	# Ahora se aplica a una imagen para filtar color
	# Se abre la cámara para capturar la imagen frame a frame
	cap = cv.VideoCapture(0)
	cv.namedWindow("Trackbars")

	# Se crean seis barras de desplazamiento mostrando los límites
	cv.createTrackbar("L - H", "Trackbars", 0, 360, nothing)
	cv.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
	cv.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
	cv.createTrackbar("U - H", "Trackbars", 360, 360, nothing)
	cv.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
	cv.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

	# Se abre un bucle para que se muestre mientras no se pulse la tecla de escape
	while True:
	    # Se muestra el resultado frame a frame y se cambia a la escala HSV
	    _, frame = cap.read()
	    frame = cv.resize(frame,(0,0),fx=0.5,fy=0.5)
	    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
	    
	    # se leen los valores de las barras de manera interactiva
	    l_h = cv.getTrackbarPos("L - H", "Trackbars")
	    l_s = cv.getTrackbarPos("L - S", "Trackbars")
	    l_v = cv.getTrackbarPos("L - V", "Trackbars")
	    u_h = cv.getTrackbarPos("U - H", "Trackbars")
	    u_s = cv.getTrackbarPos("U - S", "Trackbars")
	    u_v = cv.getTrackbarPos("U - V", "Trackbars")
	    
	    # Se filtran los valores de azul tanto altos como bajo
	    lower = np.array([l_h, l_s, l_v])
	    upper = np.array([u_h, u_s, u_v])
	    mask = cv.inRange(hsv, lower, upper)
	    
	    # Se aplican transformaciones morfológicas de apertura y cierre,
	    # además de la dilatación y la erosión
	    kernel = np.ones((5, 5), np.uint8)
	    erosion = cv.erode(mask, kernel)
	    dilation = cv.dilate(mask, kernel)
		# Se hace una apertura y un cierre
		# cv2.morphologyEx(src, dst, op, kernel, 
			# anchor = Point(-1,-1), iterations = 1, borderType = BORDER_CONSTANT,
			# borderValue = morphologyDefaultBorderValue())

			# src = Imagen de origen. El número de canales puede ser arbitrario. 
				# La profundidad debe ser una de CV_8U, CV_16U, CV_16S, CV_32F o CV_64F.
			# dst = Imagen de destino del mismo tamaño y tipo que la imagen de origen.
			# op = 	Tipo de una operación morfológica, ver MorphTypes
			# kernel = 	Elemento estructurante. Se puede crear utilizando getStructuringElement.
			# anchor = Posición de anclaje con el núcleo. 
				# Los valores negativos significan que el ancla está en el centro del kernel.
			# iterations = Número de veces que se aplican erosión y dilatación. 
			# borderType = Método de extrapolación de píxeles, consulte Tipos de borde.
				# BORDER_WRAP no es compatible.
			# borderValue = Valor de borde en caso de un borde constante.
				# El valor predeterminado tiene un significado especial.
		
	    opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=2)
	    closing = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
	    
	    # Muestra la imagen
	    cv.imshow("frame", frame)
	    cv.imshow("mask", mask)
	    # Se muestra la erosión y la dilatación
	    cv.imshow('dilation',dilation)
	    cv.imshow('erosion',erosion)
		# Se muestra la apertura y el cierre
	    cv.imshow('opening',opening)
	    cv.imshow('closing',closing)
	    
	    # Cuando se pulsa escape se sale de la pantalla
	    key = cv.waitKey(1)
	    if key == 27: break

	cap.release()
	cv.destroyAllWindows()


