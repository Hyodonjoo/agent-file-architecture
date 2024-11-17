# 필요한 모듈 및 함수들 가져오기
from tkinter import Label, Frame, Listbox, Button, ttk, font, Tk, messagebox 
from calculator_updater import get_new_version_info, download_new_version, replace_program, restore_backup, set_message_function
from start_update import start_update  # 업데이트 시작 함수 가져오기
from datetime import datetime  # 날짜 및 시간 관련 라이브러리
from monitor_error import detect_errors_real_time  # 에러 탐지 함수
from increment_version import increment_version  # 버전 증가 함수 가져오기
import calculator_updater # detect_errors_real_time 함수를 호출하고 calculator_updater의 모듈 내부에 있는 변수(ex program_name)를 불러들여서 실시간 에러를 탐지하고, 이를 UI에 반영하기 위해 calculator_updater 모듈 가져오기

# 초기 설정 값들: 현재 버전, 마지막 업데이트 시간
current_version = "0"
last_update_datetime = "0000-00-00 00:00:00"

# 새로운 텍스트 리스트박스를 전역 변수로 선언
new_text_listbox = None

# 메시지를 텍스트 리스트박스에 추가하는 함수
def add_message_to_listbox(message):
    if new_text_listbox:
        # 메시지에 현재 시간을 포맷팅하여 추가
        formatted_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
        new_text_listbox.insert("end", formatted_message)  # 리스트박스의 끝에 메시지 삽입
        new_text_listbox.yview_moveto(1)  # 자동 스크롤

# 종료 확인 함수 정의
def confirm_exit(root):
    # 업데이트 취소 확인 메시지 박스를 띄우고, 예시 '예'를 클릭하면 창을 닫음
    if messagebox.askyesno("업데이트 취소 확인", "업데이트를 취소하시겠습니까?"):
        root.destroy()  # 루트 창을 종료

# 마지막 업데이트 시간 갱신하는 함수
def update_last_update_time(last_update_label):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 현재 시간 구하기
    last_update_label.config(text=f"마지막 업데이트: {current_time}")  # 라벨 업데이트

# 상태 라벨 갱신 함수
def update_status_label(status_label, message):
    # 상태 라벨이 존재하면 주어진 메시지로 상태 라벨을 업데이트
    if status_label.winfo_exists():
        status_label.config(text=message)

# 업데이트 확인 및 시작 버튼 활성화 함수
def check_for_update_and_enable_button(update_listbox, start_update_button, update_status_label):
    version_info_url = "http://3.38.98.4:3000/agent-versions/lts"  # 서버 URL 설정
    result = get_new_version_info(version_info_url)  # 새로운 버전 정보 가져오기

    # 만약 버전 정보가 2개가 아닌 경우 오류 처리
    if len(result) != 2:  
        messagebox.showerror("오류", "버전 정보를 가져오는 데 문제가 발생했습니다.")
        return

    ok, filenames = result  # 반환값을 언패킹
    if ok:
        update_listbox.insert("end", *filenames)  # 업데이트 목록에 새 버전의 파일 리스트 추가
        messagebox.showinfo("업데이트 확인", "새로운 업데이트가 있습니다!")
        start_update_button.config(state="normal")  # 업데이트 시작 버튼 활성화
        update_status_label.config(text="새로운 업데이트 발생")  # 상태 라벨 변경

# UI 구성 함수
def setup_ui(root):
    global current_version, last_update_datetime, new_text_listbox
    default_font = font.nametofont("TkDefaultFont")  # 기본 폰트 설정

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

    # 새로운 텍스트 리스트 추가
    new_text_listbox = Listbox(root, width=60, height=5)
    new_text_listbox.pack(pady=5)

    # 메시지 추가 함수를 설정
    set_message_function(add_message_to_listbox)

    # 파일 업데이트 진행 상태 프레임 생성 및 배치
    progress_frame = Frame(root)
    progress_frame.pack(fill="x", padx=10, pady=5)

    # 진행 상태를 나타내는 프로그레스바 생성 및 프레임에 배치
    progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=460, mode="determinate")
    progress_bar.grid(row=0, column=1, padx=10)

    # 진행 상태 라벨들 (파일 이름, 크기, 전송 속도 등)
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
                                 command=lambda: check_for_update_and_enable_button(update_listbox, start_update_button, update_status_label))
    check_update_button.grid(row=0, column=1, padx=5)

    # 업데이트 시작 버튼 생성 및 비활성화 상태로 초기화
    start_update_button = Button(root, text="업데이트 시작", state="disabled", 
                                 command=lambda: start_update_process(update_listbox, start_update_button, update_status_label, 
                                                                       progress_bar, file_name_label, file_size_label, speed_label, 
                                                                       time_left_label, file_count_label, default_font, 
                                                                       version_label, last_update_label, root))
    start_update_button.config(state="disabled")
    start_update_button.pack(side="right", anchor="se", padx=10, pady=(10, 20))

# 리스트박스를 초기화하는 함수
def clear_update_listbox(update_listbox):
    update_listbox.delete(0, "end")

# 업데이트 프로세스를 실행하는 함수
def start_update_process(update_listbox, start_update_button, update_status_label, progress_bar, 
                         file_name_label, file_size_label, speed_label, time_left_label, 
                         file_count_label, default_font, version_label, last_update_label, root):
    error_detected = False
    try:
        clear_update_listbox(update_listbox)   # 리스트박스를 초기화
        
        start_update(update_listbox, start_update_button, update_status_label, progress_bar, 
                     file_name_label, file_size_label, speed_label, time_left_label, 
                     file_count_label, default_font, version_label)

        # 에러 탐지 함수 호출
        error_detected = detect_errors_real_time(calculator_updater.program_name, calculator_updater.program_dir, root, update_status_label)

        # 파일 개수 라벨 초기화
        file_count_label.config(text="파일 개수: 0/-")

        # 에러가 없을 경우 마지막 업데이트 시간 갱신 및 버전 증가
        if not error_detected:
            update_last_update_time(last_update_label)
            global current_version
            current_version = increment_version(current_version)
            version_label.config(text=f"현재 버전: {current_version}")
            update_status_label.config(text="탐지 완료")

    except Exception as e:
        update_status_label.config(text=f"업데이트 중 문제가 발생했습니다: {e}")

    finally:
        # 진행바 및 버튼 상태 초기화
        progress_bar.config(value=0)
        start_update_button.config(state="disabled")