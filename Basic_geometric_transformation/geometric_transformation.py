# Se realizan transformaciones básicas de imágenes con la librería opencv
import cv2 as cv
import numpy as np

# Se lee la imagen del león
img = cv.imread("image/león.jpg")
# Se cargan los datos de filas, columnas y canales de la imagen leída
rows, cols, ch = img.shape

# La imagen se puede escalar hasta la mitad
# fx representa la escala de abscisas y fy representa la escala de coordenada
scaled_img = cv.resize(img, None, fx=2, fy=1/2)

# Se traslada la imagen con la función cv2.warpAffine()
# Los parámetros necesarios es una matriz de translacion que desplaza -100 a la derecha y -30 hacia abajo
# warp_dst = cv.warpAffine(src, warp_mat, (src.shape[1], src.shape[0]))
	# scr es la imagen de entrada
	# warp_dst es la imagen de salida
	# warp_mat es la transformación afín
	# warp_dst.size() es el tamaño deseado de la imagen de salida
matrix_t = np.float32([[1, 0, -100], [0, 1, -30]])
translated_img = cv.warpAffine(img, matrix_t, (cols, rows))

# Para la matriz de rotación hay que llamar a la función cv2.getRotationMatrix2D
# rot_mat = cv.getRotationMatrix2D( center, angle, scale )
matrix_r = cv.getRotationMatrix2D(center=(cols/2, rows/2),angle=45,scale=0.5)
rotated_img = cv.warpAffine(img, matrix_r, (cols, rows))

# Se muestran todas las transformaciones
cv.imshow("Original image", img)
cv.imshow("Scaled image", scaled_img)
cv.imshow("Translated image", translated_img)
cv.imshow("Rotated image", rotated_img)
cv.waitKey(0)
cv.destroyAllWindows()