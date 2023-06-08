#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    //Checking if user gave only one input
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    //checking that argv[1] only contains digits
    for (int i = 0, length = strlen(argv[1]); i < length; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    string text = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int letter = 0, text_length = strlen(text); letter < text_length; letter++)
    {
        //argv[1] is the key
        int key = atoi(argv[1]);
        if islower(text[letter])
        {
            //convert ascii to alphabetical index and revert back to ascii after encipher
            printf("%c", (((text[letter] - 'a') + key) % 26) + 'a');
        }
        else if isupper(text[letter])
        {
            //convert ascii to alphabetical index and revert back to ascii after encipher
            printf("%c", (((text[letter] - 'A') + key) % 26) + 'A');
        }
        else
        {
            printf("%c", text[letter]);
        }
    }
    printf("\n");
}