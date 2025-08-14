import tkinter as tk
from tkinter import font
from calclogic import CalculatorLogic

class ModernCalculator:
    def __init__(self, master):
        self.master = master
        self.logic = CalculatorLogic()
        master.title("Калькулятор")
        master.configure(bg='#f0f0f0')
        master.resizable(False, False)
        
        self.display_font = font.Font(family='Helvetica', size=24, weight='bold')
        self.button_font = font.Font(family='Helvetica', size=12)
        self.operator_font = font.Font(family='Helvetica', size=12, weight='bold')
        
        self.display = tk.Entry(master, font=self.display_font, 
                               bg='#ffffff', fg='#333333', bd=0, 
                               justify='right', insertwidth=1, width=14)
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=(15, 10), ipady=10, sticky='ew')
        
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
        
        row, col = 1, 0
        for (text, bg_color, fg_color) in buttons:
            btn_font = self.operator_font if text in {'/', '*', '-', '+', '=', 'C', '⌫'} else self.button_font
            
            action = lambda x=text: self.button_click(x)
            btn = tk.Button(master, text=text, bg=bg_color, fg=fg_color, 
                           font=btn_font, **button_style, command=action)
            
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.lighten_color(b.cget('bg'))))
            btn.bind("<Leave>", lambda e, b=btn, c=bg_color: b.configure(bg=c))
            
            btn.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
            col += 1
            if col > 3:
                col = 0
                row += 1

        for i in range(4):
            master.columnconfigure(i, weight=1)
        for i in range(1, 6):
            master.rowconfigure(i, weight=1)

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

    def button_click(self, char):
        self.logic.click_handler(char)
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.logic.get_display_value())

if __name__ == '__main__':
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()