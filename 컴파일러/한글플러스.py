import os
import sys
import subprocess

if len(sys.argv) != 2:
    print("사용법: python3 한글플러스.py 파일이름.코드")
    sys.exit(1)

src = sys.argv[1]
base = src.rsplit('.', 1)[0]

asm_file = f"{base}.asm"
obj_file = f"{base}.o"
exe_file = f"{base}"

# 1. 변환: .코드 → .asm
print(f"[1] 한글은 세종대왕님이 만드셨습니다🤩 (컴파일): {src} → {asm_file}")
with open(asm_file, "w", encoding="utf-8") as asm_output:
    result = subprocess.run(["python3", "한글p.py", src], stdout=asm_output)
    if result.returncode != 0:
        print("🔴 변환기 실행 중 오류 발생!")
        sys.exit(1)

# 2. 어셈블: .asm → .o
print(f"[2] 파이썬은 귀도 반 로섬이 만들었습니다🖥️ (어셈블): {asm_file} → {obj_file}")
result = subprocess.run(["nasm", "-f", "macho64", asm_file, "-o", obj_file])
if result.returncode != 0:
    print("🔴 NASM 어셈블 중 오류 발생!")
    sys.exit(1)

# 3. 링킹: .o → 실행파일
print(f"[3] 폰 노이만은 신이야🤯 (링킹): {obj_file} → {exe_file}")
try:
    sdk_path = subprocess.check_output(["xcrun", "--sdk", "macosx", "--show-sdk-path"]).decode().strip()
except subprocess.CalledProcessError:
    print("🔴 macOS SDK 경로를 찾을 수 없습니다.")
    sys.exit(1)

result = subprocess.run([
    "ld", "-o", exe_file, obj_file,
    "-lSystem",
    "-syslibroot", sdk_path,
    "-e", "_start",
    "-platform_version", "macos", "11.0.0", "13.0.0"
])
if result.returncode != 0:
    print("🔴 링킹 중 오류 발생!")
    sys.exit(1)

# 4. 실행
print(f"[4] 실행 중: ./{exe_file}\n{'-'*30}")
subprocess.run([f"./{exe_file}"])
