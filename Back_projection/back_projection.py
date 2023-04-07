# Usando la librría de Opencv se pueden hacer retroprojecciones cogiendo un fondo
import cv2 as cv
import numpy as np
# Para ello e leen las imágenes deseadas de la carpeta photo
original_img = cv.imread("photos/Oblak.jpg")
lawn_img = cv.imread("photos/lawn.jpg")
# Se pasan las fotos a escala de HSV dese BGR para determinar el fondo del color
hsv_original = cv.cvtColor(original_img,cv.COLOR_BGR2HSV)
hsv_lawn = cv.cvtColor(lawn_img,cv.COLOR_BGR2HSV)
# Se paramos las matrices en tres diferentes del valor de Hue, Saturation y value del trozo de cesped
hue, saturation, value = cv.split(hsv_lawn)
# Se aplica la función de cv2.calcHist() como un Histograma ROI
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

#########################################################################
# Para calcular un histograma en escala de grises, el parámetro channels = [0]
# Para calcular un histograma en BGR, el parámetro channels = [0,1,2]
# En este caso es [0,1] porque son los canales H y S
# El parámetro histSize es una lista con todos los bins a calcular por cada canal
# En este caso es [61,256,256] porque los valores máximos son 60, 255 y 255
# Y como el último valor no se coge, se eligen esos valores
print(np.amax(hsv_lawn[:,:,0]),np.amax(hsv_lawn[:,:,1]),
	np.amax(hsv_lawn[:,:,2]))
print(np.amin(hsv_lawn[:,:,0]),np.amin(hsv_lawn[:,:,1]),
	np.amin(hsv_lawn[:,:,2]))
lawn_hist = cv.calcHist(images=[hsv_lawn],channels=[0,1],mask=None,
	histSize=[61,256],ranges=[0,61,0,256],hist=1)

# Se obtiene una máscara para aplicar en las fotos con la imagen original
# Se aplica la función de cv2.calcBackProject()
# La función cv2::calcBackProject calcula el proyecto anterior del histograma. Es decir, de manera similar a calcHist,
# en cada ubicación (x, y) la función recopila los valores de los canales seleccionados en las imágenes de entrada y 
# encuentra el contenedor de histograma correspondiente. Pero en lugar de incrementarlo, la función lee el valor del contenedor, 
# lo escala por scale y lo almacena en backProject(x,y).
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
mask = cv.calcBackProject(images=[hsv_original], channels=[0, 1], 
	hist=lawn_hist, ranges=[0, 61, 0, 256], scale=1)

# Se elimina el ruido de la máscara
# Se usa esta función y el método para construir una elipse para ser usado como kernel
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
# Esta función de cv2.filter2D convoluciona imágenes con un núcleo
# cv2.filter2d(src, dst, ddepth, kernel, anchor = Point(-1,-1), delta = 0, 
	# borderType = BORDER_DEFAULT)

	# src = imagen de entrada
	# dst = imagen de salida del mismo tamaño y el mismo número de canales que src.
	# ddepth = profundidad deseada de la imagen de destino, ver combinaciones.
	# kernel = kernel de convolución (o más bien un kernel de correlación), una matriz de punto flotante de un solo canal;
		# si desea aplicar diferentes núcleos a diferentes canales, divida la imagen en planos de color separados usando dividir
		# y procéselos individualmente.
	# anchor = ancla del kernel que indica la posición relativa de un punto filtrado dentro del kernel;
		# el ancla debe estar dentro del kernel; el valor predeterminado (-1,-1) significa que el ancla está en el centro del kernel.
	# delta =  	valor opcional agregado a los píxeles filtrados antes de almacenarlos en dst.
	# borderType = método de extrapolación de píxeles, consulte Tipos de borde . BORDER_WRAP no es compatible.
mask = cv.filter2D(src=mask,ddepth=-1,kernel=kernel)
# Hay que aplicar un umbral y luego limpiar el ruido con una apertura y cierre
# Ver carpeta de Threshold_Image
_,mask = cv.threshold(mask,100,255,cv.THRESH_BINARY)

# Con la función cv2.merge se le da las tres dimensiones a la máscara
# cv2.merge(mv, count, dst)
	# mv = matriz de entrada de matrices a fusionar; todas las matrices en mv deben tener el mismo tamaño y la misma profundidad.
	# count = número de matrices de entrada cuando mv es una matriz C simple; debe ser mayor que cero.
	# dst = matriz de salida del mismo tamaño y la misma profundidad que mv[0]; El número de canales será igual al número de parámetros.
mask = cv.merge(mv=(mask,mask,mask))
# Se une el resultado original con la máscara pra que destaque el fondo
# Se usa la función cv2.bitwise_and para convinar la máscara con la imagen inicial
result = cv.bitwise_and(original_img,mask)
# Se muestra el resultado por pantalla y se adacta la resolución si es necesario
fx, fy = 0.5, 0.5
mask = cv.resize(mask,(0,0),fx=fx,fy=fy)
result = cv.resize(result,(0,0),fx=fx,fy=fy)
original_img = cv.resize(original_img,(0,0),fx=fx,fy=fy)
lawn_img = cv.resize(lawn_img,(0,0),fx=fx,fy=fy)
cv.imshow("Mask",mask)
cv.imshow("Result",result)
cv.imshow("Original Image",original_img)
cv.imshow("lawn",lawn_img)
cv.waitKey()
cv.destroyAllWindows()