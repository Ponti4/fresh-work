# CSS Selector 유지보수 가이드

## 개요

이 문서는 지피터스 웹사이트 구조가 변경될 때 CSS Selector를 업데이트하는 방법을 설명합니다.

---

## 초기 설정 (2026-01-06)

**중요**: 첫 실행 전에 selector를 **반드시 수동으로 검증**해야 합니다.

### Selector 검증 단계

#### 1단계: 페이지 열기
```
1. Chrome 브라우저 열기
2. 주소창에 입력: https://www.gpters.org/member/WZlPiwwnpW
3. 페이지 완전 로드 대기 (5-10초)
```

#### 2단계: DevTools 열기
```
1. F12 키 누르기 (또는 우클릭 → 검사)
2. Elements 탭 확인
3. 게시물 영역으로 마우스 이동하여 하이라이트 확인
```

#### 3단계: HTML 구조 파악
```
게시물 목록의 HTML 구조 예시:

<article>
  <h2 class="title">게시물 제목</h2>
  <a href="/post/123" class="post-link">링크</a>
  <time datetime="2025-01-06">2025-01-06</time>
  <p class="summary">게시물 요약...</p>
</article>

또는:

<div data-testid="post">
  <h3>제목</h3>
  <a href="/post/456">URL</a>
  <span class="date">2025-01-05</span>
  <div class="content">요약</div>
</div>
```

#### 4단계: Console에서 Selector 테스트
```javascript
// Chrome DevTools Console 탭에서 실행

// 게시물 목록 찾기
$$('article')                    // 결과: [article, article, ...]
$$('[data-testid="post"]')       // 또는 이것
$$('[class*="post-item"]')       // 또는 이것

// 첫 번째 게시물에서 제목 추출
$$('article')[0].querySelector('h2')       // <h2> 태그 찾기
$$('article')[0].querySelector('.title')   // .title 클래스 찾기

// URL 추출
$$('article')[0].querySelector('a[href*="/post/"]')   // href 속성 포함 <a>

// 날짜 추출
$$('article')[0].querySelector('time')     // <time> 태그
$$('article')[0].querySelector('[class*="date"]')     // date 포함 클래스

// 요약 추출
$$('article')[0].querySelector('p')        // <p> 태그
$$('article')[0].querySelector('.summary') // .summary 클래스
```

### 현재 Selector (검증 대기 중)

**파일 위치**: `scrape_posts.py`

| 항목 | Selector | 대체 옵션 | 상태 |
|------|----------|----------|------|
| **게시물 컨테이너** | `article` | `[data-testid="post"]`, `[class*="post"]` | ⏳ 검증 필요 |
| **제목** | `h2, h3, .title` | `[class*="title"]`, `.post-title` | ⏳ 검증 필요 |
| **링크** | `a[href*="/post/"]` | `a[href*="/content/"]` | ⏳ 검증 필요 |
| **작성일** | `time, [class*="date"]` | `[class*="published"]` | ⏳ 검증 필요 |
| **요약** | `.summary, .description, p` | `[class*="excerpt"]` | ⏳ 검증 필요 |

---

## Selector 업데이트 방법

### 문제 증상

**에러 메시지**:
```
Page load failed: no such element: Unable to locate element: {"method":"css selector","selector":"article"}
```

**원인**: 지피터스 페이지 구조가 변경되어 selector가 일치하지 않음

### 해결 단계

#### Step 1: 페이지 구조 재분석
```bash
# 1. Chrome에서 페이지 열기
# https://www.gpters.org/member/WZlPiwwnpW

# 2. F12 → Elements 탭에서 게시물 요소 다시 확인

# 3. 새로운 selector 패턴 찾기
```

#### Step 2: scrape_posts.py 수정
```python
# scrape_posts.py 의 parse_posts() 함수 수정

# 변경 전:
post_elements = soup.select('article')[:max_results]

# 변경 후 (예: 페이지 구조가 div로 변경됨):
post_elements = soup.select('div.post-card')[:max_results]
```

#### Step 3: 작은 규모로 테스트
```bash
# 5개만 수집해서 빠르게 테스트
python scripts/scrape_posts.py \
  --profile-url "https://www.gpters.org/member/WZlPiwwnpW" \
  --max-results 5

# 에러가 없으면 정상
```

#### Step 4: 변경 이력 기록
아래 "변경 이력" 섹션에 날짜와 수정 내용 추가

---

## 변경 이력

### 초기 버전 (2026-01-06)
- **작성자**: Claude Code
- **상태**: 초기 설정 완료, 첫 검증 대기
- **Selector**:
  - 게시물: `article` (fallback: `[data-testid="post"]`)
  - 제목: `h2, h3, .title`
  - URL: `a[href*="/post/"]`
  - 날짜: `time, [class*="date"]`
  - 요약: `.summary, .description, p`

### (변경사항 추가 시 여기 기록)

```
### 수정 사항 (날짜)
- **변경 이유**: [페이지 구조 변경 / API 변경 / 기타]
- **이전 Selector**: article
- **새 Selector**: div.post-container
- **영향 범위**: parse_posts() 함수 line XX
- **테스트 결과**: ✅ 정상 작동
```

---

## Selector 선택 가이드

### 우선순위 (안정성 순)

#### 1순위: data-testid 속성 (가장 안정적)
```html
<div data-testid="post-card-123">
  ...
</div>
```
**이유**: 개발팀이 테스트를 위해 명시적으로 추가하므로 변경이 적음

