org 100h

.DATA
    helloMessage db 'Hello World', '$'

.CODE
start:
    ; Print the message the first time
    mov ah, 9       ; DOS service to display string
    lea dx, helloMessage ; Load the address of helloMessage into dx
    int 21h         ; Call DOS interrupt

    ; Print the message the second time
    mov ah, 9       ; DOS service to display string again
    lea dx, helloMessage ; Load the address of helloMessage into dx again
    int 21h         ; Call DOS interrupt again

    mov ah, 4ch     ; DOS service to return control to DOS
    int 21h         ; Call DOS interrupt

ret
