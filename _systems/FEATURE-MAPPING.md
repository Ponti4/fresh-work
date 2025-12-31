# Feature Mapping: Persona → Userflow → 필요 기능

> 각 Persona의 Userflow에서 실제로 필요한 기능들을 구체적으로 정의합니다.
> 이 문서를 통해 "뭐를 만들어야 하나?"가 명확해집니다.

---

## 📊 전체 매핑 개요

```
Persona (누가?)
    ↓
Usecase (뭘 하고 싶은가?)
    ↓
Userflow (어떤 단계로 진행되나?)
    ↓
Required Features (뭐가 필요한가?)
```

---

## 🎯 Persona별 필요 기능 매트릭스

### Legend
- 🔴 **Essential** (없으면 불가능)
- 🟡 **Important** (있으면 훨씬 좋음)
- 🟢 **Nice-to-have** (있으면 더 좋음)

---

## 1️⃣ Kim (실무형 비전공자) - 필요 기능

### 특성 요약
- **핵심 이슈**: 러닝커브, 포기 위험
- **솔루션**: 최소한의 학습 + 빠른 성공

### Userflow: 일일 반복 작업 자동화

**Step 1: 문제 명확화 (30분)**
| 기능 | 설명 | 우선순위 | 현황 |
|-----|------|---------|------|
| `/clarify` 명령어 | 사용자의 반복 업무를 Task로 변환 | 🔴 Essential | ✅ 있음 |
| 명확화 결과 파일 | 마크다운 형식의 명확화 문서 산출 | 🔴 Essential | ✅ 있음 |
| 예제 입력 가이드 | "예를 들어 이렇게 입력하세요" | 🟡 Important | ❌ 필요 |

**Step 2: 자동화 설계 (1시간)**
| 기능 | 설명 | 우선순위 | 현황 |
|-----|------|---------|------|
| `/design` 명령어 | 명확화된 Task → 설계 문서 생성 | 🔴 Essential | ❌ **필요** |
| 시각화된 설계 | Flow 다이어그램 + Input/Output 명시 | 🔴 Essential | ❌ **필요** |
| 설계 검증 | "이 설계로 진행해도 되나?" 체크리스트 | 🟡 Important | ❌ **필요** |

**Step 3: 테스트 템플릿 생성 (30분)**
| 기능 | 설명 | 우선순위 | 현황 |
|-----|------|---------|------|
| `/test-generator` 명령어 | 설계 기반 테스트 파일 자동 생성 | 🔴 Essential | ❌ **필요** |
| 테스트 케이스 예제 | "이런 상황을 테스트해야 해" | 🟡 Important | ❌ **필요** |

**Step 4: 구현 (2-3시간)**
| 기능 | 설명 | 우선순위 | 현황 |
|-----|------|---------|------|
| `/implement-assisted` | 단계별 AI 가이드 구현 | 🔴 Essential | ❌ **필요** |
| 코드 템플릿 | 복사-붙여넣기 가능한 기본 코드 | 🔴 Essential | ❌ **필요** |
| 에러 해석 | "이 에러는 이렇게 해결하세요" | 🔴 Essential | ❌ **필요** |

**Step 5: 완료 & 배포 (30분)**
| 기능 | 설명 | 우선순위 | 현황 |
|-----|------|---------|------|
| `/test-run` | 모든 테스트 자동 실행 | 🔴 Essential | ❌ **필요** |
| 테스트 결과 리포트 | 통과/실패 명확한 표시 | 🟡 Important | ❌ **필요** |
| `/git-commit` | 자동 커밋 메시지 생성 | 🟡 Important | ✅ 있음 |

### 추가: 심리적 고관여 기능

| 기능 | 설명 | 우선순위 |
|-----|------|---------|
| **Progress Dashboard** | "지금 50% 진행 중" 시각화 | 🔴 Essential |
| **Week-by-week Checklist** | 매주 달성 항목 체크 | 🔴 Essential |
| **Quick Win Signals** | 각 단계 완료 시 축하 메시지 | 🟡 Important |
| **Weekly Review Auto-generation** | 주간 정리 자동 생성 | 🟡 Important |
| **Time Tracking** | 각 단계 소요 시간 기록 | 🟢 Nice-to-have |

