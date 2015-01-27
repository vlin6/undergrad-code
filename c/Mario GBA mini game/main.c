#include <stdlib.h>
#include <stdio.h>

#include "minigame.h"
#include "startscreen.h"
#include "youwin.h"
#include "youlose.h"
#include "myLib.h"


#define NUM_ENEMIES 2
int state = BEGIN;

int main() {

	while(1)
	{
		switch(state)
		{
		case BEGIN:
			begin();
			state = GAME;
			break;
		case GAME:
			game();
			break;
		case SUCCESS:
			success();
			break;
		case FAILURE:
			failure();
			break;
		default:
			// handle error
			break;
		}
	}
	return 0;
}

void begin() {
	REG_DISPCTL = MODE3 | BG2_ENABLE;
	drawImage3 (0, 0, STARTSCREEN_WIDTH, STARTSCREEN_HEIGHT, startscreen);
	while(!KEY_DOWN_NOW(BUTTON_START)) {}
	drawRect(0, 0, 240, 160, BLACK);
}

void game() {

	//Set up screen
	videoBuffer = BUFFER0;
	REG_DISPCTL = MODE4 | BG2_ENABLE;
	setPalette(minigame_palette);

	//set up goombas
	char buffer[41];
	int goombas = 120;

	//Set up player
	MOVOBJ player;
	player.row = SCREENHEIGHT - MARIO_HEIGHT - 1; //start one pixel above the ground, so when it falls to the ground you lose.
	player.col = 0;
	player.cd = 1;
	player.rd = 3;

	//Set up goomba enemies
	static int timer = 0;
	MOVOBJ goomba[NUM_ENEMIES];
	MOVOBJ* goomba_ptr;
	int x;
	for (x = 0; x < NUM_ENEMIES; x++) {
		goomba[x].row = SCREENHEIGHT - GOOMBA_HEIGHT;
		goomba[x].col = MARIO_WIDTH + rand()%(240-MARIO_WIDTH);
		goomba[x].cd = 2;
		goomba[x].rd = 0;
	}

	//Game while loop
	while(1) {
		static int i = 0;
		static int j = 0;
		static int jump_counter = 0;
		static int time = 0;

		static int direction = STAY;
		
		static int jump = NO;
		static int fall = NO;

		/*static int jmp = 0;
		static int j = 0;*/

		
		if(KEY_DOWN_NOW(BUTTON_LEFT))
		{
			player.col -= player.cd;
			direction = LEFT;
			j = 0;
			i = (i+1) % 30;

		}
		if(KEY_DOWN_NOW(BUTTON_RIGHT))
		{
			player.col += player.cd;
			direction = RIGHT;
			i = 0;
			j = (j+1) % 30;
		}
		if(KEY_DOWN_NOW(BUTTON_UP))
		{
			jump = YES;

		}
		if(KEY_DOWN_NOW(BUTTON_SELECT))
		{
			state = BEGIN;
			break;
		}

		checkBounds(&player);

		fillScreen4(0);

		//handle goomba movement
		for(x=0; x<NUM_ENEMIES; x++) {
			goomba_ptr = &goomba[x];
			goomba_ptr->col += goomba_ptr->cd;
			if(goomba_ptr->col < 0)
			{
				goomba_ptr->col = 0;
				goomba_ptr->cd = -goomba_ptr->cd;
			}
			if(goomba_ptr->col >  240 - 1 - GOOMBA_WIDTH + 1)
			{
				goomba_ptr->col = 240 - 1 - GOOMBA_WIDTH + 1;
				goomba_ptr->cd = -goomba_ptr->cd;
			}

			if (timer < 5) {
				stand(goomba_ptr);
			} else if (timer <= 15) {
				walk_right(goomba_ptr);
			} else if (timer <= 25) {
				walk_left(goomba_ptr);
			}
			if (collide(&player, goomba_ptr)){
				jump = YES;
				goombas--;
			}
			timer = (timer + 1) % 26;
		}  


		//handle player movement
		if (direction == LEFT) {
			if (i > 0 && i < 10) {
				walk_left_one(&player);
			} else if (i >= 10 && i < 20) {
				walk_left_two(&player);
			} else if (i >= 20 && i < 30) {
				walk_left_three(&player);
			}
		}
		else if (direction == RIGHT) {
			if (j >= 0 && j < 10) {
				walk_right_one(&player);
			} else if (j >= 10 && j < 20) {
				walk_right_two(&player);
			} else if (j >= 20 && j < 30) {
				walk_right_three(&player);
			}
		}
		time++;
		if (jump == YES) {

			player.row -= player.rd;
			if (direction == LEFT && jump_counter <= 15) {
				jump_left(&player);
			} else if (direction == RIGHT && jump_counter <= 15) {
				jump_right(&player);
			} else if (jump_counter > 15){
				jump = NO;
				jump_counter = 0;
				fall = YES;
			}
			jump_counter++;
		}

		if (fall == YES) {
			player.row += player.rd;
			if (direction == LEFT && jump_counter <= 15) {
				jump_left(&player);
			} else if (direction == RIGHT && jump_counter <= 15) {
				jump_right(&player);
			} else if (jump_counter > 15){
				fall = NO;
				jump_counter = 0;
			}
			jump_counter++;
		}

		if (direction == STAY && i == 0) {
			walk_right_four(&player);
		} else if (direction == STAY && j == 0) {
			walk_left_four(&player);
		} 

		goombasLeft(goombas, buffer);

		waitForVblank();
		flipPage();

		if (win(goombas)) {
			state = SUCCESS;
			time = 0;
			break;
		}
		if (lose(time)) {
			state = FAILURE;
			time = 0;
			break;
		}

	}
}

void success() {
	REG_DISPCTL = MODE3 | BG2_ENABLE;
	victory();
	if(KEY_DOWN_NOW(BUTTON_SELECT))
	{
		state = BEGIN;
	}
}
void failure() {
	REG_DISPCTL = MODE3 | BG2_ENABLE;
	defeat();
	if(KEY_DOWN_NOW(BUTTON_SELECT))
	{
		state = BEGIN;
	}
}
