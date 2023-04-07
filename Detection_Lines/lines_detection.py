# Se usará la librería de Opencv para detectar las líneas de carretera de un vídeo y unir líneas
# Esto se hará con la transformada de Houg
import cv2 as cv
import numpy as np
# Se usa una bandera para detectar imágenes o vídeos
flag = 2
if flag==1:
	# Se lee la imagen a tratar
	img = cv.imread("videos_image/lines.png")
	# Se cambia a escala de grises
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	# Se detectan los bordes con el filtro Canni que es el que menos ruido genera
	edges = cv.Canny(gray, 75, 150)
	# cv2.HoughLinesP(image, lines, rho, theta, threshold, minLineLength = 0,
		# maxLineGap = 0)

		# image = Imagen de fuente binaria de un solo canal de 8 bits. La imagen puede ser modificada por la función.
		# lines	= 	Vector de salida de líneas. Cada línea está representada por un vector de 4 elementos.
			# (X1,y1,X2,y2), dónde(X1,y1)y(X2,y2)son los puntos finales de cada segmento de línea detectado.
		# rho = Resolución de distancia del acumulador en píxeles.
		# theta = Resolución angular del acumulador en radianes.
		# threshold = 	Parámetro de umbral del acumulador. 
			# Solo se devuelven aquellas líneas que obtienen suficientes votos (>umbral).
		# minLineLength = Longitud mínima de línea. Los segmentos de línea más cortos que eso son rechazados.
		# maxLineGap = Separación máxima permitida entre puntos de la misma línea para unirlos.
	lines = cv.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=250)

	# Todas las líneas encontrada se pintan en color verde y opteniendo los puntos
	for line in lines:
	    x1, y1, x2, y2 = line[0]
	    cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

	cv.imshow("Edges", edges)
	cv.imshow("Image", img)
	cv.imwrite("videos_image/1.3_lines_with_gap.jpg", img)
	cv.waitKey(0)
	cv.destroyAllWindows()
else:
	# Se lee el vídeo de las carreteras
	video = cv.VideoCapture("videos_image/road_car_view.mp4")

	while True:
	    ret, orig_frame = video.read()
	    # Se pone este condicional para cuando termine el vídeo salga del bucle
	    try: 
	    	orig_frame = cv.resize(orig_frame,(0,0),fx=0.5,fy=0.5)
	    except Exception:
	    	break
	    # Esta función se asegura de que la imagen se esté procesando
	    if not ret:
	        video = cv.VideoCapture("road_car_view.mp4")
	        continue
	    # Se aplica un filtro para evitar el ruido en el filtro
	    frame = cv.GaussianBlur(orig_frame, (5, 5), 0)
	    # Se pasa la imagen a escala de hsv para detectar los colores amarillos
	    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
	    low_yellow = np.array([18, 94, 140])
	    up_yellow = np.array([48, 255, 255])
	    # Se aplican la máscara y el filtro canny
	    mask = cv.inRange(hsv, low_yellow, up_yellow)
	    edges = cv.Canny(mask, 75, 150)
	    # Se obtienen las líneas obtenidas del filtro canny
	    lines = cv.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)
	    # Se activa un condicional para detectar si hay o no línea
	    if lines is not None:
	        for line in lines:
	            x1, y1, x2, y2 = line[0]
	            cv.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
	    # Se pinta la imagen y el filtro
	    cv.imshow("frame", frame)
	    cv.imshow("edges", edges)

	    key = cv.waitKey(1)
	    if key == 27:
	        break
	video.release()
	cv.destroyAllWindows()