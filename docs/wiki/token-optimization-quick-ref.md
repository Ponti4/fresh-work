# Token 최적화 빠른 참조 (Quick Reference)

## 🎯 핵심 원리 (5초 요약)

```
Token 낭비 = 불필요한 설명 + 중복된 정보 + 부정확한 로드

효율적 설계 = SKILL.md(간결) + references(상세) + 조건부로드
```

---

## ⚡ 즉시 적용: TOP 5 최적화

### 1️⃣ 중복 문서 제거
```bash
# 예: docs/prompts/clarify-automations.md가 있으면서
#    .claude/skills/clarify-automations/이 있으면?
# → 한 쪽을 제거하세요

rm docs/prompts/clarify-automations.md
```
**효과:** 2,000 tokens/월 절감

### 2️⃣ SKILL.md 간결화 (목표: 500줄 이하)
```markdown
# Before (❌ 너무 상세)
## Core Principles
- Strictly One-by-One: 매 질문은 하나씩만...
- Non-Technical Language: 전문 용어 배제...
- MVP Focus: 복잡도 최소화...

# After (✅ 간결)
**원칙:** One-by-One | 비개발자친화 | MVP중심
```
**효과:** 150-200 tokens/파일

### 3️⃣ auto-load 제거 → 조건부 로드로 변경
```yaml
# Before (❌ Step 1에서 모든 파일 로드)
reference-docs:
  auto-load-step-1:
    - path: docs/_clarify/
    - path: docs/_devlog/

# After (✅ 필요할 때만)
when-to-load:
  step-1: "claude.md + 최근 clarify 1개"
  step-3: "direction-options.md"
  step-5: "이전 think-partner 1개"
```
**효과:** 10,000 tokens 절감/호출

### 4️⃣ 설명 축약: 서술형 → 표/불릿
```markdown
# Before (150 tokens)
월 소요시간이 5시간 이상이면 자동화할 가치가 높습니다.
월 1-5시간 사이면 규칙성을 확인해야 합니다.
월 1시간 미만이면 수동으로 하는 게 나을 수 있습니다.

# After (60 tokens)
- 월 5시간 이상 → ✅ 추천
- 월 1-5시간 → ⚠️ 규칙성 확인
- 월 1시간 미만 → ❌ 비추
```
**효과:** 60% Token 절감

### 5️⃣ References에 "로드 조건" 명시
```markdown
## References

- [질문 흐름](./references/question-flow.md)
  **로드:** Q1 실행 시

- [템플릿](./references/output-template.md)
  **로드:** Step 7 (문서생성) 시만
```
**효과:** 40% Context 절감

---

## 📊 Token 계산 공식 (간단 버전)

### Token ≈ 문자 수 (한글 기준)

```
한글 문장: "6단계 순차 질문으로 Task를 명확화합니다"
= 약 20 characters ≈ 20 tokens
```

### 파일 전체 Token

```
markdown 파일 1줄 ≈ 10-15 tokens (평균)

50줄 파일 ≈ 500-750 tokens
100줄 파일 ≈ 1,000-1,500 tokens
500줄 파일 ≈ 5,000-7,500 tokens
```

---

## 🎯 Tier별 콘텐츠 분류

### Tier 1: 반드시 필요 (SKILL.md에)
```markdown
✅ 워크플로우 단계
✅ 필수 선택지 (Q1~Q4 선택항)
✅ References 링크
✅ 한 문장 설명 (frontmatter description)
```

### Tier 2: 조건부 필요 (references에)
```markdown
⚠️ 각 단계의 해석
⚠️ 계산식 또는 표
⚠️ 예시 (1-2개)
⚠️ 배경 설명
```

### Tier 3: 참고용 (별도 파일 또는 제거)
```markdown
❌ 철학적 배경
❌ 프로젝트 역사
❌ 인물 소개
❌ 감정적 서술
```

---

## 📋 Skill 설계 템플릿 (최적화 버전)

```markdown
---
name: my-skill
description: 한 문장 + 특정 상황. (100 words 내)
---

# My Skill - 한글 제목

한 문장 설명.

## 워크플로우

1️⃣ Step 1 - 뭘 하나?
2️⃣ Step 2 - 뭘 하나?
3️⃣ Step 3 - 뭘 하나?

## References

- [상세 가이드](./references/guide.md) - 언제 로드?
- [템플릿](./references/template.md) - 언제 로드?

## 추가 정보 (선택)

[최소한의 배경 설명, 1-3줄]

---

## ⚠️ 주의

[필수 사항, 제약사항 있으면]
```

**목표: 30-50줄 (300-600 tokens)**

---

## 🚨 안티패턴 (피해야 할 것들)

