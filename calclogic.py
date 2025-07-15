class CalculatorLogic:
    def __init__(self):
        self.display = ""

    def click_handler(self, char):
        if char == "=":
            self.evaluate_expression()
        elif char == "C":
            self.display = ""
        elif char == "⌫":
            self.display = self.display[:-1]
        else:
            if self.is_valid_input(char):
                self.display += char

    def evaluate_expression(self):
        try:
            expression = self.display
            result = eval(expression)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.display = str(result)
        except:
            self.display = "Ошибка"

    def is_valid_input(self, char):
        valid_chars = "0123456789+-*/().,"
        return char in valid_chars

    def get_display_value(self):
        return self.display
