import threading
import time
import requests
from tkinter import Toplevel, Label, Text
import tkinter as tk
from datetime import datetime

# 서버 설정
SERVER_URL = "http://43.203.195.185:3000/message/fetch_new_messages"  # 서버 메시지 API
ALL_MESSAGES_URL = "http://43.203.195.185:3000/message/fetch_messages"  # 서버 모든 메시지 API
FETCH_INTERVAL = 5  # 메시지 확인 주기 (초)

# 에이전트 ID 생성 (고유 ID)
AGENT_ID = "agent_12345"  # 임의의 고유 ID를 부여 (고정된 ID)

# 메시지 수신 함수
def fetch_new_messages():
    try:        
        response = requests.get(f"{SERVER_URL}/{AGENT_ID}")
        response.raise_for_status()  # HTTP 에러가 발생하면 예외를 던짐
        messages = response.json()  # 서버에서 반환된 JSON 데이터를 파싱        
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
        return messages
    except requests.RequestException as e:
        print(f"Error fetching all messages: {e}")
        return []

# 새로운 메시지를 알리기 위한 창 생성
def show_message_popup(message_content, original_date):
    formatted_date = original_date.strftime("%Y년 %m월 %d일 %H:%M:%S")
    print(f"Showing message popup for content: {message_content}")  # 로그 추가

    # 팝업 창 생성 (Toplevel 사용)
    popup = Toplevel()
    popup.title("New Message Alert")
    popup.geometry("400x300")

    # 발송자 라벨
    sender_label = Label(popup, text="발송자: 관리자", font=('Arial', 12), anchor='w')
    sender_label.pack(fill='x', padx=10, pady=5, anchor='nw')

    # 발송 날짜 라벨
    date_label = Label(popup, text=f"발송 날짜: {formatted_date}", font=('Arial', 12), anchor='w')
    date_label.pack(fill='x', padx=10, pady=5, anchor='nw')

    # 메시지 내용 표시 Text 위젯
    message_text = Text(popup, wrap='word', font=('Arial', 12), padx=10, pady=10)
    message_text.insert(tk.END, message_content)
    message_text.config(state='disabled')  # 메시지 내용 수정 불가 설정
    message_text.pack(expand=True, fill='both')

    # 5초 후 창 닫기
    popup.after(5000, popup.destroy)

# 서버 메시지 업데이트 처리
def monitor_server_messages():
    seen_message_ids = set()  # 이미 표시한 메시지 ID를 추적
    is_first_run = True  # 첫 실행 여부를 추적

    while True:
        # 서버에서 메시지 가져오기
        messages = fetch_new_messages()

        # 첫 번째 실행일 경우, 모든 메시지를 '이미 표시한 것으로' 처리
        if is_first_run:
            for msg in messages:
                seen_message_ids.add(msg['id'])  # 모든 메시지를 이미 표시된 것으로 처리
            is_first_run = False
            print("First run: Marked all existing messages as seen.")  # 로그 추가
        else:
            # 새로운 메시지만 필터링
            new_messages = [msg for msg in messages if msg['id'] not in seen_message_ids]            

            # 새로운 메시지에 대해 알림 창 띄우기
            for msg in new_messages:
                original_date = datetime.fromisoformat(msg['date'].replace('Z', '+00:00'))
                formatted_message = f"[{original_date.strftime('%Y-%m-%d %H:%M:%S')}] {msg['message']}"
                print(f"Starting thread for popup with message: {formatted_message}")  # 로그 추가
                threading.Thread(target=show_message_popup, args=(msg['message'], original_date), daemon=True).start()
                seen_message_ids.add(msg['id'])  # 이미 표시한 메시지로 기록

        time.sleep(FETCH_INTERVAL)  # 주기적으로 확인

