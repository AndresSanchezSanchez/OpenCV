# Con la librería opencv se muestra las imagenes reducidas tipo pirámide
import cv2 as cv
import numpy as np
# Se lee la imagen de la mano
img = cv.imread("photo/hand.jpg")
img = cv.resize(img,(0,0),fx=0.5,fy=0.5)
# Se le aplica un filtro gaussiano a la imagen
layer = img.copy()
# Se crea un vector con las capas
gaussian_pyramid = [layer]
for i in range(6):
	# cv2.pyrDown(src, dst, dstsize = Size(), borderType = BORDER_DEFAULT)
		# src = imagen de entrada
		# dst = imagen de salida; tiene el tamaño especificado y el mismo tipo que src.
		# dstsize = tamaño de la imagen de salida.
		# borderType = Método de extrapolación de píxeles, 
			# consulte Tipos de borde (no se admite BORDER_CONSTANT)
	layer = cv.pyrDown(layer)
	# Se guardan en el vector creado
	gaussian_pyramid.append(layer)

# Se le aplica un filtro Laplaciano a la imagen
layer = gaussian_pyramid[5]
cv.imshow("6", layer)
laplacian_pyramid = [layer]
for i in range(5, 0, -1):
	size = (gaussian_pyramid[i-1].shape[1], gaussian_pyramid[i-1].shape[0])
	# cv2.pyrUp(src, dst, dstsize = Size(), borderType = BORDER_DEFAULT)
		# src = imagen de entrada
		# dst = imagen de salida Tiene el tamaño especificado y el mismo tipo que src.
		# dstsize = tamaño de la imagen de salida.
		# borderType = 	Método de extrapolación de píxeles,
			# consulte Tipos de borde (solo se admite BORDER_DEFAULT)
	gaussian_expanded = cv.pyrUp(gaussian_pyramid[i], dstsize=size)
	# Se restan dos imágenes con la fucnión cv2.subtract()
	# cv2.subctrat(src1, src2, dst, mask, dtype)
		# src1 = primera matriz de entrada o un escalar.
		# src2 = segunda matriz de entrada o un escalar.
		# dst = matriz de salida del mismo tamaño y el mismo número de canales que la matriz de entrada.
		# mask = máscara de operación opcional; esta es una matriz de un solo canal de 8 bits 
			# que especifica los elementos de la matriz de salida que se cambiarán.
		# dtype = profundidad opcional de la matriz de salida.
	laplacian = cv.subtract(gaussian_pyramid[i-1], gaussian_expanded)
	laplacian_pyramid.append(laplacian)
	cv.imshow(str(i), laplacian)

cv.imshow("Original image", img)
cv.waitKey(0)
cv.destroyAllWindows()