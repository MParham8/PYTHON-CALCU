import customtkinter as ctk
import math

app = ctk.CTk()
app.geometry("320x400")
app.title("CALCU")
ctk.set_appearance_mode("dark")

display = ctk.CTkLabel(app, text="0", font=("Arial", 36), width=300, height=60)
display.pack(pady=20, padx=20)

frame_buttons = ctk.CTkFrame(app)
frame_buttons.pack(pady=10, padx=10)

def press_number(num):
    current = display.cget("text")
    if current == "0" or current == "Error":
        display.configure(text=str(num))
    else:
        display.configure(text=current + str(num))

def press_operator(op):
    current = display.cget("text")
    if current and current[-1] not in "+-*/^.":
        display.configure(text=current + op)

def calculate():
    try:
        expr = display.cget("text")
        allowed = "0123456789+-*/().^ "
        if not all(c in allowed for c in expr):
            display.configure(text="Error")
            return
        expr = expr.replace("^", "**")
        result = eval(expr)
        if isinstance(result, float) and result != int(result):
            display.configure(text=f"{result:.10g}")
        else:
            display.configure(text=str(int(result) if result == int(result) else result))
    except:
        display.configure(text="Error")

def clear():
    display.configure(text="0")

def backspace():
    current = display.cget("text")
    if len(current) > 1 and current != "Error":
        display.configure(text=current[:-1])
    else:
        display.configure(text="0")

# دکمه‌ها با چیدمان بهتر
buttons = [
    ("7",0,0), ("8",0,1), ("9",0,2), ("/",0,3),
    ("4",1,0), ("5",1,1), ("6",1,2), ("*",1,3),
    ("1",2,0), ("2",2,1), ("3",2,2), ("-",2,3),
    ("0",3,0), (".",3,1), ("^",3,2), ("+",3,3),
    ("C",4,0), ("⌫",4,1), ("=",4,2,2)  # دکمه = بزرگ‌تر
]

for btn in buttons:
    if len(btn) == 4:  # برای دکمه‌های با عرض بیشتر
        text, row, col, colspan = btn
        cmd = calculate
        button = ctk.CTkButton(frame_buttons, text=text, width=140, height=60, command=cmd)
        button.grid(row=row, column=col, columnspan=colspan, padx=3, pady=3)
        continue
    
    text, row, col = btn
    
    if text.isdigit() or text == ".":
        cmd = lambda x=text: press_number(x)
    elif text == "=":
        cmd = calculate
    elif text == "C":
        cmd = clear
    elif text == "⌫":
        cmd = backspace
    else:
        cmd = lambda x=text: press_operator(x)
    
    button = ctk.CTkButton(frame_buttons, text=text, width=60, height=60, command=cmd)
    button.grid(row=row, column=col, padx=3, pady=3)

app.bind("<Key>", lambda e: key_press(e) if hasattr(e, 'char') else None)
app.mainloop()
