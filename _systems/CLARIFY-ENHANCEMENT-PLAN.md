# /clarify 명령어 개선 계획 - Memory 활용 & 동적 Usecase

> Setup-workspace에서 생성된 Memory를 기반으로 `/clarify` 명령어를 개선하여
> **Usecase 자동 감지, 생성, 매칭**을 수행

---

## 🎯 목표

```
현재 상태:
/clarify "미팅 음성파일을 텍스트로..."
  ↓
기본 Task 명확화만 수행
  ↓
Usecase는 사용자가 직접 찾거나 만들어야 함

개선 후:
/clarify "미팅 음성파일을 텍스트로..."
  ↓
1. Memory 로드 (Kim 타입이라는 거 파악)
  ↓
2. Kim의 추천 Usecase 로드 (01-daily-meeting-notes 등)
  ↓
3. 입력과 기존 Usecase 매칭
  ↓
4. 기존 Usecase면 사용, 새것이면 생성
  ↓
5. Memory & CLAUDE.md 자동 업데이트
```

---

## 🔧 상세 구현 플로우

### Phase 1: Memory 로드

```python
def clarify(user_input):
    # Step 1: CLAUDE.md에서 사용자명 파악
    username = load_username_from_claude()
    # → "김철수"

    # Step 2: Memory 파일 찾기
    memory_path = find_memory_file(username)
    # → ".claude/memory/user-lee-kim-chul-soo.json"

    # Step 3: Memory 로드
    memory = load_json(memory_path)
    # {
    #   "name": "김철수",
    #   "persona": "Lee",
    #   "repeated_tasks": ["SNS 수집", "분석"],
    #   "tech_level": "intermediate",
    #   ...
    # }

    print(f"✨ {memory['name']}님의 정보를 로드했습니다!")
    print(f"📌 Persona: {memory['persona']}")
```

### Phase 2: 해당 Persona의 Usecase 로드

```python
    # Step 4: Persona 기반 Usecase 디렉토리 스캔
    persona = memory['persona']  # "Lee"
    usecase_dir = f"_systems/usecase/{persona.lower()}-xxx/"
    # → "_systems/usecase/lee-creative/"

    # Step 5: 모든 Usecase 마크다운 파일 로드
    existing_usecases = load_all_usecases(usecase_dir)
    # [
    #   {
    #     "id": "01-sns-data-collection",
    #     "title": "SNS 게시물 데이터 자동 수집",
    #     "description": "인스타그램 해시태그 검색...",
    #     "keywords": ["SNS", "데이터", "수집", "인스타"]
    #   },
    #   {
    #     "id": "02-sentiment-analysis",
    #     "title": "고객 피드백 감정 분석",
    #     ...
    #   },
    #   ...
    # ]

    print(f"\n📚 {memory['persona']} 타입의 추천 Usecase:")
    for uc in existing_usecases:
        print(f"   {uc['id']}: {uc['title']}")
```

### Phase 3: 사용자 입력과 Usecase 매칭

```python
    # Step 6: 사용자 입력 분석
    print(f"\n🔍 당신의 입력 분석 중...")
    print(f"   '{user_input}'")

    # Step 7: 기존 Usecase와 매칭 시도
    matched = match_usecase(
        user_input=user_input,
        existing_usecases=existing_usecases,
        threshold=0.7  # 70% 유사도 이상이면 매칭
    )

    if matched:
        # 기존 Usecase 발견!
        print(f"\n✅ 기존 Usecase를 찾았습니다!")
        print(f"   📄 {matched['title']}")
        print(f"   📝 {matched['description'][:100]}...")
        print(f"\n   이거 맞나요?")
        print(f"   1. 네, 맞아요!")
        print(f"   2. 아니에요, 새로 만들어야 해요")
        print(f"   3. 다른 Usecase도 보고 싶어요")

        user_choice = input()

        if user_choice == "1":
            # 기존 Usecase 사용
            return handle_existing_usecase(memory, matched)
        elif user_choice == "2":
            # 새 Usecase 생성
            return handle_new_usecase(memory, user_input)
        else:
            # 모든 Usecase 목록 제시
            return show_all_usecases(memory, existing_usecases)

    else:
        # 새로운 Usecase!
        print(f"\n🆕 새로운 케이스 같은데요!")
        print(f"   지금까지의 기록:")
        for uc in existing_usecases:
            print(f"   • {uc['title']}")
        print(f"\n   당신의 '{user_input}'은 다른 케이스군요.")
        print(f"\n   새로 추가할까요?")
        print(f"   1. 네, 추가합시다!")
        print(f"   2. 아니에요")

        if input() == "1":
            return handle_new_usecase(memory, user_input)
```

