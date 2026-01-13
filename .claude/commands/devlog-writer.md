---
name: devlog
description: 현재 세션의 맥락을 활용하여 개발 로그를 작성합니다
tags: [documentation, workflow, logging]
---

# 개발 로그 생성 (DevLog Writer)

**현재 Claude Code 세션의 Context를 활용하여 개발 로그를 작성합니다.**

이 명령어는:
- 🧠 **현재 대화의 맥락**을 인식
- 📝 **5가지 핵심 질문**으로 당신의 의도를 파악
- 📂 **날짜별 독립 파일**로 자동 저장 (`docs/_devlog/devlog_YYYYMMDD_{제목}.md`)
- 🔄 **재사용 가능한 자산**으로 활용 (개인 회고, 팀 공유, 포트폴리오)

---

## 🚀 사용법

```bash
/devlog
```

**흐름:**
1. 명령어 실행
2. 5개 질문에 **주관식으로 자유롭게** 답변
3. 자동 문서화 (`docs/_devlog/devlog_YYYYMMDD_{제목}.md`)

---

## 📋 Interactive 질문 Flow

### **질문 1️⃣: 작업 제목/주제**
> 이번 세션에서 다룬 핵심 작업이 무엇인가요?

**예시:** "DevLog 시스템 개선", "AI 리터러시 템플릿 개발"

---

### **질문 2️⃣: 문제 상황 (Before)**
> 이 작업을 시작하게 된 배경이나 불편함이 무엇이었나요?

**예시:** "기존 DEVLOG.md 누적으로 관리 어려움", "수동 정리 20-30분 소요"

---

### **질문 3️⃣: Context의 역할**
> 이번 작업에서 Claude Code 세션이 어떤 역할을 했나요?

**예시:** "현재 대화 활용해 수동 작업 감소", "복잡한 아키텍처 실시간 논의"

---

### **질문 4️⃣: DevLog의 목적**
> 이 DevLog를 어떤 용도로 활용할 예정인가요?

**선택 옵션:**
- **A) 개인 회고용** - 성장과 변화 추적
- **B) 팀/커뮤니티 공유용** - 배운 점 공유
- **C) 블로그/포스팅 기초 자료** - 블로그 변환 예정
- **D) 포트폴리오 & 경력 자산** - 보유 기술, 경험 기록
- **E) 기타** - 주관식 입력

---

### **질문 5️⃣: 주요 산출물**
> 이번 작업의 주요 결과물이나 생성된 파일이 있다면?

**예시:** `.claude/commands/devlog-writer.md`, `docs/_devlog/` 등

---

## 📄 출력 포맷

**저장 경로:** `docs/_devlog/devlog_YYYYMMDD_{제목}.md`

**구조:**
- 한줄 요약
- 타겟 독자
- 문제 상황 (Before)
- Context의 역할
- 작업 과정
- 결과 (After) - Before vs After 비교
- 배운 점 & 인사이트
- 다음 단계
- DevLog 메타정보

**상세 구조는 아래 Template Guide 참조:**
→ `.claude/reference/devlog/template-guide.md`

---

## 📖 참고 문서

### 상세 가이드
- **Template Guide** - `.claude/reference/devlog/template-guide.md`
  - 템플릿 구조 상세
  - 섹션별 작성 가이드
  - 블로그 변환 대비 팁

- **Question Guide** - `.claude/reference/devlog/question-guide.md`
  - 5개 질문의 의도와 배경
  - 질문별 작성 팁
  - 우선순위 및 생략 가능 여부

- **Examples** - `.claude/reference/devlog/examples.md`
  - 실제 사용 예시
  - 대화 흐름
  - 생성된 DevLog 샘플

### 연계 시스템
- `.claude/commands/ai-case-writer.md` - DevLog → 블로그 포스팅 변환
- `CLAUDE.md` - 프로젝트 프로필 및 4주 목표
- `docs/_think-partner/` - 전략 논의 및 방향성 정의

---

## 💭 DevLog의 가치

이 DevLog는 단순한 **작업 기록**이 아닙니다:

1. **자산화** - 개인 회고로 성장 추적, 블로그 기초 자료로 재활용
2. **맥락 보존** - 복잡한 결정 과정과 이유를 남겨 나중에 참고
3. **AI 활용 리터러시** - 비개발자도 AI와 함께 일하는 방식 학습
4. **다음 자동화의 아이디어** - 이전 경험을 바탕으로 더 나은 자동화 설계

---

**Happy DevLogging! 🚀**
