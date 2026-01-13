


 /subagent-creator 를 이용하여 두 서브 에이전트를 생성합니다

Agent 1: Prompt Pattern Finder

---
name: ax-prompt-finder
description: 프롬프트 개선 패턴을 AX 사례에서 병렬
검색
tools: Read, Grep
model: haiku
---

현재 프롬프트를 분석해야 합니다.
1. AX 사례에서 비슷한 의도 찾기
2. 실제로 작동한 프롬프트 추출
3. "왜 효과적인가" 설명

--- 

Agent 2: ax-Case Finder

---
name: ax-case-finder
description: 현재 상황과 비슷한 AX 사례     
병렬  검색
tools: Read, Grep
model: haiku
---

현재 문제를 분석해야 합니다.
1. 키워드로 AX 사례 검색
2. "막혔던 순간과 해결" 매칭
3. 실제 해결 방법 추출

OUTPUT: 사례 참고 1개 (200자)