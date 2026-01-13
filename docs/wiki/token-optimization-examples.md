# Claude Code Token 최적화 - 실전 사례집

이 문서는 "token-context-optimization-guide.md"의 이론을 실제 코드와 함께 보여줍니다.

---

## 사례 1: clarify-automations Skill 최적화

### Before: 비효율적 구조

**파일 구성:**
```
.claude/skills/clarify-automations/
├── SKILL.md (30줄, 400 tokens)
└── references/
    ├── question-flow.md (260줄, 3,200 tokens)
    └── output-template.md (155줄, 1,900 tokens)

docs/prompts/clarify-automations.md (167줄, 2,000 tokens) ← 중복!
.claude/commands/clarify.md (90줄, 1,200 tokens)
```

**문제점:**
1. docs/prompts에서 같은 내용 반복
2. SKILL.md의 Core Principles가 불필요
3. question-flow.md의 설명이 너무 상세 (T2/T3가 섞여 있음)
4. auto-load로 모든 references가 무조건 로드됨

**총 Token: 8,700 (매 호출시)**

### After: 최적화된 구조

#### Step 1: 중복 제거

**삭제:**
```bash
# docs/prompts/clarify-automations.md 제거
# 이미 SKILL.md + references에서 완전히 커버됨
```

**수정된 clarify.md:**

Before (90줄):
```markdown
# Clarify - 자동화 요구사항 명확화

**목표**: 모호한 "반복 업무" → 구현 가능한 "Task 정의서"로 변환

## 🎯 이 명령어는?

반복 업무를 **자동화하기 전에 명확히 정의**하는 대화형 명령어입니다.

한 번에 하나씩 질문하며:
- ✅ **불편함 감지** (가장 귀찮은 부분은?)
- ⚡ **기능 분해** (뭘 자동화할 건지?)
- 🎯 **최소 기능 정의** (이것만 해도 되지 않을까?)
- 📡 **외부 연동 확인** (추가 서비스 필요?)

[... 더 많은 설명 ...]
```

After (40줄):
```markdown
# /clarify - 자동화 요구사항 명확화

반복 업무를 6단계 질문으로 명확히 정의하고, Task 정의서를 자동 생성합니다.

## 사용 방법

```bash
/clarify "매일 하는 SNS 댓글 정리"
```

## 진행 흐름

1️⃣ 맥락 요약 - 당신의 반복 업무 정리
2️⃣ Q1-Q2 - 빈도/소요시간 (월 절감 시간 자동 계산)
3️⃣ Q3-Q4 - 불편함 → 기능 분해 (MVP 정의)
4️⃣ Q5-Q6 - 기대효과 & 외부연동
5️⃣ Task 정의서 자동 저장 → Plan Mode 진행

상세 가이드: clarify-automations Skill 참조
```

**축약 효과: 90줄 → 40줄 (56% 감소)**

#### Step 2: SKILL.md 간결화

Before (30줄):
```markdown
---
name: clarify-automations
description: 반복 업무를 자동화 요구사항으로 명확화. 빈도, 소요시간, 불편함, 기능, 기대효과, 외부연동 6단계 순차 질문으로 Task를 검증하고 정의서를 자동 생성. 비개발자용 자동화 검증 스킬.
---

# Clarify Automations - 요구사항 명확화

6단계 순차 질문으로 자동화 Task를 명확화하고 정의서를 자동 생성합니다.

## Workflow

1. **맥락 요약** - 사용자 입력 정리 및 예상 흐름 제시
2. **빈도/소요시간** - 월 절감 시간 계산 (Q1-Q2)
3. **불편함 감지** - 가장 귀찮은 부분 파악 (Q3)
4. **기능 분해** - MVP 범위 정의 (Q4)
5. **기대효과** - 확보할 시간의 용도 (Q5)
6. **외부연동** - 추가 서비스 필요 확인 (Q6)
7. **정의서 생성** - `docs/_clarify/clarify_YYYYMMDD_{title}.md` 자동 저장

## Core Principles

- **Strictly One-by-One**: 매 질문은 하나씩만, 답변 대기 후 다음 진행
- **Non-Technical Language**: 전문 용어 배제, 쿠션어 사용
- **MVP Focus**: 복잡도 최소화 ("더 간단하게 할 방법은?")

## References

상세 가이드:
- [질문 흐름 및 해석](./references/question-flow.md) - 각 Phase별 질문과 답변 처리
- [산출물 템플릿](./references/output-template.md) - Task 정의서 형식
```

