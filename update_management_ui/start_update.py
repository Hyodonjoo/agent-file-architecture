import os
from calculator_updater import get_new_version_info, download_new_version, stop_program
from urllib import parse
from datetime import datetime

def calculate_file_size(file_path):
    try:
        size = os.path.getsize(file_path)
        return f"{size / 1024:.2f} KB"
    except FileNotFoundError:
        return "파일 없음"

def add_message_to_listbox(new_text_listbox, message):
    if new_text_listbox:
        formatted_message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
        new_text_listbox.insert("end", formatted_message)
        new_text_listbox.yview_moveto(1)

def start_update(update_listbox, new_text_listbox, update_status_label, progress_bar,
                 file_name_label, file_count_label, version_label, last_update_label,
                 update_ui_labels, clear_listboxes,on_update_complete_message, file_size_label):
    serverURL = "http://52.79.222.121:3000/"
    new_version_dir = os.path.join(os.getcwd(), "dist", "Calculator")
    program_name = "Calculator.exe"

    # 다운로드 디렉토리 생성
    os.makedirs(new_version_dir, exist_ok=True)

    # 프로그램 종료
    if not stop_program(program_name):
        update_status_label.config(text="업데이트 실패: 프로그램 종료 오류.")
        add_message_to_listbox(new_text_listbox, "프로그램 종료 실패")
        return

    # 최신 버전 정보 가져오기
    version_info_url = f"{serverURL}agent-versions/lts"
    try:
        ok, filenames = get_new_version_info(version_info_url)
        if not ok or not filenames:
            raise Exception("서버에서 파일 목록을 가져오는 데 실패했습니다.")
    except Exception as e:
        update_status_label.config(text="업데이트 실패: 버전 정보 가져오기 실패.")
        add_message_to_listbox(new_text_listbox, f"오류 발생: {e}")
        return

    # 리스트박스에 파일 목록 추가
    update_listbox.delete(0, "end")
    for file in filenames:
        update_listbox.insert("end", file)
        update_listbox.update_idletasks()

    # 파일 다운로드 및 파일 크기 계산
    total_files = len(filenames)
    for i, file in enumerate(filenames):
        file_name_label.config(text=f"현재 파일: {file}")
        file_count_label.config(text=f"파일 개수: {i + 1}/{total_files}")

        # 다운로드 URL 생성
        download_url = f"{serverURL}agent-versions/lts/download?{parse.urlencode({'filenames': file})}"

        if not download_new_version(download_url, new_version_dir):
            update_status_label.config(text=f"업데이트 실패: {file} 다운로드 오류.")
            add_message_to_listbox(new_text_listbox, f"{file} 다운로드 실패")
            return

        # 파일 크기 계산
        file_path = os.path.join(new_version_dir, file)
        file_size = calculate_file_size(file_path)
        file_size_label.config(text=f"파일 크기: {file_size}")
        add_message_to_listbox(new_text_listbox, f"{file} 다운로드 완료 ({file_size})")

        # 진행 상태바 갱신
        progress_bar['value'] = ((i + 1) / total_files) * 100
        progress_bar.update_idletasks()

    # 업데이트 완료
    update_status_label.config(text="업데이트 완료")
    update_ui_labels(version_label, last_update_label)
    last_update_label.config(text=f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    clear_listboxes(update_listbox)
    on_update_complete_message()
    add_message_to_listbox(new_text_listbox, "모든 파일 다운로드 완료")