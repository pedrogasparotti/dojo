def checkTriangleInts(a, b, c):
    
    if a <= 0 or b<= 0 or c <= 0:
        return False
    
    if a > (b+c):
        return False
    
    if b > (a + c):
        return False
    
    if c > (a + b):
        return False
    
    return True

def checkTriangleList():

    """
    check it the sum of the two smaller sides is as large as the longest side
    """

    sides = [float(input(f"Enter float number {i+1}: ")) for i in range(3)]

    return sum(sides) - max(sides) > max(sides)