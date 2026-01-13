---
name: ai-case
description: 현재 세션을 기반으로 gpters용 AI 활용 사례 게시글 작성
tags: [documentation, case-study, gpters, sharing]
reference-docs:
  auto-load-step-0:
    - path: claude.md
      purpose: "사용자 프로필 및 문체 참조"

  dynamic-load-references:
    - name: "questions"
      path: ".claude/reference/ai-case-writer/questions.md"
      when: "질문 단계 시작 전"
      reason: "4가지 질문 가이드 및 예시 참조"

    - name: "template"
      path: ".claude/reference/ai-case-writer/template.md"
      when: "게시글 작성 시작 전"
      reason: "게시글 템플릿 및 섹션별 가이드 참조"

    - name: "guidelines"
      path: ".claude/reference/ai-case-writer/guidelines.md"
      when: "게시글 작성 완료 후"
      reason: "주의사항, 이미지 추천, 업로드 가이드 참조"
---

# AI 활용 사례 게시글 작성 (AI Case Writer)

**현재 Claude Code 세션을 기반으로 gpters 게시판용 AI 활용 사례 게시글을 작성합니다.**

이 명령어는:
- 🧠 **현재 대화의 맥락**을 인식
- 📝 **4가지 핵심 질문**으로 사례 정보 수집
- 📄 **gpters 게시 양식**에 맞춰 자동 작성
- 🖼️ **이미지 추천**까지 제공

---

## 🚀 사용법

```bash
/ai-case
```

**흐름:**
1. 명령어 실행
2. 현재 세션 요약 확인
3. 4개 질문에 서술형으로 자유롭게 답변
4. 자동 문서화 (`AI_CASE_STUDY.md`)
5. 이미지 추천 + 게시판 업로드 가이드

---

## 🔄 실행 프로세스

### **Step 0: 현재 세션 인식 및 확인**

**Claude가 자동으로:**
1. 현재 대화 세션 읽기
2. 작업 내용 요약 (도구, 작업, 결과물)
3. 사용자에게 확인 요청

**출력 예시:**
```
이번 세션을 요약해봤어요:

- 작업: 주간 리포트 자동화
- 도구: Claude Code
- 결과: Python 스크립트 생성, 2시간 → 15분 단축

제대로 이해한 게 맞나요? (예/아니요)
```

**사용자 응답:**
- "예" → Step 1로 진행
- "아니요, 실제로는 [수정 내용]" → 재확인 후 진행

---

**추가 문서 확인:**
```
추가로 공유하고 싶은 문서가 있나요?
(작업 이력, 출처, 참고 자료 등)

없으면 "없음" 또는 "바로 시작"이라고 답해주세요.
```

**사용자 응답:**
- 파일 경로 제공 → 해당 파일 읽기
- "없음" → Step 1로 진행

---

### **Step 1-4: 4가지 질문 진행**

**원칙:**
- 한 번에 하나씩 질문
- 각 질문마다 추천 답변 3개 제공 (현재 세션 맥락 기반)
- 사용자가 "그거로 해" 또는 직접 서술
- 필요 시 꼬리질문 (역시 하나씩)

**질문 목록:**
1. 시작 계기와 불편함
2. AI 협업 과정 (인상적 순간 + 시행착오)
3. 결과와 배운 점
4. 향후 계획과 참고 자료

**상세 질문 가이드는 아래 참조:**
→ `.claude/reference/ai-case-writer/questions.md`

---

### **Step 5: 게시글 생성**

수집한 답변을 바탕으로 `AI_CASE_STUDY.md` 생성

**저장 경로:** `AI_CASE_STUDY.md` (루트)

**템플릿 구조:**
- 한줄 요약
- 이런 분들께 도움돼요
- 소개: 시도하고자 했던 것과 그 이유
- 진행 방법: 어떤 도구를 사용했고, 어떻게 활용했나요?
- 결과와 배운 점
- 재사용 가능한 프롬프트
- 도움 받은 글 (옵션)

**상세 템플릿은 아래 참조:**
→ `.claude/reference/ai-case-writer/template.md`

---

### **Step 6: 피드백 및 수정**

**Claude의 질문:**
```
초안을 작성했어요!
수정하고 싶은 부분이 있나요?
```

**사용자 피드백:**
- "없음" → Step 7로 진행
- "○○ 섹션 수정" → 피드백 반영 후 재확인

---

### **Step 7: 마무리 안내**

#### 1. 이미지 추천 (최소 3개)

**섹션 이름 기준으로 추천:**
```
📸 추천 이미지 위치:

1. "소개: 문제 상황" 섹션
   - 기존 방식의 불편함 스크린샷

2. "진행 방법: AI와 협업한 과정" 섹션
   - Claude와 대화하는 터미널 화면

3. "결과와 배운 점: 결과물" 섹션
   - 완성된 결과물 전체 화면
```

#### 2. 게시판 업로드 가이드

```
📋 gpters 게시판에 올리는 방법:

1. AI_CASE_STUDY.md 파일 우클릭 → "미리보기 열기"
   (Cmd+Shift+V / Ctrl+Shift+V)

2. 미리보기 화면에서 Cmd+A로 전체 선택

3. gpters 게시판 작성 화면에 Cmd+V로 붙여넣기

4. 추천된 위치에 이미지 추가 (드래그 앤 드롭)

5. 최종 확인 후 게시!
```

**상세 가이드는 아래 참조:**
→ `.claude/reference/ai-case-writer/guidelines.md`

---

## 📖 참고 문서

### 상세 가이드

- **Questions Guide** - `.claude/reference/ai-case-writer/questions.md`
  - 4가지 질문 가이드
  - 질문별 예시 답변
  - 진행 원칙

- **Template Guide** - `.claude/reference/ai-case-writer/template.md`
  - 게시글 템플릿 구조
  - 섹션별 작성 가이드
  - gpters 양식 매칭

- **Guidelines** - `.claude/reference/ai-case-writer/guidelines.md`
  - 작성 주의사항
  - 이미지 추천 방식
  - 업로드 가이드
  - 최종 체크리스트

### 연계 시스템

- `.claude/commands/devlog-writer.md` - 현재 세션 → 개발 로그 작성
- `CLAUDE.md` - 프로젝트 프로필 및 4주 목표

---

## ⚙️ 핵심 원칙

1. **현재 세션 기반** - 별도 파일 불필요
2. **한 번에 하나씩 질문** - 사용자 부담 최소화
3. **추천 답변 제공** - 빠른 진행 가능
4. **비개발자 친화적** - 코드↓, 프롬프트↑, 이미지↑
5. **gpters 양식 매칭** - 그대로 복붙 가능

---

## 💭 이 기능의 가치

이 게시글은 단순한 **작업 기록**이 아닙니다:

1. **커뮤니티 기여** - 다른 사람에게 용기와 아이디어 제공
2. **지식 자산화** - 재사용 가능한 프롬프트 템플릿 공유
3. **경력 증명** - AI 활용 역량 증명 자료
4. **피드백 수집** - 커뮤니티의 조언으로 더 나은 자동화

---

## 📌 사용 시점

**이런 때 사용하세요:**
- Claude Code로 작업 완료했을 때
- 자동화 스크립트 만들었을 때
- AI로 문제 해결했을 때
- 다른 사람과 공유하고 싶을 때

**스터디 리더가 온보딩 시 안내:**
```
작업 완료했으면 /ai-case 실행해서
gpters에 공유해보세요!
```

---

**Happy Sharing! 🚀**
