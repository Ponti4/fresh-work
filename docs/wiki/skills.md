# Agent Skills

> Claude Code에서 Claude의 기능을 확장하기 위해 Skills를 생성, 관리 및 공유합니다.

이 가이드는 Claude Code에서 Agent Skills를 생성, 사용 및 관리하는 방법을 보여줍니다. Skills는 지침, 스크립트 및 리소스를 포함하는 구성된 폴더를 통해 Claude의 기능을 확장하는 모듈식 기능입니다.

## 필수 조건

* Claude Code 버전 1.0 이상
* [Claude Code](/ko/quickstart)에 대한 기본 지식

## Agent Skills란 무엇인가요?

Agent Skills는 전문 지식을 발견 가능한 기능으로 패키징합니다. 각 Skill은 Claude가 관련이 있을 때 읽는 지침이 포함된 `SKILL.md` 파일과 스크립트 및 템플릿과 같은 선택적 지원 파일로 구성됩니다.

**Skills가 호출되는 방식**: Skills는 **모델 호출**입니다—Claude는 사용자의 요청과 Skill의 설명을 기반으로 자율적으로 사용 시기를 결정합니다. 이는 **사용자 호출** 슬래시 명령어(명시적으로 `/command`를 입력하여 트리거)와 다릅니다.

**이점**:

* 특정 워크플로우를 위해 Claude의 기능 확장
* git을 통해 팀 전체에서 전문 지식 공유
* 반복적인 프롬프팅 감소
* 복잡한 작업을 위해 여러 Skills 구성

[Agent Skills 개요](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)에서 자세히 알아보세요.

