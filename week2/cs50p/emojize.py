import emoji

def main():
    user_input = input("Input: ")
    # language='alias' enables both standard codes and shorthand aliases
    converted = emoji.emojize(user_input, language='alias')
    print("Output:", converted)

if __name__ == "__main__":
    main()