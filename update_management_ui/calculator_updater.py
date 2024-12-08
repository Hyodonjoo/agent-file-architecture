from urllib import parse  # URL 관련 라이브러리에서 parse 기능을 가져옴
import requests  # HTTP 요청을 보내기 위한 라이브러리
import zipfile  # 압축 파일을 처리하기 위한 라이브러리
from pathlib import Path  # 파일 경로를 다루기 위한 라이브러리
import subprocess  # 시스템 명령어 실행을 위한 라이브러리
import shutil  # 파일 및 디렉토리 처리 라이브러리
import time  # 시간 관련 기능을 제공하는 라이브러리
import psutil  # 시스템 및 프로세스 모니터링 라이브러리
from urllib3.util.retry import Retry  # HTTP 요청 시 재시도 설정을 위한 라이브러리
from requests.adapters import HTTPAdapter  # HTTP 요청 시 재시도 어댑터 설정을 위한 라이브러리
import hashlib
from os import listdir, unlink
from os.path import isfile, join

# 프로그램 이름과 디렉토리 설정
program_name = "Calculator.exe"
program_dir = "dist/Calculator/"

# 디렉토리의 모든 파일을 대상 디렉토리로 이동하는 함수


def backup_contents(src_dir, dest_dir):
    src_path = Path(src_dir)  # 소스 디렉토리 경로 설정
    dest_path = Path(dest_dir)  # 대상 디렉토리 경로 설정
    if Path(dest_path).exists():  # 대상 디렉토리가 이미 있으면 삭제
        shutil.rmtree(dest_path)
    dest_path.mkdir(parents=True, exist_ok=True)  # 새 디렉토리 생성

    # 소스 디렉토리의 모든 파일을 대상 디렉토리로 복사
    for src_file in src_path.glob('*.*'):
        shutil.copy(src_file, dest_path)

# 현재 실행되어 있는 프로그램을 종료하는 함수


def stop_program(program_name):
    try:
        if program_name in (p.name() for p in psutil.process_iter()):
            # 프로세스 종료 명령 실행
            subprocess.run(
                f'taskkill /F /IM {program_name}', check=True, shell=True)
    except Exception as e:
        print(f"프로그램 종료 중 오류 발생: {e}")
        return False
    return True  # 정상적으로 종료되었으면 True 반환


def get_filenames(directory):
    filenames = [f for f in listdir(directory) if isfile(join(directory, f))]
    return filenames


def get_installed_files(directory):
    installed_files = {}

    for f in listdir(directory):
        file_path = join(directory, f)
        if isfile(file_path):
            installed_files[f] = calculate_file_hash(file_path)

    return installed_files


def calculate_file_hash(file_path):
    hash_func = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):  # 파일을 8KB 단위로 읽음
                hash_func.update(chunk)
    except FileNotFoundError:
        return None  # 파일이 없을 경우 None 반환
    return hash_func.hexdigest()

# 서버로부터 새로운 버전의 정보를 가져오는 함수


def get_new_version_info(url):
    try:
        retry = Retry(total=5, backoff_factor=1,
                      status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session = requests.Session()
        session.mount("http://", adapter)

        response = session.get(url, timeout=5)
        response.raise_for_status()

        # 콘솔창에 수신한 원본 데이터 출력
        print(f"Received raw response: {response.text}")

        response_data = response.json()

        # 콘솔창에 JSON으로 파싱된 데이터 출력
        print(f"Parsed JSON data: {response_data}")

        if response_data["ok"]:
            result = response_data["result"]
            installed_files = get_installed_files(program_dir)
            filenames = [
                fileInfo["filename"]
                for fileInfo in result["fileInfos"]
                if fileInfo["filename"] not in installed_files or
                installed_files[fileInfo["filename"]] != fileInfo["hash"]
            ]
            # 추가된 서버 버전 정보 반환
            server_version = result.get("version", "unknown")
            print(f"Parsed version data: {server_version}")
            return True, filenames, server_version
        else:
            return False, [], "unknown"
    except requests.exceptions.RequestException as e:
        print(f"새로운 버전의 정보를 가져오는 중 오류 발생: {e}")
        return False, [], "unknown"

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
    except Exception as e:
        print(f"다운로드 중 오류 발생: {e}")
        return False
    return True

# 프로그램 파일을 백업하고 교체하는 함수


def replace_program(original_dir, new_version_dir, backup_dir):
    try:
        backup_contents(original_dir, backup_dir)

        dest_path = Path(original_dir)
        if not Path(dest_path).exists():
            dest_path.mkdir(parents=True, exist_ok=True)

        src_files = get_filenames(new_version_dir)
        dest_files = get_filenames(original_dir)
        for src_file in src_files:
            if src_file in dest_files:
                unlink(join(original_dir, src_file))
            shutil.move(join(new_version_dir, src_file),
                        join(original_dir, src_file))
    except Exception as e:
        print(f"프로그램 파일 교체 중 오류 발생: {e}")
        return False
    return True

# 프로그램 실행 함수


def run_program(program_dir, program_name):
    try:
        subprocess.Popen([program_dir + program_name])
        time.sleep(3)
        if program_name not in (p.name() for p in psutil.process_iter()):
            raise Exception("프로그램 실행 오류")
    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {e}")
        return False
    return True

# 오류 발생 시 원래 파일로 복구하는 함수


def restore_backup(backup_dir, original_dir):
    try:
        backup_contents(backup_dir, original_dir)
    except Exception as e:
        print(f"백업 복구 중 오류 발생: {e}")

# 메인 업데이트 함수


def updater():
    serverURL = "http://52.79.222.121:3000/"
    new_version_dir = "new_version/"
    backup_dir = "backup/"

    if not stop_program(program_name):
        return

    version_info_url = serverURL + "agent-versions/lts"
    [ok, filenames] = get_new_version_info(version_info_url)
    if not ok:
        return

    url_query = parse.urlencode({"filenames": ",".join(filenames)})
    download_url = serverURL + "agent-versions/lts/download?" + url_query
    if not download_new_version(download_url, new_version_dir):
        run_program(program_dir, program_name)
        return

    if not replace_program(program_dir, new_version_dir, backup_dir):
        restore_backup(backup_dir, program_dir)
        run_program(program_dir, program_name)
        return

    if not run_program(program_dir, program_name):
        restore_backup(backup_dir, program_dir)
        run_program(program_dir, program_name)
        return


if __name__ == "__main__":
    updater()
