# CODEMAP (전체 코드/함수 요약)

이 문서는 저장소의 ‘지도’ 역할을 하며, 파일/모듈/함수/클래스의 역할을 한눈에 파악하기 위한 요약을 제공합니다. 코드가 추가/수정될 때마다 본 문서를 갱신합니다.

업데이트 원칙
- 새로운 파일/함수가 생기면 1~2줄의 역할 요약을 추가
- 중요한 의존 관계와 경계 조건(예외 상황)을 간단히 표기
- 항목 순서는 파일 경로 기준 사전순 또는 기능 단위로 묶어 관리

초기 상태: 아직 소스 코드 골격이 없으므로 섹션만 먼저 정의합니다.

## 애드온 메타
- addon_package/__init__.py: bl_info 및 애드온 등록/해제 엔트리 포인트 (예정)

## Operators
- addon_package/operators/...: 사용자 액션을 수행하는 오퍼레이터들 (예정)

## Panels
- addon_package/ui/...: UI 패널 및 레이아웃 정의 (예정)

## Properties
- addon_package/properties.py: Scene/Object/Addon 관련 프로퍼티 정의 (예정)

## Handlers
- addon_package/handlers.py: depsgraph/update/load_post 등 핸들러 (예정)

## Utils
- addon_package/utils/...: 공용 유틸 함수(로그, 변환, 검증 등) (예정)

## Tests (옵션)
- tests/...: 단위/통합 테스트 (예정)

갱신 규칙 예시
- 파일 추가 시: 파일 경로, 핵심 책임, 주요 함수/클래스 이름을 1~2줄로 기록
- 주요 함수 추가 시: 시그니처(간단히)와 역할, 예외/전제 조건
- 리팩터 시: 변경 의도와 영향 범위를 한 줄로 요약

