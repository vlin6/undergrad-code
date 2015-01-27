; Do not add any comments beginning with @plugin

; Author: Victor Lin
; GtId: 903004194

.orig x3000
		LD R0, ARRAY_SIZE	; R0 is array_size
		LEA R1, ARRAY		; R1 is array address
		; code starts below
		LEA R2, ARRAY		; R2 is array address for j.
		AND R3, R3, 0		; difference, temporary storage
		AND R4, R4, 0		; value of i / max
		AND R5, R5, 0		; value of j
		AND R6, R6, 0		; counter (array size aka bounds)
		AND R7, R7, 0		; temporary storage

		;sort method: each time we loop, we put put at the start of the array the largest number.
		;we compare the start of the number with each of the other numbers, and swap when necessary, then we increment the start.
		
		ADD R6, R0, #0; we will be using this as our bounds	

		;initializing / updating values
INCJ		LDR R4, R1, #0; i
		ADD R6, R6, #-1; decrement the counter
		BRz NEXT
		ADD R2, R2, #1; updating the address of j
		LDR R5, R2, #0; j
		
		
		;compares this value with the next value, and swap if next value is larger.
SWAP		NOT R7, R5;
		ADD R7, R7, #1; make R7 negative j
		AND R3, R3, 0;
		ADD R3, R4, R7;
		BRp INCJ; if the number is positive, which means i is bigger, go back to top.

		AND R3, R3, 0;
		ADD R3, R4, 0;
		ADD R4, R5, 0;
		ADD R5, R3, 0;
		; need a way to keep j's address, or store it right away
		STR R4, R1, #0;
		STR R5, R2, #0;
		BR INCJ;		

NEXT		ADD R0, R0, #-1;
		BRz DONE
		ADD R1, R1, #1;
		AND R2, R2, 0;
		ADD R2, R1, 0;
		ADD R6, R0, #0; we will be using this as our bounds
		BR INCJ

DONE		HALT					; Stop program

ARRAY_SIZE 	.fill 	5

ARRAY		.fill 	3
		.fill 	31
		.fill	12
		.fill 	6
		.fill	100
.end
