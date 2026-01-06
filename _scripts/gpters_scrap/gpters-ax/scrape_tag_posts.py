#!/usr/bin/env python3
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
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Error: Missing dependencies. {e}")
    sys.exit(1)

def setup_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def html_to_markdown(element):
    if not element: return ""
    markdown_parts = []
    
    for child in element.children:
        if child.name is None:
            text = str(child).strip()
            if text: markdown_parts.append(text)
        elif child.name == 'img':
            src = child.get('src', '')
            alt = child.get('alt', '')
            if src: markdown_parts.append(f"\n![{alt}]({src})\n")
        elif child.name == 'a':
            href = child.get('href', '')
            text = html_to_markdown(child)
            if href: markdown_parts.append(f"[{text}]({href})")
            else: markdown_parts.append(text)
        elif child.name in ['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li']:
            content = html_to_markdown(child)
            if content:
                if child.name.startswith('h'):
                    level = int(child.name[1])
                    markdown_parts.append(f"\n{'#' * level} {content}\n")
                elif child.name == 'li': markdown_parts.append(f"- {content}")
                else: markdown_parts.append(f"{content}\n")
        elif child.name == 'figure':
            for img in child.find_all('img'):
                src = img.get('src', '')
                alt = img.get('alt', '')
                if src: markdown_parts.append(f"\n![{alt}]({src})\n")
        elif child.name in ['ul', 'ol']:
            content = html_to_markdown(child)
            if content: markdown_parts.append(f"\n{content}\n")
        elif child.name == 'pre':
             markdown_parts.append(f"\n```\n{child.get_text()}\n```\n")
        elif child.name == 'code':
             markdown_parts.append(f"`{child.get_text()}`")
        else:
            markdown_parts.append(html_to_markdown(child))
    return "\n".join(markdown_parts).replace("\n\n\n", "\n\n")

def get_post_content(driver, url):
    """상세 페이지에서 본문 수집"""
    try:
        driver.get(url)
        time.sleep(3) # 로딩 대기
        soup = BeautifulSoup(driver.page_source, 'lxml')
        article = soup.select_one('article.prose, .post-content, .content')
        if article:
            return html_to_markdown(article)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return ""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--max', type=int, default=10)
    parser.add_argument('--out', default='docs/notes/gpters_aicase_ax')
    args = parser.parse_args()

    driver = setup_driver()
    try:
        print(f"Loading tag page: {args.url}")
        driver.get(args.url)
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # 태그 페이지에서 링크 추출 (패턴: /post/ 가 포함된 링크)
        post_links = soup.select('a[href*="/post/"]')
        
        posts = []
        seen_urls = set()
        for link in post_links:
            url = link.get('href', '')
            title = link.get_text(strip=True)
            if url and title and len(title) > 5:
                if not url.startswith('http'):
                    url = f"https://www.gpters.org{url}"
                if url not in seen_urls:
                    posts.append({'title': title, 'url': url})
                    seen_urls.add(url)
            if len(posts) >= args.max: break

        print(f"Found {len(posts)} posts. Starting detailed scrap...")
        
        output_path = Path(args.out)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for post in posts:
            print(f"Scraping: {post['title']}")
            content = get_post_content(driver, post['url'])
            if content:
                date_str = datetime.now().strftime('%Y%m%d')
                safe_title = re.sub(r'[<>:"/\\|?*]', '', post['title']).replace(' ', '_')[:50]
                filename = f"{date_str}_{safe_title}.md"
                
                md = f"# {post['title']}\n\n- **URL**: {post['url']}\n\n{content}"
                (output_path / filename).write_text(md, encoding='utf-8')
                print(f"Saved: {filename}")
                
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
