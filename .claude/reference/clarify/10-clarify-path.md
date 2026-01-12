---
route: "반복되는 업무 발견 → 자동화 Task 명확화 경로"
format: "통합된 단일 경로 가이드"
context: "비전공자 프리랜서가 모호한 아이디어를 구현 가능한 Skill로 변환하는 시스템"
rules: "1단계 문제 본질 파악(불편+극단화) → 2단계 Task 명확화 → 자동화 설계 → 구현 규칙 적용"
---

# 10. Clarify Path - 아이디어 명확화 경로

## 🎯 목표
반복 업무 발견 → 문제 본질 파악(불편+극단화) → Task 명확화 → 자동화 설계 → 구현 규칙 적용

---

## 🛤️ 통합 경로 (20~30분)
이제 모든 문제는 하나의 통합된 경로로 명확화됩니다.

1. **문제 본질 파악** (5분) → [10.1-discomfort-detection](10.1-discomfort-detection.md) (불편감지 + 극단적 가정)
2. **Task 명확화** (10분) → [10.3-task-clarification](10.3-task-clarification.md) (구체적인 요구사항 정의)
3. **자동화 설계** (20분) → [10.5-automation-architecture-design](10.5-automation-architecture-design.md) (기술 선택 및 아키텍처)
4. **구현 규칙 확인** (5분) → [10.6-implementation-rules](10.6-implementation-rules.md) (Python/TDD 규칙)

---

## Step 1: 문제 본질 파악 - 불편감지 + 반복 업무 검증

반복 업무를 발견했으면, "정말 자동화할 만한가?"를 객관적으로 검증합니다.
모호한 감정을 제거하고 데이터 기반으로 판단합니다.

### 체크리스트 (모두 YES여야 자동화 후보)

**반복 업무의 5가지 필수 조건**을 확인합니다:

- □ **반복성**: 이 일이 "오늘도, 내일도, 모레도" 반복되는가?
- □ **빈도**: 일주일에 1회 이상 반복되는가?
- □ **시간낭비**: 한 번에 5분 이상 시간이 드는가?
- □ **지겨움**: 정말 싫고 반복하기 싫은 업무인가?
- □ **규칙성**: 매번 거의 동일한 방식으로 진행되는가?

### 정량화 (필수)

단순한 YES/NO가 아닌 구체적인 수치로 객관화합니다:

- **현재 월 시간 낭비**: _____ 시간
- **자동화 후 월 절약 시간**: _____ 시간
- **절약 시간 활용 계획**: _________________ (예: 마케팅, 신규 고객 발굴 등)

**정량화 팁**: 한 달 동안 이 업무를 몇 번 반복하는지 세고, 회당 소요 시간을 곱합니다.

### 판정 기준

| 결과 | 조건 | 다음 단계 |
|:--:|------|---------|
| ✅ 진행 | 모두 YES + 월 2시간 이상 | [10.3-task-clarification](10.3-task-clarification.md) |
| ❌ 제외 | 월 1시간 미만 또는 규칙성 낮음 | 자동화 후보 제외 |

**핵심**:
- 모든 항목 YES여야 자동화 진행
- 하나라도 NO면 범위 재검토 또는 제외
- 월 1시간 미만 = ROI 부족, 제외 권장

---

## 📄 문서 목록

| ID | 제목 | 설명 |
|:--:|------|------|
| 10.1 | [discomfort-detection](10.1-discomfort-detection.md) | 문제 본질 파악 (불편감지 + 극단적 가정) |
| 10.3 | [task-clarification](10.3-task-clarification.md) | 5가지 질문으로 Task 명확화 |
| 10.5 | [automation-architecture-design](10.5-automation-architecture-design.md) | 자동화 아키텍처 설계 5단계 |
| 10.6 | [implementation-rules](10.6-implementation-rules.md) | 구현 규칙 (Python 3.11.7 + Git Bash) |

---

## 🚀 전체 워크플로우

```
문제 본질 파악 (10.1, 5분)
    ↓
Task명확화 (10.3, 10분)
    ↓
자동화설계 (10.5, 20분)
    ↓
구현규칙확인 (10.6, 5분)
    ↓
TDD 구현 시작
```

---

**시작**: [10.1-discomfort-detection](10.1-discomfort-detection.md)