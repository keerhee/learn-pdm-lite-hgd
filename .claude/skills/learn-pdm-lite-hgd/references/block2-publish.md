# Block 2: 공개 — GitHub Pages 주소 받기

> **Phase A 시작 시 그대로 출력한다:**
> ```
> 📖 공식 문서: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site · https://cli.github.com/manual/gh_auth_login
> ```

## EXPLAIN

### 1. 정의

| 용어 | 뜻 |
|---|---|
| GitHub 저장소 | 파일과 변경 이력을 올려 두는 GitHub의 폴더. 공개(public)면 누구나 볼 수 있다. |
| GitHub Pages | 저장소의 `index.html`을 웹 사이트로 열어 주는 GitHub 기능. 주소는 `https://내아이디.github.io/저장소이름/`. |
| 일회용 코드 | GitHub CLI(gh)로 로그인할 때 화면에 나오는 8자리 코드. 브라우저의 GitHub 화면에 내가 직접 넣는다. |

### 2. 왜 파일로 보내지 않고 주소로 공개하는가

| 기준 | 파일을 메신저로 보내기 | Pages 주소로 공개 |
|---|---|---|
| 받는 사람 | 파일을 내려받아 열어야 한다 | 휴대폰에서 링크만 누르면 열린다 |
| 고친 뒤 | 다시 보내야 한다 | 같은 주소가 새 내용으로 바뀐다 |
| 주의할 점 | 받은 사람만 본다 | **누구나 본다** — 올리기 전에 점검이 필요하다 |

### 3. 공개 전 보안 수칙

- 올릴 파일 목록을 먼저 보고, 개인정보·비밀번호·회사 내부 자료가 없는지 확인한다.
- 비밀번호나 토큰은 대화창에 입력하지 않는다. 로그인은 브라우저에서 일회용 코드로만 한다.
- 오늘 올리는 센서 값은 실습용 가상 데이터이고, 대시보드에 그 표기가 남아 있어야 한다.

## EXECUTE

아래 프롬프트를 붙여 넣으라고 안내한다.

```
~/pdm-lite 폴더를 GitHub Pages로 공개해 줘.
1. 올라갈 파일 목록을 먼저 보여 주고, 개인정보·비밀번호가 없는지 점검해 줘. 내가 "올려"라고 답하기 전에는 저장소를 만들지 마.
2. GitHub CLI(gh)가 없으면 설치해 줘. 로그인이 안 돼 있으면 일회용 코드와 접속 주소만 보여 줘. 코드는 내가 브라우저에 직접 넣을게.
3. pdm-lite 공개 저장소를 만들어 올리고 GitHub Pages(main 브랜치, 루트)를 켜 줘.
4. 배포가 끝나면 사이트 주소를 크게 보여 줘.
```

사람이 직접 하는 일(로그인이 안 되어 있을 때만):

1. 화면에 나온 접속 주소(`https://github.com/login/device`)를 브라우저에서 연다.
2. 일회용 코드 8자리를 넣고 **Continue** → **Authorize**를 누른다.
3. Code 창으로 돌아와 "로그인했어"라고 입력한다.

### 확인할 것 (Phase B)

- `gh repo view pdm-lite --json visibility,url`로 저장소가 PUBLIC으로 있는지 본다.
- `gh api repos/{owner}/pdm-lite/pages`로 Pages가 켜져 있고 주소가 `https://<아이디>.github.io/pdm-lite/`인지 본다.
- 그 주소를 열었을 때 그래프 한 장과 '실습용 가상 데이터' 표기가 보인다(배포는 1~3분 걸릴 수 있다).

막히면 아래 프롬프트를 준다.

```
Pages 주소가 404인데 원인을 찾아 줘. 3분 넘게 기다렸어.
```

## QUIZ

퀴즈 없음(실습판은 Block 1에만 1문항). 확인이 끝나면 대시보드 주소를 한 번 더 보여 주고, AskUserQuestion으로 "수업을 마칠까요, 아래 과제를 볼까요?"만 묻는다. 정답·해설은 없다.

## 과제와 다음

1. **짝에게 공유** — 대시보드 주소와 설치 한 줄(`npx skills add <내아이디>/learn-pdm-lite-<이니셜> --agent claude-code --global --yes`), 수업을 부르는 이름을 넣은 짧은 메시지를 만든다. 제출물: 메시지 3줄.
2. **내 강의 하나 더** — 다른 Day나 내 업무 주제로 `/course-forge`를 다시 돌려 learn 스킬을 하나 더 만든다. 제출물: 새 learn 스킬의 커리큘럼(`forge/curriculum.md`).