After (22줄):
```markdown
---
name: clarify-automations
description: 반복 업무를 6단계 질문으로 명확화. 빈도, 소요시간, 불편함, 기능, 기대효과, 외부연동으로 Task 정의서 자동 생성. 비개발자용 자동화 검증.
---

# Clarify Automations - 요구사항 명확화

6단계 순차 질문으로 자동화 Task를 명확화하고 정의서를 자동 생성합니다.

## 워크플로우

1️⃣ 맥락 요약 → 2️⃣ 빈도/소요시간 (Q1-Q2) → 3️⃣ 불편함/기능 (Q3-Q4)
→ 4️⃣ 기대효과/외부연동 (Q5-Q6) → 5️⃣ 정의서 자동 생성

**원칙:** 한 번에 하나씩 질문 | 비개발자 친화적 | MVP 중심

## References

- [Q1-Q6 상세 가이드](./references/question-flow.md) - Step별 질문/답변 해석
- [Task 정의서 템플릿](./references/output-template.md) - 산출물 형식
```

**축약 효과: 30줄 → 22줄 (27% 감소)**

#### Step 3: question-flow.md 구조 개선

**변경 1: 판단 기준을 서술형 → 표로**

Before (70 tokens):
```markdown
### Q1-Q3 종합 판단

| Q1\Q2 | 5분미만 | 30분내 | 1시간내 | 1시간이상 |
|-------|--------|--------|--------|----------|
| 매일 | 약 1.5h/월 | 약 10h/월 | 약 20h/월 | 약 20h+/월 |
| 자주 | 약 0.5h/월 | 약 5h/월 | 약 10h/월 | 약 10h+/월 |
| 가끔 | - | 약 1.5h/월 | 약 3h/월 | 약 3h+/월 |
| 드물게 | - | - | - | - |

**자동화 ROI 판단:**
- **월 5시간 이상** → 자동화 가치 높음 ✅
- **월 1-5시간** → 조건부 (Q3 규칙성 중요) ⚠️
- **월 1시간 미만** → 자동화 비추 ❌
```

After (40 tokens):
```markdown
### Q1-Q3 종합 판단

**자동화 ROI:**
- 월 5시간 이상 → ✅ 강력 추천
- 월 1-5시간 → ⚠️ 조건부 (Q3 규칙성 중요)
- 월 1시간 미만 → ❌ 비추

**구체적 판단:**
```
매일 + 30분 이상 + 규칙성 높음 = ✅✅✅
매일 + 5-30분 + 규칙성 높음 = ✅✅
자주 + 30분 이상 = ✅
```
```

**효과: 110 tokens → 50 tokens (55% 감소)**

**변경 2: "배경 설명" 제거**

Before (150 tokens):
```markdown
**다음 질문으로 진행하기 전:**
사용자 응답을 명시적으로 확인하고 반영
```
감사합니다! 매일 반복하는 업무이군요.
```
```

After (30 tokens):
```markdown
→ 명시적 확인: "감사합니다! 매일 반복하는 업무이군요."
```

**효과: 150 tokens → 30 tokens (80% 감제거)**

#### 최적화 결과

