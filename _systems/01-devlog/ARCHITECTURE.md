# 시스템 아키텍처

## 개요

```
┌─────────────────────────────────────────────────────────────────┐
│                   User Input (CLI)                              │
│  ./devlog-wrapper.sh [--config] [--dry-run] [--from] [--to]   │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              devlog-wrapper.sh (Bash Wrapper)                   │
│  ├─ 인자 파싱                                                   │
│  ├─ 의존성 확인 (Python, PyYAML)                                │
│  ├─ 설정 파일 검증                                              │
│  └─ Python 스크립트 호출                                        │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│      unified_devlog_generator.py (Python 메인)                 │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 1. DevlogConfig (설정 로드)                             │   │
│  │    ├─ YAML 파일 읽기                                   │   │
│  │    └─ 설정값 조회 API 제공                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 2. SessionParser (세션 파싱)                            │   │
│  │    ├─ parse_claude_code_sessions()                      │   │
│  │    │  ├─ 세션 디렉토리 탐색                             │   │
│  │    │  ├─ .jsonl 파일 수집                               │   │
│  │    │  └─ JSON Lines 형식 파싱                           │   │
│  │    ├─ parse_antigravity_sessions()                      │   │
│  │    │  ├─ brain 디렉토리 탐색                            │   │
│  │    │  ├─ conversation_log.md 수집                       │   │
│  │    │  └─ 마크다운 형식 파싱                             │   │
│  │    ├─ parse_vs_code_sessions()  [미지원]               │   │
│  │    └─ parse_aide_sessions()     [미지원]               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 3. SessionMessage (메시지 표현)                         │   │
│  │    ├─ role: user/assistant                              │   │
│  │    ├─ content: 메시지 본문                              │   │
│  │    ├─ timestamp: ISO 8601 형식                          │   │
│  │    └─ tool: 도구명 (Claude Code CLI 등)               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 4. DevlogGenerator (DEVLOG 생성)                        │   │
│  │    ├─ _group_by_date()                                  │   │
│  │    │  └─ 메시지를 날짜별로 그룹핑                       │   │
│  │    ├─ _create_task_section()                            │   │
│  │    │  └─ 사용자/어시스턴트 대화 쌍을 섹션으로 작성      │   │
│  │    └─ generate()                                        │   │
│  │       ├─ 메인 DEVLOG 콘텐츠 생성                        │   │
│  │       ├─ 커밋 히스토리 추가                              │   │
│  │       ├─ 기술 스택 추가                                  │   │
│  │       └─ 주요 기능 추가                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 5. DevlogLogger (로깅)                                  │   │
│  │    ├─ Console 출력                                      │   │
│  │    └─ 파일 저장 (logs/devlog.log)                       │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Output (DEVLOG.md)                            │
│  ├─ 프로젝트 루트: DEVLOG.md (기본)                             │
│  ├─ 또는 --output 옵션으로 지정된 경로                          │
│  └─ Markdown 형식으로 구조화된 개발 로그                        │
└─────────────────────────────────────────────────────────────────┘
```

## 데이터 흐름

### 1단계: 세션 파일 수집

```
Claude Code CLI 세션 디렉토리
~/.claude/projects/
├── -C-Users-devname-project-a/
│   ├── session-1.jsonl   ──┐
│   ├── session-2.jsonl   ──┼─ 프로젝트별 .jsonl 파일 수집
│   └── agent-*.jsonl     ──┘ (agent 제외)
│
└── -C-Users-devname-project-b/
    └── ...
```

### 2단계: 메시지 파싱

```
.jsonl 파일 (JSON Lines 형식)
{"type":"user","message":{...},"timestamp":"2025-12-28T10:00:00Z"}
{"type":"assistant","message":{...},"timestamp":"2025-12-28T10:00:05Z"}
                     ↓
         JSON 파싱 및 검증
                     ↓
           SessionMessage 객체
  ┌────────────────────────────┐
  │ role: "user"               │
  │ content: "질문 내용..."     │
  │ timestamp: datetime        │
  │ tool: "Claude Code CLI"   │
  └────────────────────────────┘
```

