; DO NOT ADD ANY LINES THAT BEGIN WITH @plugin OR YOU RISK GETTING A ZERO FOR THIS PART.

; Author: Victor Lin
; GtId: 903004194

.orig x3000
		; clear all registers we'll be using
		AND R0, R0, 0				; Register for divisor, remainder
		AND R1, R1, 0				; Register for dividend
		AND R2, R2, 0				; Register for quotient
		AND R3, R3, 0				; Register to prevent negative remainders

		; load divisor and dividend into respective registers
		LD R0, U				; U
		LD R1, V				; V
		BRz ZERO				;

		;2s complement v to make it negative
		NOT R1, R1				; invert v
		ADD R1, R1, #1				; add one.

START		ADD R3, R0, R1				; first, check if the dividend > divisor; we use a new register to avoid negative remainders
		BRn BREAK				; if it is, we're trying to overdivide, so branch to BREAK to break out of the loop
		; if dividend is smaller than divisor...
		ADD R2, R2, #1				; loop begins with incrementing quotient
		; remember R1 contains -V
		
		ADD R0, R0, R1				; we're using the divisor register as the remainder since we don't need it's original state
		BRp START				; loop (i.e. branch to START) if divisor is positive				;
		
		; when we're done with the loop, we always store the quotient and remainder
BREAK		ST R2, QUOTIENT				; store the value of the quotient register into the quotient
		ST R0, REMAINDER			; store the value of the remaining divisor into the remainder
		BR END					;

ZERO		NOT R2, R2				; -1
		ST R2, QUOTIENT				;		
		BR END					;
	
END		HALT					; Stop program x300F

		; Change U and V to suit your needs
		U .fill 23				; Initialize U
		V .fill 7				; Initialize V
		QUOTIENT .blkw 1			; Store your quotient here
		REMAINDER .blkw 1			; Store your remainder here
.end

