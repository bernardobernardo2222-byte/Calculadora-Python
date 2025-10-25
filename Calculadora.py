#Calculadora Python
import tkinter as tk
from tkinter import ttk, font
import ast
import operator as op

# --- Avaliador seguro de expressões (sem eval direto) ---
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

def safe_eval(expr: str):
    """Avalia expressão aritmética de forma segura."""
    try:
        node = ast.parse(expr, mode='eval').body
        return _eval_node(node)
    except Exception as e:
        raise ValueError("Expressão inválida") from e

def _eval_node(node):
    if isinstance(node, ast.Num):
        return node.n
    if hasattr(ast, "Constant") and isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Tipo não suportado")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Operador não permitido")
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Operador unário não permitido")
    raise ValueError("Nodo não suportado")

# --- Interface gráfica ---
class FlutterLikeCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora (Tkinter - estilo Flutter)")
        self.geometry("360x520")
        self.resizable(False, False)
        self.configure(bg="#f2f4f7")

        self.font_large = font.Font(family="Helvetica", size=28, weight="bold")
        self.font_medium = font.Font(family="Helvetica", size=14)
        self.font_button = font.Font(family="Helvetica", size=16, weight="bold")

        self.expression = ""

        container = tk.Frame(self, bg="#f2f4f7")
        container.pack(expand=True, fill="both", padx=18, pady=20)

        card = tk.Frame(container, bg="#ffffff", bd=0, highlightthickness=0)
        shadow = tk.Frame(container, bg="#e6e9ef", bd=0)
        shadow.place(relx=0.5, rely=0.03, anchor="n", relwidth=1)
        card.place(relx=0.5, rely=0.03, anchor="n", relwidth=1, relheight=1)

        # Display principal
        self.display_var = tk.StringVar(value="0")
        display_frame = tk.Frame(card, bg="#ffffff")
        display_frame.pack(fill="x", padx=12, pady=(18, 6))

        self.display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            anchor="e",
            font=self.font_large,
            bg="#ffffff",
            fg="#111827",
            padx=10
        )
        self.display_label.pack(fill="x")

        self.small_expr_var = tk.StringVar(value="")
        small_label = tk.Label(
            display_frame,
            textvariable=self.small_expr_var,
            anchor="e",
            font=self.font_medium,
            bg="#ffffff",
            fg="#6b7280"
        )
        small_label.pack(fill="x", pady=(4, 0))

        # Botões
        buttons_frame = tk.Frame(card, bg="#ffffff")
        buttons_frame.pack(expand=True, fill="both", padx=12, pady=18)

        btn_defs = [
            [("C", "clear"), ("⌫", "back"), ("%", "%"), ("/", "/")],
            [("7", "7"), ("8", "8"), ("9", "9"), ("*", "*")],
            [("4", "4"), ("5", "5"), ("6", "6"), ("-", "-")],
            [("1", "1"), ("2", "2"), ("3", "3"), ("+", "+")],
            [("0", "0"), (".", "."), ("=", "equals")],
        ]

        for r, row in enumerate(btn_defs):
            buttons_frame.rowconfigure(r, weight=1, pad=6)
            for c, (text, val) in enumerate(row):
                buttons_frame.columnconfigure(c, weight=1, pad=6)
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    bg="#f8fafc",
                    bd=0,
                    relief="flat",
                    font=self.font_button,
                    activebackground="#eef2ff",
                    padx=8,
                    pady=8,
                    command=lambda v=val: self.on_button_press(v)
                )

                if val in {"/", "*", "-", "+", "%"}:
                    btn.configure(bg="#0ea5a4", fg="white", activebackground="#089f99")
                elif val == "equals":
                    btn.configure(bg="#6366f1", fg="white", activebackground="#5450d9")
                elif val in {"clear", "back"}:
                    btn.configure(bg="#f97316", fg="white", activebackground="#f65a00")
                else:
                    btn.configure(fg="#111827")

                btn.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)

    def on_button_press(self, val):
        if val == "clear":
            self.expression = ""
            self.update_display()
            return
        if val == "back":
            self.expression = self.expression[:-1]
            self.update_display()
            return
        if val == "equals":
            self.calculate()
            return

        self.expression += val
        self.update_display()

    def calculate(self):
        if not self.expression:
            return
        try:
            result = safe_eval(self.expression)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.small_expr_var.set(self.expression + " =")
            self.expression = str(result)
            self.update_display()
        except Exception:
            self.small_expr_var.set("Erro")
            self.display_var.set("Erro")
            self.expression = ""

    def update_display(self):
        if not self.expression:
            self.display_var.set("0")
            self.small_expr_var.set("")
        else:
            shown = self.expression[-18:] if len(self.expression) > 18 else self.expression
            self.display_var.set(shown)

if __name__ == "__main__":
    app = FlutterLikeCalculator()
    app.mainloop()
# funcao +
def adicao(valor_1, valor_2):
    return valor_1 + valor_2

# funcao -
def subtracao(valor_1, valor_2):
    return valor_1 - valor_2

# funcao *
def multiplicacao(valor_1, valor_2):
    return valor_1 * valor_2

# funcao /
def divisao(valor_1, valor_2):
    return valor_1 / valor_2


print("\nEntrada: \n\na para adicao \ns para subtracao \nm para multiplicacao \nd para divisao \n")

a = int(input("Digite o primeiro numero: "))
b = int(input("Digite o segundo numero: "))

escolha = input("Escolha a operacao: ")

# adicao
if escolha == "a":
    print(adicao(a, b))

# subtracao
if escolha == "s":
    print(subtracao(a, b))

# Multiplicacao
if escolha == "m":
    print(multiplicacao(a, b))

# Divisão
if escolha == "d":
    print(divisao(a, b))
