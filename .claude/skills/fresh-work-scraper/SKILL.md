---
name: fresh-work-scraper
description: 온라인 채용 플랫폼에서 구인 공고를 크롤링하여 JSON으로 저장. "구인 공고 수집", "채용 정보 담기", "일자리 검색" 등을 언급하면 자동 실행. Selenium 기반 동적 페이지 수집.
---

# Fresh Work Scraper

여러 채용 플랫폼에서 구인 공고를 자동 수집하여 로컬 JSON 파일로 저장합니다.

## 사전 요구사항

### 필수 패키지

```bash
pip install selenium webdriver-manager beautifulsoup4 lxml
```

### 설치 확인

```bash
python -c "import selenium; print(f'Selenium {selenium.__version__}')"
python -c "import bs4; print('BeautifulSoup 설치됨')"
```

**Chrome 브라우저**: Windows 11에 기본 탑재되어 있으며, ChromeDriver는 자동으로 설치됩니다 (webdriver-manager).

---

## 사용 방법

### 기본 실행 (알바몬 최근 50개 공고)

```bash
python scripts/scrape_jobs.py --source "albamon"
```

### 추가 옵션

```bash
# 사람인에서 수집
python scripts/scrape_jobs.py --source "saramin"

# 여러 소스에서 수집
python scripts/scrape_jobs.py --source "all"

# 헤드리스 모드 (백그라운드 실행)
python scripts/scrape_jobs.py --source "albamon" --headless

# 검색어 필터링 (예: 원격, 단기)
python scripts/scrape_jobs.py --source "albamon" --keywords "원격,단기"

# 출력 경로 변경
python scripts/scrape_jobs.py --source "albamon" --output-dir "docs/jobs/"
```

---

## 옵션 설명
source` | 채용 플랫폼 (albamon, saramin, all) | albamon |
| `--keywords` | 검색 키워드 (쌍표 구분) | - |
| `--output-dir` | 저장 디렉토리 | `docs/jobs/` |
| `--headless` | 헤드리스 모드 (브라우저 숨김) | False |
| `--max-pages` | 최대 페이지 수 | 5
| `--output-dir` | 저장 디렉토리 | `docs/notes/gpters_editor_soyeon/` |
| `--headless` | 헤드리스 모드 (브라우저 숨김) | False |
| `--no-skip` | 중복 파일 덮어쓰기 | False (중복 건너뜀) |

---

## 출력 형식

### 저장 경로
```
docs/jobs/
├── albamon_20260121.json
├── saramin_20260121.json
└── all_jobs_20260121.json
```

### JSON 파일 예시

```json
{
  "source": "albamon",
  "collected_at": "2025-01-21T14:30:15",
  "total_jobs": 42,
  "jobs": [
    {
      "title": "데이터 입력 및 정리 (재택 가능)",
      "company": "ABC 회사",
      "url": "https://www.albamon.com/job/123456",
      "salary": "시급 12,000원",
      "location": "서울 강남",
      "work_type": "단기",
      "remote_available": true,
      "flexible_hours": true
    }
  ]
}
```

---

## 실행 결과
source": "albamon",
  "collected_at": "2025-01-21T14:30:15",
  "total_collected": 250,
  "saved": 245,
  "filtered_out": 5,
  "saved_file": "docs/jobs/albamon_20260121.json",
  "keywords_applied": ["원격", "단기"],
  "errors": []
}
```

### 실패 시 JSON 출력

```json
{
  "status": "error",
  "source": "albamon",
  "collected": 0,
  "saved": 0,
  "saved_file": null,
  "errors": [
    {
      "type": "connection",
      "message": "Failed to connect to albamon.com
  "skipped": 0,
  "saved_files": [],
  "errors": [
    {
      "type": "critical",
      "message": "Page load failed: no such element"
    }
  ]
}
```

---

## 에러 처리

### 일반적인 문제

#### 1. ChromeDriver 설치 실패
```
✗ ChromeDriver installation failed
```
**해결책**: Chrome 브라우저가 설치되어 있는지 확인하세요.

#### 2. 페이지 로딩 타임아웃
```
✗ Page l페이지 구조 변경
```
✗ Job element not found on page
```
**해결책**: 채용 사이트 페이지 구조가 변경되었을 수 있습니다. 선택자를 업데이트해야 
**해결책**: 지피터스 페이지 구조가 변경되었을 수 있습니다. `references/selector-guide.md`를 참조하세요.

#### 4. 한글 파일명 저장 오류 (Windows)
**해결책**: UTF-8 인코딩이 자동으로 적용되므로 추가 설정 불필요합니다.

---

## 워크플로우

### 1단계: 페이지 접속
- 채용 사이트 URL로 이동
- JavaScript 렌더링 완료 대기 (5초)

### 2단계: 공고 파싱
- 동적으로 로드된 구인 공고 대기 (최대 15초)
- BeautifulSoup으로 HTML 파싱
- 제목, 회사명, 급여, 위치, 근무형태 추출

### 3단계: JSON 저장
- `docs/jobs/` 디렉토리 생성
- 파일명: `{source}_{YYYYMMDD}.json` 형식
- UTF-8 인코딩으로 한글 정상 저장

### 4단계: 결과 출력
- JSON 형식으로 결과 출력
- 수집된 공고 수 및 필터링 통계과 출력
- 저장 파일 목록 출력

---

## Claude Code와 통합

### 자동 트리거

사용자가 다음 중 하나를 언급하면 자동으로 이 Skill을 실행합니다:

- "구인 공고 수집"
- "채용 정보 담기"
- "일자리 검색"
- "채용 공고 크롤링"
- "알바몬 공고 가져오기"

### 사용 예시

**사용자**:
```
원격근무 가능한 일자리 공고 50개 수집해줘
```

**Claude Code 응답**:
```
알바몬에서 50개 공고를 수집하여 45개를 저장했습니다.

