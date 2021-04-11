#include <stdio.h>
#include <cs50.h>

int main(void)
{
    long int x = 0, y = 0;

    // Get numbers from user
    x = get_long("x: ");
    y = get_long("y: ");
    printf("%li + %li = %li\n", x, y, x+y);
    return 0;
}