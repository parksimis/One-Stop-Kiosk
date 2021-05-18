# One-Stop 메뉴 추천 서비스

* 멀티캠퍼스 융복합 프로젝트 1조



##  커밋 컨벤션

```bash
################## Analysis Commit Convention ##################
Data : 데이터 관련 사항(데이터 수집, 전처리, 수정, cleansing)
EDA : 탐색적 데이터 분석 관련 사항
Model : 모델 생성 관련 사항
Valid : 모델 검증 관련 사항

################## Usual Commit Convention ##################
Feat     : 새로운 기능 추가
Perf     : 성능 개선
Fix      : 버그 수정, 보완
Refactor : 코드 리팩토링
Style    : 코드 포맷팅, 코드 변경이 없는 경우 (스페이스, 세미콜론 누락 등)
Docs     : 문서 추가, 수정, 삭제
Build    : 빌드 시스템 수정, 외부 종속 라이브러리 수정
Test     : 기존 테스트 코드 수정 및 새로운 테스트 코드 추가
Chore    : 소스코드, 테스트 파일을 제외한 수정

Ex. 데이터 전처리 파일 commit 시
$ git commit -m 'Data: Data preprocessing
> 데이터 전처리 파일 commit'
```

