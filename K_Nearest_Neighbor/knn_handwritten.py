# Usando la librería de opencv se usarán técnicas de aprendizaje automático para predecir digitos manuscrtitos
# Se usará la técnica de K Nearest Neighbor (K vecinos cercanos)
import cv2 as cv
import numpy as np

# Se lee la imagen de los números manuscritos que están separados en bloques de 50x50
# Se lee la imagen de test donde se encuentran los números manuscritos como un vector vertical
# Las imagenes se leen en escala de grises
digits = cv.imread("digits/digits.png",cv.IMREAD_GRAYSCALE)
test_digits = cv.imread("digits/test_digits.png",cv.IMREAD_GRAYSCALE)

# Se muestran las imagenes por pantalla
cv.imshow("digits",digits)
cv.imshow("test_digits",test_digits)
cv.waitKey()
cv.destroyAllWindows()

# Usando la función de numpy.vsplit se separan en filas la imagen de dígitos 
# numpy.vsplit(ary, indices_or_sections)
# Esta función, divide una matriz en múltiples sub-matrices verticalmente (en filas)
# Ejemplo
# >>> x = np.arange(16.0).reshape(4, 4)
# >>> x
# array([[ 0.,   1.,   2.,   3.],
#        [ 4.,   5.,   6.,   7.],
#        [ 8.,   9.,  10.,  11.],
#        [12.,  13.,  14.,  15.]])
# >>> np.vsplit(x, 2)
# [array([[0., 1., 2., 3.],
#        [4., 5., 6., 7.]]), array([[ 8.,  9., 10., 11.],
#        [12., 13., 14., 15.]])]
# >>> np.vsplit(x, np.array([3, 6]))
# [array([[ 0.,  1.,  2.,  3.],
#        [ 4.,  5.,  6.,  7.],
#        [ 8.,  9., 10., 11.]]), array([[12., 13., 14., 15.]]), array([], shape=(0, 4), dtype=float64)]

# Con una matriz dimensional más alta, la división aún se encuentra a lo largo del primer eje.
# Ejemplo
# >>> x = np.arange(8.0).reshape(2, 2, 2)
# >>> x
# array([[[0.,  1.],
#         [2.,  3.]],
#        [[4.,  5.],
#         [6.,  7.]]])
# >>> np.vsplit(x, 2)
# [array([[[0., 1.],
#         [2., 3.]]]), array([[[4., 5.],
#         [6., 7.]]])]
rows = np.vsplit(digits,50)
# Se muestra por pantalla como divide la imagen en filas, en este caso, la fila 10
cv.imshow("rows",rows[10])
cv.waitKey()
cv.destroyAllWindows()

# Se pretende separar uno a uno, cada dígito, para ello se crea una variable donde se almacenarán
cells = []
for row in rows:
	# Usando la función de numpy.vsplit se separan en filas la imagen de dígitos 
	# numpy.hsplit(ary, indices_or_sections)
	# Esta función, divide una matriz en múltiples sub-matrices horizontalmente (en forma de columna).
	# Ejemplo
	# >>> x = np.arange(16.0).reshape(4, 4)
	# >>> x
	# array([[ 0.,   1.,   2.,   3.],
	#        [ 4.,   5.,   6.,   7.],
	#        [ 8.,   9.,  10.,  11.],
	#        [12.,  13.,  14.,  15.]])
	# >>> np.hsplit(x, 2)
	# [array([[  0.,   1.],
	#        [  4.,   5.],
	#        [  8.,   9.],
	#        [12.,  13.]]),
	#  array([[  2.,   3.],
	#        [  6.,   7.],
	#        [10.,  11.],
	#        [14.,  15.]])]
	# >>> np.hsplit(x, np.array([3, 6]))
	# [array([[ 0.,   1.,   2.],
	#        [ 4.,   5.,   6.],
	#        [ 8.,   9.,  10.],
	#        [12.,  13.,  14.]]),
	#  array([[ 3.],
	#        [ 7.],
	#        [11.],
	#        [15.]]),
	#  array([], shape=(4, 0), dtype=float64)]

	# Con una matriz dimensional más alta, la división aún se encuentra a lo largo del segundo eje.
	# Ejemplo
	# >>> x = np.arange(8.0).reshape(2, 2, 2)
	# >>> x
	# array([[[0.,  1.],
	#         [2.,  3.]],
	#        [[4.,  5.],
	#         [6.,  7.]]])
	# >>> np.hsplit(x, 2)
	# [array([[[0.,  1.]],
	#        [[4.,  5.]]]),
	#  array([[[2.,  3.]],
	#        [[6.,  7.]]])]

	# Con una matriz 1-D, la división se realiza a lo largo del eje 0.
	# Ejemplo
	# >>> x = np.array([0, 1, 2, 3, 4, 5])
	# >>> np.hsplit(x, 2)
	# [array([0, 1, 2]), array([3, 4, 5])]
	row_cells = np.hsplit(row,50)
	for cell in row_cells:
		cell = cell.flatten()
		cells.append(cell)
