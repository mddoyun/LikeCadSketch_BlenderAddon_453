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
## [0002] 2025-10-23 — chore: fix initial worklog and example formatting
- Scope: docs
- Changes: wrap example as code; correct first entry
- Problem: example heading inflated sequence and wrong date literal
- Solution: format example to avoid matching; set correct entry
- Commit: 2b8cd49

## [0003] 2025-10-23 — docs: add requests logging workflow and initial session summary
- Scope: docs, scripts
- Changes: add REQUESTS folder, pending file; post-commit rename hook; guide updates
- Problem: need to track user requests and map them to commits
- Solution: PENDING request logs auto-annotated and renamed with commit info
- Notes: create new PENDING file for new/changed requests
- Commit: 68e7c13

## [0004] 2025-10-23 — chore: finalize request log for previous commit
- Scope: docs
- Changes: rename PENDING requests file with commit hash/title via hook
- Problem: hook lacked execute permission during last commit
- Solution: set executable and re-run rename; add renamed file
- Commit: b79009e

## [0005] 2025-10-23 — 마스터 프롬프트 추가 및 지침/요청·워크로그 운영 보강
- Scope: docs, prompts, scripts, hooks
- Changes: MASTERPROMPT 추가; GUIDE 보강; REQUESTS 규칙 정비; WORKLOGS 운영 추가; 훅/스크립트 업데이트
- Problem: 재사용 가능한 초기세팅 프롬프트 필요 및 추적성/절차 일관성 부족
- Solution: MASTERPROMPT 도입, PENDING 단일화/자동화, 한글 커밋/파일명 동기화
- Notes: 푸시는 지시 시 진행
- Commit: 0792bd5

## [0006] 2025-10-23 — 워크로그 사전 초안 규칙 추가 및 중복 방지 보강
- Scope: docs, scripts
- Changes: WORKLOG 사전 초안 규칙을 MASTERPROMPT에 추가하고, WORKLOG.md 중복 기록 방지를 위해 post-commit 로직 보강
- Problem: 커밋 전 WORKLOG 초안이 반영되지 않아 훅 이후 중복/불일치 가능성
- Solution: 동일 날짜/제목 블록의 Commit 라인만 갱신하도록 개선하고 사전 초안 작성 원칙 명시
- Notes: 푸시는 보류
- Commit: 422487c

## [0007] 2025-10-23 — WORKLOG 사후 수정 금지 및 REQUESTS 파일명 순번/날짜 연계
- Scope: scripts, docs, prompts
- Changes: post-commit이 WORKLOG.md를 수정하지 않도록 조정; REQUESTS 파일명에 WORKLOG의 [순번]/날짜/제목 반영; MASTERPROMPT 업데이트
- Problem: 커밋 후 WORKLOG.md가 계속 수정 상태로 남아 혼선; 요청 파일명과 WORKLOG 간 비교 정보 부족
- Solution: 커밋 전 WORKLOG 완결, post-commit은 파일명 동기화만 수행하도록 스크립트/지침 보강
- Notes: 푸시는 보류
