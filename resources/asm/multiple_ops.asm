org 100h

.STACK
.DATA
    n1 db 0 ;variable numero 1
    n2 db 0 ;variable numero 2
    n3 db 0 ;variable numero 3
    m1 db 10,13, 'INGRESA EL PRIMER NUMERO: $'
    m2 db 10,13, 'INGRESA EL SEGUNDO NUMERO: $'
    m3 DB 10,13, 'Resultado de la suma: $'
    m4 DB 10,13, 'Resultado de la resta: $'
    m5 DB 10,13, 'Resultado de la multiplicacion: $'
    m6 DB 10,13, 'Resultado de la division: $'
    
    
.CODE           
    mov ax, @DATA
    mov ds, ax 
    
    mov ah, 9
    lea dx, m1
    int 21h
    mov ah, 1    ;Interrupcion
    int 21h
    sub al,30h 
    mov n1, al
    
    mov ah, 9
    lea dx, m2
    int 21h
    mov ah, 1
    int 21h
    sub al,30h 
    mov n2, al
    
    ; Suma
    mov al, n1
    add al, n2
    add al, 30h
    mov n3, al
    
    mov ah, 9
    lea dx, m3
    int 21h
    mov ah, 2    ;Interrupción que exhibe el resultado
    mov dl, n3
    int 21h
    
    ; Resta
    mov al, n1
    sub al, n2
    add al, 30h
    mov n3, al
    
    mov ah, 9
    lea dx, m4
    int 21h
    mov ah, 2    ;Interrupción que exhibe el resultado
    mov dl, n3
    int 21h
    
    ; Multiplicación
    mov al, n1
    mul n2
    add al, 30h
    mov n3, al
    
    mov ah, 9
    lea dx, m5
    int 21h
    mov ah, 2    ;Interrupción que exhibe el resultado
    mov dl, n3
    int 21h
    
    ; División
    mov al, n1
    xor ah, ah    ; Limpiando el registro AH
    div n2        ; AL = AL / n2, AH = AL % n2
    add al, 30h   ; Convirtiendo el resultado a ASCII
    mov n3, al    ; Guardando el resultado
    
    mov ah, 9
    lea dx, m6
    int 21h
    mov ah, 2    ;Interrupción que exhibe el resultado
    mov dl, n3
    int 21h
    
    mov ah, 4ch 
    int 21h 
        
ret