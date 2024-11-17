from tkinter import messagebox, font
from update_data import update_modules  # 업데이트할 모듈 정보를 담은 데이터 가져오기

def check_for_update(update_listbox, start_update_button):
    # 업데이트할 모듈이 없는 경우
    if not update_modules:
        # 사용자에게 최신 버전임을 알리는 메시지 박스를 표시하고 함수를 종료
        messagebox.showinfo("업데이트 확인", "최신 버전입니다!")
        return
    
    # 중복을 제거한 모듈 이름 목록을 생성
    unique_modules = set(module["module"] for module in update_modules)
    
    # 각 모듈 이름에 대해
    for module in unique_modules:
        # 해당 모듈의 버전을 가져옴
        version = next(item["version"] for item in update_modules if item["module"] == module)
        # 리스트박스에 모듈 이름과 버전을 표시
        update_listbox.insert("end", f"{module} 모듈 (버전 {version})")
    
    # 업데이트 시작 버튼을 활성화하고 스타일을 변경
    start_update_button.config(state="normal", bg="#90EE90", fg="yellow", font=font.Font(weight="bold"))
    
    # 사용자에게 새로운 업데이트가 있음을 알리는 메시지 박스를 표시
    messagebox.showinfo("업데이트 확인", "새로운 업데이트가 있습니다!")