"""This module provides a no. of functions related to basic calculator operations."""


def add() :
    sum1 = 0
    x = input("Please enter the numbers to be added one by one. When you enter 0,the list terminates.\n")
    while float(x) != 0 :
        sum1 = float(x) + float(sum1)
        x = input("Continue entering :\n")        
    print("The sum of the numbers is :")
    print(sum1)
        
def subtract() :
    a = input("Enter the two numbers one by one.The second will be subtracted from the first.\n")
    b = input()
    difference = float(a) - float(b)
    print("The difference is : \n")
    print(difference)

def multiply() :
    product = 1
    m = input("Please enter the numbers to be multiplied one by one. When you enter 1,the list terminates.\n")
    while float(m) != 1 :
        product = float(m) * float(product)
        m = input("Continue entering:\n")

    print("The product of the numbers is :")
    print(product)

def divide() :
    d1 = input("Enter the two numbers (The first will be divided by the second.):")
    d2 = input()
    quotient = float(d1)/float(d2)
    remainder = float(d1)%float(d2)
    print("The quotient is :")
    print(quotient)
    print("The remainder is :")
    print(remainder)

def power():
    base = input("Please enter the base and power in this order:\n")
    power = input()
    ans = pow(float(base),float(power))
    print("The answer is: %f" %ans)

def sqrt() :
    no = input("Enter the number that you want the square root of :\n")
    sqrt = pow(float(no) , 1/2)
    print("The square root of the number is : %f" %sqrt)

"""The calc() function is the actual calculator and sort of combines all the other functions. You just hit calc.calcu() and get an instant calculator.
Be sure to 'import calc' though."""
def calcu() :
        option = 1 
        while option != 7 :
            
             print("\nPlease select one the following options by entering the respective number :\n")
             print("1.Add")
             print("2.Subtract")
             print("3.Multiply")
             print("4.Divide")
             print("5.x to the power of y")
             print("6.Square root")
             print("7.Exit\n")
             option = input()
             if int(option) == 1 :
                 add()
             elif int(option)== 2 :
                 subtract()
             elif int(option) == 3 :
                 multiply()
             elif int(option) == 4 :
                 divide()
             elif int(option) == 5 :
                 power()
             elif int(option) == 6 :
                 sqrt()
             else :
                 print("Sorry to see you go !!!!!!")
                 exit()
             print(" ================================ RESTART ================================")



       









            
