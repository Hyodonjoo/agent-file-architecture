import threading
from tkinter import Label, Frame, Listbox, ttk, Tk, messagebox
from increment_version import increment_version
from datetime import datetime

# 초기값 설정
current_version = "0"
last_update_datetime = "0000-00-00 00:00:00"

def update_ui_labels(version_label, last_update_label):
    global current_version, last_update_datetime
    try:
        current_version = increment_version(current_version)
        last_update_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        version_label.config(text=f"현재 버전: {current_version}")
        last_update_label.config(text=f"마지막 업데이트: {last_update_datetime}")
    except Exception as e:
        print(f"버전 업데이트 중 오류 발생: {e}")
        version_label.config(text="현재 버전: 오류 발생")
        last_update_label.config(text=f"마지막 업데이트: {last_update_datetime}")

def clear_listboxes(*listboxes):
    for listbox in listboxes:
        listbox.delete(0, "end")

def setup_ui(root):
    global current_version, last_update_datetime

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

    progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=460, mode="determinate")
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
            messagebox.showinfo("업데이트 완료", "업데이트가 성공적으로 완료되었습니다!")
            update_status_label.config(text="업데이트 완료!")  # 상태 업데이트
            root.deiconify()  # 창을 다시 표시

        root.after(0, show_complete_message)

    def start_update_thread():
        """
        업데이트를 스레드에서 실행하며, UI와 충돌을 방지.
        """
        def update_task():
            try:
                import start_update
                start_update.start_update(
                    update_listbox, new_text_listbox, update_status_label, progress_bar,
                    file_name_label, file_count_label, version_label, last_update_label,
                    update_ui_labels, clear_listboxes, on_update_complete_message, file_size_label
                )
            except Exception as e:
                root.after(0, lambda: messagebox.showerror("오류", f"업데이트 실패: {e}"))

        threading.Thread(target=update_task, daemon=True).start()

    root.after(100, start_update_thread)

if __name__ == "__main__":
    root = Tk()
    root.title("업데이트 시스템")
    root.geometry("600x450")
    setup_ui(root)
    root.mainloop()