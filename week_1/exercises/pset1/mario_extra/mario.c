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
    // Print out the pyramid on the left side
    for (int i = 0; i < height; i++)
    {
        // Print a new column of the left pyramid
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

        // Print a space between the left and right pyramids
        printf("  ");

        // Print a new column of the right pyramid
        for (int j = 0; j <= i; j++)
        {

            printf("#");
        }
        // Create a new row in both pyramids
        printf("\n");
    }

}