**Selector**: `[data-testid="post"]`

#### 2순위: 시맨틱 HTML 태그
```html
<article>
  <h2>제목</h2>
  ...
</article>
```
**이유**: HTML 표준에 따른 태그는 유지될 확률이 높음

**Selector**: `article`, `<section>` 등

#### 3순위: 의미 있는 클래스명
```html
<div class="post-item" data-id="123">
  ...
</div>
```
**이유**: 클래스명이 콘텐츠 의미를 나타냄

**Selector**: `.post-item`, `.article-card`

#### 4순위: 태그명만 사용 (가장 불안정)
```html
<div>
  <h2>제목</h2>
</div>
```
**이유**: 많은 요소가 `<div>`를 사용하므로 오류 가능성 높음

**Selector**: `div` (가능하면 피할 것)

### 복합 Selector 작성 팁

**좋은 예**:
```css
article h2.title              /* article 안의 h2.title */
[data-testid="post"] a[href*="/post/"]  /* post 속 post 링크 */
.post-container > .post-title  /* 직접 자식 선택 */
```

**나쁜 예**:
```css
div div div h2         /* 너무 구체적, 깨지기 쉬움 */
h2                     /* 너무 일반적, 다른 h2를 찾을 수 있음 */
```

---

## 문제 해결

### 문제: "No such element" 에러

**증상**:
```
Page load failed: no such element: Unable to locate element
```

**원인 진단**:
1. **페이지 아직 로드 안 됨**: 대기 시간 부족
   - 해결: `scrape_posts.py`의 `time.sleep()` 값 증가

2. **Selector 잘못됨**: 구조 변경
   - 해결: 새 selector 찾기 (위의 "업데이트 방법" 참고)

3. **프로필에 게시물 없음**: 비활성 계정
   - 확인: 브라우저에서 직접 방문해서 게시물 확인

**디버깅 명령**:
```bash
# GUI 모드로 브라우저 상태 확인
python scripts/scrape_posts.py \
  --profile-url "https://www.gpters.org/member/WZlPiwwnpW" \
  --max-results 1

# 브라우저가 열리면 HTML 구조 수동 확인
```

---

### 문제: 일부 게시물만 파싱됨

**증상**:
- 10개 게시물이 있지만 5개만 파싱됨
- JSON 출력: `"collected": 5`

**원인**:
- 일부 게시물이 다른 HTML 구조를 가짐
- 예: 일부는 `<article>`, 일부는 `<div class="post">`

**해결**:
```python
# scrape_posts.py의 parse_posts() 함수 수정

# Before:
post_elements = soup.select('article')

# After (여러 selector 결합):
post_elements = soup.select('article, div.post, [data-testid="post"]')
```

---

### 문제: 날짜 파싱 실패

**증상**:
```json
"published_date": "2025-01-06"  // 모두 현재 날짜
```

**원인**: 날짜 추출 실패, `parse_date()` fallback으로 현재 날짜 반환

**해결**:
1. Console에서 날짜 selector 확인:
   ```javascript
   $$('article')[0].querySelector('time')  // 결과 확인
   ```

2. `scrape_posts.py`의 `parse_posts()` 함수에서 수정:
   ```python
   # Before:
   date_elem = post.select_one('time, [class*="date"]')

   # After (새로운 selector 추가):
   date_elem = post.select_one('time, [class*="date"], span.published-at')
   ```

---

## 자동화 팁

### 모니터링 스크립트

지피터스 구조 변경을 감지하는 Python 스크립트:

```python
#!/usr/bin/env python3
"""지피터스 페이지 구조 변경 감지"""

import requests
from bs4 import BeautifulSoup
import hashlib

def check_page_structure(url):
    """페이지 구조의 해시값 반환"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    # 게시물 컨테이너의 class 목록 추출
    articles = soup.select('article, [data-testid="post"], [class*="post"]')
    structure = ' '.join([str(a.attrs) for a in articles[:3]])

    return hashlib.md5(structure.encode()).hexdigest()

# 기존 해시값 저장
saved_hash = "abc123..."

current_hash = check_page_structure("https://www.gpters.org/member/WZlPiwwnpW")

if current_hash != saved_hash:
    print("⚠️ 페이지 구조가 변경되었습니다!")
    print("selector-guide.md를 업데이트하세요.")
else:
    print("✅ 페이지 구조 정상")
```

---

## FAQ

**Q**: Selector를 자동으로 감지할 수 없나요?

**A**: 현재는 수동 검증이 필요합니다. 향후 AI 기반 selector 감지 기능 추가 예정입니다.

**Q**: 하나의 Selector로 모든 게시물을 찾을 수 없으면?

**A**: 여러 Selector를 `soup.select('selector1, selector2, selector3')`으로 결합하세요.

**Q**: 페이지가 로드되지 않는 경우?

**A**: `scrape_posts.py`의 `time.sleep()` 값을 증가시키거나 `WebDriverWait` timeout을 연장하세요.

---

## 관련 문서

- `SKILL.md` - Skill 사용 설명서
- `scrape_posts.py` - 메인 스크립트 (Selector 수정 위치)
- [Selenium 문서](https://www.selenium.dev/documentation/)
- [BeautifulSoup 문서](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

**마지막 업데이트**: 2026-01-06
**상태**: ⏳ 첫 검증 대기 중
