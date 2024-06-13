#calculator App
class Calculator:
    '''
    Calculator class

    Methods:
    add(a, b): Returns the sum of a and b
    subtract(a, b): Returns the difference betwen a and b
    multiply(a, b):Returns the product of a and b
    divide(a, b): Returns the quotient of a and b
    '''
    def add(self, a, b):
        return a + b

    def subtract(self, a , b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def division(self, a, b):
        if b == 0:
            return "Error: Divison by zero"
        return a / b
    
    def modulo(self, a, b):
        if b == 0:
            raise ValueError("The divisor 'b' cannot be zero.")
    
        quotient = a // b  # This performs integer division
        remainder = a - quotient * b
        return remainder

    
    def sqrt_newton(num, tolerance=1e-10):
        if num < 0:
            raise ValueError("Cannot compute the square root of a negative number")
    
        guess = num
        while True:
            new_guess = (guess + num / guess) / 2
            if abs(new_guess - guess) < tolerance:
                return new_guess
            guess = new_guess

calc = Calculator()

x, y = map(int, input("Enter two integers").split())
print("First integer: ", x)
print("Second integer: ", y)
print("Add: ", calc.add(x, y))
print("Subtract: ", calc.subtract(x, y))
print("Multiply: ", calc.multiply(x, y))
print("Division: ", calc.division(x, y))
print("Modulo: ", calc.modulo(x, y))
print("Sqrt of first int: ", calc.sqrt_newton(x))
print("Sqrt of second int: ", calc.sqrt_newton(y)) 

