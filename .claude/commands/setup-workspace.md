# Setup Workspace - 초기 설정 마법사

> **gpters 20기 프리랜서를 위한 Claude Code 워크스페이스 초기 설정**

4주 동안 나만의 자동화 Skill을 만들기 위한 첫 단계입니다.

## 🎯 목표

이 명령어는 다음을 진행합니다:
1. **당신의 상황 파악** (직업, 반복 업무, 목표) → Persona 자동 추론
2. **Memory 자동 생성** (Persona 정보 + 사용자 정보)
3. **시스템 환경 파악** (OS, Python, GPU)
4. **claude.md에 자동 저장** (메모리 문서화)

**중요: Persona 문서는 따로 관리하지 않습니다. Memory(JSON)로만 관리되며, 백그라운드에서 자동 업데이트됩니다.**

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

### Step 3: 당신의 상황은? (Persona 추론을 위한 질의)

**다음 4가지를 자유롭게 설명해주세요. (이를 바탕으로 Claude가 당신에게 가장 적합한 경로를 설계합니다)**

#### 3-1. 현재 상황 & 직업

```
"지금 뭐하고 계세요?"

예시:
- "마케팅 프리랜서로 일하고 있어요"
- "대학교 다니면서 취업 준비 중입니다"
- "개발자로 일하고 있는데, 부수입을 원해요"
- "일일 업무가 너무 많아서 시간을 절약하고 싶어요"
```

#### 3-2. 반복되는 업무

```
"주로 어떤 작업을 반복하세요?"

예시:
- "매일 미팅 음성 파일을 정리해야 해요"
- "SNS 댓글/좋아요 데이터를 손으로 정리하고 있어요"
- "고객 피드백을 이메일로 받아서 분류해야 해요"
- "매월 엑셀로 리포트를 만드는데 시간이 너무 걸려요"
```

#### 3-3. 가장 불편한 점

```
"그 중 가장 불편한 게 뭐예요?"

예시:
- "시간이 너무 오래 걸려요 (주 10시간 이상)"
- "정확도가 낮아서 자꾸 확인해야 해요"
- "포트폴리오가 약해서 취업이 안 돼요"
- "확장성이 없어서 데이터가 많아질수록 관리가 힘들어요"
```

#### 3-4. 기술 경험 & 4주 목표

```
"기술 경험은 어느 정도고, 4주 후 어떤 상태가 되길 원해요?"

예시:
- "코딩은 못 하는데, 3개 반복 업무를 자동화하고 싶어요"
- "Python 기초는 알지만, 실무는 처음이에요. 데이터 자동화 도구를 만들고 싶어요"
- "풀스택 개발자입니다. 판매 가능한 자동화 도구 3개를 만들고 싶어요"
- "마케팅 배경이라 데이터는 아는데, 코딩은 안 배웠어요. 포트폴리오 3개를 만들고 싶어요"
```

---

### Step 4: 당신의 Persona 확인

**분석 중입니다... 🤖**

당신의 답변을 바탕으로 분석했습니다:

```
당신은 "Lee" 타입 같습니다!

📌 Lee - 마케팅/데이터 중심

특징:
- 직업: 마케팅/성장 해킹 프리랜서
- 목표: 데이터 수집 & 분석 자동화
- 핵심: "데이터 정확성과 확장성"

추천 첫 도전:
🔴 SNS 게시물 데이터 자동 수집 (주 10시간 절약)
```

**이게 맞나요?**

1. ✅ **네, 맞아요!** → 다음으로 진행
2. ❌ **아니에요, 다시 선택하고 싶어요** → 4가지 Persona 목록 제시
3. ❓ **다른 타입들도 보고 싶어요** → 전체 4가지 Persona 상세 설명

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

### Step 12: Memory 및 CLAUDE.md 자동 생성

모든 정보가 확인되면 다음을 자동으로 수행합니다:

