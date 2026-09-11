# Firebase 연동 절차

학생은 학교 Google 계정(`@e-mirim.hs.kr`)으로 로그인하고, 반·번호는 교사가 미리 등록한 명단에서 가져옵니다.
GitHub Pages는 정적 호스팅이므로 서버 비밀을 둘 수 없습니다. 모든 권한 판단은 `firestore.rules`가 합니다.

## 1. 프로젝트 만들기

1. https://console.firebase.google.com 에서 **프로젝트 추가**. 이름은 `aipy2-lab` 등 자유. Google 애널리틱스는 끄세요.
2. 프로젝트 개요에서 **웹 앱 추가**(`</>` 아이콘). 닉네임은 `aipy2-web`. **Firebase Hosting 설정은 체크하지 않습니다.**
3. 표시되는 `firebaseConfig` 값을 [web/assets/firebase-config.js](../web/assets/firebase-config.js)에 붙여넣고 커밋합니다.
   `apiKey`는 비밀키가 아니라 프로젝트 식별자이므로 공개 저장소에 그대로 두어도 됩니다.

## 2. Google 로그인 켜기

1. **Authentication → 시작하기 → Google** 공급자를 사용 설정하고, 프로젝트 지원 이메일을 선택해 저장합니다.
2. **Authentication → Settings → 승인된 도메인**에 `progh2.github.io`를 추가합니다. `localhost`는 기본 포함입니다.
3. 로그인 창에 보이는 앱 이름은 **프로젝트 설정 → 공개 표시 이름**에서 바꿉니다.

> 학교가 Google Workspace 관리 콘솔에서 서드파티 앱을 차단해 두었다면 학생 로그인이 막힐 수 있습니다.
> 그 경우 학교 IT 담당자에게 이 OAuth 클라이언트의 허용을 요청하세요.

## 3. Firestore 만들고 규칙 게시

1. **Firestore Database → 데이터베이스 만들기**. 위치는 `asia-northeast3`(서울), **프로덕션 모드**로 시작합니다.
2. **규칙** 탭에 [firestore.rules](firestore.rules) 내용을 그대로 붙여넣고 **게시**합니다.
3. 규칙을 고칠 때는 이 파일을 수정하고 다시 게시하세요. 콘솔에서만 고치면 저장소와 어긋납니다.
   `sessions`·`presence`를 추가한 뒤에도 같은 방법으로 게시해야 수업 따라가기가 동작합니다.

## 4. 교사 계정 등록

콘솔 → Firestore → **컬렉션 시작** `admins` → 문서 ID를 **선생님 학교 이메일(모두 소문자)** 로 만들고
필드 `role`(문자열) = `teacher`를 넣습니다. 이 컬렉션은 규칙에서 클라이언트 쓰기를 금지하므로 콘솔에서만 관리합니다.

## 5. 명단 등록

컬렉션 `roster`, 문서 ID는 **학생 학교 이메일(모두 소문자)**, 필드는 다음과 같습니다.

| 필드 | 형식 | 예 | 필수 |
| --- | --- | --- | --- |
| `email` | 문자열 (문서 ID와 동일) | `20314@e-mirim.hs.kr` | 필수 |
| `studentId` | **문자열** | `20314` | 필수 |
| `admissionYear` | 숫자 (입학년도) | `2025` | 필수 |
| `name` | 문자열 | `홍길동` | 필수 |
| `grade` | 숫자 (현재 학년) | `2` | 필수 |
| `classroom` | 숫자 | `3` | 필수 |
| `number` | 숫자 (출석번호) | `14` | 선택 |

`studentId`(학번)는 **반드시 문자열로 저장하세요.** 숫자로 넣으면 `00314`처럼 앞자리 0이 사라집니다.

**학번만으로는 학생을 특정할 수 없습니다.** 입학년도가 다른 학생끼리 학번이 겹칠 수 있으므로,
학생을 가리키는 값은 항상 `admissionYear` + `studentId` 조합이며, 진짜 고유 식별자는 **이메일**입니다.
`grade`는 현재 학년이라 매 학년도마다 바뀌지만 `admissionYear`는 바뀌지 않으므로, 학년도 전환과 졸업 처리의 기준이 됩니다.

`number`(출석번호)는 학번에 이미 포함되어 있으면 비워도 됩니다. 비우면 학번순으로 정렬합니다.

지금은 테스트용으로 한두 명만 콘솔에서 직접 넣으세요. CSV 일괄 등록 화면은 교사 관리 페이지 단계에서 만듭니다.
`roster`에 없는 학교 계정도 로그인은 되지만 학번·학년·반이 비고 `명단에 없는 계정입니다` 안내가 표시됩니다.
학기 중 전학·추가는 콘솔이나 교사 페이지에서 한 줄만 추가하면 즉시 반영됩니다.

## 6. 확인

