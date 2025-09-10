# STR COMPARISON

## Variable Declaration
- `.model small`: Establece que el programa utiliza un modelo de memoria pequeño, adecuado para programas con menos de 64 KB de código y datos.
- `.stack 64`: Reserva 64 bytes para la pila, que se utiliza en llamadas a subrutinas y manejo de interrupciones.
- `.data`: Marca el inicio de la sección de datos, donde se definen todas las variables y constantes del programa.
    - `cadena01 db 0ah,0dh, 'ingrese cadena 01: ', '$'`: Define una cadena que se mostrará al usuario para solicitar la entrada de la primera cadena de texto.
    - `cadena02 db 0ah,0dh, 'ingrese cadena 02: ', '$'`: Define una cadena similar para solicitar la segunda cadena de texto.
    - `cadenas_iguales db 0ah,0dh, 'IGUALES', '$'`: Almacena el mensaje que se mostrará si las cadenas comparadas son iguales.
    - `cadenas_diferentes db 0ah,0dh, 'DIFERENTES', '$'`: Almacena el mensaje para mostrar si las cadenas son diferentes.
    - `vcad01 db 100 dup(' '), '$'`: Reserva espacio para la primera cadena de texto ingresada por el usuario, inicializado con espacios.
    - `vcad02 db 100 dup(' '), '$'`: Reserva espacio para la segunda cadena de texto, también inicializado con espacios.

## Data Input
- `.code`: Inicia la sección de código del programa.
    - El programa inicia estableciendo el segmento de datos con las instrucciones `mov ax,@data` seguido de `mov ds,ax`.
    - Se muestra al usuario un mensaje para que ingrese la primera y luego la segunda cadena, utilizando la interrupción `int 21h` con el servicio `09h` para mostrar las cadenas `cadena01` y `cadena02`.
    - Para cada cadena, se lee carácter por carácter del teclado utilizando la interrupción `int 21h` con el servicio `01h`, almacenando cada carácter en los arrays `vcad01` y `vcad02` respectivamente, hasta que se detecta un retorno de carro (`0dh`).

## String Comparison
- La comparación de las cadenas se realiza cargando primero el contador `cx` con el número máximo de caracteres a comparar.
- Se utilizan los registros `si` y `di` para apuntar a los inicios de `vcad01` y `vcad02`.
- La instrucción `repe cmpsb` compara los bytes de las dos cadenas incrementando `si` y `di` después de cada comparación, deteniéndose si encuentra una diferencia o después de `cx` comparaciones.
- Si las cadenas son iguales (`je iguales`), se salta a la etiqueta `iguales`; si no (`jne diferente`), se procede a la etiqueta `diferente`.

## Output
- **Iguales**: Si las cadenas son iguales, se muestra el mensaje `IGUALES` usando `int 21h` con el servicio `09h` y luego se termina el programa con `int 21h` servicio `4ch`.
- **Diferentes**: Si las cadenas son diferentes, se muestra el mensaje `DIFERENTES` y el programa se termina de la misma manera que en el caso anterior.



<!-- x=100 -->
...................................................................................................
<!-- x>100 -->
...................................................................................................
<!-- x<100 -->
...................................