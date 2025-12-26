# Setup Workspace - 초기 설정 마법사

> **gpters 20기 프리랜서를 위한 Claude Code 워크스페이스 초기 설정**       

4주 동안 나만의 자동화 Skill을 만들기 위한 첫 단계입니다.

## 🎯 이 명령어가 하는 일

### 1. 환영 메시지
- gpters 20기 스터디 소개
- Claude Code와 Agent Skills 간단 설명
- 4주 목표: **커스텀 Skill 3개 이상 완성**

### 2. 환경 검증 (자동)
다음 도구가 설치되어 있는지 확인합니다:
- ✅ **Claude Code** (v1.0 이상)
- ✅ **VSCode** (또는 다른 코드 에디터)
- ⏳ **Python 3.x** (Week 3에 설치 예정)
- ✅ **Git Bash** (Windows) / Terminal (Mac)

**Python 설치는 Week 3 전에 하면 됩니다!**
→ 설치 가이드: `docs/python-setup-guide.md` 참고

### 3. 필수 폴더 구조 생성

gpters-20th-templates 프로젝트에 필요한 기본 구조를 자동 생성합니다:       

gpters-20th-templates/
├── .claude/
│   ├── skills/              # Project Skills (팀 공유)
│   └── commands/            # Slash Commands
├── docs/
│   ├── python-setup-guide.md   # Python 설치 가이드
│   └── weekly-guides/          # 주차별 가이드
├── skills/                  # Skill 예제 모음
├── templates/               # 재사용 템플릿
├── examples/                # 실제 사용 예시
└── scripts/                 # 자동화 스크립트

### 4. Week 1 준비물 생성
첫 주차 학습에 필요한 파일들을 자동으로 만듭니다:
- `docs/weekly-guides/week1-guide.md` - 1주차 학습 가이드
- `templates/automation-design.md` - 자동화 설계서 템플릿
- `examples/my-first-idea.md` - 아이디어 작성 예시

### 5. Skills vs Commands 개념 설명
**중요한 차이점을 설명합니다:**

| | **Agent Skills** | **Slash Commands** |
|---|---|---|
| **실행 방식** | 🤖 모델이 자동 판단 | 👤 사용자가 직접 `/명령어` 입력 |  
| **위치** | `.claude/skills/` | `.claude/commands/` |
| **주요 파일** | `SKILL.md` | `명령어.md` |
| **사용 예** | 음성 전사, API 연동 | 워크스페이스 설정, 일일 노트 |       

**Week 2부터는 Skills를 주로 만들게 됩니다!**

### 6. 다음 단계 안내
설정 완료 후 할 일을 안내합니다.

---

## 📝 실행 방법

```bash
/setup-workspace

---
🚀 설정 완료 후 할 일

📅 Week 1: 나만의 데이터 만들고 문제 발견하기

1단계: README.md 읽기 (5분)
# 프로젝트 개요 확인
cat README.md

2단계: Week 1 가이드 확인 (10분)
# 1주차 학습 내용 확인
cat docs/weekly-guides/week1-guide.md

3단계: 자동화 아이디어 발견 (30분)
- templates/automation-design.md 템플릿 사용
- 나의 반복 업무 3가지 적기
- 자동화하고 싶은 것 1개 선정

4단계: 예제 Skill 살펴보기 (15분)
# 음성 전사 예제 확인
cat skills/voice-transcription/SKILL.md

# Google Calendar 예제 확인
cat skills/google-calendar/SKILL.md

---
📚 주요 커맨드 (Slash Commands)

스터디 기간 동안 사용할 유용한 명령어들:

Week 1-2: 기본 학습

- 이 명령어: /setup-workspace - 초기 설정 (지금 실행 중!)
- /todo - 할 일 추가
- /todos - 할 일 목록 확인

Week 3-4: Skill 개발

- (추후 추가될 명령어들)

---
❓ Skills vs Commands 더 자세히

🤖 Agent Skills (Week 2부터 만들 것)

언제 사용되나요?
- Claude가 자동으로 판단해서 사용
- 예: "이 녹음 파일 정리해줘" → 음성 전사 Skill 자동 실행

어디에 저장하나요?
- Personal Skills: ~/.claude/skills/ (모든 프로젝트에서 사용)
- Project Skills: .claude/skills/ (이 프로젝트에서만)

이번 스터디에서는?
→ Project Skills를 만들어서 팀과 공유합니다!

👤 Slash Commands (지금 사용 중)

언제 사용되나요?
- 사용자가 직접 /명령어 입력

어디에 저장하나요?
- .claude/commands/

예시:
- /setup-workspace ← 지금 이 명령어!
- /todo ← 할 일 추가

---
⚠️ 이 명령어는 하지 않습니다

❌ API 키 설정하지 않음
- API 키는 .env.local 파일에 작성해야 합니다
- Week 3 스터디에서 스터디장이 자세히 설명합니다
- .gitignore로 외부 유출 방지됨

❌ Python 패키지 자동 설치 안 함 (필요시 수동 설치 안내)
❌ Git 저장소 초기화 안 함 (이미 클론한 프로젝트 가정)
❌ 복잡한 질문하지 않음 (간단한 환영 메시지만)

→ 이유: 비개발자도 쉽게 시작할 수 있도록 최소한만 설정합니다.

---
🔄 재실행 가능

언제든 다시 실행 가능합니다.
- 기존 파일이 있으면 덮어쓰지 않습니다
- 누락된 파일만 새로 생성합니다

---
💡 자주 묻는 질문 (FAQ)

Q1. Personal Skills vs Project Skills 차이가 뭔가요?
- Personal Skills: 내 컴퓨터의 모든 프로젝트에서 사용 (~/.claude/skills/)  
- Project Skills: 이 프로젝트(gpters-20th-templates)에서만 사용 (.claude/skills/)

이번 스터디에서는?
→ Project Skills를 중심으로 팀과 공유합니다!
→ 원하면 나중에 Personal Skills로도 등록 가능합니다 (복사만 하면 됨)       

Q2. Windows에서 ~/.claude/skills/ 경로가 어딘가요?
- C:\Users\[사용자명]\.claude\skills\
- Mac/Linux: /Users/[사용자명]/.claude/skills/

Q3. Python이 없으면 어떻게 하나요?
- Week 2 전까지 설치하면 됩니다
- 설치 가이드: docs/python-setup-guide.md 참고

Q4. Skills를 만들려면 코딩을 할 줄 알아야 하나요?
- 아니요! Python 가이드를 보고 설치 + Claude에게 잘 물어보면 됩니다!       
- Week 1-2에서 차근차근 배웁니다

---
🎯 4주 후 달성 목표

✅ 핵심 결과물: 나만의 커스텀 Skill 3개 이상
✅ 서브 결과물: 업무 자동화 설계서
✅ 기대 효과: 주 5시간 이상 시간 절약

---
📖 더 알아보기

- Python 설치 가이드: docs/python-setup-guide.md
- Skills 공식 문서: docs/skills.md
- 스터디 상세 페이지: docs/gpters20.md
- 주차별 가이드: docs/weekly-guides/
- 프로젝트 README: README.md

---

환영합니다! 🎉
4주 후, 여러분만의 자동화 도구를 갖게 될 것입니다.
궁금한 점이 있으면 언제든 Claude에게 물어보세요!

--- 

