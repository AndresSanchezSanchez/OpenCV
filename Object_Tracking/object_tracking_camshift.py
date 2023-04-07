# Usando la librería de opencv para rastrear imágenes usando la teoría del histograma
# Ver carpeta Back_projection
import cv2 as cv
import numpy as np
# Se lee la imagen donde se sujeta el objeto en cuestión, en este caso, la cartera
img = cv.imread("pictures/frame01.jpg")
# Se obtiene las coordenadas donde está el objeto a rastrear porque previamente se ha usado
# el script de cut.py. Ver directorio Cut
# Se cargan los datos de las coordenadas
coordenadas = list(open("pictures/coordenadas2.txt",'r'))
pos_1, pos_2 = coordenadas[0], coordenadas[1]
x1, y1 = pos_1.split(" ")
x1 = int(x1)
y1 = int(y1[:-1])
x2, y2 = pos_2.split(" ")
x2 = int(x2)
y2 = int(y2[:-1])
x_Max, x_Min = np.maximum(x1,x2), np.minimum(x1,x2) 
y_Max, y_Min = np.maximum(y1,y2), np.minimum(y1,y2)
# Usando las coordenadas, se guarda la imagen a rastrear
img_track = img[y_Min:y_Max,x_Min:x_Max,:].copy()
# Se pasa al formato de HSV para trabajar con el canal Hue
hsv_img_track = cv.cvtColor(img_track, cv.COLOR_BGR2HSV)
# Se calcula el histograma para el canal Hue con la funcón cv2.calcHist(). Ver carpeta Back_projection
# La función cv2::calcHist calcula el histograma de una o más matrices. Los elementos de una tupla utilizada para incrementar un bin
# de histograma se toman de las matrices de entrada correspondientes en la misma ubicación.
# cv2.calcHist(images, nimages, channels, mask, hist, dims, histSize, ranges, uniform = true, accumulate = false)
	# images = Matrices de origen. Todos deben tener la misma profundidad, CV_8U, CV_16U o CV_32F, y el mismo tamaño. 
		# Cada uno de ellos puede tener un número arbitrario de canales.
	# nimages = Número de imágenes de origen.
	# channels = Lista de los canales de atenuación utilizados para calcular el histograma.
		# Los canales de la primera matriz se numeran de 0 a images[0].channels()-1 , 
		# los canales de la segunda matriz se cuentan de images[0].channels() a images[0].channels() + images[1]. canales()-1,
		# y así sucesivamente.
	# mask = Máscara opcional. Si la matriz no está vacía, debe ser una matriz de 8 bits del mismo tamaño que images[i].
		# Los elementos de máscara distintos de cero marcan los elementos de matriz contados en el histograma.
	# hist = Histograma de salida, que es una matriz de dimensiones densas o dispersas.
	# dims = Dimensionalidad del histograma que debe ser positivo y no mayor que CV_MAX_DIMS (igual a 32 en la versión actual de OpenCV).
	# histSize = Matriz de tamaños de histograma en cada dimensión.
	# ranges = Matriz de los dims matrices de los límites de bin del histograma en cada dimensión. Cuando el histograma es uniforme (uniforme = verdadero), 
		# entonces para cada dimensión i es suficiente especificar el límite inferior (inclusivo) L0 del bin de histograma 0-ésimo y 
		# el límite superior (exclusivo) UhistSize[i]−1 para el último histograma bin histSize[i]-1. 
		# Es decir, en el caso de un histograma uniforme, cada uno de los ranges[i]  es una matriz de 2 elementos.
		# Cuando el histograma no es uniforme (uniform=false), cada uno de los ranges[i] contiene histSize[i]+1 elementos: 
		# L0,U0=L1,U1=L2,...,UhistSize[i]−2=LhistSize[i]−1,UhistSize[i]−1. Los elementos de la matriz, que no están entre L0 y UhistSize[i]−1, 
		# no se encuentran en el histograma.
	# uniform = Bandera que indica si el histograma es uniforme o no (ver arriba).
	# accumulate = Bandera de acumulación. Si está configurado, el histograma no se borra al principio cuando se asigna.
		# Esta función le permite calcular un único histograma a partir de varios conjuntos de matrices o actualizar el histograma a tiempo.
img_track_hist = cv.calcHist(images=[hsv_img_track], channels=[0], mask=None, 
	histSize=[180], ranges=[0, 180])
# Se le asigna el criterio
# cv2.TermCriteria(type, maxCount, epsilon)
	# type = El tipo de criterio de terminación, uno de TermCriteria::Type
		# TermCriteria::Type = Tipo de criterio, puede ser uno de: COUNT, EPS o COUNT + EPS
			# COUNT  = el número máximo de iteraciones o elementos para calcular
			# MAX_ITER = ídem
			# EPS = la precisión deseada o el cambio en los parámetros en los que se detiene el algoritmo iterativo
	# maxCount = El número máximo de iteraciones o elementos para calcular.
	# epsilon = La precisión deseada o el cambio en los parámetros en los que se detiene el algoritmo iterativo.
term_criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)

