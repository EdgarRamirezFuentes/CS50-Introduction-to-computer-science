def count_letters(text):
    letters = 0
    for character in text:
        if character.isalpha():
            letters += 1
    return letters


def count_words(text):
    words = 0
    for character in text:
        if character == " ":
            words += 1
    return words + 1


def count_sentences(text):
    sentences = 0
    for character in text:
        if character == "." or character == "!" or character == "?":
            sentences += 1
    return sentences


def get_grade(words, sentences, letters):
    # Using the rule of three we get the average of words and sentences in the text
    average_letters = (letters * 100) / words
    average_sentences = (sentences * 100) / words
    # Return the result of the formula to calculate the grade of a text
    return round(0.0588 * average_letters - 0.296 * average_sentences - 15.8)


if __name__ == "__main__":
    # Gets the text to evaluate from user
    text = input("Text: ")
    # Storages the number of sentences in the text
    sentences = count_sentences(text)
    # Storages the number of words in the text
    words = count_words(text)
    # Storages the number of letters in the text
    letters = count_letters(text)
    # Storages the grade of the text
    grade = get_grade(words, sentences, letters)

    if grade < 1.0 and grade <= 16.0:
        print("Before Grade 1")
    elif grade >= 1.0 and grade <= 16.0:
        print(f"Grade {int(grade)}")
    else:
        print("Grade 16+")