#include <stdio.h>
// Only works on CS5 IDE
//#include <cs50.h>

int main(void)
{
    char c = 0;

    /* Get a char from user */
    c = get_char("Do you agree?  ");
    if(c == 'y' || c == 'Y')
    {
        printf("Agreed.");
    }
    else
    {
        printf("Not agreed.");
    }
    puts("");
    return 0;
}