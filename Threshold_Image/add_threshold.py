# Se le añande un humbral a las imágenes para segmentar
import cv2 as cv
import numpy as np

img1 = cv.imread("fotos/Spider-Man.jpg")
# Se realiza una parte del código para redimensionar las imágenes
img1 = cv.resize(img1, (640,640), interpolation = cv.INTER_AREA)

img2 = cv.imread("fotos/Andrés.jpg")
# Se realiza una parte del código para redimensionar las imágenes
img2 = cv.resize(img2, (640,640), interpolation = cv.INTER_AREA)

# Se convierte la imagen dos a escala de grises
img2_gray = cv.cvtColor(img2,cv.COLOR_BGR2GRAY)

# Se aplica un humbral
ret, threshold = cv.threshold(img2_gray,150,255,cv.THRESH_BINARY)

# Se suma las imágenes
suma = cv.add(img2,img2, mask=threshold)

# Se usa la función addWeighted que es otra forma de sumar imágnes con pesos ponderados
weighted = cv.addWeighted(img1,1,img2,0.5,0)

# Usar una máscara mezclando imágenes
joint = cv.bitwise_and(img1,img1,mask=threshold)
threshold_inv = cv.bitwise_not(threshold)
joint_2 = cv.bitwise_and(img2,img2,mask=threshold_inv)

# Se muestran las imágenes en pantalla
cv.imshow("joint",joint)
cv.imshow("joint_2",joint_2)
cv.imshow("suma",suma)
cv.imshow("threshold",threshold)
cv.imshow("threshold_inv",threshold_inv)
cv.imshow("weighted",weighted)
cv.imshow("img1",img1)
cv.imshow("img2",img2)
cv.imshow("img2_gray",img2_gray)
cv.waitKey()
cv.destroyAllWindows()