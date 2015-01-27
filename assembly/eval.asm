; Name: Victor Lin

; Main
; Do not edit this function!

.orig x3000

	LD R6, STACK	; Initialize the stack
 
	LEA R0, STRING	; R0 = &str[0]
	ADD R1, R0, 0   ;

SL_LOOP	LDR R2, R1, 0	; \ R1 = strlen(str)
	BRz SL_END	; |
	ADD R1, R1, 1	; |
	BR SL_LOOP	; |
SL_END	NOT R2, R0	; |
	ADD R2, R2, 1	; |
	ADD R1, R1, R2	; /

	ADD R6, R6, -2	; \ R0 = eval(str, len)
	STR R0, R6, 0	; |
	STR R1, R6, 1	; |
	LD R2, EVALPTR	; |
	JSRR R2		; |
	LDR R0, R6, 0	; |
	ADD R6, R6, 3	; /

	ST R0, ANS
	HALT

STACK	.fill xf000
ANS	.fill -1
EVALPTR	.fill EVAL
STRING	.stringz "3*2+3*4+3*2+3+3"
	.blkw 200

; third local	| right     <- R6 (stack pointer)
; second local	| left
; first local	| i	    <- R5 (frame pointer)
; OFP		|
; RA		|
; RV		|
; first argument| the string
; last argument | len 
; xf000

	; Write your function here

PLUS	.fill '+'
MULT	.fill '*'
ZERO	.fill '0'
	
	; callee handles the OFP, RV, RA.
EVAL	ADD R6, R6, #-6 ; points R6 to top of the stack (xf002 was at first argument - #6, goes through RV, RA, OFP, i, left, and stops at right)
	STR R5, R6, #3  ; store our current frame pointer into the old frame pointer (which we define as 3 below from stack pointer)
	ADD R5, R6, #2  ; set our new frame pointer (which points at the first local variable, 2 below from the stack pointer)
	STR R7, R5, #2	; store our return address, which is always in R7

	AND R0, R0, 0	;
		; initialize our local variables (to 0)
	STR R0, R5, 0	; i
	STR R0, R5, #-1	; left
	STR R0, R5, #-2	; right

	; while (i < len) - do this code unless i - len gives you positive or zero
WHILEA	LDR R0, R5, 0	; load i into R0 (R5 contains the address for i)
	LDR R1, R5, #5	; load len into R1;
	NOT R2, R1;	; R2 will contain negative of len
	ADD R2, R2, #1	; make len negative to prepare for comparison
	ADD R2, R0, R2	; 
		;only continues when it's negative (i < len)
	BRzp SKIP2

	; if (*str + i) == '+')
		;(*str + i)
	LDR R0, R5, #4	; load into R0 the address (of the first character of the string)
	LDR R1, R5, 0	; load into R1 i (the index of the character of the string)
	ADD R0, R0, R1	; R0 now has the address + i (of our actual character)
	LDR R2, R0, 0	; R2 now has the actual ascii value of the character
		;'+'
	LD R3, PLUS   ; get the ascii code for '+'
	NOT R3, R3    ; invert
	ADD R3, R3, #1; negative of '+' to prepare our comparison
	AND R4, R4, 0 ;
	ADD R4, R2, R3; we only continue if it's 0, meaning we've found a '+'.
	BRnp SKIP

	; left = eval(str, i)
		; first move stack pointer up 2
	ADD R6, R6, #-2	; move our stack pointer up 2, to store our 2 arguments.
		; caller handles the arguments
	LDR R0, R5, #4	; load into R0 the character's address (the value of our first argument)
	STR R0, R6, #0	; (str) stores the character's address as our first argument
	LDR R0, R5, #0	; loads into R0 i (the value of our second argument)
	STR R0, R6, #1	; (i) stores i as our second argument
	JSR EVAL
		; store left into the local variable
		;stack pointer (R6) is pointing at address of the return value
	LDR R0, R5, #4	; reload my str address
	LDR R4, R6, 0	; load into R4 my return value (for left)
	STR R4, R5, #-1 ; store left into local variable left
	ADD R6, R5, #-2	; reload my stack pointer back to the top (previously it pointed to the return value)

	; right = eval(str + i + 1, len - i - 1)
		; first move stack pointer up 2
	ADD R6, R6, #-2
		;str + i + 1
	LDR R0, R5, #4	; load into R0 the character's address
	LDR R1, R5, #0	; load into R1 i
	ADD R0, R0, R1	; str + i
	ADD R0, R0, #1  ; R0 contains (str + i + 1)
	STR R0, R6, #0	; store R0 into first argument
		;len - i - 1
	LDR R0, R5, #5	; load into R0 the len
	LDR R1, R5, #0	; load into R1 i
	NOT R1, R1	;
	ADD R1, R1, #1	; R1 holds -i
	ADD R0, R0, R1	; str - i
	ADD R0, R0, #-1 ; R0 contains (str - i - 1)
	STR R0, R6, #1	; store R0 into second argument
	JSR EVAL
		; store right into the local variable
		; stack pointer (R6) is pointing at address of the return value
	LDR R0, R5, #4	; reload my str address
	LDR R4, R6, 0	; load into R4 my return value (for right)
	STR R4, R5, #-2 ; store right into local variable right ;
	ADD R6, R5, #-2	; reload my stack pointer back to the top (previously it pointed to the return value)

		; return left + right
	LDR R1, R5, #-1; load into R1 left
	LDR R2, R5, #-2; load into R2 right
	ADD R0, R1, R2; R0 is left + right
	BR RETURN

