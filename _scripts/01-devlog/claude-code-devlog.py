#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code CLI DEVLOG 생성기
~/.claude/projects/{project-key}의 세션 파일(.jsonl)을 파싱하여 DEVLOG.md 생성

Usage:
    python claude-code-devlog.py
    python claude-code-devlog.py --output DEVLOG.md
    python claude-code-devlog.py --dry-run
"""

import json
import sys
import argparse
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# UTF-8 인코딩 설정 (Windows 지원)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def get_project_key():
    """현재 프로젝트 경로를 Claude Code 프로젝트 키로 변환"""
    cwd = Path.cwd()
    # Windows: C:\Users\name\project → C-Users-name-project
    # Unix: /Users/name/project → -Users-name-project
    project_key = str(cwd).replace('\\', '-').replace(':', '').replace(' ', '-')
    return project_key


def load_sessions():
    """Claude Code CLI 세션 파일 로드"""
    home = Path.home()
    session_dir = home / ".claude" / "projects" / get_project_key()

    if not session_dir.exists():
        print(f"[WARNING] 세션 디렉토리를 찾을 수 없습니다: {session_dir}")
        return []

    messages = []
    for jsonl_file in sorted(session_dir.glob('*.jsonl')):
        # agent- 파일 제외
        if jsonl_file.name.startswith('agent-'):
            continue

        try:
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        if data.get('type') in ['user', 'assistant']:
                            messages.append(data)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"[ERROR] 파일 파싱 실패: {jsonl_file}: {e}")

    return messages


def extract_content(message_obj):
    """메시지 객체에서 텍스트 추출"""
    if isinstance(message_obj, str):
        return message_obj

    if isinstance(message_obj, dict):
        content = message_obj.get('content')
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            texts = []
            for item in content:
                if isinstance(item, dict) and item.get('type') == 'text':
                    texts.append(item.get('text', ''))
                elif isinstance(item, str):
                    texts.append(item)
            return '\n'.join(texts).strip()

    return ""


def parse_messages(raw_messages):
    """메시지 정제 및 그룹핑"""
    parsed = []

    for msg in raw_messages:
        msg_type = msg.get('type')
        timestamp_str = msg.get('timestamp', '')
        message_obj = msg.get('message', {})

        # 타임스탐프 파싱
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            timestamp = datetime.now()

        # 콘텐츠 추출
        content = extract_content(message_obj)
        if not content or len(content) < 50:
            continue

        # IDE 메타데이터 제외
        if content.startswith('<ide_'):
            continue

        parsed.append({
            'role': msg_type,
            'content': content,
            'timestamp': timestamp,
            'tool': 'Claude Code CLI'
        })

    return parsed


def group_by_date(messages):
    """날짜별로 그룹핑"""
    grouped = defaultdict(list)
    for msg in sorted(messages, key=lambda m: m['timestamp']):
        date_key = msg['timestamp'].strftime('%Y-%m-%d')
        grouped[date_key].append(msg)
    return dict(sorted(grouped.items()))


def generate_devlog(grouped_messages):
    """DEVLOG.md 생성"""
    lines = []

    # 헤더
    project_name = Path.cwd().name
    lines.append(f"# {project_name} - 개발 로그 (Claude Code CLI)\n\n")
    lines.append(f"생성일: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    lines.append("---\n\n")

    # 날짜별 섹션
    day_num = 1
    for date_str in grouped_messages:
        lines.append(f"## {date_str} (Day {day_num})\n\n")
        day_num += 1

        daily_msgs = grouped_messages[date_str]
        task_num = 1

        # User/Assistant 쌍 생성
        i = 0
        while i < len(daily_msgs):
            if daily_msgs[i]['role'] == 'user':
                user_msg = daily_msgs[i]
                assistant_msgs = []

                # 다음 Assistant 메시지들 수집
                i += 1
                while i < len(daily_msgs) and daily_msgs[i]['role'] == 'assistant':
                    assistant_msgs.append(daily_msgs[i])
                    i += 1

                # 작업 섹션 생성
                title = user_msg['content'][:50].replace('\n', ' ')
                lines.append(f"### {task_num}. {title}\n\n")
                lines.append("```\n")
                lines.append(user_msg['content'][:300])
                lines.append("\n```\n\n")

                lines.append("**Claude 응답:**\n")
                if assistant_msgs:
                    first = assistant_msgs[0]['content'][:200]
                    lines.append(f"- {first}...\n\n" if len(assistant_msgs[0]['content']) > 200 else f"- {first}\n\n")

                lines.append("---\n\n")
                task_num += 1
            else:
                i += 1

    return ''.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Claude Code CLI DEVLOG 생성')
    parser.add_argument('--output', default='DEVLOG.md', help='출력 파일 경로')
    parser.add_argument('--dry-run', action='store_true', help='미리보기 모드')
    args = parser.parse_args()

    print("[INFO] Claude Code CLI 세션 로드 중...")
    raw_messages = load_sessions()

    if not raw_messages:
        print("[WARNING] 메시지를 찾을 수 없습니다.")
        return

    print(f"[INFO] {len(raw_messages)}개 메시지 파싱 중...")
    parsed = parse_messages(raw_messages)

    if not parsed:
        print("[WARNING] 처리할 메시지가 없습니다.")
        return

    print(f"[INFO] {len(parsed)}개 유효한 메시지 발견")

    grouped = group_by_date(parsed)
    print(f"[INFO] {len(grouped)}일의 데이터 발견")

    devlog = generate_devlog(grouped)

    if args.dry_run:
        print("\n[DRY RUN] 미리보기:\n")
        print(devlog[:1000])
        print("\n... (이하 생략)\n")
    else:
        Path(args.output).write_text(devlog, encoding='utf-8')
        print(f"[SUCCESS] {args.output} 생성 완료")


if __name__ == '__main__':
    main()
