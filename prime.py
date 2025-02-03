def isPrime(x):
    
    if x == 2:
     return False   

    if x%2==0:
        return False
    
    upper_limit = int( x**(1/2) + 1)

    for i in range(3, upper_limit, 2):
        if x%i==0:
            return False
    return True
