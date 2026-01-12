---
name: routing-rules
description: Think Partner 커맨드에서 자동 라우팅하는 문서 경로 규칙 및 우선순위. Glob 패턴 및 로드 순서 정의.
---

# 문서 라우팅 규칙 (Routing Rules)

Think Partner 커맨드의 Step 1에서 사용되는 자동 문서 발견 및 로드 규칙입니다.

---

## 🔍 라우팅 규칙 정의

### 로드 순서 및 우선순위

```yaml
Phase 1: 기본 정보 (Priority: 1)
├─ claude.md
│  └─ 프로필 (이름, 상황, 목표)
│  └─ 목표 설정 (4주 목표, 반복 업무 등)
│  └─ 설정 정보 (OS, Python 설치 여부 등)

Phase 2: 자동화 의도 (Priority: 2)
├─ docs/_clarify/*.md (최근 3개 파일, 시간순 역순)

Phase 3: 진행 기록 (Priority: 2)
├─ docs/_devlog/*.md (최근 3개 파일, 시간순 역순)

Phase 4: 이전 논의 (Priority: 3)
├─ docs/_think-partner/*.md (최근 2개 파일, 시간순 역순)

Phase 5: 성공 패턴 (Priority: 4, Optional)
├─ docs/_patterns/*.md (있으면 자동 로드)
```

---

## 📋 Glob 패턴 상세

### 1. 프로필 정보 (claude.md)

```yaml
경로: claude.md (프로젝트 루트)
파일 존재 필수: Yes
로드 전략: 전체 파일 읽기

추출 정보:
├─ name: 사용자 이름
├─ job: 직업/상황
├─ 4-week-goal: 4주 목표
├─ repeat-task-1,2,3: 반복 업무
└─ setup-date: 설정 날짜
```

### 2. 자동화 의도 (clarify)

```yaml
경로: docs/_clarify/
패턴: docs/_clarify/clarify_*.md

로드 전략:
├─ 가장 최신 파일 3개 로드
├─ 시간순 역순 정렬 (최신 우선)
└─ 없으면 스킵 (에러 없음)
```

### 3. 진행 기록 (devlog)

```yaml
경로: docs/_devlog/
패턴: docs/_devlog/devlog_*.md

로드 전략:
├─ 가장 최신 파일 3개 로드
├─ 시간순 역순 정렬 (최신 우선)
└─ 없으면 스킵
```

### 4. 이전 논의 (think-partner)

```yaml
경로: docs/_think-partner/
패턴: docs/_think-partner/think_*.md

로드 전략:
├─ 가장 최신 파일 2개 로드
├─ 시간순 역순 정렬 (최신 우선)
└─ 없으면 스킵
```

---

## ⚠️ 에러 처리 규칙

### 파일 없을 때 처리

```yaml
claude.md:
└─ 필수 파일: Yes
└─ 없으면: 에러 발생 (커맨드 중단)

docs/_clarify/:
└─ 필수: No
└─ 없으면: 진행

docs/_devlog/:
└─ 필수: No
└─ 없으면: 진행

docs/_think-partner/:
└─ 필수: No
└─ 없으면: 스킵

docs/_patterns/:
└─ 필수: No
└─ 없으면: 스킵
```

---

**이 규칙에 따라 Think Partner 커맨드가 자동으로 맥락을 분석합니다!**
