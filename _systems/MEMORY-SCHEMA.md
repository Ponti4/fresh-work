# Memory Schema - 사용자 정보 저장 구조

> Setup-workspace에서 자동으로 생성되는 Memory(JSON) 파일의 스키마 정의

---

## 📂 위치

```
.claude/memory/
└── user-{persona-type}-{name-slug}.json
```

**예시:**
- `user-lee-kim-chul-soo.json`
- `user-kim-park-ji-won.json`
- `user-choi-john-doe.json`

---

## 📋 JSON Schema

```json
{
  "user_id": "lee-kim-chul-soo-20251231",

  // 기본 정보
  "name": "김철수",
  "persona": "Lee",
  "persona_description": "마케팅/데이터 중심",

  // 직업 & 배경
  "job_title": "마케팅 프리랜서",
  "job_context": "성장 해킹, SNS 마케팅",
  "industry": "e-commerce",

  // 반복 업무
  "repeated_tasks": [
    "SNS 데이터 수집",
    "고객 피드백 분석",
    "성과 리포트 작성"
  ],

  // 불편함 & 동기
  "main_pain_point": "시간이 너무 오래 걸림",
  "secondary_pain_points": [
    "정확도 낮음",
    "확장성 부족"
  ],
  "motivation": "데이터 자동화로 분석에 집중하고 싶음",

  // 기술 & 경험
  "tech_level": "intermediate",  // beginner, intermediate, advanced
  "tech_experience": {
    "python": "basic",  // none, basic, intermediate, advanced
    "api": "intermediate",
    "databases": "basic",
    "data_analysis": "intermediate"
  },

  // 목표
  "goal_4weeks": "데이터 자동화 Skill 3개 완성",
  "first_challenge": "SNS 게시물 데이터 자동 수집",
  "expected_impact": "주 10시간 절약",

  // 환경 정보
  "system_info": {
    "os": "Windows",
    "os_version": "11 Pro",
    "cpu": "Intel Core i7-12700K",
    "ram": "16GB",
    "gpu": "NVIDIA RTX 3080",
    "python_version": "3.11.5"
  },

  // 진행 상황
  "status": {
    "setup_completed": true,
    "current_week": 1,
    "current_usecase": null,  // "01-daily-meeting-notes" 등
    "usecases_completed": [],
    "last_action": "setup_workspace"
  },

  // 타임스탬프
  "created_at": "2025-12-31T10:30:00Z",
  "updated_at": "2025-12-31T10:30:00Z",
  "setup_completed_at": "2025-12-31T10:35:00Z"
}
```

---

## 🔄 필드별 설명

### Persona 관련
```json
{
  "persona": "Lee",  // Kim / Lee / Park / Choi
  "persona_description": "마케팅/데이터 중심"
}
```

**사용처:**
- `/clarify`에서 Usecase 추천
- `/design`에서 난이도 결정
- `/implement`에서 가이드 수준 결정

### 기술 수준
```json
{
  "tech_level": "intermediate",  // 전체 난이도
  "tech_experience": {
    "python": "basic",
    "api": "intermediate",
    "databases": "basic",
    "data_analysis": "intermediate"
  }
}
```

**매핑:**
- `beginner` → `/implement-assisted` 사용
- `intermediate` → `/implement` 직접 가능
- `advanced` → `/implement` + 고도화 가능

### Status 추적
```json
{
  "status": {
    "current_week": 1,
    "current_usecase": "01-sns-data-collection",
    "usecases_completed": [],
    "last_action": "/clarify"
  }
}
```

**용도:**
- 각 명령어에서 "지금 뭘 하고 있나?" 파악
- Progress 계산
- 다음 Step 제시

---

## 📝 자동 업데이트 시점

### Setup-workspace 완료 후
```json
{
  "created_at": "2025-12-31T10:30:00Z",
  "setup_completed_at": "2025-12-31T10:35:00Z"
}
```

### /clarify 실행 후
```json
{
  "status": {
    "current_usecase": "01-sns-data-collection"
  },
  "updated_at": "2025-12-31T11:05:00Z"
}
```

### /design, /implement 등 실행 후
```json
{
  "status": {
    "last_action": "/design"
  },
  "updated_at": "2025-12-31T11:35:00Z"
}
```

