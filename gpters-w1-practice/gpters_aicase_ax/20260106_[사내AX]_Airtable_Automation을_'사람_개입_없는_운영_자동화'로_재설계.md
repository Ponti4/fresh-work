# [사내AX] Airtable Automation을 '사람 개입 없는 운영 자동화'로 재설계해보기 (with Claude Code)

- **URL**: https://www.gpters.org/dev/post/sanaeax-airtable-automationeul-saram-gaeib-eobsneun-unyeong-jadonghwa-ro-aFkvSi745CY8nqM


## 한 줄 요약 :

## Claude Code로 Airtable Automation을 '사람 개입 없는 운영 자동화'로 재설계

## 배경

기존에는 Airtable Automation을 활용해 아래와 같은 자동화 작업을 실행하고 있었습니다.

- 매일 오전 9시

- 각 스터디의 신청자 명단을 스터디장에게 이메일로 자동 발송

- 스터디 모집 기간 동안만 Automation을 수동으로 on/off 해야함


![](https://tribe-s3-production.imgix.net/aTchqkWNHm6hDCpfwWrY8?auto=compress,format)

이 방식의 문제점은

- 모집기간 마다, "아, Automation 켜야지/꺼야지" -> 인지적 비용 발생

- 자동화 자체는 단순하지만, 사람이 개입해야만 정상 동작

- 가끔 Airtable 내 문제로 인해 정상 작동하지 않는 경우가 있음

였습니다.

예전 같았으면 n8n으로 로직을 짜서 대체하려고 했겠지만, 바이브코딩으로 쉽게 그리고 궁극적으로 모든 자동화를 AI가 이해하고 개입하기 쉬운 CLI 환경으로 통합해보는 AX 시도를 해보기 위해 아래와 같은 질문을 떠올렸습니다.

- "Claude Code 만으로 스케줄링 + 자동화를 끝까지 가져갈 수 있을까?"


## 목표

- Airtable Automation 완전 대체

- 스터디 모집 기간에 맞춰 자동으로 판단 & 사람이 켜고 끄지 않아도 되는 구조

- 사내 24시간 동작 중인 미니PC를 서버로 활용


## 구현 과정

### 1. 먼저 자동화 정의를 문서로 만들기

- Claude와 대화 과정을 거치고 (
[링크](https://claude.ai/share/766f783f-0e64-42db-9306-dfef3e400187)
),

- 먼저 "설계 문서(md 파일)"을 만들게 함

- 필요에 따라 예시 이메일의 캡쳐본까지 활용하기도 함

- 만들어진 md파일

사본

```
## 스터디 신청자 명단 자동 발송 시스템

개요

매일 오전 9시에 각 스터디의 신청자 명단을 스터디장에게 이메일로 자동 발송하는 시스템

## 기술 스택

- Python 3.x
- pyairtable (Airtable API)
- Gmail API 또는 smtplib
- cron (스케줄링)

## Airtable 구조

### Base 정보

- Base ID: `appqXXXXXXXXXXX`

### 테이블 0: 기수관리

모집 기간 확인용 테이블

- `기수`: 숫자 (예: 20)
- `모집시작일`: 날짜
- `모집마감일`: 날짜

### 테이블 1: 확정된 스터디(건들지X)

조회할 필드:

- `AI스터디 기수`: 숫자 (현재 20기 대상)
- `폐강됨`: 체크박스
- `주제명`: 스터디 제목
- `스터디장s_이메일`: 스터디장 이메일 주소

### 테이블 2: 스터디 신청

조회할 필드:

- `신청스터디`: 링크 필드 (확정된 스터디 테이블과 연결)
- `status`: 텍스트 ("스터디신청" 또는 "변경" 포함)
- `상태`: 텍스트 ("Success" 포함)
- `무료초대_구분`: 텍스트 ("스터디장본인스터디"가 아닌 것만)
- `전화번호`: 신청자 전화번호
- `이메일`: 신청자 이메일
- `이름`: 신청자 이름
- `닉네임`: 신청자 닉네임

## 자동화 로직

```
1. 매일 오전 9시 실행 (cron)

2. 모집 기간 확인 (먼저 실행)
   - '기수관리' 테이블에서 기수 = 20인 레코드 조회
   - 오늘 날짜가 모집시작일 ~ 모집마감일 사이인지 확인
   - 모집 기간이 아니면 실행 종료 (이메일 발송 안 함)

3. Airtable '확정된 스터디(건들지X)' 테이블에서 조회
   - 조건: AI스터디 기수 = 20 AND 폐강됨 = false
   - 결과: 대상 스터디 목록

4. 각 스터디에 대해 반복:
   a. '스터디 신청' 테이블에서 해당 스터디 신청자 조회
      - 조건:
        - 신청스터디 = 현재 스터디
        - status에 "스터디신청" 또는 "변경" 포함
        - 상태에 "Success" 포함
        - 무료초대_구분 ≠ "스터디장본인스터디"

   b. 이메일 발송
      - To: 스터디장s_이메일
      - BCC: ##@gpters.org
      - From: ##@gpters.org
      - Subject: [신청자수명] 주제명 신청자 명단입니다
      - Body: 아래 형식 참고

5. 실행 로그 저장

```

## 이메일 형식

### 제목

```
[{신청자수}명] {주제명} 신청자 명단입니다

```

### 본문 (HTML)

```html
<h2>{주제명}</h2>
<h3>신청자 <strong>{신청자수}</strong>명 (스터디장 제외, 버디 포함)</h3>

<table border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr>
      <th>전화번호</th>
      <th>이메일</th>
      <th>이름</th>
      <th>닉네임</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>01011112222</td>
      <td>sasasa@gmail.com</td>
      <td>노승제</td>
      <td>도라에몽</td>
    </tr>
    <!-- 반복 -->
  </tbody>
</table>

```

## 환경 변수 (필요)

```bash
# Airtable
AIRTABLE_API_KEY=pat_xxxxx  # Personal Access Token
AIRTABLE_BASE_ID=appq8xK4PLp7D7aCg

# Gmail
GMAIL_ADDRESS=yk@gpters.org
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx  # Google App Password

```

## Cron 설정

```bash
# 매일 오전 9시 (KST) 실행
0 9 * * * /usr/bin/python3 /path/to/study_notification.py >> /var/log/study_notification.log 2>&1

```

※ 서버 시간대가 UTC인 경우 `0 0 * * *`로 설정 (UTC 0시 = KST 9시)

## 에러 처리 요구사항

1. Airtable API 호출 실패 시 재시도 (최대 3회)
2. 이메일 발송 실패 시 로그에 기록
3. 전체 실행 결과를 Slack 또는 이메일로 알림 (선택)

## 예상 파일 구조

```
/study-notification/
├── main.py              # 메인 실행 스크립트
├── airtable_client.py   # Airtable API 래퍼
├── email_sender.py      # 이메일 발송 모듈
├── config.py            # 환경 변수 로드
├── requirements.txt     # 의존성 목록
└── README.md            # 실행 방법 안내

```

## 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
export AIRTABLE_API_KEY=pat_xxxxx
export GMAIL_APP_PASSWORD=xxxx

# 수동 실행 (테스트)
python main.py

# cron 등록
crontab -e
# 0 9 * * * /usr/bin/python3 /path/to/main.py

```

## 참고 사항

- Airtable Personal Access Token은 https://airtable.com/create/tokens 에서 발급
- Gmail App Password는 Google 계정 > 보안 > 2단계 인증 > 앱 비밀번호에서 발급
- 테이블 ID는 Airtable URL에서 확인 가능 (tblXXXXX 형식)
```



### 2. Claude Code에게 md 파일을 읽히고 구현 요청

- 정리된 md 파일을 그대로 Claude Code 에게 읽게 한 뒤, 자동화 구현 요청

![](https://tribe-s3-production.imgix.net/EsxGgi2E92tSGtXtHpyRF?auto=compress,format)

- 자동화 실행 전, 필수 사항들을 정리해달라고 요청 -> Airtable, Gmail 관련 설정

![](https://tribe-s3-production.imgix.net/0ZIfpg50mY9bm8sVci70M?auto=compress,format)

- 스케줄링 자동화를 실행하기 위해 서버가 필요함

- 개인 맥 / Cloud / 별도 서버용 PC - 등의 방법이 있으나 우선 개인 맥에서 실행

![](https://tribe-s3-production.imgix.net/pqHRqH142mAoTLDAcA2yl?auto=compress,format)



### 3. 스터디 신청자 명단 자동 발송 시스템 완성

- 자동화 로직 구현

- 매일 오전 9시 실행 / 모집기간 여불르 먼저 판단 - 기간이 아니면 아무 작업도 하지 않음

- 대상 스터디만 필터링 / 조건에 맞는 신청자만 집계

- 스터디장에게 Gmail 발송 / 실행 로그 남김

-> 사람이 개입할 지점이 완전히 사라짐

![](https://tribe-s3-production.imgix.net/0jzTAc8twki38gHiKdhmB?auto=compress,format)



## 테스트

### 1. 로컬(Mac) 환경에서 테스트

- 스케줄러 비활성화

- 특정 스터디 1개를 지정하여 테스트

![](https://tribe-s3-production.imgix.net/sEBLAWEcSP3u95gd2zZWc?auto=compress,format)

- 이메일 정상 발송 확인

![](https://tribe-s3-production.imgix.net/1lVIDWz34FV2zjpvkVWix?auto=compress,format)

- 테스트 데이터 외 실제 데이터를 전송해보도록 시킴 : 정상 발송 (신청자 수, 조건 필터 모두 정상)

![](https://tribe-s3-production.imgix.net/Pd8Fgf9Fv8Hd4QXyj23we?auto=compress,format)


### 2. 미니PC 환경에서 테스트

- 클라우드도 가능했지만, 항상 켜져있는 사내 미니PC를 서버로 활용하기로 결정

- Mac과 동일한 환경 구성

- SETUP_MINIPC.md 가이드 기반 설치

- 환경변수 설정

![](https://tribe-s3-production.imgix.net/gU0k05xJOH3xshhLX94aW?auto=compress,format)

![](https://tribe-s3-production.imgix.net/G4zLN5P8VUq4lpogxG8vJ?auto=compress,format)

** Claude Code가 생성한 SETUP_MINIPC.md 파일에 상세 가이드가 있어 이 가이드에 따라 미니PC에 설치

- 테스트 메일 발송 : 정상

![](https://tribe-s3-production.imgix.net/BsxNdSY9so4xGAHymmMLi?auto=compress,format)

![](https://tribe-s3-production.imgix.net/YQ36N9JM2T0CUolCGLGLb?auto=compress,format)


### 3. 미니PC 환경에서 실제 스케줄링 동작 확인

- Windows 작업 스케줄러 등록 후,

![](https://tribe-s3-production.imgix.net/j2NrflG1rvtWghPm6zj8B?auto=compress,format)

- 스케줄링 동작 확인

- 다음 날 오전 9시 : 메일 미발송 - 작업 스케줄러의 환경변수나 실행경로 설정의 문제로 추정

- Claude Code에게 진단 요청 후, 안내에 따라

- 실행 경로, 환경 변수 수정

- 작업 스케줄러 설정 보완

-> main.py 파일 자체는 잘 동작함(수동 실행)

-> 다음 스케줄러 실행 여부 재확인 예정

- 아래와 같이 Claude Code로 문제 해결 후, 내일 다시 동작 확인하기로 함  (작동할 것으로 예상)

![](https://tribe-s3-production.imgix.net/dz1QRZDH3IKYH6xwQniaZ?auto=compress,format)


## 결과/배운 점

### "결과물을 빨리 만드는 것"보다 "AI를 더 잘 쓰는 방법"이 목적

- 이번 자동화는 단순히 Airtable을 대체하는 것이 아니라, AI가 이해할 수 있는 형태로 명세를 먼저 정리했고, 그 명세를 기준으로 구현, 디버깅, 실행 환경까지 반복적으로 보완한 결과 사람의 개입이 필요 없는 자동화에 도달할 수 있었음

- AI는 코드 생성기가 아니라 설계 파트너 + 리뷰어 + 디버깅 도구로 쓸 때 더 강력해짐

- 바로 구현에 들어가기 보다 명세를 먼저 만들고 그 명세를 기준으로 구현하는 접근이 효과적임


### 다음에 진행한다면,

- 처음부터

- "서버리스 / 클라우드 / 로컬" 각 환경 비교 리서치

- 운영 관점(로그, 장애 대응)까지 설계

- Windows Scheduler 대신 다른 단순한 방법이나 환경 고려

- 앞으로 다른 스케줄링 자동화에도 확대 적용

이처럼, Claude Code로 "기획 -> 설계 -> 구현 -> 디버깅 -> 운영"까지 실제 운영 자동화를 만들어보았습니다. 이 글이 단순히 도구를 바꾸는 것이 아니라, 사람이 개입하지 않아도 되는 자동화를 어떻게 설계할 수 있는지를 고민하는 분들께 조금이나마 참고가 되면 좋겠습니다 🙂
