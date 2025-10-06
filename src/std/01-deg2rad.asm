; =============================================================================
;   std/01-deg2rad.asm
;   Converts degrees to radians using the standard library.
;   Usage: run-asm std/01-deg2rad.asm [degrees]
;   Receives degrees as command line parameter and converts to radians.
; =============================================================================

; --- Include our standard library ---
%include "src/lib/macros.inc"
%include "src/lib/io.inc"

; --- Data section for messages ---
section .data
    msg_input      db 'Converting degrees to radians:', 0
    msg_usage      db 13, 10, 'Usage: deg2rad [degrees]', 0
    msg_degrees    db 13, 10, 'Degrees: ', 0
    msg_radians    db 13, 10, 'Radians: ', 0
    msg_punto      db '.', 0
    newline        db 13, 10, 0
    input_degrees  dw 0
    radians_fixed  dw 0

section .text

program_begin
    ; Print header message
    mov si, msg_input
    call PrintString

    ; Extract parameter from command line using DOS PSP
    ; Command line at offset 81h in PSP, length at 80h
    mov cl, [0x80]         ; Get length of command line
    cmp cl, 1              ; Check if we have parameters (at least 1 char)
    jl .show_usage          ; If not, show usage

    mov si, 0x81           ; Point to the command line string
    call ParseNumberFromCommandLine
    mov [word input_degrees], ax

    ; Print "Degrees: " message
    mov si, msg_degrees
    call PrintString
    
    ; Print the input degrees
    mov ax, [word input_degrees]
    call PrintU16

    ; Print "Radians: " message
    mov si, msg_radians
    call PrintString

    ; Perform the conversion: radians = degrees * PI / 180
    ; Using fixed point arithmetic with factor of 1000 for precision (simpler than 10000)
    mov ax, [word input_degrees]  ; Load degrees
    mov bx, 31416                 ; PI * 10000 (approximation)
    mul bx                        ; AX = degrees * PI * 10000, DX gets overflow
    
    ; Now divide by 180
    mov bx, 180                   ; Divide by 180
    div bx                        ; AX = (degrees * PI * 10000) / 180
    
    ; Store the result 
    mov [word radians_fixed], ax
    
    ; Print the result as a fixed point number
    call PrintFixedPoint
    
    ; Print newline and exit
    mov si, newline
    call PrintString
    jmp .exit_program

.show_usage:
    mov si, msg_usage
    call PrintString

.exit_program:
    ; Print newline before exit
    mov si, newline
    call PrintString

program_end

; --- Subroutine to parse number from DOS command line ---
; Input: SI = pointer to command line string (after length at 80h)
; Output: AX = parsed number
ParseNumberFromCommandLine:
    push bx
    push cx
    push dx
    push si

    ; Skip leading spaces
.skip_spaces:
    mov al, [si]
    cmp al, ' '
    je .skip_space
    cmp al, 9       ; Tab character
    je .skip_space
    cmp al, 13      ; Carriage return
    je .parse_done_zero
    cmp al, 10      ; Line feed
    je .parse_done_zero
    jmp .parse_digits  ; Found non-space character, start parsing
    
.skip_space:
    inc si
    jmp .skip_spaces

.parse_digits:
    xor ax, ax      ; Result will be in AX
    xor bx, bx      ; Temporary register for digit conversion
    
.parse_loop:
    mov bl, [si]
    cmp bl, 0       ; Check for null terminator (not in PSP command line)
    je .parse_done
    cmp bl, ' '     ; Check for space (end of parameter)
    je .parse_done
    cmp bl, 9       ; Check for tab
    je .parse_done
    cmp bl, 13      ; Check for carriage return (end of line)
    je .parse_done
    cmp bl, 10      ; Check for line feed
    je .parse_done
    
    ; Convert ASCII digit to value
    sub bl, '0'
    jc .parse_done    ; If carry flag set, not a digit
    
    ; Check if digit is valid (0-9)
    cmp bl, 9
    ja .parse_done    ; If greater than 9, not a digit
    
    ; Multiply result by 10 and add current digit
    push ax
    mov ax, 10
    mul bx
    pop bx
    add ax, bx
    
    inc si
    jmp .parse_loop
    
.parse_done:
    pop si
    pop dx
    pop cx
    pop bx
    ret

.parse_done_zero:
    xor ax, ax
    pop si
    pop dx
    pop cx
    pop bx
    ret

; --- Subroutine to print fixed point number ---
; Input: AX = fixed point value (scaled by 10000)
PrintFixedPoint:
    push ax
    push bx
    push cx
    push dx
    
    ; Divide by 10000 to get integer part (for a value scaled by 10000)
    mov bx, 10000
    div bx            ; AX = integer part, DX = fractional part
    
    ; Print integer part
    call PrintU16
    
    ; Print decimal point
    mov si, msg_punto
    call PrintString
    
    ; Print fractional part
    mov ax, dx        ; AX now has the remainder (fractional part)
    cmp ax, 0
    je .frac_done
    
    ; Print the fractional part with leading zeros if needed
    cmp ax, 1000
    jb .print_frac_4
    call PrintU16
    jmp .frac_done

.print_frac_4:
    cmp ax, 100
    jb .print_frac_3
    mov ah, 0x0E
    mov al, '0'        ; Print leading zero
    int 0x10
    call PrintU16
    jmp .frac_done

.print_frac_3:
    cmp ax, 10
    jb .print_frac_2
    mov ah, 0x0E
    mov al, '0'        ; Print leading zero
    int 0x10
    mov ah, 0x0E
    mov al, '0'        ; Print another leading zero
    int 0x10
    call PrintU16
    jmp .frac_done

.print_frac_2:
    cmp ax, 1
    jb .frac_done
    mov ah, 0x0E
    mov al, '0'        ; Print leading zero
    int 0x10
    mov ah, 0x0E
    mov al, '0'        ; Print another leading zero
    int 0x10
    mov ah, 0x0E
    mov al, '0'        ; Print another leading zero
    int 0x10
    call PrintU16

.frac_done:
    pop dx
    pop cx
    pop bx
    pop ax
    ret