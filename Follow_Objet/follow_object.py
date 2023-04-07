# Se usa la librería de Opencv para seguir el flujo óptico con el algoritmo Lucas-Kanade
import cv2 as cv
import numpy as np

# Se abre la cámara para poder detectar ese movimiento
cap = cv.VideoCapture(0)

# Se crea un frame inicial para poder realizar ese seguimiento
ret, frame = cap.read()
initial_frame_gray = cv.cvtColor(frame.copy(),cv.COLOR_BGR2GRAY)

# Para desplegar el algoritmo de Lucas-Kanade se definmen previamente los parámetros explicados debajo
lk_params = dict(winSize=(15,15), maxLevel=4, 
	criteria= (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT,10,0.03))
# Para usar el puntero de ratón, se crea una función de ratón y se usan funciones globales
# Nota. Rervisar las funciones globales para mejorar tus códidos
def select_point(event,x,y,flags,params):
	# Se declaran como globales las variables point, point_selected y old_points
	global point, point_selected, old_points
	if event == cv.EVENT_LBUTTONDOWN:
		point = (x,y)
		point_selected = True
		# Se marca el punto antiguo y se convierte en una matriz
		old_points = np.array([[x,y]], dtype=np.float32)

# Para usar la función anterior hay que llamar a las funciones del ratón
cv.namedWindow("frame")
cv.setMouseCallback("frame",select_point)
# Se inicializan las variables globales
point = ()
point_selected = False
old_points = np.array([[]])

# Se entra en el bucle donde se aplicará el algoritmo de Lucas-Kanade
while True:
	# Se lee los datos de la cámara
	ret,frame = cap.read()
	# Se aplica la función simetrica
	frame = cv.flip(frame,1)
	# Se pasa el resultado a escala de grises, porque el algoritmo funciona en escala de grises
	frame_gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
	# Se abre una condición preguntando si se ha seleccionado algún punto
	if point_selected is True:
		# Se pinta un círculo donde se hizo clic
		cv.circle(frame,point,6,(255,50,255),2)
		# Ahora se aplica el algoritmo con la función cv2.calcOpticalFlowPytLK()
		# cv2.calcOpticalFlowPytLK(prevImg, nextImg, prevPts, nextPts, status, err, winSize = Size(21, 21),
			# maxLevel = 3, criteria = TermCriteria(TermCriteria::COUNT+TermCriteria::EPS, 30, 0.01),
			# flags = 0, minEigThreshold = 1e-4)

			# prevImg = primera imagen o pirámide de entrada de 8 bits construida por buildOpticalFlowPyramid.
			# nextImg = segunda imagen de entrada o pirámide del mismo tamaño y del mismo tipo que prevImg.
			# prevPts = vector de puntos 2D para los que se necesita encontrar el flujo; las coordenadas de los 
				# puntos deben ser números de punto flotante de precisión simple.
			# nextPts = vector de salida de puntos 2D (con coordenadas de punto flotante de precisión simple) 
				# que contienen las nuevas posiciones calculadas de las entidades de entrada en la segunda imagen;
				# cuando se pasa el indicador OPTFLOW_USE_INITIAL_FLOW, el vector debe tener 
				# el mismo tamaño que en la entrada.
			# status = vector de estado de salida (de caracteres sin firmar); cada elemento del vector 
				# se establece en 1 si se ha encontrado el flujo para las características correspondientes;
				# de lo contrario, se establece en 0.
			# err = vector de salida de errores; cada elemento del vector se establece en un error para la 
				# característica correspondiente, el tipo de medida de error se puede establecer en el 
				# parámetro de banderas; si no se encontró el flujo, entonces el error no está definido 
				# (use el parámetro de estado para encontrar tales casos).
			# winSize = tamaño de la ventana de búsqueda en cada nivel de la pirámide.
			# maxLevel =  número de nivel de pirámide máximo basado en 0; si se establece en 0, no se utilizan 
				# pirámides (un solo nivel), si se establece en 1, se utilizan dos niveles, y así sucesivamente;
				# si las pirámides se pasan a la entrada, el algoritmo usará tantos niveles como las pirámides tengan,
				# pero no más que maxLevel.
			# criteria = parámetro, que especifica los criterios de finalización del algoritmo de búsqueda iterativa
				# (después del número máximo especificado de iteraciones criterio.maxCount o cuando la ventana de 
				# búsqueda se mueve menos de criterio.epsilon.
			# flags =  banderas de operación:
				# OPTFLOW_USE_INITIAL_FLOW usa estimaciones iniciales, almacenadas en nextPts; 
					# si el indicador no está establecido, entonces prevPts se copia en nextPts y
					# se considera la estimación inicial.
				# OPTFLOW_LK_GET_MIN_EIGENVALS utiliza valores propios mínimos como medida de error 
					# (consulte la descripción de minEigThreshold); si la bandera no está configurada,
					# entonces la distancia L1 entre los parches alrededor del original y un punto movido,
					# dividida por el número de píxeles en una ventana, se usa como medida de error.
			# minEigThreshold = el algoritmo calcula el valor propio mínimo de una matriz normal 2x2 de ecuaciones 
				# de flujo óptico (esta matriz se denomina matriz de gradiente espacial), dividida por el número de 
				# píxeles en una ventana; si este valor es menor que minEigThreshold, entonces se filtra la función
				# correspondiente y su flujo no se procesa, por lo que permite eliminar puntos defectuosos y
				# obtener un aumento del rendimiento.
		new_points, status, error = cv.calcOpticalFlowPyrLK(prevImg=initial_frame_gray, nextImg=frame_gray,
			prevPts=old_points, nextPts=None, **lk_params)
		# Se actualiza la imagen inicial tara seguir el movimiento
		initial_frame_gray = frame_gray.copy()
		# Los nuevos pasan a ser los puntos viejos
		old_points=new_points
		# Se convierten los datos en una matriz plana y se actualizan los nuevos puntos
		x,y = new_points.ravel()
		# Se convierten las coordenadas en números enteros
		x,y =int(x),int(y)
		# Se dibuja la bolita de seguimiento
		cv.circle(frame,(x,y),5,(174,255,174),-1)


	cv.imshow("frame",frame)
	key=cv.waitKey(1)
	if key==27: break

cap.release()
cv.destroyAllWindows()