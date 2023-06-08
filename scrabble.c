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

    // Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else if (score1 == score2)
    {
        printf("It's a tie!\n");
    }
}

int compute_score(string word)
{
    int score = 0;
    //count the length of the word and give each letter a cooresponding number
    for (int letter = 0, length = strlen(word); letter < length; letter++)
    {
        if (islower(word[letter]))
        {
            // Compare letter of word given to lowercase ASCII
            score = score + POINTS[word[letter] - 'a'];
        }
        else if (isupper(word[letter]))
        {
            // Compare letter of word given to uppercase ASCII
            score = score + POINTS[word[letter] - 'A'];
        }
    }
    return score;
}
