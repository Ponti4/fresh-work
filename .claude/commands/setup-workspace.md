# Setup Workspace - 초기 설정 마법사

> **gpters 20기 프리랜서를 위한 Claude Code 워크스페이스 초기 설정**

4주 동안 나만의 자동화 Skill을 만들기 위한 첫 단계입니다.

## 🎯 목표

이 명령어는 다음을 진행합니다:
1. **참여자 정보 수집** (이름, 목표, 숙련도)
2. **시스템 환경 파악** (OS, Python, GPU)
3. **claude.md에 자동 저장** (메모리 문서화)

---

## 📋 Part 1: 참여자 정보 수집

### Step 1: 환영 메시지

안녕하세요! 👋

**gpters 20기 Claude Code 워크스페이스 초기 설정**을 시작하겠습니다.

이 설정에서는 다음을 진행합니다:
- ✅ 당신에 대한 정보 수집 (이름, 목표, 숙련도)
- ✅ 시스템 환경 정보 확인
- ✅ 수집된 정보를 `claude.md`에 자동 저장

**예상 소요 시간:** 10-15분

계속하시겠습니까?

---

### Step 2: 이름/닉네임 입력

**자신을 소개해주세요!**

다음 중 하나를 선택하세요:
- 실명 사용
- 닉네임 사용
- 기타 (입력)

**입력 예시:**
- "김철수"
- "CodingKing"
- "freelancer_2025"

---

### Step 3: 원하는 목표 & 기대하는 성과

**4주 후 어떤 결과물을 기대하나요?**

자유롭게 작성해주세요:

**예시:**
- "음성 파일을 텍스트로 자동 변환하는 스크립트 만들기"
- "일일 업무 자동 정리 시스템 구축"
- "데이터 수집 및 분석 자동화 도구 개발"
- "API 연동 자동화 Skill 3개 만들기"

---

### Step 4: AI 숙련도 선택

**현재 Claude Code와 자동화에 대한 숙련도는 어느 정도인가요?**

다음 중 하나를 선택하세요:

1. **클로드 코드 및 자동화 입문자**
   - Claude Code를 처음 사용합니다
   - 자동화/Skill이 무엇인지 모릅니다
   - Python도 처음 배우는 중입니다

2. **클로드 코드 사용만 할 수 있고 나머지는 모름**
   - Claude Code의 기본 사용법은 알고 있습니다
   - 하지만 Skill, 자동화 등은 처음입니다
   - Python 경험이 거의 없습니다

3. **클로드 코드 숙련자**
   - Claude Code를 잘 사용하고 있습니다
   - Skill 개발 경험이 있습니다
   - Python을 어느 정도 할 수 있습니다

---

## 📋 Part 2: 시스템 환경 정보 수집

### Step 5: 운영체제 선택

사용 중인 운영체제를 선택해주세요:

**다음 중 하나를 선택하세요:**

- Windows (Windows 10/11)
- Mac (Intel 또는 Apple Silicon M1/M2/M3)
- Linux (wsl, Ubuntu, Fedora 등)

---

### Step 6: 시스템 정보 스크린샷 수집

### Windows 사용자

**다음 중 하나의 방법을 선택하세요:**

#### 방법 1: Settings 앱 (권장)
1. Windows 키 + I 누르기 (Settings 열기)
2. "System" 선택
3. 스크롤해서 "About" 클릭
4. 다음 정보가 보이는 스크린샷 촬영:
- Edition (예: Windows 11 Pro)
- Version
- OS Build
- Processor (CPU)
- Installed RAM

**스크린샷을 업로드해주세요.**

#### 방법 2: 명령어 방식
터미널을 열고 다음 명령어 실행:
```bash
systeminfo
```
결과 스크린샷 촬영 후 업로드

---

### Mac 사용자

**다음을 진행하세요:**

1. Apple 메뉴 클릭 (좌측 상단)
2. "About This Mac" 선택
3. 다음이 보이는 스크린샷 촬영:
   - macOS 버전 (예: macOS Sonoma 14.6)
   - Chip (Intel 또는 Apple Silicon M1/M2/M3)
   - Memory (RAM 크기)
   - Processor (CPU 정보)

**스크린샷을 업로드해주세요.**

---

### Linux 사용자

터미널에서 다음 명령어 실행:
```bash
uname -a
lsb_release -a
free -h
lscpu
```
결과 스크린샷 또는 텍스트 업로드

---

### Step 7: 정보 검증

스크린샷을 확인하여 다음 정보를 추출하겠습니다:

**확인할 정보:**

- 운영체제 및 버전
- 프로세서 (CPU)
- 메모리 (RAM)
- 아키텍처 (x64, ARM64, M1/M2 등)

---

### Step 8: Python 설치 여부 확인

**Python이 설치되어 있나요?**

### Python 확인 방법

**Windows 또는 Mac/Linux 모두:**

터미널/커맨드 프롬프트 열고 다음 입력:

```bash
python --version
```

또는

```bash
python3 --version
```

**결과 예시:**
```
Python 3.11.5
```

---

### 선택지:

1. **Python이 설치되어 있음** → Python 버전 입력 (예: 3.11.5)
2. **Python이 설치되어 있지 않음** → 설치 가이드 제공
3. **확실하지 않음** → 명령어 실행 후 스크린샷 업로드

