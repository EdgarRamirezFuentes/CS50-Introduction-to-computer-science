#include <stdio.h>
// Only works on CS5 IDE
//#include <cs50.h>

int main(void)
{
    float x = 0, y = 0;
    x = get_float("x: ");
    y = get_float("y: ");
    printf("%.50f\n", x / y);
}