---

## 2️⃣ Lee (마케팅 배경) - 필요 기능

### 특성 요약
- **핵심 이슈**: 데이터 정확성, 확장 가능성
- **솔루션**: 이해할 수 있는 구조 + 검증 로직

### Userflow: 데이터 수집 & 분석 자동화

| Step | 기능 | 설명 | 우선순위 | 현황 |
|-----|------|------|---------|------|
| 1 | `/clarify` + 데이터 타입 분류 | Task + 데이터 형식 지정 | 🔴 Essential | ❌ **필요** |
| 2 | `/design` + 데이터 흐름 다이어그램 | 데이터 수집→정제→분석 흐름 | 🔴 Essential | ❌ **필요** |
| 2-1 | API 문서 링크 | 사용할 API 공식 문서 | 🟡 Important | ❌ **필요** |
| 2-2 | 데이터 검증 설계 | "어떻게 정확성을 확인할까?" | 🔴 Essential | ❌ **필요** |
| 3 | `/test-generator` + 데이터 테스트 | 샘플 데이터로 테스트 케이스 | 🔴 Essential | ❌ **필요** |
| 4 | `/implement` + 모듈화 구조 | 각 부분(수집/정제/분석)이 독립적 | 🟡 Important | ❌ **필요** |
| 4-1 | 에러 로깅 | 뭐가 실패했는지 추적 | 🟡 Important | ❌ **필요** |
| 5 | `/schedule-setup` | 크론잡 설정 가이드 | 🔴 Essential | ❌ **필요** |
| 5-1 | 결과 알림 설정 | 이메일/슬랙/노션 연동 | 🟡 Important | ❌ **필요** |

### 추가: 데이터 중심 기능

| 기능 | 설명 | 우선순위 |
|-----|------|---------|
| **Data Schema Validator** | "수집된 데이터가 정확한가?" 체크 | 🔴 Essential |
| **API Testing Playground** | 실제 API 호출 테스트 가능 | 🟡 Important |
| **Data Sample Preview** | "처음 100개 데이터 이렇게 생겼어" 보여주기 | 🟡 Important |
| **Expansion Guide** | "다른 데이터소스 추가하는 방법" | 🟡 Important |
| **Monitoring Dashboard** | "얼마나 많은 데이터가 수집됐나?" | 🟢 Nice-to-have |

---

## 3️⃣ Park (학생/취준생) - 필요 기능

### 특성 요약
- **핵심 이슈**: 포트폴리오 가치, 배포 경험
- **솔루션**: 전문적인 결과 + 배포 단순화

### Userflow: 포트폴리오 프로젝트 구현

| Step | 기능 | 설명 | 우선순위 | 현황 |
|-----|------|------|---------|------|
| 1 | `/clarify` + 포트폴리오 맥락 | "이걸 이력서에 어떻게 설명할까?" 포함 | 🟡 Important | ❌ **필요** |
| 2 | `/design` + 코드 구조 | 프로 같은 구조 (모듈화, 클래스 등) | 🔴 Essential | ❌ **필요** |
| 3 | `/test-generator` + pytest 예제 | 전문적인 테스트 코드 | 🟡 Important | ❌ **필요** |
| 4 | `/implement` + 코드 품질 체크 | Lint, 포맷팅 자동 | 🟡 Important | ❌ **필요** |
| 5 | `/deploy` 명령어 | 무료 플랫폼(Vercel, PythonAnywhere)으로 배포 | 🔴 Essential | ❌ **필요** |
| 5-1 | Docker 템플릿 | 배포 가능한 Docker 파일 자동 생성 | 🟡 Important | ❌ **필요** |
| 6 | `/portfolio-docs` | README, 사용 설명서 자동 생성 | 🔴 Essential | ❌ **필요** |
| 7 | `/git-setup` | 포트폴리오용 GitHub 설정 | 🟡 Important | ❌ **필요** |

