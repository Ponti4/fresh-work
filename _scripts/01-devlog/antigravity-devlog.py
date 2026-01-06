#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AntiGravity (Gemini) DEVLOG 생성기
~/.gemini/antigravity/brain의 conversation_log.md 파싱하여 DEVLOG.md 생성

Usage:
    python antigravity-devlog.py
    python antigravity-devlog.py --output DEVLOG.md
    python antigravity-devlog.py --dry-run
"""

import json
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# UTF-8 인코딩 설정 (Windows 지원)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def load_sessions():
    """AntiGravity 세션 파일 로드"""
    home = Path.home()
    brain_dir = home / ".gemini" / "antigravity" / "brain"

    if not brain_dir.exists():
        print(f"[WARNING] Brain 디렉토리를 찾을 수 없습니다: {brain_dir}")
        return []

    sessions = []
    for session_folder in brain_dir.iterdir():
        if not session_folder.is_dir():
            continue

        conv_log = session_folder / 'conversation_log.md'
        if not conv_log.exists():
            continue

        # 타임스탐프 추출 (메타데이터에서)
        timestamp = None
        metadata_file = session_folder / 'conversation_log.md.metadata.json'
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    ts_str = metadata.get('updatedAt', '')
                    if ts_str:
                        timestamp = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
            except:
                pass

        sessions.append({
            'path': conv_log,
            'session_id': session_folder.name,
            'timestamp': timestamp
        })

    return sessions


def parse_conversation_log(file_path, session_id, base_timestamp=None):
    """마크다운 형식의 대화 파일 파싱"""
    messages = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # "## 대화 내용" 섹션만 추출
        if '## 대화 내용' in content:
            content = content.split('## 대화 내용', 1)[1]

        # 마크다운 블록 인용 파싱 (> **User**: / > **Antigravity**:)
        lines = content.split('\n')
        current_role = None
        current_content = []
        msg_index = 0

        for line in lines:
            line_stripped = line.strip()

            # User 메시지 시작
            if '> **User**:' in line:
                if current_content and current_role:
                    msg_text = '\n'.join(current_content).strip()
                    if len(msg_text) >= 50:
                        messages.append({
                            'role': 'user' if current_role == 'User' else 'assistant',
                            'content': msg_text,
                            'tool': 'AntiGravity'
                        })
                    current_content = []
                    msg_index += 1

                current_role = 'User'
                msg_text = line_stripped.replace('> **User**:', '').strip()
                if msg_text:
                    current_content.append(msg_text)

            # AntiGravity 응답 시작
            elif '> **Antigravity**:' in line:
                if current_content and current_role:
                    msg_text = '\n'.join(current_content).strip()
                    if len(msg_text) >= 50:
                        messages.append({
                            'role': 'user' if current_role == 'User' else 'assistant',
                            'content': msg_text,
                            'tool': 'AntiGravity'
                        })
                    current_content = []
                    msg_index += 1

                current_role = 'Antigravity'
                msg_text = line_stripped.replace('> **Antigravity**:', '').strip()
                if msg_text:
                    current_content.append(msg_text)

            # 계속되는 블록 인용 내용
            elif line.startswith('>') and current_role:
                msg_text = line_stripped.lstrip('> ').strip()
                if msg_text:
                    current_content.append(msg_text)

            # 섹션 분리선
            elif line.startswith('##') or line.startswith('---'):
                if current_content and current_role:
                    msg_text = '\n'.join(current_content).strip()
                    if len(msg_text) >= 50:
                        messages.append({
                            'role': 'user' if current_role == 'User' else 'assistant',
                            'content': msg_text,
                            'tool': 'AntiGravity'
                        })
                    current_content = []
                    msg_index += 1
                current_role = None

        # 마지막 메시지
        if current_content and current_role:
            msg_text = '\n'.join(current_content).strip()
            if len(msg_text) >= 50:
                messages.append({
                    'role': 'user' if current_role == 'User' else 'assistant',
                    'content': msg_text,
                    'tool': 'AntiGravity'
                })

        # 타임스탐프 할당
        if base_timestamp:
            for i, msg in enumerate(messages):
                msg['timestamp'] = base_timestamp

        return messages

    except Exception as e:
        print(f"[ERROR] 파일 파싱 실패: {file_path}: {e}")
        return []


def group_by_date(messages):
    """날짜별로 그룹핑"""
    grouped = defaultdict(list)
    for msg in sorted(messages, key=lambda m: m.get('timestamp', datetime.now())):
        timestamp = msg.get('timestamp', datetime.now())
        date_key = timestamp.strftime('%Y-%m-%d')
        grouped[date_key].append(msg)
    return dict(sorted(grouped.items()))


def generate_devlog(grouped_messages):
    """DEVLOG.md 생성"""
    lines = []

    # 헤더
    project_name = Path.cwd().name
    lines.append(f"# {project_name} - 개발 로그 (AntiGravity)\n\n")
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

                lines.append("**AntiGravity 응답:**\n")
                if assistant_msgs:
                    first = assistant_msgs[0]['content'][:200]
                    lines.append(f"- {first}...\n\n" if len(assistant_msgs[0]['content']) > 200 else f"- {first}\n\n")

                lines.append("---\n\n")
                task_num += 1
            else:
                i += 1

    return ''.join(lines)


def main():
    parser = argparse.ArgumentParser(description='AntiGravity (Gemini) DEVLOG 생성')
    parser.add_argument('--output', default='DEVLOG.md', help='출력 파일 경로')
    parser.add_argument('--dry-run', action='store_true', help='미리보기 모드')
    args = parser.parse_args()

    print("[INFO] AntiGravity 세션 로드 중...")
    sessions = load_sessions()

    if not sessions:
        print("[WARNING] 세션을 찾을 수 없습니다.")
        return

    print(f"[INFO] {len(sessions)}개 세션 발견")

    all_messages = []
    for session in sessions:
        messages = parse_conversation_log(
            session['path'],
            session['session_id'],
            session['timestamp']
        )
        all_messages.extend(messages)

    if not all_messages:
        print("[WARNING] 처리할 메시지가 없습니다.")
        return

    print(f"[INFO] {len(all_messages)}개 유효한 메시지 발견")

    grouped = group_by_date(all_messages)
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
