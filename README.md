# :warning:  메뉴 선택? 고민 ZERO! [KIO-ZERO]

![header](https://capsule-render.vercel.app/api?type=waving&color=FFD159&height=250&text=[KIO-ZERO]%20Project&&fontAlignY=45&desc=Multi%20Campus&Desc&descAlignY=25&descAlign=22)

![kio-zero_logo](https://user-images.githubusercontent.com/76501345/120985259-68bb1b00-c7b6-11eb-857c-f506df30dfb6.png)





## :pushpin:  프로젝트 소개

모든 키오스크 이용 고객들을 위해 만든 빠른 주문 & 간편한 조작의 키오스크 !

바쁜 현대 사회에서 메뉴로 고민하는 모든 연령층과 키오스크 사용이 어려운 연령층까지 !

얼굴 인식으로 메뉴를 추천받는 One-Stop Kiosk Service 입니다.



- 기간 : 2021. 04. 27 ~ 2021. 06. 04





## :date:  ​Plan

#### 1주차 : 주제 선정 및 기획

- 프로젝트 타이틀 선정

- 팀원 간 역할 분담 및 일정 수립

- 프로젝트 수행 방향 논의

#### 2주차 : 분제 분석 및 프로젝트 설계

- `빅`  필요 데이터 정의 및 수집 · 전처리
- `AI`  인물 이미지 데이터 수집 및 라벨링
- `클`  EC2 생성 및 환경 설정
- `IoT`  PiCamera로 이미지 촬영

#### 3주차 : 기능 구현 및 Proto Type 도출

- `빅`  변수 간 상관관계 분석 및 모델링
- `AI`  이미지 분류 모델링 (성별 · 연령대 · 감정)
- `클`  HTTPS 보안 구축
- `IoT`  원격 카메라 제어 및 스트리밍 출력

#### 4주차 : 기능 병합 및 서비스 배포

- `빅 · AI`  모델링 검증 및 테스트 후, 병합
- `클`  AJAX 통신 이용하여 IoT와 연계 및 서비스 배포 · 통합
- `IoT`  AWS와 연계를 위한 서비스 구축





## :family_man_woman_girl:  ​Teammate



<p align="center" style="font-size:20px;"><b>Bigdata</b></p>

|    팀장 [박선익](https://github.com/parksimis)     |            [이다운](https://github.com/leedawoon)            |      [정민규](https://github.com/topdury)       |
| :------------------------------------------------: | :----------------------------------------------------------: | :---------------------------------------------: |
| 프로젝트 총괄<br>웹 서비스 구축<br>DB 구축 및 설계 | 전처리 및 EDA<br>데이터 크롤링<br>추천시스템 모델링<br>시연 영상 제작 | 데이터 전처리<br>설문 조사<br>추천시스템 모델링 |



<p align="center" style="font-size:20px;"><b>AI</b></p>

|           [엄정민](https://github.com/jungmin0710)           |           [이해동](https://github.com/leegongja07)           |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| 테스트 모델 제작<br>성별 모델 Fine-Tuning<br>감정 모델 Fine-Tuning<br>AI 모델 배포 파일 제작 | 훈련 데이터 탐색<br>데이터 정제 및 라벨링<br>연령 모델 Fine-Tuning |



<p align="center" style="font-size:20px;"><b>Cloud & IoT</b></p>

|           [강연옥](https://github.com/janine-kang)           |                            최현호                            |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| 프로젝트 아키텍처 설계<br>ACM으로 HTTPS 적용<br>AWS 운영 환경 구축 및 서비스 배포 | PiCamera를 이용한 이미지 송신<br>Raspberry Pi와 AWS 서버 연결<br>키오스크 제작 |





## :books:  ​Tech Stack

![GITHUB](https://img.shields.io/badge/GitHub-gray?style=plastic&logo=github)![GDRIVE](https://img.shields.io/badge/Google_Drive-gray?style=plastic&logo=google-drive)

![JUPYTER](https://img.shields.io/badge/Jupyter-v1.0.0-orange?style=plastic&logo=jupyter)![VSCODE](https://img.shields.io/badge/VSCode-v1.56.2-blue?style=plastic&logo=visual-studio-code)![COLAB](https://img.shields.io/badge/Google_Colab-gray?style=plastic&logo=google-colab)

![FLASK](https://img.shields.io/badge/Flask-v2.0.1-lightgray?style=plastic&logo=flask)![JAVASCRIPT](https://img.shields.io/badge/Javascript-ES6+-yellow?style=plastic&logo=javascript)![MYSQL](https://img.shields.io/badge/MySQL-v15.1-blue?style=plastic&logo=mysql)![MARIADB](https://img.shields.io/badge/MariaDB-v10.5.10-navy?style=plastic&logo=mariadb)





|                           Bigdata                            |                              AI                              |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| ![PYTHON](https://img.shields.io/badge/Python-v3.9-blue?style=plastic&logo=python)![R](https://img.shields.io/badge/R-v4.0.4-lightgray?style=plastic&logo=r)<br>![PANDAS](https://img.shields.io/badge/Pandas-v1.2.3-blue?style=plastic&logo=pandas)<br>![KERAS](https://img.shields.io/badge/Keras-v2.4.3-red?style=plastic&logo=keras)<br>![SKLEARN](https://img.shields.io/badge/Scikit_Learn-v0.24.1-orange?style=plastic&logo=scikit-learn)<br>![NUMPY](https://img.shields.io/badge/NumPy-v1.19.5-yellow?style=plastic&logo=numpy)<br>![MATPLOTLIB](https://img.shields.io/badge/Matplotlib-v3.3.4-lightgray?style=plastic&logo=matplotlib)<br>![SELENIUM](https://img.shields.io/badge/Selenium-v3.141.0-green?style=plastic&logo=selenium) | ![PYTHON](https://img.shields.io/badge/Python-v3.9-blue?style=plastic&logo=python)<br>![PANDAS](https://img.shields.io/badge/Pandas-v1.2.3-blue?style=plastic&logo=pandas)<br>![KERAS](https://img.shields.io/badge/Keras-v2.4.3-red?style=plastic&logo=keras)<br>![TENSORFLOW](https://img.shields.io/badge/Tensorflow-v2.5.0rc1-orange?style=plastic&logo=tensorflow)<br>![NUMPY](https://img.shields.io/badge/NumPy-v1.19.5-yellow?style=plastic&logo=numpy)<br>![PIL](https://img.shields.io/badge/PIL-v1.19.5-yellow?style=plastic)<br>![OPENCV](https://img.shields.io/badge/OpenCV-v4.5.2.52-green?style=plastic&logo=opencv) |
|                         <b>Cloud</b>                         |                          <b>IoT</b>                          |
| ![AWS](https://img.shields.io/badge/AWS-gray?style=plastic&logo=amazon-aws)<br>![DOCKER](https://img.shields.io/badge/Docker-v19.03.11-blue?style=plastic&logo=docker) | ![RASPBERRYPI](https://img.shields.io/badge/Raspberry Pi-red?style=plastic&logo=raspberry-pi)<br>![UBUNTU](https://img.shields.io/badge/ubuntu-v20.10-orange?style=plastic&logo=ubuntu) |

 



## :traffic_light:  Commit Convention

| Analysis Commit Convention                                   |
| ------------------------------------------------------------ |
| Data : 데이터 관련 사항 (데이터 수집 · 전처리 · 수정 · Cleansing)<br>EDA : 탐색적 데이터 분석 관련 사항<br>Model : 모델 생성 관련 사항<br>Valid : 모델 검증 관련 사항 |
| <b>Usual Commit Convention</b>                               |
| Feat : 새로운 기능 추가<br>Perf : 성능 개선<br>Fix : 버그 수정 · 보완<br>Refactor : 코드 리팩토링<br>Style : 코드 포맷팅, 코드 변경이 없는 경우 (스페이스, 세미콜론 누락 등)<br>Docs : 문서 추가 · 수정 · 삭제<br>Build : 빌드 시스템 · 외부 종속 라이브러리 수정<br>Test : 기존 테스트 코드 수정 및 새로운 테스트 코드 추가<br>Chore : 소스 코드, 테스트 파일을 제외한 수정 |
| <b>Example</b><br>데이터 전처리 파일 Commit 시,<br>$ git commit -m 'Data : Data Preprocessing<br>> 데이터 전처리 파일' |



