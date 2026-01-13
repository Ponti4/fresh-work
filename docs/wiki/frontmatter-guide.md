---
name: frontmatter-guide
description: Claude Code의 YAML Frontmatter 가이드. 일반 Markdown과 Skill의 필수/선택 필드 구분 및 작성 방법
---

# Claude Code Frontmatter 가이드

> Claude Code에서 파일의 메타데이터를 정의하는 방법과 파일 타입별 차이점을 이해하기 위한 가이드입니다.

---

## 🔍 Read Context란?

**Read Context**는 Claude Code에서 파일을 읽을 때 **메타데이터(Frontmatter)를 먼저 로드하고 파싱하는 메커니즘**입니다.

### 파일 로드 순서

```
1️⃣ Frontmatter 파싱 (YAML 메타데이터) ← Read Context
   ↓
2️⃣ 본문 콘텐츠 로드
   ↓
3️⃣ 리소스/번들 로드 (필요시)
```

### Read Context의 4가지 역할

| 역할 | 설명 | 예시 |
|------|------|------|
| **인식 (Discovery)** | 파일의 목적을 즉시 파악 | `description`으로 언제 사용할지 판단 |
| **최적화 (Optimization)** | 필요한 메타데이터만 로드 | 전체 파일이 아닌 frontmatter만 먼저 읽음 |
| **라우팅 (Routing)** | 올바른 에이전트/도구 선택 | `model: haiku`, `allowed-tools` 적용 |
| **토큰 절감 (Token Efficiency)** | 불필요한 데이터 로드 방지 | 전체 본문 로드 전에 필터링 |

---

## 📋 Frontmatter란?

**Frontmatter**는 마크다운 파일의 **최상단에 위치하는 YAML 형식의 메타데이터**입니다.

### 기본 형식

```yaml
---
name: 파일-이름
description: 파일의 목적 및 사용 시점
추가-필드: 값
---
```

**구조:**
- `---`로 시작
- YAML 형식 (키: 값)
- `---`로 종료
- 파일 본문 시작 전에 위치

---

## 📊 파일 타입별 Frontmatter 비교

### 1️⃣ 일반 Markdown 문서 (docs/wiki/*.md)

**예시: `claude-code-change-log.md`**

```yaml
---
name: claude-code-change-log
description: Claude Code 공식 변경 로그 및 버전별 업데이트 내역
---
```

**특징:**
- **필수 필드**: `name`, `description`
- **불필요한 필드**: `context`, `agent`, `hooks`, `allowed-tools`
- **용도**: "읽혀지는" 리소스 (정보 제공)
- **이유**: 실행 코드가 아니라 정보만 전달

**일반 Markdown의 역할:**
- 초보자 가이드
- 개념 설명서
- 변경 로그
- 문서화

---

### 2️⃣ Skill 문서 (.claude/skills/SKILL.md)

**예시: `clarify-automations/SKILL.md`**

```yaml
---
name: clarify-automations
description: 반복 업무를 자동화 요구사항으로 명확화하는 대화형 스킬. 불편함 감지 → 기능 분해 → 최소 기능 정의 → 외부 연동 확인의 순차적 질문으로 Task를 검증하고 간단한 Task 정의서를 docs/_clarify 경로에 자동 저장. 비개발자용 자동화 아이디어 검증 스킬.
model: haiku
color: green
context: fork
allowed-tools: [Read, Write, Bash]
---
```

**특징:**
- **필수 필드**: `name`, `description`
- **추가 필드**: `model`, `color`, `context: fork`, `allowed-tools`
- **용도**: "실행되는" 인터랙티브 스킬
- **이유**: 도구를 호출하고 독립적인 서브-에이전트로 실행

**Skill의 역할:**
- 사용자 상호작용 (질문/답변)
- 파일 생성/수정 작업
- 외부 도구 실행
- 독립적인 작업 흐름

---

## 📈 필드별 비교표

| 필드 | 일반 MD | Skill | 설명 |
|------|--------|-------|------|
| **name** | ✅ 필수 | ✅ 필수 | 파일 식별자 (중복 불가) |
| **description** | ✅✅ 필수 | ✅✅ 필수 | 파일의 목적/사용 시점 (가장 중요) |
| **model** | ❌ | ✅ | 실행 에이전트 모델 (haiku/sonnet/opus) |
| **color** | ❌ | ✅ | UI 표시 색상 |
| **context** | ❌ | ⚠️ 선택 | 실행 컨텍스트 (none/fork) |
| **allowed-tools** | ❌ | ✅ | 사용 가능 도구 목록 |
| **agent** | ❌ | ❌ | **(사용 안함)** |
| **hooks** | ❌ | ❌ | **(사용 안함)** |

