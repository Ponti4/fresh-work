#!/usr/bin/env python3
"""
지피터스(gpters.org) 멤버 프로필에서 게시물을 스크래핑하여 Markdown으로 저장하는 스크립트

Usage:
    python scrape_posts.py --profile-url "https://www.gpters.org/member/WZlPiwwnpW"
    python scrape_posts.py --profile-url "URL" --max-results 20 --headless

Output:
    JSON 형식으로 처리 결과 요약 출력 (stdout)
    에러 발생 시 JSON 에러 출력 (stderr)

Requirements:
    pip install selenium webdriver-manager beautifulsoup4 lxml
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError as e:
    print(json.dumps({
        "error": "필요한 모듈을 import할 수 없습니다.",
        "detail": str(e),
        "install": "pip install selenium webdriver-manager"
    }))
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print(json.dumps({
        "error": "BeautifulSoup이 설치되어 있지 않습니다.",
        "install": "pip install beautifulsoup4"
    }))
    sys.exit(1)


# ===== 1. Selenium 설정 =====

def setup_driver(headless=False):
    """
    Chrome WebDriver 설정 및 초기화

    Args:
        headless (bool): 헤드리스 모드 활성화 여부

    Returns:
        webdriver.Chrome: 설정된 WebDriver 인스턴스
    """
    options = Options()

    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

    # 안정성 향상 옵션
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')

    # User-Agent 설정 (일반 브라우저처럼 보이도록)
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        raise Exception(f"ChromeDriver 초기화 실패: {str(e)}")


# ===== 2. 페이지 로딩 =====

def load_profile_page(driver, profile_url):
    """
    프로필 페이지 로드 및 동적 콘텐츠 대기

    Args:
        driver: Selenium WebDriver
        profile_url: 프로필 URL

    Returns:
        bool: 로딩 성공 여부
    """
    try:
        driver.get(profile_url)

        # 1단계: 기본 페이지 로드 (5초 대기)
        time.sleep(5)

        # 2단계: 게시물 컨테이너 로딩 대기 (최대 15초)
        # 다양한 selector를 시도합니다
        wait = WebDriverWait(driver, 15)

        try:
            # 첫 번째 시도: article 태그
            posts_container = wait.until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
            )
        except:
            try:
                # 두 번째 시도: data-testid 속성
                posts_container = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid*='post']"))
                )
            except:
                # 세 번째 시도: 일반 콘텐츠 div
                posts_container = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='content']"))
                )

        # 3단계: JavaScript 렌더링 완료 대기 (추가 3초)
        time.sleep(3)

        return True

    except Exception as e:
        print(f"페이지 로딩 실패: {str(e)}", file=sys.stderr)
        return False


# ===== 3. 게시물 파싱 =====

def parse_date(date_str):
    """
    다양한 형식의 날짜 문자열을 YYYY-MM-DD로 변환

    Args:
        date_str: 날짜 문자열

    Returns:
        str: YYYY-MM-DD 형식 또는 현재 날짜
    """
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d')

    try:
        # ISO 8601 형식 (2025-01-06T12:00:00Z)
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d')

        # YYYY-MM-DD 형식 (이미 정규화됨)
        if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
            return date_str[:10]

        # 상대 시간 처리 ("2일 전", "방금 전" 등)
        if '전' in date_str or 'ago' in date_str.lower():
            return datetime.now().strftime('%Y-%m-%d')

        # 파싱 실패 시 현재 날짜
        return datetime.now().strftime('%Y-%m-%d')

    except Exception:
        return datetime.now().strftime('%Y-%m-%d')


def html_to_markdown(element):
    """
    HTML 요소를 Markdown으로 변환 (간이 변환기)
    - 텍스트는 그대로 유지
    - 이미지는 ![alt](src) 형식으로 변환
    - 링크는 [text](href) 형식으로 변환
    """
    if not element:
        return ""

    markdown_parts = []
    
    # 재귀적으로 자식 요소를 순회하며 처리
    # (BeautifulSoup의 .descendants는 너무 세세하므로, 주요 블록 단위로 처리)
    
    # 1. 텍스트 노드 처리 (태그가 아닌 경우)
    if isinstance(element, str):
        text = element.strip()
        return text if text else ""

    # 2. 자식 요소 순회
    for child in element.children:
        if child.name is None: # 텍스트 노드
            text = str(child).strip()
            if text:
                markdown_parts.append(text)
        
        elif child.name == 'img':
            src = child.get('src', '')
            alt = child.get('alt', '')
            if src:
                markdown_parts.append(f"\n![{alt}]({src})\n")
        
        elif child.name == 'a':
            href = child.get('href', '')
            text = html_to_markdown(child)
            if href:
                markdown_parts.append(f"[{text}]({href})")
            else:
                markdown_parts.append(text)
                
        elif child.name in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']:
            # 블록 요소는 내용을 변환하고 개행 추가
            # figure 내의 div 등은 이미지 처리를 위해 재귀 호출
            content = html_to_markdown(child)
            if content:
                # 헤딩 처리
                if child.name.startswith('h'):
                    level = int(child.name[1])
                    markdown_parts.append(f"\n{'#' * level} {content}\n")
                elif child.name == 'li':
                    markdown_parts.append(f"- {content}")
                else:
                    markdown_parts.append(f"{content}\n")
        
        elif child.name == 'figure':
            # figure 태그 처리: 내부의 img만 추출하고 나머지(중복 캡션 등)는 무시하거나 선택적 포함
            # sample.html 구조상 figure 안에 img와 캡션이 혼재함.
            # 여기서는 figure 내부를 순회하되, img는 살리고 'ALT' 라벨 등은 건너뜀
            imgs = child.find_all('img')
            for img in imgs:
                src = img.get('src', '')
                alt = img.get('alt', '')
                if src:
                    markdown_parts.append(f"\n![{alt}]({src})\n")
            # 캡션(figcaption 또는 p)은 이미지가 있으면 생략하거나 필요시 추가
            # 여기서는 이미지 ALT와 중복되는 경우가 많아 생략하거나 텍스트만 추출
            
        elif child.name in ['ul', 'ol']:
            content = html_to_markdown(child)
            if content:
                markdown_parts.append(f"\n{content}\n")
                
        elif child.name == 'pre':
             # 코드 블록 처리
             code = child.get_text()
             markdown_parts.append(f"\n```\n{code}\n```\n")
             
        elif child.name == 'code':
             # 인라인 코드
             markdown_parts.append(f"`{child.get_text()}`")

        else:
            # 기타 태그는 재귀적으로 내용만 추출
            markdown_parts.append(html_to_markdown(child))

    return "\n".join(markdown_parts).replace("\n\n\n", "\n\n")


def parse_posts(driver, max_results=10):
    """
    페이지에서 게시물 데이터 추출

    Args:
        driver: Selenium WebDriver
        max_results: 최대 수집 개수

    Returns:
        list[dict]: 게시물 데이터 목록
    """
    posts_data = []

    try:
        # 페이지 소스를 BeautifulSoup으로 파싱
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # CSS Selector로 게시물 요소 추출 (순서 변경: 카드 컨테이너를 먼저 찾아야 링크와 본문을 모두 잡을 수 있음)
        post_elements = None

        # 시도 1: class 기반 post-card (가장 확실한 단위)
        post_elements = soup.select('.post-card, [class*="post-card"]')
        
        if not post_elements:
            # 시도 2: data-testid 속성
            post_elements = soup.select('[data-testid*="post"]')
            
        if not post_elements:
            # 시도 3: article 태그 (최후의 보루)
            post_elements = soup.select('article')
            
        if not post_elements:
            # 시도 4: 일반적인 post/content 클래스
            post_elements = soup.select('[class*="post"], [class*="content"]')

        if not post_elements:
            print(f"게시물 요소를 찾을 수 없습니다.", file=sys.stderr)
            return posts_data

        # 최대 개수까지만 처리
        post_elements = post_elements[:max_results]

        for idx, post in enumerate(post_elements, 1):
            try:
                # URL 추출 (개선된 로직: 모든 a 태그 중 /post/ 패턴 검색)
                url = ''
                links = post.select('a[href]')
                for link in links:
                    href = link.get('href', '')
                    if '/post/' in href or '/content/' in href:
                        # 댓글 링크(#replies) 등은 제외하고 싶다면 조건 추가 가능
                        if '#replies' not in href:
                            url = href
                            break
                
                # 절대 URL로 변환
                if url:
                    if not url.startswith('http'):
                        if url.startswith('/'):
                            url = f"https://www.gpters.org{url}"
                        else:
                            url = f"https://www.gpters.org/{url}"

                # 제목 추출 (다양한 selector 시도)
                title = ''
                title_elem = post.select_one('h2, h3, .title, [class*="title"]')
                if title_elem:
                    title = title_elem.get_text(strip=True)
                
                # 제목을 못 찾았고 URL이 있다면, URL의 slug를 활용하거나 본문 앞부분 사용
                if not title:
                    if url:
                        # 예: .../post/title-slug-hash -> title slug
                        parts = url.split('/')
                        if parts:
                            slug = parts[-1].split('-')[:-1] # 마지막 해시 제외 시도
                            if slug:
                                title = ' '.join(slug)
                    
                    if not title:
                        title = f"제목없음_{idx}"

                # 작성일 추출 (다양한 selector 시도)
                date_elem = post.select_one('time, [class*="date"], [class*="published"]')
                date_str = date_elem.get('datetime') or date_elem.get_text(strip=True) if date_elem else ''
                published_date = parse_date(date_str)

                # 요약/본문 추출 (업데이트: HTML to Markdown 변환 적용)
                content_elem = post.select_one('article.prose, .post-content, .content, .summary, .description')
                if content_elem:
                    # 사용자 정의 변환 함수 사용
                    summary = html_to_markdown(content_elem)
                    # 불필요한 공백 정리
                    summary = re.sub(r'\n{3,}', '\n\n', summary).strip()
                else:
                    summary_elem = post.select_one('p')
                    summary = summary_elem.get_text(strip=True) if summary_elem else ''

                # 데이터 추가
                posts_data.append({
                    'title': title,
                    'url': url,
                    'published_date': published_date,
                    'summary': summary,
                })

            except Exception as e:
                print(f"게시물 {idx} 파싱 오류: {str(e)}", file=sys.stderr)
                continue

        return posts_data

    except Exception as e:
        print(f"게시물 목록 파싱 실패: {str(e)}", file=sys.stderr)
        return posts_data


# ===== 4. 파일 저장 =====

def sanitize_filename(title, max_length=50):
    """
    제목을 Windows 호환 파일명으로 정규화

    Args:
        title: 원본 제목
        max_length: 최대 길이

    Returns:
        str: 정규화된 파일명 (확장자 제외)
    """
    # Windows 금지 문자 제거
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)

    # 공백을 언더스코어로 변경
    safe_title = safe_title.replace(' ', '_')

    # 연속된 언더스코어 제거
    safe_title = re.sub(r'_+', '_', safe_title)

    # 양쪽 언더스코어 제거
    safe_title = safe_title.strip('_')

    # 길이 제한
    if len(safe_title) > max_length:
        safe_title = safe_title[:max_length].rstrip('_')

    # 빈 문자열 방지
    if not safe_title:
        safe_title = 'untitled'

    return safe_title


def generate_filename(post_data):
    """
    게시물 데이터로부터 파일명 생성

    Args:
        post_data: {'title': str, 'published_date': str, ...}

    Returns:
        str: YYYYMMDD_title.md 형식 파일명
    """
    # 날짜 추출 (YYYY-MM-DD → YYYYMMDD)
    date = post_data.get('published_date', '')
    date_prefix = date.replace('-', '') if date else datetime.now().strftime('%Y%m%d')

    # 제목 정규화
    title = post_data.get('title', 'untitled')
    safe_title = sanitize_filename(title, max_length=50)

    return f"{date_prefix}_{safe_title}.md"


def generate_markdown(post_data):
    """
    게시물 데이터를 Markdown 형식으로 변환

    Args:
        post_data: {'title', 'url', 'published_date', 'summary'}

    Returns:
        str: Markdown 문자열
    """
    title = post_data.get('title', '제목 없음')
    url = post_data.get('url', '')
    published_date = post_data.get('published_date', '')
    summary = post_data.get('summary', '요약 없음')

    # Markdown 템플릿
    markdown = f"""# {title}

