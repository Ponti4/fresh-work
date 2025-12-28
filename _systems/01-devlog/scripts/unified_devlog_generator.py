#!/usr/bin/env python3
"""
통합 개발 로그 생성 시스템
Claude Code CLI, VS Code Extensions, Aide 등 다중 도구의 세션을 추적하여 DEVLOG.md 생성

Usage:
    python unified_devlog_generator.py --config ../config/devlog.config.yaml
    python unified_devlog_generator.py --config ../config/devlog.config.yaml --dry-run
    python unified_devlog_generator.py --config ../config/devlog.config.yaml --from 2025-12-25 --to 2025-12-28
"""

import json
import os
import sys
import argparse
import logging
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict
import subprocess

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


class DevlogConfig:
    """설정 파일 관리"""

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """설정값 조회"""
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

    def __repr__(self) -> str:
        return f"DevlogConfig({self.config_path})"


class SessionMessage:
    """단일 메시지 표현"""

    def __init__(self, role: str, content: str, timestamp: datetime, tool: str, session_id: str = ""):
        self.role = role  # "user" 또는 "assistant"
        self.content = content.strip() if content else ""
        self.timestamp = timestamp
        self.tool = tool  # "Claude Code CLI", "VS Code", "Aide" 등
        self.session_id = session_id

    def is_valid(self, min_length: int = 50) -> bool:
        """메시지 유효성 검사"""
        return len(self.content) >= min_length

    def __repr__(self) -> str:
        return f"SessionMessage({self.tool}, {self.role}, {self.timestamp})"


