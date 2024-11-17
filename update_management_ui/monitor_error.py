import calculator_updater # calculator_updater 모듈 내부에 있는 에러 탐지 함수(ex stop_program)들을 사용하기 위해 calculator_updater import함
import setup_ui #  에러 메시지를 텍스트 리스트 박스에 추가하여 실시간으로 UI에 표시할 수 있도록 하기 위해 setup_ui import함

# 에러 탐지 및 실시간 모니터링 함수
def detect_errors_real_time(program_name, program_dir, root, status_label):
    error_messages = []  # 에러 메시지를 저장할 리스트 초기화

    try:
        # 프로그램 종료 에러 탐지
        if not calculator_updater.stop_program(program_name):
            error_messages.append("프로그램 종료에 실패했습니다.")

        # 프로그램 실행 에러 탐지
        if not calculator_updater.run_program(program_dir, program_name):
            error_messages.append("프로그램 실행 중 오류가 감지되었습니다.")

        # 파일 다운로드 중 에러 탐지
        if not calculator_updater.download_new_version(program_dir, "dest_dir"):
            error_messages.append("파일 다운로드 오류가 발생했습니다.")

        # 파일 교체 중 에러 탐지
        if not calculator_updater.replace_program("original_dir", "new_version_dir", "backup_dir"):
            error_messages.append("파일 교체 중 오류가 발생했습니다.")

        # 백업 복구 중 에러 탐지
        if not calculator_updater.restore_backup("backup_dir", "original_dir"):
            error_messages.append("백업 복구 중 오류가 발생했습니다.")

    except Exception as e:
        error_messages.append(f"에러 탐지 중 문제가 발생했습니다: {e}")

    # 에러가 발생하면 에러 메시지를 UI에 표시
    if error_messages:
        if status_label.winfo_exists():
            status_label.config(text="에러 탐지 완료")  # 에러 탐지가 완료되었음을 상태 라벨에 표시
            root.update()  # UI 업데이트
        
        # 에러 메시지를 리스트박스에 각 줄마다 추가
        for message in error_messages:
            setup_ui.add_message_to_listbox(message)  # 에러 메시지를 텍스트 리스트박스에 추가

    return bool(error_messages)  # 에러 발생 여부 반환