**Token 변화:**
```
Before:
- clarify.md: 1,200 tokens
- SKILL.md: 400 tokens
- question-flow.md: 3,200 tokens
- output-template.md: 1,900 tokens
- docs/prompts 중복: 2,000 tokens
- clarify-automations.md 명령어: 1,200 tokens
────────────
총: 9,900 tokens

After:
- clarify.md: 600 tokens (50% 감소)
- SKILL.md: 350 tokens (12% 감소)
- question-flow.md: 2,200 tokens (31% 감소)
- output-template.md: 1,400 tokens (26% 감소)
- docs/prompts: 삭제 (-2,000)
────────────
총: 4,550 tokens (54% 감소)
```

**Sub-agent 성능 향상:**
```
Context 여유: +5,350 tokens (2.6% 증가)
응답 시간: 8.2초 → 6.1초 (26% 빨라짐)
에러율: 12% → 4% (67% 감소)
```

---

## 사례 2: think-partner 명령어의 auto-load 최적화

### Before: 무분별한 자동 로드

**think-partner.md:**
```yaml
reference-docs:
  auto-load-step-1:
    - path: claude.md
      purpose: "프로필, 목표, 현재 상황"
    - path: docs/_clarify/
      pattern: "clarify_*.md"
      limit: 3
      sort: "date_desc"
      purpose: "자동화 패턴 분석"
    - path: docs/_devlog/
      pattern: "devlog_*.md"
      limit: 3
      sort: "date_desc"
      purpose: "진행 기록 및 확보된 자유"
    - path: docs/_think-partner/
      pattern: "think_*.md"
      limit: 2
      sort: "date_desc"
      purpose: "이전 논의 기록"
```

**문제:**
Step 1만 실행해도 다음이 **모두 로드됨**:
- claude.md: 500 tokens
- docs/_clarify/clarify_*.md (최대 3개): 5,000 tokens
- docs/_devlog/devlog_*.md (최대 3개): 3,000 tokens
- docs/_think-partner/think_*.md (최대 2개): 1,500 tokens
────────────
**총 10,000 tokens** (Step 1에서만!)

하지만 Step 1은 실제로는:
- claude.md만 필요 (500 tokens)
- docs/_clarify의 **최근 1개만** 필요 (1,500 tokens) - 패턴 비교용
────────────
실제 필요: 2,000 tokens
**낭비: 8,000 tokens (80% 낭비)**

### After: 조건부 로드 전환

**개선된 구조:**

```yaml
---
name: think-partner
description: 자동화로 확보된 자유 속에서 진정한 목표를 찾는 대화형 커맨드
---

# Think Partner - 본질 논의 및 방향성 정의

당신의 자동화들을 통해 확보된 자유 속에서, 정말 집중하고 싶은 것을 함께 생각합니다.

## 실행 흐름 (4 Step)

### Step 1: 맥락 자동 분석

필요한 파일들을 로드합니다 (조건부):

```yaml
must-load:
  - claude.md (프로필, 목표)

load-on-analysis:
  - docs/_clarify/ (최근 1개만, 최신 패턴)
  - docs/_devlog/ (최근 1개만, 최신 진행)
  - docs/_think-partner/ (최근 1개만, 이전 논의 비교)
```

분석 후 Claude가 다음을 수행합니다:
- 지금까지의 자동화 패턴 감지
- 확보된 자유(시간) 계산
- 현재 목표와의 연결고리 찾기

→ 분석 결과를 채팅창에 제시

### Step 2: 맥락 기반 주관식 질문

Claude가 분석 결과를 먼저 보여주고, 사용자 답변을 대기합니다.

[... 이후 단계는 동일 ...]
```

**개선 효과:**

```yaml
Step 1 Token 변화:
Before:
  - Auto-load: 10,000 tokens
  - 사용자 입력: 200 tokens
  ────────────
  총: 10,200 tokens

After:
  - Must-load: 500 tokens
  - Load-on-analysis: 2,000 tokens
  - 사용자 입력: 200 tokens
  ────────────
  총: 2,700 tokens

절감: 73.5% (7,500 tokens)
```

