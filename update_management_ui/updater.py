from urllib import parse
import requests
import zipfile
from pathlib import Path
import subprocess
import shutil
import time
import psutil


def move_dir_contents(src_dir, dest_dir):
    src_path = Path(src_dir)
    dest_path = Path(dest_dir)
    if Path(dest_path).exists():
        shutil.rmtree(dest_path)
    dest_path.mkdir(parents=True, exist_ok=True)

    for src_file in src_path.glob('*.*'):
        shutil.copy(src_file, dest_path)
    shutil.rmtree(src_path)


# 현재 실행되어 있는 프로그램을 종료하는 함수
def stop_program(program_name):
    try:
        # 프로그램 종료 (윈도우에서는 'taskkill' 명령 사용)
        subprocess.run(
            f'taskkill /F /IM {program_name}', check=True, shell=True)
        print(f"{program_name} 종료 완료.")
    except Exception as e:
        print(f"프로그램 종료 중 오류 발생: {e}")
        return False

    return True


# 서버로부터 새로운 버전의 정보를 가져오는 함수
def get_new_version_info(url):
    try:
        response: dict = requests.get(url).json()
        if response["ok"]:
            result = response["result"]
            print("최신 버전: " + result["version"])

            filenames = []
            for fileInfo in result["fileInfos"]:
                filenames.append(fileInfo["filename"])

            return [True, filenames]
        else:
            return [False]
    except Exception as e:
        print(f"새로운 버전의 정보를 가져오는 중 오류 발생: {e}")
        return [False]


# 서버로부터 새로운 버전의 프로그램을 다운로드하는 함수
def download_new_version(url, dest_dir):
    try:
        response = requests.get(url, stream=True)
        with open("new_version.zip", 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        with zipfile.ZipFile("new_version.zip", 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
        Path("new_version.zip").unlink()

        print("새 버전 다운로드 완료.")
    except Exception as e:
        print(f"다운로드 중 오류 발생: {e}")
        return False

    return True


# 프로그램 파일을 백업하고 교체하는 함수
def replace_program(original_dir, new_version_dir, backup_dir):
    try:
        # 원래 프로그램 백업
        move_dir_contents(original_dir, backup_dir)
        # 새 버전으로 교체
        move_dir_contents(new_version_dir, original_dir)
        print("프로그램 파일 교체 완료.")
    except Exception as e:
        print(f"프로그램 파일 교체 중 오류 발생: {e}")
        return False

    return True


# 프로그램 실행 함수
def run_program(program_dir, program_name):
    try:
        subprocess.Popen([program_dir + program_name])
        print(f"{program_name} 실행 중...")
        time.sleep(3)  # 프로그램 실행 대기

        if program_name not in (p.name() for p in psutil.process_iter()):
            raise Exception("프로그램 실행 오류")

    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {e}")
        return False

    return True


# 오류 발생 시 원래 파일로 복구하는 함수
def restore_backup(backup_dir, original_dir):
    try:
        move_dir_contents(backup_dir, original_dir)
        print("백업 파일로 복구 완료.")
    except Exception as e:
        print(f"백업 복구 중 오류 발생: {e}")


def updater():
    serverURL = "http://localhost:3000/"
    program_name = "Calculator.exe"
    program_dir = "dist/"
    new_version_dir = "new_version/"
    backup_dir = "backup/"

    # 프로그램 종료
    if not stop_program(program_name):
        return

    # 새로운 버전 정보 서버로부터 가져옴
    version_info_url = serverURL + "agent-versions/lts"
    [ok, filenames] = get_new_version_info(version_info_url)
    if not ok:
        return

    # 새로운 버전 다운로드
    url_query = parse.urlencode({"filenames": ",".join(filenames)})
    download_url = serverURL + "agent-versions/lts/download?" + url_query
    if (not download_new_version(download_url, new_version_dir)):
        run_program(program_dir, program_name)
        return

    # 프로그램 백업 및 교체
    if not replace_program(program_dir, new_version_dir, backup_dir):
        restore_backup(backup_dir, program_dir)
        run_program(program_dir, program_name)
        return

    # 프로그램 실행
    if not run_program(program_dir, program_name):
        restore_backup(backup_dir, program_dir)
        run_program(program_dir, program_name)
        return


if __name__ == "__main__":
    updater()
