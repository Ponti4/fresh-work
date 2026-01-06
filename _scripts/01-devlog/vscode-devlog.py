#!/usr/bin/env python3
"""
VS Code Extensions DEVLOG 생성기
VS Code 확장 로그 파싱하여 DEVLOG.md 생성

지원 예정:
- GitHub Copilot
- Codeium
- Tabnine

Usage:
    python vscode-devlog.py
    python vscode-devlog.py --output DEVLOG.md
    python vscode-devlog.py --dry-run
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description='VS Code Extensions DEVLOG 생성')
    parser.add_argument('--output', default='DEVLOG.md', help='출력 파일 경로')
    parser.add_argument('--dry-run', action='store_true', help='미리보기 모드')
    args = parser.parse_args()

    print("[INFO] VS Code Extensions DEVLOG 생성 (아직 구현되지 않음)")
    print("[INFO] 지원 예정: GitHub Copilot, Codeium, Tabnine")
    print()
    print("향후 구현 예정입니다.")
    print()
    print("지금은 다음을 사용하세요:")
    print("  - claude-code-devlog.py (Claude Code CLI)")
    print("  - antigravity-devlog.py (AntiGravity/Gemini)")


if __name__ == '__main__':
    main()
