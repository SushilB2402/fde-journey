def main():
    # Loop until the user provides valid input
    while True:
        user_input = input("Fraction: ")
        try:
            percentage = convert(user_input)
            result = gauge(percentage)
            print(result)
            break
        except (ValueError, ZeroDivisionError):
            continue

def convert(fraction):
    # Split the string by the slash
    X, Y = fraction.split("/")

    # Convert to integers
    X = int(X)
    Y = int(Y)

    # Check for negative numbers or if X is greater than Y
    if X < 0 or Y < 0 or X > Y:
        raise ValueError

    # Division by zero will automatically raise ZeroDivisionError if Y is 0
    return round((X / Y) * 100)

def gauge(percentage):
    # Check bounds for Empty and Full states
    if percentage <= 1:
        return "E"
    elif percentage >= 99:
        return "F"
    else:
        return f"{percentage}%"


if __name__ == "__main__":
    main()
