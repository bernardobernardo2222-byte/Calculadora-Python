#Calculadora Python
import tkinter as tk
from tkinter import ttk
import ast
import operator

# --- Função de avaliação segura de expressões ---
# Aceita números, parênteses e operadores: + - * / ** % (potência e módulo)
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

ALLOWED_UNARY = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def safe_eval(expr: str):
    """
    Avalia expressões matemáticas simples de forma segura usando AST.
    Lança ValueError se a expressão contiver algo não permitido.
    """
    expr = expr.strip()
    if not expr:
        raise ValueError("Expressão vazia")

    node = ast.parse(expr, mode="eval")

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in ALLOWED_OPERATORS:
                return ALLOWED_OPERATORS[op_type](left, right)
            raise ValueError(f"Operador não permitido: {op_type}")
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in ALLOWED_UNARY:
                return ALLOWED_UNARY[op_type](operand)
            raise ValueError(f"Unary operator not allowed: {op_type}")
        if isinstance(node, ast.Constant):  # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Somente números são permitidos")
        if isinstance(node, ast.Num):  # older AST node
            return node.n
        if isinstance(node, ast.Call):
            raise ValueError("Chamadas de função não são permitidas")
        raise ValueError(f"Elemento não permitido: {type(node)}")

    return _eval(node)


# --- UI ---
class Calculadora(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Tkinter")
        self.resizable(False, False)
        self.configure(padx=8, pady=8)

        self.valor = tk.StringVar()
        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        entry = ttk.Entry(self, textvariable=self.valor, font=("Segoe UI", 20), justify="right")
        entry.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 8))
        entry.focus_set()

        btn_specs = [
            ("C", 1, 0, self.limpar),
            ("⌫", 1, 1, self.apagar),
            ("%", 1, 2, lambda: self.adicionar("%")),
            ("/", 1, 3, lambda: self.adicionar("/")),

            ("7", 2, 0, lambda: self.adicionar("7")),
            ("8", 2, 1, lambda: self.adicionar("8")),
            ("9", 2, 2, lambda: self.adicionar("9")),
            ("*", 2, 3, lambda: self.adicionar("*")),

            ("4", 3, 0, lambda: self.adicionar("4")),
            ("5", 3, 1, lambda: self.adicionar("5")),
            ("6", 3, 2, lambda: self.adicionar("6")),
            ("-", 3, 3, lambda: self.adicionar("-")),

            ("1", 4, 0, lambda: self.adicionar("1")),
            ("2", 4, 1, lambda: self.adicionar("2")),
            ("3", 4, 2, lambda: self.adicionar("3")),
            ("+", 4, 3, lambda: self.adicionar("+")),

            ("+/-", 5, 0, self.trocar_sinal),
            ("0", 5, 1, lambda: self.adicionar("0")),
            (".", 5, 2, lambda: self.adicionar(".")),
            ("=", 5, 3, self.calcular),
        ]

        for (text, r, c, cmd) in btn_specs:
            btn = ttk.Button(self, text=text, command=cmd)
            btn.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

        # Ajusta colunas/linhas para redimensionamento (mesmo que fixed size)
        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.grid_columnconfigure(j, weight=1)

    # --- ações ---
    def adicionar(self, s: str):
        cur = self.valor.get()
        # evita dois pontos ou múltiplos operadores inicialmente (simples heurística)
        self.valor.set(cur + s)

    def limpar(self):
        self.valor.set("")

    def apagar(self):
        self.valor.set(self.valor.get()[:-1])

    def trocar_sinal(self):
        cur = self.valor.get().strip()
        if not cur:
            return
        # tenta avaliar e inverter sinal; fallback simples
        try:
            val = safe_eval(cur)
            val = -val
            self.valor.set(self._format_result(val))
        except Exception:
            # fallback: se começa com '-', remove; senão coloca '-'
            if cur.startswith("-"):
                self.valor.set(cur[1:])
            else:
                self.valor.set("-" + cur)

    def calcular(self, _event=None):
        expr = self.valor.get()
        try:
            resultado = safe_eval(expr)
            self.valor.set(self._format_result(resultado))
        except Exception as e:
            self.valor.set("Erro")
            # opcional: após 1.2s limpamos a mensagem de erro
            self.after(1200, lambda: self.valor.set(""))

    def _format_result(self, value):
        # mostra inteiro sem .0
        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            # limita casas decimais (removendo zeros desnecessários)
            s = f"{value:.10f}".rstrip("0").rstrip(".")
            return s
        return str(value)

    # --- teclado ---
    def _bind_keys(self):
        self.bind("<Return>", self.calcular)
        self.bind("<KP_Enter>", self.calcular)
        self.bind("<Escape>", lambda e: self.limpar())
        self.bind("<BackSpace>", lambda e: self.apagar())
        # números, operadores básicos e ponto
        for key in "0123456789+-*/().%":
            self.bind(key, lambda e, ch=key: self.adicionar(ch))
        # tecla +/- (não existe pad numérico universal) -> use n para trocar sinal
        self.bind("n", lambda e: self.trocar_sinal())


if __name__ == "__main__":
    app = Calculadora()
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
