// Implements a dictionary's functionality

#include "dictionary.h"
#include <stdbool.h>
#include <ctype.h>
#include <stdlib.h> // Used for malloc
#include <string.h> // Used to strlen
#include <strings.h> // Used for case insensitive comparison
#include <stdio.h> // Used of EOF
// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 10000;

// Hash table
node *table[N];

// Number of current values in the hash table
unsigned int SIZE = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hash_index = hash(word);
    node *position = table[hash_index];
    // Loop over the linked list looking for the given word
    while (position)
    {
        if (!strcasecmp(position->word, word))
        {
            // The Word was found in the hash table
            return true;
        }
        position = position->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Souce: http://www.cse.yorku.ca/~oz/hash.html
    unsigned long hash = 5381;
    int length = strlen(word);
    char c;
    while ((c = *(word++)))
    {
        hash = ((hash << 5) + hash) + tolower(c); /* hash * 33 + c */
    }
    // Modulus N to make it fit into the hash table size
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    // The file could not be open
    if (!file)
    {
        return false;
    }

    char word[LENGTH + 1];
    int hash_code;
    node *new_node = NULL;
    // Loads the words in the hash table
    while ((fscanf(file, "%s", word) != EOF))
    {
        // Allocates memory for the new node
        new_node = malloc(sizeof(node));
        if (!new_node)
        {
            // There is no more memory available to add a new node in the hash table
            return false;
        }

        hash_code = hash(word);
        // Initialize the new node created
        strcpy(new_node->word, word);
        // Reconnect the new node to the list
        new_node->next = table[hash_code];
        // Set the new node as the root of the list
        table[hash_code] = new_node;
        SIZE++;
    }

    // Avoids memory leaks
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return SIZE;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    node *aux = NULL;
    for (int i = 0; i < N; i++)
    {
        aux = table[i];
        while (aux)
        {
            // Set a "new root" in the bucket
            table[i] = aux->next;
            // Frees the "old root"
            free(aux);
            // Decrement the deleted item in the hash table
            SIZE--;
            // Places aux in the "new root"
            aux = table[i];
        }
    }
    return (SIZE == 0 ? true : false);
}

