# Aquí se muestran los operadores de la librería Opencv
import cv2 as cv
import numpy as np

# Se leen dos imágenes
img1 = cv.imread("image/B_W.jpg")
img1 = cv.resize(img1, (255,255), interpolation = cv.INTER_AREA)
img2 = cv.imread("image/CR.jpg")
img2 = cv.resize(img2, (255,255), interpolation = cv.INTER_AREA)

bit_and = cv.bitwise_and(img2, img1)
# La función bitwise_and es la siguiente:
# TABLA DE VERDAD (AND)         EN OPENCV    ---->     VISUALIZACIÓN
# A B | SALIDA                  # A B | SALIDA         # A B | SALIDA
# ___ | ______                   _____|_______          _____|_______
# 0 0 |   0                       0 0 |   0              N N |   N
# 0 1 |   0               --->   0 255|   0              N B |   N
# 1 0 |   0                      255 0|   0              B N |   N
# 1 1 |   1                    255 255|  255             B B |   B


bit_or = cv.bitwise_or(img2, img1)
# La función bitwise_and es la siguiente:
# TABLA DE VERDAD (AND)         EN OPENCV    ---->     VISUALIZACIÓN
# A B | SALIDA                  # A B | SALIDA         # A B | SALIDA
# ___ | ______                   _____|_______          _____|_______
# 0 0 |   0                       0 0 |   0              N N |   N
# 0 1 |   1               --->   0 255|  255             N B |   B
# 1 0 |   1                      255 0|  255             B N |   B
# 1 1 |   1                    255 255|  255             B B |   B


bit_xor = cv.bitwise_xor(img1, img2)
# La función bitwise_and es la siguiente:
# TABLA DE VERDAD (AND)         EN OPENCV    ---->     VISUALIZACIÓN
# A B | SALIDA                  # A B | SALIDA         # A B | SALIDA
# ___ | ______                   _____|_______          _____|_______
# 0 0 |   0                       0 0 |   0              N N |   N
# 0 1 |   1               --->   0 255|  255             N B |   B
# 1 0 |   1                      255 0|  255             B N |   B
# 1 1 |   0                    255 255|   0              B B |   N


bit_not = cv.bitwise_not(img1)
# La función bitwise_and es la siguiente:
# TABLA DE VERDAD (AND)         EN OPENCV   ---->  VISUALIZACIÓN
# A | SALIDA                  # A | SALIDA         # A | SALIDA
# __| ______                   ___|_______          ___|_______
# 0 |   1                       0 |  255             N |   B
# 1 |   0               --->  255 |   0              B |   N


bit_not2 = cv.bitwise_not(img2)
# La función bitwise_and es la siguiente:
# TABLA DE VERDAD (AND)         EN OPENCV   ---->  VISUALIZACIÓN
# A | SALIDA                  # A | SALIDA         # A | SALIDA
# __| ______                   ___|_______          ___|_______
# 0 |   1                       0 |  255             N |   B
# 1 |   0               --->  255 |   0              B |   N


# Se muestran las imágenes
cv.imshow("img1", img1)
cv.imshow("img2", img2)

cv.imshow("bit_and", bit_and)
cv.imshow("bit_or", bit_or)
cv.imshow("bit_xor", bit_xor)
cv.imshow("bit_not", bit_not)
cv.imshow("bit_not2", bit_not2)

cv.waitKey()
cv.destroyAllWindows()