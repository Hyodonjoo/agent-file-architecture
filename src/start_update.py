import os
from calculator_updater import run_program, replace_program, restore_backup, get_new_version_info, download_new_version, stop_program
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
                 update_ui_labels, clear_listboxes, on_update_complete_message, file_size_label, program_pid):

    serverURL = "http://52.79.222.121:3000/"    

    new_version_dir = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "dist", "Calculator/")
    print("[DEBUG] new_version_dir: ", new_version_dir)
    program_name = "Calculator.exe"

    # 다운로드 디렉토리 생성
    print("[DEBUG] 다운로드 디렉토리 생성 중")
    os.makedirs(new_version_dir, exist_ok=True)

    # 최신 버전 정보 가져오기
    version_info_url = f"{serverURL}agent-versions/lts"
    try:
        print("[DEBUG] 최신 버전 정보 가져오기 시도")
        ok, filenames, server_version = get_new_version_info(version_info_url)
        if not ok:
            raise Exception("서버에서 파일 목록을 가져오는 데 실패했습니다.")

        # 현재 버전 확인
        last_update_file_path = "../../last_update.txt"
        current_version = "unknown"
        if os.path.exists(last_update_file_path):
            with open(last_update_file_path, "r") as file:
                lines = file.readlines()
                if len(lines) >= 1:
                    current_version = lines[0].strip()
        print(f"[DEBUG] 현재 버전: {current_version}, 서버 버전: {server_version}")

        # # 서버 버전과 현재 버전을 비교
        # if current_version == server_version:
        #     update_status_label.config(text="업데이트 필요 없음: 최신 버전입니다.")
        #     add_message_to_listbox(new_text_listbox, "현재 최신 버전을 사용 중입니다.")
        #     print("[DEBUG] 서버 버전과 로컬 버전이 동일합니다. on_update_complete_message() 호출")
        #     on_update_complete_message()  # 업데이트 완료 후 처리 호출
        #     return

    except Exception as e:
        print(f"[ERROR] 최신 버전 정보 가져오기 실패: {e}")
        update_status_label.config(text="업데이트 실패: 버전 정보 가져오기 실패.")
        add_message_to_listbox(new_text_listbox, f"오류 발생: {e}")
        return

    print(f"[DEBUG] 최신 버전 정보 가져오기 성공. 파일 목록: {filenames}")

    # 리스트박스에 파일 목록 추가
    print("[DEBUG] 파일 목록 리스트박스에 추가 중")
    update_listbox.delete(0, "end")
    for file in filenames:
        update_listbox.insert("end", file)
        update_listbox.update_idletasks()
    print("[DEBUG] 파일 목록 리스트박스에 추가 완료")   

    # 파일 다운로드 및 파일 크기 계산
    total_files = len(filenames)
    print("[DEBUG] 파일 다운로드 시작")
    temp_dir = os.path.join(os.getcwd(), "temp")
    os.makedirs(temp_dir, exist_ok=True)

    for i, file in enumerate(filenames):
        print(f"[DEBUG] 파일 다운로드 중: {file}")
        file_name_label.config(text=f"현재 파일: {file}")
        file_count_label.config(text=f"파일 개수: {i + 1}/{total_files}")

        # 다운로드 URL 생성
        download_url = f"{serverURL}agent-versions/lts/download?{parse.urlencode({'filenames': file})}"

        if not download_new_version(download_url, temp_dir):
            print(f"[ERROR] 파일 다운로드 실패: {file}")
            update_status_label.config(text=f"업데이트 실패: {file} 다운로드 오류.")
            add_message_to_listbox(new_text_listbox, f"{file} 다운로드 실패")
            return

        # 파일 크기 계산
        file_path = os.path.join(temp_dir, file)
        file_size = calculate_file_size(file_path)
        file_size_label.config(text=f"파일 크기: {file_size}")
        add_message_to_listbox(new_text_listbox, f"{file} 다운로드 완료 ({file_size})")

        # 진행 상태바 갱신
        progress_bar['value'] = ((i + 1) / total_files) * 100
        progress_bar.update_idletasks()
        print(f"[DEBUG] 파일 다운로드 완료: {file} ({file_size})")    

    # 업데이트 완료
    print("[DEBUG] 모든 파일 다운로드 및 교체 완료. 업데이트 완료 처리 중")
    update_status_label.config(text="업데이트 완료")
    update_ui_labels(version_label, last_update_label)
    last_update_label.config(text=f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 최신 버전을 파일에 저장
    with open(last_update_file_path, "w") as file:
        file.write(f"{server_version}\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[DEBUG] 최신 버전 저장: {server_version}")

    clear_listboxes(update_listbox)

    # on_update_complete_message() 호출 여부 확인을 위해 콘솔 로그 추가    
    on_update_complete_message()    

    add_message_to_listbox(new_text_listbox, "모든 파일 다운로드 및 업데이트 완료")
    print("[DEBUG] 모든 업데이트 작업 완료 메시지 추가 완료")    

    # 다운로드 완료 후 프로그램 교체 및 실행
    print("[DEBUG] 모든 파일 다운로드 완료. 프로그램 교체 및 실행 시작")
    backup_dir = os.path.join(os.getcwd(), "backup")
    if not replace_program(new_version_dir, temp_dir, backup_dir):
        print("[DEBUG] 삭제 에러")
        restore_backup(backup_dir, new_version_dir)
        run_program(new_version_dir, program_name)
        return

    if not run_program(new_version_dir, program_name):
        print("[DEBUG] 실행 에러")
        restore_backup(backup_dir, new_version_dir)
        run_program(new_version_dir, program_name)
        return
    
    # 프로그램 종료
    print(f"[DEBUG] 프로그램 종료 시도: PID {program_pid}")
    if not stop_program(program_pid):
        print("[ERROR] 프로그램 종료 실패")
        update_status_label.config(text="업데이트 실패: 프로그램 종료 오류.")
        add_message_to_listbox(new_text_listbox, "프로그램 종료 실패")
        return
    print("[DEBUG] 프로그램 종료 성공")