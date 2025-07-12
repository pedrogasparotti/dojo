def somar(v1, v2):

    if len(v1) != len(v2):
        print("vetores incompatíveis")
        return 0
    res = []
    
    for i in range(len(v1)):
        res.append(v1[i] + v2[i])

    return res

def subtrair(v1, v2):
    
    res = []

    res.append(somar(v1, inverter(v2)))

    return res

def inverter(v):

    res = []

    for i in range(len(v)):
        res.append(-v[i])

    return res

def multiplicar(vet, num):

    return [vet[i] * num for i in range(len(vet))]

def prod_escalar(v1, v2):

    if len(v1) != len(v2):
        print("vetores incompatíveis")
        return None
        
    res = 0

    for i in range(len(v1)):

        res += v1[i] * v2[i]

    return res

    pass

if __name__ == '__main__':
    a = [2, 5, 3]
    b = [1.5, 7.0, 0]
    num = 4

    print('Soma dos vetores a e b: ', somar(a,b))
    print('Diferença dos vetores a e b ', subtrair(a, b))
    print('Multiplicação de a por num: ', multiplicar(a, num))
    print('produto escalar entre a e b: ', prod_escalar(a, b))