---
name: daangn-scraper
description: 당근알바에서 구인 공고를 크롤링하여 SQLite DB에 저장. "당근알바", "당근 일자리", "당근마켓 알바" 등을 언급하면 자동 실행.
---

# 당근알바 크롤러

당근마켓 일자리(당근알바) 공고를 자동 수집하여 SQLite DB에 저장합니다.

---

## 사전 요구사항

```bash
pip install selenium webdriver-manager beautifulsoup4 lxml
```

Chrome 브라우저가 설치되어 있어야 합니다.

---

## 사용 방법

### 기본 실행

```bash
# GUI 모드 (브라우저 창 보임)
python scripts/scrape_daangn.py

# 헤드리스 모드 (백그라운드 실행)
python scripts/scrape_daangn.py --headless
```

### 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--max-jobs` | 최대 수집 공고 수 | 100 |
| `--headless` | 헤드리스 모드 | False |
| `--db-path` | SQLite DB 경로 | `data/daangn_jobs.db` |

### 예시

```bash
# 50개만 수집
python scripts/scrape_daangn.py --max-jobs 50

# 헤드리스 + 200개 수집
python scripts/scrape_daangn.py --headless --max-jobs 200

# DB 경로 변경
python scripts/scrape_daangn.py --db-path data/my_jobs.db
```

---

## 수집 데이터

### 기본 정보
- `title`: 공고 제목
- `company`: 업체명
- `address`: 근무지 주소

### 급여/근무 조건
- `salary_type`: 급여 유형 (시급/일당/월급/건당)
- `salary_amount`: 급여 금액
- `work_days`: 근무 요일
- `work_hours`: 근무 시간
- `negotiable`: 협의 가능 여부

### 직무 내용
- `job_description`: 상세 업무 내용

### 작성자 정보
- `author_nickname`: 작성자 닉네임
- `author_region`: 작성자 지역
- `manner_temp`: 매너온도
- `badges`: 배지 (모범 구인자 등)
- `review_count`: 후기 수

### 공고 통계
- `applicant_count`: 지원자 수
- `interest_count`: 관심 수
- `posted_at`: 작성일

---

## 출력 형식

### 성공 시

```json
{
  "status": "success",
  "collected_at": "2026-01-21T14:30:00",
  "total_found": 150,
  "new_saved": 45,
  "duplicates_skipped": 100,
  "errors": 5,
  "db_path": "data/daangn_jobs.db"
}
```

### 실패 시

```json
{
  "status": "error",
  "error_type": "PageLoadError",
  "message": "목록 페이지 로딩 실패"
}
```

---

## DB 조회

```bash
# 전체 공고 수 확인
sqlite3 data/daangn_jobs.db "SELECT COUNT(*) FROM jobs"

# 최근 5개 공고 보기
sqlite3 data/daangn_jobs.db "SELECT title, salary_amount, address FROM jobs ORDER BY collected_at DESC LIMIT 5"

# 월급 공고만 보기
sqlite3 data/daangn_jobs.db "SELECT title, salary_amount FROM jobs WHERE salary_type = '월급'"
```

---

## 에러 해결

### ChromeDriver 오류
Chrome 브라우저가 설치되어 있는지 확인하세요. ChromeDriver는 자동 설치됩니다.

### 페이지 로딩 타임아웃
인터넷 연결을 확인하고, `--headless` 없이 GUI 모드로 실행해 보세요.

### 수집된 데이터가 없음
당근알바 페이지 구조가 변경되었을 수 있습니다. CSS Selector 업데이트가 필요합니다.

---

## 관련 파일

- `scripts/scrape_daangn.py` - 메인 크롤러 스크립트
- `data/daangn_jobs.db` - SQLite 데이터베이스
