# 자동 업데이트 및 오류 복구 시스템 에이전트 
아래 링크에 있는 서버 코드와 통신
<br>[자동 업데이트 및 오류 복구 시스템 서버 코드](https://github.com/Hyodonjoo/version-management-server.git)

업데이트를 위한 기본적인 계산기를 에이전트 대상으로 설정

## 개발 기간
- 2024.10 ~ 2024.12

## 역할
| 이름 | 담당 역할 및 기능 |
| ------ |  ------ |
| 주효돈 | PM, 계산기 UI, 메세지 수신, 자동 업데이트, 오류 탐지 구현 |
| 노유신 | 오류 복구 API, 업데이트 수신 API 구현 |
| 박용수 | 업데이터 UI 구성 |

## 기술 스택
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

## 실행
1. 업데이트 전 계산기
<br>![계산기](https://github.com/user-attachments/assets/9e93cc19-e93d-420c-a456-4f4115d797e7)

2. 업데이트 진행 UI
<br> ![업데이트 진행](https://github.com/user-attachments/assets/b2be1ef9-2120-4ce4-8bcd-551e715a8818)

3. 업데이트 완료 후 계산기
<br> 메세지 수신 시 아래와 같은 창이 뜨고 5초뒤 종료
<br> ![계산기ver2](https://github.com/user-attachments/assets/9edfb558-d7d7-4f08-a127-c230f2575567)

## 실행 방법

<details> 
  <summary><b>exe 파일 생성방법</b></summary>
 
Calculator.py가 저장되어있는 폴더(src폴더)로 이동하여
<br/>`pyinstaller --onefile Calculator.py`
<br/>또는
<br/>`pyinstaller --noconsole Calculator.py`
<br/>를 입력하면 해당 폴더 내에 dist 폴더가 생성됨.
<br/> 1번째 방법으로는 exe파일 자체는 어디에 옮기더라도 정상적으로 작동이 가능해야함
<br/> 2번쨰 방법으로는 Calculator.exe가 위치한 폴더에 \_internal이 있어야 실행이 가능.
<br/>만약 파일에 엑세스 할 수 없다고 나올경우, 관리자 권한으로 실행 (외부로부터 받은 exe 파일이라 윈도우에서 권한을 막은것)

</details>

<details> 
  <summary><b>updater 실행 방법</b></summary>

### 사전 조건

1. 서버가 실행되어 있어야 합니다.
2. Calculator.exe의 실행파일 위치는 `dist/Calculator/Calculator.exe`에 있어야 합니다.
3. 아래 명령어 모두 프로젝트의 가장 상위 디렉토리에서 실행해야 합니다. (src 폴더 바깥)

### 개발 중에 실행하기
1. `py update_ui_main.py ` 명령어 실행해서 UI 창 뜨면, `업데이트 확인` 버튼 누른 후 `업데이트 시작` 버튼 누름

- 그럼 업데이터가 탐지한 에러 내용들을 UI 텍스트 리스트 박스에 표시함.
- 그 다음에 UI 상태 라벨은 "에러 탐지 완료" 라는 문구가 뜸.

### 실행 파일 생성하기

1. `pyinstaller --onefile --distpath updater src/updater.py` 명령어로 Calculator.exe와 다른 폴더에 updater.exe 실행파일 생성
2. updater.exe를 실행

</details>

<details> 
  <summary><b>자동 업데이트 실행방법</b></summary>
 
Calculator.py에 있는 call_update_ui_main(root):에 절대 경로를 확인하는 script_path에 update_management_ui/update_ui_main.py가 있는 경로를 넣어서 경로중 \를 /로 바꾸고 Calculator.py가 저장되어있는 폴더(src폴더)로 이동하여 `pyinstaller --onefile Calculator.py `
 dist 폴더가 생성되고 Calculator.exe 실행

</details>
