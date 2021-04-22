#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>
#include <ctype.h>
#include <stdlib.h>

int valid_key(const string);

int main(int argc, string argv[])
{
    // The user sent 2 arguments and until now that is correct
    if (argc == 2)
    {
        // Only continue the execution if the key provided from user is valid
        if (valid_key(argv[1]))
        {
            int key = atoi(argv[1]);
            // Get the plain text from user
            string plain_text = get_string("plaintext: ");
            // Cipher the plain text
            for (int i = 0, size = strlen(plain_text); i < size; i++)
            {
                char current = plain_text[i];
                // Only will change its value if the current character is a letter
                if (isalpha(current))
                {
                    // Calculates the position in the alphabet of the new letter
                    int position = (islower(current) ? (key + current - 'a') : (key + current - 'A')) % 26;
                    // Change the new letter in the string
                    plain_text[i] = (islower(current) ? 'a' : 'A') + position;
                }
            }
            // Print the cipher plain text
            printf("ciphertext: %s\n", plain_text);
        }
        else
        {
            // The key was not valid.
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    else
    {
        // The arguments were no valid.
        printf("Usage: ./caesar key\n");
        return 1;
    }
    return 0;
}

// Verify that each character of the key is a digit
int valid_key(const string key)
{
    for (int i = 0, size = strlen(key); i < size; i++)
    {
        if (!isdigit(key[i]))
        {
            return 0;
        }
    }
    return 1;
}