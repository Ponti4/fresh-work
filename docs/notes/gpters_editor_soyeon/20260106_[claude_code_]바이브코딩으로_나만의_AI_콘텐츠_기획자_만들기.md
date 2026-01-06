# [claude code ]바이브코딩으로 나만의 AI 콘텐츠 기획자 만들기

- **작성일**: 2026-01-06
- **URL**: [https://www.gpters.org/marketing/post/create-your-own-ai-X4ZU5c5k3Sv4Ut5](https://www.gpters.org/marketing/post/create-your-own-ai-X4ZU5c5k3Sv4Ut5)

## 요약
[
## [claude code ]바이브코딩으로 나만의 AI 콘텐츠 기획자 만들기
](/marketing/post/create-your-own-ai-X4ZU5c5k3Sv4Ut5)

콘텐츠 마케팅을 하다보면 글감(source)를 찾고 개괄적인 내용을 작성해도 이를 베리에이션하는데 시간이 걸리는데요.

이 작업을 위해 GPTs를 만들거나 LLM 맞춤 지침을 설정할 수 있기는하지만 2~5개 정도의 포맷을 매번 텍스트로 요청하는 것도 번거롭다고 생각했어요.

이상적으로 생각하는 컨텐츠 파이프라인의 구조는 아래와 같았습니다. 오늘은 기획-제작 부분 구현에 대한 바이브코딩기를 공유하려고해요.

- [[지난 글: 소스 수집]](/dev/post/content-automation-ai-era-jjUC06rnpnAJjbC)
- 이 작업은 이미 마쳐서 활용중입니다!

- 콘텐츠 기획 - 콘텐츠 아이디어도 매번 AI한테 추천 받을 수 없을까?

- 콘텐츠 제작 - 포맷별로 결과물이 나와야한다

- 콘텐츠 분석

![](https://tribe-s3-production.imgix.net/Ou7yOdWFDWvGfIJ6WCSYG?auto=compress,format)

### 1. 화면 설계

기획 문서를 먼저 작성하는 것이 좋지만 (!!) 아무래도 비개발자다보니 개발 지식에 한계가 있어 md 파일로 클로드코드와 티키타카를 하며 내가 만들고 싶은 서비스를 기획하는 것에 어려움이 있었습니다.

그래서 저는 이 단계로 처음에 프로젝트 빌딩을 하는데요

- 구현하고싶은 서비스에 대해 자연어로 지피티와 기획

- 해당 화면을 잘 구현해줄 수 있는 영문 프롬프트 도출

- 러버블/구글AI스튜디오 빌드/피그마 등 프론트를 구현할 수 있는 툴에 적용해보기

- 제 기준에서는 러버블이 조금 더 투박한 느낌이네요.

- 러버블

![중국사이트 스크린샷](https://tribe-s3-production.imgix.net/1kP6r0pefXq9ub6Xjiwl5?auto=compress,format)

- 구글 Build

![](https://tribe-s3-production.imgix.net/TkqGlSYGElDksNYZpKG3O?auto=compress,format)

몇가지 팁이 있다면 ..

- 프론트를 구현할 때는 같은 프롬프트로 여러 툴에 넣어보는 것이 좋다

- 각각 컴포넌트를 조합해서 활용한다

- 구글 빌드의 경우 API가 필요한 AI 활용까지 미리 구현해볼 수 있다 (구글의 권력..)

- 프론트가 필요하지않은 서비스라면 구현에 시간을 많이 쏟지않는다

비개발자가 바이브 코딩을 하다보면 프론트 구현이 적당히만 되면 되어도

욕심을 내 시간을 허비하는 경우도 있는 것 같아서 이 부분에 염두하는 게 좋을 것 같아요!

### 2. 개발 기획 및 스택 설정

![](https://tribe-s3-production.imgix.net/zA5QS4DBFokurm0PYFVkd?auto=compress,format)

구글 빌드, 러버블 모두 깃에 저장이 가능해서 해당하는 레포지토리에 올려주고 클로드 코드를 실행하는데요.

프로젝트 폴더에 build로 구현한 파일을 모두 넣고 아래처럼 요청합니다.

사본

```
bulild 폴더 파일을 읽고 가장 적절한 개발 기획을 진행해주고 해당 내용을 .md 파일로 넣어줘 ]
```

기술스택은 이렇게 설정해줬네요.

Frontend: React 18 + TypeScript + Vite

Styling: Tailwind CSS

AI: Google Gemini 2.5 Flash API

Markdown Rendering: react-markdown

### 세부 조정+ 추가 기획

![](https://tribe-s3-production.imgix.net/sdAGqf5IKX1JAOjlVBoF1?auto=compress,format)

![한국어 페이지 스크린샷](https://tribe-s3-production.imgix.net/AsLB9xmqvYvbpngByStD0?auto=compress,format)

url이나 텍스트를 넣으면 원하는 포맷으로 생성해주는 것은 사실

GPTs를 고도화해서 만드는 느낌이라 그것보다 더 편하고 효율적인 방법이 필요했어요.

![](https://tribe-s3-production.imgix.net/I8D5PPA0c3IQajBXx1HVO?auto=compress,format)

그러다가 AI한테 글의 테마까지 추천 받자 라는 생각이 떠올랐어요!

사본

```
[산출된 결과물 하단에 같은 소스로 쓸 수 있는 새로운 콘텐츠 주제 4가지를 제안해줘]
```

이때 4가지 주제는 지금까지 발행했던 콘텐츠 중에서 결과가 좋았던 것들의 공통점을 뽑아 주제를

제가 먼저 제안했습니다. 그게 무엇인지는 비밀 ..(아무도 안궁금해하시겠지만)

![](https://tribe-s3-production.imgix.net/ZhkjG8IQrwcug0OlZMLNA?auto=compress,format)

이렇게 4가지 중 궁금한 것을 누르면 바로 완성된 콘텐츠로 보여주는데요.

이렇게 생성된 글을 바로 콘텐츠로 활용하기엔 어렵지만

아이데이션도 되고 주제를 확장할 수 있다는 점에서 만족스러웠어요.

콘텐츠 마케팅에서는 무조건 업무를 자동화하기보다 확장하고 퀄리티를 높여야하는 부분에 AI를 잘 활용하는 것이 매우 중요하다고 생각해서 주제를 제안해주는 일이 아이데이션에 도움이 된다고 생각했습니다.

그러다보니 해당 제안으로 얻게된 아이디어로 또 변형할수도있겠다싶어서..

![](https://tribe-s3-production.imgix.net/TA2TT9GocP3tpxWry626O?auto=compress,format)

이 마저도 자연어로 넣으면 되게끔 업그레이드 시켰습니다!

별거 아니어도 이 기능이 추가되니 훨씬 콘텐츠를 생성하는 것에

제약이 없어지고 좀 더 마케터의 직관과 역량을 활용할 수 있게 됐다고 느꼈어요.

![](https://tribe-s3-production.imgix.net/tZKBbyJ1qpL9LXwEp3ZPp?auto=compress,format)

### 결과

클로드 코드로 구현한 이 서비스로 1일 2콘텐츠 발행이 가능해졌어요.

주제 확장성이 있기때문에 하나의 소스로도 여러개의 포맷뿐 아니라 콘텐츠를 생성할 수 있게됐습니다.

- 보통 콘텐츠 기획하고 작성하는데 드는 시간이 2시간이었다면 30분으로 줄어든 것 같아요.

- 발행량과 주제가 늘어나니 SNS 기준 조회수도 평균대비 2배로 올라갔습니다.

무엇보다 콘텐츠 발행을 무겁게 접근하기보다 브레인스토밍하듯 그려나갈 수 있게된 점이 가장 좋았어요.

추후에는 성과 측정을 통한 콘텐츠 기획쪽 강화 부분을 보강해보려고해요🍀

더 보기

4

[1개의 답글](/marketing/post/create-your-own-ai-X4ZU5c5k3Sv4Ut5#replies)

---

**수집 일시**: 2026-01-06 15:55:18