```bash
python tools/web/build.py
python -m http.server 8000 --directory web
```

`http://localhost:8000`에서 헤더의 **학교 계정으로 로그인**을 누릅니다. 성공하면 헤더에 `20314 홍길동`과 `2학년 3반`이 표시되고
Firestore `students/{uid}` 문서가 생깁니다. 개인 Google 계정으로 로그인하면 즉시 로그아웃되며 안내가 나옵니다.

## 데이터 구조

```
admins/{교사이메일}                   교사 권한 (콘솔에서만 관리)
roster/{학생이메일}                   교사가 등록한 반·번호 명단
students/{uid}                        학생 프로필 (반·번호는 명단과 일치해야 저장됨)
students/{uid}/state/current          학습 기록 미러 (complete/answers/journals/projects/last + times)
students/{uid}/submissions/{과제id}    제출 소스·입력·채점 결과·출력 (다음 단계)
progress/{uid}                        반별 집계용 요약 (단원 완료·문항 시도/정답·이해도 맵·updatedAt)
sessions/{학년}-{반}                   수업 세션(반당 하나). 예: sessions/2-3
presence/{uid}                        접속·따라가기 상태(90초 하트비트)
helpRequests/{요청id}                  도움 요청(학생 생성·취소, 교사 해결)
feedback/{uid}_{주제id}                어려워요 한 줄 코멘트 (progress와 분리)
```

교사가 학생용 단원 페이지에서 주제를 눌러 초점을 보낼 때도 `sessions/{학년}-{반}`을
갱신합니다. 반은 관리 화면에서 고른 값입니다. 규칙 변경은 없습니다.

`sessions`·`presence`·`helpRequests`·`feedback` 규칙은 [firestore.rules](firestore.rules)에 있습니다.
GitHub Pages 배포는 규칙 파일을 게시하지 않습니다. 규칙을 바꾼 뒤에는 콘솔
**Firestore Database → 규칙**에 파일 내용을 붙여넣고 게시하거나,
`firebase deploy --only firestore:rules` 로 배포하세요. 규칙이 아직 이전 버전이면
세션 쓰기는 거부되고, 학습 화면은 따라가기 UI 없이 기존처럼 동작합니다.

## 설정값을 공개 저장소에 커밋해도 되는가

`firebaseConfig`의 `apiKey`는 인증 자격증명이 아니라 요청을 어느 프로젝트로 보낼지 알려 주는 식별자입니다.
이 값만으로는 데이터를 읽을 수 없고, 모든 Firebase 웹 앱이 브라우저에 그대로 내려보내므로 애초에 숨길 수 있는 값이 아닙니다.
데이터를 지키는 것은 로그인(누구인지)과 `firestore.rules`(무엇을 할 수 있는지)뿐입니다. 규칙 파일도 공개를 전제로 작성합니다.

공개로 인해 실제로 생기는 위험은 데이터 접근이 아니라 남용이며, 다음과 같이 막습니다.

| 위험 | 대응 |
| --- | --- |
| 외부인이 계정을 무한정 생성 | **Google 공급자만** 사용 설정. 이메일/비밀번호·익명 로그인은 켜지 않습니다. |
| 다른 사이트가 설정값을 복사해 사용 | 승인된 도메인에 `progh2.github.io`와 `localhost`만 등록. 그 외 도메인은 `auth/unauthorized-domain`으로 실패합니다. |
| 할당량·요금 남용 | 규칙이 계정 확인부터 거부하므로 `get()`/`exists()`가 실행되지 않습니다. Spark 플랜은 한도에서 멈추고 청구되지 않습니다. Blaze로 올릴 때만 예산 알림을 설정하세요. |
| 명단·이메일 노출 | 학생은 `roster`에서 자기 한 줄만 읽고, 목록 조회는 교사만 가능합니다. 명단 CSV를 `web/`에 커밋하지 마세요. |

절대 저장소에 넣으면 안 되는 것은 **서비스 계정 키**(`*-firebase-adminsdk-*.json`)입니다.
이 키는 규칙을 무시하고 데이터베이스 전체를 읽고 지울 수 있습니다. 이 설계는 Admin SDK를 사용하지 않으므로 발급받을 일도 없습니다.
학생 개인정보가 담긴 파일도 저장소에 두지 않고 Firestore에만 둡니다.

남용을 더 막고 싶다면 **App Check**(reCAPTCHA v3, 무료 한도 있음)를 추가하는 것이 정식 방법입니다.
Google Cloud 콘솔의 API 키 HTTP 리퍼러 제한도 걸 수 있지만, 리퍼러는 위조가 가능해 보조 수단이며 잘못 설정하면 로그인이 깨집니다.

## 비용

Spark(무료) 플랜으로 학교 규모는 충분합니다. Cloud Functions를 쓰게 될 때만 Blaze가 필요합니다.
