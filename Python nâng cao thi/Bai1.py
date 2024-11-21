import math
from tkinter import *
from tkinter import messagebox

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("400x700")  # Tăng chiều cao của cửa sổ để phù hợp với giao diện mới
        
        self.expression = ""
        self.result = ""
        self.create_widgets()

    def create_widgets(self):
        # Entry widget to show the expression (above the result)
        self.expression_var = StringVar()
        self.result_var = StringVar()

        # Display the expression entered by the user
        self.expression_label = Label(self.root, textvariable=self.expression_var, font=("Arial", 18), height=2, anchor="e", bg="lightgray")
        self.expression_label.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        # Display the result after calculation
        self.result_label = Label(self.root, textvariable=self.result_var, font=("Arial", 24, "bold"), height=2, anchor="e", bg="lightgreen")
        self.result_label.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        
        # Button layout (Include all digits, operators and functions)
        button_texts = [
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("/", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("*", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("-", 4, 3),
            ("0", 5, 0), (".", 5, 1), ("=", 5, 2), ("+", 5, 3),
            ("sin(", 6, 0), ("cos(", 6, 1), ("tan(", 6, 2), ("log(", 6, 3),
            ("(", 7, 0), (")", 7, 1), ("*", 7, 2), ("C", 7, 3),
            ("Reset", 8, 0)  # Thêm nút Reset
        ]
        
        for text, row, col in button_texts:
            button = Button(self.root, text=text, font=("Arial", 18), command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky="nsew", ipadx=10, ipady=10)
        
        # Adjust grid configuration
        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == "=":
            self.evaluate_expression()
        elif char == "C":
            self.clear_expression()
        elif char == "Reset":
            self.reset_calculator()  # Reset máy tính
        else:
            self.expression += char
            self.expression_var.set(self.expression)

    def evaluate_expression(self):
        try:
            # Evaluate the expression safely
            expr = self.expression.replace("x", "*")  # Thay thế "x" bằng "*"
            
            # Evaluate the expression safely
            result = self.evaluate_complex_expression(expr)
            
            # Display the result
            self.result_var.set(result)
            self.expression = str(result)
        except Exception as e:
            self.show_error(f"Error: {e}")

    def evaluate_complex_expression(self, expr):
        # Safely evaluate the expression with proper handling of functions
        expr = expr.replace("sin", "math.sin")
        expr = expr.replace("cos", "math.cos")
        expr = expr.replace("tan", "math.tan")
        expr = expr.replace("log", "math.log10")  # Assuming log is base 10, you can modify if you need ln (base e)

        # Evaluate the expression using eval
        return eval(expr)

    def clear_expression(self):
        self.expression = ""
        self.result_var.set("")
        self.expression_var.set("")

    def reset_calculator(self):
        # Xóa toàn bộ biểu thức và kết quả
        self.expression = ""
        self.result_var.set("")
        self.expression_var.set("")

    def show_error(self, message):
        messagebox.showerror("Error", message)
        self.expression = ""
        self.result_var.set("")
        self.expression_var.set("")

# Create the main window
root = Tk()
app = CalculatorApp(root)
root.mainloop()
