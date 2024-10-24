import tkinter as tk
import add_module
import subtract_module
import multiply_module
import divide_module
import math         # 제곱근 함수 sqlt를 사용하기 위해서 math 라이브러리 함수 import
import binary_module# 이진수 모듈 추가
import mod_module   # 나머지 모듈 추가
import pow_module   # 거듭제곤 모듈 추가
import sqrt_module  # 제곱근 모듈 추가

def press_key(key):
    if key == "=":
        try:
            expression = entry.get()
            if '+' in expression:
                operands = expression.split('+')
                result = add_module.add(float(operands[0]), float(operands[1]))
            elif '-' in expression:
                operands = expression.split('-')
                result = subtract_module.subtract(float(operands[0]), float(operands[1]))
            elif '*' in expression:
                operands = expression.split('*')
                result = multiply_module.multiply(float(operands[0]), float(operands[1]))
            elif '/' in expression:
                operands = expression.split('/')
                result = divide_module.divide(float(operands[0]), float(operands[1]))
            elif '^' in expression:  # 거듭제곱 연산 추가
                operands = expression.split('^')
                result = pow_module.power(float(operands[0]), float(operands[1]))
            elif '%' in expression:  # 나머지 연산 추가
                operands = expression.split('%')
                result = mod_module.mod(float(operands[0]), float(operands[1]))
            else:
                result = "Error"
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif key == "C":
        entry.delete(0, tk.END)
    elif key == "B": # 십진수를 이진수로 변경하는 연산 추가
        try:
            num = int(float(entry.get()))
            result = binary_module.to_binary(num)
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    
    elif key == "√":  # 제곱근 연산 추가
        try:
            num = float(entry.get())
            result = sqrt_module.sqrt(num)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    else:
        entry.insert(tk.END, key)

# GUI 창 생성
root = tk.Tk()
root.title("계산기")

# 입력창 생성
entry = tk.Entry(root, width=20, font=('Arial', 18), bd=8, insertwidth=4, justify='right')
entry.grid(row=0, column=0, columnspan=4)

# 버튼 레이아웃
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', 'C', '=', '+',
    'B', '√', '%', '^',
      # 제곱근 버튼 추가
]

# 버튼 생성 및 배치
row_val = 1
col_val = 0

for button in buttons:
    tk.Button(root, text=button, padx=20, pady=20, font=('Arial', 18), command=lambda key=button: press_key(key)).grid(row=row_val, column=col_val)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# GUI 루프 실행
root.mainloop()

# add.py
def add_module(a, b):
    return a + b

# subtract.py
def subtract_module(a, b):
    return a - b

# multiply.py
def multiply_module(a, b):
    return a * b


# divide.py
def divide_module(a, b):
    if b != 0:
        return a / b
    else:
        return "Error: Division by zero"
 
# binary_module.py
def to_binary(n):  # EX) 10 B = 1010 
    return bin(n)[2:] 

# pow_module.py
def power(a, b):   # EX) 4 ^ 2 = 16
    return a ** b

# mod_module.py
def mod(a, b):     # EX) 10 % 20 = 10
    return a % b

# sqrt_module.py
def sqrt(a):      #  EX) 9 √ = 3
    if a >= 0:
        return math.sqrt(a)
    else:
        return "Error: Negative number"