---

### Step 9: GPU 정보 (선택사항)

프로젝트에서 음성 전사(Whisper), 이미지 처리 등 **GPU가 필요한 작업**을 계획 중이라면 GPU 정보를 수집합니다.

### NVIDIA GPU 확인 (Windows/Linux)

터미널에서 다음 명령어 실행:
```bash
nvidia-smi
```

**설치되어 있다면 결과 스크린샷 업로드**
**설치되지 않았다면 "GPU 없음" 선택**

### Apple Silicon GPU (Mac)

이미 "About This Mac" 스크린샷에서 확인했습니다! ✅

---

### Step 10: 정보 재확인

수집된 모든 정보를 다시 한 번 확인합니다:

**확인 사항:**

- ✅ 이름/닉네임 정확한가요?
- ✅ 목표 & 성과 정확한가요?
- ✅ 숙련도 선택 정확한가요?
- ✅ OS 정보 정확한가요?
- ✅ CPU 정보 정확한가요?
- ✅ RAM 크기 정확한가요?
- ✅ Python 버전 정확한가요?
- ✅ GPU 정보 정확한가요?

---

### Step 11: README 문서 확인

**이제 README.md를 읽으시겠습니까?**

README.md에는 다음 내용이 포함되어 있습니다:
- 프로젝트 전체 구조 및 목표
- 4주 학습 로드맵
- Skills 개발 프로세스
- 팀 협업 방식

**선택지:**
- ✅ **네, README를 읽겠습니다** → README 읽기 안내
- ⏭️ **나중에 읽겠습니다** → 바로 완료 화면으로 진행

---

### Step 12: claude.md에 자동 저장

모든 정보가 확인되면 다음을 수행합니다:

1. **claude.md 파일 업데이트**

   예시:
   ```markdown
   ## 📋 User Profile

   **Setup Status:** ✅ Complete

   ### Participant Information
   - **Name:** 김철수 (또는 닉네임)
   - **Goal & Expected Outcome:**
     - "음성 파일을 텍스트로 자동 변환하는 스크립트 만들기"
   - **AI Proficiency:** 클로드 코드 및 자동화 입문자

   ### System Information
   - **OS:** Windows 11 Pro
   - **OS Version:** 23H2
   - **Architecture:** x64
   - **CPU:** Intel Core i9-13900K
   - **RAM:** 32GB

   ### GPU Configuration
   - **GPU:** NVIDIA RTX 4090
   - **GPU Type:** nvidia_cuda
   - **Driver Version:** 550.40

   ### Python Environment
   - **Python Installed:** ✅ Yes
   - **Python Version:** 3.11.5
   - **Installation Path:** C:\Users\[username]\AppData\Local\Programs\Python\Python311
   - **Virtual Environment:** Not yet

   ### Project Progress
   - **Current Week:** Week 1
   - **Setup Date:** 2025-12-27
   - **Last Updated:** 2025-12-27
   ```

2. **파일 저장 완료**

---

## 🎉 Step 13: 완료 및 다음 단계

설정이 완료되었습니다! 축하합니다! 🎊

이제 `claude.md`에 당신의 모든 정보가 저장되었습니다.
이후 Claude Code와 함께 작업할 때 이 정보를 자동으로 참고합니다.

### 다음 단계:

**Week 1: 나만의 데이터 만들고 문제 발견하기**

1. **README.md 읽기** (5분)
   - 프로젝트 전체 개요 파악

2. **Week 1 가이드 확인** (10분)
   - 1주차 학습 내용 확인

3. **자동화 아이디어 정리** (30분)
   - 반복되는 업무 3가지 적기
   - 자동화하고 싶은 것 1개 선정

4. **예제 Skill 살펴보기** (15분)
   - 기존 Skill 분석

---

## ❓ Skills vs Commands

이 명령어는 **Slash Command**입니다.

### 🤖 Agent Skills
- Claude가 **자동으로** 판단해서 사용
- 예: "이 녹음 파일 전사해줘" → Whisper Skill 자동 실행
- Week 2부터 직접 만들 예정!

### 👤 Slash Commands
- 사용자가 **직접** `/명령어` 입력
- 예: `/setup-workspace`, `/todo`

---

## 📖 참고 문서

- Python 설치 가이드: `docs/python-setup-guide.md`
- Skills 공식 문서: `docs/skills.md`
- 스터디 상세 페이지: `docs/gpters20.md`
- 주차별 가이드: `docs/weekly-guides/`

---

## ⚠️ 주의사항

❌ **이 명령어는 하지 않습니다**
- API 키 자동 설정 (수동으로 `.env.local`에 입력)
- Python 패키지 자동 설치 (필요 시 별도 안내)
- Git 저장소 초기화 (이미 클론한 프로젝트 가정)

→ 비개발자도 쉽게 시작할 수 있도록 **최소한만** 설정합니다.

---

## 🔄 재실행 가능

이 명령어는 언제든 다시 실행 가능합니다:
- 기존 정보가 있으면 업데이트
- 누락된 정보만 추가 수집

---

**궁금한 점이 있으면 언제든 Claude에게 물어보세요!**

질문을 입력하시면 해당 Step으로 이동하겠습니다. 💡
