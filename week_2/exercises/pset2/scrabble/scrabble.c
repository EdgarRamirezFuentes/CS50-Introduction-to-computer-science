#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);
    // There is a winner in this game
    if (score1 != score2)
    {
        // Using ternary operator to print the winner
        printf(score1 > score2 ? "Player 1 wins!\n" : "Player 2 wins!\n");
    }
    // Player 1 and player 2 got the same score
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    // TODO: Compute and return score for string
    int total = 0;
    for (int i = 0,  word_length = strlen(word); i < word_length; i++)
    {
        char current_letter = word[i];
        if (isalpha(current_letter))
        {
            // Get the index of the array depending on if the current letter is lower or not.
            total += POINTS[isupper(current_letter) ? current_letter - 'A' : current_letter - 'a'];
        }
    }
    return total;
}
