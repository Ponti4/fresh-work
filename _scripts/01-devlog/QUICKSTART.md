# 빠른 시작 (1분)

## 📍 위치 확인

```
_scripts/01-devlog/
├── claude-code-devlog.py      # Claude Code CLI용
├── antigravity-devlog.py       # AntiGravity(Gemini)용
├── vscode-devlog.py           # VS Code용 (준비 중)
├── README.md                  # 상세 가이드
└── QUICKSTART.md              # 이 파일
```

---

## 🚀 한 줄로 실행

### Claude Code CLI 사용했다면

```bash
cd _scripts/01-devlog
python claude-code-devlog.py
```

### AntiGravity(Gemini) 사용했다면

```bash
cd _scripts/01-devlog
python antigravity-devlog.py
```

**결과:** 프로젝트 루트에 `DEVLOG.md` 생성 ✅

---

## 💡 주요 옵션

```bash
# 다른 파일명으로 저장
python claude-code-devlog.py --output MY_DEVLOG.md

# 미리보기만 (파일 미생성)
python claude-code-devlog.py --dry-run
```

---

## 📝 생성되는 형식

```
# 프로젝트명 - 개발 로그 (Claude Code CLI)

생성일: 2025-12-28 14:30:45

---

## 2025-12-28 (Day 1)

### 1. 작업 제목

```
사용자 입력
```

**Claude 응답:**
- 응답 요약...
```

---

## ❓ 문제 발생 시

### "세션을 찾을 수 없습니다"

- Claude Code: `~/.claude/projects/` 확인
- AntiGravity: `~/.gemini/antigravity/brain/` 확인

### "메시지가 없습니다"

- 해당 도구로 아직 세션이 없을 수 있음
- `--dry-run` 실행하여 상세 정보 확인

---

## 📖 더 알아보기

상세한 설명은 `README.md` 참조:
- 경로 설정
- 필터링 규칙
- 트러블슈팅
- 커스터마이징

---

**끝! 이제 DEVLOG.md를 확인하세요.**
