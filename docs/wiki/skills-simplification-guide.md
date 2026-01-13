# Skills 문서 간략화 가이드

## 📌 핵심 원칙

### 1. Frontmatter의 Description이 핵심
- **Description에 모든 정보를 담기** (언제 사용하는지, 뭘 하는지)
- Body는 실행 시에만 로드되므로, "When to Use" 섹션은 중복 낭비

### 2. Body는 Essential만
- 절대적으로 필요한 절차만 포함
- 예시, 설명, 상세 가이드는 `references/` 폴더로 이동
- 500줄 이상이면 구조 분해 필요

### 3. Progressive Disclosure
```
Metadata (name + description) → Always in context
SKILL.md body → When skill triggers
References/ → Only when Claude determines needed
Scripts/ → Execute without loading
Assets/ → Use directly in output
```

---

## 📋 Simplified SKILL.md 구조 (권장)

### 1. Frontmatter (3줄)
```yaml
---
name: skill-name
description: 무엇을 하는가? + 언제 사용하는가? (50-100 words max)
---
```

### 2. Body (2-3 섹션, 200-300 words max)

**패턴 A: 순차적 워크플로우**
```markdown
# Skill Name

1단계부터 N단계까지 순서대로 진행. 상세 가이드는 [references/...](reference/...)

## Quick Start
[즉시 사용 가능한 예시 1개]

## Workflow
- Step 1: [간단한 설명]
- Step 2: [간단한 설명]
- Step N: [간단한 설명]

## References
- [상세 가이드 1](references/...)
- [상세 가이드 2](references/...)
```

**패턴 B: 선택지 있는 워크플로우**
```markdown
# Skill Name

5가지 방향 중 하나 선택. 각 방향별 상세 가이드는 [references/...](references/...)

## Quick Start
[즉시 사용 가능한 예시 1개]

## Options
- **(1) Option A** (언제 사용?) - 상세 가이드는 [reference/option-a.md](...)
- **(2) Option B** (언제 사용?) - 상세 가이드는 [reference/option-b.md](...)
- **(3) Option C** (언제 사용?) - 상세 가이드는 [reference/option-c.md](...)

## References
- [상세 가이드](references/...)
```

**패턴 C: 도구 사용 스킬**
```markdown
# Skill Name

[1줄 설명] 상세 가이드: [references/...](...)

## Setup
[필수 설치 사항]

## Usage
[기본 사용 명령어]

## References
- [상세 옵션](references/...)
- [데이터 스키마](references/...)
- [에러 처리](references/...)
```

---

## 🔄 현재 8개 스킬의 간략화 계획

### 1. **skill-creator** (현재: 356줄 → 목표: 150줄)
**현재 문제:** 6단계 상세 절차가 전부 body에 있음
**해결책:** "Step 1-6" 개요만 유지 → 각 단계별 상세 가이드는 references로 이동

### 2. **clarify-automations** (현재: 254줄 → 목표: 120줄)
**현재 문제:** Q1-Q6 상세 안내가 전부 body에 있음
**해결책:** "Workflow 개요" 유지 → 질문 가이드는 references로 이동

### 3. **skill-think-partner** (현재: 340줄 → 목표: 120줄)
**현재 문제:** Step 1-6, 5가지 방향, 심화 질문이 모두 body에 있음
**해결책:** "6단계 개요" + "5가지 방향 선택지" 유지 → 심화 질문은 references로 이동

### 4. **youtube-collector** (현재: 159줄 → 목표: 100줄)
**현재 문제:** 워크플로우 상세 설명이 길어짐
**해결책:** "4가지 워크플로우" 개요만 유지 → 스크립트 옵션 상세는 references로

### 5. **gpters-scraper** (현재: 예상 100줄 → 목표: 70줄)
**현재 문제:** 설치 확인, 여러 옵션이 섞여있음
**해결책:** Setup + 기본 usage만 유지 → 상세 옵션은 references로

