def main():
    # Prompt the user for a variable name in camel case
    camel_case = input("camelCase: ")

    snake_case = ""
    for char in camel_case:
        # If the character is uppercase, add an underscore and lowercase it
        if char.isupper():
            snake_case += "_" + char.lower()
        else:
            snake_case += char

    # Output the corresponding name in snake case
    print(f"snake_case: {snake_case}")


if __name__ == "__main__":
    main()