저장 위치: docs/jobs/albamon_20260121.json

총 수집: 50개
저장: 45개 (원격근무 가능)
필터 제외: 5개 (원격 불가능)
```

---

## 데이터 구조

상세 문서: [references/selector-guide.md](references/selector-guide.md)

### 수집 데이터
### 수집 데이터

각 구인 공고에서 추출되는 정보:

- **title** (string): 공고 제목
- **company** (string): 회사명
- **url** (string): 공고 링크 (절대 URL)
- **salary** (string): 급여 정보
- **location** (string): 근무 위치
- **work_type** (string): 근무 형태 (단기, 장기, 프로젝트 등)
- **remote_available** (boolean): 원격근무 가능 여부
- **flexible_hours** (boolean): 유연 근무시간 여부
## 고급 사용법

### 여러 프로필 수집
플랫폼 수집

```bash
# 알바몬에서 수집
python scripts/scrape_jobs.py --source "albamon" --max-pages 10

# 사람인에서 수집
python scripts/scrape_jobs.py --source "saramin" --max-pages 10

# 모든 플랫폼에서 수집
python scripts/scrape_jobs.py --source "all"
```

### 키워드 필터링으로 맞춤 공고 검색

```bash
# 원격근무 가능 + 단기 공고
python scripts/scrape_jobs.py --source "all" --keywords "원격,단기"

# 유연한 근무시간 공고
python scripts/scrape_jobs.py --source "albamon" --keywords "유연근무"
```
import subprocess
import json

profiles = [
    ("https://www.gpters.org/member/ID1", "profile1"),
    ("https://www.gpters.org/member/ID2", "profile2"),
]

for url, name in profiles:
    result = subprocess.run(
        ["python", "scripts/scrape_posts.py",
         "--profile-url", url,
         "--output-dir", f"docs/notes/gpters_{name}"],
        capture_output=True,
        text=True
    )
    output = json.loads(result.stdout)
    print(f"{name}: {output['saved']}개 저장, {output['skipped']}개 건너뜀")
```

---

## 유지보수

### 페이지 구조 변경 시

지피터스 페이지가 변경되면 `references/selector-guide.md`를 참조하여 CSS Selector를 업데이트하세요.

**수정 단계**:
1. Chrome DevTools (F12)에서 게시물 요소 구조 확인
2. `scrape_posts.py`의 Selector 값 업데이트
3. 작은 규모로 테스트 (`--max-results 3`)
4. 성공 시 full run 실행

### 로깅 활성화 (개발용)

Python 스크립트에 다음 추가:
```python
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

---

## 문제 해결 팁

### 브라우저 창이 제대로 로드되지 않는 경우

```bash
# GUI 모드에서 실행해서 상태 확인
python scripts/scrape_posts.py --profile-url "URL" --max-results 5

# (헤드리스 모드는 나중에)
```

### Selector 찾기

1. Chrome에서 https://www.gpters.org/member/WZlPiwwnpW 방문
2. F12 → Elements 탭
3. 게시물 요소 우클릭 → "Inspect" 또는 Ctrl+Shift+C로 선택
4. HTML 구조 확인

---

## FAQ

**Q**: 스케줄링은 지원하나요?

**A**: MVP에는 수동 실행만 포함되어 있습니다. 자동 스케줄링이 필요하면 `APScheduler` 또는 Windows 작업 스케줄러를 별도로 설정하세요.

**Q**: 게시물 본문 전체를 수집할 수 있나요?

**A**: 현재는 제목, URL, 작성일, 요약만 수집합니다. 본문 전체 수집은 향후 업데이트 예정입니다.

**Q**: 이미지도 다운로드되나요?

**A**: 현재는 Markdown 텍스트만 저장합니다. 이미지 다운로드는 향후 기능 추가 예정입니다.

**Q**: 프록시 설정이 필요한가요?

**A**: 기본 설정은 프록시 없이 작동합니다. 필요시 `scrape_posts.py`의 `setup_driver()` 함수를 수정하세요.

---

## 관련 리소스

- [references/selector-guide.md](references/selector-guide.md) - CSS Selector 유지보수 가이드
- [Selenium 공식 문서](https://www.selenium.dev/documentation/)
- [BeautifulSoup 공식 문서](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

**버전**: 1.0.0 MVP
**최종 업데이트**: 2025-01-06
**상태**: Ready for Use ✅
