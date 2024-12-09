import os
import time
from tkinter import messagebox
import tkinter as tk
import subprocess
import threading

from tkinter import Toplevel, Label, Text
from datetime import datetime
from fetch_message import monitor_server_messages, fetch_all_messages  # 서버 메시지 함수 임포트
import add_module
import subtract_module
import multiply_module
import divide_module
from calculator_updater import get_new_version_info

WEEKDAY_MAP = {
    'Monday': '월',
    'Tuesday': '화',
    'Wednesday': '수',
    'Thursday': '목',
    'Friday': '금',
    'Saturday': '토',
    'Sunday': '일'
}

# 현재 버전과 최신 버전 비교
last_update_file_path = "../../last_update.txt"

# 현재 버전 불러오기
if os.path.exists(last_update_file_path):
    with open(last_update_file_path, "r") as file:
        lines = file.readlines()
        CURRENT_VERSION = lines[0].strip() if lines else "0"
else:
    CURRENT_VERSION = "0"

# 최신 버전 정보 가져오기
LATEST_VERSION = "unknown"
try:
    server_url = "http://52.79.222.121:3000/agent-versions/lts"
    ok, _, server_version = get_new_version_info(server_url)
    if ok:
        LATEST_VERSION = server_version
    else:
        print("[ERROR] 서버에서 최신 버전 정보를 가져오지 못했습니다.")
except Exception as e:
    print(f"[ERROR] 최신 버전 정보를 가져오는 중 오류 발생: {e}")

FETCH_INTERVAL = 5  # 메시지 확인 주기 (초)
is_manual_check = False

def check_for_updates_async(root):
    global is_manual_check  # 전역 변수를 사용한다고 명시
    # 현재 버전 불러오기
    if os.path.exists(last_update_file_path):
        with open(last_update_file_path, "r") as file:
            lines = file.readlines()
            CURRENT_VERSION = lines[0].strip() if lines else "0"
    else:
        CURRENT_VERSION = "0"

    def update_process():
        global is_manual_check  # 전역 변수를 사용한다고 명시
        if CURRENT_VERSION == LATEST_VERSION:
            if is_manual_check:
                messagebox.showinfo("업데이트 확인", "현재 최신 버전입니다.")
            is_manual_check = False  # 확인 후 플래그 초기화
            return

        # 새 버전이 있을 때만 업데이트 확인 메시지 표시
        response = messagebox.askyesno("업데이트 필요", "새로운 업데이트가 있습니다. 업데이트를 진행하시겠습니까?")
        if response:
            root.after(0, lambda: call_update_ui_main(root))
        is_manual_check = False  # 확인 후 플래그 초기화

    threading.Thread(target=update_process, daemon=True).start()

def manual_check_for_updates(root):
    global is_manual_check
    is_manual_check = True  # 버튼 클릭으로 수동 확인을 수행하도록 플래그 설정
    check_for_updates_async(root)

def call_update_ui_main(root):
    try:
        import update_ui_main  # 모듈로 import
        update_ui_main.main()  # main 함수 호출
        messagebox.showinfo("업데이트 완료", "업데이트가 성공적으로 완료되었습니다.")
    except ModuleNotFoundError:
        messagebox.showerror("업데이트 오류", "update_ui_main 모듈을 찾을 수 없습니다.")
    except Exception as e:
        messagebox.showerror("업데이트 오류", f"업데이트 실행 중 오류가 발생했습니다: {e}")

def press_key(key):
    if key == "=":
        try:
            expression = entry.get()
            if '+' in expression:
                operands = expression.split('+')
                result = add_module.add(float(operands[0]), float(operands[1]))
            elif '-' in expression:
                operands = expression.split('-')
                result = subtract_module.subtract(float(operands[0]), float(operands[1]))
            elif '*' in expression:
                operands = expression.split('*')
                result = multiply_module.multiply(float(operands[0]), float(operands[1]))
            elif '/' in expression:
                operands = expression.split('/')
                result = divide_module.divide(float(operands[0]), float(operands[1]))
            else:
                result = "Error"
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif key == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, key)

def update_messages():
    global all_messages_cache
    all_messages_cache = fetch_all_messages()  
    messages.delete(0, tk.END)  
    if all_messages_cache:
        for msg in reversed(all_messages_cache):             
            original_date = datetime.fromisoformat(msg['date'].replace('Z', '+00:00'))
            formatted_date = original_date.strftime("%m-%d %H:%M:%S")           
            messages.insert(tk.END, f"[{formatted_date}]")
            messages.insert(tk.END, f"{msg['message']}")
            messages.insert(tk.END, "")             
    else:
        print("No messages fetched from the server.")

