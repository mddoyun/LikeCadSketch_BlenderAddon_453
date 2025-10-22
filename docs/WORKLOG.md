# WORKLOG (작업 이력 요약)

요구사항: “작업로그 제목 = 커밋 제목(Subject)”을 유지합니다. 커밋이 생성되면 Git 훅이 아래 포맷으로 자동 기록합니다.

포맷
- 제목: `## [순번] YYYY-MM-DD — <커밋제목>`
- 본문: Scope/Changes/Problem/Solution/Notes/Commit

예시
```
## [0001] 2025-01-01 — feat: add base operator
- Scope: operators/base.py
- Changes: 신규 오퍼레이터 추가 및 등록
- Problem: 초기 등록 순서 오류
- Solution: register_class 호출 순서 조정
- Notes: 추후 단축키 매핑 필요
- Commit: abcdef1
```

## [0001] 2025-10-23 — chore: bootstrap docs and git hooks
- Scope: docs, tooling
- Changes: add GUIDE, CODEMAP, WORKLOG; git hooks; template
- Problem: need sustainable process and traceability from day 1
- Solution: add docs + post-commit worklog auto-sync
- Notes: titles between commit and worklog remain identical
- Commit: a2301db
