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

1. 서버가 실행되어 있어야 합니다.
2. Calculator.exe의 실행파일 위치는 `dist/Calculator/Calculator.exe`에 있어야 합니다.
3. 아래 명령어 모두 프로젝트의 가장 상위 디렉토리에서 실행해야 합니다. (src 폴더 바깥)

## 개발 중에 실행하기
1. `py update_ui_main.py ` 명령어 실행해서 UI 창 뜨면, `업데이트 확인` 버튼 누른 후 `업데이트 시작` 버튼 누름

- 그럼 업데이터가 탐지한 에러 내용들을 UI 텍스트 리스트 박스에 표시함.
- 그 다음에 UI 상태 라벨은 "에러 탐지 완료" 라는 문구가 뜸.

## 실행 파일 생성하기

1. `pyinstaller --onefile --distpath updater src/updater.py` 명령어로 Calculator.exe와 다른 폴더에 updater.exe 실행파일 생성
2. updater.exe를 실행


## 자동 업데이트 실행방법
Calculator.py에 있는 call_update_ui_main(root):에 절대 경로를 확인하는 script_path에 update_management_ui/update_ui_main.py가 있는 경로를 넣어서 경로중 \를 /로 바꾸고 Calculator.py가 저장되어있는 폴더(src폴더)로 이동하여 `pyinstaller --onefile Calculator.py `
 dist 폴더가 생성되고 Calculator.exe 실행

