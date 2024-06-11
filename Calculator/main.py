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

calc = Calculator()

x, y = map(int, input("Enter two integers").split())
print("First integer: ", x)
print("Second integer: ", y)
print(calc.add(x, y))
print(calc.add(10, 5))
print(calc.subtract(10, 5))
print(calc.multiply(10, 5))
print(calc.division(10, 5))

