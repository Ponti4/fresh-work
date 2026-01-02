# System Information Auto Detection Scripts

입문자 프리랜서를 위한 자동 시스템 정보 감지 스크립트입니다.

## 개요

사용자가 스크린샷을 촬영하거나 CLI 명령어를 수동으로 실행할 필요 없이, Claude가 자동으로 다음 정보를 수집합니다:

- ✅ Python 버전 및 설치 경로
- ✅ OS 정보 (이름, 버전, 빌드, 아키텍처)
- ✅ CPU 정보 (모델, 코어, 속도)
- ✅ RAM 정보 (용량, 사용 가능 메모리)
- ✅ GPU 정보 (디바이스, 드라이버 버전)
- ✅ 디스크 정보 (용량, 여유 공간)

## 스크립트 목록

| 파일 | 대상 OS | 형식 |
|------|--------|------|
| `01-detect-system-windows.ps1` | Windows | PowerShell |
| `02-detect-system-macos.sh` | macOS / Linux | Bash |

## 사용 방법

### Windows 사용자

```bash
powershell -ExecutionPolicy Bypass -File "01-detect-system-windows.ps1"
```

**실행 결과:**
- 콘솔에 사람이 읽기 좋은 형식으로 시스템 정보 출력
- JSON 형식으로 파싱 가능한 데이터 출력
- `system-info.json` 파일로 자동 저장

### Mac / Linux 사용자

```bash
bash ./02-detect-system-macos.sh
```

**실행 결과:**
- 콘솔에 사람이 읽기 좋은 형식으로 시스템 정보 출력
- JSON 형식으로 파싱 가능한 데이터 출력
- `system-info.json` 파일로 자동 저장

## 출력 형식

### 콘솔 출력 예시 (Windows)

```
Checking Python version...
Checking OS information...
Checking CPU information...
Checking RAM information...
Checking GPU information...
Checking disk information...

System information collection completed!

=====================================================
Collected System Information:
=====================================================

OS Information
   Name: Microsoft Windows 11 Home
   Version: 10.0.26100 (Build: 26100)
   Architecture: 64-bit

Python
   Status: Installed
   Version: Python 3.13.7

CPU
   Name: AMD Ryzen 7 7735HS with Radeon Graphics
   Cores: 8 cores / 16 threads
   Speed: 3.2 GHz

RAM
   Total: 15.25 GB
   Available: 0.01 GB

GPU
   - AMD Radeon(TM) Graphics
     Driver: 32.0.11038.3
   - NVIDIA GeForce RTX 4050 Laptop GPU
     Driver: 32.0.15.8142

Disk (C:)
   Total: 449.39 GB
   Free: 164.61 GB

=====================================================
```

### JSON 출력 예시

```json
{
  "os_type": "windows",
  "timestamp": "2026-01-02T04:43:06Z",
  "os": {
    "name": "Microsoft Windows 11 Home",
    "version": "10.0.26100",
    "build": "26100",
    "architecture": "64-bit"
  },
  "python": {
    "installed": true,
    "version": "Python 3.13.7",
    "path": "C:\\Users\\username\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
  },
  "cpu": {
    "name": "AMD Ryzen 7 7735HS with Radeon Graphics",
    "cores": 8,
    "logical_processors": 16,
    "speed_ghz": 3.2
  },
  "memory": {
    "total_gb": 15.25,
    "available_gb": 0.01
  },
  "gpu": {
    "count": 2,
    "devices": [
      {
        "name": "AMD Radeon(TM) Graphics",
        "driver_version": "32.0.11038.3"
      },
      {
        "name": "NVIDIA GeForce RTX 4050 Laptop GPU",
        "driver_version": "32.0.15.8142"
      }
    ]
  },
  "disk": {
    "total_gb": 449.39,
    "free_gb": 164.61
  }
}
```

## setup-workspace에서의 통합

이 스크립트는 다음과 같이 setup-workspace 플로우에 통합됩니다:

```
Step 5: OS 선택 (Windows / Mac / Linux)
         ↓
Step 6: 자동 감지 실행
         - Claude가 해당 OS별 스크립트 실행
         - 시스템 정보 자동 수집
         ↓
Step 7: 수집된 정보 확인
         - 사용자에게 감지된 정보 표시
         - "확인" 또는 "수정" 옵션 제시
         ↓
Step 8: Memory에 저장 및 CLAUDE.md 업데이트
```

## 장점

| 항목 | 기존 방식 | 개선 방식 |
|------|---------|---------|
| 사용자 부담 | 스크린샷 촬영 + CLI 명령어 실행 | 스크립트 실행만 (자동) |
| 단계 수 | 13단계 | 9단계 |
| 정확성 | 수동 입력 시 오류 가능 | 자동 감지로 100% 정확 |
| 소요 시간 | 15분 | 5-7분 |
| 진입 장벽 | 높음 (비개발자 어려움) | 낮음 (한 버튼 클릭) |

## 문제 해결

### Python이 감지되지 않는 경우

```bash
# 수동으로 Python 경로 확인
which python3  # Mac/Linux
where python   # Windows
```

### GPU 정보가 없는 경우

- Mac: Apple Silicon (M1/M2/M3)은 자동 감지
- Linux: NVIDIA GPU는 `nvidia-smi`로 감지하며, 드라이버 미설치 시 감지 안 됨

### 권한 문제 (Windows)

PowerShell 실행 정책이 제한되어 있는 경우:

```bash
powershell -ExecutionPolicy Bypass -File "01-detect-system-windows.ps1"
```

## 기술 스택

| OS | 기술 |
|----|------|
| Windows | PowerShell WMI (Get-WmiObject, Get-CimInstance) |
| Mac | POSIX tools (sw_vers, sysctl, system_profiler) |
| Linux | POSIX tools (lsb_release, /proc, /etc/os-release) |

## 라이선스

이 스크립트는 gpters 20기 프리랜서 프로젝트의 일부입니다.
