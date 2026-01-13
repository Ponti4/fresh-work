---
name: bash-terminal-guide
description: gpters 20기 프리랜서를 위한 Terminal/Bash 기초 완전 초보자 가이드
context: none
agent: none
hooks: none
allowed-tools: none
---

# Terminal/Bash 기초 가이드

> **gpters 20기 프리랜서를 위한 완전 초보자 가이드**

Git, Python, 그리고 모든 프로그래밍 작업은 Terminal(터미널)이라는 도구에서 시작합니다. 이 가이드는 **Terminal을 처음 접하는 분**도 따라할 수 있도록 작성되었습니다.

---

## 📋 목차

1. [Terminal/Bash란?](#terminalbash란) ← **여기부터 시작!**
2. [OS별 Terminal 열기](#os별-terminal-열기)
3. [Step 0: Terminal 기본 구조](#step-0-terminal-기본-구조)
4. [Step 1: 경로 이해하기 (pwd, ls)](#step-1-경로-이해하기-pwd-ls)
5. [Step 2: 폴더 이동 (cd)](#step-2-폴더-이동-cd)
6. [Step 3: 파일/폴더 생성 (mkdir, touch)](#step-3-파일폴더-생성-mkdir-touch)
7. [Step 4: 파일 관리 (cp, mv, rm)](#step-4-파일-관리-cp-mv-rm)
8. [Step 5: 파일 내용 보기 (cat)](#step-5-파일-내용-보기-cat)
9. [Step 6: 경로와 명령어 팁](#step-6-경로와-명령어-팁)
10. [주의사항 & FAQ](#주의사항--faq)
11. [명령어 빠른 참조](#명령어-빠른-참조)

**총 소요 시간: 20-30분**

---

## Terminal/Bash란?

### 🤔 쉽게 설명하면

**Terminal = 컴퓨터와 대화하는 도구 (마우스 대신 텍스트로 명령어 입력)**

#### GUI vs CLI

```
GUI (Graphical User Interface)     CLI (Command Line Interface)
├── 마우스로 클릭                 ├── 텍스트로 명령어 입력
├── 시각적, 직관적                ├── 텍스트 기반, 강력함
├── 느림                          ├── 빠름
└── 초보자 친화적                 └── 강력한 기능 가능

예: 폴더 만들기
GUI: 우클릭 → New Folder → 이름 입력
CLI: mkdir my_folder
```

### 📌 Terminal의 역할

| 역할 | 설명 |
|------|------|
| **파일/폴더 관리** | 파일 생성, 삭제, 이동, 복사 |
| **프로그램 실행** | Python, Git 같은 프로그램 실행 |
| **텍스트 파일 편집** | 코드, 설정 파일 수정 |
| **시스템 명령** | 권한 변경, 프로세스 관리 등 |

### 🔄 Terminal과 Bash의 관계

```
Terminal = 프로그램 (창을 열고 입력받는 것)
Bash     = 언어 (Terminal 안에서 실행되는 명령어)
```

**비유:**
- Terminal = 채팅 앱 (Messenger)
- Bash = 한국어 (언어)

→ 대부분의 초보자는 "Terminal"과 "Bash"를 같은 의미로 사용해도 됩니다.

---

## OS별 Terminal 열기

### 🪟 Windows 사용자

#### 방법 1: PowerShell (권장)

1. Windows 시작 버튼 클릭
2. "powershell" 입력
3. **Windows PowerShell** 클릭

#### 방법 2: Command Prompt (CMD)

1. Windows 시작 버튼 클릭
2. "cmd" 입력
3. **명령 프롬프트** 클릭

#### 방법 3: Git Bash (Git 설치 후)

1. 폴더에서 우클릭
2. **Open Git Bash here** 클릭

→ PowerShell 또는 Git Bash 권장

---

### 🍎 Mac 사용자

1. **Spotlight 검색** 열기 (⌘ + Space)
2. "terminal" 입력
3. **Terminal.app** 클릭

또는:
- Finder → Applications → Utilities → Terminal

---

### 🐧 Linux 사용자

일반적으로 기본으로 설치되어 있습니다.

1. Ctrl + Alt + T (Ubuntu)
2. 또는 애플리케이션 메뉴에서 "Terminal" 검색

---

## Step 0: Terminal 기본 구조

Terminal을 열면 다음과 같은 화면이 나타납니다:

```
user@MacBook-Pro ~ %
```

또는 Windows (PowerShell):

```
PS C:\Users\YourName>
```

### 🔍 각 부분의 의미

#### Mac/Linux

```
user          @  MacBook-Pro  ~      %
│             │   │           │      │
현재 사용자   구분 컴퓨터 이름  현재 위치 프롬프트
```

#### Windows (PowerShell)

```
PS  C:\Users\YourName>
│   │
│   현재 경로
PowerShell 표시

(Git Bash의 경우: user@DESKTOP ~ $)
```

### 📍 프롬프트 (Prompt)

- `%` (Mac/Linux)
- `$` (Mac/Linux, Git Bash)
- `>` (PowerShell)

→ 명령어를 입력할 수 있다는 의미

---

## Step 1: 경로 이해하기 (pwd, ls)

### 🗺️ 파일 시스템의 구조

컴퓨터의 파일/폴더는 나무 구조처럼 되어 있습니다:

```
/ (루트, 최상위)
├── Users (또는 home)
│   ├── YourName
│   │   ├── Desktop
│   │   ├── Documents
│   │   ├── Projects
│   │   │   ├── gpters-20th-templates
│   │   │   │   ├── src
│   │   │   │   ├── docs
│   │   │   │   └── scripts
│   │   └── Downloads
│   └── OtherUser
└── Applications
```

Terminal에서는 **현재 어느 폴더에 있는지** 항상 알아야 합니다.

---

### 📍 pwd: 현재 위치 확인

```bash
pwd
```

**출력 예시:**

```
/Users/YourName/Projects
```

→ "지금 나는 `/Users/YourName/Projects` 폴더에 있다"는 의미

#### Windows (PowerShell)

```bash
pwd
```

또는

```bash
echo $PWD
```

---

### 📂 ls: 현재 폴더 내용 보기

```bash
ls
```

**출력 예시:**

```
Desktop
Documents
Downloads
Projects
```

→ 현재 폴더에 있는 파일과 폴더 목록

#### 자세히 보기

```bash
ls -la
```

또는 더 읽기 쉽게:

```bash
ls -lh
```

**출력 예시:**

```
drwxr-xr-x   5 user  staff     160 Dec 26 10:30 Desktop
drwxr-xr-x   3 user  staff      96 Dec 20 14:22 Documents
drwxr-xr-x   8 user  staff     256 Dec 24 18:45 Projects
-rw-r--r--   1 user  staff    1024 Dec 25 09:15 README.md
```

**의미:**
- `d`: 폴더 (directory)
- `-`: 파일 (file)
- 날짜/시간: 생성 또는 수정 시간

#### Windows (PowerShell)

```bash
dir
```

또는

```bash
ls
```

---

### 🎯 pwd + ls 조합

```bash
# 현재 위치 확인
pwd

# 현재 폴더의 파일 목록
ls

# 현재 위치를 출력하면서 목록도 보기
ls -la
```

---

## Step 2: 폴더 이동 (cd)

### 📍 cd: 폴더로 이동

Terminal에서는 폴더를 "이동"할 수 없습니다 (마우스로 더블클릭처럼).

대신 **"현재 위치를 변경"**합니다.

```bash
cd 폴더_경로
```

### 🎯 절대경로로 이동 (전체 주소)

```bash
# Mac/Linux
cd /Users/YourName/Projects

# Windows
cd C:\Users\YourName\Projects
```

---

### 🎯 상대경로로 이동 (현재 위치에서 상대적으로)

#### 예시: 현재 위치가 `/Users/YourName`

```
/Users/YourName
├── Desktop
├── Documents
├── Projects
│   └── gpters-20th-templates
```

**Desktop으로 이동:**

```bash
cd Desktop
```

**Projects 내의 gpters-20th-templates로 이동:**

```bash
cd Projects/gpters-20th-templates
```

---

### 🔄 특수 경로

| 경로 | 의미 | 예시 |
|------|------|------|
| `.` | 현재 폴더 | `cd .` (현재 위치 유지) |
| `..` | 부모 폴더 (위로) | `cd ..` (한 단계 위로) |
| `~` | 홈 폴더 | `cd ~` (홈으로 이동) |
| `/` | 루트 | `cd /` (최상위로) |

**예시:**

```bash
# 현재: /Users/YourName/Projects/gpters-20th-templates/docs

# 한 단계 위로
cd ..
# → /Users/YourName/Projects/gpters-20th-templates

# 두 단계 위로
cd ../..
# → /Users/YourName/Projects

# 홈 폴더로 이동
cd ~
# → /Users/YourName

# 다시 gpters로
cd Projects/gpters-20th-templates
```

---

### 📝 실습: 프로젝트 폴더로 이동

```bash
# 1. 현재 위치 확인
pwd

# 2. 홈 폴더로 이동
cd ~

# 3. Projects 폴더로 이동
cd Projects

# 4. gpters-20th-templates로 이동
cd gpters-20th-templates

# 5. 파일 목록 확인
ls

# 6. docs 폴더 이동
cd docs

# 7. 현재 위치 확인
pwd
```

---

## Step 3: 파일/폴더 생성 (mkdir, touch)

### 📁 mkdir: 폴더 생성

```bash
mkdir 폴더_이름
```

**예시:**

```bash
# 하나의 폴더 생성
mkdir my_project

# 여러 폴더 생성
mkdir folder1 folder2 folder3

# 중첩된 폴더 생성
mkdir -p path/to/deep/folder
```

**확인:**

```bash
ls
```

---

### 📄 touch: 파일 생성

```bash
touch 파일_이름
```

**예시:**

```bash
# 빈 파일 생성
touch hello.py

# 여러 파일 생성
touch file1.txt file2.txt file3.txt
```

**확인:**

```bash
ls
```

---

### 🎯 실습

```bash
# 1. 프로젝트 폴더 생성
mkdir my_skill_project

# 2. 폴더로 이동
cd my_skill_project

# 3. 필요한 폴더 생성
mkdir -p src/components
mkdir -p tests
mkdir docs

# 4. 초기 파일 생성
touch README.md
touch main.py
touch .gitignore

# 5. 폴더 구조 확인
ls -la
```

---

## Step 4: 파일 관리 (cp, mv, rm)

### 📋 cp: 파일/폴더 복사

```bash
cp 원본_파일 복사본_이름
```

**예시:**

```bash
# 파일 복사
cp hello.py hello_backup.py

# 폴더 복사 (폴더 안의 모든 파일 포함)
cp -r my_folder my_folder_backup
```

---

### ➡️ mv: 파일/폴더 이동 또는 이름 변경

```bash
mv 현재_이름 새로운_이름
```

**이동:**

```bash
# 파일을 다른 폴더로 이동
mv hello.py src/

# 파일을 다른 폴더로 이동하면서 이름 변경
mv hello.py src/hello_v2.py
```

**이름 변경:**

```bash
# 파일 이름 변경
mv old_name.py new_name.py

# 폴더 이름 변경
mv old_folder new_folder
```

---

### 🗑️ rm: 파일/폴더 삭제

⚠️ **경고**: `rm`은 **영구 삭제**입니다! (휴지통에 안 들어감)

```bash
rm 파일_이름
```

**예시:**

```bash
# 파일 삭제
rm hello.py

# 폴더 삭제 (폴더 안의 모든 파일 포함)
rm -r my_folder

# 확인 메시지 보이고 삭제 (안전)
rm -i file.txt

# 여러 파일 삭제
rm file1.py file2.py file3.py
```

---

### 🎯 실습

```bash
# 1. 파일 생성
touch test.txt

# 2. 파일 복사
cp test.txt test_backup.txt

# 3. 이름 변경
mv test.txt original.txt

# 4. 폴더 생성
mkdir archive

# 5. 파일을 폴더로 이동
mv original.txt archive/

# 6. 백업 파일 삭제
rm test_backup.txt

# 7. 폴더 구조 확인
ls -la
ls -la archive/
```

---

## Step 5: 파일 내용 보기 (cat)

### 📖 cat: 파일 내용 출력

```bash
cat 파일_이름
```

**예시:**

```bash
# Python 파일 내용 보기
cat hello.py

# 텍스트 파일 보기
cat README.md

# 설정 파일 보기
cat .env.example
```

**출력 예시:**

```
print("Hello, World!")
print("This is my first Python file")
```

---

### 📝 여러 파일 동시에 보기

```bash
# 여러 파일 연달아 보기
cat file1.txt file2.txt

# 합쳐서 새 파일로 저장
cat file1.txt file2.txt > combined.txt
```

---

### 🎯 실습

```bash
# 1. 파이썬 파일 생성 (에디터로)
# (아직 배우지 않음, 건너뛰기)

# 2. 기존 파일 내용 보기
cat README.md

# 3. 설정 파일 보기
cat .gitignore
```

---

## Step 6: 경로와 명령어 팁

### 💡 유용한 팁들

#### Tab 자동완성

폴더나 파일 이름을 완전히 입력하지 않고 **Tab 키**를 누르면 자동완성됩니다.

```bash
# 입력:
cd Proj

# Tab 누르면:
cd Projects/

# 다시 입력:
cd Projects/gpt

# Tab 누르면:
cd Projects/gpters-20th-templates/
```

---

#### 화살표 키로 명령어 히스토리

```bash
# 이전 명령어 보기: ↑
# 다음 명령어 보기: ↓
```

---

#### Ctrl+A, Ctrl+E (라인 이동)

```bash
# Ctrl+A: 라인 시작으로 이동
# Ctrl+E: 라인 끝으로 이동
# Ctrl+U: 라인 처음부터 커서까지 삭제
# Ctrl+K: 커서부터 라인 끝까지 삭제
```

---

#### 와일드카드 (*)

```bash
# 모든 Python 파일 목록
ls *.py

# 모든 파일 삭제 (조심!)
rm *

# 모든 .txt 파일 복사
cp *.txt backup/
```

---

### 📍 절대경로 vs 상대경로

| 유형 | 형태 | 예시 | 장점 | 단점 |
|------|------|------|------|------|
| **절대경로** | `/`로 시작 | `/Users/YourName/Projects/gpters` | 어디서나 명확 | 길고 복잡 |
| **상대경로** | `.`, `..`로 시작 | `Projects/gpters` | 짧고 간단 | 현재 위치에 따라 다름 |

**추천:**
- 터미널에서는 **상대경로** (현재 위치 기준)
- 스크립트에서는 **절대경로** (어디서든 작동)

---

## 주의사항 & FAQ

### ⚠️ 중요한 주의사항

#### 1. **`rm` 명령어는 영구 삭제**

```bash
# ❌ 절대 하지 말 것
rm -r /   # 전체 시스템 삭제!

# ❌ 신중할 것
rm *.py   # 모든 Python 파일 삭제
rm -r *   # 현재 폴더의 모든 것 삭제

# ✅ 안전하게
rm file_name.py  # 특정 파일만
```

⚠️ **경고**: 삭제하면 **복구 불가능**합니다!

---

#### 2. **경로에 공백이 있으면 따옴표로 감싸기**

```bash
# ❌ 잘못된 예
cd My Project Folder    # 에러!

# ✅ 올바른 예
cd "My Project Folder"
cd 'My Project Folder'
```

---

#### 3. **명령어는 소문자 권장**

```bash
# ❌
CD my_folder
LS

# ✅
cd my_folder
ls
```

---

#### 4. **파일명에 특수문자 피하기**

```bash
# ❌ 피할 것
my file.py        # 공백
my-file@.py       # @, !, &, 등
my$(date).py      # $, 특수문자

# ✅ 좋은 예
my_file.py        # 언더스코어
my-file.py        # 하이픈
myfile.py         # 글자만
myFile.py         # camelCase
```

---

### 💡 자주 묻는 질문 (FAQ)

#### **Q1. 명령어를 입력해도 아무것도 안 보여요**

일부 명령어는 성공하면 아무 메시지도 안 보입니다.

```bash
# 예: mkdir (폴더 생성)
mkdir my_folder

# 아무것도 나오지 않으면 성공!
# 확인하려면:
ls
```

---

#### **Q2. "command not found" 에러가 나요**

프로그램이 설치되지 않았거나 경로가 잘못되었습니다.

```bash
# 예: Python이 설치되지 않음
python --version
# command not found: python

# 해결: python3 또는 전체 경로 사용
python3 --version
```

---

#### **Q3. 폴더 구조를 시각적으로 보고 싶어요**

```bash
# tree 명령어 (설치 필요)
tree

# 설치하지 않았으면:
ls -R     # 재귀적으로 보기
```

---

#### **Q4. 폴더 내용이 많아서 스크롤이 안 보여요**

```bash
# less 명령어 사용 (위/아래 화살표로 스크롤)
ls -la | less

# 또는 head/tail로 처음/끝만 보기
ls | head -10    # 처음 10개
ls | tail -10    # 마지막 10개
```

---

#### **Q5. 파일을 실행하려면?**

```bash
# Python 파일 실행
python hello.py      # Windows
python3 hello.py     # Mac/Linux

# 현재 폴더의 파일 실행
./script.sh          # Shell script
```

---

#### **Q6. 현재 폴더로 빠르게 돌아가려면?**

```bash
# 홈 폴더로
cd ~

# 최근 폴더로
cd -

# 한 단계 위로
cd ..
```

---

#### **Q7. 이전에 입력한 명령어를 다시 실행하려면?**

```bash
# 화살표 ↑ 누르기
# 또는 history 보기
history

# 또는 Ctrl+R로 검색
# Ctrl+R 후 명령어의 일부 입력
```

---

## 명령어 빠른 참조

### 경로 및 위치

```bash
# 현재 위치 확인
pwd

# 홈 폴더로 이동
cd ~

# 위로 한 단계 이동
cd ..

# 두 단계 위로 이동
cd ../..

# 절대경로로 이동
cd /Users/YourName/Projects

# 상대경로로 이동
cd Projects/my_folder
```

### 파일/폴더 목록

```bash
# 기본 목록
ls

# 자세한 목록
ls -la

# 읽기 쉬운 크기로 표시
ls -lh

# 숨김 파일 포함
ls -a

# 역순 정렬
ls -r

# 시간순 정렬
ls -t
```

### 파일/폴더 생성

```bash
# 폴더 생성
mkdir my_folder

# 중첩된 폴더 생성
mkdir -p path/to/folder

# 파일 생성
touch filename.txt

# 파일 내용 보기
cat filename.txt
```

### 파일/폴더 관리

```bash
# 파일 복사
cp original.txt copy.txt

# 폴더 복사
cp -r original_folder copy_folder

# 파일 이동/이름 변경
mv old_name.py new_name.py

# 파일 삭제
rm file.txt

# 폴더 삭제
rm -rf folder_name

# 파일 삭제 전 확인
rm -i file.txt
```

### 파일 검색 및 확인

```bash
# 파일명 검색
find . -name "filename.txt"

# 파일 내용 검색
grep "search_text" file.txt

# 파일 크기 확인
ls -lh filename

# 폴더 크기 확인
du -sh folder_name
```

### 유용한 조합

```bash
# 최신 파일부터 보기
ls -ltr

# Python 파일만 보기
ls *.py

# 폴더 내용을 파일로 저장
ls -la > file_list.txt

# 여러 파일 합치기
cat file1.txt file2.txt > combined.txt
```

---

## 🎯 완료 체크리스트

기본 스킬을 습득했는지 확인하세요:

- [ ] Terminal을 열 수 있다
- [ ] `pwd` 명령어로 현재 위치를 확인할 수 있다
- [ ] `ls` 명령어로 파일 목록을 볼 수 있다
- [ ] `cd` 명령어로 폴더를 이동할 수 있다
- [ ] `mkdir`으로 폴더를 생성할 수 있다
- [ ] `touch`로 파일을 생성할 수 있다
- [ ] `cp`로 파일을 복사할 수 있다
- [ ] `mv`로 파일을 이동/이름변경할 수 있다
- [ ] `rm`으로 파일을 삭제할 수 있다
- [ ] `cat`으로 파일 내용을 볼 수 있다
- [ ] Tab 자동완성을 사용할 수 있다

**모두 체크되었으면 준비 완료입니다!** 🎉

---

**작성일**: 2025-12-26
**대상**: gpters 20기 프리랜서, 비전공자, 초보자
**난이도**: 입문 (Beginner)
