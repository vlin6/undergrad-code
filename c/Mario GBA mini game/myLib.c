#include "myLib.h"
#include "minigame.h"
#include "text.h"
#include "youwin.h"
#include "youlose.h"
#include <stdlib.h>
#include <stdio.h>

u16* videoBuffer = (u16*) 0x6000000;

void setPixel4 (int r, int c, u8 color)
{
	int pixel = OFFSET(r, c, 240);
	int whichShort = pixel/2; //since half of mode4 is reserved for the other screen.
	if (c&1) { //odd columns correspond with the left side of the pixel byte, [0 1] <-> [1 0]
		//clear the left side of the pixel byte and replace it with color palette pointer
		videoBuffer[whichShort] = (videoBuffer[whichShort] & 0x00FF) | (color << 8);
	} else {
		videoBuffer[whichShort] = (videoBuffer[whichShort] & 0xFF00) | (color);
	}
}

void drawRect4 (int r, int c, int width, int height, u8 index) {
	int row;
	//this is the mode3 set up
	volatile u16 color = (index << 8) || index;

	for (row = 0; row < height; row++) {
		DMA[3].src = &color;
		DMA[3].dst = &videoBuffer[OFFSET(r+row, c, 240)>>1];
		int width4 = width>>1;
		DMA[3].cnt = DMA_ON | width4 | DMA_DESTINATION_INCREMENT | DMA_SOURCE_FIXED;
	}
}

void drawImage4 (int r, int c, int width, int height, const u16* image) {
	int row;
	//this is the mode3 set up
	for (row = 0; row < height; row++) {
		int width4 = width>>1;
		DMA[3].src = &image[OFFSET(row, 0, width4)];
		DMA[3].dst = &videoBuffer[OFFSET(r+row, c, 240)>>1];
		DMA[3].cnt = DMA_ON | DMA_DESTINATION_INCREMENT | DMA_SOURCE_INCREMENT | width4;
	}
}

void setPalette (const u16* palette)
{
	DMA[3].src = palette;
	DMA[3].dst = PALETTE;
	DMA[3].cnt = DMA_ON | MINIGAME_PALETTE_SIZE;
}

void fillScreen4(u8 index)
{	
	volatile u16 color = (index<<8) | index;
	DMA[3].src = &color;
	DMA[3].dst = videoBuffer;
	DMA[3].cnt = DMA_ON | DMA_SOURCE_FIXED | 19200;	
}

void waitForVblank() {
	while(SCANLINECOUNTER < 160);
	while(SCANLINECOUNTER > 160);
}

void walk_right_one(MOVOBJ* player) {

	drawImage4(player->row, player->col, MARIO_RIGHT_ONE_WIDTH, MARIO_RIGHT_ONE_HEIGHT, mario_right_one);

}

void walk_right_two(MOVOBJ* player) {

	drawImage4(player->row, player->col, MARIO_RIGHT_TWO_WIDTH, MARIO_RIGHT_TWO_HEIGHT, mario_right_two);

}

void walk_right_three(MOVOBJ* player) {

	drawImage4(player->row, player->col, MARIO_RIGHT_THREE_WIDTH, MARIO_RIGHT_THREE_HEIGHT, mario_right_three);

}

void walk_right_four(MOVOBJ* player) {

	drawImage4(player->row, player->col, MARIO_RIGHT_FOUR_WIDTH, MARIO_RIGHT_FOUR_HEIGHT, mario_right_four);

}

void walk_left_one(MOVOBJ* player) {

	drawImage4(player->row, player->col, MARIO_LEFT_ONE_WIDTH, MARIO_LEFT_ONE_HEIGHT, mario_left_one);

}

void walk_left_two(MOVOBJ* player) {

	drawImage4(player->row, player->col, MARIO_LEFT_TWO_WIDTH, MARIO_LEFT_TWO_HEIGHT, mario_left_two);

}

void walk_left_three(MOVOBJ* player) {

	drawImage4(player->row, player->col, MARIO_LEFT_THREE_WIDTH, MARIO_LEFT_THREE_HEIGHT, mario_left_three);

}

void walk_left_four(MOVOBJ* player) {

	drawImage4(player->row, player->col, MARIO_LEFT_FOUR_WIDTH, MARIO_LEFT_FOUR_HEIGHT, mario_left_four);

}

void jump_left(MOVOBJ* player) {

	drawImage4(player->row, player->col, MARIO_JUMP_LEFT_WIDTH, MARIO_JUMP_LEFT_HEIGHT, mario_jump_left);

}

void jump_right(MOVOBJ* player) {

	drawImage4(player->row, player->col, MARIO_JUMP_RIGHT_WIDTH, MARIO_JUMP_RIGHT_HEIGHT, mario_jump_right);

}

void walk_right(MOVOBJ* player)  {

	drawImage4(player->row, player->col, GOOMBA_RIGHT_WIDTH, GOOMBA_RIGHT_HEIGHT, goomba_right);

}

void walk_left(MOVOBJ* player)  {

	drawImage4(player->row, player->col, GOOMBA_LEFT_WIDTH, GOOMBA_LEFT_HEIGHT, goomba_left);

}

void stand(MOVOBJ* player) {

	drawImage4(player->row, player->col, GOOMBA_STAND_WIDTH, GOOMBA_STAND_HEIGHT, goomba_stand);

}

void checkBounds(MOVOBJ* player) {
	if(player->col < 0)
	{
		player->col = 0;
	}
	if(player->col > 240 - 1 - MARIO_WIDTH + 1) 
	{
		player->col = 240 - 1 - MARIO_WIDTH + 1;
	}
	if(player->row < 0)
	{
		player->row = 0;
	}
	if(player->row > SCREENHEIGHT - MARIO_HEIGHT) 
	{
		player->row = SCREENHEIGHT - MARIO_HEIGHT;
	}
}


