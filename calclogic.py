import ast 

class CalculatorLogic:   
    def __init__(self):
        self.display = ""

    def click_handler(self, char):
        if char == "=":
            self.calculate()
        elif char == "C":
            self.display = ""
        elif char == "⌫":
            self.display = self.display[:-1]
        elif char == "*":
            self.display += "×"
        elif char == "/":
            self.display += "÷"
        else:
            if self.valid_input(char):
                self.display += char

    def calculate(self):
        try:
            expression = self.display 
            
            expression = expression.replace('×', '*').replace('÷', '/')
            expression = expression.replace(',', '.')
            
            if not self.safe_calculate(expression): #if too big = error
                self.display = "Ошибка"
                return
            
            result = eval(expression)
            
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            original_str = str(result) 
            if len(original_str) > 14:
                formatted_str = "{:.8g}".format(result)
                self.display = formatted_str
            else:
                self.display = original_str
        except:
            self.display = "Ошибка"
            
    def safe_calculate(self, expr):
        try:
            tree = ast.parse(expr, mode='eval')
    
            pow_count = 0 # 
            
            for node in ast.walk(tree):
                if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow): 
                    pow_count += 1
                    
                    if isinstance(node.right, ast.BinOp) and isinstance(node.right.op, ast.Pow):
                        return False  
    
                    if isinstance(node.right, ast.Num) and node.right.n > 100:
                        return False  
                    
            if pow_count > 1:
                return False
    
            return True
        except:
            return False

    def valid_input(self, char):
        valid_chars = "0123456789+-*/().,×÷"
        return char in valid_chars

    def get_display_value(self):
        return self.display