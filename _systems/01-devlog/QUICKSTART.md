# 🚀 빠른 시작 가이드 (1분)

## 최소한의 단계로 시작하기

### 1️⃣ 의존성 확인 (30초)

```bash
python3 --version
pip install pyyaml
```

### 2️⃣ 실행 (30초)

#### 방법 A: Git Bash (Windows 권장)
```bash
cd _systems/01-devlog
chmod +x devlog-wrapper.sh
./devlog-wrapper.sh
```

#### 방법 B: Python 직접 실행
```bash
cd _systems/01-devlog
python scripts/unified_devlog_generator.py --config config/devlog.config.yaml
```

### 3️⃣ 결과 확인 (즉시)

```bash
# 프로젝트 루트에서
cat DEVLOG.md
```

## 일반적인 사용 사례

### 📌 미리보기만 보기 (파일 미생성)

```bash
./devlog-wrapper.sh --dry-run
```

### 📌 특정 기간만 포함

```bash
./devlog-wrapper.sh --from 2025-12-25 --to 2025-12-31
```

### 📌 다른 파일 경로에 저장

```bash
./devlog-wrapper.sh --output ~/DevLogs/DEVLOG-2025-12-28.md
```

### 📌 상세 정보 보기

```bash
./devlog-wrapper.sh --verbose
```

## ⚙️ 설정 파일 기본 수정

`config/devlog.config.yaml`을 열어서 프로젝트명 수정:

```yaml
project:
  name: "your-project-name"  # ← 이 부분만 수정
  root_dir: "."
```

## 🆘 문제 해결

### ❌ "Config file not found"
```bash
# 올바른 위치에서 실행하는지 확인
pwd  # _systems/01-devlog 디렉토리여야 함
```

### ❌ "No module named 'yaml'"
```bash
pip install pyyaml
```

### ❌ "Permission denied"
```bash
chmod +x devlog-wrapper.sh
```

## 📚 더 알아보기

- 전체 가이드: [README.md](./README.md)
- 설정 옵션: [config/devlog.config.yaml](./config/devlog.config.yaml)
- Python 스크립트: [scripts/unified_devlog_generator.py](./scripts/unified_devlog_generator.py)

---

💡 **Tip**: 처음 실행할 때는 `--dry-run` 옵션으로 미리보기를 확인한 후 실행하세요!

```bash
./devlog-wrapper.sh --dry-run
./devlog-wrapper.sh  # 미리보기가 정상이면 실행
```
