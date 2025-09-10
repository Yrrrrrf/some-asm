org 100h

.DATA
    message db 'Hi bro', 0Dh, 0Ah, '$' ; Add carriage return and line feed for a newline

.CODE
start:
    mov cx, 10     ; Counter for the loop, set to 10 for ten iterations

print_loop:
    mov ah, 9      ; DOS service to display string
    lea dx, message; Load the address of the message into dx
    int 21h        ; Call DOS interrupt

    dec cx         ; Decrement the counter
    jnz print_loop ; Jump to print_loop if CX is not zero (JNZ = Jump if Not Zero)

    mov ah, 4ch    ; DOS service to return control to DOS
    int 21h        ; Call DOS interrupt

ret
