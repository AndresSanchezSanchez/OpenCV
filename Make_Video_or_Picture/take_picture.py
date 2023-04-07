# Con este código se puede hacer una foto de con la cámara
import cv2 as cv
import os
# Se decide el directorio donde se guardará el vídeo
os.chdir("/home/grasshopper41/Porfolio/Object_Tracking/Object_Tracking")
# Se abre la cámara para hacer la foto
cap = cv.VideoCapture(0)
ret,frame = cap.read()
cv.imwrite("pictures/frame.jpg",frame)
cap.release()
cv.imshow("Frame",frame)
cv.waitKey()
cv.destroyAllWindows()