#include <stdio.h>
// Only works on CS5 IDE
//#include <cs50.h>

int get_positive_int(void);

int main(void)
{
    int x = get_positive_int();
    printf("The number is %i\n", x);
    return 0;
}

int get_positive_int(void)
{
    int n = 0;
    // Get a number from the user until the number is positive;
    do
    {
        n = get_int("Positive Integer: ");
    }
    while(n < 1);
    return n;
}
