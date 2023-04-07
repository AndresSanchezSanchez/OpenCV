# Con la librería de opencv y las funciones necesarias se vam a desplazar los puntos de las imágenes a determinar
import cv2 as cv
import numpy as np

# Se crea un archivo txt para almacenar las coordenadas
file = open("coordenadas.txt","w")

# Se crea una matriz para señalar los puntos en la imagen
def matriz_imagen(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(img, (x, y), 5, (0, 0, 255), -1)
        print(f'x={x} e y={y}')
        # Se añade más texto usando la modalidad "a"
        archivo = open("coordenadas.txt", "a")
        string = str(x)+" "+str(y)
        archivo.write(string+"\n")
        archivo.close()

# Se lee la imagen para deterctar los puntos
img = cv.imread("image/paper.jpeg")
img = cv.resize(img,(0,0),fx=0.5,fy=0.5)
# Se alamcenan en una variable las dimensiones de la magen
rows, cols, ch = img.shape
while True:
	cv.namedWindow('Imagen')
	cv.setMouseCallback('Imagen',matriz_imagen)

	cv.imshow("Imagen",img)
    # Si se pulsa escape se rompe el bucle
	if cv.waitKey(1)==27: break
cv.destroyAllWindows()

# Se leen las coordenadas que se han marcado en la imagen
coordenadas = open("coordenadas.txt").read().split("\n")
coordenadas=coordenadas[0:3]
# Se crea una variable para hacer un rectángulo
# Hay que seleccionar de izquierda a derecha
pts1 = np.float32([[int(coordenadas[0].split(" ")[0]), 
    int(coordenadas[0].split(" ")[1])], 
    [int(coordenadas[1].split(" ")[0]), 
    int(coordenadas[1].split(" ")[1])], 
    [int(coordenadas[2].split(" ")[0]), 
    int(coordenadas[2].split(" ")[1])]])
print(pts1)
# Se indica los movimientos en píxeles que se quieren hacer
pts2 = np.float32([[int(coordenadas[0].split(" ")[0])+30, 
    int(coordenadas[0].split(" ")[1])+30], 
    [int(coordenadas[1].split(" ")[0])+30, 
    int(coordenadas[1].split(" ")[1])-12], 
    [int(coordenadas[2].split(" ")[0])-40, 
    int(coordenadas[2].split(" ")[1])+15]])
print(pts2)

# Se crea una matriz de transformación que toma los tres pares de punto de entrada
# y da como salida la matriz transformada.
# cv2.getAffineTransform(src, dst)
	# src: coordenadas de la imagen de entrada
	# dst: coordenadas de la imagen de salida
matrix = cv.getAffineTransform(pts1, pts2)
# Esta función aplica una transformación de una imagen afin
	# cv2.warpAffine(src, dst, M, dsize, flags = INTER_LINEAR, 
	# borderMode = BORDER_CONSTANT,borderValue = Scalar())
################################################################################
	# src = imagen de entrada.
	# dst =	imagen de salida que tiene el tamaño dsize y el mismo tipo que src.
	# M = 2×3 matriz de transformación.
	# dsize = tamaño de la imagen de salida.
	# flags =	combinación de métodos de interpolación (ver InterpolationFlags) 
		# y el flag opcional es WARP_INVERSE_MAP que significa que M 
		# es la transformación inversa( dst→src ).
	# borderMode = método de extrapolación de píxeles (ver BorderTypes); 
		# donde borderMode=BORDER_TRANSPARENT, significa que la función no modifica 
		# los píxeles de la imagen de destino correspondientes a los "outliers" de 
		# la imagen de origen.
	# borderValue = valor utilizado en caso de un border constante; por defecto, es 0.
result = cv.warpAffine(img, matrix, (cols, rows))

# Se muestra la imagen real y la modificada
cv.imshow("Image", img)
cv.imshow("Affine transformation", result)
cv.waitKey(0)
cv.destroyAllWindows()