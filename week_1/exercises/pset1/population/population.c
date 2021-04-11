#include <stdio.h>
// Only works on CS5 IDE
//#include <cs50.h>

int main(void)
{
    int current_size = 0, end_size = 0, years = 0;
    do
    {
        // Get the current population of llamas
        current_size = get_int("Start size: ");
    }
    while (current_size < 9);

    do
    {
        // Get the aim population of llamas
        end_size = get_int("End size: ");
    }
    while (end_size < current_size);

    // Calculate how many years it takes to reach the aim population of llamas
    while (current_size < end_size)
    {
        int born = current_size / 3;
        int passed_away = current_size / 4;
        current_size = current_size + born - passed_away;
        years++;
    }

    // Print out the years that took to reach the aim population of llamas
    printf("Years: %d\n", years);

}
