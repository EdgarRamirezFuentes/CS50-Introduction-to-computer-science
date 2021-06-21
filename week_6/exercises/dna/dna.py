import csv
import sys

# Gets the number of STR of the sequence appearances


def get_appearances(STR, sequence):
    appearances = []

    # For each STR check its number of consecutive appearances
    for data in STR:
        # Keeps track of the max number of consecutive appearances of the current STR
        max_ap = 0
        # Keeps track of the current number of consecutive appearances of the current STR
        current_ap = 0
        # Keeps track of the index in the sequence
        current_index = 0
        while current_index < len(sequence):
            current_STR = sequence[current_index:current_index + len(data)]
            if current_STR == data:
                # The current substring matches with the current STR and the current appearances is added up by 1
                current_ap += 1
                # Go to the next contiguos substring of the same length
                current_index += len(data)
            else:
                # The consecutive appearances finished. Thus, the max contiguous apperances of the current STR is updated
                max_ap = max(current_ap, max_ap)
                # The current appearances starts from zero again
                current_ap = 0
                # Adds up by 1 the current index to check if the next contiguos letter is a possible beginning of a string that matches with the current STR
                current_index += 1
        # Appends the max number of appearances of the current STR (as string) to the list.
        appearances.append(str(max(max_ap, current_ap)))
    return appearances


# Finds to whom these STR appearances belong if they exist


def find_person(sequence_STR, people_data):
    for person in people_data:
        if sequence_STR == people_data[person]:
            return person
    return "No match"


if __name__ == "__main__":

    # Contains the STR data of each person in the database
    people_data = {}

    # Contains the STR that will looked for in the DNA sequence
    STR = []

    # Contains the DNA sequence that will be analyzed
    sequence = ""

    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # Getting the data from database
    with open(sys.argv[1], mode="r") as data_file:
        data_reader = csv.reader(data_file)
        line_counter = 0
        for row in data_reader:
            if line_counter == 0:
                # Creates a copy of the STR that will be looked for in the sequence
                STR = row[1:]
            else:
                # Gets the name of the current person
                person_name = row[0]
                # Gets the number of appareances of their STR and stores them in the dictionary where the key of the person these STR belong to
                people_data[person_name] = row[1:]
            line_counter += 1

    # Getting the sequence that will be analyzed
    with open(sys.argv[2], "r") as sequence_file:
        sequence = sequence_file.readline()

        # Geting the number of each STR appearances in the sequence
        sequence_STR = get_appearances(STR, sequence)

        # Getting to whom this DNA sequeence belongs
        print(find_person(sequence_STR, people_data))

    sys.exit(0)