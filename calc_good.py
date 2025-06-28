import tkinter as tk
from tkinter import font, messagebox
import sys
import os
import re

class ModernCalculator:
    def __init__(self, master):
        self.master = master
        master.title("Калькулятор")
        master.configure(bg='#f0f0f0')
        master.resizable(False, False)
        
        # set icon
        self.set_calculator_icon(master)
        
        # fonts
        self.display_font = font.Font(family='Helvetica', size=24, weight='bold')
        self.button_font = font.Font(family='Helvetica', size=12)
        self.operator_font = font.Font(family='Helvetica', size=12, weight='bold')
        
        # input
        self.display = tk.Entry(master, font=self.display_font, 
                               bg='#ffffff', fg='#333333', bd=0, 
                               justify='right', insertwidth=1, width=14)
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=(15, 10), ipady=10, sticky='ew')
        
        # button styles
        button_style = {
            'bd': 0, 
            'relief': 'flat',
            'height': 2,
            'width': 5,
            'cursor': 'hand2'
        }
        
        buttons = [
            ('C', '#f44336', 'white'), ('⌫', '#607d8b', 'white'), ('(', '#9e9e9e', 'white'), (')', '#9e9e9e', 'white'),
            ('7', '#e0e0e0', '#212121'), ('8', '#e0e0e0', '#212121'), ('9', '#e0e0e0', '#212121'), ('/', '#ff9800', 'white'),
            ('4', '#e0e0e0', '#212121'), ('5', '#e0e0e0', '#212121'), ('6', '#e0e0e0', '#212121'), ('*', '#ff9800', 'white'),
            ('1', '#e0e0e0', '#212121'), ('2', '#e0e0e0', '#212121'), ('3', '#e0e0e0', '#212121'), ('-', '#ff9800', 'white'),
            ('0', '#e0e0e0', '#212121'), ('.', '#e0e0e0', '#212121'), ('=', '#4caf50', 'white'), ('+', '#ff9800', 'white')
        ]
        
        # buttons
        row, col = 1, 0
        for (text, bg_color, fg_color) in buttons:
            btn_font = self.operator_font if text in {'/', '*', '-', '+', '=', 'C', '⌫'} else self.button_font
            
            action = lambda x=text: self.click_handler(x)
            btn = tk.Button(master, text=text, bg=bg_color, fg=fg_color, 
                           font=btn_font, **button_style, command=action)
            
            # whoosh effect
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.lighten_color(b.cget('bg'))))
            btn.bind("<Leave>", lambda e, b=btn, c=bg_color: b.configure(bg=c))
            
            btn.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
            col += 1
            if col > 3:
                col = 0
                row += 1

        # weight column
        for i in range(4):
            master.columnconfigure(i, weight=1)
        for i in range(1, 6):
            master.rowconfigure(i, weight=1)

    # idk wth this dont work correct so todo
    def set_calculator_icon(self, window):
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            icon_path = os.path.join(base_path, "calculator.ico")
            if os.path.exists(icon_path):
                window.iconbitmap(icon_path)
        except Exception as e:
            print("Icon error:", e)
            pass

    def lighten_color(self, color):
        # when you hover over the button, it becomes brighter.
        if color.startswith('#') and len(color) == 7:
            try:
                r = min(255, int(color[1:3], 16) + 40)
                g = min(255, int(color[3:5], 16) + 40)
                b = min(255, int(color[5:7], 16) + 40)
                return f'#{r:02x}{g:02x}{b:02x}'
            except ValueError:
                pass
        return color

    def is_valid_expression(self, expr):
        # check if user sus and try do sus things with eval
        if not re.match(r'^[\d+\-*/().\s×÷]+$', expr):
            return False
        
        parts = re.split(r'[+\-*/(),÷×]', expr)
        for part in parts:
            if part.count('.') > 1:
                return False
        
        if re.search(r'[+\-*/×÷]{2,}', expr):
            return False
            
        return True

    def is_valid_next_char(self, current, new_char):
        # check if user stupi and try 5.5.5 + 5 or something else
        if not current:
            return new_char in '0123456789.(-'
        
        last_char = current[-1]
        
        if new_char == '.':
            start_index = 0
            for i in range(len(current)-1, -1, -1):
                if current[i] in '+-*/(),÷×':
                    start_index = i+1
                    break
            current_number = current[start_index:]
            return '.' not in current_number
        
        if new_char in '+-*/×÷':
            if new_char == '-' and last_char in '+-*/(,÷×':
                return True
            return last_char not in '+-*/×÷'
        
        if last_char == ')' and new_char.isdigit():
            return False
            
        return True

    def click_handler(self, key):
        current_text = self.display.get()
        
        # delete 'error' 
        if current_text == "Ошибка":
            self.display.delete(0, tk.END)
            current_text = ""

        if key == '=':
            # change symb
            expression = current_text.replace('×', '*').replace('÷', '/')
            
            # security guard
            if not self.is_valid_expression(expression):
                messagebox.showerror("Ошибка", "Недопустимое выражение")
                return
                
            try:
                # very security guard!
                result = eval(
                    expression,
                    {'__builtins__': None},  # not on my watch
                    {}
                )
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except ZeroDivisionError:
                messagebox.showerror("Ошибка", "Деление на ноль невозможно")
                self.display.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Ошибка", "Неправильный ввод")
                self.display.delete(0, tk.END)
                
        elif key == 'C':
            self.display.delete(0, tk.END)
            
        elif key == '⌫':
            if current_text:
                self.display.delete(len(current_text) - 1)
                
        else:
            # todo
            display_key = key
            if key == '*': display_key = '×'
            elif key == '/': display_key = '÷'
            
            # small security guard
            if self.is_valid_next_char(current_text, key):
                self.display.insert(tk.END, display_key)

if __name__ == '__main__':
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()