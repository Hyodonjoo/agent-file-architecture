import os
import time
import threading
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Text
from datetime import datetime

from fetch_message import monitor_server_messages, fetch_all_messages
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

last_update_file_path = "../../last_update.txt"

if os.path.exists(last_update_file_path):
    with open(last_update_file_path, "r") as file:
        lines = file.readlines()
        CURRENT_VERSION = lines[0].strip() if lines else "0"
else:
    CURRENT_VERSION = "0"

LATEST_VERSION = "unknown"
CHANGED_FILES = []
try:
    server_url = "http://52.79.222.121:3000/agent-versions/lts"
    ok, changed_files, server_version = get_new_version_info(server_url)
    if ok:
        LATEST_VERSION = server_version        
    else:
        print("[ERROR] 서버에서 최신 버전 정보를 가져오지 못했습니다.")
except Exception as e:
    print(f"[ERROR] 최신 버전 정보를 가져오는 중 오류 발생: {e}")

FETCH_INTERVAL = 5
is_manual_check = False

def check_for_updates_async(root):
    global is_manual_check
    if os.path.exists(last_update_file_path):
        with open(last_update_file_path, "r") as file:
            lines = file.readlines()
            CURRENT_VERSION = lines[0].strip() if lines else "0"
    else:
        CURRENT_VERSION = "0"
        
    def update_process():
        global is_manual_check
        if CURRENT_VERSION == LATEST_VERSION:
            if is_manual_check:
                messagebox.showinfo("업데이트 확인", "현재 최신 버전입니다.")
            is_manual_check = False
            return

        response = messagebox.askyesno("업데이트 필요", "새로운 업데이트가 있습니다. 업데이트를 진행하시겠습니까?")
        if response:
            root.after(0, lambda: call_update_ui_main(root))
        is_manual_check = False

    threading.Thread(target=update_process, daemon=True).start()

def manual_check_for_updates(root):
    global is_manual_check
    is_manual_check = True
    check_for_updates_async(root)

def call_update_ui_main(root):
    try:
        import update_ui_main
        update_ui_main.main()
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
        messages_label.grid_remove()
        messages.grid_remove()
        update_button.grid_remove()
        toggle_button.set_text("▶")
    else:
        messages_label.grid()
        messages.grid()
        update_button.grid()
        toggle_button.set_text("◀")
    message_panel_visible = not message_panel_visible

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width=80, height=40, corner_radius=15, bg="#B0E0E6", fg="black", font=('Arial',14),
                 text="", command=None):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bg=parent['bg'])
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.bg_color = bg
        self.fg = fg
        self.font = font
        self.text = text
        self.command = command
        
        self.border_color = "#A0C0D0"
        self.border_width = 2

        self.text_id = None

        self.draw_button()
        self.bind("<Button-1>", self.on_click)

    def draw_button(self):
        self.delete("all")
        w = self.width
        h = self.height
        r = self.corner_radius
        bw = self.border_width

        self.create_arc((0, 0, 2*r, 2*r), start=90, extent=90, fill=self.bg_color, outline="", width=0)
        self.create_arc((w-2*r, 0, w, 2*r), start=0, extent=90, fill=self.bg_color, outline="", width=0)
        self.create_arc((w-2*r, h-2*r, w, h), start=270, extent=90, fill=self.bg_color, outline="", width=0)
        self.create_arc((0, h-2*r, 2*r, h), start=180, extent=90, fill=self.bg_color, outline="", width=0)

        self.create_rectangle((r, 0, w-r, h), fill=self.bg_color, outline="", width=0)
        self.create_rectangle((0, r, w, h-r), fill=self.bg_color, outline="", width=0)

       
        self.text_id = self.create_text(w/2, h/2, text=self.text, fill=self.fg, font=self.font)

        self.create_arc((0, 0, 2*r, 2*r), start=90, extent=90, style='arc', outline=self.border_color, width=bw)
        self.create_arc((w-2*r, 0, w, 2*r), start=0, extent=90, style='arc', outline=self.border_color, width=bw)
        self.create_arc((w-2*r, h-2*r, w, h), start=270, extent=90, style='arc', outline=self.border_color, width=bw)
        self.create_arc((0, h-2*r, 2*r, h), start=180, extent=90, style='arc', outline=self.border_color, width=bw)
       
        self.create_line(r, 0, w-r, 0, fill=self.border_color, width=bw)
        self.create_line(w-r, h, r, h, fill=self.border_color, width=bw)      
        self.create_line(0, r, 0, h-r, fill=self.border_color, width=bw)     
        self.create_line(w, r, w, h-r, fill=self.border_color, width=bw)

    def on_click(self, event):
        if self.command:
            self.command()

    def set_text(self, new_text):
        self.text = new_text
        self.draw_button()

root = tk.Tk()
root.title("계산기")

root.config(bg="#ADD8E6")

root.resizable(width=False, height=False)

# 필수 파일 체크 로직
required_files = ["add_module.py", "subtract_module.py", "multiply_module.py", "divide_module.py"]
missing_files = [f for f in required_files if not os.path.exists(os.path.join(os.getcwd(), f))]

if missing_files:
    messagebox.showwarning("필수 파일 누락", "필수 파일이 없어서 복구를 진행합니다.")
    call_update_ui_main(root)
    

entry = tk.Entry(root, width=20, font=('Arial', 18), bd=1, insertwidth=4, justify='right', bg="#E0FFFF", fg="black", relief="sunken")
entry.grid(row=0, column=0, columnspan=4, pady=5, padx=5)

buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', 'C', '=', '+'
]

row_val = 1
col_val = 0

def make_press_func(k):
    return lambda: press_key(k)

for button in buttons:
    rb = RoundedButton(root, width=60, height=50, corner_radius=15, bg="#B0E0E6", fg="black",
                       font=('Arial',18), text=button, command=make_press_func(button))
    rb.grid(row=row_val, column=col_val, padx=5, pady=5)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

message_panel_visible = True

toggle_button = RoundedButton(root, width=40, height=200, corner_radius=15, bg="#B0E0E6", fg="black",
                              font=('Arial',14), text="◀", command=toggle_message_panel)
toggle_button.grid(row=1, column=4, rowspan=5, padx=5, sticky='ns')

messages_label = Label(root, text="관리자 메시지", font=('Arial', 14), pady=5, bg="#ADD8E6")
messages_label.grid(row=0, column=5, padx=10, pady=5)

messages = tk.Listbox(root, width=20, height=15, font=('Arial', 12), bg="#E0FFFF")
messages.grid(row=1, column=5, rowspan=5, padx=10, pady=10)
messages.bind("<Double-1>", on_message_click)

update_button = RoundedButton(root, width=100, height=50, corner_radius=15, bg="#B0E0E6", fg="black",
                              font=('Arial',14), text="업데이트", command=lambda: manual_check_for_updates(root))
update_button.grid(row=6, column=5, pady=10)

threading.Thread(target=monitor_server_messages, daemon=True).start()
all_messages_cache = []
update_messages()
threading.Thread(target=periodic_update_messages, daemon=True).start()
check_for_updates_async(root)

root.mainloop()
