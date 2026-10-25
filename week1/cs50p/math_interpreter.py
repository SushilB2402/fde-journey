# Prompt user for an arithmetic expression
expression = input("Expression: ")

# Unpack the string by splitting at the spaces
x_str, y, z_str = expression.split(" ")

# Convert operands to integers
x = int(x_str)
z = int(z_str)

# Calculate the result based on the operator
if y == "+":
    result = x + z
elif y == "-":
    result = x - z
elif y == "*":
    result = x * z
elif y == "/":
    result = x / z

# Output the result formatted as a floating-point value to one decimal place
print(f"{result:.1f}")