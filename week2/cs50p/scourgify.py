import csv
import sys


def main():
    # Check command-line arguments
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")

    students = []

    # Read the input CSV file
    try:
        with open(sys.argv[1], "r") as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                last, first = row["name"].split(", ")
                students.append(
                    {"first": first, "last": last, "house": row["house"]}
                )
    except FileNotFoundError:
        sys.exit(f"Could not read {sys.argv[1]}")

    # Write the cleaned data to the output CSV file
    with open(sys.argv[2], "w", newline="") as output_file:
        fieldnames = ["first", "last", "house"]
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for student in students:
            writer.writerow(student)


if __name__ == "__main__":
    main()
