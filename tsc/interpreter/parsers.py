from sympy.parsing.maxima import parse_maxima
from sympy.parsing.mathematica import parse_mathematica
from sympy.parsing.latex import parse_latex


def maxima(expr: str) -> str:
    try:
        return str(parse_maxima(expr))
    except Exception as e:
        return f"Error parsing Maxima: {e}"


def mathematica(expr: str) -> str:
    try:
        return str(parse_mathematica(expr))
    except Exception as e:
        return f"Error parsing Mathematica: {e}"


def from_latex(expr: str) -> str:
    try:
        return str(parse_latex(expr))
    except Exception as e:
        return f"Error parsing LaTeX: {e}"
