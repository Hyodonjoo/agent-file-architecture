# agent-file-architecture

JBNU 2024-2 캡스톤

# exe 파일 생성방법

Calculator.py가 저장되어있는 폴더(src폴더)로 이동하여
<br/>`pyinstaller --onefile Calculator.py `
<br/>또는
<br/>`pyinstaller --noconsole Calculator.py`
<br/>를 입력하면 해당 폴더 내에 dist 폴더가 생성됨.
<br/> 1번째 방법으로는 exe파일 자체는 어디에 옮기더라도 정상적으로 작동이 가능해야함
<br/> 2번쨰 방법으로는 Calculator.exe가 위치한 폴더에 \_internal이 있어야 실행이 가능.

---

만약 파일에 엑세스 할 수 없다고 나올경우, 관리자 권한으로 실행 (외부로부터 받은 exe 파일이라 윈도우에서 권한을 막은것)

# updater 실행 방법

## 사전 조건

1. 서버가 실행되어 있어야 합니다. (기본 localhost:3000로 설정되어 있음)
2. Calculator.exe의 실행파일 위치 `dist/`를 변경했다면 updater.exe에서 해당 경로로 수정해야 합니다.
3. 아래 명령어 모두 프로젝트의 가장 상위 디렉토리에서 실행해야 합니다. (src 폴더 바깥)

## 개발 중에 실행하기

2. Calculator.exe가 실행되어 있는 상태에서 `python .\src\updater.py` 명령어 실행

## 실행 파일 생성하기

1. `pyinstaller --onefile --distpath updater src/updater.py` 명령어로 Calculator.exe와 다른 폴더에 updater.exe 실행파일 생성
2. Calculator.exe가 실행되어 있는 상태에서 updater.exe를 실행
