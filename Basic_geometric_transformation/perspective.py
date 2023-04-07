# Usando las librerías de Opencv se va a variar la perspectiva de una imagen
import cv2 as cv
import numpy as np

# Se crea un archivo txt para almacenar las coordenadas
file = open("coordenadas.txt","w")

# Se crea una matriz para señalar los puntos en la imagen
def matriz_imagen(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(frame, (x, y), 5, (0, 0, 255), -1)
        print(f'x={x} e y={y}')
        # Se añade más texto usando la modalidad "a"
        archivo = open("coordenadas.txt", "a")
        string = str(x)+" "+str(y)
        archivo.write(string+"\n")
        archivo.close()


# Se lee la imagen de la cámara
cap = cv.VideoCapture(0)
# Se almacena la lectura en un frame
_,frame = cap.read()

while True:
	cv.namedWindow('frame')
	cv.setMouseCallback('frame',matriz_imagen)

	cv.imshow("frame",frame)
    # Si se pulsa escape se rompe el bucle
	if cv.waitKey(1)==27: break

# Se cierra la cámara y se destrullen todas las ventanas
cap.release()
cv.destroyAllWindows()

# Se leen las coordenadas que se han marcado en el screanshot y se coge
# las 4 coordenadas iniciales
coordenadas = open("coordenadas.txt").read().split("\n")
coordenadas=coordenadas[0:4]
# Se crea una variable para hacer un rectángulo
# Hay que seleccionar de izquierda a derecha
pts1 = np.float32([[int(coordenadas[0].split(" ")[0]), 
    int(coordenadas[0].split(" ")[1])], 
    [int(coordenadas[1].split(" ")[0]), 
    int(coordenadas[1].split(" ")[1])], 
    [int(coordenadas[2].split(" ")[0]), 
    int(coordenadas[2].split(" ")[1])], 
    [int(coordenadas[3].split(" ")[0]), 
    int(coordenadas[3].split(" ")[1])]])
print(pts1)
# Se usa el tamaño de la imagen capturada para la nueva resulución
pts2 = np.float32([[0, 0], [frame.shape[0], 0], [0, frame.shape[1]], 
    [frame.shape[0], frame.shape[1]]])
print(pts2)
# Se crea una matriz de transformación con la función cv2.getPerspectiveTransform()
matrix = cv.getPerspectiveTransform(pts1, pts2)
# Se almacena el alto y el ancho
height, weight = frame.shape[0], frame.shape[1]
print(height,weight)

# Se muestra la imagen transformadas
cap = cv.VideoCapture(0)
while True:
    # Se lee la cámara de nuevo
    _, frame = cap.read()
    # Se aplica la transformación con la función cv2.warpPerspective()
    result = cv.warpPerspective(frame, matrix, (height, weight))
    cv.imshow("Frame", frame)
    cv.imshow("Perspective transformation", result)
    key = cv.waitKey(1)
    if key == 27: break
cap.release()
cv.destroyAllWindows()