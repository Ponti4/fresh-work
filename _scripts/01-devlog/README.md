# 01-devlog: 환경별 간단한 DEVLOG 생성기

각 AI 도구(Claude Code CLI, AntiGravity, VS Code)의 세션을 파싱하여 DEVLOG.md를 자동으로 생성합니다.

**특징:**
- 각 환경별로 독립적인 간단한 스크립트
- 복잡한 설정 없이 바로 실행 가능
- Python 3.7+ 만으로 실행 가능

---

## 📋 스크립트별 사용 가이드

### 1. Claude Code CLI - `claude-code-devlog.py`

Claude Code CLI로 작업한 세션을 DEVLOG.md로 생성합니다.

**경로:**
- macOS/Linux: `~/.claude/projects/{project-key}/*.jsonl`
- Windows: `%USERPROFILE%\.claude\projects\{project-key}\*.jsonl`

**사용:**
```bash
# 기본 실행
python claude-code-devlog.py

# 다른 파일명으로 저장
python claude-code-devlog.py --output MY_DEVLOG.md

# 미리보기 모드 (파일 생성 안함)
python claude-code-devlog.py --dry-run
```

**출력:**
```
DEVLOG.md
├── # 프로젝트명 - 개발 로그 (Claude Code CLI)
├── ## 2025-12-28 (Day 1)
│  └── ### 1. 작업 제목
│      ├── 사용자 입력 (코드블록)
│      └── Claude 응답
└── ---
```

---

### 2. AntiGravity (Gemini) - `antigravity-devlog.py`

AntiGravity(Gemini AI)와의 대화 기록을 DEVLOG.md로 생성합니다.

**경로:**
- macOS/Linux: `~/.gemini/antigravity/brain/*/conversation_log.md`
- Windows: `%USERPROFILE%\.gemini\antigravity\brain\*\conversation_log.md`

**사용:**
```bash
# 기본 실행
python antigravity-devlog.py

# 다른 파일명으로 저장
python antigravity-devlog.py --output MY_DEVLOG.md

# 미리보기 모드
python antigravity-devlog.py --dry-run
```

**출력:**
```
DEVLOG.md
├── # 프로젝트명 - 개발 로그 (AntiGravity)
├── ## 2025-12-28 (Day 1)
│  └── ### 1. 작업 제목
│      ├── 사용자 입력 (코드블록)
│      └── AntiGravity 응답
└── ---
```

---

### 3. VS Code Extensions - `vscode-devlog.py`

VS Code 확장의 로그를 파싱합니다. (**향후 구현**)

```bash
python vscode-devlog.py
```

---

## 🚀 빠른 시작

### 필수 요구사항
- Python 3.7+
- 해당 AI 도구의 세션이 저장되어 있어야 함

### 1단계: 스크립트 실행

프로젝트 루트에서:
```bash
# Claude Code CLI 사용했다면
python _scripts/01-devlog/claude-code-devlog.py

# AntiGravity 사용했다면
python _scripts/01-devlog/antigravity-devlog.py
```

### 2단계: 결과 확인

```bash
cat DEVLOG.md
```

---

## 📊 처리 과정

### Claude Code CLI

```
~/.claude/projects/{project-key}/*.jsonl
    ↓
[JSON Lines 파싱]
  - type: user/assistant
  - message: {content: "..."}
  - timestamp: ISO 8601
    ↓
[필터링]
  - 50자 이상만 포함
  - <ide_* 메타데이터 제외
    ↓
[날짜별 그룹핑]
  - 타임스탐프 기반 정렬
    ↓
[DEVLOG.md 생성]
  - 날짜별 섹션
  - User/Assistant 쌍
```

### AntiGravity

```
~/.gemini/antigravity/brain/*/conversation_log.md
    ↓
[마크다운 파싱]
  - > **User**: ... 형식
  - > **Antigravity**: ... 형식
    ↓
[필터링]
  - 50자 이상만 포함
  - 빈 메시지 제외
    ↓
[날짜별 그룹핑]
  - 메타데이터의 updatedAt 사용
    ↓
[DEVLOG.md 생성]
  - 날짜별 섹션
  - User/Assistant 쌍
```

---

## 🔍 트러블슈팅

### 문제: "세션 디렉토리를 찾을 수 없습니다"

**해결책:**

**Claude Code CLI:**
```bash
# 세션 디렉토리 확인
ls ~/.claude/projects/

# 프로젝트별 세션 찾기
ls ~/.claude/projects/ | grep -i $(pwd | tr '/' '-')
```

**AntiGravity:**
```bash
# Brain 디렉토리 확인
ls ~/.gemini/antigravity/brain/
```

### 문제: "메시지를 찾을 수 없습니다"

- 해당 도구로 아직 세션이 없을 수 있습니다
- `--dry-run`으로 상세한 정보를 확인하세요

### 문제: "권한 오류 (Permission denied)"

```bash
# Python 파일 실행 권한 추가
chmod +x claude-code-devlog.py
chmod +x antigravity-devlog.py

# 다시 실행
python claude-code-devlog.py
```

---

## 💡 팁

### 여러 도구 동시 사용

각 도구별로 따로 실행 후 수동으로 합치기:

```bash
# Claude Code 버전
python _scripts/01-devlog/claude-code-devlog.py --output DEVLOG_CLAUDE.md

# AntiGravity 버전
python _scripts/01-devlog/antigravity-devlog.py --output DEVLOG_ANTIGRAVITY.md

# 수동으로 병합
cat DEVLOG_CLAUDE.md DEVLOG_ANTIGRAVITY.md > DEVLOG.md
```

### Windows Batch 파일로 실행

`run.bat` 만들기:
```batch
@echo off
python _scripts/01-devlog/claude-code-devlog.py
pause
```

---

## 📝 스크립트 커스터마이징

### 필터링 기준 변경

`claude-code-devlog.py` 또는 `antigravity-devlog.py` 편집:

```python
# 최소 메시지 길이 변경 (기본값: 50자)
if len(content) < 30:  # ← 여기를 변경
    continue
```

### 날짜 형식 변경

```python
# 기본값: '%Y-%m-%d' (2025-12-28)
date_key = msg['timestamp'].strftime('%Y년 %m월 %d일')
```

---

## 🎯 다음 단계

1. 적절한 스크립트 선택 (Claude Code / AntiGravity)
2. 프로젝트 루트에서 실행
3. 생성된 `DEVLOG.md` 확인
4. 필요에 따라 수정

---

**Last Updated:** 2025-12-28
**Version:** 1.0
