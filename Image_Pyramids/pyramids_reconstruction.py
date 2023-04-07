# Se usa la librería de opencv para reconstruir la función de la piramide
import cv2 as cv
import numpy as np
# Para observar los resultados previamente hay que reducir la resolución
# Para ello se lee la imagen de la mano redimensionada
img = cv.imread("photo/hand_resize.jpg")
# Se aplica una piramide Gaussian
layer = img.copy()
gaussian_pyramid = [layer]
for i in range(6):
	# cv2.pyrDown(src, dst, dstsize = Size(), borderType = BORDER_DEFAULT)
		# src = imagen de entrada
		# dst = imagen de salida; tiene el tamaño especificado y el mismo tipo que src.
		# dstsize = tamaño de la imagen de salida.
		# borderType = Método de extrapolación de píxeles, 
			# consulte Tipos de borde (no se admite BORDER_CONSTANT)
	layer = cv.pyrDown(layer)
	gaussian_pyramid.append(layer)

#Se aplica una piramide Lapalcian
# Esta función se aplica la última imagen que ya ha sido modificada
layer = gaussian_pyramid[5]
laplacian_pyramid = [layer]
# Se realiza un recorrido inverso, de 5 a cero
for i in range(5,0,-1):
	# Se analiza la dimensión anterior y se alamacena en la variable size
	size = (gaussian_pyramid[i-1].shape[1],gaussian_pyramid[i-1].shape[0])
	# cv2.pyrUp(src, dst, dstsize = Size(), borderType = BORDER_DEFAULT)
		# src = imagen de entrada
		# dst = imagen de salida Tiene el tamaño especificado y el mismo tipo que src.
		# dstsize = tamaño de la imagen de salida.
		# borderType = 	Método de extrapolación de píxeles,
			# consulte Tipos de borde (solo se admite BORDER_DEFAULT)
	gaussian_expanded = cv.pyrUp(gaussian_pyramid[i],dstsize=size)
	# Se restan dos imágenes con la fucnión cv2.subtract()
	# cv2.subctrat(src1, src2, dst, mask, dtype)
		# src1 = primera matriz de entrada o un escalar.
		# src2 = segunda matriz de entrada o un escalar.
		# dst = matriz de salida del mismo tamaño y el mismo número de canales que la matriz de entrada.
		# mask = máscara de operación opcional; esta es una matriz de un solo canal de 8 bits 
			# que especifica los elementos de la matriz de salida que se cambiarán.
		# dtype = profundidad opcional de la matriz de salida.
	laplacian = cv.subtract(gaussian_pyramid[i-1],gaussian_expanded)
	laplacian_pyramid.append(laplacian)

# Se crea el inicio de reconstrución de las imágenes almacenado en una variable
reconstructed_image = laplacian_pyramid[0]
# Solo se recorre desde el uno hasta el 5 porque el cero ya está incluido
for i in range(1,6):
	size = (laplacian_pyramid[i].shape[1],laplacian_pyramid[i].shape[0])
	reconstructed_image = cv.pyrUp(reconstructed_image,dstsize=size)
	# Se hace la suma de las dos imágenes para conseguir el color
	# cv2.add(src1, src2, dst, mask, dtype)
		# src1 = primera matriz de entrada o un escalar.
		# src2 = segunda matriz de entrada o un escalar.
		# dst = matriz de salida que tiene el mismo tamaño y número de canales que la(s) matriz(es) de entrada;
			# la profundidad está definida por dtype o src1/src2.
		# mask = máscara de operación opcional: matriz de un solo canal de 8 bits, 
			# que especifica los elementos de la matriz de salida que se cambiarán.
		# dtype = profundidad opcional de la matriz de salida.
	reconstructed_image = cv.add(reconstructed_image,laplacian_pyramid[i])
	cv.imshow(str(i),reconstructed_image)

cv.imshow("Original",img)
cv.waitKey()
cv.destroyAllWindows()
