import threading
import os
import psutil
from tkinter import Label, Frame, Listbox, ttk, Tk, messagebox
from calculator_updater import get_new_version_info, stop_program
from datetime import datetime

# 파일 경로 설정
last_update_file_path = "last_update.txt"

# 파일에 마지막 업데이트 정보를 저장하는 함수
def save_last_update_info(version, update_time):
    global last_update_datetime, current_version
    current_version = version
    last_update_datetime = update_time
    with open(last_update_file_path, "w") as file:
        file.write(f"{current_version}\n{last_update_datetime}")
    print(f"[INFO] 파일에 마지막 업데이트 정보를 저장했습니다: 버전={current_version}, 시간={last_update_datetime}")

# UI 라벨을 업데이트하는 함수
def update_ui_labels(version_label, last_update_label):
    global current_version, last_update_datetime
    try:
        last_update_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        version_label.config(text=f"현재 버전: {current_version}")
        last_update_label.config(text=f"마지막 업데이트: {last_update_datetime}")
        print(f"[INFO] 버전이 업데이트되었습니다. 현재 버전: {current_version}, 마지막 업데이트: {last_update_datetime}")
    except Exception as e:
        print(f"[ERROR] 버전 업데이트 중 오류 발생: {e}")
        version_label.config(text="현재 버전: 오류 발생")
        last_update_label.config(text=f"마지막 업데이트: {last_update_datetime}")

# Listbox를 비우는 함수
def clear_listboxes(*listboxes):
    for listbox in listboxes:
        listbox.delete(0, "end")
    print("[INFO] Listbox가 모두 비워졌습니다.")

# UI를 설정하는 함수
def setup_ui(root, on_update_finished):
    global current_version, last_update_datetime

    # 마지막 업데이트 정보를 파일에서 불러옴
    if os.path.exists(last_update_file_path):
        with open(last_update_file_path, "r") as file:
            lines = file.readlines()
            if len(lines) >= 2:
                current_version = lines[0].strip()
                last_update_datetime = lines[1].strip()
            print(f"[INFO] 파일에서 마지막 업데이트 정보를 불러왔습니다: 버전={current_version}, 시간={last_update_datetime}")
    else:
        print("[INFO] 마지막 업데이트 파일을 찾을 수 없습니다. 기본값을 사용합니다.")

    version_label = Label(root, text=f"현재 버전: {current_version}")
    version_label.pack(pady=5)

    last_update_label = Label(root, text=f"마지막 업데이트: {last_update_datetime}")
    last_update_label.pack(pady=5)

    update_status_label = Label(root, text="업데이트를 확인 중입니다...")
    update_status_label.pack(pady=10)

    update_listbox = Listbox(root, width=60, height=8)
    update_listbox.pack(pady=5)

    new_text_listbox = Listbox(root, width=60, height=5)
    new_text_listbox.pack(pady=5)

    progress_frame = Frame(root)
    progress_frame.pack(fill="x", padx=10, pady=5)

    progress_bar = ttk.Progressbar(
        progress_frame, orient="horizontal", length=460, mode="determinate")
    progress_bar.grid(row=0, column=0, padx=10)

    file_name_label = Label(progress_frame, text="현재 파일: ")
    file_name_label.grid(row=1, column=0, sticky="w")
    file_count_label = Label(progress_frame, text="파일 개수: -/-")
    file_count_label.grid(row=2, column=0, sticky="w")
    file_size_label = Label(progress_frame, text="파일 크기: ")
    file_size_label.grid(row=3, column=0, sticky="w")

    def on_update_complete_message():
        """
        업데이트 완료 후 메시지를 표시하고, UI 상태를 유지.
        """
        def show_complete_message():
            print("[INFO] 업데이트가 완료되었습니다. 사용자에게 알림을 띄웁니다.")
            update_status_label.config(text="업데이트 완료!")  # 상태 업데이트

            # 업데이트 완료 후 메인 윈도우 창 종료 콜백 호출
            print("[INFO] 업데이트가 완료되었으므로 메인 창 종료 콜백을 호출합니다.")
            root.after(100, on_update_finished)

        root.after(0, show_complete_message)

    def start_update_thread():
        """
        업데이트를 스레드에서 실행하며, UI와 충돌을 방지.
        """
        def update_task():
            try:
                print("[INFO] 업데이트 작업이 시작됩니다.")

                # 최신 버전 정보 가져오기
                server_url = "http://52.79.222.121:3000/agent-versions/lts"
                ok, filenames, server_version = get_new_version_info(server_url)

                if not ok:
                    raise Exception("최신 버전 정보를 가져오는 데 실패했습니다.")
                
                program_pid = next((p.pid for p in psutil.process_iter(['name']) if p.info['name'] == "Calculator.exe"), None)                        

                # 업데이트 작업 수행
                import start_update
                start_update.start_update(
                    update_listbox, new_text_listbox, update_status_label, progress_bar,
                    file_name_label, file_count_label, version_label, last_update_label,
                    update_ui_labels, clear_listboxes, on_update_complete_message, file_size_label, program_pid
                )

                # 업데이트 정보 저장
                update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                save_last_update_info(server_version, update_time)
                print(f"[INFO] 서버 버전: {server_version}, 업데이트 시간: {update_time}")
                
                print("[INFO] 업데이트 작업이 성공적으로 완료되었습니다.")                

            except Exception as e:
                root.after(0, lambda: messagebox.showerror(
                    "오류", f"업데이트 실패: {e}"))
                print(f"[ERROR] 업데이트 작업 중 오류 발생: {e}")

        threading.Thread(target=update_task, daemon=True).start()
        print("[INFO] 업데이트 스레드가 시작되었습니다.")

    root.after(100, start_update_thread)
    print("[INFO] 업데이트 스레드가 시작될 예정입니다.")
