; Author: Victor Lin
; GtId: 903004194

.orig x3000
	;set up our registers
	LD R0, K; the potential prime number
	AND R1, R1, 0; the divisor
	AND R2, R2, 0; half of the potential prime
	AND R3, R3, 0; prime or not (remainder is 0 or not)
	LD R4, K; the prime number

	;gets k/2 into R2
	; what is half? if you take a number, substract it twice, and you get either 1 or 0.
	AND R5, R5, 0; potential half
	AND R6, R6, 0; half in negative
	
START	ADD R4, R4, #1;


HLOOP	AND R0, R0, 0;
	ADD R0, R4, 0;
	ADD R5, R5, #1;
	NOT R6, R5;
	ADD R6, R6, #1;
	ADD R0, R0, R6; twice
	ADD R0, R0, R6;
	BRp HLOOP
	BRz READY
	ADD R5, R5, #-1;
READY	ADD R2, R5, 0;
	
	AND R1, R1, 0; Reset divisor
	ADD R1, R1, #1; this gives register a divisor of 2

DIV	ADD R1, R1, #1; increment the divisor
	;CHECK to see if the divisor is not larger than k/2
CHECK	AND R5, R5, 0; 
	NOT R6, R1;
	ADD R6, R6, #1; make divisor negative
	ADD R5, R2, R6; Half of our prime - Divisor
	BRn DONE

;MOD is a loop that lets you get the remainder into R3
	AND R0, R0, 0;
	ADD R0, R4, 0;
	NOT R5, R1;
	ADD R5, R5, #1; R5 now negative divisor
MOD	ADD R0, R0, R5;
	BRp MOD
 	AND R3, R3, 0;
	ADD R3, R3, R0;
	BRz START
	ADD R3, R3, R1; if we 'divided' past zero, add the dividend back one.
	BRp DIV

DONE	ST R4, NEXTPRIME;

	K		.fill	712			; K
	NEXTPRIME	.blkw 	1			; store your answer here
.end
