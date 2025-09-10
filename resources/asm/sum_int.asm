org 100h

.STACK
.DATA
    n1 db 0 ;variable numero 1
    n2 db 0 ;variable numero 2
    n3 db 0 ;resultado de la suma
    m1 db 10,13, 'INGRESA EL PRIMER NUMERO: $'
    m2 db 10,13, 'INGRESA EL SEGUNDO NUMERO: $'
    m3 DB 10,13, 'Resultado de la suma: $'

.CODE
    mov ax, @DATA
    mov ds, ax 

    ; Pedir el primer número
    mov ah, 9
    lea dx, m1
    int 21h
    mov ah, 1    ; Leer tecla pulsada
    int 21h
    sub al, 30h  ; Convertir de ASCII a valor numérico
    mov n1, al

    ; Pedir el segundo número
    mov ah, 9
    lea dx, m2
    int 21h
    mov ah, 1
    int 21h
    sub al, 30h
    mov n2, al

    ; Sumar
    mov al, n1
    add al, n2
    add al, 30h  ; Convertir de valor numérico a ASCII
    mov n3, al

    ; Mostrar resultado
    mov ah, 9
    lea dx, m3
    int 21h
    mov ah, 2    ; Interrupción para mostrar el resultado
    mov dl, n3
    int 21h

    ; Salir
    mov ah, 4ch
    int 21h

ret
