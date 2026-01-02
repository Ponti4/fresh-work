# Setup Workspace - 초기 설정

> 당신의 상황을 파악하고 맞춤형 자동화 경로를 만들기 위한 첫 단계입니다.

**예상 시간: 5-7분**

---

## 📋 Step 1-3: 당신의 상황 설명

### Step 1: 환영

시작하겠습니다. 계속하시겠습니까?

---

### Step 2: 이름/닉네임

자신을 소개해주세요.

---

### Step 3: 4가지 질문에 답하기

1. **지금 뭐하고 계세요?**
   - 예: "마케팅 프리랜서로 일하고 있어요"

2. **주로 어떤 작업을 반복하세요?**
   - 예: "SNS 댓글을 손으로 정리하고 있어요"

3. **그 중 가장 힘든 게 뭐예요?**
   - 예: "시간이 너무 오래 걸려요 (주 10시간 이상)"

4. **기술 경험은 어느 정도고, 4주 후 어떤 상태가 되길 원해요?**
   - 예: "코딩은 못 하는데, 3개 반복 업무를 자동화하고 싶어요"

---

### Step 4: 정보 수집 완료

당신의 답변이 모두 수집되었습니다!

---

## 📋 Step 5-7: 시스템 정보 자동 감지

### Step 5: 운영체제 선택

사용 중인 OS를 선택하세요:
- Windows (Windows 10/11)
- Mac (Intel 또는 Apple Silicon M1/M2/M3)
- Linux (Ubuntu, Fedora 등)

---

### Step 6: 자동 감지 스크립트 실행

선택한 OS에 따라 아래 스크립트가 자동으로 실행됩니다:

**Windows:**
```bash
powershell -ExecutionPolicy Bypass -File "_scripts/00-user/01-detect-system-windows.ps1"
```

**Mac / Linux:**
```bash
bash _scripts/00-user/02-detect-system-macos.sh
```

감지되는 정보:
- OS 정보 (버전, 빌드, 아키텍처)
- CPU 정보 (모델, 코어, 속도)
- RAM 정보
- Python 설치 여부 & 버전
- GPU 정보 (있으면)
- 디스크 여유 공간

감지 결과 예시:
```
OS: Microsoft Windows 11 Home
CPU: AMD Ryzen 7 7735HS (8 cores, 3.2 GHz)
RAM: 15.25 GB
Python: 3.13.7 ✅
```

**Python이 미설치된 경우:**
- 경고만 표시되고 계속 진행됩니다
- 나중에 필요할 때 설치하면 됩니다

---

### Step 7: 정보 확인 및 저장

수집된 정보를 확인합니다:
- 이름, 직업, 목표
- OS, CPU, RAM, Python

이 정보가 맞으면 루트 `claude.md`의 "당신의 프로필" 섹션에 입력합니다.

---

## 🎉 완료!

루트 `claude.md` 파일을 열어서 프로필 섹션을 채우면 됩니다:

```markdown
## 📋 당신의 프로필

- **이름**: 김철수
- **직업/상황**: 마케팅 프리랜서
- **첫 자동화**: SNS 게시물 데이터 수집
- **OS**: Windows 11 Home
- **Python**: ☐ 미설치 / ☐ 설치됨
```

---

## 🚀 다음 단계

```bash
/clarify "당신의 반복 업무 설명"
```

예시:
```bash
/clarify "인스타그램 팔로워 댓글을 매일 2시간 걸려 정리하고 있어"
```

이 명령어로 첫 자동화가 시작됩니다!

---

**궁금한 점이 있으면 Claude에게 물어보세요!** 💡
