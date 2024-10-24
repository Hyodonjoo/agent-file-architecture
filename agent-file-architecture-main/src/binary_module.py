def to_binary(n): #    정수 n을 2진수 문자열로 변환
    return bin(n)[2:]  # bin() 함수는 접두사로 '0b'를 붙이므로 [2:]로 제거