**범례:**
- ✅✅ = 필수 (반드시 포함)
- ✅ = 필수 (파일 타입마다)
- ⚠️ = 선택 (필요시만)
- ❌ = 불필요 (포함하지 말 것)

---

## 🔑 필드 상세 설명

### name (필수)

**역할:** 파일의 유일한 식별자

```yaml
name: claude-code-change-log
```

**작성 규칙:**
- kebab-case (소문자-하이픈)
- 파일명과 동일 (확장자 제외)
- 중복 불가

**예시:**
```yaml
name: bash-terminal-guide
name: clarify-automations
name: python-setup-guide
```

---

### description (✅✅ 가장 중요)

**역할:** 파일의 **목적**과 **사용 시점** 설명

Claude가 이를 읽고 "언제 이 파일을 사용할지" 결정합니다.

#### ❌ 나쁜 예시

```yaml
description: 터미널 가이드
```

❌ **문제점:**
- 언제 사용할지 불분명
- Claude가 활용 불가
- 사용자도 혼란

#### ✅ 좋은 예시

```yaml
description: gpters 20기 프리랜서를 위한 Terminal/Bash 기초 완전 초보자 가이드
```

✅ **포함된 정보:**
- **대상**: gpters 20기, 프리랜서
- **주제**: Terminal/Bash 기초
- **수준**: 완전 초보자

#### 📋 작성 체크리스트

```
✅ "누가" - 대상 사용자 (초보자/전문가/특정 역할)
✅ "언제" - 사용 시점 (문제 상황/학습 단계)
✅ "뭐" - 주제/내용 (기술/개념/가이드)
✅ "왜" - 목적 (학습/이해/해결)
```

**구조 (권장):**
```
[대상자] + "를 위한" + [주제] + [추가 정보]
```

**더 많은 예시:**
```yaml
description: Claude Code 공식 변경 로그 및 버전별 업데이트 내역

description: 반복 업무를 자동화 요구사항으로 명확화하는 대화형 스킬

description: Python을 처음 접하는 gpters 20기 프리랜서를 위한 설치 및 환경 설정 가이드
```

---

### model (Skill에서만 사용)

**역할:** 스킬 실행에 사용할 Claude 모델 지정

```yaml
model: haiku        # 빠르고 저비용 (권장)
model: sonnet       # 균형잡힌 성능
model: opus         # 최고 성능 (고비용)
```

**권장:**
- `haiku`: 대부분의 스킬 (빠른 응답, 낮은 비용)
- `sonnet`: 복잡한 분석 필요시
- `opus`: 매우 복잡한 작업

**예시:**
```yaml
model: haiku        # clarify-automations
```

---

### color (Skill UI에서 표시)

**역할:** slash command 메뉴에서 스킬 색상 표시

```yaml
color: green
color: orange
color: blue
```

**용도:** 시각적 구분 (선택사항)

---

### context (Skill의 실행 환경)

**역할:** 스킬이 **어떤 실행 환경**에서 작동할지 정의

```yaml
context: none       # 공유 컨텍스트 (기본값)
context: fork       # 격리된 서브-에이전트 실행
```

**차이점:**

| 값 | 의미 | 사용 |
|---|------|------|
| `none` | 메인 에이전트의 컨텍스트 내 실행 | 간단한 작업 |
| `fork` | **별도의 격리된 서브-에이전트에서 실행** | 독립적 작업 필요 |

**왜 fork를 사용하나?**
- 스킬이 독립적으로 작동
- 메인 컨텍스트 보호
- 에러 격리

**예시:**
```yaml
context: fork       # clarify-automations (독립적 질문 진행)
```

---

### allowed-tools (Skill에서 사용 가능한 도구)

**역할:** 스킬이 사용할 수 있는 Claude Code 도구 지정

```yaml
allowed-tools: [Read, Write, Bash]
allowed-tools: [Glob, Grep, Read]
```

**일반적인 도구:**
- `Read`: 파일 읽기
- `Write`: 파일 쓰기
- `Edit`: 파일 편집
- `Bash`: 터미널 명령 실행
- `Glob`: 파일 패턴 검색
- `Grep`: 콘텐츠 검색

