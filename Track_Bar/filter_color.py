# Usando la librería de Opencv se puede filtrar por color con barras de desplazamiento
import cv2 as cv
import numpy as np

#Se carga la imagen de un dibujo con la librería de cv2
filname='Spider-Man.jpg'
img = cv.imread(filname)

# Función mostrar en pantalla las coordenadas del pixel seleccionado
def matriz_imagen(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(im_c,(x,y),15,(0,255,0),2)
        print(f'x={x} e y={y}')
        # Se crea un archivo txt donde se almacena la última coordenada presionada
        string = str(x)+" "+str(y)
        archivo = open("coordenadas.txt","w")
        archivo.write(string)
        archivo.close()


def guess_coordenadas(im_c):
    #Relacción de proporcionalidad para que la ventana emergente de cv 
    #se tenga unas porporciones que se adapten a la pantalla del ordenador de las variables fx y fy
    fx=1
    fy=1
    cv.namedWindow('Imagen')
    cv.setMouseCallback('Imagen',matriz_imagen)
    
    while True:
        newImg = cv.resize(im_c, (0,0), fx=fx, fy=fy)
        cv.imshow('Imagen',newImg)

        k=cv.waitKey(1) & 0xFF
        if k==27: #Si pulsamos esc se cierra la imagen
            cv.destroyAllWindows()
            break
            
#Función de lectura de la imagen para selecionar el pixel
def imagen(name):
    im_c=cv.imread(name)
    return im_c

# Se obtiene las coordenadas para filtrar por color
im_c=imagen(filname)
guess_coordenadas(im_c)

# Se almacenan las coordenadas en una variable x e y
coordenadas = open("coordenadas.txt").read().split(" ")
x, y = int(coordenadas[0]), int(coordenadas[1])

# Se crea una función para mostrar el color seleccionado en las coordenadas x,y
def muestra(x,y,fx,fy,im):
    #Hay que tener en cuenta los coeficientes de fx y fy porque las coordenadas obtenidas son de una imágen igual 
    #pero reducida en esa proporción y por tanto hay que buscar las coordenadas reales
    if im.shape[1]<round(x/fx):
        #el objetivo es que no se salga de los límites de la imagen original con un redondeo
        a1=im.shape[1]-1
    else:
        a1=round(x/fx)
    if im.shape[0]<round(y/fy):
        a2=im.shape[0]-1
    else:
        a2=round(y/fy)
    #Se sacan lo valores del canal RGB con esas coordenadas de la imagen real
    v=im[a2,a1]
    print(v)
    #Se crea una imágen con esos valores de RGB de 640x640
    R=np.ones((640, 640))*v[0]
    G=np.ones((640, 640))*v[1]
    B=np.ones((640, 640))*v[2]
    total=[R,G,B]
    #Se convinan los tres canales
    total=np.stack(total,axis=2)
    total=total.astype('uint8')
    
    cv.imshow('color',total)
    cv.waitKey()
    cv.destroyAllWindows()
    #devuelve las coordenadas de la imagen original sin aplicar escala
    return a1, a2
#Aplicamos la función con los datos de coordenadas escalados al 1 tanto en x como en y
xR, yR = muestra(x,y,1,1,img)

# Hay que cambiar las coordenadas del color de formato BGR a formato HSV
# Para ello se crea la siguiente función
def rgb_to_hsv(vetor): 
    b, g, r = vetor[0]/255, vetor[1]/255, vetor[2]/255
    maxc, minc = max(r, g, b), min(r, g, b) 
    v = maxc 
    if minc == maxc: 
        return 0, 0, int(v) 
    s = (maxc-minc) / maxc 
    rc = (maxc-r) / (maxc-minc) 
    gc = (maxc-g) / (maxc-minc) 
    bc = (maxc-b) / (maxc-minc) 
    if r == maxc: 
        h = 0.0+bc-gc 
    elif g == maxc: 
        h = 2.0+rc-bc 
    else: 
        h = 4.0+gc-rc 
    h = (h/6.0) % 1.0 
    return int(h * 360), int(s * 100), int(v * 100)
# Se obtiene el valor de HSV de las coordenadas marcadas
p_hsv = rgb_to_hsv(img[yR,xR])

# Función de apoyo para las trackbar
def nothing(x):
    pass

cv.namedWindow("Trackbars")
#Mediante barras se determina cual será el humbral de manera interactiva
#Los valores máximos
max_H=360
max_S=255
max_V=255
#Son los valores mínimos controlando que estas variables no se salgan de los límites en su valor mínimo del rango
min_H=p_hsv[0]+40
if min_H>360:
    min_H=360
min_S=p_hsv[1]+40
if min_S>100:
    min_S=255
min_V=p_hsv[2]+40
if min_V>100:
    min_V=255

#Se crean las barras para modular
cv.createTrackbar("L-H","Trackbars",0,min_H,nothing)
cv.createTrackbar("L-S","Trackbars",0,min_S,nothing)
cv.createTrackbar("L-V","Trackbars",0,min_V,nothing)
cv.createTrackbar("U-H","Trackbars",max_H,max_H,nothing)
cv.createTrackbar("U-S","Trackbars",max_S,max_S,nothing)
cv.createTrackbar("U-V","Trackbars",max_V,max_V,nothing)

#Con un while se vuelve interactivo y se actualiza el resultado hasta pulsar la tecla esc
#Después se mostrarán los humbrales
while True:
    hsv = cv.cvtColor(img.copy(), cv.COLOR_BGR2HSV)
    
    l_h= cv.getTrackbarPos("L-H","Trackbars")
    l_s= cv.getTrackbarPos("L-S","Trackbars")
    l_v= cv.getTrackbarPos("L-V","Trackbars")
    u_h= cv.getTrackbarPos("U-H","Trackbars")
    u_s= cv.getTrackbarPos("U-S","Trackbars")
    u_v= cv.getTrackbarPos("U-V","Trackbars")
    
    lower = np.array([l_h,l_s,l_v])
    upper = np.array([u_h,u_s,u_v])
    mask=cv.inRange(hsv,lower,upper)
    result=cv.bitwise_and(img,img,mask=mask)
    #Se reduce un 45% la escala de la imagen para mostrar los efectos que ocurren
    fx=0.45
    fy=0.45
    newImg = cv.resize(img, (0,0), fx=fx, fy=fy)
    
    newMask = cv.resize(mask, (0,0), fx=fx, fy=fy)
    
    newresult = cv.resize(result, (0,0), fx=fx, fy=fy)
    
    cv.imshow("mask",newMask)
    cv.imshow("frame",newImg)
    cv.imshow("result",newresult)
    
    key=cv.waitKey(1)
    if key==27:
        print(l_h,l_s,l_v,u_h,u_s,u_v)
        print(lower)
        print(upper)
        break

cv.destroyAllWindows()