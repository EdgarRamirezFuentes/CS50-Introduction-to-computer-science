#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int valid_key(const string);

int main(int argc, string argv[])
{
    // The user sent 2 arguments and until now that is correct
    if (argc == 2)
    {
        // Only continue the execution if the key provided from user is valid
        if (strlen(argv[1]) != 26)
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
        else if (valid_key(argv[1]))
        {
            string key = argv[1];
            // Get the plain text from user
            string plain_text = get_string("plaintext: ");
            // Cipher the plain text
            for (int i = 0, size = strlen(plain_text); i < size; i++)
            {
                char current = plain_text[i];
                // Only will change its value if the current character is a letter
                if (isalpha(current))
                {
                    // Calculates the position in the key of the new letter
                    int position = islower(current) ? (current - 'a') : (current - 'A');
                    // Change the new letter in the string
                    plain_text[i] = islower(current) ? tolower(key[position]) : toupper(key[position]);
                }
            }
            // Print the cipher plain text
            printf("ciphertext: %s\n", plain_text);
        }
        else
        {
            // The key was not valid.
            printf("Usage: ./substitution key\n");
            return 1;
        }
    }
    else
    {
        // The arguments were no valid.
        printf("Usage: ./substitution key\n");
        return 1;
    }
    return 0;
}

// Verify that each character of the key is a letter
int valid_key(const string key)
{
    // Count the times of appearances of a letter
    int appearances[26] = {};
    for (int i = 0, size = strlen(key); i < size; i++)
    {
        char current = key[i];
        if (isalpha(current))
        {
            current = tolower(current);
            int position = current - 'a';
            // Add up by 1 the appearance ofthe current letter
            appearances[position]++;
            // It not allowed to have a letter more than once in the key
            if (appearances[position] > 1)
            {
                return 0;
            }
        }
        else
        {
            return 0;
        }
    }
    return 1;
}