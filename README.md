# Fresh Work - 암환자 맞춤형 일자리 플랫폼

**목표**: 인터넷 구인 공고를 크롤링하여 암환자를 위한 맞춤형 일자리 제공

---

## 🎯 빠른 시작

**지금 바로 시작하세요:**

```bash
/setup-workspace
```

이 명령어가 자동으로 당신의 프로필을 [`CLAUDE.md`](CLAUDE.md)에 저장하고, 첫 자동화를 시작하게 됩니다!

---

## 👋 이 프로젝트는?

**Fresh Work**는 암을 경험한 분들이 지금 당장 할 수 있는 일자리를 찾도록 도와주는 플랫폼입니다.

우리가 하는 일:
- ✅ 인터넷의 다양한 구인 공고를 자동으로 수집하고
- ✅ 암환자 친화적의 업무 조건으로 필터링하고
- ✅ 한 곳에 모아서 쉽게 볼 수 있도록 제공합니다!

---

## 📚 폴더 구조

```
.claude/                          ← Claude Code 설정 (자동화의 핵심!)
├── commands/                     (사용자가 호출하는 명령어)
│   ├── setup-workspace.md        (/setup-workspace - 초기 설정)
│   ├── clarify.md                (/clarify - 요구사항 명확화)
│   ├── think-partner.md          (/think-partner - 목표 명확화)
│   ├── ai-case-writer.md         (/ai-case-writer - 사례 글 작성)
│   ├── devlog-writer.md          (/devlog-writer - 작업 기록)
│   └── git-commit.md             (/git-commit - Git 커밋 자동화)
│
├── skills/                       (재사용 가능한 로직)
│   ├── fresh-work-scraper/       (구인 공고 수집)
│   ├── job-filter/               (암환자 맞춤 필터링)
│   ├── web-ui/                   (웹 인터페이스)
│   ├── notification/             (새 공고 알림)
│   ├── scheduler/                (정기 크롤링)
│   └── analytics/                (사용자 분석)
│
├── agents/                       (특화된 Sub-Agents)
│   ├── ax-case-finder.md         (AX 사례 검색)
│   ├── code-simplifier.md        (코드 간소화)
│   └── markdown-optimizer.md     (문서 토큰 최적화)
│
└── reference/                    (상세 참고 자료)
    ├── clarify/                  (요구사항 명확화 가이드)
    ├── think-partner/            (목표 명확화 가이드)
    └── ai-case-writer/           (AI 사례 글 작성 가이드)

docs/                             ← 문서 및 학습 자료
├── wiki/                         (설치, Git, Python 가이드)
│   ├── bash-terminal-guide.md    (터미널 가이드)
│   ├── git-setup-and-usage.md    (Git 사용법)
│   ├── python-setup-guide.md     (Python 설치)
│   ├── hooks.md                  (Claude Code Hooks)
│   ├── skills-simplification-guide.md  (Skill 생성법)
│   ├── token-optimization-*.md   (토큰 최적화 가이드)
│   └── claude-code-change-log.md (변경사항 기록)
│
├── prompts/                      (프롬프트 템플릿)
├── plan/                         (프로젝트 계획)
├── job_posts/                    (수집된 구인 공고)
├── filtered_jobs/                (필터링된 일자리)
└── _devlog/                      (작업 기록)

CLAUDE.md                         ← 📍 프로젝트 대시보드 (여기서 시작!)
```

**필요할 때 찾아보세요 (Lazy Load):**
- 설치 문제? → `docs/wiki/python-setup-guide.md`
- 깃 사용법? → `docs/wiki/git-setup-and-usage.md`
- Skill 만드는 법? → `docs/wiki/skills-simplification-guide.md`
- 토큰 최적화? → `docs/wiki/token-optimization-*.md`

---

## 🚀 워크플로우

1. `/setup-workspace` → 당신의 정보 수집
2. `/clarify "반복 업무"` → 자동화 방안 제시
3. 설계 + 구현 → Claude와 협력
4. `/git-commit` → 저장
5. **반복 (3회)** → 4주 목표 달성

---

## 📅 주차별 과제

| 주차 | 과제 | 결과물 |
|------|------|--------|
| **W1** | 구인 공고 크롤링 로직 개발 | 크롤러 알고리즘 완성 |
| **W2** | 구인 공고 크롤링 로직 개발 → 테스트 및 개선 | 크롤러 알고리즘 완성 |
| **W3** | 암환자 친화 필터링 로직 개발 → 웹 인터페이스 구축 | 필터링 시스템 + 웹 UI |
| **W4** | 베타 테스트 및 피드백 수집 → 개선 및 배포 | 서비스 런칭 |

---

## 🆘 막혔을 때

| 상황 | 찾아보기 |
|------|---------|
| 설치 오류 | `docs/wiki/python-setup-guide.md` 참고 |
| 깃 사용 문제 | `docs/wiki/git-setup-and-usage.md` 참고 |
| Plan Mode 진행 중 | Claude에게 직접 물어보기 |
| Skill/Sub-Agent 만들기 | `docs/wiki/skills-simplification-guide.md` 참고 |

---

🤖 **Claude와 함께 시작하세요!**
