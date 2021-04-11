#include <stdio.h>
// Only works on CS5 IDE
//#include <cs50.h>

int main(void)
{
    int x = 0, y = 0;

    /* Get numbers from user */
    x = get_long("x: ");
    y = get_long("y: ");
    /* Compares x and y */
    if(x > y)
    {
        printf("x larger than y");
    }
    else if (x < y)
    {
      printf("x smaller than y");
    }
    else
    {
        printf("x and y are equal");
    }
    puts("");
    return 0;
}