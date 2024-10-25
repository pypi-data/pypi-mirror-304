# calculadora_avancada/calculadora.py

def soma(a, b):
    """Retorna a soma de a e b."""
    return a + b

def subtracao(a, b):
    """Retorna a subtração de b de a."""
    return a - b

def multiplicacao(a, b):
    """Retorna o produto de a e b."""
    return a * b

def divisao(a, b):
    """Retorna a divisão de a por b. Lança um erro se b for zero."""
    if b == 0:
        raise ValueError("Não é possível dividir por zero.")
    return a / b

def potencia(base, expoente):
    """Retorna base elevada ao expoente."""
    return base ** expoente

def raiz_quadrada(x):
    """Retorna a raiz quadrada de x. Lança um erro se x for negativo."""
    if x < 0:
        raise ValueError("Não é possível calcular a raiz quadrada de um número negativo.")
    return x ** 0.5
