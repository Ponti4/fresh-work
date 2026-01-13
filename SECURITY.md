# 🔒 보안 정책

## 개요

이 프로젝트는 Claude Code 학습 템플릿입니다. 사용자의 민감한 정보를 보호하기 위해 다음 보안 정책을 준수합니다.

---

## 1️⃣ 절대로 Git에 커밋하지 않을 파일

### 환경 변수 & API 키
```
.env
.env.local
.env.*.local
```

### 인증 토큰 & 자격증명
```
.gcalcli_oauth      # Google Calendar OAuth 토큰
.credentials*       # 인증 자격증명
.token*             # API 토큰
*.pem, *.key, *.cert  # SSL/TLS 인증서
```

### Cloud 설정
```
.aws/               # AWS 크레덴셜
.gcloud/            # Google Cloud 설정
credentials.json    # Firebase 등
```

### 개인 설정
```
.claude/settings.local.json  # 개인 권한 설정 (Git 추적 안 함)
```

**→ 이 파일들은 `.gitignore`에 모두 포함되어 있습니다.**

---

## 2️⃣ Claude Code 권한 설정

### 설정 파일 위치
```
.claude/settings.local.json  (개인 설정 - 커밋 금지)
.claude/settings.template.json  (템플릿 - 참고용)
```

### 설정 방법

1. **템플릿 복사**
   ```bash
   cp .claude/settings.template.json .claude/settings.local.json
   ```

2. **필요한 권한만 활성화**
   - 불필요한 Bash 권한 제거
   - 신뢰할 수 있는 웹사이트만 허용
   - 개인 환경 경로는 절대 Git에 커밋하지 않기

3. **주의 사항**
   - 절대 경로(예: `/c/Users/username/...`) 제거
   - 개인 Python 설치 경로 커밋 금지
   - API 키가 포함된 URL 금지

---

## 3️⃣ Git 안전 운영

### ✅ 안전한 커밋
```bash
/git-commit
```
이 명령어는 다음을 자동으로 확인합니다:
- 민감한 파일 감지
- `.gitignore` 준수 여부
- 커밋 메시지 형식

### ❌ 위험한 운영
```bash
# 절대 하지 마세요!
git push --force              # 강제 푸시 금지
git add .env                  # 민감한 파일 추가 금지
git commit --amend --no-verify  # 훅 스킵 금지
```

---

## 4️⃣ 데이터 보안 체크리스트

커밋하기 전에 다음을 확인하세요:

- [ ] `.env` 파일이 포함되지 않았는가?
- [ ] API 키/토큰이 코드에 하드코딩되지 않았는가?
- [ ] 개인 정보 (이메일, 전화, 주소)가 포함되지 않았는가?
- [ ] 프라이빗 키 (*.pem, *.key)가 포함되지 않았는가?
- [ ] 절대 경로 (C:\Users\username\...)가 포함되지 않았는가?
- [ ] 민감한 URL (기업 내부 시스템)이 포함되지 않았는가?

---

## 5️⃣ 실수로 민감한 정보를 커밋했다면?

### 즉시 조치
```bash
# 1. 마지막 커밋에서 파일 제거 (아직 푸시하지 않은 경우)
git rm --cached .env
echo ".env" >> .gitignore
git commit --amend --no-edit

# 2. 이미 푸시한 경우 (저장소 관리자에 연락)
git reset HEAD~1
git rm --cached .env
git commit -m "Remove sensitive file from history"
# 주의: 히스토리 재정렬은 모든 팀원에게 영향을 줍니다
```

### 예방
- 정기적으로 `git status` 확인
- 커밋 전 `git diff` 검토
- `.gitignore` 정기 점검

---

## 6️⃣ Claude Code 환경 변수 사용

### 안전한 방법
환경 변수는 `.env` 파일에 저장하고, 코드에서 로드합니다:

```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
```

### Python 가상환경에서 설정
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows

pip install python-dotenv
```

---

## 7️⃣ 팀 작업 시 보안

### Git 설정
```bash
# 전역 .gitignore 설정
git config --global core.excludesfile ~/.gitignore_global

# 프로젝트별 .gitignore 준수
git check-ignore -v *  # .gitignore 적용 상태 확인
```

### 커밋 전 체크
```bash
# 커밋할 파일 목록 확인
git status

# 변경사항 상세 확인
git diff --cached

# 민감한 문자열 검색
grep -r "API_KEY\|SECRET\|PASSWORD" . --exclude-dir=.git
```

---

## 📚 참고 문서

- [GitHub - 민감한 데이터 제거](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [Python dotenv](https://python-dotenv.readthedocs.io/)
- [Git Security Best Practices](https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage)

---

## 🤝 질문 또는 우려사항?

보안 관련 문제는:
1. `/setup-workspace`에서 "보안 설정"을 선택하거나
2. Claude에게 직접 문의하세요

**안전한 개발 환경을 함께 만들어갑시다!** 🔐
