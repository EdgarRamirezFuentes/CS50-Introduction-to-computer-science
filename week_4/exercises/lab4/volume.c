// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Get the factor from user
    float factor = atof(argv[3]);

    uint8_t *header = NULL;

    // Allocate the necessary memory to store the header from the source file
    header = malloc(HEADER_SIZE * sizeof(uint8_t));
    // It was not possible to allocate the necessary memory to read teh header of the souce file.
    if (!header)
    {
        return 1;
    }

    // Read the header from the source file
    fread(header, sizeof(uint8_t), HEADER_SIZE, input);
    // Copy the header from the source file to the destiny file
    fwrite(header, sizeof(uint8_t), HEADER_SIZE, output);

    int16_t sample;
    // Read each sample of the file until it gets to the end.
    while (fread(&sample, sizeof(int16_t), 1, input))
    {
        // Increase the volume of the sample
        sample *= factor;
        // Write (copy) the modified sample to the destiny file
        fwrite(&sample, sizeof(int16_t), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);

    // Free the allocated memory to avoid memory leaks
    free(header);
}