---

### Phase 4: 기존 Usecase 처리

```python
def handle_existing_usecase(memory, matched_usecase):
    """기존 Usecase를 선택한 경우"""

    print(f"\n✨ {matched_usecase['title']} 시작합니다!")
    print(f"   Usecase ID: {matched_usecase['id']}")

    # Step 8: Memory 업데이트
    memory['status']['current_usecase'] = matched_usecase['id']
    memory['updated_at'] = now()

    # Step 9: Memory 저장
    save_json(memory_path, memory)

    # Step 10: 기본 Clarify 진행 (기존 방식)
    # → Task 명확화 프롬프트 실행

    # Step 11: CLAUDE.md 업데이트
    update_claude_md(
        current_usecase=matched_usecase['id'],
        userflow_link=f"_systems/userflow/{persona.lower()}-xxx/{matched_usecase['id']}/flow.md"
    )

    print(f"\n📚 Userflow 가이드: {userflow_link}")
    print(f"💡 Usecase 설명: _systems/usecase/{matched_usecase['id']}.md")
```

### Phase 5: 새 Usecase 생성

```python
def handle_new_usecase(memory, user_input):
    """새로운 Usecase를 생성하는 경우"""

    print(f"\n🆕 새로운 Usecase를 생성합니다!")

    # Step 12: 기존 Usecase ID 중 다음 번호 찾기
    existing_ids = [uc['id'] for uc in existing_usecases]
    # ["01-sns-data-collection", "02-sentiment-analysis"]
    next_id = get_next_usecase_id(existing_ids)
    # → "03-xxx"

    # Step 13: Usecase 마크다운 템플릿 생성
    usecase_content = generate_usecase_from_template(
        id=next_id,
        user_input=user_input,
        persona=memory['persona'],
        tech_level=memory['tech_level']
    )
    # → 마크다운 텍스트

    # Step 14: 파일 저장
    usecase_path = f"_systems/usecase/{persona.lower()}-xxx/{next_id}.md"
    save_file(usecase_path, usecase_content)

    # Step 15: Userflow 기본 템플릿도 생성
    flow_content = generate_flow_template(next_id, persona)
    flow_path = f"_systems/userflow/{persona.lower()}-xxx/{next_id}/flow.md"
    save_file(flow_path, flow_content)

    print(f"\n✅ 새 Usecase 생성 완료!")
    print(f"   📄 {usecase_path}")
    print(f"   🔗 {flow_path}")

    # Step 16: Memory 업데이트
    memory['status']['current_usecase'] = next_id
    memory['updated_at'] = now()
    save_json(memory_path, memory)

    # Step 17: CLAUDE.md 업데이트
    update_claude_md(current_usecase=next_id)

    # Step 18: 기본 Clarify 진행
    # → Task 명확화 프롬프트 실행
```

---

## 📂 필요한 변경 사항

### 1. `/clarify` 명령어 수정

**현재:**
```markdown
---
description: 반복되는 업무를 자동화 Task로 변환
---

# Clarify...
```

**개선 후:**
```markdown
---
description: 당신의 Persona 기반 Usecase 자동 감지 + 명확화
argument-hint: <반복 업무 또는 문제 상황 설명>
related: _systems/persona, _systems/usecase, .claude/memory
---

# Clarify - 당신의 상황 이해하기

## 기능
1. Memory 로드 (당신의 Persona & 정보)
2. 기존 Usecase 로드 (추천 케이스)
3. 입력과 매칭 (기존 vs 새로운)
4. Usecase 생성 (필요시 자동)
5. Memory & CLAUDE.md 업데이트

## 사용법

당신의 상황을 자유롭게 설명해주세요:

```bash
/clarify "매일 미팅 음성파일을 텍스트로 바꾸는데 30분 걸려"
/clarify "인스타 팔로워들의 댓글을 자동으로 수집하고 싶어"
/clarify "이미지에서 텍스트를 자동으로 추출하려고"
```
```

---

### 2. 필요한 Utility 함수

