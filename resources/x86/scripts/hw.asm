.model small

.data segment
        saludo db "Hola mundo", "$"
        ends
.code segment
        programa:
                mov ax, seg, saludo
                mov ds, ax
                mov ah, 09h
                lea dx, saludo
                int 21h
                mov ax, 4c00h
                int 21h
        end programa
