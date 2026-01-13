# 1주차 실습 - AX Mentor와 함께하는 DevLog 자동화

## 🎯 실습 개요

**목표**: Claude Code로 오늘 작업 내용을 자동으로 DevLog로 정리하는 자동화를 만들고, 실제 AX 사례를 학습한 멘토 에이전트의 도움을 받아 완성합니다.

**소요 시간**: 40분

**난이도**: ⭐ 쉬움

---

## 📋 이 실습에서 배우는 것

1. **순수 프롬프트로 자동화 구현** (Python 스크립트 NO)
2. **Sub-agent 생성 및 활용** (병렬 실행의 힘)
3. **실제 AX 사례 기반 문제 해결**
4. **AI Case Study 작성** (사례 게시글 자동 생성)

---

## 🎁 완성 후 얻는 것

### 결과물
```
gpters-practice/
├── devlog/
│   └── 20260113_my-first-automation.md  # 오늘 작업 자동 정리
├── .claude/
│   └── agents/
│       ├── ax-context-loader.md         # 사례 사전 로드 에이전트
│       └── ax-troubleshooter.md         # 문제 해결 에이전트
└── AI_CASE_STUDY.md                     # 사례 게시글 (자동 생성)
```

### 학습 효과
- ✅ 매일 20분 걸리던 작업 → 1분으로 단축
- ✅ Sub-agent의 병렬 실행 체험
- ✅ 실제 AX 사례 기반 문제 해결 경험
- ✅ 2-3주차에 활용할 기초 다지기

---

## 🔄 전체 워크플로우

```
1. Setup (5분)
   └─ 두 개의 AX Mentor Agent 생성

2. DevLog 자동화 실습 (20분)
   ├─ 프롬프트 5개로 DevLog 생성
   ├─ [막힘 발생 시]
   │  └─ ax-troubleshooter 자동 실행 → 실제 사례 제공
   └─ 완성

3. 사례 게시글 작성 (10분)
   └─ AI Case Write로 자동 생성

4. 회고 (5분)
   └─ 배운 점 정리
```

---

## 📊 Sub-agent가 해결하는 문제

### Before (Sub-agent 없이)
```
참가자: "프롬프트가 안 먹혀요"
→ Claude: AX 문서 10개 검색 (메인 context 가득 참)
→ Claude: 사례 분석
→ Claude: 답변
→ 메인 context 오염, 실습 흐름 끊김
```

### After (Sub-agent 활용)
```
참가자: "프롬프트가 안 먹혀요"
→ [메인] 즉시 해결 시도
→ [백그라운드] ax-troubleshooter가 별도 context에서 사례 검색
→ 0.5초 후: "해결했어요 + [실제 사례] 참고"
→ 메인 context 깨끗, 실습 계속 진행
```

---

## 🚀 시작하기

다음 문서를 순서대로 진행하세요:

1. **week1-practice-prompts.md** - 단계별 프롬프트 가이드
2. **.claude/agents/ax-context-loader.md** - 사례 로더 에이전트 (자동 생성)
3. **.claude/agents/ax-troubleshooter.md** - 문제 해결 에이전트 (자동 생성)

---

## 💡 핵심 개념

### Context 분리
- 메인 대화는 실습에만 집중
- 사례 검색은 별도 context에서 처리
- 40분 실습 내내 context 깨끗하게 유지

### 병렬 실행
- 문제 해결 + 사례 검색 동시 진행
- 0.5초 안에 종합 답변 제공
- 대기 시간 없이 빠른 실습

### 실제 사례 기반
- 이론이 아닌 실제로 작동한 프롬프트
- 10개 AX 사례에서 자동 추출
- "이렇게 하면 안 돼요"도 함께 학습

---

## ❓ 준비물

- ✅ Claude Code 설치 완료
- ✅ VSCode 실행 중
- ✅ gpters-20th-templates 프로젝트 열림
- ✅ 40분 집중 시간

준비되셨나요? **week1-practice-prompts.md**를 열어주세요! 🚀
