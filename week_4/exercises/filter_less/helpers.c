#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Takes the red value of the curent pixel
            int red = image[i][j].rgbtRed;
            // Takes the blue value of the currente píxel
            int blue = image[i][j].rgbtBlue;
            // Takes the green value of the current pixel
            int green = image[i][j].rgbtGreen;

            // Calculates the average of the red, green, and blue pizel
            int new_value = round((red + blue + green) / 3.0);

            // Set the new RGB value to the current pixel
            image[i][j].rgbtRed = new_value;
            image[i][j].rgbtGreen = new_value;
            image[i][j].rgbtBlue = new_value;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int original_red;
    int original_blue;
    int original_green;
    int sepia_red;
    int sepia_blue;
    int sepia_green;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Takes the red value of the curent pixel
            original_red = image[i][j].rgbtRed;
            // Takes the blue value of the currente píxel
            original_blue = image[i][j].rgbtBlue;
            // Takes the green value of the current pixel
            original_green = image[i][j].rgbtGreen;

            // Calculates the new value of the RGB of the current pixel
            sepia_red = round((0.393 * original_red) + (0.769 * original_green) + (0.189 * original_blue));
            sepia_green = round((0.349 * original_red) + (0.686 * original_green) + (0.168 * original_blue));
            sepia_blue = round((0.272 * original_red) + (0.534 * original_green) + (0.131 * original_blue));

            // Set the new RGB value to the current pixel
            image[i][j].rgbtRed = (sepia_red < 256 ? sepia_red : 255);
            image[i][j].rgbtGreen = (sepia_green < 256 ? sepia_green : 255);
            image[i][j].rgbtBlue = (sepia_blue < 256 ? sepia_blue : 255);
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE aux;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            aux = image[i][width - 1 - j];
            image[i][width - 1 - j] = image[i][j];
            image[i][j] = aux;
        }
    }
}


// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    int posRow[9] = {-1, -1, -1, 0, 0, 0, 1, 1, 1};
    int posCol[9] = {-1, 0, 1, -1, 0, 1, -1, 0, 1};
    int possibleRow;
    int possibleCol;

    float total_pixels = 0.0;
    int sum_red = 0;
    int sum_blue = 0;
    int sum_green = 0;

    // Create a copy of the image to take the original values of the image while the original one is being modified.
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }


    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sum_red = 0;
            sum_blue = 0;
            sum_green = 0;
            total_pixels = 0.0;

            // Adds up the RGB values of the adjacent pixels of the current pixel
            for (int k = 0; k < 9; k++)
            {
                possibleRow = i + posRow[k];
                possibleCol = j + posCol[k];

                if ((possibleRow < height && possibleRow >= 0) && (possibleCol < width && possibleCol >= 0))
                {
                    sum_red += copy[possibleRow][possibleCol].rgbtRed;
                    sum_green += copy[possibleRow][possibleCol].rgbtGreen;
                    sum_blue += copy[possibleRow][possibleCol].rgbtBlue;
                    total_pixels++;
                }
            }

            // Set the new RGB value of the current pixel
            image[i][j].rgbtRed = round(sum_red / total_pixels);
            image[i][j].rgbtBlue = round(sum_blue / total_pixels);
            image[i][j].rgbtGreen = round(sum_green / total_pixels);
        }
    }
    return;
}