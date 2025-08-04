section .data
buffer times 20 db 0
newline_len equ $ - newline
newline db 10
값 dq 3

section .text
global _start

_start:
    mov rax, qword [rel 값]
    add rax, 2
    mov qword [rel 값], rax
    ; 정수 출력 루틴 시작 for 값
    mov rax, qword [rel 값]
    lea rsi, [rel buffer + 19]
    mov rcx, 0
.print_loop_값:
    xor rdx, rdx
    mov rbx, 10
    div rbx
    add dl, '0'
    dec rsi
    mov [rsi], dl
    inc rcx
    test rax, rax
    jnz .print_loop_값
    mov rax, 0x2000004
    mov rdi, 1
    mov rdx, rcx
    syscall
    mov rax, 0x2000004
    mov rdi, 1
    lea rsi, [rel newline]
    mov rdx, newline_len
    syscall

    mov rax, 0x2000001
    xor rdi, rdi
    syscall
