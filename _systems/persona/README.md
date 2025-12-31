# Persona - 입문자 프리랜서 타입 정의

> 4주 내에 자동화 Skill을 만드는 입문자 프리랜서들의 다양한 타입을 정의합니다.

---

## 📌 Persona 구조

각 Persona 문서는 다음 항목을 포함합니다:

### 1. 기본 정보
- **이름 & 별칭**: Persona의 대표 이름
- **기술 배경**: Python/개발 경험 수준
- **나이대 & 직업**: 현재 상황
- **월 소득대**: 프리랜서 수익 수준

### 2. 동기 & 목표 (Why)
- **자동화를 시작한 이유**: 근본 동기
- **4주 후 바라는 결과**: 구체적 목표상
- **성공의 정의**: 측정 가능한 지표

### 3. 제약사항 & 환경
- **기술적 제약**: Python 미경험, IDE 사용 불익 등
- **시간 제약**: 주 몇 시간 투자 가능?
- **환경**: OS, 장비, 네트워크

### 4. 행동 패턴 & 선호도
- **학습 스타일**: 영상/텍스트/예제 중심?
- **결과 지향성**: 과정을 즐기나, 결과만 원하나?
- **커뮤니티**: 혼자 하기 vs 함께 하기
- **도움 요청 빈도**: 자주 도움 요청? 독립적?

### 5. 고통점 (Pain Points)
- **현재 가장 큰 문제**: 반복되는 일, 시간 낭비
- **시도했던 해결책**: 이전에 뭘 했나?
- **왜 실패했나**: 막혔던 부분

---

## 🎯 정의된 Personas

| 이름 | 배경 | 주요 동기 | 파일 |
|------|------|---------|------|
| **김실무** | 비전공 프리랜서 | 반복 업무 자동화로 시간 절약 | `01-kim-practical.md` |
| **이창의** | 마케터 → 자동화 도전 | 데이터 수집/분석 자동화 | `02-lee-creative.md` |
| **박급함** | 학생/취준생 | 포트폴리오 + 수입 창출 | `03-park-hurried.md` |
| **최여유** | 숙련 개발자 (심화) | Skill을 팔기 위해 고도화 | `04-choi-leisure.md` |

---

## 📂 파일 구조

```
_systems/persona/
├── README.md (이 파일)
├── 01-kim-practical.md      (Kim - 실무형 비전공자)
├── 02-lee-creative.md       (Lee - 마케팅 배경)
├── 03-park-hurried.md       (Park - 급함)
└── 04-choi-leisure.md       (Choi - 숙련자)
```

---

## 🔗 관련 문서

- **Usecase**: `_systems/usecase/README.md` - 각 Persona가 할 수 있는 구체적 상황
- **Userflow**: `_systems/userflow/README.md` - 각 Usecase의 단계별 흐름
- **Feature Mapping**: `_systems/feature-mapping.md` - Persona별 필요 기능

---

## 📖 사용 방법

### 1. Persona 이해하기
→ 해당 Persona 문서 읽기 (5분)

### 2. 나와 가장 가까운 Persona 찾기
→ 어느 Persona와 가장 비슷한가? → 그 Persona의 Usecase 확인

### 3. Usecase 확인
→ `_systems/usecase/README.md`에서 해당 Persona의 Usecase 선택

### 4. Userflow 따라하기
→ 해당 Usecase의 Userflow 문서 열기 → 단계별 명령어 따라 실행

---

## 💡 Persona 확장

새로운 Persona가 필요하면:
1. 이 README의 포맷에 맞춰 새로운 `.md` 파일 생성
2. 파일 번호 붙이기 (05, 06...)
3. README의 "정의된 Personas" 테이블에 추가
4. `_systems/usecase/README.md`에 해당 Persona의 Usecase 추가
