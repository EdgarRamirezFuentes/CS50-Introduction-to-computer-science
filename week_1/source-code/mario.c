#include <stdio.h>
// Only works on CS5 IDE
//#include <cs50.h>
int get_positive_int(void);

int main(void)
{
    int width = 0;

    width = get_positive_int();

    // Print out width times the character ?
   for(int i = 0; i < width; i++)
   {
       printf("?");
   }
   printf("\n");
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
