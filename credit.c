#include <cs50.h>
#include <stdio.h>

long get_card_number(void);
int calculate_digits(long card_number);
int calculate_sum_odd(long card_number, int digits);
int calculate_sum_even(long card_number, int digits);

int main(void)
{
    long card_number = get_card_number();
    int digits = calculate_digits(card_number);
    int sum_odd = calculate_sum_odd(card_number, digits);
    int sum_even = calculate_sum_even(card_number, digits);
    int total_sum = sum_even + sum_odd;

//Checksum total
    if (total_sum % 10 != 0)
    {
        printf("INVALID\n");
    }

//AMEX 15 digits long and starts with 34 or 37
    else if (digits == 15)
    {
        if (card_number / 10000000000000 == 34 ||card_number / 10000000000000 == 37)
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }

//Mastercard 16 digits long and starts with 51, 52, 53, 54, and 55
    else if (digits == 16)
    {
        if ((card_number / 100000000000000 >= 51 && card_number / 100000000000000 < 56))
        {
            printf("MASTERCARD\n");
        }
        else if (card_number / 1000000000000000 == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }

//Visa 13 or 16 digits and starts with 4
    else if (digits == 13)
    {
        if (card_number / 1000000000000 == 4)
        {
        printf("VISA\n");
        }
        else
        {
        printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}


long get_card_number(void)
{
    //Ask user for their credit card number
    long card_number;
    do
    {
        card_number = get_long("Number: ");
    }
    while (card_number < 0);
    return card_number;
}

//Calculate number of digits
int calculate_digits(long card_number)
{
    int digits = 0;
    while (card_number > 0)
    {
        card_number /= 10;
        digits++;
    }
    return digits;
}

//Calculate sum of odd digits multiplied by 2
int calculate_sum_odd(long card_number, int digits)
{
    int sum_odd = 0;
    card_number = card_number / 10;
    while (digits > 0)
    {
        if ((card_number % 10) * 2 >= 10)
        {
            sum_odd += ((card_number % 10 * 2) % 10) + 1;
        }
        else
        {
            sum_odd = sum_odd + ((card_number % 10) * 2);
        }
        card_number = card_number / 100;
        digits = digits - 2;
    }
    return sum_odd;
}

//Calculate the sum of even digits
int calculate_sum_even(long card_number, int digits)
{
    int sum_even = 0;
    while (digits > 0)
    {
        sum_even = sum_even + (card_number % 10);
        card_number = card_number / 100;
        digits = digits - 2;
    }
    return sum_even;
}


