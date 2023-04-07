# Se filtra por colores a través de las barras
import cv2
import numpy as np

# Se crea una función de apoyo para las barras de desplazamiento
def nothing(x):
    pass

# Se abre la cámara para capturar la imagen frame a frame
cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")

# Se crean seis barras de desplazamiento mostrando los límites
cv2.createTrackbar("L - H", "Trackbars", 0, 360, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 360, 360, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

# Se abre un bucle para que se muestre mientras no se pulse la tecla de escape
while True:
    # Se muestra el resultado frame a frame y se cambia a la escala HSV
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # se leen los valores de las barras de manera interactiva
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    
    # Se filtran los valores de azul tanto altos como bajo
    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower, upper)
    
    # Con la función bitwise_and se mezclan las dos fotos usando la máscara
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Muestra la imagen
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)
    
    # Cuando se pulsa escape se sale de la pantalla
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()