### 추가: 포트폴리오 & 배포 기능

| 기능 | 설명 | 우선순위 |
|-----|------|---------|
| **Portfolio Checklist** | 각 단계마다 "포트폴리오 가치" 체크 | 🔴 Essential |
| **README Generator** | 프로 같은 README 자동 생성 | 🟡 Important |
| **Code Quality Report** | "코드 품질 점수" 표시 | 🟡 Important |
| **One-Click Deploy** | 1개 명령어로 배포 완료 | 🔴 Essential |
| **Deployment URL** | 배포 후 실제 접속 가능한 URL | 🟡 Important |
| **Interview Prep Guide** | "면접에서 이렇게 설명하세요" 팁 | 🟡 Important |
| **Blog Writing Guide** | 프로젝트 블로그 포스팅 가이드 | 🟢 Nice-to-have |

---

## 4️⃣ Choi (숙련 개발자) - 필요 기능

### 특성 요약
- **핵심 이슈**: 제품화, 비즈니스 모델, 성능
- **솔루션**: 고도화된 아키텍처 + 사업성 검증

### Userflow: 판매 가능한 Skill 개발

| Step | 기능 | 설명 | 우선순위 | 현황 |
|-----|------|------|---------|------|
| 1 | `/market-research` | 타겟 고객/경쟁사 분석 | 🔴 Essential | ❌ **필요** |
| 1-1 | `/clarify` + 비즈니스 가치 | "이걸 누가 사나? 얼마에?" | 🔴 Essential | ❌ **필요** |
| 2 | `/design` + 아키텍처 | 확장성 있는 아키텍처 + 성능 요구사항 | 🔴 Essential | ❌ **필요** |
| 2-1 | 성능 벤치마크 설계 | "얼마나 빨라야 하나?" 정의 | 🔴 Essential | ❌ **필요** |
| 3 | `/implement` + 엔터프라이즈 코드 | 프로덕션 레벨 코드 | 🔴 Essential | ❌ **필요** |
| 3-1 | 모니터링/로깅 자동 추가 | 프로덕션 모니터링 코드 | 🟡 Important | ❌ **필요** |
| 4 | `/deploy-production` | CI/CD 파이프라인 자동 구성 | 🔴 Essential | ❌ **필요** |
| 4-1 | 다중 리전 배포 | AWS/GCP 다중 리전 | 🟡 Important | ❌ **필요** |
| 5 | `/beta-launch` | Beta 테스터 모집/관리 | 🔴 Essential | ❌ **필요** |
| 5-1 | 피드백 수집 자동화 | 고객 피드백 시스템 | 🟡 Important | ❌ **필요** |
| 6 | `/pricing-strategy` | 가격 책정 가이드 | 🔴 Essential | ❌ **필요** |
| 6-1 | `/go-to-market` | 마케팅/출시 전략 | 🟡 Important | ❌ **필요** |

### 추가: 엔터프라이즈 & 비즈니스 기능

| 기능 | 설명 | 우선순위 |
|-----|------|---------|
| **Architecture Review** | 아키텍처 검토 및 피드백 | 🔴 Essential |
| **Performance Benchmarking** | 성능 테스트 자동화 | 🔴 Essential |
| **Production Monitoring Setup** | 프로덕션 모니터링 자동 구성 | 🔴 Essential |
| **CI/CD Pipeline Template** | GitHub Actions/GitLab CI 자동 구성 | 🟡 Important |
| **Security Audit** | 보안 체크리스트 | 🟡 Important |
| **API Documentation Auto-generation** | Swagger/OpenAPI 자동 생성 | 🟡 Important |
| **Beta User Management** | Beta 테스터 관리 시스템 | 🟡 Important |
| **Pricing Calculator** | 수익화 시나리오 계산기 | 🟢 Nice-to-have |
| **Marketing Toolkit** | Product Hunt, Indie Hackers 출시 가이드 | 🟢 Nice-to-have |

