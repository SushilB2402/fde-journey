import csv
import sys
from tabulate import tabulate


def main():
    check_command_line_arguments()

    table = []
    try:
        with open(sys.argv[1], "r") as file:
            reader = csv.reader(file)
            for row in reader:
                table.append(row)
    except FileNotFoundError:
        sys.exit("File does not exist")

    # The first row of the CSV is used as headers for tabulate
    headers = table[0]
    rows = table[1:]
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def check_command_line_arguments():
    # Expects exactly one command-line argument (plus the script name = 2 elements)
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")
    if len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")

    # Must end in .csv
    if not sys.argv[1].endswith(".csv"):
        sys.exit("Not a CSV file")


if __name__ == "__main__":
    main()