#include <cs50.h>
#include <stdio.h>

int main(void)

//ask user for height

{
    int size;
    do
    {
        size = get_int("size: ");
    }

    while (size < 1 || size > 8);

//print pyramid

    for (int column = 0 ; column < size; column++)
    {
        for (int space = size - 1 ; space > column; space--)
        {
            printf(" ");
        }
        for (int row = 0; row <= column; row++)
        {
            printf("#");
        }
        printf("\n");
    }
}