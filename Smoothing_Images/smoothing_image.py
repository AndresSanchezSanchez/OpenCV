# Con la librería opencv se va a procesar imagenes para suavizado
import cv2 as cv
import numpy as np

# Se lee la imagen de la carpeta imagen
img = cv.imread("image/early_1800.jpg")
img = cv.resize(img,(0,0),fx=0.3,fy=0.3)

# Se aplican una serie de filtros que se muestran por pantalla
# cv2.blur(src, dst, ksize, anchor = Point(-1,-1), borderType = BORDER_DEFAULT )
	# src = imagen de entrada; puede tener cualquier número de canales, 
		# que se procesan de forma independiente, pero la profundidad debe ser CV_8U, CV_16U, CV_16S, CV_32F o CV_64F.
	# dst = imagen de salida del mismo tamaño y tipo que src.
	# ksize = difuminar el tamaño del kernel.
	# anchor = 	punto de anclaje; valor predeterminado Point(-1,-1) significa que el ancla está en el centro del kernel.
	# borderType = modo de borde utilizado para extrapolar píxeles fuera de la imagen, consulte Tipos de borde. 
		#BORDER_WRAP no es compatible.
averaging = cv.blur(img, (21, 21))
# cv2.GaussianBlur(src, dst, ksize, sigmaX, sigmaY = 0, borderType = BORDER_DEFAULT)
	# src = 	imagen de entrada; la imagen puede tener cualquier número de canales, que se procesan de forma independiente, 
		# pero la profundidad debe ser CV_8U, CV_16U, CV_16S, CV_32F o CV_64F.
	# dst = imagen de salida del mismo tamaño y tipo que src.
	# ksize = Tamaño del núcleo gaussiano. ksize.width y ksize.height pueden diferir, pero ambos deben ser positivos e impares. 
		# O bien, pueden ser ceros y luego se calculan a partir de sigma.
	# sigmaX = Desviación estándar del núcleo gaussiano en la dirección X.
	# sigmaY = Desviación estándar del núcleo gaussiano en la dirección Y; si sigmaY es cero, se establece para que sea igual a sigmaX, 
		# si ambos sigmas son ceros, se calculan a partir de ksize.width y ksize.height, 
		# respectivamente (ver getGaussianKernel para más detalles); 
		# para controlar completamente el resultado independientemente de posibles modificaciones futuras de toda esta semántica, 
		# se recomienda especificar todo de ksize, sigmaX y sigmaY.
	# borderType = método de extrapolación de píxeles, consulte Tipos de border. BORDER_WRAP no es compatible.
gaussian = cv.GaussianBlur(img, (21, 21), 0)
# cv2.medianBlur(src, dst, ksize)
	# src = entrada de imagen de 1, 3 o 4 canales; cuando ksize es 3 o 5, 
	# la profundidad de la imagen debe ser CV_8U, CV_16U o CV_32F, para tamaños de apertura más grandes, solo puede ser CV_8U.
	# dst = matriz de destino del mismo tamaño y tipo que src.
	# ksize = tamaño lineal de apertura; debe ser impar y mayor que 1, por ejemplo: 3, 5, 7...
median = cv.medianBlur(img, 5)
# cv2.bilateralFilter(src, dst, kernel_size, sigma_color, sigma_spatial, borderMode = BORDER_DEFAULT, stream)
	# src = imagen de origen. Solo admite (canales != 2 && profundidad() != CV_8S && profundidad() != CV_32S && profundidad() != CV_64F).
	# dst = Imagen de destino.
	# kernel_size = Tamaño de la ventana del núcleo.
	# sigma_color = Filtre sigma en el espacio de color.
	# sigma_spatial = 	Filtre sigma en el espacio de coordenadas.
	# borderMode = Tipo de borde. Ver borderInterpolate para más detalles. 
		#BORDER_REFLECT101 , BORDER_REPLICATE , BORDER_CONSTANT , BORDER_REFLECT y BORDER_WRAP son compatibles por ahora.
	# stream = Stream para la versión asíncrona.
bilateral = cv.bilateralFilter(img, 9, 350, 350)

cv.imshow("Original image", img)
cv.imshow("Averaging", averaging)
cv.imshow("Gaussian", gaussian)
cv.imshow("Median", median)
cv.imshow("Bilateral", bilateral)
cv.waitKey(0)
cv.destroyAllWindows()