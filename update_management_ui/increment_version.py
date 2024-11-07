# 버전 증가 함수
def increment_version(version):
    # 문자열로 된 버전 번호를 정수로 변환
    version_number = int(version)
    # 버전 번호를 1 증가시키고 문자열로 변환하여 반환
    return str(version_number + 1)