### 6. **hook-creator** (현재: 예상 100줄 → 목표: 70줄)
**현재 문제:** 패턴 예시들이 많음
**해결책:** 워크플로우 개요만 유지 → 패턴 예시는 references로

### 7. **slash-command-creator** (예상 100줄 → 목표: 70줄)
**해결책:** 워크플로우 개요만 유지 → 상세 가이드는 references로

### 8. **subagent-creator** (예상 100줄 → 목표: 70줄)
**해결책:** 워크플로우 개요만 유지 → 상세 가이드는 references로

---

## ✅ 간략화 체크리스트

각 SKILL.md를 다음 기준으로 검토하세요:

```
□ Frontmatter description이 50-100 words?
□ Body가 200-300 words (max 500)?
□ "When to Use" 섹션 제거됨? (Frontmatter에 있음)
□ 상세 설명/예시는 references로 이동?
□ 스크립트 옵션 상세는 references로 이동?
□ 패턴, 에러 처리 등은 references로 이동?
□ Body에는 절차/워크플로우만 남음?
□ References 파일들이 각각 50-200 words?
□ 모든 references가 SKILL.md에서 링크됨?
```

---

## 💡 간략화 예시

### Before (current clarify-automations)
```markdown
---
name: clarify-automations
description: 반복 업무를 자동화 요구사항으로 명확화하는 대화형 스킬...
---

# Clarify Automations

## 역할
반복 업무를 **명확한 자동화 Task로 정의**하는...

## 핵심 원칙
**⚠️ 원격 제어 원칙 (Strictly One-by-One)**
1. 모든 질문은...

## 워크플로우
### Step 1: ...
### Step 2: ...
### Step 3: ...
[... 254줄 전부 ...]
```

### After (simplified)
```markdown
---
name: clarify-automations
description: 반복 업무를 자동화 요구사항으로 명확화. 빈도, 소요시간, 불편함, 기능, 기대효과, 외부연동 6단계 순차 질문 후 Task 정의서 자동 생성. 비개발자용 자동화 검증 스킬.
---

# Clarify Automations - 요구사항 명확화

6단계 순차 질문으로 자동화 Task를 명확화하고 정의서를 자동 생성합니다.

## Workflow

1. **불편함 감지** - 가장 귀찮은 부분 파악
2. **빈도/소요시간** - 월 절감 시간 계산
3. **기능 분해** - MVP 범위 정의
4. **기대효과** - 확보할 시간의 용도
5. **외부연동** - 추가 서비스 필요 확인
6. **정의서 생성** - `docs/_clarify/` 경로에 자동 저장

## References

상세 가이드:
- [질문 흐름 및 해석](references/question-flow.md)
- [산출물 템플릿](references/output-template.md)
```

**줄 수: 254줄 → 30줄 (88% 감소)**

---

## 🎯 실행 순서

1. **skill-creator** 먼저 간략화 (다른 스킬 창시 가이드 역할)
2. **clarify-automations** 다음 간략화 (주요 프로젝트 스킬)
3. **skill-think-partner** 다음 간략화 (주요 프로젝트 스킬)
4. 나머지 5개 스킬 순차 간략화

---

## 📌 주의사항

**하지 말 것:**
- ❌ Frontmatter에 상세 설명 (30-50 words가 좋음)
- ❌ Body에 너무 많은 예시
- ❌ "Step-by-step" 절차를 너무 상세하게
- ❌ References 폴더를 링크하지 않은 채로 남기기
- ❌ 50줄 이상의 긴 예시 코드 (scripts로 빼기)

**해야 할 것:**
- ✅ Description에 "When to Use" 정보 담기
- ✅ Body에는 절차/선택지 개요만
- ✅ 상세 내용은 모두 references로
- ✅ References의 각 파일을 적절한 크기로 (50-200 words)
- ✅ 모든 references를 SKILL.md에서 명시적으로 링크