### 3단계: 그룹핑 및 정렬

```
[SessionMessage, SessionMessage, ...]
           ↓
   타임스탐프 기반 정렬
           ↓
   날짜별 그룹핑
   {
     "2025-12-25": [msgs...],
     "2025-12-26": [msgs...],
     "2025-12-27": [msgs...],
     ...
   }
```

### 4단계: DEVLOG 생성

```
그룹핑된 메시지들
         ↓
  ┌─ 날짜별 섹션 생성
  ├─ User/Assistant 쌍 감지
  ├─ 작업 섹션 생성
  ├─ 메타정보 추가 (커밋, 스택)
  └─ Markdown 포맷팅
         ↓
    DEVLOG.md (마크다운)
```

## 주요 클래스 및 함수

### DevlogConfig
```python
class DevlogConfig:
    """설정 파일 관리"""

    def __init__(self, config_path: str)
        # YAML 파일 로드

    def get(self, key: str, default: Any = None) -> Any
        # 점 표기법으로 설정값 조회
        # 예: config.get('tools.claude_code_cli.enabled')
```

### SessionParser
```python
class SessionParser:
    """세션 파일 파싱"""

    def parse_claude_code_sessions(session_dir: str) -> List[SessionMessage]
        # Claude Code CLI 세션 파싱

    def parse_antigravity_sessions(brain_dir: str) -> List[SessionMessage]
        # AntiGravity(Gemini) 마크다운 세션 파싱

    def _parse_antigravity_markdown(file_path: Path, session_id: str, base_timestamp: Optional[datetime]) -> List[SessionMessage]
        # 마크다운 파일 파싱 (User/Antigravity 대화 추출)

    def _calculate_message_timestamp(base_timestamp: Optional[datetime], message_index: int) -> datetime
        # 메시지 타임스탐프 추정 (metadata.json의 updatedAt 기반)

    def parse_vs_code_sessions(session_dirs: List[str]) -> List[SessionMessage]
        # VS Code 세션 파싱 (미지원)

    def _parse_jsonl_file(file_path: Path) -> List[SessionMessage]
        # JSONL 파일 파싱

    def _extract_content(message: Any) -> str
        # 메시지에서 텍스트 추출
```

### SessionMessage
```python
class SessionMessage:
    """단일 메시지 표현"""

    role: str           # "user" 또는 "assistant"
    content: str        # 메시지 본문
    timestamp: datetime # 타임스탐프
    tool: str          # 도구명
    session_id: str    # 세션 ID

    def is_valid(min_length: int) -> bool
        # 메시지 유효성 검사
```

### DevlogGenerator
```python
class DevlogGenerator:
    """DEVLOG.md 생성"""

    def generate(messages: List[SessionMessage]) -> str
        # 메인 DEVLOG 콘텐츠 생성

    def _group_by_date(messages: List[SessionMessage]) -> Dict
        # 날짜별 그룹핑

    def _create_task_section(task_num, user_msg, assistant_msgs) -> List[str]
        # 작업 섹션 생성

    def _generate_commit_history() -> List[str]
        # Git 커밋 히스토리 추가

    def _generate_tech_stack() -> List[str]
        # 기술 스택 추가

    def _generate_main_features() -> List[str]
        # 주요 기능 추가
```

## 설정 파일 구조

```yaml
project:
  name: string          # 프로젝트명
  description: string   # 설명
  root_dir: string      # 프로젝트 루트 디렉토리

tools:
  claude_code_cli:
    enabled: bool
    session_dir: string
    patterns: [string]
    exclude_patterns: [string]
    filters:
      min_message_size: int
      exclude_ide_metadata: bool

  vs_code_extension:
    enabled: bool
    session_dirs: [string]
    patterns: [string]

session:
  date_format: string              # "%Y-%m-%d"
  timezone: string                 # "UTC" 또는 "Asia/Seoul"
  group_by: string                 # "date", "tool", "both"
  sort_order: string               # "asc" 또는 "desc"

output:
  show_tool_name: bool
  show_timestamp: bool
  include_sections:
    commit_history: bool
    tech_stack: bool
    main_features: bool
```