### Usecase 완료 후
```json
{
  "status": {
    "usecases_completed": [
      "01-sns-data-collection"
    ],
    "current_usecase": "02-sentiment-analysis"
  },
  "updated_at": "2026-01-02T10:30:00Z"
}
```

---

## 🔧 Memory 로드 & 사용

### /clarify에서 로드
```python
# Step 1: Memory 파일 찾기
memory_path = find_memory_file(username)

# Step 2: 파일 로드
memory = load_json(memory_path)

# Step 3: Persona 기반 Usecase 추천
persona = memory['persona']
repeated_tasks = memory['repeated_tasks']
recommended_usecases = get_usecases(persona, repeated_tasks)

# Step 4: 사용자 입력과 매칭
matched = match_usecase(user_input, recommended_usecases)

if matched:
    # 기존 Usecase 사용
    memory['status']['current_usecase'] = matched
else:
    # 새 Usecase 생성 + Memory 업데이트
    new_usecase = create_usecase(...)
    memory['status']['current_usecase'] = new_usecase

# Step 5: Memory 저장
save_json(memory_path, memory)
```

### /design에서 로드
```python
# Memory 로드
memory = load_memory()

# 난이도 결정
difficulty = decide_difficulty(memory['tech_level'])

# 설계 가이드 선택
if difficulty == 'beginner':
    template = basic_design_template
else:
    template = advanced_design_template

# 설계 생성
design = generate_design(template, difficulty)
```

---

## 💾 Memory 수정 가이드

사용자가 직접 수정할 수 있는 필드:

```json
{
  "job_context": "변경 가능",
  "repeated_tasks": "추가/제거 가능",
  "motivation": "변경 가능",
  "first_challenge": "변경 가능"
}
```

수정 불가 필드 (자동 관리):

```json
{
  "user_id": "생성 후 고정",
  "created_at": "생성 후 고정",
  "status": "자동 업데이트"
}
```

---

## 🔐 파일 보안

- **위치**: `.claude/memory/` (`.gitignore`에 등록)
- **형식**: JSON (평문)
- **접근**: 사용자 / Claude Code만 접근 가능
- **백업**: Git에 포함 안 됨

---

## 📊 Memory 활용 예시

### 예시 1: Lee 타입 (마케팅)
```json
{
  "persona": "Lee",
  "tech_level": "intermediate",
  "repeated_tasks": ["SNS 데이터 수집", "분석"],
  "main_pain_point": "시간 낭비",
  "first_challenge": "SNS 게시물 데이터 자동 수집"
}
```

**활용:**
- `/clarify` → "SNS 데이터 자동 수집" Usecase 추천
- `/design` → "데이터 검증" 강조
- `/implement` → 모듈화 구조 강조

### 예시 2: Kim 타입 (비전공)
```json
{
  "persona": "Kim",
  "tech_level": "beginner",
  "repeated_tasks": ["미팅 정리", "이메일 분류"],
  "main_pain_point": "러닝커브",
  "first_challenge": "일일 미팅 노트 정리"
}
```

**활용:**
- `/clarify` → "미팅 정리" Usecase 추천
- `/design` → 간단한 설계 (비전공자용)
- `/implement` → `/implement-assisted` 사용

---

## 🚀 확장 가능성

### 새로운 필드 추가 (예상)
```json
{
  "preferences": {
    "communication": "korean",
    "learning_style": "hands-on",
    "output_format": "markdown"
  },

  "progress_metrics": {
    "total_hours_spent": 12.5,
    "time_saved_estimated": 8.0,
    "satisfaction_score": 4.5
  }
}
```

### API 연동 (예상)
```json
{
  "api_keys": {
    "openai": "sk-...",
    "google": "AIzaSy...",
    "stripe": "sk_live_..."
  }
}
```

---

## ✅ 검증 체크리스트

Memory 파일 생성 후 확인사항:

- [ ] JSON 형식 유효성
- [ ] 필수 필드 모두 포함
- [ ] Persona 값 유효 (Kim/Lee/Park/Choi)
- [ ] tech_level 값 유효 (beginner/intermediate/advanced)
- [ ] 타임스탬프 형식 ISO 8601
- [ ] 파일명 형식 `user-{persona}-{slug}.json`

---

이 구조를 바탕으로 모든 명령어가 자동으로 Memory를 로드하고 업데이트합니다.
