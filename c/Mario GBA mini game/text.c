#include "myLib.h"
#include "text.h"


void drawChar(int row, int col, char ch, u16 color)
{
    int r, c;
    for(r=0; r<8; r++)
    {
        for(c=0; c<6; c++)
        {
            if(fontdata_6x8[OFFSET(r, c, 6) + ch*48])
            {
                setPixel4(row+r, col+c, color);
            }
        }
    }
}

void drawString(int row, int col, char *str, u16 color)
{
    while(*str)
    {
        drawChar(row, col, *str++, color);
        col+= 6;
    }
}
