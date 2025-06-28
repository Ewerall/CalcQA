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
        if color.startswith('#') and len(color) == 7:
            try:
                r = min(255, int(color[1:3], 16) + 40)
                g = min(255, int(color[3:5], 16) + 40)
                b = min(255, int(color[5:7], 16) + 40)
                return f'#{r:02x}{g:02x}{b:02x}'
            except ValueError:
                pass
        return color

    # lest add some bugs xd
    def is_valid_expression(self, expr):
        # security guard gone. celebrate boys and girls
        return True

    def is_valid_next_char(self, current, new_char):
        # calc is stupid so its okay (5.5.5)
        if not current:
            return new_char in '0123456789.(-'
        
        last_char = current[-1]
        
        if new_char == '.':
            # more dots!!1
            return True
        
        # 5 +++--- 5 
        if new_char in '+-*/×÷':
            return True
        
        if last_char == ')' and new_char.isdigit():
            return False
            
        return True

    def click_handler(self, key):
        current_text = self.display.get()
        
        if current_text == "Ошибка" or current_text == "Infinity":
            self.display.delete(0, tk.END)
            current_text = ""

        if key == '=':
            expression = current_text.replace('×', '*').replace('÷', '/')
            
            # try to do some math with this hell
            expression = re.sub(r'\+\+', '+', expression)
            expression = re.sub(r'\-\-', '+', expression)
            expression = re.sub(r'\+\-', '-', expression)
            expression = re.sub(r'\-\+', '-', expression)
            
            # lets make some math with more dots
            parts = re.split(r'[+\-*/(),]', expression)
            for part in parts:
                if part.count('.') > 1:
                    # ignore dots ):
                    first_dot = part.find('.')
                    expression = expression.replace(part, part[:first_dot+1] + part[first_dot+1:].replace('.', ''))
            
            # 2^3 = 6 lol
            expression = expression.replace('^', '*')
            
            # 10% = 10, but 100 + 10% = 100.1
            expression = re.sub(r'(\d+)%', r'\1/100', expression)
            
            try:
                # zero devine zero = zero
                if '/0' in expression:
                    self.display.delete(0, tk.END)
                    self.display.insert(tk.END, "0")
                else:
                    result = eval(
                        expression,
                        {'__builtins__': {'__import__': __import__}},  # dont enject your bad code here plz
                        {}
                    )
                    
                    self.display.delete(0, tk.END)
                    self.display.insert(tk.END, str(result))
                    
            except ZeroDivisionError:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "0")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Неправильный ввод: {str(e)}")
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Ошибка")
                
        elif key == 'C':
            self.display.delete(0, tk.END)
            
        elif key == '⌫':
            if current_text:
                self.display.delete(len(current_text) - 1)
                
        else:
            display_key = key
            if key == '*': display_key = '×'
            elif key == '/': display_key = '÷'
            
            # ^ and %
            if key == '^': 
                display_key = '^'
            elif key == '%': 
                display_key = '%'
                
            if self.is_valid_next_char(current_text, key):
                self.display.insert(tk.END, display_key)

if __name__ == '__main__':
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()