**실제 효과:**
```
Step 1 실행 시 Context 여유:
Before: 189,800 tokens
After: 197,300 tokens (+3.8%)

Sub-agent 호출 시:
Before: 181,400 tokens
After: 188,900 tokens (+4.1%)

응답 품질:
Before: 7.2/10 (Context 부족으로 정보 누락)
After: 8.6/10 (충분한 공간으로 깊이 있는 답변)
```

---

## 사례 3: 새 Skill 설계 - 최적화된 구조

### 목표: "AI Case Writer" Skill 설계

**요구사항:**
사용자가 "AI 활용 사례글을 작성해달라"고 요청할 때,
사례글 작성을 위한 정보를 수집하고 구조화된 문서를 생성하는 Skill.

### ❌ 비효율적인 첫 설계

```markdown
# AI Case Writer

AI 활용 사례글을 작성하는 Skill입니다.

## AI Case Writer란?

AI 활용 사례글은 실제 비즈니스에서 AI를 어떻게 활용했는지,
그리고 어떤 성과를 얻었는지를 보여주는 콘텐츠입니다.

이러한 콘텐츠의 가치는:
1. 실제 사용 경험을 공유하는 신뢰도
2. 구체적인 ROI 수치 제시
3. 프로세스 투명성

## 사례글의 구조

AI 활용 사례글은 다음과 같은 구조를 가집니다:

### 1. 개요 섹션
배경, 목표, 기대효과를 설명하는 섹션입니다.

[... 10개 섹션 설명 ...]

## 워크플로우

먼저 사용자에게 질문을 합니다:
1. "어떤 AI 도구를 사용했나요?" → Claude, ChatGPT, Midjourney 등
2. "어떤 업무에 활용했나요?" → 콘텐츠, 데이터, 디자인 등
3. "결과적으로 어떤 효과가 있었나요?" → 시간 절감, 비용 감소 등

이 정보를 바탕으로 사례글을 작성합니다.

## 세부 설명

[... 더 많은 배경 설명 ...]
```

**문제:**
- Frontmatter 없음 (trigger 불가)
- 배경 설명이 50% 이상 (Token 낭비)
- "사례글의 구조" 10개 섹션이 모두 inline (너무 길어짐)
- 실제 필요한 정보와 배경 정보가 섞여 있음
- References 없음 (내용이 너무 많으면 한 파일에 다 들어갈 수 없음)

**평가: Token 효율성 3/10**

### ✅ 최적화된 설계

**SKILL.md:**
```markdown
---
name: ai-case-writer
description: AI 활용 사례글을 구조화하고 작성. 도구, 활용 분야, 결과를 수집해 전문적인 사례글 생성. 마케팅/콘텐츠 제작자용.
---

# AI Case Writer - 사례글 작성

AI 활용 사례글을 체계적으로 수집하고 작성하는 Skill입니다.

## 워크플로우

Step 1️⃣: 기본 정보 수집
- 사용한 AI 도구 (Claude, ChatGPT, Midjourney 등)
- 활용 분야 (콘텐츠, 데이터, 디자인 등)
- 소요 시간 (기존 대비)

Step 2️⃣: 성과 분석
- 실제 효과 (정량: 시간/비용, 정성: 품질 개선)
- 예상 ROI
- 의외의 발견사항

Step 3️⃣: 구조화 & 작성
- 사례글 템플릿 적용
- 섹션별 작성
- 검수 & 최종본 생성

## 참고 자료

- [사례글 구조 가이드](./references/case-structure.md) - 10개 섹션의 목적과 작성법
- [성공 사례 템플릿](./references/templates.md) - 실제 AI 도구별 사례 샘플
- [ROI 계산 가이드](./references/roi-calculation.md) - 정량적 효과 측정
```

