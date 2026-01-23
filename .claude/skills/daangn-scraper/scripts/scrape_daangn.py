#!/usr/bin/env python3
"""
당근알바 구인 공고 크롤러

Usage:
    python scrape_daangn.py
    python scrape_daangn.py --max-jobs 50 --headless
    python scrape_daangn.py --db-path data/jobs.db

Output:
    JSON 형식으로 처리 결과 요약 출력 (stdout)

Requirements:
    pip install selenium webdriver-manager beautifulsoup4 lxml
"""

import argparse
import json
import re
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

# Selenium imports
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError as e:
    print(json.dumps({
        "status": "error",
        "error_type": "ImportError",
        "message": f"Selenium 설치 필요: {e}",
        "install": "pip install selenium webdriver-manager"
    }, ensure_ascii=False))
    sys.exit(1)

# BeautifulSoup import
try:
    from bs4 import BeautifulSoup
except ImportError:
    print(json.dumps({
        "status": "error",
        "error_type": "ImportError",
        "message": "BeautifulSoup 설치 필요",
        "install": "pip install beautifulsoup4 lxml"
    }, ensure_ascii=False))
    sys.exit(1)


# ===== 상수 =====
BASE_URL = "https://www.daangn.com"
JOBS_LIST_URL = f"{BASE_URL}/kr/jobs/"
DEFAULT_DB_PATH = "data/daangn_jobs.db"


# ===== 에러 클래스 =====
class DaangnScraperError(Exception):
    """기본 에러 클래스"""
    pass


class PageLoadError(DaangnScraperError):
    """페이지 로딩 실패"""
    pass


class DatabaseError(DaangnScraperError):
    """DB 저장 실패"""
    pass


# ===== 유틸리티 함수 =====
def safe_extract(element, selector, attribute=None, default=None):
    """
    안전하게 데이터 추출 (None 반환, 예외 없음)

    Args:
        element: BeautifulSoup 요소
        selector: CSS 선택자
        attribute: 추출할 속성 (없으면 텍스트)
        default: 기본값

    Returns:
        추출된 값 또는 기본값
    """
    try:
        found = element.select_one(selector)
        if found is None:
            return default
        if attribute:
            return found.get(attribute, default)
        text = found.get_text(strip=True)
        return text if text else default
    except Exception:
        return default


def safe_extract_all(element, selector, attribute=None):
    """
    안전하게 여러 요소 추출

    Returns:
        리스트 (빈 리스트 가능)
    """
    try:
        found_list = element.select(selector)
        if not found_list:
            return []
        if attribute:
            return [el.get(attribute) for el in found_list if el.get(attribute)]
        return [el.get_text(strip=True) for el in found_list if el.get_text(strip=True)]
    except Exception:
        return []


def parse_number(text, default=0):
    """
    텍스트에서 숫자 추출

    Args:
        text: "37.2°C", "43개", "11명" 등
        default: 기본값

    Returns:
        int 또는 float
    """
    if not text:
        return default
    try:
        # 숫자와 소수점만 추출
        numbers = re.findall(r'[\d.]+', str(text))
        if numbers:
            num_str = numbers[0]
            return float(num_str) if '.' in num_str else int(num_str)
        return default
    except Exception:
        return default


# ===== DB 함수 =====
def init_db(db_path):
    """
    SQLite DB 초기화 (테이블 생성)

    Args:
        db_path: DB 파일 경로
    """
    # 디렉토리 생성
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- 기본 정보
            title TEXT NOT NULL,
            company TEXT,
            address TEXT,

            -- 급여/근무 조건
            salary_type TEXT,
            salary_amount TEXT,
            work_days TEXT,
            work_hours TEXT,
            negotiable BOOLEAN DEFAULT FALSE,

            -- 직무 내용
            job_description TEXT,

            -- 작성자 정보
            author_nickname TEXT,
            author_region TEXT,
            manner_temp REAL,
            badges TEXT,
            review_count INTEGER DEFAULT 0,

            -- 공고 통계
            applicant_count INTEGER DEFAULT 0,
            interest_count INTEGER DEFAULT 0,
            posted_at TEXT,

            -- 메타
            url TEXT UNIQUE NOT NULL,
            collected_at TEXT NOT NULL,
            updated_at TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_url ON jobs(url)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_posted_at ON jobs(posted_at)")

    conn.commit()
    conn.close()