- **작성일**: {published_date}
- **URL**: [{url}]({url})

## 요약
{summary}

---

**수집 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    return markdown


def save_posts_to_markdown(posts_data, output_dir='docs/notes/gpters_editor_soyeon', skip_existing=True):
    """
    게시물 데이터를 Markdown 파일로 저장

    Args:
        posts_data: 게시물 데이터 목록
        output_dir: 저장 경로
        skip_existing: 중복 파일 건너뛰기

    Returns:
        dict: {'saved': int, 'skipped': int, 'saved_files': list, 'errors': list}
    """
    result = {
        'saved': 0,
        'skipped': 0,
        'saved_files': [],
        'errors': []
    }

    # 디렉토리 생성
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for post in posts_data:
        try:
            # 파일명 생성
            filename = generate_filename(post)
            file_path = output_path / filename

            # 중복 체크
            if skip_existing and file_path.exists():
                result['skipped'] += 1
                continue

            # Markdown 내용 생성
            markdown_content = generate_markdown(post)

            # UTF-8 인코딩으로 저장 (Windows 한글 처리)
            file_path.write_text(markdown_content, encoding='utf-8')

            result['saved'] += 1
            result['saved_files'].append(filename)

        except Exception as e:
            result['errors'].append({
                'title': post.get('title', 'Unknown'),
                'error': str(e)
            })

    return result


