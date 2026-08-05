import customtkinter as ctk
import math

app = ctk.CTk()
app.geometry("320x440")
app.title("CALCU")
app.resizable(False, False)
ctk.set_appearance_mode("dark")

display = ctk.CTkLabel(app, text="0", font=("Arial", 36), width=300, height=60)
display.pack(pady=20, padx=20)

frame_buttons = ctk.CTkFrame(app)
frame_buttons.pack(pady=10, padx=10)

def press_number(num):
    current = display.cget("text")
    if current == "Error" or current == "Infinity" or current == "NaN":
        display.configure(text=str(num))
        return
    
    # جلوگیری از چند نقطه پشت سر هم
    if num == ".":
        # پیدا کردن آخرین عدد در عبارت
        parts = current.split()
        if parts and "." in parts[-1]:
            return
        # اگر آخرین کاراکتر نقطه نباشه
        if current and current[-1].isdigit():
            display.configure(text=current + ".")
        elif current and current[-1] in "+-*/^":
            display.configure(text=current + "0.")
        else:
            display.configure(text="0.")
        return
    
    if current == "0":
        display.configure(text=str(num))
    else:
        display.configure(text=current + str(num))

def press_operator(op):
    current = display.cget("text")
    if current in ["Error", "Infinity", "NaN"]:
        display.configure(text="0")
        return
        
    # جلوگیری از عملگرهای پشت سر هم
    if current and current[-1] in "+-*/^.":
        # جایگزینی عملگر قبلی با جدید
        display.configure(text=current[:-1] + op)
    else:
        display.configure(text=current + op)

def calculate():
    try:
        expr = display.cget("text")
        if expr in ["Error", "Infinity", "NaN", ""]:
            display.configure(text="0")
            return
            
        # بررسی کاراکترهای مجاز
        allowed = "0123456789+-*/().^ "
        if not all(c in allowed for c in expr):
            display.configure(text="Error")
            return
            
        # بررسی پرانتزها
        if expr.count("(") != expr.count(")"):
            display.configure(text="Error")
            return
            
        expr = expr.replace("^", "**")
        result = eval(expr)
        
        # بررسی بی‌نهایت
        if not math.isfinite(result):
            display.configure(text="Infinity")
            return
            
        # نمایش نتیجه
        if isinstance(result, float):
            if result == int(result):
                display.configure(text=str(int(result)))
            else:
                # محدود کردن اعشار به 10 رقم
                display.configure(text=f"{result:.10g}")
        else:
            display.configure(text=str(result))
            
    except ZeroDivisionError:
        display.configure(text="Cannot divide by zero")
    except SyntaxError:
        display.configure(text="Error")
    except Exception:
        display.configure(text="Error")

def clear():
    display.configure(text="0")

def backspace():
    current = display.cget("text")
    if current in ["Error", "Infinity", "NaN", "Cannot divide by zero"]:
        display.configure(text="0")
        return
        
    if len(current) > 1:
        display.configure(text=current[:-1])
        if display.cget("text") == "":
            display.configure(text="0")
    else:
        display.configure(text="0")

def key_press(event):
    key = event.char
    if key.isdigit():
        press_number(key)
    elif key == ".":
        press_number(".")
    elif key in "+-*/^":
        press_operator(key)
    elif key == "\r":  # Enter
        calculate()
    elif key == "\b":  # Backspace
        backspace()
    elif key.lower() == "c":
        clear()
    elif key == "=":
        calculate()

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
        button = ctk.CTkButton(frame_buttons, text=text, width=140, height=60, command=calculate)
        button.grid(row=row, column=col, columnspan=colspan, padx=3, pady=3)
        continue
    
    text, row, col = btn
    
    if text.isdigit():
        cmd = lambda x=text: press_number(x)
    elif text == ".":
        cmd = lambda: press_number(".")
    elif text == "=":
        cmd = calculate
    elif text == "C":
        cmd = clear
    elif text == "⌫":
        cmd = backspace
    else:  # عملگرها
        cmd = lambda x=text: press_operator(x)
    
    button = ctk.CTkButton(frame_buttons, text=text, width=60, height=60, command=cmd)
    button.grid(row=row, column=col, padx=3, pady=3)

# اتصال کیبورد
app.bind("<Key>", key_press)

app.mainloop()
