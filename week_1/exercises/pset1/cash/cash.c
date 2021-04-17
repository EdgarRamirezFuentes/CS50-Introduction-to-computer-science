#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main()
{
    float change = 0;
    int coins = 0;
    int cents = 0;

    // Change owed from user
    do
    {
        change = get_float("Change owed: ");
    }
    while (change < 0);

    cents = round(change * 100);

    // 25 cents
    coins += cents / 25;
    cents -= (cents / 25) * 25;

    // 10 cents
    coins += cents / 10;
    cents -= (cents / 10) * 10;

    // 5 cents
    coins += cents / 5;
    cents -= (cents / 5) * 5;

    // 1 cent
    coins += cents / 1;
    cents -= (cents / 1) * 1;

    // Print the minimum of coins needed to
    // pay the change owed. 
    printf("%d\n", coins);

    return 0;
}