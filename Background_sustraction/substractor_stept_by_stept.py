# Usando la librería de opencv se va a crear un modelo para analizar el movimiento de un video en una cámara fija
import cv2 as cv
import numpy as np

# Se carga el vídeo 
cap = cv.VideoCapture("video/highway.mp4")
_,first_frame = cap.read()
# Se pasa a escala de grises para reducir el ruido y se aplica un filtro gausiano
first_gray = cv.cvtColor(first_frame,cv.COLOR_BGR2GRAY)
# cv2.GaussianBlur(src, dst, ksize, sigmaX, sigmaY = 0, borderType = BORDER_DEFAULT)
	# src = imagen de entrada; la imagen puede tener cualquier número de canales,
		# que se procesan de forma independiente, pero la profundidad debe ser
		# CV_8U, CV_16U, CV_16S, CV_32F o CV_64F.
	# dst = imagen de salida del mismo tamaño y tipo que src.
	# ksize = Tamaño del núcleo gaussiano. ksize.width y ksize.height pueden diferir,
		# pero ambos deben ser positivos e impares. O bien, pueden ser ceros y luego
		# se calculan a partir de sigma.
	# sigmaX = Desviación estándar del núcleo gaussiano en la dirección X.
	# sigmaY = Desviación estándar del núcleo gaussiano en la dirección Y;
		# si sigmaY es cero, se establece para que sea igual a sigmaX,
		# si ambos sigmas son ceros, se calculan a partir de ksize.width y ksize.height,
		# respectivamente (ver getGaussianKernel para más detalles);
		# para controlar completamente el resultado independientemente de posibles
		# modificaciones futuras de toda esta semántica,
		# se recomienda especificar todo de ksize, sigmaX y sigmaY.
	# borderType = método de extrapolación de píxeles, consulte Tipos de borde.
		# BORDER_WRAP no es compatible.
first_gray = cv.GaussianBlur(src=first_gray,ksize=(5,5),sigmaX=0)

# Se reproduce el vídeo
while True:
	_,frame = cap.read()
	# Usa la función try para cuando se acabe el vídoe
	try:
		gray_frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
	except Exception:
		break

	gray_frame = cv.GaussianBlur(src=gray_frame,ksize=(5,5),sigmaX=0)
	# Se aplica la diferencia entre el frame inicial y el resto con la función cv2.adsdiff()
	# cv2.absdiff(src1, src2, dst)
	# src1 = primera matriz de entrada o un escalar.
	# src2 = segunda matriz de entrada o un escalar.
	# dst = matriz de salida que tiene el mismo tamaño y tipo que las matrices de entrada.
	difference = cv.absdiff(src1=first_gray,src2=gray_frame)
	# Se aplica un umbral para eliminar el ruido con la función cv2.threshold()
	# cv2.threshold(src, dst, thresh, maxval, type)
	# src = matriz de entrada (punto flotante de múltiples canales, 8 bits o 32 bits).
	# dst = matriz de salida del mismo tamaño y tipo y la misma cantidad de canales que src.
	# thresh = valor umbral.
	# maxval = valor máximo para usar con los tipos de umbral THRESH_BINARY y THRESH_BINARY_INV.
	# type = tipo de umbral (ver ThresholdTypes).
	_,difference = cv.threshold(src=difference,thresh=25,
		maxval=255,type=cv.THRESH_BINARY)

	# Se muestran los resultados
	cv.imshow("first frame",cv.pyrDown(first_frame))
	cv.imshow("frame",cv.pyrDown(frame))
	cv.imshow("difference",cv.pyrDown(difference))
	key = cv.waitKey(30)
	if key == 27: break
# Se cierra la cámara y se acaban las ventanas
# Se hace un try por si el vídeo ha terminado
try:
	cap.realease()
except Exception:
	pass
cv.destroyAllWindows()