#### 1. Memory 자동 생성
```
✅ Memory 저장 중입니다...

.claude/memory/
└── user-lee-kim-chul-soo.json
    {
      "name": "김철수",
      "persona": "Lee",
      "job": "마케팅 프리랜서",
      "repeated_tasks": [
        "SNS 데이터 수집",
        "고객 피드백 분석"
      ],
      "main_pain": "시간이 너무 오래 걸림 + 정확도 문제",
      "tech_level": "Python 기초 가능",
      "first_challenge": "SNS 게시물 데이터 자동 수집",
      "created_at": "2025-12-31T10:30:00Z",
      "updated_at": "2025-12-31T10:30:00Z"
    }

✅ Memory 저장 완료!
```

**특징:**
- Persona 문서는 따로 생성되지 않습니다
- 모든 Persona 정보는 Memory(JSON)에만 저장됩니다
- `/clarify` 실행 시 이 Memory가 자동으로 로드됩니다
- 필요시 `.claude/memory/` 폴더에서 JSON을 직접 수정할 수 있습니다

#### 2. CLAUDE.md 파일 업데이트

```markdown
## 📋 User Profile

**Setup Status:** ✅ Complete

### Participant Information
- **Name:** 김철수
- **Persona:** Lee (마케팅/데이터 중심)
  - Memory: .claude/memory/user-lee-kim-chul-soo.json
- **Goal & Expected Outcome:** 데이터 자동화 (SNS 수집 & 분석)

### First Challenge (Week 1-2)
- **Title:** SNS 게시물 데이터 자동 수집
- **Expected Duration:** 3-4일
- **Expected Impact:** 주 10시간 절약

### System Information
- **OS:** Windows 11 Pro
- **CPU:** Intel Core i7-12700K
- **RAM:** 16GB
- **Python:** 3.11.5 ✅
- **GPU:** NVIDIA RTX 3080

### Project Progress
- **Current Week:** Week 1
- **Setup Date:** 2025-12-31
- **Last Updated:** 2025-12-31

### Next Steps
1. `/clarify "인스타그램 팔로워들의 댓글을 매일 수작업으로 정리하는데 2시간 걸려"`
2. 명확화 문서 생성 (자동)
3. `/design` → 설계 문서 생성
4. `/implement` → 코드 작성
5. `/git-commit` → 배포
```

✅ CLAUDE.md 저장 완료!

---

## 🎉 Step 13: 완료 및 다음 단계

설정이 완료되었습니다! 축하합니다! 🎊

이제 당신의 모든 정보가 자동으로 저장되었습니다:

```
✅ Memory: .claude/memory/user-lee-kim-chul-soo.json
✅ CLAUDE.md: Persona + 목표 정보 저장
✅ 다음 명령어 준비 완료
```

### 🚀 지금 바로 시작하세요:

**Step 1: 문제 명확화 (30분)**

```bash
/clarify "인스타그램 팔로워들의 댓글을 매일 수작업으로 정리하는데 2시간 걸려"
```

이 명령어를 실행하면:
1. 당신의 Memory가 자동으로 로드됨
2. 입력한 내용이 분석됨
3. 명확화 문서가 자동 생성됨
4. Memory와 CLAUDE.md가 자동 업데이트됨

**Step 2: 자동화 설계 (1시간)**

```bash
/design
```

**Step 3: 구현 (2-3시간)**

```bash
/implement
```

**Step 4: 배포 (1시간)**

```bash
/git-commit
```

---

### 📝 Memory 수정하기 (필요시)

당신의 정보를 수정하고 싶으면:

```bash
.claude/memory/user-lee-kim-chul-soo.json 파일을 열어서 수정
```

예:
- Persona 변경
- 목표 변경
- 반복 업무 추가/삭제

### 💡 자동 업데이트

- `/clarify` 실행 후 Usecase 생성 시 자동으로 Memory 업데이트
- `/design` → `/implement` 단계별로 Progress 자동 추적
- CLAUDE.md는 항상 최신 상태 유지

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
