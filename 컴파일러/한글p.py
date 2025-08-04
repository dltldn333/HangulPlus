import sys
import re

def compile_hancode(lines):
    data_section = ["section .data",
                    "buffer times 20 db 0",
                    "newline_len equ $ - newline",
                    "newline db 10"
    ]
    text_section = [
        "section .text",
        "global _start",
        "",
        "_start:"
    ]
    declared_vars = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 변수 선언: 정수 값 는(은) 3;
        match_decl = re.match(r"정수 ([\w가-힣]+) 는\(은\) (\d+);", line)
        if match_decl:
            var, val = match_decl.groups()
            declared_vars[var] = True
            data_section.append(f"{var} dq {val}")
            continue

        # 변수 대입: 값 를(을) 값 + 2;
        match_assign = re.match(r"([\w가-힣]+) 를\(을\) ([\w가-힣\d+\-*/ ]+);", line)
        if match_assign:
            var, expr = match_assign.groups()
            if var not in declared_vars:
                print(f"오류: 변수 '{var}'가 선언되지 않았습니다.")
                sys.exit(1)

            if '+' in expr:
                left, right = map(str.strip, expr.split('+'))
                text_section.append(f"    mov rax, qword [rel {left}]")
                text_section.append(f"    add rax, {right}")
                text_section.append(f"    mov qword [rel {var}], rax")
            elif '-' in expr:
                left, right = map(str.strip, expr.split('-'))
                text_section.append(f"    mov rax, qword [rel {left}]")
                text_section.append(f"    sub rax, {right}")
                text_section.append(f"    mov qword [rel {var}], rax")
            else:
                text_section.append(f"    mov rax, {expr}")
                text_section.append(f"    mov qword [rel {var}], rax")
            continue


        # 문자열 출력
        match_print_string = re.match(r'출력\("(.+)"\);', line)
        if match_print_string:
            string_val = match_print_string.group(1)
            label = f"__str_{len(data_section)}"
            data_section.append(f'{label} db "{string_val}", 10')  # 줄바꿈 포함
            data_section.append(f'{label}_len equ $ - {label}')
            text_section += [
                "    mov rax, 0x2000004",
                "    mov rdi, 1",
                f"    lea rsi, [rel {label}]",
                f"    mov rdx, {label}_len",
                "    syscall"
            ]
            continue


        # 숫자를 문자로 바꿔봅시다!!!
        match_print_number = re.match(r"출력\(([\w가-힣]+)\);", line)
        if match_print_number:
            var_name = match_print_number.group(1)
            text_section += [
                f"    ; 정수 출력 루틴 시작 for {var_name}",
                f"    mov rax, qword [rel {var_name}]",
                f"    lea rsi, [rel buffer + 19]",
                f"    mov rcx, 0",
                f".print_loop_{var_name}:",
                f"    xor rdx, rdx",
                f"    mov rbx, 10",
                f"    div rbx",
                f"    add dl, '0'",
                f"    dec rsi",
                f"    mov [rsi], dl",
                f"    inc rcx",
                f"    test rax, rax",
                f"    jnz .print_loop_{var_name}",
                f"    mov rax, 0x2000004",
                f"    mov rdi, 1",
                f"    mov rdx, rcx",
                f"    syscall",
                f"    mov rax, 0x2000004",
                f"    mov rdi, 1",
                f"    lea rsi, [rel newline]",
                f"    mov rdx, newline_len",
                f"    syscall"
            ]
            continue



        # 출력(변수);
        match_print = re.match(r"출력\(([\w가-힣]+)\);", line)
        if match_print:
            var = match_print.group(1)
            if var not in declared_vars:
                print(f"오류: 변수 '{var}'가 선언되지 않았습니다.")
                sys.exit(1)

            text_section += [
                "    mov rax, 0x2000004",  # write
                "    mov rdi, 1",          # stdout
                f"    lea rsi, [rel {var}]",  # 변수 주소
                "    mov rdx, 8",          # 출력 바이트 수
                "    syscall"
            ]
            continue

        print(f"알 수 없는 문장: {line}")
        sys.exit(1)

    text_section += [
        "",
        "    mov rax, 0x2000001",  # exit
        "    xor rdi, rdi",
        "    syscall"
    ]

    return "\n".join(data_section + [""] + text_section)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python3 한글p.py input.코드 > output.asm")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        lines = f.readlines()

    asm = compile_hancode(lines)
    print(asm)