def is_duplicate(url, db_path):
    """
    URL이 이미 DB에 있는지 확인

    Returns:
        bool: True if duplicate
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM jobs WHERE url = ?", (url,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception:
        return False


def save_to_db(job_data, db_path):
    """
    공고 데이터를 DB에 저장

    Args:
        job_data: dict
        db_path: DB 파일 경로

    Returns:
        bool: 성공 여부
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # badges를 JSON 문자열로 변환
        badges = job_data.get('badges', [])
        badges_json = json.dumps(badges, ensure_ascii=False) if badges else '[]'

        cursor.execute("""
            INSERT OR REPLACE INTO jobs (
                title, company, address,
                salary_type, salary_amount, work_days, work_hours, negotiable,
                job_description,
                author_nickname, author_region, manner_temp, badges, review_count,
                applicant_count, interest_count, posted_at,
                url, collected_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job_data.get('title', '제목없음'),
            job_data.get('company'),
            job_data.get('address'),
            job_data.get('salary_type'),
            job_data.get('salary_amount'),
            job_data.get('work_days'),
            job_data.get('work_hours'),
            job_data.get('negotiable', False),
            job_data.get('job_description'),
            job_data.get('author_nickname', '익명'),
            job_data.get('author_region'),
            job_data.get('manner_temp'),
            badges_json,
            job_data.get('review_count', 0),
            job_data.get('applicant_count', 0),
            job_data.get('interest_count', 0),
            job_data.get('posted_at'),
            job_data.get('url'),
            job_data.get('collected_at'),
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"[DB 에러] {e}", file=sys.stderr)
        return False


# ===== Selenium 설정 =====
def setup_driver(headless=True):
    """
    Chrome WebDriver 설정

    Args:
        headless: 헤드리스 모드 여부

    Returns:
        webdriver.Chrome
    """
    options = Options()

    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

    # 안정성 옵션
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1920,1080')

    # User-Agent
    options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        raise DaangnScraperError(f"ChromeDriver 초기화 실패: {e}")


# ===== 크롤링 함수 =====
def crawl_job_list(driver, max_scroll=10, max_jobs=100):
    """
    목록 페이지에서 공고 URL 추출

    Args:
        driver: Selenium WebDriver
        max_scroll: 최대 스크롤 횟수
        max_jobs: 최대 수집 공고 수

    Returns:
        list[str]: 공고 URL 목록
    """
    urls = set()

    try:
        driver.get(JOBS_LIST_URL)
        time.sleep(3)  # 초기 로딩 대기

        for scroll_count in range(max_scroll):
            # 현재 페이지의 공고 링크 추출
            soup = BeautifulSoup(driver.page_source, 'lxml')

            # 공고 링크 찾기 (href에 /kr/jobs/ 포함)
            job_links = soup.select('a[href*="/kr/jobs/"]')

            for link in job_links:
                href = link.get('href', '')
                # 목록 페이지 자체는 제외
                if href and href != '/kr/jobs/' and not href.endswith('/about/'):
                    full_url = f"{BASE_URL}{href}" if href.startswith('/') else href
                    # 쿼리 파라미터 제거
                    full_url = full_url.split('?')[0]
                    # 목록 페이지 URL 제외 (상세 페이지는 /kr/jobs/제목-해시/ 형태)
                    if full_url.rstrip('/').endswith('/kr/jobs'):
                        continue
                    urls.add(full_url)

            # 최대 개수 도달 시 종료
            if len(urls) >= max_jobs:
                break

            # 스크롤 다운
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 로딩 대기

            # 더 이상 새 콘텐츠가 없으면 종료
            new_height = driver.execute_script("return document.body.scrollHeight")
            if scroll_count > 0:
                if new_height == driver.execute_script("return document.body.scrollHeight"):
                    break

        return list(urls)[:max_jobs]

    except TimeoutException:
        raise PageLoadError("목록 페이지 로딩 타임아웃")
    except Exception as e:
        raise PageLoadError(f"목록 페이지 크롤링 실패: {e}")


def extract_json_data(soup):
    """
    페이지에서 JSON-LD 또는 __remixContext 데이터 추출

    Returns:
        dict | None: JSON 데이터
    """
    # 방법 1: JSON-LD 스키마 추출
    json_ld = soup.select_one('script[type="application/ld+json"]')
    if json_ld:
        try:
            data = json.loads(json_ld.string)
            if data:
                return {'source': 'json-ld', 'data': data}
        except Exception:
            pass

    # 방법 2: __remixContext에서 추출 (React 앱)
    scripts = soup.select('script')
    for script in scripts:
        if script.string and '__remixContext' in script.string:
            try:
                # __remixContext = {...} 형태에서 JSON 추출
                match = re.search(r'__remixContext\s*=\s*({.*?});?\s*(?:</script>|$)', script.string, re.DOTALL)
                if match:
                    data = json.loads(match.group(1))
                    return {'source': 'remix', 'data': data}
            except Exception:
                pass

    return None


def parse_salary_type(salary_type_code):
    """
    급여 유형 코드를 한글로 변환

    Args:
        salary_type_code: "HOURLY", "DAILY", "MONTHLY", "PER_CASE" 등
    """
    mapping = {
        'HOURLY': '시급',
        'DAILY': '일당',
        'MONTHLY': '월급',
        'PER_CASE': '건당',
        'WEEKLY': '주급',
    }
    return mapping.get(salary_type_code, salary_type_code)


def format_salary(amount, salary_type):
    """
    급여 금액 포맷팅

    Args:
        amount: 숫자 (예: 10320)
        salary_type: 한글 유형 (예: "시급")
    """
    if not amount:
        return None
    try:
        amount = int(amount)
        if amount >= 10000:
            만원 = amount // 10000
            나머지 = amount % 10000
            if 나머지 == 0:
                return f"{salary_type} {만원}만원"
            else:
                return f"{salary_type} {만원}만{나머지}원"
        else:
            return f"{salary_type} {amount:,}원"
    except Exception:
        return f"{salary_type} {amount}"


def crawl_job_detail(driver, url, retry=3):
    """
    상세 페이지에서 공고 정보 추출

    Args:
        driver: Selenium WebDriver
        url: 공고 URL
        retry: 재시도 횟수

    Returns:
        dict | None: 공고 데이터 또는 None
    """
    for attempt in range(retry):
        try:
            driver.get(url)
            time.sleep(2)  # 렌더링 대기

            soup = BeautifulSoup(driver.page_source, 'lxml')
            page_text = soup.get_text()

            # JSON 데이터 추출 시도
            json_result = extract_json_data(soup)

            # 기본값 초기화
            title = None
            company = None
            address = None
            salary_type = None
            salary_amount = None
            work_days = None
            work_hours = None
            job_description = None
            author_nickname = None
            author_region = None
            manner_temp = None
            badges = []
            review_count = 0
            applicant_count = 0
            interest_count = 0
            posted_at = None

            # JSON-LD에서 데이터 추출
            if json_result and json_result['source'] == 'json-ld':
                data = json_result['data']
                title = data.get('title')
                job_description = data.get('description')
                if 'hiringOrganization' in data:
                    company = data['hiringOrganization'].get('name')
                if 'jobLocation' in data:
                    loc = data['jobLocation']
                    if isinstance(loc, dict) and 'address' in loc:
                        addr = loc['address']
                        if isinstance(addr, dict):
                            address = addr.get('streetAddress') or addr.get('addressLocality')
                        else:
                            address = str(addr)
                if 'baseSalary' in data:
                    sal = data['baseSalary']
                    if isinstance(sal, dict):
                        salary_amount = sal.get('value', {}).get('value')
                        unit = sal.get('value', {}).get('unitText', '')
                        if 'HOUR' in unit.upper():
                            salary_type = '시급'
                        elif 'DAY' in unit.upper():
                            salary_type = '일당'
                        elif 'MONTH' in unit.upper():
                            salary_type = '월급'
                posted_at = data.get('datePosted')

            # HTML에서 추가 데이터 추출 (JSON에서 못 찾은 경우)
            if not title:
                title = safe_extract(soup, 'h1', default='제목없음')

            if not company:
                company = (
                    safe_extract(soup, '[class*="business"]') or
                    safe_extract(soup, '[class*="store"]') or
                    safe_extract(soup, '[class*="company"]')
                )

            if not address:
                address = (
                    safe_extract(soup, '[class*="address"]') or
                    safe_extract(soup, '[class*="location"]')
                )

            # 급여 정보 (HTML에서)
            if not salary_amount:
                # 페이지 텍스트에서 급여 패턴 찾기 (다양한 형식 지원)
                salary_patterns = [
                    # "시급 1만 320원", "시급 1만원", "시급 12,000원"
                    r'(시급|일당|일비|월급|건당)\s*(\d+만?\s*\d*,?\d*)\s*원',
                    # "월 180만원", "월 200만원"
                    r'(월)\s*(\d+만?\s*\d*,?\d*)\s*원',
                ]
                for pattern in salary_patterns:
                    match = re.search(pattern, page_text)
                    if match:
                        type_str = match.group(1)
                        amount_str = match.group(2)

                        # 급여 유형 정규화
                        if type_str == '일비':
                            salary_type = '일당'
                        elif type_str == '월':
                            salary_type = '월급'
                        else:
                            salary_type = type_str

                        # 금액 정규화 ("1만 320" -> "1만 320원")
                        salary_amount = f"{salary_type} {amount_str}원"
                        break

            # 근무 요일/시간 (HTML에서)
            if not work_days:
                # 요일 패턴 찾기
                days_match = re.search(r'(월|화|수|목|금|토|일)[\s,]*(월|화|수|목|금|토|일)?[\s,]*(월|화|수|목|금|토|일)?', page_text)
                if days_match:
                    work_days = ', '.join([d for d in days_match.groups() if d])

            if not work_hours:
                # 시간 패턴 찾기 (예: 09:00~18:00)
                time_match = re.search(r'(\d{1,2}:\d{2})\s*[~\-]\s*(\d{1,2}:\d{2})', page_text)
                if time_match:
                    work_hours = f"{time_match.group(1)}~{time_match.group(2)}"

            # 상세내용 (HTML에서 추출)
            if not job_description:
                # "상세 내용" 다음에 나오는 텍스트 추출
                desc_match = re.search(r'상세 내용(.+?)(?:지원자|관심|공유|신고|채팅)', page_text, re.DOTALL)
                if desc_match:
                    job_description = desc_match.group(1).strip()
                    # 너무 길면 자르기
                    if len(job_description) > 2000:
                        job_description = job_description[:2000] + '...'

            # 협의 가능 여부
            negotiable = '협의' in page_text or '조정 가능' in page_text

            # 작성자 정보
            if not author_nickname:
                author_nickname = (
                    safe_extract(soup, '[class*="nickname"]') or
                    safe_extract(soup, '[class*="author"]') or
                    safe_extract(soup, '[class*="profile-name"]') or
                    '익명'
                )

            if not author_region:
                author_region = safe_extract(soup, '[class*="region"]')

            # 매너온도
            manner_match = re.search(r'(\d{2}\.?\d?)\s*°?C?', page_text)
            if manner_match:
                temp_val = float(manner_match.group(1))
                if 30 <= temp_val <= 100:  # 매너온도 범위 체크
                    manner_temp = temp_val

            # 배지
            badges = safe_extract_all(soup, '[class*="badge"]')
            if not badges:
                # 텍스트에서 배지 키워드 찾기
                badge_keywords = ['모범 구인자', '모범구인자', '빠른응답', '당일지급']
                badges = [kw for kw in badge_keywords if kw in page_text]

            # 후기/지원자/관심 수
            review_match = re.search(r'후기\s*(\d+)', page_text)
            if review_match:
                review_count = int(review_match.group(1))

            applicant_match = re.search(r'지원자?\s*(\d+)', page_text)
            if applicant_match:
                applicant_count = int(applicant_match.group(1))

            interest_match = re.search(r'관심\s*(\d+)', page_text)
            if interest_match:
                interest_count = int(interest_match.group(1))

            return {
                'title': title or '제목없음',
                'company': company,
                'address': address,
                'salary_type': salary_type,
                'salary_amount': salary_amount,
                'work_days': work_days,
                'work_hours': work_hours,
                'negotiable': negotiable,
                'job_description': job_description,
                'author_nickname': author_nickname or '익명',
                'author_region': author_region,
                'manner_temp': manner_temp,
                'badges': badges,
                'review_count': review_count,
                'applicant_count': applicant_count,
                'interest_count': interest_count,
                'posted_at': posted_at,
                'url': url,
                'collected_at': datetime.now().isoformat()
            }

        except TimeoutException:
            if attempt < retry - 1:
                time.sleep(5)
                continue
            print(f"[타임아웃] {url}", file=sys.stderr)
            return None

        except Exception as e:
            if attempt < retry - 1:
                time.sleep(5)
                continue
            print(f"[파싱 에러] {url}: {e}", file=sys.stderr)
            return None

    return None


# ===== 메인 함수 =====
def main(max_jobs=100, headless=True, db_path=DEFAULT_DB_PATH):
    """
    메인 크롤링 함수

    Args:
        max_jobs: 최대 수집 공고 수
        headless: 헤드리스 모드
        db_path: DB 파일 경로
    """
    result = {
        'status': 'started',
        'collected_at': datetime.now().isoformat(),
        'total_found': 0,
        'new_saved': 0,
        'duplicates_skipped': 0,
        'errors': 0,
        'db_path': db_path
    }

    driver = None

    try:
        # DB 초기화
        init_db(db_path)

        # 드라이버 설정
        driver = setup_driver(headless)

        # 1단계: 목록 페이지에서 URL 수집
        print(f"[시작] 당근알바 크롤링 (최대 {max_jobs}개)", file=sys.stderr)
        job_urls = crawl_job_list(driver, max_scroll=20, max_jobs=max_jobs)
        result['total_found'] = len(job_urls)
        print(f"[목록] {len(job_urls)}개 공고 URL 발견", file=sys.stderr)

        # 2단계: 각 상세 페이지 크롤링
        for idx, url in enumerate(job_urls, 1):
            # 중복 체크
            if is_duplicate(url, db_path):
                result['duplicates_skipped'] += 1
                continue

            # 상세 페이지 크롤링
            job_data = crawl_job_detail(driver, url)

            if job_data:
                # DB 저장
                if save_to_db(job_data, db_path):
                    result['new_saved'] += 1
                    print(f"[{idx}/{len(job_urls)}] 저장: {job_data.get('title', '')[:30]}", file=sys.stderr)
                else:
                    result['errors'] += 1
            else:
                result['errors'] += 1

            # 요청 간격 (서버 부하 방지)
            time.sleep(1)

        result['status'] = 'success'

    except PageLoadError as e:
        result['status'] = 'error'
        result['error_type'] = 'PageLoadError'
        result['message'] = str(e)

    except DaangnScraperError as e:
        result['status'] = 'error'
        result['error_type'] = 'DaangnScraperError'
        result['message'] = str(e)

    except Exception as e:
        result['status'] = 'error'
        result['error_type'] = type(e).__name__
        result['message'] = str(e)

    finally:
        if driver:
            driver.quit()

    # JSON 출력
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if result['status'] == 'error':
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='당근알바 구인 공고 크롤러')
    parser.add_argument('--max-jobs', type=int, default=100, help='최대 수집 공고 수 (기본: 100)')
    parser.add_argument('--headless', action='store_true', help='헤드리스 모드 (브라우저 숨김)')
    parser.add_argument('--db-path', default=DEFAULT_DB_PATH, help=f'DB 파일 경로 (기본: {DEFAULT_DB_PATH})')

    args = parser.parse_args()

    main(
        max_jobs=args.max_jobs,
        headless=args.headless,
        db_path=args.db_path
    )
