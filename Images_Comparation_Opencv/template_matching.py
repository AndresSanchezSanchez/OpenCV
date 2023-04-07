# Con la librería de opencv se buscan los puntos de coincidencias
import cv2 as cv
import numpy as np
# Se lee la imagen original
img = cv.imread("image/digimon.jpg")
# Se pasa a escala de grises
gray_img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
# Se lee el modelo en escala de grises
template = cv.imread("image/patamon.jpg",cv.IMREAD_GRAYSCALE)
# Se alamacena en dos variable el alto y el ancho del modelo para encuadrar la coincidencia
w,h = template.shape[::-1]
# Se detecta el resultado
# cv2.matchTemplate(image, templ, result, method, mask = noArray()))
	# image = Imagen donde se ejecuta la búsqueda. Debe ser de coma flotante de 8 o 32 bits.
	# templ = Plantilla buscada. No debe ser mayor que la imagen de origen y tener el mismo tipo de datos. 
	# result = Mapa de resultados de comparación. Debe ser de punto flotante de 32 bits de un solo canal.
		# Si la imagen es W×H y templ es w×h, entonces el resultado es (W−w+1)×(H−h+1) .
	# method = Parámetro que especifica el método de comparación, consulte TemplateMatchModes.
	# mask = Máscara opcional. Debe tener el mismo tamaño que templ. 
		# Debe tener la misma cantidad de canales que la plantilla o solo un canal, 
		# que luego se usa para todas las plantillas y los canales de imagen. 
		# Si el tipo de datos es CV_8U , la máscara se interpreta como una máscara binaria, 
		# lo que significa que solo se usan los elementos donde la máscara no es cero y 
		# se mantienen sin cambios independientemente del valor real de la máscara (el peso es igual a 1).
		# Para el tipo de datos CV_32F , los valores de máscara se utilizan como pesos. 
		# Las fórmulas exactas están documentadas en TemplateMatchModes.

# Se obtiene el resultado que devuelve un punto blanco como una especie de mapa
result = cv.matchTemplate(gray_img, template, cv.TM_CCOEFF_NORMED)
# Con la variable loc se buscan los puntos cercanos al color blanco para detectar coincidencias
loc = np.where(result >= 0.9)

# Se analizan todos los puntos para pintarlos en la imagen orifinal
# La función de Python zip()se define como zip(*iterables). 
# La función toma iterables como argumentos y devuelve un iterador.
# Este iterador genera una serie de tuplas que contienen elementos de cada iterable. 
# zip()puede aceptar cualquier tipo de iterable, como archivos ,
# listas, tuplas , diccionarios , conjuntos , etc.
for pt in zip(*loc[::-1]):
	cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
cv.imshow('imagen',img)
cv.imshow('gray_img',gray_img)
cv.imshow('template',template)
cv.imshow('result',result)
cv.waitKey()
cv.destroyAllWindows()