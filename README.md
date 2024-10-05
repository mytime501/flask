# Who 미라클모닝 프로젝트

## 개요
이 프로젝트는 MongoDB를 사용하는 `Who 미라클모닝` 애플리케이션으로, 사용자에게 미라클모닝 루틴을 관리하고 최적화하는 기능을 제공합니다. 사용자 인터페이스를 통해 데이터의 추가, 조회 및 관리가 가능하며, Python과 Flask 프레임워크를 기반으로 구현되었습니다.

## 주요 기능
- 사용자가 자신의 미라클모닝 루틴을 추가하고 관리할 수 있는 기능
- MongoDB를 사용한 데이터 저장 및 관리
- 사용자 인터페이스를 통한 간편한 데이터 조회

## 기술 스택
- **프레임워크**: Flask
- **언어**: Python
- **데이터베이스**: MongoDB
- **패키지 관리**: pip, Pipenv, Poetry

## 설치 및 실행 방법
1. 레포지토리를 클론합니다:
    ```bash
    git clone https://github.com/mytime501/who-miraclemorning
    ```
2. 프로젝트 디렉토리로 이동합니다:
    ```bash
    cd who-miraclemorning
    ```
3. 필요한 패키지를 설치합니다 (Pipenv 또는 Poetry 사용):
    ```bash
    pipenv install
    # 또는
    poetry install
    ```
4. MongoDB 데이터베이스에 연결합니다.
5. 서버를 실행합니다:
    ```bash
    python app.py
    ```

## 데이터베이스
MongoDB를 사용하여 미라클모닝 루틴 데이터를 저장하며, Mongoose를 통해 데이터 모델을 정의하고 관리합니다.

## 기여 방법
기여를 원하시면 이슈를 등록하거나 풀 리퀘스트를 보내주세요. 주요 변경 사항을 논의하려면 먼저 이슈를 생성하는 것이 좋습니다.

## 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다.
