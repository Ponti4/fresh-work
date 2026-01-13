---
name: git-setup-and-usage
description: gpters 20기 프리랜서를 위한 Git 설치 및 사용 완전 초보자 가이드
context: none
agent: none
hooks: none
allowed-tools: none
---

# Git 설치 및 사용 가이드

> **gpters 20기 프리랜서를 위한 완전 초보자 가이드**

Week 2부터 본격적인 프로젝트 작업을 시작하려면 Git이 필요합니다. 이 가이드는 **Git을 처음 접하는 분**도 따라할 수 있도록 작성되었습니다.

---

## 📋 목차

1. [Git이란?](#git이란) ← **여기부터 시작!**
2. [Git vs GitHub](#git-vs-github)
3. [Step 0: Git 설치 여부 확인](#step-0-git-설치-여부-확인)
4. [Step 1: Git 설치](#step-1-git-설치)
5. [Step 2: 초기 설정](#step-2-초기-설정)
6. [Step 3: GitHub 계정 연결](#step-3-github-계정-연결)
7. [Step 4: 첫 번째 프로젝트 복제 (Clone)](#step-4-첫-번째-프로젝트-복제-clone)
8. [Step 5: 기본 워크플로우](#step-5-기본-워크플로우)
9. [주의사항 & FAQ](#주의사항--faq)
10. [명령어 빠른 참조](#명령어-빠른-참조)

**총 소요 시간: 20-30분**

---

## Git이란?

### 🤔 쉽게 설명하면

**Git = 코드 변경 기록을 남기는 도구**

예를 들어 Word 문서로 생각해봅시다:

```
문서.docx
├── 원본 (2025-12-01)
├── 수정 v1 (2025-12-05)
├── 수정 v2 (2025-12-10)
├── 수정 v3 (2025-12-15)
└── 최종본 (2025-12-20)
```

이렇게 여러 버전을 관리하지 않아도 Git이 자동으로 모든 변경을 기록합니다!

### 📌 Git의 역할

| 역할 | 설명 |
|------|------|
| **변경 기록 저장** | 누가, 언제, 무엇을 바꿨는지 기록 |
| **이전 버전으로 복구** | 실수한 부분을 예전 상태로 되돌리기 |
| **협업 관리** | 여러 사람이 같은 프로젝트에서 작업할 때 충돌 방지 |
| **코드 안전 보관** | 컴퓨터가 망가져도 클라우드에 백업됨 |

### 🔄 Git의 기본 개념

```
작업 디렉토리 (파일 수정)
    ↓
Staging Area (변경사항 준비)
    ↓
Repository (변경사항 저장)
    ↓
원격 저장소 (클라우드에 업로드)
```

**쉽게 말하면:**
1. 파일을 수정한다
2. "이 변경사항을 저장할 거야"라고 표시한다 (add)
3. 변경사항에 설명을 붙여서 저장한다 (commit)
4. 클라우드에 업로드한다 (push)

---

## Git vs GitHub

초보자가 가장 많이 헷갈리는 부분입니다!

### 🔍 차이점

| 항목 | Git | GitHub |
|------|-----|--------|
| **정의** | 버전 관리 소프트웨어 | 인터넷 서비스 (Git을 사용) |
| **설치** | 컴퓨터에 설치 필요 | 웹에서 사용 (설치 X) |
| **역할** | 로컬에서 변경사항 관리 | 원격에 코드 백업 & 공유 |
| **비유** | 가정용 노트북 | 클라우드 (구글 드라이브 같은 것) |

### 🎯 관계도

```
당신의 컴퓨터                GitHub (인터넷)
┌─────────────┐            ┌─────────────┐
│   Git       │   push →   │   GitHub    │
│  (로컬)     │   ← pull   │   (원격)    │
└─────────────┘            └─────────────┘
```

**정리:**
- Git을 **설치**하면 → 로컬 컴퓨터에서 버전 관리 가능
- GitHub **계정**을 만들면 → 인터넷에 코드 보관 가능
- 둘을 연결하면 → 완벽한 협업 환경 구성!

---

## Step 0: Git 설치 여부 확인

### Windows 사용자

1. **명령 프롬프트 (CMD)** 또는 **Git Bash** 열기
2. 다음 명령어 입력:

```bash
git --version
```

### Mac 사용자

1. **터미널** 열기 (⌘ + Space → "터미널" 검색)
2. 다음 명령어 입력:

```bash
git --version
```

---

### 🔍 결과 판단

#### ✅ Case 1: 버전이 나온 경우

```
git version 2.43.0
```

→ **이미 설치되어 있습니다!** [Step 2: 초기 설정](#step-2-초기-설정)으로 이동하세요.

#### ❌ Case 2: "command not found" 또는 에러가 나온 경우

```
'git' is not recognized as an internal or external command
```

→ **Git이 설치되어 있지 않습니다.** [Step 1: Git 설치](#step-1-git-설치)로 이동하세요.

---

## Step 1: Git 설치

### 📥 Windows 사용자

#### 다운로드

[Git for Windows 공식 사이트](https://git-scm.com/download/win)에서 최신 버전 다운로드

또는 직접 링크:
- **64비트**: [Git-2.43.0-64-bit.exe](https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe)

#### 설치 방법

1. 다운로드한 `.exe` 파일 실행
2. 설치 마법사가 나타남 (기본 설정 유지 권장)
   - "Next" 클릭하며 진행
   - **중요**: "Adjusting your PATH environment" 단계에서 "Git from the command line and also from 3rd-party software" 선택
3. **"Install"** 클릭
4. 설치 완료 (약 2-3분 소요)

#### 설치 확인

CMD 또는 Git Bash를 **새로** 열고:

```bash
git --version
```

→ `git version 2.43.0` 같은 버전이 나오면 성공!

---

### 📥 Mac 사용자

#### 방법 1: Command Line Tools 설치 (권장)

터미널을 열고:

```bash
git --version
```

처음 실행하면 Command Line Tools 설치 창이 나타납니다.
- **"Install"** 클릭
- 약 5-10분 소요

#### 방법 2: 공식 설치 파일

[Git 공식 사이트](https://git-scm.com/download/mac)에서 `.dmg` 파일 다운로드

1. 파일 실행
2. 설치 마법사 따라가기
3. 설치 완료

#### 설치 확인

터미널에서:

```bash
git --version
```

→ `git version 2.43.0` 같은 버전이 나오면 성공!

---

#### 방법 3: Homebrew 사용 (이미 Homebrew를 사용하는 경우)

```bash
brew install git
```

---

## Step 2: 초기 설정

Git을 처음 사용하면 **당신이 누구인지** 알려줘야 합니다.

이 정보는 모든 커밋(변경사항 저장)에 포함됩니다.

### ⚙️ 사용자 정보 설정

#### Windows (CMD 또는 Git Bash)

```bash
git config --global user.name "당신의 이름"
git config --global user.email "당신의 이메일"
```

#### Mac/Linux

```bash
git config --global user.name "당신의 이름"
git config --global user.email "당신의 이메일"
```

### 📝 예시

```bash
git config --global user.name "Kim Hyungwon"
git config --global user.email "hyungwon@example.com"
```

### ✅ 설정 확인

설정이 제대로 되었는지 확인:

```bash
git config --global user.name
git config --global user.email
```

→ 방금 입력한 정보가 나오면 성공!

---

### 💡 추가 설정 (선택사항)

기본 에디터 설정 (commit 메시지 작성 시 사용):

```bash
# Windows (Git Bash)
git config --global core.editor "notepad"

# Mac
git config --global core.editor "nano"
```

---

## Step 3: GitHub 계정 연결

Git은 로컬(컴퓨터)에서 버전 관리를 하고, GitHub는 원격(인터넷)에 코드를 보관합니다.

### 🔐 GitHub 계정 만들기

1. [GitHub 공식 사이트](https://github.com) 방문
2. **Sign up** 클릭
3. 이메일, 비밀번호, 사용자명 입력
4. 이메일 인증 완료

→ GitHub 계정 생성 완료!

---

### 🔑 로컬 컴퓨터와 GitHub 연결

#### 방법 1: HTTPS (초보자 권장)

HTTPS는 비밀번호 대신 "Personal Access Token"을 사용합니다.

**1단계: Personal Access Token 생성**

GitHub 로그인 후:
1. 우측 상단 프로필 → **Settings**
2. 좌측 메뉴 → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** 클릭
5. 설정:
   - Note: "gpters-project" (이름)
   - Expiration: "90 days" 또는 "No expiration"
   - Scopes: `repo` 체크
6. **Generate token** 클릭
7. 나타난 토큰을 **안전한 곳에 복사해서 저장** (나중에 다시 볼 수 없음)

**2단계: Git에 저장 (Windows)**

CMD 또는 Git Bash에서:

```bash
git config --global user.token "복사한_토큰을_여기에_붙여넣기"
```

또는 Git Credential Manager를 사용하면 자동으로 저장됩니다 (Git for Windows에 포함).

**3단계: 테스트**

```bash
git clone https://github.com/당신의_사용자명/테스트_저장소.git
```

처음 실행할 때 GitHub 로그인 창이 나타나면 사용자명 + 토큰 입력.

---

#### 방법 2: SSH (고급, 권장)

SSH는 공개키-개인키 쌍으로 인증합니다. 더 안전하지만 초보자에게는 복잡합니다.

**1단계: SSH 키 생성**

```bash
ssh-keygen -t ed25519 -C "당신의_이메일@example.com"
```

실행 후:
- "Enter file in which to save the key" → Enter (기본값)
- "Enter passphrase" → 비밀번호 입력 (또는 Enter로 스킵)

**2단계: 공개키를 GitHub에 등록**

```bash
# Mac/Linux
cat ~/.ssh/id_ed25519.pub

# Windows (Git Bash)
cat ~/.ssh/id_ed25519.pub
```

나타난 키를 복사 → GitHub → Settings → SSH and GPG keys → New SSH key → 붙여넣기

**3단계: 테스트**

```bash
ssh -T git@github.com
```

→ "Hi username! You've successfully authenticated" 메시지가 나오면 성공!

---

## Step 4: 첫 번째 프로젝트 복제 (Clone)

이제 GitHub의 프로젝트를 당신의 컴퓨터에 받아옵니다.

### 📥 프로젝트 Clone

**gpters-20th-templates** 프로젝트를 받아보겠습니다.

#### 1단계: 저장소 URL 준비

GitHub 프로젝트 페이지 → **Code** (초록색 버튼) → HTTPS 또는 SSH URL 복사

예시:
```
https://github.com/anthropics/gpters-20th-templates.git
```

#### 2단계: 터미널에서 프로젝트 받기

```bash
git clone https://github.com/anthropics/gpters-20th-templates.git
```

실행 후:
- GitHub 로그인 창이 나타나면 사용자명 + 토큰 입력
- 약 1-2분 소요

#### 3단계: 프로젝트 폴더로 이동

```bash
cd gpters-20th-templates
```

→ 프로젝트 폴더가 컴퓨터에 복제되었습니다!

---

### 확인

프로젝트 폴더 구조:

```bash
ls -la
```

또는 Windows:

```bash
dir
```

→ `.git` 폴더가 보이면 성공!

---

## Step 5: 기본 워크플로우

이제 실제로 코드를 작성하고 변경사항을 저장하는 방법을 배워봅시다.

### 🔄 일반적인 작업 흐름

```
1. 현재 상태 확인 (git status)
   ↓
2. 파일 수정 또는 생성
   ↓
3. 변경사항을 Staging Area에 추가 (git add)
   ↓
4. 변경사항을 저장 (git commit)
   ↓
5. 최신 코드 받기 (git pull) - 협업 시
   ↓
6. 원격 서버에 업로드 (git push)
```

---

### 📊 Step 5-1: 현재 상태 확인 (git status)

작업을 시작하기 전에 항상 현재 상태를 확인합니다.

```bash
git status
```

**출력 예시:**

```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

→ 모든 것이 저장된 상태 (깨끗한 상태)

**수정 후 출력 예시:**

```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to stage changes)
  (use "git restore <file>..." to discard changes)
        modified:   src/script.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        new_file.txt
```

→ 수정된 파일과 새 파일이 있는 상태

---

### 🔧 Step 5-2: 파일 수정 또는 생성

예시: `hello.py` 파일 생성

```python
print("Hello, Git!")
```

이제 파일을 저장합니다.

---

### 📝 Step 5-3: 변경사항 Staging (git add)

변경사항을 "저장할 준비"로 표시합니다.

#### 특정 파일만 추가

```bash
git add hello.py
```

#### 모든 변경사항 추가 (권장)

```bash
git add .
```

**확인:**

```bash
git status
```

→ 파일이 "Changes to be committed" 아래에 나타나면 성공!

---

### 💾 Step 5-4: 변경사항 저장 (git commit)

변경사항에 **설명을 붙여서** 저장합니다.

```bash
git commit -m "파일 설명을 여기에 작성"
```

### 📝 좋은 커밋 메시지 작성법

| 하지 말 것 | 하기 | 이유 |
|---------|------|------|
| "수정" | "Fix login validation" | 구체적 |
| "파일 생성" | "Add user authentication module" | 무엇을 했는지 명확 |
| "ㅗ" | "Update database connection" | 전문성 |

### 🎯 예시

```bash
git commit -m "feat: Add voice transcription skill for Week 2"
```

→ 커밋이 저장되었습니다!

---

### 📥 Step 5-5: 최신 코드 받기 (git pull)

여럿이 협업할 때, 다른 사람이 이미 코드를 업로드했을 수 있습니다.

push하기 전에 항상 pull하세요!

```bash
git pull
```

**출력 예시:**

```
Already up to date.
```

→ 새로운 변경사항이 없음

**다른 사람이 수정했으면:**

```
Updating abc1234..def5678
Fast-forward
 file.py | 5 +++
 1 file changed, 5 insertions(+)
```

→ 최신 코드를 받았습니다!

---

### 🚀 Step 5-6: 원격 서버에 업로드 (git push)

변경사항을 GitHub에 업로드합니다.

```bash
git push
```

**출력 예시:**

```
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Delta compression using up to 8 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (2/2), 290 bytes | 290.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/yourusername/gpters-20th-templates.git
   abc1234..def5678  main -> main
```

→ GitHub에 업로드 완료!

---

## 주의사항 & FAQ

### ⚠️ 중요한 주의사항

#### 1. **항상 push 전에 pull하기**

```bash
# ❌ 잘못된 예
git add .
git commit -m "my changes"
git push

# ✅올바른 예
git add .
git commit -m "my changes"
git pull        # 먼저 최신 코드 받기!
git push
```

**이유**: 다른 사람의 변경사항과 충돌할 수 있음

---

#### 2. **커밋 메시지는 명확하게**

```bash
# ❌ 나쁜 예
git commit -m "fix"
git commit -m "update"

# ✅ 좋은 예
git commit -m "Fix authentication bug in login form"
git commit -m "Update database connection timeout"
```

---

#### 3. **민감한 정보는 커밋하지 않기**

```bash
# ❌ 절대 하지 말 것
git add .env           # API 키, 비밀번호 포함!
git add secrets.txt    # 민감한 정보!

# ✅ 올바른 방법
# .gitignore에 다음 추가:
# .env
# .env.local
# secrets/
```

---

#### 4. **큰 파일은 커밋하지 않기**

```bash
# ❌ 문제 발생
git add large_video.mp4   # 100MB 이상
git add dataset.zip       # 수백 MB

# ✅ 해결책
# .gitignore에 추가하거나
# Git LFS 사용
```

---

### 💡 자주 묻는 질문 (FAQ)

#### **Q1. 마지막 커밋 메시지를 수정하고 싶어요**

```bash
git commit --amend -m "새로운 메시지"
```

⚠️ **주의**: push한 후엔 사용하지 마세요!

---

#### **Q2. 파일을 실수로 커밋했어요**

```bash
# 마지막 커밋 취소 (파일은 유지)
git reset --soft HEAD~1

# 파일 수정 후 다시 커밋
git add correct_file.py
git commit -m "Fixed file"
```

---

#### **Q3. 의도하지 않은 파일을 .gitignore에 추가해도 이미 커밋된 파일은?**

```bash
# 파일 추적 해제 (이전 버전은 유지)
git rm --cached file_to_remove.txt

# .gitignore에 추가
echo "file_to_remove.txt" >> .gitignore

# 커밋
git add .gitignore
git commit -m "Remove tracked file from git"
```

---

#### **Q4. GitHub에 푸시했는데 거부되었어요**

**원인과 해결:**

| 에러 메시지 | 원인 | 해결책 |
|-----------|------|--------|
| "Permission denied" | 인증 실패 | SSH 키 확인 또는 토큰 재생성 |
| "rejected" | 원격이 최신 | `git pull` 후 `git push` |
| "fatal: not a git repository" | Git 초기화 안 됨 | `git clone` 다시 실행 |

---

#### **Q5. 변경사항을 모두 취소하고 싶어요**

```bash
# 현재 작업 디렉토리 초기화 (주의!)
git checkout .

# 또는 특정 파일만
git checkout file.py
```

⚠️ **경고**: 저장되지 않은 변경사항은 영구 삭제됩니다!

---

#### **Q6. 예전 버전으로 되돌리고 싶어요**

```bash
# 커밋 히스토리 보기
git log --oneline

# 예전 커밋으로 돌아가기
git revert abc1234

# 또는 강제로 되돌리기 (조심!)
git reset --hard abc1234
```

---

#### **Q7. 여러 사람과 작업할 때 "merge conflict"가 나요**

같은 파일의 같은 부분을 수정하면 충돌이 발생합니다.

```bash
# 충돌 파일 확인
git status

# 파일을 열어서 충돌 부분 수정:
# <<<<<<< HEAD
# 당신의 코드
# =======
# 다른 사람의 코드
# >>>>>>> branch-name

# 수정 후 커밋
git add .
git commit -m "Resolve merge conflict"
git push
```

---

## 명령어 빠른 참조

### 설정 명령어

```bash
# 사용자 정보 설정
git config --global user.name "이름"
git config --global user.email "이메일"

# 설정 확인
git config --global --list
```

### 기본 워크플로우

```bash
# 프로젝트 받기
git clone https://github.com/repo.git

# 프로젝트 폴더로 이동
cd project-folder

# 현재 상태 확인
git status

# 모든 변경사항 추가
git add .

# 특정 파일만 추가
git add file.py

# 커밋 (변경사항 저장)
git commit -m "커밋 메시지"

# 최신 코드 받기
git pull

# 원격 서버에 업로드
git push
```

### 히스토리 확인

```bash
# 커밋 히스토리 보기
git log

# 간단하게 보기
git log --oneline

# 최근 5개만
git log --oneline -5

# 특정 파일의 변경사항
git log file.py
```

### 변경사항 확인

```bash
# 수정사항 보기
git diff

# 스테이지된 변경사항 보기
git diff --staged

# 특정 파일만 보기
git diff file.py
```

### 되돌리기

```bash
# 스테이지된 파일 제거
git reset file.py

# 작업 디렉토리 되돌리기
git checkout .

# 특정 파일만 되돌리기
git checkout file.py

# 마지막 커밋 취소 (파일 유지)
git reset --soft HEAD~1

# 마지막 커밋 취소 (파일도 삭제)
git reset --hard HEAD~1
```

### 브랜치 (고급)

```bash
# 브랜치 목록
git branch

# 새 브랜치 생성
git branch new-branch

# 브랜치 전환
git checkout new-branch

# 또는 한 번에
git checkout -b new-branch

# 브랜치 삭제
git branch -d old-branch
```

---

## 🎯 완료 체크리스트

설정이 완료되었는지 확인하세요:

- [ ] Git 설치됨 (`git --version` 확인)
- [ ] 사용자 정보 설정됨 (`git config --global user.name` 확인)
- [ ] GitHub 계정 생성됨
- [ ] GitHub와 로컬 연결됨 (HTTPS 또는 SSH)
- [ ] 프로젝트 Clone 완료 (`cd` 명령어로 폴더 이동 가능)
- [ ] `git status` 명령어 실행 가능

**모두 체크되었으면 준비 완료입니다!** 🎉

---

**작성일**: 2025-12-26
**대상**: gpters 20기 프리랜서, 비전공자, 초보자
**난이도**: 입문 (Beginner)
