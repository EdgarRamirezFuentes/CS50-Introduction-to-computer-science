#include <stdio.h>
// Only works on CS5 IDE
//#include <cs50.h>

int main(void)
{
    int height = 0;
    do
    {
        // Get the height of the pyramid
        height = get_int("Height: ");
    }

    while (height < 1 || height > 8);
    // Print out the pyramid
    for (int i = 0; i < height; i++)
    {
        // Print a new column of our pyramid
        for (int j = 0; j < height; j++)
        {

            if (j >= height - 1 - i)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        // Create a new row in the pyramid
        printf("\n");
    }
}