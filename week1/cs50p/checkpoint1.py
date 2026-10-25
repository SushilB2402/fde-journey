def is_even(num):
    return num % 2 == 0

number = int(input("Enter a number: "))
if is_even(number):
    print(f"{number} is an even number.") 
else:
    print(f"{number} is an odd number.")