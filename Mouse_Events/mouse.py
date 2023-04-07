import cv2
import numpy as np
# Valores de los eventos del ratón de cv2.setMouseCallback
# event
    # cv2.EVENT_MOUSEMOVE = 0, indica que el puntero del mouse  se ha movido por la ventana.
    # cv2.EVENT_LBUTTONDOWN = 1, indica que el botón izquierdo del mouse es presionado.
    # cv2.EVENT_RBUTTONDOWN = 2, indica que el botón derecho del mouse es presionado.
    # cv2.EVENT_MBUTTONDOWN = 3, indica que el botón central del mouse es presionado.
    # cv2.EVENT_LBUTTONUP = 4, indica que se suelta el botón izquierdo del ratón.
    # cv2.EVENT_RBUTTONUP = 5, indica que se suelta el botón derecho del ratón.
    # cv2.EVENT_MBUTTONUP = 6, indica que se suelta el botón central del ratón.
    # cv2.EVENT_LBUTTONDBLCLK = 7, indica que se hace doble clic en el botón izquierdo del ratón.
    # cv2.EVENT_RBUTTONDBLCLK = 8, indica que se hace doble clic en el botón derecho del ratón.
    # cv2.EVENT_MBUTTONDBLCLK = 9, indica que se hace doble clic en el botón central del ratón.
    # cv2.EVENT_MOUSEWHEEL = 10, desplazamiento (scrolling) del ratón adelante y atrás.
    # cv2.EVENT_MOUSEHWHEEL = 11, desplazamiento (scrolling) del ratón izquierda y derecha.

# x representa la coordenada x del evento del ratón
# y representa la coordenada y del evento del ratón

#flags
    # cv2.EVENT_FLAG_LBUTTON = 1, indica que el botón izquierdo del mouse está presionado.
    # cv2.EVENT_FLAG_RBUTTON = 2, indica que el botón derecho del mouse está presionado.
    # cv2.EVENT_FLAG_MBUTTON = 4, indica que el botón central del mouse está presionado.
    # cv2.EVENT_FLAG_CTRLKEY = 8, indica que la tecla CTRL está presionada.
    # cv2.EVENT_FLAG_SHIFTKEY = 16, indica que la tecla SHIFT está presionada.
    # cv2.EVENT_FLAG_ALTKEY = 32, indica que la tecla ALT está presionada.

def drawing(event,x,y,flags,param):
    # Imprimimos la información sobre los eventos que se estén realizando
    print('-----------------------------')
    print('event=',event)
    print('x=',x)
    print('y=',y)
    print('flags=',flags)
    # Ejemplos de acciones con algunos eventos del mouse
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(imagen,(x,y),20,(255,255,255),2)
    if event == cv2.EVENT_RBUTTONDOWN:
        cv2.circle(imagen,(x,y),20,(0,0,255),2)
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(imagen,(x,y),10,(255,0,0),-1)
    if event == cv2.EVENT_RBUTTONDBLCLK:
        cv2.circle(imagen,(x,y),10,(0,255,0),-1)
    if event == cv2.EVENT_LBUTTONUP:
        cv2.putText(imagen,'Ha dejado de presionar (Izquierdo)',(x,y),2,0.4,(255,255,0),1,cv2.LINE_AA)
    if event == cv2.EVENT_RBUTTONUP:
        cv2.putText(imagen,'Ha dejado de presionar (Derecho)',(x,y),2,0.4,(0,255,255),1,cv2.LINE_AA)
imagen = np.zeros((480,640,3),np.uint8)
imagen = cv2.imread('Saturation_Spider-Man.jpg')
cv2.namedWindow('Imagen')
cv2.setMouseCallback('Imagen',drawing)
while True:
    cv2.imshow('Imagen',imagen)
    
    k = cv2.waitKey(1) & 0xFF
    if k == ord('l'): # Limpiar el contenido de la imagen
        imagen = np.zeros((480,640,3),np.uint8)
    elif k == 27:
        break
cv2.destroyAllWindows()