# Se covierte en inmagen el resultado obtenido
cells = np.array(cells,dtype=np.float32)
# Corresponde a los números 9 de la última fila
cv.imshow("row_cells",row_cells[0])
cv.imshow("cells",cells[0])
cv.waitKey()
cv.destroyAllWindows()

# Se crea una matriz que repite los elementos con la función numpy.reapeat()
# El objetivo es el de generar las etiquetas para hacer las técnicas de aprendizaje automático
# numpy.repeat(a, repeats, axis=None)
	# a = Matriz de entrada.
	# repeats = El número de repeticiones de cada elemento. Las repeticiones 
		# se transmiten para adaptarse a la forma del eje dado.
	# axis = El eje a lo largo del cual se repiten los valores. De forma 
		# predeterminada, use la matriz de entrada aplanada y 
		# devuelva una matriz de salida plana.
# Esta función devuelve una matriz de salida que tiene la misma forma que a, excepto a los
# largo del eje dado
# Ejemplo
# >>> np.repeat(3, 4)
# array([3, 3, 3, 3])
# >>> x = np.array([[1,2],[3,4]])
# >>> np.repeat(x, 2)
# array([1, 1, 2, 2, 3, 3, 4, 4])
# np.repeat(x, 3, axis=1)
# >>> array([[1, 1, 1, 2, 2, 2],
#        [3, 3, 3, 4, 4, 4]])
# >>> np.repeat(x, [1, 2], axis=0)
# array([[1, 2],
#        [3, 4],
#        [3, 4]])
# Hay 250 número de cada uno de los números manuscritos del 0 al 9 
k = np.arange(10)
cells_labels = np.repeat(k,250)
# Se muestra por pantalla las etiquetas
print([i for i in cells_labels])

# Se desglosan los números de la imagen de test_digits.png
test_digits = np.vsplit(test_digits,50)
# Se muestra el número de la posición 30 que corresponde con un 6
cv.imshow("test_digits",test_digits[30])
cv.waitKey()
cv.destroyAllWindows()
# Se repite un razonamiento similar
test_cells = []
for d in test_digits:
	d = d.flatten()
	test_cells.append(d)
test_cells = np.array(test_cells,dtype=np.float32)
# Se muestra en forma de flattern los números y uno de los números de test de 
# la posición 0 igual 0
cv.imshow("test_cells",test_digits[0])
cv.imshow("d",d)
cv.waitKey()
cv.destroyAllWindows()

# Se aplican ahora las téncinas de aprendizaje automático con el algoritmo KNN
# K-Nearest Neighbor (KNN)
# Se usa la clase ml (corresponde a MACHINE LEARNING) junto con KNearest_create()
# El objetivo será crear un modelo que se entrenará con el dataset generado
# cv2.ml.KNearest_create()
knn = cv.ml.KNearest_create()
# Se usa el método de train para entrenar el modelo
# knn.train(trainData, cv.ml.ROW_SAMPLE, responses)
knn.train(cells, cv.ml.ROW_SAMPLE, cells_labels)
# Después de entrenarlo se usa la función findNearest() para encontrar la solución
# cv2::ml::KNearest::findNearest(samples, k, results, neighborResponses = noArray(),
	# dist =noArray())

	# samples = Muestras de entrada almacenadas por filas. Es una matriz de 
		# <number_of_samples> * ktamaño de punto flotante de precisión simple.
	# k = 	Número de vecinos más cercanos utilizados. Debe ser mayor que 1.
	# results = Vector con resultados de predicción (regresión o clasificación) para 
		# cada muestra de entrada. Es un vector de punto flotante de precisión simple 
		# con <number_of_samples>elementos.
	# neighborResponses = Valores de salida opcionales para los vecinos correspondientes. 
		# Es una matriz de <number_of_samples> * ktamaño de punto flotante de precisión simple.
	# dist = Distancias de salida opcionales desde los vectores de entrada a los vecinos 
		# correspondientes. Es una matriz de <number_of_samples> * ktamaño de punto 
		# flotante de precisión simple.
retval, results, neighborResponses, dist = knn.findNearest(test_cells,k=3)
# Se puestra el resultado por pantalla
print(results)