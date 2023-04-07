# Usando la librería de opencv para rastrear imágenes usando la teoría del histograma
# Ver carpeta Back_projection
import cv2 as cv
import numpy as np
# Se coge la foto inicial y se obtienen las coordenadas de esa foto de lo que se va a
# rastrear, además de generar un foto para obtener el ancho y alto para determinar en
# que parte de la foto está

# Se cargan los datos de las coordenadas
coordenadas = list(open("pictures/coordenadas.txt",'r'))
pos_1, pos_2 = coordenadas[0], coordenadas[1]
x1, y1 = pos_1.split(" ")
x1 = int(x1)
y1 = int(y1[:-1])
x2, y2 = pos_2.split(" ")
x2 = int(x2)
y2 = int(y2[:-1])
x_Max, x_Min = np.maximum(x1,x2), np.minimum(x1,x2) 
y_Max, y_Min = np.maximum(y1,y2), np.minimum(y1,y2)
# Se crea la imagen a rastrear dentro de la imagen original
img = cv.imread("pictures/frames.jpg")
img_track = img[y_Min: y_Max, x_Min: x_Max]
# Se convierte esa imagen en formato HSV para poder tratar mejor la imagen
# y buscar la jor representación de la imagen a rastrear, para ello se usa 
# la funcón cv2.calcHist(). Ver carpeta Back_projection
hsv_img_track = cv.cvtColor(img_track, cv.COLOR_BGR2HSV)
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
# Para conseguir una mejor representación de todos los datos se normalizan con la función cv2.normalize
# Normaliza la norma o rango de valores de una matriz.
# cv2.normalize(src, dst, alpha = 1, beta = 0, norm_type = NORM_L2, dtype = -1, mask = noArray())
	# src = matriz de entrada
	# dst = matriz de salida del mismo tamaño que src .
	# alpha = valor de norma para normalizar o el límite inferior del rango en el caso de la normalización del rango.
	# beta = límite superior del rango en el caso de la normalización del rango; no se utiliza para la normalización de normas.
	# norm_type = 	tipo de normalización (ver cv::NormTypes).
	# dtype = cuando es negativo, la matriz de salida tiene el mismo tipo que src; de lo contrario, 
		# tiene la misma cantidad de canales que src y la profundidad = CV_MAT_DEPTH(dtype).
	# mask = máscara de operación opcional.
img_track_hist = cv.normalize(src=img_track_hist, dst=img_track_hist, alpha=0, beta=255, 
	norm_type=cv.NORM_MINMAX)
# Después hay que elegir un criterio de rastreo acorde a un algoritmo iterativo que en este caso será:
# cv2.TermCriteria(type, maxCount, epsilon)
	# type = El tipo de criterio de terminación, uno de TermCriteria::Type
		# TermCriteria::Type = Tipo de criterio, puede ser uno de: COUNT, EPS o COUNT + EPS
			# COUNT  = el número máximo de iteraciones o elementos para calcular
			# MAX_ITER = ídem
			# EPS = la precisión deseada o el cambio en los parámetros en los que se detiene el algoritmo iterativo
	# maxCount = El número máximo de iteraciones o elementos para calcular.
	# epsilon = La precisión deseada o el cambio en los parámetros en los que se detiene el algoritmo iterativo.
term_criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
# Se carga el vídeo para reproducirlo o la web cam, para ello se usa una bandera
flag = 1
if flag==1:
	cap = cv.VideoCapture("pictures/video.avi")
else:
	cap = cv.VideoCapture(0)
while True:
	# Se alamacena frame a frame en una variable
	ret, frame = cap.read()
	# Se convierte en formato HSV y se crea una máscara con la mejor proyección. Ver carpeta Back_projection
	# Se pone una condicción try para cuando se acabe el vídeo
	try:
		hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
	except Exception:
		break
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
	# Con la máscara se puede rastrear la imagen deseada con la función cv2.meanShift()
	# cv2.meanShift(probImage, window, criteria)
		# probImage = Retroproyección del histograma del objeto. Ver calcBackProject para más detalles.
		# window = Ventana de búsqueda inicial.
		# criteria = Criterios de parada para el algoritmo de búsqueda iterativa. devuelve: Número de iteraciones que CAMSHIFT tomó para converger.
			# La función implementa el algoritmo iterativo de búsqueda de objetos. Toma la retroproyección de entrada de un objeto y la posición inicial.
			# Se calcula el centro de masa en la ventana de la imagen de retroproyección y el centro de la ventana de búsqueda se desplaza al centro de masa.
			# El procedimiento se repite hasta que se realiza el número especificado de iteraciones criterio.maxCount o hasta que el centro de la ventana se 
			# desplaza menos de criterio.epsilon. El algoritmo se usa dentro de CamShift y, a diferencia de CamShift, el tamaño o la orientación 
			# de la ventana de búsqueda no cambian durante la búsqueda. Simplemente puede pasar la salida de calcBackProject a esta función.
			# Pero se pueden obtener mejores resultados si prefiltra la retroproyección y elimina el ruido.
	_, track_window = cv.meanShift(probImage=mask, window=(x_Min,y_Min,x_Max-x_Min,y_Max-y_Min),
		criteria=term_criteria)

	# Se almacenan las coordenadas en las variables x,y, w, h y después se grafica
	x, y, w, h = track_window
	cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	
	# Se muestra el vídeo
	cv.imshow("Viedo",frame)
	cv.imshow("Mask", mask)
	
	key = cv.waitKey(60)
	if key==27: break

# Se cierra el video
cap.release()
cv.destroyAllWindows()