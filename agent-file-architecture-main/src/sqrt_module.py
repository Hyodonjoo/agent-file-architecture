import math # 제곱근 함수 sqlt를 사용하기 위해서 math 라이브러리 함수 impor

def sqrt(a):
    if a >= 0:
        return math.sqrt(a)
    else:
        return "Error: Negative number"