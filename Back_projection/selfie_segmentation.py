# Se usará la librería de opencv y mediapipe para hacer
# segmentación de los selfies d euna imagen
import cv2 as cv
import mediapipe as mp
import numpy as np

# Se carga el modelo de mediapipe con la función
# mediapipe.solutions.selfie_segmentation


mp_selfie_segmentation = mp.solutions.selfie_segmentation

# Se puede hacer tanto con la webcam o en fotos
# Para ello se crea una bándera que si tiene el valor 0, se aplica a una
# imagen dada, y si un valor diferente se aplica a la webcam
flag = 1

# Se accede a la función SelfieSegmentation del modelo ya creado
# Existen dos timpos de segmentación, la que tiene el model_selection
# igual a 0 y la que es igual a 1
with mp_selfie_segmentation.SelfieSegmentation(
    model_selection=0) as selfie_segmentation:
    
    if flag == 0:
        # Se carga la imagen que se va a tratar
        img = cv.imread("photos/selfie.jpg")
        # Se cambian los colores de BGR a RGB
        img_rgb = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        # Se aplica el procesamiento de la imagen para obtener el selfie
        results = selfie_segmentation.process(img_rgb)
        # Con el resultado se obtiene la mascara de la imagen
        mask = results.segmentation_mask
        
        
        cv.imshow("Image",img)
        cv.imshow("Image_RGB",img_rgb)
        cv.imshow("Mask",mask)
        cv.waitKey()
    else:
        cap = cv.VideoCapture(0)
        background = cv.imread("back_ground/winterfell.jpg")
        background = cv.resize(background,(1280,672)) 
        while True:
           
            ret, img = cap.read()
            # Se crea un marco mayor donde se ajuste la imagen al backgraund
            great_img = np.zeros_like(background)
            great_img[great_img.shape[0]-img.shape[0]:great_img.shape[0],
            int(great_img.shape[1]/2-img.shape[1]/2):
            int(great_img.shape[1]/2+img.shape[1]/2),:] = img
            if ret==False: break
            # Se cambian los colores de BGR a RGB
            img_rgb = cv.cvtColor(great_img,cv.COLOR_BGR2RGB)
            # Se aplica el procesamiento de la imagen para obtener el selfie
            results = selfie_segmentation.process(img_rgb)
            # Con el resultado se obtiene la mascara de la imagen
            mask = results.segmentation_mask
            # Se ajusta los valore entre 0 y 255
            mask = mask*255
            # Se aplica el umbral para binarizar la imagen de la máscara
            # Se saca tanto la máscara original como la inversa
            # El objetivo es aplicarlas de manera independiente, una de ellas sobre 
            # la imagen original que obtiene el selfie con un fondo negro del tamaño
            # del fondo.
            # La otra sobre el fondo en la cual aparezca en negor el hueco del slefie
            # con el objetivo de sumarlas y obtener el resultado esperado
            ret,mask = cv.threshold(mask,5,255,cv.THRESH_BINARY)
            ret,mask_inv = cv.threshold(mask,5,255,cv.THRESH_BINARY_INV)
            mask = np.array(mask,dtype=np.uint8)
            mask_inv = np.array(mask_inv,dtype=np.uint8)
            # Se usa un kernel para eliminar el ruido con una apertura y un cierre
            # kernel = np.ones((5, 5), np.uint8)
            # mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=2)
            # mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
            # Se combinan las imágen con la máscara para segmentar a la persona
            new_image=cv.bitwise_and(great_img,great_img,mask=mask)
            new_background = cv.bitwise_and(background,background,
                mask=mask_inv)
            final_img = cv.add(new_image,new_background)

            # cv.imshow("Image",img)
            # cv.imshow("Image_RGB",img_rgb)
            # cv.imshow("new_image",new_image)
            # cv.imshow("background",background)
            # cv.imshow("new_background",new_background)
            # cv.imshow("great_img",great_img)
            # cv.imshow("shame_size",shame_size)
            cv.imshow("final_img",final_img)
            k = cv.waitKey(1)
            if k==27: break
        cap.release()
            
            
cv.destroyAllWindows()