## 필터링 및 검증

### 메시지 필터링

```
Raw Message
    ↓
[필터 1] IDE 메타데이터 제거
  - <ide_opened_file> 제외
  - <ide_* 태그 제외
    ↓
[필터 2] 최소 길이 확인
  - min_message_size 이상만 포함
    ↓
[필터 3] 중복 제거 (선택)
  - similarity_threshold 이상은 중복으로 간주
    ↓
Valid Message ✓
```

## 에러 처리

```python
# 전략:
# 1. 명시적 검증 (설정 파일, 세션 디렉토리)
# 2. 에러 로깅 및 계속 진행
# 3. 최종 결과 요약

try:
    parse_session()
except FileNotFoundError:
    logger.warning("세션 디렉토리 없음, 계속 진행...")
except JSONDecodeError:
    logger.error("JSON 파싱 실패, 다음 파일 처리...")
```

## 성능 고려사항

### 처리 시간

| 작업 | 예상 시간 |
|------|---------|
| 설정 로드 | < 100ms |
| 100개 메시지 파싱 | ~200ms |
| 1000개 메시지 파싱 | ~2s |
| DEVLOG 생성 | ~500ms |
| **총 시간** | **< 5초** |

### 메모리 사용

```
메시지 개수별 메모리:
- 100 메시지: ~2-5 MB
- 1000 메시지: ~20-50 MB
- 10000 메시지: ~200-500 MB
```

### 최적화 팁

1. **대량 처리**
   ```yaml
   session:
     max_workers: 4  # 병렬 처리
   ```

2. **특정 기간만 처리**
   ```bash
   ./devlog-wrapper.sh --from 2025-12-25
   ```

3. **메시지 크기 제한**
   ```yaml
   tools:
     claude_code_cli:
       filters:
         min_message_size: 100  # 증가시키면 더 빠름
   ```

## 확장 포인트

### 새로운 도구 추가

```python
class SessionParser:
    def parse_new_tool_sessions(self, session_dir: str) -> List[SessionMessage]:
        """새로운 도구 구현 템플릿"""
        messages = []
        # 1. 세션 디렉토리 탐색
        # 2. 파일 수집
        # 3. 메시지 파싱
        # 4. SessionMessage 객체로 변환
        return messages
```

### 커스텀 필터 추가

```python
def custom_filter(message: SessionMessage) -> bool:
    """커스텀 필터 예시"""
    # IDE 메타데이터 제거 외의 추가 필터링
    if "sensitive_word" in message.content:
        return False
    return True
```

### 출력 형식 확장

```python
def _generate_custom_section(self) -> List[str]:
    """커스텀 섹션 추가"""
    lines = []
    lines.append("## 커스텀 섹션\n\n")
    lines.append("내용...\n")
    return lines
```

## 테스트 전략

```bash
# 1. 의존성 확인
python -c "import yaml"

# 2. 설정 파일 검증
python -c "import yaml; yaml.safe_load(open('config/devlog.config.yaml'))"

# 3. 단위 테스트 (향후)
python -m pytest tests/test_parser.py

# 4. 통합 테스트 (미리보기)
./devlog-wrapper.sh --dry-run

# 5. 프로덕션 실행
./devlog-wrapper.sh
```

## 보안 고려사항

1. **파일 접근**
   - 홈 디렉토리 설정 파일만 읽음
   - 쓰기는 프로젝트 디렉토리만

2. **데이터 필터링**
   - IDE 메타데이터 자동 제거
   - 민감한 정보 필터링 가능

3. **로깅**
   - 로그 파일은 로컬에만 저장
   - 외부 전송 없음

## 향후 개선 계획

- [x] Claude Code CLI 지원 ✅
- [x] AntiGravity(Gemini) 지원 ✅
- [ ] VS Code Extensions 지원
- [ ] Aide 지원
- [ ] 실시간 모니터링 (Watch mode)
- [ ] AI 기반 자동 요약
- [ ] 웹 대시보드
- [ ] 클라우드 동기화
- [ ] 플러그인 시스템

---

**Version**: 1.0
**Last Updated**: 2025-12-28