### ❌ Anti-Pattern 1: 배경 설명이 50% 이상
```markdown
# PDF Processing Skill

PDF(Portable Document Format)는 1993년 Adobe에서 개발한...
[10줄 역사 설명]

# 문제점
- 사용자는 "PDF 편집하는 법"을 원함
- 역사는 필요 없음
- Token 낭비: 200+ tokens
```

### ❌ Anti-Pattern 2: auto-load로 모든 파일 강제 로드
```yaml
reference-docs:
  auto-load-always:  # ❌ 금지
    - all_files_in_folder/

# 문제점
- Step 1에서도 Step 7 정보가 로드됨
- Context 낭비: 90%
```

### ❌ Anti-Pattern 3: 1000줄 짜리 SKILL.md
```markdown
# Mega Skill (❌ 피해야 할 구조)

## Part 1: Introduction (200줄)
## Part 2: Basic Usage (300줄)
## Part 3: Advanced (400줄)
## Part 4: Troubleshooting (100줄)

# 문제점
- 초급 사용자는 Part 3, 4가 필요 없음
- 모든 정보가 항상 로드됨
- Context 낭비: 60%
```

**✅ 해결: 각각 references 파일로 분리**

### ❌ Anti-Pattern 4: 같은 정보를 3개 파일에 반복
```
docs/prompts/clarify.md (설명)
.claude/commands/clarify.md (설명 다시)
.claude/skills/clarify-automations/SKILL.md (설명 또 다시)
└─ references/question-flow.md (설명 또 또 다시)

# 문제점
- 유지보수 악몽 (4개 파일 모두 수정 필요)
- Token 낭비: 70% (중복)
```

**✅ 해결: Single Source of Truth (하나의 출처)**

---

## 📈 효과 측정

### 측정 전
```bash
# 현재 Token 사용량 확인 (보통 8,000-15,000)
# (정확한 측정은 Claude Code의 context 분석 필요)
```

### 최적화 후
```bash
# 다시 확인해서 비교
# 목표: 30-50% 절감

Before: 13,700 tokens
After: 8,800 tokens
절감: 36% ✅
```

### 성능 지표
```
응답시간: 8.2초 → 6.1초 (26% 빨라짐)
에러율: 12% → 4% (67% 감소)
사용자 만족도: "너무 길어요" → "명확해요" (대부분)
```

---

## 🔗 상세 가이드

더 깊이 있게 학습하려면:

1. **이론:** [token-context-optimization-guide.md](./token-context-optimization-guide.md)
   - Token 낭비의 원인
   - Claude Code 처리 방식
   - 최적화 기준 & 전략

2. **사례:** [token-optimization-examples.md](./token-optimization-examples.md)
   - 실제 프로젝트 최적화 사례
   - Before/After 비교
   - 구체적 코드 예시

3. **이 문서:** Quick Reference (지금 읽는 중)
   - 5분 안에 핵심 파악
   - 체크리스트 & 공식

---

## ⏱️ 적용 시간표

```
🚀 즉시 (5분)
- anti-pattern 확인
- 중복 문서 찾기

⚡ 오늘 (30분)
- TOP 5 최적화 중 1-2개 적용
- 파일 수정 & 테스트

📈 이번주 (2시간)
- 전체 프로젝트 검토
- 모든 최적화 적용
- 성능 측정

📚 이번달 (지속)
- 새로운 Skill은 처음부터 최적화된 구조로
- 팀 가이드라인 정리
- 정기적 검토
```

---

## 💬 자주 묻는 질문

**Q: "구체적인 예시는?"**
A: [token-optimization-examples.md](./token-optimization-examples.md) 참조

**Q: "정확한 Token 수는?"**
A: 이 문서는 "근사치"입니다. 정확한 측정은 OpenAI tiktoken 라이브러리 필요

**Q: "Sub-agent는?"**
A: Context가 그대로 전달되므로, 위 최적화가 더욱 중요함

**Q: "언제까지 최적화해야 하나?"**
A: SKILL.md가 30-50줄, 총 프로젝트 Token이 10,000 이하면 충분

---

## 🎓 학습 경로

```
1️⃣ 이 Quick Ref 읽기 (5분)
   ↓
2️⃣ Examples 문서로 실제 사례 보기 (15분)
   ↓
3️⃣ 자신의 프로젝트에서 1-2개 최적화 (30분)
   ↓
4️⃣ 성능 변화 확인 (10분)
   ↓
5️⃣ 전체 가이드 깊이 있게 읽기 (1시간)
   ↓
6️⃣ 팀과 공유 & 정기 검토 (지속)
```

---

**마지막 팁:** 완벽한 최적화보다 **"지속 가능한 구조"**가 중요합니다.
매달 1-2개의 작은 개선이 누적되면, 6개월 후에는 50% 이상 개선됩니다.