SKIP	LDR R1, R5, 0	; load i into R1
	ADD R1, R1, #1	; (i++)  
	STR R1, R5, 0	; store this incremented i
	BR WHILEA

SKIP2 

	AND R0, R0, 0	;
		; initialize our local variables (to 0)
	STR R0, R5, 0	; i
	STR R0, R5, #-1	; left
	STR R0, R5, #-2	; right

	; while (i < len) - do this code unless i - len gives you positive or zero
WHILEB	LDR R0, R5, 0	; load i into R0 (R5 contains the address for i)
	LDR R1, R5, #5	; load len into R1;
	NOT R2, R1;	; R2 will contain negative of len
	ADD R2, R2, #1	; make len negative to prepare for comparison
	ADD R2, R0, R2	; 
		;only continues when it's negative (i < len)
	BRzp SKIP3

	; if (*str + i) == '+')
		;(*str + i)
	LDR R0, R5, #4	; load into R0 the address (of the first character of the string)
	LDR R1, R5, 0	; load into R1 i (the index of the character of the string)
	ADD R0, R0, R1	; R0 now has the address + i (of our actual character)
	LDR R2, R0, 0	; R2 now has the actual ascii value of the character
		;'*'
	LD R3, MULT   ; get the ascii code for '*'
	NOT R3, R3    ; invert
	ADD R3, R3, #1; negative of '*' to prepare our comparison
	AND R4, R4, 0 ;
	ADD R4, R2, R3; we only continue if it's 0, meaning we've found a '*'.
	BRnp SKIPB

	; left = eval(str, i)
		; first move stack pointer up 2
	ADD R6, R6, #-2	; move our stack pointer up 2, to store our 2 arguments.
		; caller handles the arguments
	LDR R0, R5, #4	; load into R0 the character's address (the value of our first argument)
	STR R0, R6, #0	; (str) stores the character's address as our first argument
	LDR R0, R5, #0	; loads into R0 i (the value of our second argument)
	STR R0, R6, #1	; (i) stores i as our second argument
	JSR EVAL
		; store left into the local variable
		;stack pointer (R6) is pointing at address of the return value
	LDR R0, R5, #4	; reload my str address
	LDR R4, R6, 0	; load into R4 my return value (for left)
	STR R4, R5, #-1 ; store left into local variable left
	ADD R6, R5, #-2	; reload my stack pointer back to the top (previously it pointed to the return value)

	; right = eval(str + i + 1, len - i - 1)
		; first move stack pointer up 2
	ADD R6, R6, #-2
		;str + i + 1
	LDR R0, R5, #4	; load into R0 the character's address
	LDR R1, R5, #0	; load into R1 i
	ADD R0, R0, R1	; str + i
	ADD R0, R0, #1  ; R0 contains (str + i + 1)
	STR R0, R6, #0	; store R0 into first argument
		;len - i - 1
	LDR R0, R5, #5	; load into R0 the len
	LDR R1, R5, #0	; load into R1 i
	NOT R1, R1	;
	ADD R1, R1, #1	; R1 holds -i
	ADD R0, R0, R1	; str - i
	ADD R0, R0, #-1 ; R0 contains (str - i - 1)
	STR R0, R6, #1	; store R0 into second argument
	JSR EVAL
		; store right into the local variable
		; stack pointer (R6) is pointing at address of the return value
	LDR R0, R5, #4	; reload my str address
	LDR R4, R6, 0	; load into R4 my return value (for right)
	STR R4, R5, #-2 ; store right into local variable right ;
	ADD R6, R5, #-2	; reload my stack pointer back to the top (previously it pointed to the return value)

		; return left + right
	LDR R1, R5, #-1; load into R1 left
	LDR R2, R5, #-2; load into R2 right
		; left * right is to add left 'right' number of times.
		; use right as a counter
	AND R3, R3, 0; R3 will contain the product
TIMES	ADD R3, R3, R1; 
	ADD R2, R2, #-1;
	BRp TIMES
	ADD R0, R3, 0;
	BR RETURN

SKIPB	LDR R1, R5, 0	; load i into R1
	ADD R1, R1, #1	; (i++)  
	STR R1, R5, 0	; store this incremented i
	BR WHILEB

SKIP3 
	; *str - '0' (converting data to decimal by str minus '0', the source)
	LDR R0, R5, #4; gets you the address of the character
	LDR R0, R0, 0; gets you the ascii value of character
	LD R1, ZERO; gets you the ascii value of zero
	NOT R1, R1;
	ADD R1, R1, #1; get ready to minus the source
	ADD R0, R0, R1;
	BR RETURN

RETURN 	; handles RV, RA, point the return value
	STR R0, R5, #3	; save return value (make sure before you get here that R0 is your return value)
	LDR R7, R5, #2 	; restore return address
	ADD R6, R5, #3	; R6 -> return value (point the stack pointer to return value)
	LDR R5, R5, #1	; restore R5 as old frame pointer
	RET
.end
