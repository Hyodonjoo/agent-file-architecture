import threading
import time
import requests
from tkinter import Tk, Label

# 서버 설정
SERVER_URL = "http://3.39.238.10:3000/message/fetch_new_messages"  # 서버 메시지 API
ALL_MESSAGES_URL = "http://3.39.238.10:3000/message/fetch_messages"  # 서버 모든 메시지 API
FETCH_INTERVAL = 5  # 메시지 확인 주기 (초)

# 메시지 수신 함수
def fetch_new_messages():    
    try:
        response = requests.get(SERVER_URL)
        response.raise_for_status()  # HTTP 에러가 발생하면 예외를 던짐
        messages = response.json()  # 서버에서 반환된 JSON 데이터를 파싱
        print(f"메세지 수신확인중")
        return messages
    except requests.RequestException as e:
        print(f"Error fetching messages: {e}")
        return []
    
# 서버에 저장된 모든 메시지 목록을 가져오는 함수
def fetch_all_messages():       
    try:
        response = requests.get(ALL_MESSAGES_URL)
        response.raise_for_status()  # HTTP 에러가 발생하면 예외를 던짐
        messages = response.json()  # 서버에서 반환된 JSON 데이터를 파싱
        print(f"모든 메세지 수신확인중")
        return messages
    except requests.RequestException as e:
        print(f"Error fetching all messages: {e}")
        return []

# 새로운 메시지를 알리기 위한 창 생성
def show_message_popup(message_content):   
    popup = Tk()
    popup.title("New Message Alert")
    popup.geometry("300x150")

    # 메시지 라벨
    message_label = Label(popup, text=message_content, wraplength=250, justify="center", padx=10, pady=10)
    message_label.pack(expand=True)

    # 창 닫기 버튼
    popup.after(5000, popup.destroy)  # 5초 후 자동으로 창 닫기
    popup.mainloop()

# 서버 메시지 업데이트 처리
def monitor_server_messages():   
    seen_message_ids = set()  # 이미 표시한 메시지 ID를 추적

    while True:
        # 서버에서 메시지 가져오기
        messages = fetch_new_messages()

        # 새로운 메시지만 필터링
        new_messages = [msg for msg in messages if msg['id'] not in seen_message_ids]

        # 새로운 메시지에 대해 알림 창 띄우기
        for msg in new_messages:
            formatted_message = f"[{msg['date']}] {msg['message']}"
            threading.Thread(target=show_message_popup, args=(formatted_message,), daemon=True).start()
            seen_message_ids.add(msg['id'])  # 이미 표시한 메시지로 기록

        time.sleep(FETCH_INTERVAL)  # 주기적으로 확인
