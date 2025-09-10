; # Comparacion de cadenas de 100 bytes

; El Antuan
; Reza Campos Fernando Bryan
; Amairany Bernal 

.model small ; Establece el modelo de memoria peque�o. Usado para programas que requieren menos de 64KB para c�digo y datos.
.stack 64    ; Reserva 64 bytes para la pila, usada en llamadas a funciones y manejo de interrupciones.
.data        ; Inicia la secci�n de definici�n de datos.

; Define cadenas de texto para mostrar al usuario, incluyendo saltos de l�nea (0ah,0dh) y el fin de cadena ('$').
cadena01 db 0ah,0dh, 'ingrese cadena 01: ', '$'
cadena02 db 0ah,0dh, 'ingrese cadena 02: ', '$'
cadenas_iguales db 0ah,0dh, 'IGUALES', '$'
cadenas_diferentes db 0ah,0dh, 'DIFERENTES', '$'

; Define dos arrays de 100 bytes cada uno para almacenar las cadenas ingresadas por el usuario, inicializados con espacios.
vcad01 db 100 dup(' '), '$'  ; Reserva 100 bytes para vcad01, inicializados con espacios y terminados con '$'.
vcad02 db 100 dup(' '), '$'   ; Reserva 100 bytes para vcad02, inicializados con espacios y terminados con '$'.
  
.code        ; Inicia la secci�n de c�digo.
inicio:      ; Etiqueta que marca el inicio del programa.
  mov ax,@data ; Carga la direcci�n del segmento de datos en AX.
  mov ds,ax    ; Mueve el valor de AX al registro de segmento de datos DS.

; Imprime la cadena 'ingrese cadena 01: '.
  mov ah,09   ; Establece la funci�n del sistema DOS para imprimir cadena en pantalla.
  mov dx,offset cadena01 ; Carga la direcci�n de memoria de cadena01 en DX.
  int 21h     ; Invoca la interrupci�n 21h para imprimir la cadena.

; Prepara para leer la primera cadena del usuario.
  lea si,vcad01 ; Carga la direcci�n de inicio de vcad01 en SI.
pedir1:
  mov ah,01h   ; Establece la funci�n del sistema DOS para leer un car�cter del teclado.
  int 21h      ; Lee un car�cter y lo almacena en AL.
  mov [si],al  ; Almacena el car�cter le�do en la posici�n actual de vcad01.
  inc si       ; Incrementa SI para apuntar al siguiente byte.
  cmp al,0dh   ; Compara el car�cter le�do con el retorno de carro.
  ja pedir1    ; Si el car�cter es mayor que el retorno de carro, repite.
  jb pedir1    ; Si el car�cter es menor, tambi�n repite.

; Repite el proceso anterior para la segunda cadena.
  mov ax,@data
  mov ds,ax
  mov ah,09
  mov dx,offset cadena02  
  int 21h
  lea si,vcad02  

pedir2:    
  mov ah,01h
  int 21h
  mov [si],al
  inc si
  cmp al,0dh
  ja pedir2
  jb pedir2
  
; Prepara para comparar las cadenas.
  mov cx,100   ; Establece el contador CX en 100 (el c�digo original dice 100, pero aqu� es 100 por error o modificaci�n).
  mov AX,DS    ; Carga el valor de DS en AX.
  mov ES,AX    ; Mueve el valor de DS a ES para la comparaci�n de segmentos.

; Comienza la comparaci�n de las cadenas byte por byte.
compara: 
  lea si,vcad01 ; Carga la direcci�n de vcad01 en SI.
  lea di,vcad02 ; Carga la direcci�n de vcad02 en DI.
  repe cmpsb    ; Compara byte a byte hasta que encuentre una diferencia o complete CX bytes.
  Jne diferente; Salta a la etiqueta 'diferente' si encuentra una diferencia.
  je iguales   ; Si no hay diferencias, salta a 'iguales'.

; Si las cadenas son iguales, imprime 'IGUALES' y termina el programa.
iguales:
   mov ax,@data
  mov ds,ax
  mov ah,09
  mov dx,offset cadenas_iguales
  int 21h
  mov ah,4ch   ; Establece la funci�n del sistema DOS para terminar el programa.
  int 21h      ; Termina el programa.

; Si las cadenas son diferentes, imprime 'DIFERENTES' y termina el programa.
diferente:
  mov ax,@data
  mov ds,ax
  mov ah,09
  mov dx,offset cadenas_diferentes
  int 21h
  mov ah,4ch   ; Establece la funci�n del sistema DOS para terminar el programa.
  int 21h      ; Termina el programa.
end inicio    ; Indica el fin del bloque de inicio.