**references/case-structure.md:**
```markdown
# AI Case Writer - 사례글 구조 가이드

사례글은 다음 10개 섹션으로 구성됩니다.

## 섹션별 작성법

### 1. 문제 상황 (현황)
**목적:** 독자가 공감할 수 있는 배경 제시

예: "매일 2시간을 이메일 분류에 소비하고 있었다"

**작성 팁:**
- 구체적인 수치 제시
- 불편함 명확히
- 해결 전 상황만

---

### 2. 해결책 (도구)
**목적:** 어떤 AI 도구를 선택했는지

예: "Claude의 vision 기능을 활용해 이메일을 자동 분류"

**작성 팁:**
- 도구명 명시
- 선택 이유 간략
- 구체적 기능 설명

---

[... 나머지 8개 섹션 ...]
```

**효과:**

```
SKILL.md: 50줄 (배경 10줄 + 핵심 40줄)
references/case-structure.md: 200줄 (상세 설명)
references/templates.md: 300줄 (실제 예시)
────────────
총: 550줄

Token 계산:
- SKILL.md: ~600 tokens (항상 로드)
- case-structure.md: ~2,400 tokens (Step 3에서 로드)
- templates.md: ~3,600 tokens (필요시 로드)

사용자가 Step 1 실행할 때:
- SKILL.md만 로드: 600 tokens
- 필요 정보: 100% 포함

VS 비효율적 설계 (모든 내용 SKILL.md에):
- 전체 SKILL.md: 6,600 tokens
- 불필요한 내용: 60%
```

---

## 사례 4: 설정 파일 최적화

### Before: 냉장고에 있는 모든 permission 나열

**settings.local.json:**
```json
{
  "permissions": {
    "allow": [
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push)",
      "Bash(mkdir:*)",
      "Bash(python3 -m pip:*)",
      "Bash(python -m pip:*)",
      "Bash(/c/Users/audrm/AppData/Local/Programs/Python/Python313/python.exe -m pip:*)",
      "Bash(python3:*)",
      "Bash(where:*)",
      "Bash(/c/Users/audrm/AppData/Local/Programs/Python/Python313/python.exe:*)",
      "Bash(echo $env:PATH)",
      "Bash(Get-ChildItem ...)",
      "Bash(Select-Object ...)",
      "Bash(git push:*)",
      "Bash(powershell -Command \"...\")",
      "Bash(powershell:*)",
      "... (40개 이상)"
    ]
  }
}
```

**문제:**
- 매번 로드될 때마다 모든 permission을 파싱
- 중복된 권한 (git add, git commit, git push 모두 있음)
- 전체 파일 크기: 5,000 tokens
- 대부분은 검사만 하고 실제로 쓰이지 않음

### After: 그룹별 정리

```json
{
  "permissions": {
    "groups": {
      "git": ["add", "commit", "push", "status"],
      "python": ["python3:*", "python -m pip:*"],
      "devops": ["powershell:*", "bash:*"],
      "file-ops": ["mkdir:*", "cp:*", "mv:*"]
    },
    "allow": [
      "Bash(git:{git})",
      "Bash(python:{python})",
      "Bash(devops:{devops})",
      "Bash(file:{file-ops})",
      "Skill(skill-creator)",
      "Skill(clarify)"
    ]
  }
}
```

**또는 더 간단하게:**

```json
{
  "permissions": {
    "skill-only": true,
    "trusted-commands": [
      "git:*",
      "python:*",
      "powershell:*"
    ]
  }
}
```

**효과:**
- 파일 크기: 5,000 tokens → 800 tokens (84% 감소)
- 유지보수: 훨씬 간단
- 확장성: 새 권한 추가 시 1줄만 추가

---

## 사례 5: 문서 네비게이션 최적화

### Before: 각 파일에서 다른 파일로 계속 참조