# ===== 5. 통합 실행 =====

def scrape_posts(profile_url, max_results=10, headless=False):
    """
    메인 스크래핑 함수

    Args:
        profile_url: 프로필 URL
        max_results: 최대 수집 개수
        headless: 헤드리스 모드 여부

    Returns:
        list[dict]: 게시물 데이터 목록
    """
    driver = None
    posts = []

    try:
        driver = setup_driver(headless)

        if not load_profile_page(driver, profile_url):
            return posts

        posts = parse_posts(driver, max_results)

        if posts:
            print(f"[수집 완료] 총 {len(posts)}개 게시물 수집")

    except Exception as e:
        print(f"[오류] 스크래핑 중 오류 발생: {str(e)}", file=sys.stderr)
        raise

    finally:
        if driver:
            driver.quit()

    return posts


def main():
    """CLI 진입점"""
    parser = argparse.ArgumentParser(description='지피터스 게시물 스크래핑')
    parser.add_argument('--profile-url', required=True, help='프로필 URL (필수)')
    parser.add_argument('--max-results', type=int, default=10, help='최대 수집 개수 (기본: 10)')
    parser.add_argument('--output-dir', default='docs/notes/gpters_editor_soyeon', help='저장 경로')
    parser.add_argument('--headless', action='store_true', help='헤드리스 모드')
    parser.add_argument('--no-skip', action='store_true', help='중복 파일 덮어쓰기')

    args = parser.parse_args()

    result = {
        'status': 'started',
        'profile_url': args.profile_url,
        'collected_at': datetime.now().isoformat(),
        'collected': 0,
        'saved': 0,
        'skipped': 0,
        'saved_files': [],
        'errors': []
    }

    try:
        print(f"[시작] 스크래핑: {args.profile_url}")

        # 게시물 수집
        posts = scrape_posts(args.profile_url, args.max_results, args.headless)
        result['collected'] = len(posts)

        if posts:
            print(f"[저장] {args.output_dir}에 저장 중...")

            # 파일 저장
            save_result = save_posts_to_markdown(
                posts,
                args.output_dir,
                skip_existing=not args.no_skip
            )

            # 결과 병합
            result['saved'] = save_result['saved']
            result['skipped'] = save_result['skipped']
            result['saved_files'] = save_result['saved_files']
            result['errors'] = save_result['errors']
            result['status'] = 'success'

            print(f"[완료] {result['saved']}개 저장, {result['skipped']}개 건너뜀")
        else:
            result['status'] = 'no_posts'
            print("[정보] 수집된 게시물이 없습니다.")

        # JSON 출력
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        result['status'] = 'error'
        result['errors'].append({
            'type': 'critical',
            'message': str(e)
        })
        print(json.dumps(result, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