def periodic_update_messages():
    while True:
        update_messages()
        time.sleep(FETCH_INTERVAL)

def on_message_click(event):
    selection = messages.curselection()
    if selection:
        index = selection[0]        
        if index % 3 == 1:  
            msg = all_messages_cache[len(all_messages_cache) - 1 - (index // 3)] 
            original_date = datetime.fromisoformat(msg['date'].replace('Z', '+00:00'))
            weekday = WEEKDAY_MAP[original_date.strftime("%A")]
            detailed_date = original_date.strftime(f"%Y년 %m월 %d일 ({weekday})  %H:%M:%S")
            
            detail_window = Toplevel(root)
            detail_window.title("상세 메시지")
            detail_window.geometry("400x300")

            sender_label = Label(detail_window, text="발송자: 관리자", font=('Arial', 12), anchor='w')
            sender_label.pack(fill='x', padx=10, pady=5, anchor='nw')

            date_label = Label(detail_window, text=f"발송 날짜: {detailed_date}", font=('Arial', 12), anchor='w')
            date_label.pack(fill='x', padx=10, pady=5, anchor='nw')

            message_text = Text(detail_window, wrap='word', font=('Arial', 12), padx=10, pady=10)
            message_text.insert(tk.END, msg['message'])
            message_text.config(state='disabled')  
            message_text.pack(expand=True, fill='both')

def toggle_message_panel():
    global message_panel_visible
    if message_panel_visible:
        # 메시지 창 숨기기
        messages_label.grid_remove()
        messages.grid_remove()
        update_button.grid_remove()
        toggle_button.config(text="▶")
    else:
        # 메시지 창 보이기
        messages_label.grid()
        messages.grid()
        update_button.grid()
        toggle_button.config(text="◀")
    message_panel_visible = not message_panel_visible

# 창 생성
root = tk.Tk()
root.title("계산기")

# 창 크기 고정
root.resizable(width=False, height=False)

# 입력창 생성
entry = tk.Entry(root, width=20, font=('Arial', 18), bd=8, insertwidth=4, justify='right')
entry.grid(row=0, column=0, columnspan=4)

# 버튼 레이아웃
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', 'C', '=', '+'
]

row_val = 1
col_val = 0

for button in buttons:
    tk.Button(root, text=button, padx=20, pady=20, font=('Arial', 18), command=lambda key=button: press_key(key)).grid(row=row_val, column=col_val)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# 메시지 창 토글 버튼 추가 (계산기와 메시지 목록 창 사이에 위치)
message_panel_visible = True  # 메시지 창이 보이는지 여부를 추적하는 플래그
toggle_button = tk.Button(root, text="◀", font=('Arial', 14), command=toggle_message_panel, height=15)  # 버튼 높이 조정
toggle_button.grid(row=1, column=4, rowspan=5, padx=5, sticky='ns')  # 계산기와 메시지 목록 창 사이에 위치

# 관리자 메시지 라벨 생성
messages_label = Label(root, text="관리자 메시지", font=('Arial', 14), pady=5)
messages_label.grid(row=0, column=5, padx=10, pady=5)

# 메시지 표시 창 생성 (우측에 배치)
messages = tk.Listbox(root, width=20, height=15, font=('Arial', 12))
messages.grid(row=1, column=5, rowspan=5, padx=10, pady=10)
messages.bind("<Double-1>", on_message_click)

# 업데이트 버튼 생성 (메시지 창 아래에 배치)
update_button = tk.Button(root, text="업데이트 실행", padx=20, pady=10, font=('Arial', 14), command=lambda: manual_check_for_updates(root))
update_button.grid(row=6, column=5, pady=10)

# 서버 메시지 모니터링 쓰레드 시작
threading.Thread(target=monitor_server_messages, daemon=True).start()

# 메시지 캐시 초기화
all_messages_cache = []

# 프로그램 실행 시 초기 메시지 목록 불러오기
update_messages()

# 프로그램 실행 시 주기적인 메시지 업데이트 쓰레드 시작
threading.Thread(target=periodic_update_messages, daemon=True).start()

# 프로그램 실행 시 업데이트 확인
check_for_updates_async(root)

# GUI 루프 실행
root.mainloop()
