def main():
    user_input = input("Input: ")
    print("Output:", omit_vowels(user_input))


def omit_vowels(text):
    vowels = "AEIOUaeiou"
    result = []
    for char in text:
        if char not in vowels:
            result.append(char)
    return "".join(result)


if __name__ == "__main__":
    main()