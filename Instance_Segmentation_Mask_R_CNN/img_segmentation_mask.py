# Se importan las librerías para el procesamiento de imagenes y segmentación
import cv2 as cv
import numpy as np

# Se carga el modelo de tensorflow de opencv en una variable
# Lee un modelo de red almacenado en el formato del marco TensorFlow.
# cv2.readNetFromTensorflow(model, config = String())
	# model = ruta al archivo .pb con protobuf binario descripción 
		# de la arquitectura de red
	# config = ruta al archivo .pbtxt que contiene la definición 
		# del gráfico de texto en formato protobuf. El objeto neto 
		# resultante se construye mediante un gráfico de texto 
		# utilizando pesos de uno binario que nos permite hacerlo 
		# más flexible.
net = cv.dnn.readNetFromTensorflow("dnn/frozen_inference_graph_coco.pb",
	"dnn/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt")

# Se generan de manera aleatoria los colores de las máscaras
# Se generan las 80 clases de colores diferentes y tres para los
# canales RGB
colors = np.random.randint(0,255,(80,3))

# Se carga las imágenes para analizar
img = cv.imread("image/road.jpg")
# Se redimensiona para ajustarla a la pantalla
img = cv.resize(img,(0,0),fx=0.8,fy=0.8)
height, width, channels = img.shape

# Se crea una imagen en negro de las mismas dimensiones que la que
# se pretende analizar
black_img = np.zeros((height,width,channels), np.uint8)
# Se cambia el fondo de detección
black_img[:] = (100,100,0)

# Con la función cv2.dnn.blobFromImage() se detectan las diferentes
# 80 clases
# Crea un blob de 4 dimensiones a partir de una imagen. Opcionalmente, 
# cambia el tamaño y recorta imagedesde el centro, resta meanvalores, 
# escala valores por scalefactor, intercambia canales azul y rojo.
# cv::dnn::blobFromImage(image, scalefactor = 1.0, size = Size(),
	# mean = Scalar(), swapRB = false, crop = false, ddepth = CV_32F)

	# image = imagen de entrada (con 1, 3 o 4 canales).
	# scalefactor = multiplicador de imagevalores.
	# size = tamaño espacial para la imagen de salida
	# mean = escalar con valores medios que se restan de los canales. 
		# Los valores están destinados a estar en orden 
		# (media-R, media-G, media-B) si imagetiene un orden BGR 
		# y swapRBes verdadero.
	# wapRB = indicador que indica que es necesario intercambiar el 
		# primer y el último canal en una imagen de 3 canales.
	# crop = bandera que indica si la imagen se recortará después 
		# de cambiar el tamaño o no.
	# ddepth = Profundidad del blob de salida. Elija CV_32F o CV_8U.

# si cropes verdadero, la imagen de entrada cambia de tamaño para 
	# que un lado después del cambio de tamaño sea igual a la dimensión 
	# correspondiente sizey el otro sea igual o más grande. Luego, se 
	# realiza el recorte desde el centro. Si cropes falso, se realiza 
	# el cambio de tamaño directo sin recortar y conservando la 
	# relación de aspecto.
blob = cv.dnn.blobFromImage(img,swapRB=True)

# Se establece el nuevo valor de entrada para la red  con cv::dnn::Net::setInput()
	# cv::dnn::Net::setInput(blob, name = "", scalefactor = 1.0, mean = Scalar())

	# blob = Un nuevo blob. Debe tener profundidad CV_32F o CV_8U.
	# name = Un nombre de la capa de entrada.
	# scalefactor = Una escala de normalización opcional.
	# mean = Un valor de sustracción media opcional.

net.setInput(blob)

# Se almacenan en una variable los datos de las coordenadas donde se encuentran las
# clases detectadas y la mascara equivalente de la clase detectada
boxes, masks = net.forward(["detection_out_final","detection_masks"])
# Se almacena el número todo lo que ha sido detectado para recorrelo individualmente
detection_count = boxes.shape[2]

for i in range(detection_count):
	# Se pasa la coordenada del objeto detectado uno a uno y se alamacena la clase
	box = boxes[0,0,i]
	class_id = box[1]
	# Se alamcena la confianza de la predicción para poner un umbral
	score = box[2]
	if score<0.5: continue

	# Se crean las coordenadas de la caja del objeto detectado
	x = int(box[3]*width)
	y = int(box[4]*height)
	x2 = int(box[5]*width)
	y2 = int(box[6]*height)

	roi = black_img[y:y2,x:x2]
	roi_height, roi_width,_ = roi.shape

	# Se obtiene la máscara
	mask = masks[i,int(class_id)]
	mask = cv.resize(mask,(roi_width,roi_height))
	# Se umbraliza y se realiza operaciones morfológicas de apertura y cierre
	# Los datos de la máscara están entre 0 y 1
	_,mask = cv.threshold(mask,0.5,255,cv.THRESH_BINARY)
	kernel = np.ones((5, 5), np.uint8)
	mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=2)
	mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

	# Se pinta el rectangulo de los objetos detectados
	cv.rectangle(img,(x,y),(x2,y2),(255,0,0),3)

	# Se construye la máscara usando la función para encontrar contornos
	contours,_ = cv.findContours(np.array(mask,np.uint8),cv.RETR_EXTERNAL, 
		cv.CHAIN_APPROX_SIMPLE)
	# Se le asigna su color aleatorio a la clase que ha sido detectada
	color = colors[int(class_id)]
	for cnt in contours:
		# Se pinta la máscara encontrada con el color encontrado en la imagen 
		# de fondo negro (verdoso)
		cv.fillPoly(roi, [cnt], (int(color[0]),int(color[1]),int(color[2])))
	    
	# cv.imshow("roi",roi)
	# cv.waitKey(0)

# Se muestra los resultados	
cv.imshow("img",img)
cv.imshow("Black Image", black_img)
cv.waitKey(0)
cv.destroyAllWindows()