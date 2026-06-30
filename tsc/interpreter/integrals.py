from sympy import sympify, SympifyError
from sympy.integrals.integrals import integrate


def integrate_cmd(arg: str) -> str:
    try:
        parts = sympify(f"({arg})")
        if not isinstance(parts, tuple):
            parts = (parts,)
        result = integrate(*parts)
        return str(result)
    except SympifyError as e:
        return f"Error parsing arguments: {e}"
    except Exception as e:
        return f"Error: {e}"