<Note>
  Agent Skills의 아키텍처 및 실제 응용 프로그램에 대한 심층 분석을 위해 엔지니어링 블로그를 읽어보세요: [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
</Note>

## Skill 생성

Skills는 `SKILL.md` 파일을 포함하는 디렉토리로 저장됩니다.

### Personal Skills

Personal Skills는 모든 프로젝트에서 사용 가능합니다. `~/.claude/skills/`에 저장하세요:

```bash  theme={null}
mkdir -p ~/.claude/skills/my-skill-name
```

**Personal Skills 사용 대상**:

* 개인 워크플로우 및 기본 설정
* 개발 중인 실험적 Skills
* 개인 생산성 도구

### Project Skills

Project Skills는 팀과 공유됩니다. 프로젝트 내 `.claude/skills/`에 저장하세요:

```bash  theme={null}
mkdir -p .claude/skills/my-skill-name
```

**Project Skills 사용 대상**:

* 팀 워크플로우 및 규칙
* 프로젝트별 전문 지식
* 공유 유틸리티 및 스크립트

Project Skills는 git에 체크인되며 팀 멤버에게 자동으로 사용 가능합니다.

### Plugin Skills

Skills는 [Claude Code 플러그인](/ko/plugins)에서도 제공될 수 있습니다. 플러그인은 플러그인이 설치될 때 자동으로 사용 가능한 Skills를 번들로 제공할 수 있습니다. 이러한 Skills는 personal 및 project Skills와 동일한 방식으로 작동합니다.

## SKILL.md 작성

YAML 프론트매터와 Markdown 콘텐츠가 포함된 `SKILL.md` 파일을 생성하세요:

```yaml  theme={null}
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.
```

**필드 요구사항**:

* `name`: 소문자, 숫자 및 하이픈만 사용해야 함(최대 64자)
* `description`: Skill이 수행하는 작업과 사용 시기에 대한 간단한 설명(최대 1024자)

`description` 필드는 Claude가 Skill을 사용할 시기를 발견하는 데 중요합니다. Skill이 수행하는 작업과 Claude가 사용해야 할 시기를 모두 포함해야 합니다.

검증 규칙을 포함한 완전한 작성 지침은 [모범 사례 가이드](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)를 참조하세요.

## 지원 파일 추가

SKILL.md 옆에 추가 파일을 생성하세요:

```
my-skill/
├── SKILL.md (required)
├── reference.md (optional documentation)
├── examples.md (optional examples)
├── scripts/
│   └── helper.py (optional utility)
└── templates/
    └── template.txt (optional template)
```

SKILL.md에서 이러한 파일을 참조하세요:

````markdown  theme={null}
For advanced usage, see [reference.md](reference.md).

Run the helper script:
```bash
python scripts/helper.py input.txt
```
````

Claude는 필요할 때만 이러한 파일을 읽으며, 점진적 공개를 사용하여 컨텍스트를 효율적으로 관리합니다.

## allowed-tools로 도구 액세스 제한

`allowed-tools` 프론트매터 필드를 사용하여 Skill이 활성화될 때 Claude가 사용할 수 있는 도구를 제한하세요:

```yaml  theme={null}
---
name: safe-file-reader
description: Read files without making changes. Use when you need read-only file access.
allowed-tools: Read, Grep, Glob
---

# Safe File Reader

This Skill provides read-only file access.

## Instructions
1. Use Read to view file contents
2. Use Grep to search within files
3. Use Glob to find files by pattern
```

이 Skill이 활성화되면 Claude는 권한을 요청할 필요 없이 지정된 도구(Read, Grep, Glob)만 사용할 수 있습니다. 이는 다음에 유용합니다:

* 파일을 수정하지 않아야 하는 읽기 전용 Skills
* 제한된 범위의 Skills(예: 데이터 분석만, 파일 쓰기 없음)
* 기능을 제한하려는 보안에 민감한 워크플로우

`allowed-tools`를 지정하지 않으면 Claude는 표준 권한 모델을 따르면서 일반적으로 도구 사용 권한을 요청합니다.

<Note>
  `allowed-tools`는 Claude Code의 Skills에서만 지원됩니다.
</Note>

## 사용 가능한 Skills 보기

Skills는 Claude에 의해 세 가지 소스에서 자동으로 발견됩니다:

* Personal Skills: `~/.claude/skills/`
* Project Skills: `.claude/skills/`
* Plugin Skills: 설치된 플러그인과 함께 번들됨

**모든 사용 가능한 Skills를 보려면** Claude에 직접 질문하세요:

```
What Skills are available?
```

또는

```
List all available Skills
```

이는 플러그인 Skills를 포함한 모든 소스의 모든 Skills를 표시합니다.

**특정 Skill을 검사하려면** 파일 시스템을 확인할 수도 있습니다:

```bash  theme={null}
# List personal Skills
ls ~/.claude/skills/

# List project Skills (if in a project directory)
ls .claude/skills/

# View a specific Skill's content
cat ~/.claude/skills/my-skill/SKILL.md
```

## Skill 테스트

Skill을 생성한 후 설명과 일치하는 질문을 하여 테스트하세요.

**예**: 설명에 "PDF 파일"이 언급되어 있으면:

```
Can you help me extract text from this PDF?
```

Claude는 요청과 일치하면 자율적으로 Skill을 사용하기로 결정합니다—명시적으로 호출할 필요가 없습니다. Skill은 질문의 컨텍스트를 기반으로 자동으로 활성화됩니다.

## Skill 디버깅

Claude가 Skill을 사용하지 않으면 다음 일반적인 문제를 확인하세요:

### 설명을 구체적으로 작성

**너무 모호함**:

```yaml  theme={null}
description: Helps with documents
```

**구체적**:

```yaml  theme={null}
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

설명에 Skill이 수행하는 작업과 사용 시기를 모두 포함하세요.

### 파일 경로 확인

**Personal Skills**: `~/.claude/skills/skill-name/SKILL.md`
**Project Skills**: `.claude/skills/skill-name/SKILL.md`

파일이 존재하는지 확인하세요:

```bash  theme={null}
# Personal
ls ~/.claude/skills/my-skill/SKILL.md

# Project
ls .claude/skills/my-skill/SKILL.md
```

### YAML 구문 확인

잘못된 YAML은 Skill이 로드되지 않도록 합니다. 프론트매터를 확인하세요:

```bash  theme={null}
cat SKILL.md | head -n 10
```

다음을 확인하세요:

* 1번 줄에 시작 `---`
* Markdown 콘텐츠 전에 종료 `---`
* 유효한 YAML 구문(탭 없음, 올바른 들여쓰기)

### 오류 보기

디버그 모드로 Claude Code를 실행하여 Skill 로드 오류를 확인하세요:

```bash  theme={null}
claude --debug
```

## 팀과 Skills 공유

**권장 접근 방식**: [플러그인](/ko/plugins)을 통해 Skills를 배포하세요.

플러그인을 통해 Skills를 공유하려면:

1. `skills/` 디렉토리에 Skills가 있는 플러그인 생성
2. 플러그인을 마켓플레이스에 추가
3. 팀 멤버가 플러그인 설치

완전한 지침은 [플러그인에 Skills 추가](/ko/plugins#add-skills-to-your-plugin)를 참조하세요.

프로젝트 저장소를 통해 직접 Skills를 공유할 수도 있습니다:

### 1단계: 프로젝트에 Skill 추가

프로젝트 Skill을 생성하세요:

```bash  theme={null}
mkdir -p .claude/skills/team-skill
# Create SKILL.md
```

### 2단계: git에 커밋

```bash  theme={null}
git add .claude/skills/
git commit -m "Add team Skill for PDF processing"
git push
```

### 3단계: 팀 멤버가 자동으로 Skills 받기

팀 멤버가 최신 변경사항을 가져오면 Skills를 즉시 사용할 수 있습니다:

```bash  theme={null}
git pull
claude  # Skills are now available
```

## Skill 업데이트

SKILL.md를 직접 편집하세요:

```bash  theme={null}
# Personal Skill
code ~/.claude/skills/my-skill/SKILL.md

# Project Skill
code .claude/skills/my-skill/SKILL.md
```

변경사항은 다음에 Claude Code를 시작할 때 적용됩니다. Claude Code가 이미 실행 중이면 업데이트를 로드하려면 다시 시작하세요.

## Skill 제거

Skill 디렉토리를 삭제하세요:

```bash  theme={null}
# Personal
rm -rf ~/.claude/skills/my-skill

# Project
rm -rf .claude/skills/my-skill
git commit -m "Remove unused Skill"
```

## 모범 사례

### Skills를 집중적으로 유지

하나의 Skill은 하나의 기능을 다루어야 합니다:

**집중적**:

* "PDF form filling"
* "Excel data analysis"
* "Git commit messages"

**너무 광범위**:

* "Document processing" (별도의 Skills로 분할)
* "Data tools" (데이터 유형 또는 작업별로 분할)

### 명확한 설명 작성

설명에 특정 트리거를 포함하여 Claude가 Skills를 발견하도록 도와주세요:

**명확**:

```yaml  theme={null}
description: Analyze Excel spreadsheets, create pivot tables, and generate charts. Use when working with Excel files, spreadsheets, or analyzing tabular data in .xlsx format.
```

**모호**:

```yaml  theme={null}
description: For files
```

### 팀과 함께 테스트

팀 멤버가 Skills를 사용하고 피드백을 제공하도록 하세요:

* Skill이 예상대로 활성화되나요?
* 지침이 명확한가요?
* 누락된 예제나 엣지 케이스가 있나요?

### Skill 버전 문서화

SKILL.md 콘텐츠에서 Skill 버전을 문서화하여 시간 경과에 따른 변경사항을 추적할 수 있습니다. 버전 기록 섹션을 추가하세요:

```markdown  theme={null}
# My Skill

## Version History
- v2.0.0 (2025-10-01): Breaking changes to API
- v1.1.0 (2025-09-15): Added new features
- v1.0.0 (2025-09-01): Initial release
```

이는 팀 멤버가 버전 간 변경사항을 이해하는 데 도움이 됩니다.

## 문제 해결

### Claude가 내 Skill을 사용하지 않음

**증상**: 관련 질문을 하지만 Claude가 Skill을 사용하지 않습니다.

**확인**: 설명이 충분히 구체적인가요?

모호한 설명은 발견을 어렵게 합니다. Skill이 수행하는 작업과 사용 시기를 모두 포함하고 사용자가 언급할 주요 용어를 포함하세요.

**너무 일반적**:

```yaml  theme={null}
description: Helps with data
```

**구체적**:

```yaml  theme={null}
description: Analyze Excel spreadsheets, generate pivot tables, create charts. Use when working with Excel files, spreadsheets, or .xlsx files.
```

**확인**: YAML이 유효한가요?

검증을 실행하여 구문 오류를 확인하세요:

```bash  theme={null}
# View frontmatter
cat .claude/skills/my-skill/SKILL.md | head -n 15

# Check for common issues
# - Missing opening or closing ---
# - Tabs instead of spaces
# - Unquoted strings with special characters
```

**확인**: Skill이 올바른 위치에 있나요?

```bash  theme={null}
# Personal Skills
ls ~/.claude/skills/*/SKILL.md

# Project Skills
ls .claude/skills/*/SKILL.md
```

### Skill에 오류가 있음

**증상**: Skill이 로드되지만 제대로 작동하지 않습니다.

**확인**: 종속성을 사용할 수 있나요?

Claude는 필요할 때 필요한 종속성을 자동으로 설치하거나(또는 설치 권한을 요청) 설치합니다.

**확인**: 스크립트에 실행 권한이 있나요?

```bash  theme={null}
chmod +x .claude/skills/my-skill/scripts/*.py
```

**확인**: 파일 경로가 올바른가요?

모든 경로에서 슬래시(Unix 스타일)를 사용하세요:

**올바름**: `scripts/helper.py`
**잘못됨**: `scripts\helper.py` (Windows 스타일)

### 여러 Skills 충돌

**증상**: Claude가 잘못된 Skill을 사용하거나 유사한 Skills 간에 혼동되는 것 같습니다.

**설명에서 구체적으로 작성**: 설명에서 고유한 트리거 용어를 사용하여 Claude가 올바른 Skill을 선택하도록 도와주세요.

대신:

```yaml  theme={null}
# Skill 1
description: For data analysis

# Skill 2
description: For analyzing data
```

사용:

```yaml  theme={null}
# Skill 1
description: Analyze sales data in Excel files and CRM exports. Use for sales reports, pipeline analysis, and revenue tracking.

# Skill 2
description: Analyze log files and system metrics data. Use for performance monitoring, debugging, and system diagnostics.
```

## 예제

### 간단한 Skill (단일 파일)

```
commit-helper/
└── SKILL.md
```

```yaml  theme={null}
---
name: generating-commit-messages
description: Generates clear commit messages from git diffs. Use when writing commit messages or reviewing staged changes.
---

# Generating Commit Messages

## Instructions

1. Run `git diff --staged` to see changes
2. I'll suggest a commit message with:
   - Summary under 50 characters
   - Detailed description
   - Affected components

## Best practices

- Use present tense
- Explain what and why, not how
```

### 도구 권한이 있는 Skill

```
code-reviewer/
└── SKILL.md
```

```yaml  theme={null}
---
name: code-reviewer
description: Review code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
allowed-tools: Read, Grep, Glob
---

# Code Reviewer

## Review checklist

1. Code organization and structure
2. Error handling
3. Performance considerations
4. Security concerns
5. Test coverage

## Instructions

1. Read the target files using Read tool
2. Search for patterns using Grep
3. Find related files using Glob
4. Provide detailed feedback on code quality
```

### 다중 파일 Skill

```
pdf-processing/
├── SKILL.md
├── FORMS.md
├── REFERENCE.md
└── scripts/
    ├── fill_form.py
    └── validate.py
```

**SKILL.md**:

````yaml  theme={null}
---
name: pdf-processing
description: Extract text, fill forms, merge PDFs. Use when working with PDF files, forms, or document extraction. Requires pypdf and pdfplumber packages.
---

# PDF Processing

## Quick start

Extract text:
```python
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

For form filling, see [FORMS.md](FORMS.md).
For detailed API reference, see [REFERENCE.md](REFERENCE.md).

## Requirements

Packages must be installed in your environment:
```bash
pip install pypdf pdfplumber
```
````

<Note>
  필수 패키지를 설명에 나열하세요. Claude가 사용하기 전에 패키지를 환경에 설치해야 합니다.
</Note>

Claude는 필요할 때만 추가 파일을 로드합니다.

## 다음 단계

<CardGroup cols={2}>
  <Card title="작성 모범 사례" icon="lightbulb" href="https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices">
    Claude가 효과적으로 사용할 수 있는 Skills 작성
  </Card>

  <Card title="Agent Skills 개요" icon="book" href="https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview">
    Claude 제품 전체에서 Skills가 어떻게 작동하는지 알아보기
  </Card>

  <Card title="Agent SDK에서 Skills 사용" icon="cube" href="https://docs.claude.com/en/docs/agent-sdk/skills">
    TypeScript 및 Python으로 프로그래밍 방식으로 Skills 사용
  </Card>

  <Card title="Agent Skills 시작하기" icon="rocket" href="https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart">
    첫 번째 Skill 생성
  </Card>
</CardGroup>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://code.claude.com/docs/llms.txt