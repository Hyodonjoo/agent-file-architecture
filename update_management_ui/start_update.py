from tkinter import messagebox
from update_data import update_modules  # 업데이트할 모듈 정보 가져오기
from increment_version import increment_version  # 버전 증가 함수 가져오기

def start_update(update_listbox, start_update_button, update_status_label, progress_bar, 
                 file_name_label, file_size_label, speed_label, time_left_label, file_count_label, default_font, version_label):
    # 업데이트할 총 파일 수를 계산하고 이를 표시하는 라벨을 초기화
    total_files = len(update_modules)
    file_count_label.config(text=f"파일 개수: 0/{total_files}")
    
    # 각 모듈을 순회하며 업데이트를 진행
    for i, module in enumerate(update_modules, start=1):
        # 현재 진행 중인 파일 개수를 업데이트하여 표시
        file_count_label.config(text=f"파일 개수: {i}/{total_files}")
        
        # 진행 상태바(Progress Bar) 업데이트
        progress_bar['value'] = (i / total_files) * 100
        
        # UI 업데이트 (idletasks로 즉시 반영)
        file_name_label.update_idletasks()

    # 업데이트 완료 후 메시지 박스 표시
    messagebox.showinfo("업데이트 완료", "업데이트가 완료되었습니다!")
    
    # 시작 버튼 스타일을 초기화하여 비활성화 상태로 복원
    start_update_button.config(bg="SystemButtonFace", fg="black", font=default_font)
    
    # 파일 개수 라벨과 진행 상태바를 초기화
    file_count_label.config(text="파일 개수: -/-")
    progress_bar['value'] = 0

    # 업데이트된 모듈 중 가장 높은 버전을 가져와 최신 버전으로 설정
    latest_version = max(module["version"] for module in update_modules)
    version_label.config(text=f"현재 버전: {latest_version}")

    # 각 모듈의 버전을 하나씩 증가시키고 업데이트
    for module in update_modules:
        module["version"] = increment_version(latest_version)
    
    # 업데이트 리스트박스를 초기화하여 완료된 항목을 제거
    update_listbox.delete(0, "end")