class SessionParser:
    """세션 파일 파싱"""

    def __init__(self, config: DevlogConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger

    def parse_claude_code_sessions(self, session_dir: str) -> List[SessionMessage]:
        """Claude Code CLI 세션 파싱 (.jsonl 형식)"""
        messages = []
        session_path = Path(session_dir).expanduser()

        if not session_path.exists():
            self.logger.warning(f"Claude Code session dir not found: {session_path}")
            return messages

        try:
            # 프로젝트 세션 찾기 (프로젝트 경로를 키로 변환)
            cwd = Path.cwd()
            project_key = str(cwd).replace('\\', '-').replace(':', '').replace(' ', '-')
            project_session_dir = session_path / project_key

            if not project_session_dir.exists():
                self.logger.warning(f"Project session dir not found: {project_session_dir}")
                return messages

            # .jsonl 파일 수집
            exclude_patterns = self.config.get('tools.claude_code_cli.exclude_patterns', [])
            for jsonl_file in sorted(project_session_dir.glob('*.jsonl')):
                # 제외 패턴 확인
                if any(jsonl_file.name.startswith(p.rstrip('*')) for p in exclude_patterns):
                    continue

                messages.extend(self._parse_jsonl_file(jsonl_file))

        except Exception as e:
            self.logger.error(f"Error parsing Claude Code sessions: {e}")

        return messages

    def _parse_jsonl_file(self, file_path: Path) -> List[SessionMessage]:
        """JSONL 파일 파싱"""
        messages = []
        min_size = self.config.get('tools.claude_code_cli.filters.min_message_size', 50)
        exclude_metadata = self.config.get('tools.claude_code_cli.filters.exclude_ide_metadata', True)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue

                    try:
                        data = json.loads(line)
                        msg = self._extract_claude_message(data, exclude_metadata, min_size)
                        if msg:
                            messages.append(msg)
                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            self.logger.error(f"Error parsing JSONL file {file_path}: {e}")

        return messages

    def _extract_claude_message(self, data: dict, exclude_metadata: bool = True, min_size: int = 50) -> Optional[SessionMessage]:
        """JSON 데이터에서 메시지 추출"""
        msg_type = data.get('type')
        if msg_type not in ['user', 'assistant']:
            return None

        # 타임스탐프 추출
        timestamp_str = data.get('timestamp', '')
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            timestamp = datetime.now()

        # 컨텐츠 추출 - message 필드 확인
        message_obj = data.get('message', {})
        content = None

        # message가 dict인 경우 (신규 형식)
        if isinstance(message_obj, dict):
            content = self._extract_content(message_obj)
        # message가 string인 경우 (구형식)
        elif isinstance(message_obj, str):
            content = message_obj

        if not content:
            return None

        # IDE 메타데이터 필터링
        if exclude_metadata and content.startswith('<ide_'):
            return None

        # 크기 검사
        if len(content) < min_size:
            return None

        return SessionMessage(
            role=msg_type,
            content=content,
            timestamp=timestamp,
            tool="Claude Code CLI",
            session_id=data.get('session_id', '')
        )

    def _extract_content(self, message: Any) -> str:
        """메시지 객체에서 텍스트 콘텐츠 추출"""
        if isinstance(message, str):
            return message

        if isinstance(message, dict):
            # 'content' 필드 추출
            if 'content' in message:
                content = message['content']

                # content가 string인 경우
                if isinstance(content, str):
                    return content

                # content가 list인 경우 (블록 형식)
                if isinstance(content, list):
                    texts = []
                    for item in content:
                        if isinstance(item, dict):
                            if item.get('type') == 'text':
                                texts.append(item.get('text', ''))
                            elif item.get('type') == 'thinking':
                                # thinking 블록은 제외
                                continue
                        elif isinstance(item, str):
                            texts.append(item)
                    return '\n'.join(texts).strip()

        return ""

    def parse_vs_code_sessions(self, session_dirs: List[str]) -> List[SessionMessage]:
        """VS Code 세션 파싱 (향후 확장)"""
        messages = []
        # TODO: VS Code 확장 로그 파싱 구현
        self.logger.info("VS Code session parsing not yet implemented")
        return messages

    def parse_antigravity_sessions(self, brain_dir: str) -> List[SessionMessage]:
        """AntiGravity (Gemini) 세션 파싱 (마크다운 형식)"""
        messages = []
        brain_path = Path(brain_dir).expanduser()

        if not brain_path.exists():
            self.logger.warning(f"AntiGravity brain dir not found: {brain_path}")
            return messages

        try:
            # 모든 세션 폴더 탐색
            for session_folder in brain_path.iterdir():
                if not session_folder.is_dir():
                    continue

                # conversation_log.md 파일 찾기
                conv_log = session_folder / 'conversation_log.md'
                metadata_file = session_folder / 'conversation_log.md.metadata.json'

                if not conv_log.exists():
                    continue

                # 메타데이터에서 타임스탐프 추출
                timestamp = None
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                            timestamp_str = metadata.get('updatedAt', '')
                            if timestamp_str:
                                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    except (json.JSONDecodeError, ValueError):
                        pass

                # 마크다운 파일 파싱
                parsed_msgs = self._parse_antigravity_markdown(conv_log, session_folder.name, timestamp)
                messages.extend(parsed_msgs)

        except Exception as e:
            self.logger.error(f"Error parsing AntiGravity sessions: {e}")

        return messages

    def _parse_antigravity_markdown(self, file_path: Path, session_id: str, base_timestamp: Optional[datetime] = None) -> List[SessionMessage]:
        """AntiGravity 마크다운 파일 파싱"""
        messages = []
        min_size = self.config.get('tools.antigravity.filters.min_message_size', 50)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 대화 내용 섹션 추출
            if '## 대화 내용' in content:
                conv_section = content.split('## 대화 내용', 1)[1]
            else:
                conv_section = content

            # 마크다운 블록 인용 파싱 (> **User**: ... 형식)
            lines = conv_section.split('\n')
            current_role = None
            current_content = []
            message_index = 0

            for line in lines:
                line_stripped = line.strip()

                # User 메시지 시작
                if '> **User**:' in line:
                    # 이전 메시지 저장
                    if current_content and current_role:
                        msg_text = '\n'.join(current_content).strip()
                        if len(msg_text) >= min_size:
                            timestamp = self._calculate_message_timestamp(base_timestamp, message_index)
                            messages.append(SessionMessage(
                                role='user' if current_role == 'User' else 'assistant',
                                content=msg_text,
                                timestamp=timestamp,
                                tool="AntiGravity",
                                session_id=session_id
                            ))
                            message_index += 1
                        current_content = []

                    current_role = 'User'
                    # User 메시지의 내용 추출
                    msg_text = line_stripped.replace('> **User**:', '').strip()
                    if msg_text:
                        current_content.append(msg_text)

                # AntiGravity 응답 시작
                elif '> **Antigravity**:' in line:
                    # 이전 메시지 저장
                    if current_content and current_role:
                        msg_text = '\n'.join(current_content).strip()
                        if len(msg_text) >= min_size:
                            timestamp = self._calculate_message_timestamp(base_timestamp, message_index)
                            messages.append(SessionMessage(
                                role='user' if current_role == 'User' else 'assistant',
                                content=msg_text,
                                timestamp=timestamp,
                                tool="AntiGravity",
                                session_id=session_id
                            ))
                            message_index += 1
                        current_content = []

                    current_role = 'Antigravity'
                    # Antigravity 메시지의 내용 추출
                    msg_text = line_stripped.replace('> **Antigravity**:', '').strip()
                    if msg_text:
                        current_content.append(msg_text)

                # 계속되는 블록 인용 내용
                elif line.startswith('>') and current_role:
                    msg_text = line_stripped.lstrip('> ').strip()
                    if msg_text:
                        current_content.append(msg_text)

                # 섹션 구분선 또는 새로운 섹션
                elif line.startswith('##') or line.startswith('---'):
                    # 마지막 메시지 저장
                    if current_content and current_role:
                        msg_text = '\n'.join(current_content).strip()
                        if len(msg_text) >= min_size:
                            timestamp = self._calculate_message_timestamp(base_timestamp, message_index)
                            messages.append(SessionMessage(
                                role='user' if current_role == 'User' else 'assistant',
                                content=msg_text,
                                timestamp=timestamp,
                                tool="AntiGravity",
                                session_id=session_id
                            ))
                            message_index += 1
                        current_content = []
                        current_role = None

            # 마지막 메시지 저장
            if current_content and current_role:
                msg_text = '\n'.join(current_content).strip()
                if len(msg_text) >= min_size:
                    timestamp = self._calculate_message_timestamp(base_timestamp, message_index)
                    messages.append(SessionMessage(
                        role='user' if current_role == 'User' else 'assistant',
                        content=msg_text,
                        timestamp=timestamp,
                        tool="AntiGravity",
                        session_id=session_id
                    ))

        except Exception as e:
            self.logger.error(f"Error parsing AntiGravity markdown {file_path}: {e}")

        return messages

    def _calculate_message_timestamp(self, base_timestamp: Optional[datetime], message_index: int) -> datetime:
        """AntiGravity 메시지의 타임스탐프 계산 (정확한 개별 타임스탐프가 없으므로 추정)"""
        if base_timestamp is None:
            base_timestamp = datetime.now()

        # 메시지 인덱스별로 약간씩 다른 시간 할당 (정렬 가능하도록)
        return base_timestamp - timedelta(seconds=len(range(message_index)))

    def parse_aide_sessions(self, session_dir: str) -> List[SessionMessage]:
        """Aide 세션 파싱 (향후 확장)"""
        messages = []
        # TODO: Aide 세션 파싱 구현
        self.logger.info("Aide session parsing not yet implemented")
        return messages


class DevlogGenerator:
    """DEVLOG.md 생성"""

    def __init__(self, config: DevlogConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger

    def generate(self, messages: List[SessionMessage], existing_devlog: Optional[str] = None) -> str:
        """DEVLOG.md 내용 생성"""
        output_lines = []

        # 헤더
        project_name = self.config.get('project.name', 'Project')
        output_lines.append(f"# {project_name} - 개발 로그\n")
        output_lines.append(f"생성일: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        output_lines.append("Claude Code와 함께 진행한 개발 작업 기록입니다.\n")
        output_lines.append("---\n")

        # 메시지 날짜별로 그룹핑
        grouped = self._group_by_date(messages)

        # 날짜별 섹션 생성
        day_counter = 1
        for date_str in sorted(grouped.keys()):
            output_lines.append(f"\n## {date_str} (Day {day_counter})\n")
            day_counter += 1

            daily_messages = grouped[date_str]
            task_counter = 1

            # 연속된 user/assistant 쌍을 섹션으로 묶기
            i = 0
            while i < len(daily_messages):
                msg = daily_messages[i]

                # User 메시지 찾기
                if msg.role == 'user':
                    user_msg = msg
                    assistant_msgs = []

                    # 다음에 따라오는 assistant 메시지들 수집
                    i += 1
                    while i < len(daily_messages) and daily_messages[i].role == 'assistant':
                        assistant_msgs.append(daily_messages[i])
                        i += 1

                    # 섹션 생성
                    output_lines.extend(self._create_task_section(
                        task_counter,
                        user_msg,
                        assistant_msgs
                    ))
                    task_counter += 1
                else:
                    i += 1

            output_lines.append("\n---\n")

        # 추가 섹션
        if self.config.get('output.include_sections.commit_history', True):
            output_lines.extend(self._generate_commit_history())

        if self.config.get('output.include_sections.tech_stack', True):
            output_lines.extend(self._generate_tech_stack())

        if self.config.get('output.include_sections.main_features', True):
            output_lines.extend(self._generate_main_features())

        return ''.join(output_lines)

    def _group_by_date(self, messages: List[SessionMessage]) -> Dict[str, List[SessionMessage]]:
        """메시지를 날짜별로 그룹핑"""
        grouped = defaultdict(list)
        date_format = self.config.get('session.date_format', '%Y-%m-%d')

        for msg in sorted(messages, key=lambda m: m.timestamp):
            date_key = msg.timestamp.strftime(date_format)
            grouped[date_key].append(msg)

        return dict(sorted(grouped.items()))

    def _create_task_section(self, task_num: int, user_msg: SessionMessage, assistant_msgs: List[SessionMessage]) -> List[str]:
        """작업 섹션 생성"""
        lines = []

        # 제목 (사용자 메시지 첫 20자)
        title = user_msg.content[:50].replace('\n', ' ')
        tool_name = user_msg.tool if self.config.get('output.show_tool_name', True) else ""
        tool_marker = f" [{tool_name}]" if tool_name else ""

        lines.append(f"### {task_num}. {title}{tool_marker}\n\n")

        # 사용자 요청 (코드블록)
        lines.append("```\n")
        lines.append(user_msg.content[:500])  # 최대 500자
        lines.append("\n```\n\n")

        # Claude 작업 설명
        lines.append("**Claude 작업:**\n")
        if assistant_msgs:
            # 첫 번째 assistant 메시지 요약
            first_response = assistant_msgs[0].content[:300]
            lines.append(f"- {first_response}...\n" if len(first_response) == 300 else f"- {first_response}\n")

            # 추가 메시지가 있으면 언급
            if len(assistant_msgs) > 1:
                lines.append(f"- (추가 {len(assistant_msgs) - 1}개 응답 포함)\n")
        else:
            lines.append("- 응답 처리 중...\n")

        lines.append("\n")
        return lines

    def _generate_commit_history(self) -> List[str]:
        """커밋 히스토리 생성"""
        lines = []
        lines.append("## 커밋 히스토리\n\n")

        try:
            # git log 실행
            result = subprocess.run(
                ['git', 'log', '--oneline', '-20'],
                cwd=self.config.get('project.root_dir', '.'),
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0 and result.stdout:
                commits = result.stdout.strip().split('\n')
                lines.append("| 날짜 | 커밋 | 설명 |\n")
                lines.append("|------|------|------|\n")

                for commit in commits:
                    commit = commit.strip()
                    if commit:
                        parts = commit.split(' ', 1)
                        if len(parts) == 2:
                            commit_hash = parts[0]
                            message = parts[1]
                            # 날짜는 별도로 조회 필요하면 추가
                            lines.append(f"| - | `{commit_hash}` | {message} |\n")

                lines.append("\n")
            else:
                lines.append("(Git 저장소 없음)\n\n")

        except Exception as e:
            self.logger.warning(f"Failed to generate commit history: {e}")
            lines.append("(커밋 히스토리 조회 실패)\n\n")

        lines.append("---\n\n")
        return lines

    def _generate_tech_stack(self) -> List[str]:
        """기술 스택 섹션 생성"""
        lines = []
        lines.append("## 기술 스택\n\n")
        lines.append("- **Language**: Python, JavaScript/TypeScript\n")
        lines.append("- **Tools**: Claude Code, VS Code Extensions\n")
        lines.append("- **DevOps**: Git, GitHub\n")
        lines.append("- **AI**: Claude (Anthropic)\n")
        lines.append("\n---\n\n")
        return lines

    def _generate_main_features(self) -> List[str]:
        """주요 기능 섹션 생성"""
        lines = []
        lines.append("## 주요 기능\n\n")
        lines.append("1. **다중 도구 세션 통합 추적**\n")
        lines.append("   - Claude Code CLI, VS Code Extensions, Aide 등\n")
        lines.append("   - 타임스탐프 기반 자동 정렬 및 그룹핑\n\n")
        lines.append("2. **자동 DEVLOG 생성**\n")
        lines.append("   - 기존 파일 보존 및 점진적 업데이트\n")
        lines.append("   - 날짜별, 도구별 체계적 분류\n\n")
        lines.append("3. **맥락 기반 문서화**\n")
        lines.append("   - IDE 메타데이터 자동 필터링\n")
        lines.append("   - 의미있는 대화만 선별 기록\n\n")
        lines.append("---\n\n")
        return lines


class DevlogLogger:
    """로깅 설정"""

    @staticmethod
    def setup(config: DevlogConfig) -> logging.Logger:
        """로거 초기화"""
        logger = logging.getLogger('devlog')
        logger.setLevel(logging.DEBUG)

        log_level_str = config.get('logging.level', 'INFO')
        log_level = getattr(logging, log_level_str.upper(), logging.INFO)
        logger.setLevel(log_level)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (선택사항)
        if config.get('logging.enabled', True):
            log_file = config.get('logging.log_file', '_systems/01-devlog/logs/devlog.log')
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='통합 개발 로그 생성 시스템',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python unified_devlog_generator.py --config ../config/devlog.config.yaml
  python unified_devlog_generator.py --config ../config/devlog.config.yaml --dry-run
  python unified_devlog_generator.py --config ../config/devlog.config.yaml --from 2025-12-25 --to 2025-12-31
        '''
    )

    parser.add_argument('--config', required=True, help='설정 파일 경로')
    parser.add_argument('--output', help='출력 DEVLOG.md 파일 경로')
    parser.add_argument('--dry-run', action='store_true', help='미리보기 (파일 생성 안함)')
    parser.add_argument('--from', dest='from_date', help='시작 날짜 (YYYY-MM-DD)')
    parser.add_argument('--to', dest='to_date', help='종료 날짜 (YYYY-MM-DD)')
    parser.add_argument('--project-root', help='프로젝트 루트 디렉토리')

    args = parser.parse_args()

    try:
        # 설정 로드
        config = DevlogConfig(args.config)

        # 로거 설정
        logger = DevlogLogger.setup(config)
        logger.info("=" * 60)
        logger.info("통합 개발 로그 생성 시작")
        logger.info("=" * 60)

        # 세션 파싱
        parser_obj = SessionParser(config, logger)
        all_messages = []

        # Claude Code CLI 세션
        if config.get('tools.claude_code_cli.enabled', True):
            logger.info("Claude Code CLI 세션 수집 중...")
            session_dir = config.get('tools.claude_code_cli.session_dir', '~/.claude/projects')
            messages = parser_obj.parse_claude_code_sessions(session_dir)
            all_messages.extend(messages)
            logger.info(f"  → {len(messages)}개 메시지 수집")

        # VS Code 세션 (향후 구현)
        if config.get('tools.vs_code_extension.enabled', False):
            logger.info("VS Code 세션 수집 중... (미지원)")

        # Aide 세션 (향후 구현)
        if config.get('tools.aide.enabled', False):
            logger.info("Aide 세션 수집 중... (미지원)")

        # 날짜 범위 필터링
        if args.from_date:
            from_date = datetime.strptime(args.from_date, '%Y-%m-%d')
            all_messages = [m for m in all_messages if m.timestamp >= from_date]
            logger.info(f"필터링: {args.from_date} 이후의 메시지만 포함")

        if args.to_date:
            to_date = datetime.strptime(args.to_date, '%Y-%m-%d') + timedelta(days=1)
            all_messages = [m for m in all_messages if m.timestamp < to_date]
            logger.info(f"필터링: {args.to_date} 이전의 메시지만 포함")

        logger.info(f"총 {len(all_messages)}개 메시지 처리")

        # DEVLOG 생성
        generator = DevlogGenerator(config, logger)
        devlog_content = generator.generate(all_messages)

        # 출력
        output_path = args.output or config.get('devlog.output_file', 'DEVLOG.md')

        if args.dry_run:
            logger.info("=" * 60)
            logger.info("[DRY RUN] DEVLOG.md 미리보기:")
            logger.info("=" * 60)
            print("\n" + devlog_content[:2000] + "\n... (이하 생략)\n")
            logger.info(f"전체 길이: {len(devlog_content)} 자")
        else:
            output_file = Path(output_path)
            output_file.write_text(devlog_content, encoding='utf-8')
            logger.info(f"DEVLOG 생성 완료: {output_file.absolute()}")

        logger.info("=" * 60)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.error(f"처리 중 오류 발생: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
