from tkinter import Tk  # Tkinter 라이브러리에서 Tk 클래스를 가져옴 (GUI 창 생성에 사용)
from setup_ui import setup_ui  # UI 설정 함수 가져오기

def main():
    # Tk 객체를 생성하여 애플리케이션의 메인 윈도우 창을 만듦
    root = Tk()
    
    # 창의 제목을 설정
    root.title("계산기 업데이트 관리")
    
    # 창의 크기를 가로 500, 세로 600으로 설정
    root.geometry("500x600")
    
    # 창 크기 조절을 비활성화 (사용자가 창 크기를 변경하지 못하도록 설정)
    root.resizable(False, False)
    
    # UI 설정 함수 호출 (root 창을 기반으로 UI 구성)
    setup_ui(root)
    
    # 이벤트 루프를 시작하여 창이 닫힐 때까지 프로그램이 실행됨
    root.mainloop()
    return 0  # 정상 종료를 명시적으로 반환

# 메인 프로그램 실행 조건
if __name__ == "__main__":
    exit(main())  # 종료 상태를 반환하도록 설정