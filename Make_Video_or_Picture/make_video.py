# Usando la librería de opencv se crea un vídeo y se
import cv2 as cv
import os
# Se decide el directorio donde se guardará el vídeo
os.chdir("/home/grasshopper41/Porfolio/Object_Tracking/Object_Tracking/pictures")
# Se abre la cámara web del ordenador
cap = cv.VideoCapture(0)
# Se activa la función para escirbir cada frame
out = cv.VideoWriter('video.avi',
  cv.VideoWriter_fourcc(*'XVID'),20.0,(640,480))
# Mientras la cámara esté abierta se repite el bucle o se pulse la tecla ec o "s"
while (cap.isOpened()):
  ret, img = cap.read()
  if ret == True:
    cv.imshow('video', img)
    out.write(img)
    if cv.waitKey(1) & 0xFF == ord('s'): break
  else: break
# Se cierra la cámara y se rompen todas las ventanas
cap.release()
out.release()
cv.destroyAllWindows()