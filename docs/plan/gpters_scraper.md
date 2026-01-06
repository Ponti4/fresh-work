
# Implementation Plan: gpters-scraper Skill

## Overview
Create a Claude Code Skill that scrapes editor_소연's posts from gpters.org and saves them as Markdown files.

**Target URL**: https://www.gpters.org/member/WZlPiwwnpW
**Environment**: Windows 11, Python 3.13.7, Chrome browser
**Dependencies**: selenium, webdriver-manager, beautifulsoup4, lxml (all installed ✅)

---

## Requirements Summary

### User Selections
- **Scraping Method**: Selenium (browser automation)
- **Collection Range**: Recent 10-20 posts
- **Execution**: Manual only (no scheduling)

### Output Specification
- **Format**: Markdown files
- **Path**: `docs/notes/gpters_editor_soyeon/YYYYMMDD_title.md`
- **Data**: Title, URL, published date, summary

### Website Analysis
- **Rendering**: JavaScript SPA (GraphQL API: api.bettermode.com)
- **Approach**: Selenium required (BeautifulSoup alone insufficient)

---

## Implementation Plan

### Phase 1: Core Scraping (MVP)

#### 1.1 Create Skill Structure
```
.claude/skills/gpters-scraper/
├── SKILL.md
├── scripts/
│   └── scrape_posts.py
└── references/
    └── selector-guide.md
```

#### 1.2 SKILL.md
**File**: `C:\test\duwls-workspace\gpters-20th-templates\.claude\skills\gpters-scraper\SKILL.md`

**Frontmatter**:
```yaml
---
name: gpters-scraper
description: 지피터스(gpters.org) 멤버 프로필에서 게시물을 스크래핑하여 Markdown으로 저장. "지피터스 게시물 수집", "gpters 스크랩", "editor_소연 게시물", "프로필 크롤링" 등을 언급하면 자동 실행. Selenium 기반 동적 페이지 수집.
---
```

**Content** (~150 lines):
- Prerequisites: pip install commands
- Usage: CLI examples with options
- Output format: Markdown template example
- Options table: --profile-url, --max-results, --output-dir, --headless

**Reference Pattern**: `.claude\skills\youtube-collector\SKILL.md` (lines 1-159)

---

#### 1.3 scrape_posts.py
**File**: `C:\test\duwls-workspace\gpters-20th-templates\.claude\skills\gpters-scraper\scripts\scrape_posts.py`

**Core Functions** (~400 lines):

