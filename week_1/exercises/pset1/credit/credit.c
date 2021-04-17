#include <stdio.h>
//#include <cs50.h>
#include <math.h>

int get_length(long int);
int is_valid_card(long int, int);


int main()
{
    // Get the User's card number
    long int card_number = get_long("Number: ");
    // Storage the amount of digits of that card -> 100 has 3 digits
    int card_digits = get_length(card_number);
    // Storage the first two digits of the card number
    int card_type = card_number / pow(10, card_digits - 2);
    // Storage the first digit of the card to check if it is a possible Visa card
    int visa_value = card_number / pow(10, card_digits - 1);
    int valid_card = is_valid_card(card_number, card_digits);
    if (valid_card)
    {
        // Visa
        if (visa_value == 4 && (card_digits == 13 || card_digits == 16))
        {
            printf("VISA\n");
        }
        // American Express
        else if ((card_type == 34 || card_type == 37) && card_digits == 15)
        {
            printf("AMEX\n");
        }
        // Mastercard
        else if ((card_type > 50 && card_type < 56) && card_digits == 16)
        {
            printf("MASTERCARD\n");
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

    return 0;
}


/*
    For each iteration of the while loop removes the last digit of a number until the number becomes zero.
    for each time the while loop is repeated the size of the number is increased.
    Example:
    Number: 129 Size: 0
    Number: 12 Size: 1
    Number: 1 Size: 2
    Number: 0 Size: 3

*/
int get_length(long int card_number)
{
    int size = 0;
    while (card_number)
    {
        card_number /= 10;
        size++;
    }
    return size;
}


// Luhn's algorithm
int is_valid_card(long int number, int card_digits)
{
    int multiplied_digits_sum = 0, normal_digits_sum = 0, current_digit = 0;

    for (int i = 0; i < card_digits; i++)
    {
        current_digit = number % 10;
        if (i % 2 == 0)
        {
            normal_digits_sum += current_digit;
        }
        else
        {
            multiplied_digits_sum += (current_digit < 5 ? current_digit * 2 : ((current_digit * 2) % 10) + 1);
        }
        number /= 10;
    }
    return (multiplied_digits_sum + normal_digits_sum) % 10 ? 0 : 1;
}
