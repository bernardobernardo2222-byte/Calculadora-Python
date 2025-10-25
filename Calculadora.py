#Calculadora Python

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