**작성 형식:**
```yaml
# 배열 형식
allowed-tools: [Read, Write, Bash]

# 또는 리스트 형식
allowed-tools:
  - Read
  - Write
  - Bash
```

---

### agent, hooks (사용 안함 ❌)

**이 두 필드는 일반 Markdown과 Skill에서 모두 불필요합니다.**

```yaml
# ❌ 불필요
agent: none
hooks: none
```

**이유:**
- **agent**: 파일이 "실행되는" 코드가 아님
- **hooks**: 파일 읽기 시 자동 실행할 사건이 없음

---

## ✅ 작성 체크리스트

### 일반 Markdown 작성 시

```
✅ name과 description만 작성
✅ context, agent, hooks, allowed-tools 제외
✅ description에 대상/시점/주제 포함
✅ 공백만 사용 (탭 금지)
✅ --- 으로 시작, --- 으로 종료
```

**최소 예시:**
```yaml
---
name: bash-terminal-guide
description: gpters 20기 프리랜서를 위한 Terminal/Bash 기초 완전 초보자 가이드
---
```

---

### Skill 작성 시

```
✅ name, description 작성
✅ model: haiku 지정
✅ color 추가 (선택)
✅ context: fork 지정 (필요시)
✅ allowed-tools 리스트 작성
✅ agent, hooks 제외
```

**일반적 예시:**
```yaml
---
name: clarify-automations
description: 반복 업무를 자동화 요구사항으로 명확화하는 대화형 스킬
model: haiku
color: green
context: fork
allowed-tools: [Read, Write, Bash]
---
```

---

## 🔴 주의사항

### 일반 실수

| 실수 | ❌ | ✅ |
|------|-----|-----|
| **탭 사용** | `	name: file` | `name: file` (공백 2칸) |
| **구분자 생략** | `name: file` (---없음) | `---`로 시작/종료 |
| **불필요한 필드** | `agent: none` | (포함하지 말 것) |
| **모호한 description** | `가이드` | `gpters 20기를 위한 Python 설치 가이드` |
| **대문자 name** | `name: Terminal-Guide` | `name: terminal-guide` |

---

## 📚 실제 예시

### 예시 1: docs/wiki - 일반 가이드 문서

**파일:** `docs/wiki/claude-code-change-log.md`

```yaml
---
name: claude-code-change-log
description: Claude Code 공식 변경 로그 및 버전별 업데이트 내역
---

# Changelog
## 2.1.3
...
```

**분석:**
- ✅ `name`, `description`만 사용
- ✅ 불필요한 필드 없음
- ✅ 읽혀지는 리소스

---

### 예시 2: .claude/skills - 스킬 문서

**파일:** `.claude/skills/clarify-automations/SKILL.md`

```yaml
---
name: clarify-automations
description: 반복 업무를 자동화 요구사항으로 명확화하는 대화형 스킬. 불편함 감지 → 기능 분해 → 최소 기능 정의 → 외부 연동 확인의 순차적 질문으로 Task를 검증하고 간단한 Task 정의서를 docs/_clarify 경로에 자동 저장. 비개발자용 자동화 아이디어 검증 스킬.
model: haiku
color: green
context: fork
allowed-tools: [Read, Write, Bash]
---

# Clarify Automations - 요구사항 명확화 스킬
...
```

**분석:**
- ✅ 필수 필드: `name`, `description`
- ✅ Skill 특화: `model`, `color`, `context`, `allowed-tools`
- ✅ 실행되는 코드 (스킬)
- ✅ 도구 사용 (Read, Write, Bash)

---

## 🎓 핵심 정리

### 일반 Markdown (docs/wiki)

```yaml
---
name: {파일-이름}
description: {구체적-목적-및-사용-시점}
---
```

**핵심:** "읽혀지는" 리소스 → `name`과 `description`만 필요

---

### Skill Markdown (.claude/skills)

```yaml
---
name: {스킬-이름}
description: {스킬의-목적-및-사용-시점}
model: haiku
color: {색상}
context: fork
allowed-tools: [도구1, 도구2]
---
```

**핵심:** "실행되는" 코드 → 추가 메타데이터 필요

---

## 📖 관련 문서

- [Claude Code Changelog](claude-code-change-log.md) - 공식 버전 정보
- [Hooks 가이드](hooks.md) - 훅 사용법
- [Skills 가이드](skills.md) - 스킬 개발 방법

---

**마크다운 파일 작성할 때 이 가이드를 참고하세요!** 🚀