---

## 📊 교차 분석: 모든 Persona에 공통으로 필요한 기능

### Tier 1: 모두 필수
| 기능 | 이유 |
|-----|------|
| `/clarify` | 모든 Persona가 먼저 문제를 명확해야 함 |
| `/design` | 모든 Persona가 설계 단계 필요 |
| `/implement` (또는 `/implement-assisted`) | 모든 Persona가 구현해야 함 |
| `/test-run` | 모든 Persona가 동작 확인해야 함 |
| `/git-commit` | 모든 Persona가 진행사항 기록해야 함 |

### Tier 2: 대부분 필요
| 기능 | 필요한 Persona | 이유 |
|-----|---------|------|
| `/test-generator` | Kim, Lee, Park | 테스트 코드 생성 |
| Progress Dashboard | Kim, Park | 진도 시각화 |
| Weekly Review | Kim, Park | 주간 정리 |
| Documentation Auto-gen | Park, Choi | 문서화 자동화 |

### Tier 3: 특정 Persona만
| 기능 | 필요한 Persona | 이유 |
|-----|---------|------|
| `/schedule-setup` | Lee, Choi | 정기 실행 설정 |
| `/deploy` (무료) | Park | 배포 |
| `/market-research` | Choi | 시장 검증 |
| `/pricing-strategy` | Choi | 수익화 |

---

## 🎯 구현 우선순위 (전체)

### Phase 1: MVP Commands (필수)
1. ✅ `/clarify` - 이미 있음
2. ✅ `/design` - 필요함 ← **우선순위 1**
3. ✅ `/implement-assisted` - 필요함 ← **우선순위 2**
4. ✅ `/test-generator` - 필요함 ← **우선순위 3**
5. ✅ `/test-run` - 필요함 ← **우선순위 4**

### Phase 2: 고관여 기능
6. 🟡 **Progress Dashboard** - 우선순위 5
7. 🟡 **Weekly Review** - 우선순위 6
8. 🟡 **Quick Win Signals** - 우선순위 7

### Phase 3: 특화 기능
9. 🟢 `/deploy` (무료 플랫폼) - Park용
10. 🟢 `/schedule-setup` - Lee/Choi용
11. 🟢 `/market-research` - Choi용

---

## 📝 각 기능의 상세 정의

### `/design` 명령어 (Tier 1 - 우선순위 1)

**목표**: 명확화된 Task를 실행 가능한 설계 문서로 변환

**입력**:
- Clarify 단계에서 생성된 Task 문서

**출력**:
- 설계 문서 (마크다운)
  - Input 명확히 (뭘 받는가?)
  - Process 단계별 (어떤 단계로 처리하나?)
  - Output 명확히 (뭘 내보내는가?)
  - Dependencies (뭐가 필요한가? 라이브러리, API 등)
  - Flow 다이어그램

**실행 방식**:
```bash
/design
```

**예상 결과**:
```
__test__/{YYYYMMDD}_{title}/design.md
```

**Kim이 보는 모습**:
```
┌─────────────────┐
│ 입력: 음성 파일  │
└────────┬────────┘
         │
    ┌────▼────┐
    │Whisper  │ (음성→텍스트)
    └────┬────┘
         │
    ┌────▼─────┐
    │ Claude   │ (텍스트→요약)
    └────┬─────┘
         │
    ┌────▼──────────┐
    │출력: 마크다운  │
    └───────────────┘
```

---

### `/implement-assisted` 명령어 (Tier 1 - 우선순위 2)

**목표**: 입문자도 따라할 수 있는 단계별 구현 가이드

**입력**:
- 설계 문서

**출력**:
- 구현 코드 (파이썬)
- 단계별 가이드
- 에러 해결 가이드

**실행 방식**:
```bash
/implement-assisted
```

