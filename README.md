# agent-file-architecture
JBNU 2024-2 캡스톤

# exe 파일 생성방법
Calculator.py가 저장되어있는 폴더(src폴더)로 이동하여 
<br/>``` pyinstaller --noconsole Calculator.py ```
<br/>를 입력하면 해당 폴더 내에 dist 폴더가 생성됨.
dist 폴더내의 Calculator.exe를 실행시키면 계산기 프로그램 실행이 가능.
<br/>(exe파일 자체는 어디에 옮기더라도 정상적으로 작동이 가능해야함)
