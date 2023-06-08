#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // check that argument count is two
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
    // keep track of location of input file
    // mode r opens file for reading
    FILE *input = fopen(argv[1], "r");

    // check that input file is valid
    if (input == NULL)
    {
        printf("File cannot be opened\n");
        return 2;
    }

    // store 512 bytes in array
    unsigned char buffer[512];
    int count = 0;
    // pointer for recovered images
    FILE *output = NULL;
    // allocate space for 8 bit chars
    char *filename = malloc(8 * sizeof(char));

    while (fread(buffer, sizeof(char), 512, input))
    {
        // check for JPEG start bytes
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (output != NULL)
            {

                fclose(output);
            }
            sprintf(filename, "%03d.jpg", count++);
            output = fopen(filename, "w");
        }
        if (output != NULL)
        {
            fwrite(buffer, sizeof(char), 512, output);
        }
    }
    if (output != NULL)
    {
        free(filename);
        fclose(output);
    }

    fclose(input);

    return 0;
}