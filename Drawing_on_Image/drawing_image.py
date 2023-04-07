# Modelo para dibujar en imágenes
import cv2 as cv
import numpy as np

# Se lee foto a dibujar 
image = cv.imread("animals/mapache.jpg")
# Se realiza una parte del código para ajustarlo a la escala
scale = 100
dim = (int(image.shape[1] * scale / 100), 
	int(image.shape[1] * scale / 100))
image = cv.resize(image, dim, interpolation = cv.INTER_AREA)

# Se determina cual es la dimensión de la imagen que se muestra a continuación
print("#####################################################################")
print("#####################################################################")
print("#####################################################################")
print(image.shape)
print("#####################################################################")
print("#####################################################################")
print("#####################################################################")

# Se determinan los colores que se usarán para dibujar
blue = (255,0,0)
green = (0,255,0)
red = (0,0,255)
white = (255,255,255)
black = (0,0,0)

# Se pinta la línea
cv.line(image, (92,19), (187,27), blue, thickness = 5)
# Se pinta un círculo
cv.circle(image, (150,200),10, red,-1)
# Se pinta un rectángulo
cv.rectangle(image, (92,28), (166,75), green, -1)
# Se pinta una elipse
cv.ellipse(image, (140,130),(30,20),5,90,360,white,-1)
# Se pinta una polilínea
points = np.array([[[120,120], [100,200], [50,30], [280,280]]], np.int32)
cv.polylines(image,[points],True, black, thickness=2)
# Se pone texto
font = cv.FONT_HERSHEY_COMPLEX
cv.putText(image,"Mapache", (1,50), font, 2, red)

# Se muestra la imagen
cv.imshow('image',image)
cv.waitKey()
cv.destroyAllWindows()