numeros = [7, 8, 15]
outro = numeros.copy()

matriz = [numeros, outro]
matriz2 = matriz.copy()

for i in range(len(matriz)):
        print(matriz2[i])

for i in range(len(matriz)):
        print(matriz[i])

print("--------")

matriz[0][0] = 22

for i in range(len(matriz)):
        print(matriz2[i])

for i in range(len(matriz)):
        print(matriz[i])