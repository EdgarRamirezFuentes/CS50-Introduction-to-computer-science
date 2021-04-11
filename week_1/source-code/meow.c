#include <stdio.h>

// Prototype
void meow(void);
void meowLoop(int);
int main(void)
{
    int counter = 0;
    // Using for loop to print out Meow! three times using our own functiom called meow
    for(int i = 0; i < 3; i++)
    {
        meow();
    }

    // Using while loop to print out Meow! three times using our own functiom called meow
    while(counter < 3)
    {
        meow();
        counter++;
    }

    meowLoop(3);

    return 0;
}

void meow(void)
{
    printf("Meow!\n");
}

void meowLoop(int counter)
{
    for(int i = 0; i < counter; i++)
    {
        printf("Meow!\n");
    }
}