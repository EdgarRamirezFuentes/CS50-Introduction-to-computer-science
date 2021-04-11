#include <stdio.h>
// Only works on CS5 IDE
//#include <cs50.h>

int main(void)
{
    int x = 0, y = 0;

    // Get numbers from user
    x = get_long("x: ");
    y = get_long("y: ");
    /*
    Z stores the reesult of the division as a integer because x and y are integers
    float z = x / y;
    */

    /* Using cast we can store the result of the division as a float because we are casting x and y as float numbers */
    float z = (float) x / (float) y;
    printf("%i / %i = %f\n", x, y, z);
    return 0;
}