//displays one screen, writes to another.
void flipPage()
{
	if(REG_DISPCTL & BUFFER1FLAG)
	{
		//screen displays buffer0, we write to buffer1
		REG_DISPCTL = REG_DISPCTL & ~BUFFER1FLAG;
		videoBuffer = BUFFER1;
	}
	else
	{
		REG_DISPCTL = REG_DISPCTL | BUFFER1FLAG;
		videoBuffer = BUFFER0;
	}
}

void goombasLeft(int num, char buffer[]) {
	sprintf(buffer, "Goomba affection pts: %d", num); //puts all this into the buffer
       	drawRect4(150, 5, 100, 50, BLACK);
	drawString(150, 5, buffer, 2);
}


/* these are collision algorithms from hw 10 
 . . . . . . . . . . . . . . . . . . . . . . . . .
 . . . . . . . . . . . . . . . . . . . . . . . . .
 . . . . . . . . . . . . . . . . . . . . . . . . .
 . . . . . . . . . . . . . . . . . . . . . . . . .
 . . . . . . . . . . . . . . . . . . . . . . . . .
*/


/*int collideTop(MOVOBJ* player, MOVOBJ* goomba) {
	if (	//use top left vertex as reference point
		((player->row + MARIO_HEIGHT) == (goomba->row)) && //check if row of bottom of player same as the platform
		(( ((player->col + MARIO_WIDTH) > (goomba->col)) && ((player->col + MARIO_WIDTH) < (goomba->col+GOOMBA_WIDTH)) ) ||
		( ((player->col) > (goomba->col)) && ((goomba->col) < (goomba->col+GOOMBA_WIDTH)) )) //check if left side is in bound
	)
	{
		return 1;
	}
	return 0;
}
*/


int collide(MOVOBJ* player, MOVOBJ* goomba) {
	//we check if a point in a certain region
	//point x, y;
	//if((x > player->col && x < player->col + player->width) && (y > player->row && y < player->row + player->size)){ return 1; }
	
	//top left vertex from enemy
	if ( (goomba->col > player->col && goomba->col < (player->col + MARIO_WIDTH)) && (goomba->row > player->row && goomba->row < (player->row + MARIO_HEIGHT)) )
	{ return 1; }
	
	//top right vertex from enemy
	if ( ( (goomba->col + GOOMBA_WIDTH) > player->col && (goomba->col + GOOMBA_WIDTH) < (player->col + MARIO_WIDTH)) && (goomba->row > player->row && goomba->row < (player->row + MARIO_HEIGHT)) )
	{ return 1; }

	//bottom left vertex from enemy
	if ( (goomba->col > player->col && goomba->col < (player->col + MARIO_WIDTH)) && ( (goomba->row + GOOMBA_HEIGHT) > player->row && (goomba->row + GOOMBA_HEIGHT) < (player->row + MARIO_HEIGHT)) )
	{ return 1; }

	//bottom right vertex from enemy
	if ( ((goomba->col + GOOMBA_WIDTH) > player->col && (goomba->col + GOOMBA_WIDTH) < (player->col + MARIO_WIDTH)) && ( (goomba->row + GOOMBA_HEIGHT) > player->row && (goomba->row + GOOMBA_HEIGHT) < (player->row + MARIO_HEIGHT)) )
	{ return 1; }

	return 0;
}

void drawRect(int row, int col, int width, int height, volatile u16 color)
{
    int r;
    for(r=0; r<height; r++)
    {
        DMA[3].src = &color;
        DMA[3].dst = &videoBuffer[OFFSET(row+r, col, 240)]; //it'll start here
        DMA[3].cnt = width | DMA_DESTINATION_INCREMENT | DMA_SOURCE_FIXED | DMA_ON; //the DMA_DESTINATION_INCREMENT handles the columns until width is reached.
    }
}

/*
* drawimage3
* A function that will draw an arbitrary sized image
* onto the screen (with DMA).
* @param r row to draw the image
* @param c column to draw the image
* @param width width of the image
* @param height height of the image
* @param image Pointer to the first element of the image.
*/
void drawImage3 (int row, int col, int width, int height, const u16* image) {
	int r;
	/* 
	* we use the DMA to transfer a row of pixels.
	* we increment both the src and dst to transfer a 'width' amount of pixels per row,
	* before incrementing the for loop to do this for the next row.
	*/
	for (r = 0; r<height; r++) {
		DMA[3].src = &image[OFFSET(r, 0, width)]; //the address of the starting pixel of that file 
			//recall: if a is a pointer,
			//a[1] is the same as *(a + 1), and &a[1] is the same as &(*(a + 1)), 
			//which gives you a pointer (&) to the (dereferenced, *) int at a + 1
		DMA[3].dst = &videoBuffer[OFFSET(row+r, col, 240)];
		DMA[3].cnt = width | DMA_DESTINATION_INCREMENT | DMA_SOURCE_INCREMENT | DMA_ON;
		//we specify 'width' in the count register as the number of pixels we want to make per transfer
		//we specify incrementing src and dst because we'll be transferring different pixels
	}
}


int win(int num) {
	if (num < 0) {
		return 1;
	}
	return 0;
}

int lose(int num) {
	if (num > 500) {
		return 1;
	}
	return 0;
}

void victory() {
	drawImage3 (0, 0, YOUWIN_WIDTH, YOUWIN_HEIGHT, youwin);	
}

void defeat() {
	drawImage3 (0, 0, YOULOSE_WIDTH, YOULOSE_HEIGHT, youlose);	
}