```python
#!/usr/bin/env python3
"""지피터스 게시물 스크래핑"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# === 1. Selenium Setup ===
def setup_driver(headless=False):
    """ChromeDriver initialization with options"""
    options = Options()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    return driver

# === 2. Page Loading ===
def load_profile_page(driver, profile_url):
    """Load profile page and wait for dynamic content"""
    try:
        driver.get(profile_url)
        time.sleep(5)  # Initial load

        wait = WebDriverWait(driver, 15)
        # Adjust selector after manual inspection
        posts_container = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "article, [data-testid='post'], .post-item")
            )
        )
        time.sleep(3)  # JS rendering
        return True
    except Exception as e:
        print(f"Page load failed: {str(e)}")
        return False

# === 3. Parsing ===
def parse_posts(driver, max_results=10):
    """Extract post data from page"""
    posts = []
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Selectors TBD after manual page inspection
    post_elements = soup.select('article')[:max_results]

    for idx, post in enumerate(post_elements, 1):
        try:
            title = post.select_one('h2, .title').get_text(strip=True)
            link = post.select_one('a[href*="/post/"]')
            url = link.get('href', '') if link else ''
            if url and not url.startswith('http'):
                url = f"https://www.gpters.org{url}"

            date_elem = post.select_one('time, .date')
            date_str = date_elem.get('datetime') or date_elem.get_text(strip=True) if date_elem else ''
            published_date = parse_date(date_str)

            summary = post.select_one('.summary, p').get_text(strip=True)[:200] if post.select_one('.summary, p') else ''

            posts.append({
                'title': title,
                'url': url,
                'published_date': published_date,
                'summary': summary
            })
        except Exception as e:
            print(f"Post {idx} parse error: {str(e)}")
            continue

    return posts

def parse_date(date_str):
    """Convert various date formats to YYYY-MM-DD"""
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d')
    try:
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d')
        return datetime.now().strftime('%Y-%m-%d')
    except:
        return datetime.now().strftime('%Y-%m-%d')

# === 4. File Saving ===
def sanitize_filename(title, max_length=50):
    """Windows-compatible filename normalization"""
    import re
    safe = re.sub(r'[<>:"/\\|?*]', '', title)
    safe = safe.replace(' ', '_')
    safe = re.sub(r'_+', '_', safe).strip('_')
    return safe[:max_length] if safe else 'untitled'

def generate_filename(post_data):
    """Create YYYYMMDD_title.md filename"""
    date = post_data.get('published_date', '').replace('-', '') or datetime.now().strftime('%Y%m%d')
    title = sanitize_filename(post_data.get('title', 'untitled'))
    return f"{date}_{title}.md"

def generate_markdown(post_data):
    """Create Markdown content"""
    title = post_data.get('title', 'No Title')
    url = post_data.get('url', '')
    date = post_data.get('published_date', '')
    summary = post_data.get('summary', 'No summary')

    return f"""# {title}

- **작성일**: {date}
- **URL**: [{url}]({url})

## 요약
{summary}

---

**수집 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

def save_posts_to_markdown(posts, output_dir, skip_existing=True):
    """Save posts as Markdown files"""
    result = {'saved': 0, 'skipped': 0, 'saved_files': [], 'errors': []}

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for post in posts:
        try:
            filename = generate_filename(post)
            file_path = output_path / filename

            if skip_existing and file_path.exists():
                result['skipped'] += 1
                continue

            markdown = generate_markdown(post)
            file_path.write_text(markdown, encoding='utf-8')

            result['saved'] += 1
            result['saved_files'].append(filename)
        except Exception as e:
            result['errors'].append({'title': post.get('title'), 'error': str(e)})

    return result

# === 5. Main Integration ===
def scrape_posts(profile_url, max_results=10, headless=False):
    """Main scraping function"""
    driver = setup_driver(headless)
    posts = []

    try:
        if not load_profile_page(driver, profile_url):
            return posts
        posts = parse_posts(driver, max_results)
        print(f"Collected {len(posts)} posts")
    except Exception as e:
        print(f"Scraping error: {str(e)}")
    finally:
        driver.quit()

    return posts

def main():
    """CLI entry point with JSON output"""
    parser = argparse.ArgumentParser(description='gpters 게시물 스크래핑')
    parser.add_argument('--profile-url', required=True, help='프로필 URL')
    parser.add_argument('--max-results', type=int, default=10, help='최대 수집 개수')
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
        print(f"Scraping: {args.profile_url}")
        posts = scrape_posts(args.profile_url, args.max_results, args.headless)
        result['collected'] = len(posts)

        if posts:
            print(f"Saving to: {args.output_dir}")
            save_result = save_posts_to_markdown(posts, args.output_dir, not args.no_skip)
            result.update(save_result)
            result['status'] = 'success'
        else:
            result['status'] = 'no_posts'

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        result['status'] = 'error'
        result['errors'].append({'type': 'critical', 'message': str(e)})
        print(json.dumps(result, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Reference Patterns**:
- `.claude\skills\youtube-collector\scripts\collect_videos.py` (lines 95-128: file saving, lines 186-304: main function, JSON output)

---

#### 1.4 selector-guide.md
**File**: `C:\test\duwls-workspace\gpters-20th-templates\.claude\skills\gpters-scraper\references\selector-guide.md`

**Content**:
```markdown
# CSS Selector Maintenance Guide

## Initial Setup (2026-01-06)

**IMPORTANT**: Selectors must be verified manually before first run.

### Verification Steps:
1. Open https://www.gpters.org/member/WZlPiwwnpW in Chrome
2. Press F12 → Elements tab
3. Locate post elements in DOM
4. Test selectors in Console:
   ```javascript
   $$('article')  // Test if this finds posts
   $$('[data-testid="post"]')  // Alternative
   ```

### Current Selectors (TBD):
- **Post container**: `article` or `[data-testid="post"]`
- **Title**: `h2.title` or `.post-title`
- **Link**: `a[href*="/post/"]`
- **Date**: `time` or `.published-date`
- **Summary**: `.summary` or `p.excerpt`

### Fallback Strategy:
If page structure changes, update `scrape_posts.py` line ~XX with new selectors.

