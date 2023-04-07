import cv2 as cv
import numpy as np
import os
# Se decide el directorio donde se va a aplicar este script
# os.chdir("/home/grasshopper41/Porfolio/Object_Tracking/pictures")

lista = os.listdir()
# if "coordenadas.txt" in lista:
# 	os.remove("coordenadas.txt")

# Se crea una variable donde almacenas los x's y las y's
xS, yS = [], []
def matriz_imagen(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(img, (x, y), 5, (0, 0, 255), -1)
        print(f'x={x} e y={y}')
        xS.append(x)
        yS.append(y)
        # Se añade más texto usando la modalidad "a"
        # archivo = open("coordenadas.txt", "a")
        # string = str(x)+" "+str(y)
        # archivo.write(string+"\n")
        # archivo.close()

def guess_coordenadas(img):
    cv.namedWindow('Imagen')
    cv.setMouseCallback('Imagen',matriz_imagen)
    
    while True:
        # Se copia la imagen para que no se copie el círculo rojo
        newImg = img.copy()
        cv.imshow('Imagen',newImg)

        k=cv.waitKey(1) & 0xFF
        if k==27: #Si pulsamos esc se cierra la imagen
            cv.destroyAllWindows()
            break
# Se pone el nombre del archivo que hay que leer
filname='digimon.jpg'
img = cv.imread(filname)
#Relacción de proporcionalidad para que la ventana emergente de cv 
#se tenga unas porporciones que se adapten a la pantalla del ordenador de las variables fx y fy
img = cv.resize(img,(0,0),fx=1,fy=1)
guess_coordenadas(img)

# Se almacenan las coordenadas en una variable x e y
# coordenadas = open("coordenadas.txt").read().split("\n")
# x1, y1 = int(coordenadas[0].split()[0]), int(coordenadas[0].split()[1])
# x2, y2 = int(coordenadas[1].split()[0]), int(coordenadas[1].split()[1])
# Se ordena las coordenadas de menor a mayor
# x_Max, x_Min = np.maximum(x1,x2), np.minimum(x1,x2)
# y_Max, y_Min = np.maximum(y1,y2), np.minimum(y1,y2)
x_Max, x_Min = np.maximum(xS[0],xS[1]), np.minimum(xS[0],xS[1])
y_Max, y_Min = np.maximum(yS[0],yS[1]), np.minimum(yS[0],yS[1])
img_new = img[y_Min:y_Max,x_Min:x_Max,:].copy()
cv.imshow('Imagen2',img_new)
cv.waitKey()
cv.destroyAllWindows()
# Se guarda la imagen
cv.imwrite('Kari.jpg',img_new)
os.remove('coordenadas.txt')