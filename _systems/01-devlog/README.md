# 01-devlog: 통합 개발 로그 생성 시스템

Claude Code CLI, AntiGravity(Gemini), VS Code Extensions 등 여러 AI 도구에서의 개발 세션을 추적하여 통합 DEVLOG.md를 자동 생성하는 시스템입니다.

## 📋 목표

- **다중 도구 세션 추적**: Claude Code CLI, AntiGravity(Gemini), VS Code, Aide 등에서의 개발 기록 통합
- **자동 로그 생성**: 여러 소스의 세션을 수집하여 시간순으로 정렬
- **맥락 기반 문서화**: 날짜별, 도구별로 구분된 체계적인 DEVLOG 생성
- **지속적 업데이트**: 기존 DEVLOG.md가 있으면 이어서 추가 (덮어쓰기 금지)

## 🗂️ 디렉토리 구조

```
_systems/01-devlog/
├── README.md                               # 이 파일
├── config/
│   └── devlog.config.yaml                  # 세션 추적 대상 도구 및 경로 설정
├── scripts/
│   └── unified_devlog_generator.py        # Python 메인 스크립트
├── devlog-wrapper.sh                       # Git Bash 래퍼 스크립트
└── logs/                                   # 실행 로그 디렉토리 (자동생성)
    └── devlog.log
```

## 🚀 빠른 시작

### 1단계: 의존성 설치

```bash
# Python 및 PyYAML 설치 확인
python3 --version
pip install pyyaml
```

### 2단계: 설정 파일 준비

`config/devlog.config.yaml`을 프로젝트에 맞게 수정:

```yaml
project:
  name: "gpters-20th-templates"
  root_dir: "."

tools:
  claude_code_cli:
    enabled: true
    session_dir: "~/.claude/projects"
```

### 3단계: 스크립트 실행

#### 옵션 A: 직접 Python 실행
```bash
cd _systems/01-devlog
python scripts/unified_devlog_generator.py --config config/devlog.config.yaml
```

#### 옵션 B: Git Bash 래퍼 사용 (권장)
```bash
cd _systems/01-devlog
chmod +x devlog-wrapper.sh
./devlog-wrapper.sh
```

#### 옵션 C: 프로젝트 루트에서 실행
```bash
python _systems/01-devlog/scripts/unified_devlog_generator.py \
  --config _systems/01-devlog/config/devlog.config.yaml
```

### 4단계: 결과 확인

프로젝트 루트에 생성된 `DEVLOG.md` 확인:

```bash
cat DEVLOG.md
```

## 📝 상세 사용 가이드

### Python 직접 실행

```bash
# 기본 실행
python scripts/unified_devlog_generator.py --config config/devlog.config.yaml

# 미리보기 (파일 생성 안함)
python scripts/unified_devlog_generator.py --config config/devlog.config.yaml --dry-run

# 특정 날짜 범위만 포함
python scripts/unified_devlog_generator.py \
  --config config/devlog.config.yaml \
  --from 2025-12-25 \
  --to 2025-12-31

# 다른 경로에 출력
python scripts/unified_devlog_generator.py \
  --config config/devlog.config.yaml \
  --output /path/to/DEVLOG.md
```

### Git Bash 래퍼 실행

```bash
# 기본 실행
./devlog-wrapper.sh

# 미리보기 모드
./devlog-wrapper.sh --dry-run

# 특정 설정 파일 사용
./devlog-wrapper.sh --config config/devlog.config.yaml

# 기간 지정
./devlog-wrapper.sh --from 2025-12-25 --to 2025-12-31

# 도움말
./devlog-wrapper.sh --help
```

## ⚙️ 설정 파일 상세

### Claude Code CLI

```yaml
claude_code_cli:
  enabled: true
  name: "Claude Code CLI"
  session_dir: "~/.claude/projects"
  patterns:
    - "*.jsonl"
  exclude_patterns:
    - "agent-*.jsonl"  # Agent 세션 제외
  filters:
    min_message_size: 50  # 50자 이상만 포함
    exclude_ide_metadata: true
```