**진행 방식** (Kim):
```
Step 1: 필요한 라이브러리 설치
→ 명령어 제공 (복사-붙여넣기)
→ 예상 결과 (설치 완료 메시지)

Step 2: API 키 설정
→ 어디서 API 키를 얻는지 (링크 제공)
→ 어디에 넣을 건지 (.env.local)
→ 확인 명령어

Step 3: 메인 함수 작성
→ 템플릿 코드 제공
→ 주석으로 설명
→ 복사-붙여넣기 가능

Step 4: 테스트 실행
→ 테스트 실행 명령어
→ 예상 결과 ("SUCCESS" 메시지)
```

---

### `/test-generator` 명령어 (Tier 1 - 우선순위 3)

**목표**: 설계 문서 기반 자동 테스트 생성

**입력**:
- 설계 문서

**출력**:
- 테스트 파일 (pytest 기반)
- 테스트 샘플 데이터

**예시** (Kim의 음성→텍스트):
```python
# test_meeting_notes.py

def test_valid_audio_file():
    """정상 음성 파일 테스트"""
    result = transcribe("sample.mp3")
    assert result is not None
    assert isinstance(result, str)

def test_invalid_file_format():
    """잘못된 형식 파일 테스트"""
    with pytest.raises(ValueError):
        transcribe("file.txt")

def test_empty_file():
    """빈 파일 테스트"""
    with pytest.raises(ValueError):
        transcribe("empty.mp3")
```

---

### Progress Dashboard (UI Feature - 우선순위 5)

**목표**: 현재 진행상황을 매 세션마다 시각화

**표시 내용**:
```
📊 Progress Dashboard

Week 1/4 (25%)
├─ Setup ✅ (완료)
├─ Clarify 🚀 (진행 중 - 60%)
└─ Design ⏳ (예정)

Skills Completed: 0/3 (0%)
Total Time: 2h 30m / 20h 예상 (12.5%)

✨ Next: Step 2 설계 진행 (예상 1시간)
```

**어디에 표시**:
- CLAUDE.md 자동 업데이트
- 각 명령어 실행 시 상단 표시
- `/progress` 명령어로 언제든 확인

---

## 🎯 최종 정리: 필요한 명령어 목록

### 필수 (Phase 1)
- [ ] `/design` - 자동화 설계 생성
- [ ] `/implement-assisted` - 단계별 구현 가이드
- [ ] `/test-generator` - 테스트 템플릿 자동 생성
- [ ] `/test-run` - 자동 테스트 실행

### 중요 (Phase 2)
- [ ] `/progress` - 진도 대시보드 표시
- [ ] `/weekly-review` - 주간 리뷰 자동 생성
- [ ] `/schedule-setup` - 정기 실행 설정 (크론잡)

### 선택 (Phase 3)
- [ ] `/deploy` - 무료 플랫폼 배포
- [ ] `/market-research` - 시장 조사
- [ ] `/pricing-strategy` - 수익화 전략

---

## 📋 다음 단계

1. **Usecase 문서 작성** (`_systems/usecase/`)
   - Kim: 3개 Usecase (미팅정리, 이메일분류, 영수증정리)
   - Lee: 3개 Usecase (SNS수집, 감정분석, 리포트생성)
   - Park: 3개 Usecase (음성변환, 크롤링, 웹배포)
   - Choi: 3개 Usecase (API오케스트레이션, AI처리, ETL)

2. **Userflow 문서 작성** (`_systems/userflow/`)
   - 각 Usecase별로 상세한 단계별 흐름 정의
   - 정확한 명령어와 예상 결과 기술

3. **명령어 구현**
   - Phase 1 명령어부터 순서대로 구현
   - 각 명령어별 테스트 코드 작성

4. **UI/UX 개선**
   - Progress Dashboard 구현
   - 각 Persona별 가이드 화면 맞춤

---

## 🔗 관련 문서

- Persona: `_systems/persona/`
- Usecase: `_systems/usecase/README.md`
- Userflow: `_systems/userflow/README.md`
