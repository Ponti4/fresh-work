# Usecase - 각 Persona의 구체적 상황과 목표

> 각 Persona가 4주 동안 해결하고 싶은 구체적인 상황(Usecase)을 정의합니다.

---

## 📌 Usecase 구조

각 Usecase 문서는 다음 항목을 포함합니다:

### 1. Usecase 제목 & 기본정보
- **제목**: 한 문장으로 요약 (예: "일일 메일 정리 자동화")
- **Persona**: 어느 Persona를 위한가?
- **문제 상황**: 지금 뭐가 불편한가?
- **목표**: 자동화 후 어떻게 달라길 원하나?

### 2. Current State (현황)
- **현재 프로세스**: 수동으로 어떻게 하고 있나? (단계별)
- **소요 시간**: 1회에 몇 분? 주 몇 회?
- **정량화**: 월 몇 시간 낭비되나?
- **고통점**: 가장 반복적이고 지겨운 부분은?

### 3. Desired State (원하는 상태)
- **자동화된 프로세스**: 이상적으로 어떻게 되길?
- **예상 절약 시간**: 월 몇 시간 절약?
- **추가 이득**: 시간 절약 외에 뭐가 좋아질까?

### 4. Constraints (제약사항)
- **기술 제약**: 무엇을 할 수 없나?
- **도구 제약**: 어떤 도구/서비스를 써야 하나?
- **보안/프라이버시**: 민감한 데이터 있나?

### 5. Success Criteria (성공 기준)
- **측정 가능한 지표**: 뭘 성공이라고 할 것인가?
  - 예: "월 5시간 절약", "오류율 0%", "설정 5분 이내"

---

## 🎯 Personas별 Usecase 매트릭스

### **Kim (실무형 비전공자)**
| # | Usecase | 우선순위 | 난이도 |
|---|---------|---------|--------|
| 01 | 일일 미팅 노트 자동 정리 | 🔴 High | ⭐⭐ |
| 02 | 일일 영수증 자동 분류 | 🟡 Medium | ⭐⭐⭐ |
| 03 | 주간 리포트 자동 작성 | 🟡 Medium | ⭐⭐⭐⭐ |

### **Lee (마케팅 배경)**
| # | Usecase | 우선순위 | 난이도 |
|---|---------|---------|--------|
| 01 | SNS 게시물 데이터 수집 자동화 | 🔴 High | ⭐⭐⭐ |
| 02 | 고객 피드백 감정 분석 자동화 | 🟡 Medium | ⭐⭐⭐⭐ |
| 03 | 월간 리포트 자동 생성 | 🟡 Medium | ⭐⭐⭐ |

### **Park (학생/취준생)**
| # | Usecase | 우선순위 | 난이도 |
|---|---------|---------|--------|
| 01 | 음성 녹음 자동 텍스트화 | 🔴 High | ⭐⭐ |
| 02 | 웹 크롤링으로 데이터 수집 | 🟡 Medium | ⭐⭐⭐ |
| 03 | 자동 이력서 포맷팅 | 🔴 High | ⭐⭐ |

### **Choi (숙련 개발자)**
| # | Usecase | 우선순위 | 난이도 |
|---|---------|---------|--------|
| 01 | 복잡한 API 오케스트레이션 | 🟡 Medium | ⭐⭐⭐⭐⭐ |
| 02 | AI 모델 자동 파인튜닝 | 🟡 Medium | ⭐⭐⭐⭐⭐ |
| 03 | 다중 데이터소스 통합 ETL | 🔴 High | ⭐⭐⭐⭐ |

---

## 📂 파일 구조

```
_systems/usecase/
├── README.md (이 파일)
│
├── kim-practical/
│   ├── 01-daily-meeting-notes.md
│   ├── 02-daily-receipt-classification.md
│   └── 03-weekly-report.md
│
├── lee-creative/
│   ├── 01-sns-data-collection.md
│   ├── 02-sentiment-analysis.md
│   └── 03-monthly-report.md
│
├── park-hurried/
│   ├── 01-voice-transcription.md
│   ├── 02-web-scraping.md
│   └── 03-resume-formatting.md
│
└── choi-leisure/
    ├── 01-api-orchestration.md
    ├── 02-ai-fine-tuning.md
    └── 03-multi-source-etl.md
```

---

## 🔗 관련 문서

- **Persona**: `_systems/persona/README.md` - 각 타입의 사람 정의
- **Userflow**: `_systems/userflow/README.md` - 각 Usecase의 단계별 실행 흐름
- **Feature Mapping**: `_systems/feature-mapping.md` - 필요한 기능 정리

---

## 📖 사용 방법

### 1단계: 자신의 Persona 찾기
→ `_systems/persona/README.md`에서 가장 가까운 Persona 선택

### 2단계: Usecase 선택
→ 위 매트릭스에서 자신이 원하는 Usecase 선택
→ 해당 Usecase 문서 읽기

### 3단계: Userflow 따라하기
→ `_systems/userflow/[persona-name]/[usecase-number]-[title]/`의 userflow 문서 열기
→ 각 Step별로 명령어 실행

### 4단계: 완료 후
→ `/devlog` 로 진행 문서화
→ 다음 Usecase 선택

---

## 💡 Usecase 추가

새로운 Usecase가 필요하면:
1. 해당 Persona 폴더 내에 `0N-title.md` 파일 생성
2. 위의 구조를 따라 작성
3. README의 매트릭스에 추가
4. 대응하는 Userflow 문서도 함께 생성 (같은 이름, 다른 폴더)