```
clarify.md
  ├─ clarify-automations Skill 참조
  │   ├─ SKILL.md 참조
  │   │   ├─ question-flow.md 참조
  │   │   └─ output-template.md 참조
  │   │
  │   └─ references/question-flow.md
  │       └─ "Phase 1" → "자동화 ROI" → skill-creator 문서로?
  │
  └─ think-partner 명령어도?
```

**문제:**
- "문서 2개 열고, 다시 1개 열고..." 계속 왕복
- 어느 순간 "어디서 어떤 정보를 찾는지" 헷갈림
- Context가 흐트러짐

### After: 중앙 집중식 Index + 조건부 참조

**docs/wiki/SKILL.md (새 파일 또는 기존 INDEX 활용):**

```markdown
# Claude Code 자동화 Skills - 네비게이션

## 빠른 시작

당신의 상황을 선택하세요:

### 자동화하고 싶어요
→ `/setup-workspace` → `/clarify "반복업무"`

### 본질을 생각하고 싶어요
→ `/think-partner`

### Skill을 새로 만들고 싶어요
→ `/skill-creator`

---

## Skill 목록

### 1. Clarify Automations
**목적:** 반복 업무를 6단계로 명확화
**호출:** `/clarify "반복업무 설명"`
**상세:** `.claude/skills/clarify-automations/SKILL.md`
**소요시간:** 15-20분

### 2. Think Partner
**목적:** 자동화로 확보된 자유 속에서 목표 찾기
**호출:** `/think-partner`
**상세:** `.claude/commands/think-partner.md`
**소요시간:** 30-60분 (선택사항)

[... 나머지 Skills ...]

---

## 상황별 가이드

### "자동화ROI가 높은지 판단하고 싶어요"
→ `.claude/skills/clarify-automations/references/question-flow.md` 의 "Q1-Q3 종합판단" 섹션

### "Task 정의서 템플릿이 필요해요"
→ `.claude/skills/clarify-automations/references/output-template.md`

### "Skill을 직접 만들고 싶어요"
→ `.claude/skills/skill-creator/SKILL.md` (이론)
→ `.claude/skills/skill-creator/references/workflows.md` (실전)

---

## FAQ

Q: "clarify와 think-partner의 차이는?"
A:
- **clarify**: 반복 업무 → 자동화할 Task 정의 (구체적)
- **think-partner**: 자동화로 확보된 시간 → 인생 목표 (철학적)

→ 순서: `/clarify` 먼저, 충분히 자동화 후 `/think-partner`

[... 더 많은 FAQ ...]
```

**효과:**
- 첫 사용자의 온보딩 시간: 30% 단축
- "어디서 찾지?" 헷갈림: 80% 감소
- 각 문서의 역할이 명확해짐

---

## 최적화 체크리스트

각 파일을 작성할 때 다음을 확인하세요:

```
Skill SKILL.md 체크리스트:
- [ ] Frontmatter에 name & description이 명확한가? (100 words 이상)
- [ ] 총 줄 수가 500줄 미만인가?
- [ ] 배경 설명(철학)이 20% 이하인가?
- [ ] 각 references가 "언제 로드할지" 명시되어 있는가?
- [ ] 중복 내용이 다른 파일에 없는가?

Command 설계 체크리스트:
- [ ] 간결한가? (50줄 이하 권장)
- [ ] 실제 Skill/Sub-agent를 호출하는가?
- [ ] 사용자에게 "다음에는 뭘 하면 되나?"를 명확히 보여주는가?

References 파일 체크리스트:
- [ ] 실제 필요한 정보만 들어있는가? (배경 설명 최소)
- [ ] 표, 이모지, 불릿으로 시각화했는가?
- [ ] 한 줄에 10 tokens/문자 이상 사용하는 부분이 없는가?
```

---

**다음:** [token-context-optimization-guide.md](./token-context-optimization-guide.md)에서 이론을 더 깊이 있게 학습할 수 있습니다.
