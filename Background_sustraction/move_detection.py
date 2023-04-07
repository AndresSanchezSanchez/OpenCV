# Se usará la librería de opencv para substraer el fondo y detectar movimiento
from tkinter import Frame
import cv2 as cv
import numpy as np
import os

video = "centro_comercial.mp4"

cap = cv.VideoCapture("./video/"+video)

########### Se lee el primer fotograma ###########
# Lo que se pretende es identificar los puntos donde se 
# quiere que se haga el detector de movimiento
def matriz_imagen(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(img, (x, y), 5, (0, 0, 255), -1)
        print(f'x={x} e y={y}')
        # Se añade más texto usando la modalidad "a"
        archivo = open("coordenadas.txt", "a")
        string = str(x)+" "+str(y)
        archivo.write(string+"\n")
        archivo.close()
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

ret, img = cap.read()

guess_coordenadas(img)

coordenadas = open("coordenadas.txt").read().split("\n")
x1, y1 = int(coordenadas[0].split()[0]), int(coordenadas[0].split()[1])
x2, y2 = int(coordenadas[1].split()[0]), int(coordenadas[1].split()[1])
x3, y3 = int(coordenadas[2].split()[0]), int(coordenadas[2].split()[1])
x4, y4 = int(coordenadas[3].split()[0]), int(coordenadas[3].split()[1])
# Se ordenan en sentido horario
# Se almacenan todas las x's e y's por separado
xS = [x1,x2,x3,x4]
yS = [y1,y2,y3,y4]
# 1º se busca la x más pequeña de la imagen
# Se busca el valor de x mínimo, se localiza el índice, y luego se asigna
# la segunda x más pequeña y se comparan con las yS. La que tenga la y
# más pequeña corresponderá al punto 1 y la otra al punto 2
x_Min = np.amin(xS)
index_x = xS.index(x_Min)
x1, y1 = xS[index_x], yS[index_x]
xS.pop(index_x)
yS.pop(index_x)

x_Min = np.amin(xS)
index_x = xS.index(x_Min)
x2, y2 = xS[index_x], yS[index_x]
xS.pop(index_x)
yS.pop(index_x)

if y1<y2:
    x1P, y1P, x2P, y2P = x1, y1, x2, y2
else:
    x1P, y1P, x2P, y2P = x2, y2, x1, y1


# 2º se busca la y más grande de la imagen
# Se busca el valor de y máximo, se localiza el índice, se le asigna el
# punto 3 y se saca esos puntos del array de xS e yS
y_Max = np.amax(yS)
index_y = yS.index(y_Max)
x3P, y3P = xS[index_y], yS[index_y]
xS.pop(index_y)
yS.pop(index_y)
# 4º se le asigna el punto que queda en los arrays de xS y yS
x4P, y4P = xS[0], yS[0]

#########################################################


# Se crea el modelo para substraer los datos de movimiento.
# Esto se hace con un algoritmo de segmentación de fondo de
# primer plano basado en una mezcla gaussiana.
# fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
fgbg = cv.createBackgroundSubtractorMOG2()

# Se crea un kernel para posteriormente suabizar la imagen 
# para evitar que detecte imágenes muy pequeñas
# La función cv2.getStructuringElement() devuelve un elemento
# estructurante del tamaño y forma especificados para 
# operaciones morfológicas.

    # cv2.getStructuringElement(shape, ksize, anchor = Point(-1,-1))
        # shape = Forma de elemento que podría ser uno de MorphShapes
        # ksize = Tamaño del elemento estructurante.
        # anchor = Posición del ancla dentro del elemento. El valor 
        # predeterminado( -1 , -1 ) _ _significa que el ancla está en 
        # el centro. Tenga en cuenta que solo la forma de un elemento 
        # en forma de cruz depende de la posición del ancla. En otros 
        # casos, el ancla simplemente regula cuánto se desplaza el 
        # resultado de la operación morfológica.
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(2,2))
# Se genera aleatoriamente el un color que se usará
color = np.random.randint(0, high=255, size=3, dtype=int)
color = (int(color[0]),int(color[1]),int(color[2]))
while True:
    ret, img = cap.read()

    # Cuando termina el vídeo, se repite otra vez
    if ret==False: 
        cap = cv.VideoCapture("./video/"+video)
        ret, img = cap.read()

    # Se pasa cada frame en escala de grises
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    # Se crea un recuadro donde se indica si se ha detectado
    # movimiento o no se ha detectado
    cv.rectangle(img,(0,0), (img.shape[1],40), (0,0,0),-1)
    state_text = "Estado: No se ha detectado movimiento"

    # Se visualiza el estado de la detección del movimiento
    cv.putText(img, state_text, (10,30), cv.FONT_HERSHEY_SIMPLEX,1,
    color, 2)

    # Se especifica el área donde se detectará el movimiento
    area_points = np.array([[x1P,y1P],[x2P,y2P],[x3P,y3P],[x4P,y4P]])
    #area_points = np.array([[240,320], [480,320], [620,img.shape[0]], [50,img.shape[0]]])

    # Se genera una imagen donde se verá el área de actuación 
    # de detección de movimiento apoyado en una imagen auxiliar
    imAux = np.zeros(shape=(img.shape[:2]), dtype=np.uint8)
    imAux = cv.drawContours(imAux,[area_points],-1,(255),-1)
    image_area = cv.bitwise_and(gray,gray,mask=imAux)

    # Se busca la imagen binaria donde la región en blanco y negro
    # representa la existencia de algún tipo de movimiento
    # Se aplica la imagen al modelo
    fgmask = fgbg.apply(image_area)
    fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)
    fgmask = cv.dilate(fgmask, None, iterations=2)

    # Se buscan los contornos presentes en fgmask, para encontrar
    # áreas más grandes que ayuden a determinar el movimiento
    
    cnts = cv.findContours(fgmask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    for cnt in cnts:
        if cv.contourArea(cnt) > 100:
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(img,(0,0), (img.shape[1],40), (0,0,0),-1)
            cv.rectangle(img, (x,y), (x+w, y+h),(0,255,0), 2)
            state_text = "Estado: Alerta Movimiento Detectado!"
            color = (int(color[0]),int(color[1]),int(color[2]))  
        # Se busca el área alrededor del cuerpo en movimiento
        cv.drawContours(img, [area_points], -1, color, 2)
        cv.putText(img, state_text , (10, 30),
                cv.FONT_HERSHEY_SIMPLEX, 1, color,2)

    
    cv.imshow("image",img)
    # cv.imshow("gray",gray)
    # cv.imshow("image_area",image_area)
    # cv.imshow("fgmask",fgmask)

    k = cv.waitKey(15)
    if k == 27: break

cap.release()
cv.destroyAllWindows()
os.remove('coordenadas.txt')