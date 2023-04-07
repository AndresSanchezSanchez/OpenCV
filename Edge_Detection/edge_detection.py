# Detección de bordes con la librería de opencv
import cv2 as cv
import numpy as np
# Se hará en imágenes y en tiempo real con la webcam

# Se crea una bandera para determinar si uso la webcan o imágenes
flag = 2
if flag==1:
	img = cv.imread("image/Black_Spider-Man.jpg", cv.IMREAD_GRAYSCALE)
	img = cv.resize(img,(0,0),fx=0.6,fy=0.6)
	# Se le aplican tres filtros de detección de bordes
		# Sobel
		# Laplacian
		# Canny
	# Se le aplica un filtro gausiano para difuminar la imagen
	img = cv.GaussianBlur(img,(5,5),0)
	# Se analiza el filtro sobel en x e y
	soblex = cv.Sobel(img,cv.CV_64F,1,0)
	sobley = cv.Sobel(img,cv.CV_64F,0,1)
	# Se aplica un filtro laplacian
	laplacian = cv.Laplacian(img,cv.CV_64F,ksize=5)
	# Finalmente se aplica el filtro canny que elimina más ruido
	canny = cv.Canny(img, 100 ,  150) 
	cv.imshow('Imagen',img)
	cv.imshow('soblex',soblex)
	cv.imshow('sobley',sobley)
	cv.imshow('laplacian',laplacian)
	cv.imshow('canny',canny)
	cv.waitKey(0)
	cv.destroyAllWindows()

else:
	# Se hace lo mismo pero con la webcan
	cap = cv.VideoCapture(0)
	while True:
	    # Se muestra el resultado frame a frame y se cambia a la escala HSV
	    _, frame = cap.read()
	    frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
	    frame = cv.resize(frame,(0,0),fx=0.5,fy=0.5)
		# Se le aplica un filtro gausiano para difuminar la imagen
	    frame = cv.GaussianBlur(frame,(5,5),0)
		# Se analiza el filtro sobel en x e y
	    soblex = cv.Sobel(frame,cv.CV_64F,1,0)
	    sobley = cv.Sobel(frame,cv.CV_64F,0,1)
		# Se aplica un filtro laplacian
	    laplacian = cv.Laplacian(frame,cv.CV_64F,ksize=5)
		# Finalmente se aplica el filtro canny que elimina más ruido
	    canny = cv.Canny(frame, 100 ,  150)
	    cv.imshow('Imagen',frame)
	    cv.imshow('soblex',soblex)
	    cv.imshow('sobley',sobley)
	    cv.imshow('laplacian',laplacian)
	    cv.imshow('canny',canny)
	    key = cv.waitKey(1)
	    if key == 27: break
	cap.release()
	cv.destroyAllWindows()