**세션 파일 위치:**
- macOS/Linux: `~/.claude/projects/{project-key}/`
- Windows: `%USERPROFILE%\.claude\projects\{project-key}\`

**프로젝트 키 형식:**
- 현재 작업 디렉토리를 특정 형식으로 변환
- 예: `/Users/name/projects/my-app` → `-Users-name-projects-my-app`

### AntiGravity (Gemini)

```yaml
antigravity:
  enabled: true
  name: "AntiGravity"
  brain_dir: "~/.gemini/antigravity/brain"
  patterns:
    - "conversation_log.md"
    - "conversation_log.md.metadata.json"
  filters:
    min_message_size: 50
    exclude_metadata: false
```

**세션 파일 위치:**
- macOS/Linux: `~/.gemini/antigravity/brain/{session-id}/`
- Windows: `%USERPROFILE%\.gemini\antigravity\brain\{session-id}\`

**저장 형식:**
- `conversation_log.md`: 마크다운 형식의 대화 기록
- `conversation_log.md.metadata.json`: 메타데이터 (updatedAt 등)

### VS Code Extensions

```yaml
vs_code_extension:
  enabled: true
  name: "VS Code Extension"
  session_dirs:
    - "~/.vscode"
    - "~/.config/Code"  # Linux/Mac
    - "~/AppData/Roaming/Code"  # Windows
```

**주요 확장:**
- GitHub Copilot: `~/.vscode/extensions/github.copilot-*/`
- Codeium: `~/.vscode/extensions/codeium.codeium-*/`

### Aide

```yaml
aide:
  enabled: false  # 필요시 true로 변경
  name: "Aide"
  session_dir: "~/.aide"
```

## 📋 출력 형식

생성되는 DEVLOG.md 구조:

```markdown
# gpters-20th-templates - 개발 로그

생성일: 2025-12-28 14:30:45
Claude Code와 함께 진행한 개발 작업 기록입니다.

---

## 2025-12-28 (Day 1)

### 1. 통합 devlog 스크립트 개발 [Claude Code CLI]

```
다중 AI 도구 세션 통합 추적 시스템 구축
```

**Claude 작업:**
- _systems/01-devlog 디렉토리 구조 생성
- config/devlog.config.yaml 설정 파일 작성
- unified_devlog_generator.py Python 메인 스크립트 구현
- devlog-wrapper.sh Git Bash 래퍼 작성
- 자동 로그 생성 및 업데이트 기능 구현

---

## 커밋 히스토리

| 날짜 | 커밋 | 설명 |
|------|------|------|
| 12/28 | `abc1234` | feat: 통합 devlog 생성 시스템 구축 |

---

## 기술 스택

- **Language**: Python 3.7+
- **Tools**: Claude Code, VS Code Extensions
- **Format**: YAML (설정), JSON Lines (세션)
- **DevOps**: Git, GitHub

---

## 주요 기능

1. **다중 도구 세션 통합 추적**
   - Claude Code CLI, VS Code Extensions, Aide 등
   - 타임스탐프 기반 자동 정렬 및 그룹핑

2. **자동 DEVLOG 생성**
   - 기존 파일 보존 및 점진적 업데이트
   - 날짜별, 도구별 체계적 분류

3. **맥락 기반 문서화**
   - IDE 메타데이터 자동 필터링
   - 의미있는 대화만 선별 기록
```

## 🔍 트러블슈팅

### 문제: "Config file not found"

**원인**: 설정 파일 경로가 잘못되었거나 파일이 없음

**해결책:**
```bash
# 설정 파일 확인
ls -la _systems/01-devlog/config/

# 절대 경로 사용
python scripts/unified_devlog_generator.py \
  --config /full/path/to/devlog.config.yaml
```

### 문제: "ModuleNotFoundError: No module named 'yaml'"

**원인**: PyYAML이 설치되지 않음

**해결책:**
```bash
pip install pyyaml
# 또는
python -m pip install pyyaml
```

### 문제: 세션 파일을 찾을 수 없음

**원인**: Claude Code 세션 디렉토리 설정이 잘못됨

**해결책:**
```bash
# 세션 디렉토리 확인
ls -la ~/.claude/projects/

