; exit.asm
; A program that cleanly exits 8086tiny.

org 0x100

; 8086tiny uses an OUT instruction to port 0x78
; as a special signal to terminate the emulator.
; We can put any value in AL.
mov al, 0
out 0x78, al

; The code will never reach here, but hlt is good practice.
hlt
