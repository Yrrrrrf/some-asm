; This file represents a Hello World program in AssemblyX86.
; It is a simple program that prints "Hello, World!" to the console.

section .data                   ; This section is for initialized data
helloMessage db 'Hello, World!',0xa  ; Define a byte array 'Hello, World!' followed by newline character (0xa)
len equ $-helloMessage          ; Calculate the length of helloMessage

section .text                   ; This section is for code
global _start                   ; Declare the starting point for the linker

_start:                         ; This is where execution starts
    mov eax, 4                  ; System call number for sys_write (to write to a file/stdout)
    mov ebx, 1                  ; File descriptor 1 is stdout
    mov ecx, helloMessage       ; Pointer to the message to write
    mov edx, len                ; Length of the message to write
    int 0x80                    ; Interrupt to make the system call

    mov eax, 1                  ; System call number for sys_exit (to exit the program)
    mov ebx, 0                  ; Exit status 0 (success)
    int 0x80                    ; Interrupt to make the system call
