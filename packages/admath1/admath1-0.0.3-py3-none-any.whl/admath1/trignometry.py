import math
def tan(x):
    # Convert the angle to radians
    rad = x * (3.14159/180)
    # Use the formula tan(x) = sin(x) / cos(x)
    return sin(rad) / cos(rad)

def sin(x):
    # Convert the angle to radians
    rad = x * (3.14159/180)
    # Use the Taylor series approximation for sin(x)
    sinx = rad - (rad**3)/math.factorial(3) + (rad**5)/math.factorial(5) - (rad**7)/math.factorial(7)
    return sinx

def cos(x):
    # Convert the angle to radians
    rad = x * (3.14159/180)
    # Use the Taylor series approximation for cos(x)
    cosx = 1 - (rad**2)/math.factorial(2) + (rad**4)/math.factorial(4) - (rad**6)/math.factorial(6)
    return cosx

print(tan(36))