# NASBT SPEC DOC — EDITION 3T
NASBT is an esoteric programming language, kinda
A vomit of INTERCAL, Brainfuck and BASIC

Made for fun

***

NASBT is a *stack-based language*, the stack is a list of numbers that can be manipulated throughout the code, it has no fixed size, the pointer is used to change, output, etc. the stack, it's position can be changed, most instructions are based on the value that the pointer is at

Values in the stack have no limits, they can be negative or be the biggest number you have ever seen in your life

NASBT's file extension is .nsbt or .nasbt

the code is executed line-by-line

***

# INSTRUCTIONS
There can only be one instruction executed per line
Some have args, some don't
Semicolons are comments

Parentheses are obligatory args, brackets are optional args

## BASIC INSTRS.
PUSH (num) - Adds a value to the stack

DUP - Duplicates the value that the pointer is at

SWAP - Swaps the bottom and the top stack values

POP - Pops a value from the stack

REMOVE - Pops the value that the pointer is at 
from the stack

CLEAR - Removes all the values from the stack

INPUT (ASCII/NUMERIC) - receives input, ASCII mode adds the a

OUTPUT - Prints the current ASCII/Decimal Unicode value that the pointer is at into the console, no newline

MESSAGE (text) - Prints text into the console, no newline

INCREMENT - Increments the value that the pointer is at by 1

DECREMENT - Decrements the value that the pointer is at by 1

STACK - Prints the stack into the console, debug tool

PEEK - Prints the value that the pointer is at,
debug tool

DUMP - Prints the stack and the pointer position, debug tool

## POINTER MOVEMENT
MOVE (LEFT/RIGHT) - Moves the pointer on the stack left or right, wraps around

TOP - Moves the pointer to the end of the stack

BOTTOM - Moves the pointer to the start of the stack

TELEPORT - Moves the pointer to a specific position based on the value that the pointer is at

## CONTROL FLOW
JUMP (line) [IF/IFNOT] [value] - Jumps to a specific line, the condition value is checked with the value that the pointer is at

ERROR <text> - Raises an error

HALT - Stops the program's execution

## OTHER
RAND (min) (max) - Adds a random value between min and max to the stack

INSTRUCTION - Does nothing

***

# VERSION SUFFIXES
f - bugfix

p - patch

q - quality of life

hf - hotfix

r - revision

mu - minor update

xp - experimental
