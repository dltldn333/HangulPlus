# 한글+ 컴파일러

한글+ 프로그래밍 언어를 x86-64 어셈블리어로 컴파일하는 시스템입니다.

## 요구사항

- **macOS** (Intel Mac)
- **Python 3**
- **NASM** (Netwide Assembler)
- **Xcode Command Line Tools** (링커용)

## 설치

### 1. NASM 설치

```bash
# Homebrew 사용
brew install nasm

# 또는 공식 사이트에서 다운로드
# https://www.nasm.us/
```

### 2. Xcode Command Line Tools 설치

```bash
xcode-select --install
```

## 사용법

### 기본 컴파일 및 실행

```bash
python3 한글플러스.py 파일명.코드
```

### 단계별 컴파일 과정

#### 1. 한글 코드 → 어셈블리어 변환

```bash
python3 한글p.py 입력.코드 > 출력.asm
```

#### 2. 어셈블리어 → 오브젝트 파일

```bash
nasm -f macho64 출력.asm -o 출력.o
```

#### 3. 오브젝트 파일 → 실행 파일

```bash
ld -o 출력 실행파일명 출력.o -lSystem -syslibroot $(xcrun --sdk macosx --show-sdk-path) -e _start -platform_version macos 11.0.0 13.0.0
```

## 컴파일 과정 자동화

`한글플러스.py` 스크립트가 전체 과정을 자동화합니다:

1. **변환**: `.코드` → `.asm` (한글p.py)
2. **어셈블**: `.asm` → `.o` (NASM)
3. **링킹**: `.o` → 실행 파일 (ld)
4. **실행**: 생성된 실행 파일 실행

## 예제

### 입력 파일 (example.코드)

```한글
정수 값 는(은) 3;
값 를(을) 값 + 2;
출력(값);
출력("안녕하세요!");
```

### 실행

```bash
python3 한글플러스.py example.코드
```

### 출력

```
[1] 한글은 세종대왕님이 만드셨습니다🤩 (컴파일): example.코드 → example.asm
[2] 파이썬은 귀도 반 로섬이 만들었습니다🖥️ (어셈블): example.asm → example.o
[3] 폰 노이만은 신이야🤯 (링킹): example.o → example
[4] 실행 중: ./example
------------------------------
5
안녕하세요!
```

## 파일 설명

- **한글p.py**: 한글 코드를 x86-64 어셈블리어로 변환하는 파서
- **한글플러스.py**: 전체 컴파일 과정을 자동화하는 스크립트
- **입력.코드**: 예제 코드 파일
- **어셈블리어 연습.txt**: 학습 자료

## 문제 해결

### 정수 출력 문제

정수형 변수를 출력할 때 바이너리 형태로 출력되는 문제를 해결하기 위해, 어셈블리 수준에서 문자열로 변환하여 명시적으로 출력하는 로직을 추가했습니다.

### macOS SDK 오류

```bash
# SDK 경로 확인
xcrun --sdk macosx --show-sdk-path
```

### 권한 문제

```bash
# 실행 파일에 실행 권한 부여
chmod +x 실행파일명
```
