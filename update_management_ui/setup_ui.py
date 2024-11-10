from tkinter import Label, Frame, Listbox, Button, ttk, font, Tk, messagebox
from calculator_updater import stop_program, get_new_version_info, download_new_version, replace_program, restore_backup, run_program
from start_update import start_update  # 업데이트 시작 함수 가져오기
from datetime import datetime  # 날짜 및 시간 관련 라이브러리

# 현재 버전 설정
current_version = "0"  # 현재 버전 번호

# 마지막 업데이트 날짜 및 시간 설정 (초기값)
last_update_datetime = "0000-00-00 00:00:00"  # 마지막 업데이트 날짜 및 시간 (초기 상태)


# 종료 확인 함수 정의
def confirm_exit(root):
    result = messagebox.askyesno("업데이트 취소 확인", "업데이트를 취소하시겠습니까?")
    if result:  # 예 버튼을 눌렀을 경우
        root.destroy()


# 업데이트 완료 후 마지막 업데이트 날짜와 시간을 갱신하는 함수
def update_last_update_time(last_update_label):
    # 현재 날짜와 시간을 "YYYY-MM-DD HH:MM:SS" 형식으로 가져오기
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_update_label.config(text=f"마지막 업데이트: {current_time}")


# 업데이트 확인 및 시작 버튼 활성화 함수 정의
def check_for_update_and_enable_button(update_listbox, start_update_button):
    version_info_url = "http://3.38.98.4:3000/agent-versions/lts"
    [ok, filenames] = get_new_version_info(version_info_url)

    if ok:
        update_listbox.insert("end", *filenames)
        messagebox.showinfo("업데이트 확인", "새로운 업데이트가 있습니다!")  # 업데이트가 있으면 메시지 표시
        start_update_button.config(state="normal")  # 업데이트 시작 버튼 활성화


# UI 구성 함수
def setup_ui(root):
    global current_version, last_update_datetime
    default_font = font.nametofont("TkDefaultFont")

    # 현재 버전을 표시하는 라벨 생성 및 배치
    version_label = Label(root, text=f"현재 버전: {current_version}")
    version_label.pack(pady=5)

    # 마지막 업데이트 날짜 및 시간을 표시하는 라벨 생성 및 배치
    last_update_label = Label(root, text=f"마지막 업데이트: {last_update_datetime}")
    last_update_label.pack(pady=5)

    # 업데이트 상태 안내 라벨 생성 및 배치
    update_status_label = Label(root, text="업데이트 확인을 눌러 최신 버전을 확인하세요.")
    update_status_label.pack(pady=10)

    # 업데이트 목록을 표시하는 리스트박스 생성 및 배치
    update_listbox = Listbox(root, width=60, height=8)
    update_listbox.pack(pady=5)

    # 파일 업데이트 진행 상태 프레임 생성 및 배치
    progress_frame = Frame(root)
    progress_frame.pack(fill="x", padx=10, pady=5)

    # 진행 상태를 나타내는 프로그레스바 생성 및 프레임에 배치
    progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=460, mode="determinate")
    progress_bar.grid(row=0, column=1, padx=10)

    # 현재 파일 이름, 파일 크기, 전송 속도, 남은 시간, 파일 개수를 표시하는 라벨 생성 및 배치
    file_name_label = Label(progress_frame, text="현재 파일: ")
    file_name_label.grid(row=1, column=0, columnspan=2, sticky="w")
    file_size_label = Label(progress_frame, text="파일 크기: - KB")
    file_size_label.grid(row=2, column=0, columnspan=2, sticky="w")
    speed_label = Label(progress_frame, text="전송 속도: - KB/s")
    speed_label.grid(row=3, column=0, columnspan=2, sticky="w")
    time_left_label = Label(progress_frame, text="남은 시간: - 초")
    time_left_label.grid(row=4, column=0, columnspan=2, sticky="w")
    file_count_label = Label(progress_frame, text="파일 개수: -/-")
    file_count_label.grid(row=5, column=0, columnspan=2, sticky="w")

    # 버튼 프레임 생성
    button_frame = Frame(root)
    button_frame.pack(pady=10)

    # 업데이트 취소 버튼 생성
    cancel_button = Button(button_frame, text="업데이트 취소", command=lambda: confirm_exit(root))
    cancel_button.grid(row=0, column=0, padx=5)

    # 업데이트 확인 버튼 생성 및 업데이트 확인 함수 연결
    check_update_button = Button(button_frame, text="업데이트 확인",
                                 command=lambda: check_for_update_and_enable_button(update_listbox,
                                                                                    start_update_button))
    check_update_button.grid(row=0, column=1, padx=5)

    # 업데이트 시작 버튼 생성 및 비활성화 상태로 초기화
    start_update_button = Button(
        root,
        text="업데이트 시작",
        state="disabled",
        command=lambda: [
            download_new_version("http://3.38.98.4:3000/agent-versions/lts/download", "new_version/"),
            replace_program("dist/", "new_version/", "backup/"),
            run_program("dist/", "Calculator.exe"),
            update_last_update_time(last_update_label),
            start_update_button.config(state="disabled")
        ]
    )
    start_update_button.pack(side="right", anchor="se", padx=10, pady=(10, 20))


# 파일이 직접 실행될 때만 특정 코드를 실행하도록 하기 위해서 if main 코드 부분을 추가
if __name__ == "__main__":
    root = Tk()
    root.title("업데이트 관리자")
    root.geometry("600x380")  # 창 크기를 설정 (너비 x 높이), 높이를 조금 낮춤
    setup_ui(root)
    root.mainloop()