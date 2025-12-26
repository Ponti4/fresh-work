---
route: "반복되는 업무 발견 → 자동화 Task 명확화 경로"
format: "3가지 분기 선택 지도"
context: "비전공자 프리랜서가 모호한 아이디어를 구현 가능한 Skill로 변환하는 시스템"
rules: "1단계 불편감지 → 2단계 극단화(선택) → 3단계 Task명확화 → 자동화설계 → 구현규칙 → 산출물매핑"
---

# 10. Clarify Path - 아이디어 명확화 경로

## 🎯 목표
반복 업무 발견 → 불편함 감지 → 극단화(선택) → Task 명확화 → 자동화 설계 → 구현 규칙 적용 → 산출물 매핑

---

## 🛤️ 경로 선택

### 경로 1: 명확한 문제 → Task 명확화 (20분)
불편함이 명확 → [10.1-discomfort-detection](10.1-discomfort-detection.md) → [10.3-task-clarification](10.3-task-clarification.md) → [10.5-automation-architecture-design](10.5-automation-architecture-design.md)

### 경로 2: 애매한 문제 → 극단화 → Task 명확화 (30분)
불편함이 모호 → [10.1-discomfort-detection](10.1-discomfort-detection.md) → [10.2-extreme-thinking](10.2-extreme-thinking.md) → [10.3-task-clarification](10.3-task-clarification.md) → [10.5-automation-architecture-design](10.5-automation-architecture-design.md)

### 경로 3: 경로 결정 (1분)
어떤 경로? → [10.4-agent-selection-guide](10.4-agent-selection-guide.md)

---

## 📄 문서 목록

| ID | 제목 | 설명 |
|:--:|------|------|
| 10.1 | [discomfort-detection](10.1-discomfort-detection.md) | 불편함 감지 체크리스트 |
| 10.2 | [extreme-thinking](10.2-extreme-thinking.md) | 극단화를 통한 문제 본질 발굴 |
| 10.3 | [task-clarification](10.3-task-clarification.md) | 5가지 질문으로 Task 명확화 |
| 10.4 | [agent-selection-guide](10.4-agent-selection-guide.md) | 경로 선택 가이드 |
| 10.5 | [automation-architecture-design](10.5-automation-architecture-design.md) | 자동화 아키텍처 설계 5단계 |
| 10.5.1 | [design-document-guide](10.5.1-design-document-guide.md) | 설계 문서 작성 방법 (모호함 제거) |
| 10.6 | [implementation-rules](10.6-implementation-rules.md) | 구현 규칙 (Python 3.11.7 + Git Bash) |
| 10.7 | [artifact-mapping](10.7-artifact-mapping.md) | 산출물 매핑 (설계→테스트→구현) |

---

## 🚀 전체 워크플로우

```
경로 결정 (10.4, 1분)
    ↓
불편감지 (10.1, 3분)
    ↓
극단화 (10.2, 10분, 선택)
    ↓
Task명확화 (10.3, 15분)
    ↓
자동화설계 (10.5, 30분)
    ↓
설계문서작성 (10.5.1, 참고)
    ↓
구현규칙적용 (10.6, 기본)
    ↓
산출물매핑 (10.7, 검증)
    ↓
TDD 구현 시작
```

---

**시작**: [10.4-agent-selection-guide](10.4-agent-selection-guide.md)