# 현재 프로젝트의 세션 디렉토리 확인
ls -la ~/.claude/projects/ | grep $(pwd | tr '/' '-')

# 상세 실행으로 디버깅
./devlog-wrapper.sh --verbose --dry-run
```

### 문제: 권한 오류 (Permission denied)

**원인**: 스크립트 실행 권한 없음

**해결책:**
```bash
# 실행 권한 추가
chmod +x devlog-wrapper.sh
chmod +x scripts/unified_devlog_generator.py

# 다시 실행
./devlog-wrapper.sh
```

### 문제: 생성된 DEVLOG.md가 너무 크거나 느림

**원인**: 세션 파일이 매우 크거나 처리할 메시지가 많음

**해결책:**
```bash
# 특정 기간만 처리
./devlog-wrapper.sh --from 2025-12-20

# 최대 항목 수 제한 (config에서 설정)
# devlog:
#   max_entries_per_session: 100
```

## 🛠️ 개발 팁

### 1. 테스트 모드 (미리보기)

```bash
# 파일을 생성하지 않고 미리보기
./devlog-wrapper.sh --dry-run

# Python으로 직접
python scripts/unified_devlog_generator.py \
  --config config/devlog.config.yaml --dry-run
```

### 2. 로그 파일 확인

```bash
# 실행 로그 확인
cat logs/devlog.log

# 실시간 모니터링
tail -f logs/devlog.log
```

### 3. 설정 파일 검증

```bash
# YAML 문법 확인
python -c "import yaml; yaml.safe_load(open('config/devlog.config.yaml'))" && echo "OK"
```

### 4. 디버깅 모드

```bash
# 상세 출력으로 실행
./devlog-wrapper.sh --verbose --dry-run
```

## 📚 파일 설명

### config/devlog.config.yaml
- 도구별 세션 디렉토리 설정
- 필터링 규칙 및 출력 형식 설정
- 로깅 및 백업 설정

### scripts/unified_devlog_generator.py
- 메인 로직 구현
- 여러 도구의 세션 파싱
- DEVLOG.md 생성

### devlog-wrapper.sh
- Git Bash 래퍼 스크립트
- 사용자 친화적 인터페이스
- 의존성 자동 확인

## 🔄 작업 흐름

```
1. 설정 파일 로드 (devlog.config.yaml)
   ↓
2. 의존성 확인 (Python, PyYAML)
   ↓
3. 세션 디렉토리 수집
   - Claude Code CLI: ~/.claude/projects/{project-key}/
   - VS Code: ~/.vscode/ (향후)
   - Aide: ~/.aide/ (향후)
   ↓
4. 세션 파일 파싱
   - JSONL 파일 읽기
   - 메시지 추출
   - IDE 메타데이터 필터링
   ↓
5. 메시지 정렬 및 그룹핑
   - 타임스탐프 기반 정렬
   - 날짜별 그룹핑
   ↓
6. DEVLOG.md 생성
   - 날짜별 섹션 생성
   - 도구별 표시
   - 메타정보 추가 (커밋, 기술스택)
   ↓
7. 파일 저장 또는 미리보기
```

## 📖 참고 문서

- `../10-clarify/` - 프로젝트 명확화 시스템
- `../../.claude/commands/gpters-devlog-writer.md` - 원본 devlog 스크립트 명세
- `../../CLAUDE.md` - 프로젝트 프로필

## 🤝 기여 및 개선

이 시스템은 지피터스 20기 프리랜서들의 자동화 요구사항을 기반으로 설계되었습니다.

**향후 계획:**
- [x] Claude Code CLI 세션 파싱 ✅
- [x] AntiGravity(Gemini) 세션 파싱 ✅
- [ ] VS Code Extensions 세션 파싱
- [ ] Aide 세션 파싱
- [ ] 자동 요약 기능 (AI 기반)
- [ ] 실시간 모니터링
- [ ] 웹 대시보드 생성

## 📜 라이선스

이 프로젝트는 지피터스 20기 프리랜서 프로젝트의 일부입니다.

---

**Last Updated**: 2025-12-28
**Version**: 1.0
**Maintained by**: Gpters 20th Freelancer Project
