
## 17:00 

해당 작업이 성공적으로 잘 된 이유를 설명하라
이후 이렇게 작업을 더 잘하기 위해 어떻게 해야하는지 
프롬프트와 재사용이 용이한 스크립트로서 설명하라

--- 

1. 파일명: 새 문서를 어떻게 이름 지을까요?
- 10.4-task-design.md (같은 단계 계속)
- 11-design.md (새로운 섹션)
- 다른 이름?
2. 설계 파트의 목표: 어떤 내용을 포함해야 할까요?
- Task 명확화 후 → 자동화 솔루션을 설계하는 단계?
- 기술 스택, 아키텍처, 구현 방식을 결정하는 부분?
- 구체적인 구현 계획(단계별)?
3. 구조: 현재 10.3처럼 구조화된 질문 형식을 이어갈까요, 아니면 다른 형식으 로?

--- 

## 10.5 설계 문서화

title : 10.5 automation-architecture-design.md
이후 설계 문서는 마크다운, 한국어로 모호/누락 없이 간결하게 작성한다 

이후 사용자에게 설계문서 경로 : docs/{title}/{title}.md 로 만들어도 되는지 동의를 묻는 과정을 반영한다

설계 문서를 만든 다음, 

스크립트로 만들 수 있는 내용에서 git bash & Python 3.11.7 버전을 준수하여 작성해야 한다

구현은 tdd 를 준수하여 작성한다. 
tdd path : __test__/{YYYYMMDD}_title 형식으로 테스트 코드를 
작성하고 올바르게 실행되면 scripts 경로에 코드를 작성해야한다.
script path : _scripts/{title}

# 25/12/28

## S : devlog Context 스크립트 작성

AIDE, vscode claude extensions, claude code cli
해당 작업의 세션을 파악하는 스크립트
이의 대화 이력을 읽고, 


## pr

현재 프로젝트 이용자는 claude code cli, vs code extensions, aide  등의     
이용을 진행하기 때문에 적절한 세션을 추적, 이후 log 로 작성하기 위한       
스크립트를 `_system/01-devlog` path 에서 작성한다.
스크립트는 python, git bash 를 이용해야한다.

--- 

올바르게 실헹되고 있는지 qa 진행한다
현재 대화 세션 기준으로, 해당 스크립트가 현재 대화 세션을 올바르게 

