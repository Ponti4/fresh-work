#!/bin/bash
# 통합 개발 로그 생성 래퍼 스크립트
# 다양한 AI 도구의 세션을 추적하여 DEVLOG.md 생성
#
# Usage:
#   ./devlog-wrapper.sh
#   ./devlog-wrapper.sh --config config/devlog.config.yaml
#   ./devlog-wrapper.sh --config config/devlog.config.yaml --dry-run
#   ./devlog-wrapper.sh --help

set -euo pipefail

# 스크립트 디렉토리
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$SCRIPT_DIR/scripts"
CONFIG_DIR="$SCRIPT_DIR/config"
LOGS_DIR="$SCRIPT_DIR/logs"

# 기본값
CONFIG_FILE="${CONFIG_DIR}/devlog.config.yaml"
OUTPUT_FILE=""
DRY_RUN=false
FROM_DATE=""
TO_DATE=""
PROJECT_ROOT="."
VERBOSE=false

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 함수: 로그 출력
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# 함수: 사용법 출력
usage() {
    cat << EOF
통합 개발 로그 생성 시스템

Usage:
    $(basename "$0") [OPTIONS]

Options:
    -c, --config FILE       설정 파일 경로 (기본값: ${CONFIG_FILE})
    -o, --output FILE       출력 파일 경로
    -d, --dry-run          미리보기 모드 (파일 생성 안함)
    -f, --from DATE        시작 날짜 (YYYY-MM-DD)
    -t, --to DATE          종료 날짜 (YYYY-MM-DD)
    -r, --root DIR         프로젝트 루트 디렉토리
    -v, --verbose          상세 출력
    -h, --help             이 도움말 표시

Examples:
    # 기본 실행
    $(basename "$0")

    # 미리보기 모드
    $(basename "$0") --dry-run

    # 특정 설정 파일 사용
    $(basename "$0") --config ../config/devlog.config.yaml

    # 기간 지정
    $(basename "$0") --from 2025-12-25 --to 2025-12-31

    # 모든 옵션 함께 사용
    $(basename "$0") \\
        --config config/devlog.config.yaml \\
        --output DEVLOG.md \\
        --from 2025-12-20 \\
        --dry-run

EOF
    exit 0
}

# 함수: 의존성 확인
check_dependencies() {
    local missing=()

    # Python 확인
    if ! command -v python3 &> /dev/null; then
        missing+=("python3")
    fi

    # PyYAML 확인
    if ! python3 -c "import yaml" 2>/dev/null; then
        missing+=("PyYAML (pip install pyyaml)")
    fi

    if [ ${#missing[@]} -gt 0 ]; then
        log_error "다음 의존성을 설치해야 합니다:"
        printf '%s\n' "${missing[@]}" | sed 's/^/  - /'
        return 1
    fi

    return 0
}

# 함수: 설정 파일 확인
check_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        log_error "설정 파일을 찾을 수 없습니다: $CONFIG_FILE"
        log_info "설정 파일 경로:"
        log_info "  기본값: $CONFIG_DIR/devlog.config.yaml"
        log_info "  또는 --config 옵션으로 지정"
        return 1
    fi
}

# 함수: 로그 디렉토리 생성
setup_log_dir() {
    if [ ! -d "$LOGS_DIR" ]; then
        mkdir -p "$LOGS_DIR" || {
            log_warn "로그 디렉토리 생성 실패: $LOGS_DIR"
            return 1
        }
    fi
}

# 함수: Python 스크립트 실행
run_generator() {
    local python_script="$SCRIPTS_DIR/unified_devlog_generator.py"

    if [ ! -f "$python_script" ]; then
        log_error "Python 스크립트를 찾을 수 없습니다: $python_script"
        return 1
    fi

    # 명령행 인자 구성
    local cmd=("python3" "$python_script" "--config" "$CONFIG_FILE")

    if [ -n "$OUTPUT_FILE" ]; then
        cmd+=("--output" "$OUTPUT_FILE")
    fi

    if [ "$DRY_RUN" = true ]; then
        cmd+=("--dry-run")
    fi

    if [ -n "$FROM_DATE" ]; then
        cmd+=("--from" "$FROM_DATE")
    fi

    if [ -n "$TO_DATE" ]; then
        cmd+=("--to" "$TO_DATE")
    fi

    if [ -n "$PROJECT_ROOT" ]; then
        cmd+=("--project-root" "$PROJECT_ROOT")
    fi

    if [ "$VERBOSE" = true ]; then
        log_info "실행 명령어: ${cmd[@]}"
    fi

    # 스크립트 실행
    "${cmd[@]}" || return 1
}

# 함수: 메인 프로세스
main() {
    log_info "=========================================="
    log_info "통합 개발 로그 생성 시스템"
    log_info "=========================================="
    log_info ""

    # 의존성 확인
    if ! check_dependencies; then
        return 1
    fi

    # 설정 파일 확인
    if ! check_config; then
        return 1
    fi

    log_info "설정 파일: $CONFIG_FILE"

    # 로그 디렉토리 준비
    setup_log_dir

    # Python 스크립트 실행
    log_info "개발 로그 생성 중..."
    log_info ""

    if run_generator; then
        log_success ""
        log_success "완료!"
        if [ "$DRY_RUN" = true ]; then
            log_info "미리보기 모드였습니다. 실제 파일을 생성하려면 --dry-run 옵션을 제거하세요."
        fi
        return 0
    else
        log_error "개발 로그 생성 중 오류 발생"
        return 1
    fi
}

# 인자 파싱
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -f|--from)
            FROM_DATE="$2"
            shift 2
            ;;
        -t|--to)
            TO_DATE="$2"
            shift 2
            ;;
        -r|--root)
            PROJECT_ROOT="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            log_error "알 수 없는 옵션: $1"
            echo ""
            usage
            ;;
    esac
done

# 메인 실행
if main; then
    exit 0
else
    exit 1
fi
