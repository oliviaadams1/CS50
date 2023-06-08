#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// functions defined later in code 
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);


int main(void)
{
    string text = get_string("Text: ");

// Input variables used in functions below
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);
    float L = (float) letters / (float) words * 100;
    float S = (float) sentences / (float) words * 100;
    int grade_level = round(0.0588 * L  - 0.296 * S - 15.8);

// Print grade level given text
    if (grade_level < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade_level > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade_level);
    }
}

int count_letters(string text)
{
    int letters = 0;
    // counting array length of text
    for (int length = 0, character = strlen(text); length < character; length++)
    {
        // Letters defined by being alphabetical
        if (isalpha(text[length]))
        {
            letters++;
        }
    }
    return letters;
}

int count_words(string text)
{
    int words = 1;
    for (int length = 0, character = strlen(text); length < character; length++)
    {
        // Words defined as being separated by space
        if (isblank(text[length]))
        {
            words++;
        }
    }
    return words;
}

int count_sentences(string text)
{
    int sentences = 0;
    //
    for (int length = 0, character = strlen(text); length < character; length++)
    {
        // Sentences defined as having exclamation, question mark, or period
        if (text[length] == '!' || text[length] == '?' || text[length] == '.')
        {
            sentences++;
        }
    }
    return sentences;
}