### Change Log:
- 2026-01-06: Initial selectors (pending verification)
```

---

### Phase 2: Execution Steps

#### Step 1: Manual Page Inspection (Critical)
**Before running the script**, inspect the actual page structure:

```bash
# Open Chrome manually
# Navigate to: https://www.gpters.org/member/WZlPiwwnpW
# F12 → Elements → Find post elements
# Console: $$('article') to test selectors
```

**Update `scrape_posts.py` line ~XX** with verified selectors.

#### Step 2: First Test Run
```bash
cd .claude/skills/gpters-scraper
python scripts/scrape_posts.py --profile-url "https://www.gpters.org/member/WZlPiwwnpW" --max-results 5
```

**Expected Output**:
- Browser opens (GUI mode)
- Page loads for 5-10 seconds
- Console shows: "Collected 5 posts"
- JSON output with file list
- 5 Markdown files in `docs/notes/gpters_editor_soyeon/`

#### Step 3: Verify Output
Check created Markdown files:
```
docs/notes/gpters_editor_soyeon/
├── 20260106_first_post.md
├── 20260105_second_post.md
└── ...
```

Each file should contain:
- Title
- URL
- Published date
- Summary

#### Step 4: Test Headless Mode
```bash
python scripts/scrape_posts.py --profile-url "URL" --max-results 10 --headless
```

---

### Phase 3: Claude Code Integration

#### Step 1: Reload Skills
In Claude Code conversation:
```
/reload-skills
```

#### Step 2: Test Trigger
User message:
```
지피터스 editor_소연님 게시물 10개 수집해줘
```

Claude should:
1. Detect trigger keywords ("지피터스", "게시물 수집")
2. Execute `gpters-scraper` skill
3. Run scrape_posts.py
4. Parse JSON output
5. Report results to user

---

## Critical Files

### Files to Create:
1. **C:\test\duwls-workspace\gpters-20th-templates\.claude\skills\gpters-scraper\SKILL.md**
   - Skill definition with frontmatter
   - Usage guide and options

2. **C:\test\duwls-workspace\gpters-20th-templates\.claude\skills\gpters-scraper\scripts\scrape_posts.py**
   - Main scraping logic (~400 lines)
   - Selenium + BeautifulSoup + file saving

3. **C:\test\duwls-workspace\gpters-20th-templates\.claude\skills\gpters-scraper\references\selector-guide.md**
   - CSS Selector documentation
   - Manual verification checklist

### Reference Files (Read-only):
- `.claude\skills\youtube-collector\SKILL.md` - Frontmatter pattern
- `.claude\skills\youtube-collector\scripts\collect_videos.py` - JSON output, file saving

---

## Error Handling

### Common Issues:

**1. Selector Not Found**
```json
{
  "status": "error",
  "errors": [{"type": "critical", "message": "no such element: article"}]
}
```
**Solution**: Update selectors in `scrape_posts.py` after manual page inspection.

**2. ChromeDriver Error**
```json
{
  "error": "ChromeDriver installation failed"
}
```
**Solution**: Verify Chrome browser is installed. webdriver-manager should auto-install driver.

**3. Page Timeout**
```
Page load failed: Timeout waiting for element
```
**Solution**: Increase `time.sleep()` values or `WebDriverWait` timeout.

**4. UTF-8 Encoding (Windows)**
- Always use `encoding='utf-8'` in file operations
- Already handled in `file_path.write_text(markdown, encoding='utf-8')`

---

## Success Criteria

### Phase 1 MVP:
- [ ] Skill directory created
- [ ] SKILL.md with valid frontmatter
- [ ] scrape_posts.py executable
- [ ] Manual test creates at least 1 Markdown file
- [ ] Korean text saves correctly (UTF-8)

### Phase 2 Integration:
- [ ] `/reload-skills` recognizes gpters-scraper
- [ ] Trigger keywords work
- [ ] JSON output parsed correctly
- [ ] User receives readable summary

---

## Next Steps After Implementation

### Optional Enhancements (Phase 3):
1. **Full Post Content**: Visit detail pages for complete text
2. **Image Download**: Save images locally
3. **Duplicate Detection**: Skip already-collected posts
4. **GraphQL API**: Direct API calls instead of Selenium (faster)

### Maintenance:
- Update `selector-guide.md` when gpters.org changes
- Monitor for Cloudflare/bot detection
- Test monthly to catch structure changes

---

## Estimated Timeline

- **Phase 1 (MVP)**: 2-3 hours
  - 30min: Create structure + SKILL.md
  - 1.5hr: Write scrape_posts.py
  - 30min: Manual page inspection + selector verification
  - 30min: Testing + debugging

- **Phase 2 (Integration)**: 30 minutes
  - Test in Claude Code
  - Verify JSON parsing

**Total**: ~3-4 hours for complete MVP

---

## Notes

- **Windows Paths**: pathlib.Path handles forward slashes automatically
- **Korean Text**: UTF-8 encoding specified in all file operations
- **Selenium Stability**: 5-15 second delays account for network latency
- **Headless Mode**: Use GUI for initial development, headless for production

---

**Status**: Ready for implementation ✅
