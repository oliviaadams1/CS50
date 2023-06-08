// Implements a dictionary's functionality
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

unsigned int words;
unsigned int hash_val;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO 4
    // hash to word to obtain hash value
    hash_val = hash(word);

    // point cursor to first node
    node *cursor = table[hash_val];
    // iterateover linked list
    while (cursor != 0)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO 2: Improve this hash function

    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // open the noor (dictionary)
    FILE *dictionary_file = fopen(dictionary, "r");

    // if dictionary cannot be opened
    if (dictionary_file == NULL)
    {
        printf("Unable to open %s\n", dictionary);
        return false;
    }

    // declare word that includes nul character following the string
    char word[LENGTH + 1];

    // scan dictionary for until the end of file
    while (fscanf(dictionary_file, "%s", word) != EOF)
    {
        // allocate memory for new node
        node *new_node = malloc(sizeof(node));
        // if memory cannot be allocated
        if (new_node == NULL)
        {
            printf("Unable to allocate memory\n");
            return false;
        }
        // copy word from dictionary to node
        strcpy(new_node->word, word);
        hash_val = hash(word);
        new_node->next = table[hash_val];
        table[hash_val] = new_node;
        words++;
    }
    fclose(dictionary_file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO 3 return word count
    if (words > 0)
    {
        return words;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO 5
    // iterate through "buckets"
    for (int i = 0; i < N; i++)
    {
        // set curser to the beginning of linked list
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }

    return true;
}