# Ahora se abre la cámara para poder rastrear el objeto en cuestión y se entra en el bucle para mostrarlo
cap = cv.VideoCapture(0)
while True:
	_,frame = cap.read()
	hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
	# Se calcula la mejor projección como la máscara
	# cv2.calcBackProject(images, nimages, channels, hist, backProject, ranges,
	# scale = 1, uniform = true)
	# images = Matrices de origen. Todos deben tener la misma profundidad, CV_8U, CV_16U o CV_32F, y el mismo tamaño. 
		# Cada uno de ellos puede tener un número arbitrario de canales.
	# nimages = Número de imágenes de origen.
	# channels = Lista de los canales de atenuación utilizados para calcular el histograma.
		# Los canales de la primera matriz se numeran de 0 a images[0].channels()-1 , 
		# los canales de la segunda matriz se cuentan de images[0].channels() a images[0].channels() + images[1]. canales()-1,
		# y así sucesivamente.
	# hist = Histograma de entrada que puede ser denso o disperso.
	# backProject = Matriz de retroproyección de destino que es una matriz de un solo canal del mismo tamaño y profundidad que las imágenes[0] 
	# ranges = Matriz de los dims matrices de los límites de bin del histograma en cada dimensión. Cuando el histograma es uniforme (uniforme = verdadero), 
		# entonces para cada dimensión i es suficiente especificar el límite inferior (inclusivo) L0 del bin de histograma 0-ésimo y 
		# el límite superior (exclusivo) UhistSize[i]−1 para el último histograma bin histSize[i]-1. 
		# Es decir, en el caso de un histograma uniforme, cada uno de los ranges[i]  es una matriz de 2 elementos.
		# Cuando el histograma no es uniforme (uniform=false), cada uno de los ranges[i] contiene histSize[i]+1 elementos: 
		# L0,U0=L1,U1=L2,...,UhistSize[i]−2=LhistSize[i]−1,UhistSize[i]−1. Los elementos de la matriz, que no están entre L0 y UhistSize[i]−1, 
		# no se encuentran en el histograma.
	# scale = Factor de escala opcional para la retroproyección de salida.
	# uniform = Bandera que indica si el histograma es uniforme o no (ver arriba).
	mask = cv.calcBackProject(images=[hsv],channels=[0],hist=img_track_hist,ranges=[0,180],scale=1)
	# Con la máscara se puede proceder al rastreo con la función cv2.CamShift() que encuentra el centro, el tamaño y la orientación de un objeto.
	# cv2.CamShift(probImage, window, criteria)
		# probImage = Retroproyección del histograma del objeto. Consulte calcBackProject.
		# window = Ventana de búsqueda inicial.
		# criteria = 	Criterios de parada para el cambio medio subyacente. devuelve (en interfaces antiguas) Número de iteraciones que CAMSHIFT
			# tomó para converger La función implementa el algoritmo de seguimiento de objetos CAMSHIFT [35] . Primero, encuentra el centro de 
			# un objeto usando meanShift y luego ajusta el tamaño de la ventana y encuentra la rotación óptima. La función devuelve la estructura 
			# del rectángulo rotado que incluye la posición, el tamaño y la orientación del objeto. La siguiente posición de la ventana de 
			# búsqueda se puede obtener con RotatedRect::boundingRect()
				# boundingRect() = devuelve el rectángulo entero vertical mínimo que contiene el rectángulo girado.
	ret, track_window = cv.CamShift(probImage=mask, window=(x_Min,y_Min,x_Max-x_Min,y_Max-y_Min),
		criteria=term_criteria)
	# El valor obtenido de ret son los datos de la ventana y la orientación conseguida del rastreo
	# Encuentra los cuatro vértices de un recto rotado. Útil para dibujar el rectángulo girado.
	# El resultado se encuerran en una caja con la función de cv2.boxPoints()
	# cv2.boxPoints(box, points)
		# box = El rectángulo girado de entrada. Puede ser la salida de points
		# points = La matriz de salida de cuatro vértices de rectángulos.
	pts = cv.boxPoints(ret)
	# Se convierten los puntos en una imagen
	pts = np.int0(pts)
	# Se pintan como una polilínea
	# cv2.polyline(img, pts, isClosed, color, thickness = 1, lineType = LINE_8, shift = 0)
		# img = Imagen.
		# pts = Matriz de curvas poligonales.
		# isClosed = 	Bandera que indica si las polilíneas dibujadas están cerradas o no. Si están cerrados, 
			# la función dibuja una línea desde el último vértice de cada curva hasta su primer vértice.
		# color = Color de polilínea.
		# thickness = Grosor de los bordes de la polilínea.
		# lineType = Tipo de los segmentos de línea. Ver LineTypes.
			# cv.FILLED, cv.LINE_4, cv.LINE_8, cv.LINE_AA
		# shift = Número de bits fraccionarios en las coordenadas del vértice.
	cv.polylines(img=frame, pts=[pts], isClosed=True, color=(255, 255, 0), thickness=2)

	# Se muestra el resultado
	cv.imshow('mask',mask)
	cv.imshow('frame',frame)
	key = cv.waitKey(1)
	if key==27: break

cap.release()
cv.destroyAllWindows()