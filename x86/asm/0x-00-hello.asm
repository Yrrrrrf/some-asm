; =============================================================================
;   0x-00-skeleton.asm
;   A minimal boilerplate for an 8086 .com program.
;
;   This program does nothing except load and then immediately exit cleanly
;   using the standard DOS termination interrupt. It is the simplest
;   functional program you can write.
; =============================================================================

org 0x100           ; Origin for a .com program. This tells the assembler
                    ; that the code will be loaded at memory address 0x100,
                    ; which is standard for all .com files.

section .text
global _start

_start:
    ; The program's execution begins here.
    ; Since we want to do nothing, we proceed directly to the exit call.


    ; --- Exit the program gracefully ---
    ; To terminate a program and return control to the operating system (DOS),
    ; we use interrupt 0x21 with the exit function (0x4C) in the AH register.
    mov ah, 0x4C
    int 0x21           ; Call the DOS interrupt to terminate the program.
