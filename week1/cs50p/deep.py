def main():
    # Prompt the user for the answer
    answer = input("What is the Answer to the Great Question of Life, the Universe and Everything? ")

    # Clean and check the input case-insensitively
    answer = answer.strip().lower()

    if answer in ["42", "forty-two", "forty two"]:
        print("Yes")
    else:
        print("No")


if __name__ == "__main__":
    main()