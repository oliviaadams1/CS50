import csv
import sys


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    # user inputs database
    names = []
    database = sys.argv[1]
    with open(database) as file:
        reader = csv.DictReader(file)
        for name in reader:
            # convert rating from string to integer and replace in dictionary
            names.append(name)

    # TODO: Read DNA sequence file into a variable
    # user inputs sequence
    sequence = sys.argv[2]
    with open(sequence, 'r') as file:
        sequences = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    subsequences = list(names[0].keys())[1:]
    matches = {}
    for subsequence in subsequences:
        matches[subsequence] = longest_match(sequences, subsequence)

    # TODO: Check database for matching profiles
    for name in names:
        match = 0

        # if match not found 
        for subsequence in subsequences:
            if int(name[subsequence]) == matches[subsequence]:
                match += 1

        # if match found
        if match == len(subsequences):
            print(name["name"])
            return

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
