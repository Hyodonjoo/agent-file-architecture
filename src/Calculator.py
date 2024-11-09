import tkinter as tk

import add_module
import subtract_module
import multiply_module
import divide_module

# import add_module # exe 변환시 add로 변경
# import subtract_module # exe 변환시 subtract로 변경
# import multiply_module # exe 변환시 multiply로 변경
# import divide_module # exe 변환시 divide로 변경

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
            else:
                result = "Error"
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif key == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, key)

# 창 생성
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
    '0', 'C', '=', '+'
]

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