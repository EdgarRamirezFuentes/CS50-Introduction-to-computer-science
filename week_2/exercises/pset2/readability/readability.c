#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>
#include <cs50.h>


int count_words(string);
int count_sentences(string);
int count_letters(string);
float get_grade(int, int, int);

int main(void)
{
    // Get the text to evaluate from user
    string text = get_string("Text: ");
    // Storage the number of words in the text
    int words = count_words(text);
    // Storage the number of sentences in the text
    int sentences = count_sentences(text);
    // Storage the number of letters in the text
    int letters = count_letters(text);
    // Storage the grade of the text
    float grade = get_grade(words, sentences, letters);

    // Print the grade of the text
    if (grade < 1.0)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 1.0 && grade <= 16.0)
    {
        printf("Grade %d\n", (int) grade);
    }
    else
    {
        printf("Grade 16+\n");
    }
}

int count_words(string text)
{
    // Count the number of words in the text
    int words = 0;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        char current_character = text[i];
        // Each word is separated by a space
        if (current_character == ' ')
        {
            words++;
        }
    }
    // The last word is added to the count
    return words + 1;
}

int count_letters(string text)
{
    int letters = 0;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        char current_character = text[i];
        // Check if the current character is a valid letter and add up the count by 1
        if (isalpha(current_character) && tolower(current_character) >= 'a' &&  tolower(current_character) <= 'z')
        {
            letters++;
        }
    }
    return letters;
}

int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        char current_character = text[i];
        // Check if the current character is a sentence ending character
        if (current_character == '.' || current_character == '!' || current_character == '.' || current_character == '?')
        {
            sentences++;
        }
    }
    return sentences;
}

float get_grade(int words, int sentences, int letters)
{
    // Using the rule of three we get the average of words and sentences in the text
    float average_letters = (letters * 100.0) / words;
    float average_sentences = (sentences * 100.0) / words;
    // Return the result of the formula to calculate the grade of a text
    return round(0.0588 * average_letters - 0.296 * average_sentences - 15.8);
}