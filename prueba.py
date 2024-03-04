import numpy as np

# Definir la matriz original
matriz_original = np.array([[False,False,False,False,False],#5x5,5x5,5x5and5x5
                [False,False,True,False,False],
                [False,False,False,True,False],
                [False,True,True,True,False],
                [False,False,False,False,False]])

# Rotar la matriz 90 grados en sentido horario
matriz_rotada = [list(row) for row in zip(*matriz_original[::-1])]

# Imprimir la matriz rotada
for fila in matriz_rotada:
    print(fila)