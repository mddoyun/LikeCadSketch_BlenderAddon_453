# WORKLOGS 개별 파일 운영

- 위치: `docs/WORKLOGS/`
- 진행 중 파일: `YYYY-MM-DD--after-<이전커밋제목>--PENDING.md` (커밋 직전 정확히 1개)
- 커밋 후 자동 이름 변경: `<커밋제목>.md` (커밋 제목과 동일, 한글 허용)
- 내용: 이번 커밋에서 무엇을 했는지 요약(When/Scope/Changes/Problem/Solution/Notes 등)
- `docs/WORKLOG.md`에는 post-commit 훅이 누적 요약(순번/날짜/제목=커밋제목)을 계속 추가

운영 규칙
- pre-commit 훅이 PENDING 파일이 없으면 자동 생성, 2개 이상이면 커밋을 중단합니다.
- post-commit 훅이 PENDING 파일을 커밋 제목과 동일한 이름으로 변경하고, 메타를 파일 하단에 주입합니다.
