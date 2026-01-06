# Task 정의서: editor_소연 게시물 스크래퍼 Skill

**작성일**: 2026-01-06
**자동화 대상**: AI 커뮤니티 "지피터스" - editor_소연님 게시물 스크랩
**상태**: 준비 완료 → Plan Mode 진행

---

## 📊 비즈니스 케이스

| 항목 | 내용 |
|------|------|
| **현재 월 소요시간** | 1-2시간 |
| **연간 절감 시간** | 12-24시간 |
| **스크랩 빈도** | 주 2-3회 |
| **목표 효과** | 더 많은 게시물 읽고 깊이 있게 학습하기 |

---

## 🎯 MVP (Minimum Viable Product)

**핵심 기능 1개만**: 게시물 자동 수집

### 수집 대상
- **URL**: https://www.gpters.org/member/WZlPiwwnpW
- **대상 작가**: editor_소연
- **수집 데이터**:
  - 제목 (title)
  - 게시물 URL (url)
  - 작성일 (date)
  - 요약/설명 (description) - 선택사항

### 저장 방식
- **형식**: Markdown (.md)
- **경로**: `docs/notes/gpters_editor_soyeon/YYYYMMDD_title.md`
- **파일 예시**: `20260106_AI_프롬프트_활용법.md`

---

## 🔧 기술 스택

| 항목 | 선택 |
|------|------|
| **OS** | Windows 11 |
| **Python** | 3.13.7 |
| **웹 스크래핑** | BeautifulSoup4 / Selenium (선택 필요) |
| **스케줄링** | APScheduler (주 2-3회 실행) - 선택사항 |
| **저장 포맷** | Markdown (pathlib으로 관리) |

---

## ❌ 불필요한 기능 (MVP에서 제외)

- ❌ 자동 모니터링 / 스케줄링 (수동 실행으로 시작)
- ❌ 중복 제거 (나중에 추가 가능)
- ❌ 알림 시스템 (이메일/Slack 연동)
- ❌ 분류/태그 시스템
- ❌ 데이터베이스 저장

---

## 📋 구현 체크리스트

### Phase 1: 웹 스크래핑 기능
- [ ] 지피터스 프로필 페이지 접근
- [ ] editor_소연 게시물 목록 파싱
- [ ] 제목, URL, 작성일 추출

### Phase 2: 파일 저장 로직
- [ ] `docs/notes/gpters_editor_soyeon/` 디렉토리 생성
- [ ] Markdown 파일 자동 생성
- [ ] 파일명: `YYYYMMDD_title.md` 형식

### Phase 3: Skill 패키징
- [ ] Python 스크립트를 Claude Code Skill로 변환
- [ ] 사용 설명서 작성

---

## 🚀 다음 단계

**Plan Mode 진행**:
```bash
/plan
```

또는 Claude와 함께 구현 설계를 시작합니다.

---

## 💡 잠재적 고려사항

1. **지피터스 API vs 웹 스크래핑**
   - 지피터스가 API 제공하는지 확인 필요
   - API 있으면 더 안정적, 없으면 BeautifulSoup 사용

2. **동적 콘텐츠**
   - JavaScript로 렌더링되는지 확인
   - 필요시 Selenium 사용

3. **저작권 / 이용 약관**
   - 개인 학습용도이므로 문제없음
   - 상업적 사용 시 확인 필요

---

**📌 준비 완료! Plan Mode로 구현을 시작하세요.**
