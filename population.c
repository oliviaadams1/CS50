#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //get starting population size from user
    int start_size;
    do
    {
        start_size = get_int("staring population size: ");
    }
    while (start_size < 9);

    //get ending population size from user
    int end_size;
    do
    {
        end_size = get_int("ending population size: ");
    }
    while (end_size < start_size);

    //Calculate number of years until we reach threshold
    int years = 0;
    int current_size = start_size;
    while (end_size > current_size)
    {
        current_size = (current_size + current_size / 3 - current_size / 4);
        years++;
    }
    
    printf("Years: %i \n", years); //Print number of years
}