```python
# Memory 관련
def find_memory_file(username: str) -> str:
    """사용자명으로 Memory 파일 경로 찾기"""
    pass

def load_json(path: str) -> dict:
    """JSON 파일 로드"""
    pass

def save_json(path: str, data: dict) -> None:
    """JSON 파일 저장"""
    pass

# Usecase 관련
def load_all_usecases(persona_dir: str) -> list:
    """해당 Persona의 모든 Usecase 로드"""
    pass

def match_usecase(
    user_input: str,
    usecases: list,
    threshold: float = 0.7
) -> dict or None:
    """사용자 입력과 기존 Usecase 매칭"""
    pass

def get_next_usecase_id(existing_ids: list) -> str:
    """다음 Usecase ID 생성 (01 → 02 → 03)"""
    pass

# 생성 관련
def generate_usecase_from_template(
    id: str,
    user_input: str,
    persona: str,
    tech_level: str
) -> str:
    """Usecase 마크다운 자동 생성"""
    pass

def generate_flow_template(id: str, persona: str) -> str:
    """Flow 마크다운 자동 생성"""
    pass

# CLAUDE.md 관련
def update_claude_md(current_usecase: str) -> None:
    """CLAUDE.md 업데이트"""
    pass
```

---

### 3. Usecase 마크다운 Template

**위치:** `_systems/templates/usecase-template.md`

```markdown
# {Title}

## 📌 기본정보
- **ID**: {ID}
- **Persona**: {Persona}
- **우선순위**: {Priority}
- **난이도**: {Difficulty}
- **예상 기간**: {Duration}

## 🎯 목표
{Goal - 사용자 입력 기반으로 자동 생성}

## 📊 Current State
{Current - 자유형식 입력 정리}

## 🎯 Desired State
{Desired - 자동 생성 또는 사용자 입력}

## ✅ Success Criteria
- 측정 가능한 지표 1
- 측정 가능한 지표 2

## 🔗 Userflow
_systems/userflow/{persona}/{id}/flow.md
```

**Flow Template**: `_systems/templates/flow-template.md`

```markdown
# {Title} - Userflow

## 📌 Usecase 요약
- 제목: {Title}
- 대상: {Persona}
- 난이도: {Difficulty}
- 소요 시간: {Duration}

## 🎯 전체 Flow

```
┌─ Step 1: 문제 명확화
│  └─ /clarify
│
├─ Step 2: 자동화 설계
│  └─ /design
│
├─ Step 3: 테스트 템플릿
│  └─ /test-generator
│
├─ Step 4: 구현
│  └─ /implement
│
└─ Step 5: 배포
   └─ /git-commit
```

## 📋 Step별 상세

### Step 1: 문제 명확화 (30분)
명령어: /clarify ...
예상 결과: ...

### Step 2: ...
```

---

## 🔄 매칭 알고리즘

### 유사도 점수 계산

```python
def calculate_similarity(user_input, usecase):
    """사용자 입력과 Usecase의 유사도 계산"""

    score = 0

    # 1. 키워드 매칭 (60%)
    user_keywords = extract_keywords(user_input)
    usecase_keywords = usecase['keywords']
    matching_keywords = len(set(user_keywords) & set(usecase_keywords))
    total_keywords = len(set(user_keywords) | set(usecase_keywords))
    keyword_score = matching_keywords / total_keywords * 60

    # 2. 제목 유사도 (20%)
    title_similarity = fuzzy_match(user_input, usecase['title'])
    title_score = title_similarity * 20

    # 3. 설명 유사도 (20%)
    desc_similarity = fuzzy_match(user_input, usecase['description'])
    desc_score = desc_similarity * 20

    total_score = keyword_score + title_score + desc_score
    return total_score / 100
```

### 임계값 설정

```
점수 >= 0.7: 기존 Usecase와 매칭
점수 < 0.7: 새로운 Usecase 생성
```

---

## 🎯 향후 확장

### 즉시 (Phase 1)
- [ ] Memory 로드 + Usecase 매칭
- [ ] 새 Usecase 자동 생성
- [ ] Memory 자동 업데이트

### 단기 (Phase 2)
- [ ] 유사도 점수 개선 (NLP)
- [ ] Usecase 추천 개선
- [ ] 매칭 실패 디버깅 로그

### 장기 (Phase 3)
- [ ] 멀티 Usecase 동시 처리
- [ ] 자동 Persona 조정
- [ ] 사용자 피드백 반영

---

이 플로우로 `/clarify`가 단순 "명확화"에서 **지능형 자동화 어시스턴트**로 변화합니다.
