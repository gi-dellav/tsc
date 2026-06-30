from sympy import SympifyError, sympify, solve, Eq, simplify

from . import parsers
from . import integrals


class Interpreter:
    """Core TSC Interpreter"""

    def exec_str(self, expression: str) -> str:
        if len(expression) == 0:
            return "Empty string."

        first_char = expression[0]
        if first_char == "/":
            pass  # TODO Commands for the interactive interface
        elif first_char == ":":
            return self._exec_instruction(expression[1:])
        elif first_char == "$":
            pass  # TODO Memory assignment
        else:
            return self._evaluate_sympy(expression)

    def _exec_instruction(self, instruction: str) -> str:
        if not instruction.strip():
            return "Empty instruction."
        parts = instruction.split(None, 1)
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else ""
        if cmd == "maxima":
            return parsers.maxima(arg)
        elif cmd == "mathematica":
            return parsers.mathematica(arg)
        elif cmd == "from_latex":
            return parsers.from_latex(arg)
        elif cmd == "integrate" or cmd == "integral":
            return integrals.integrate_cmd(arg)
        else:
            return f"Unknown instruction: :{cmd}"

    def _evaluate_sympy(self, expression: str) -> str:
        try:
            if "=" in expression:
                return self._solve_equation(expression)
            return str(sympify(expression))
        except SympifyError as e:
            return f"Error: {e}"

    def _solve_equation(self, equation: str) -> str:
        left_str, right_str = equation.split("=", 1)
        left = sympify(left_str.strip())
        right = sympify(right_str.strip())
        diff = simplify(left - right)
        if not diff.free_symbols:
            return "True" if diff == 0 else "False"
        solution = solve(Eq(left, right, evaluate=False), dict=True)
        if not solution:
            return "No solution."
        parts = []
        for sol_dict in solution:
            assignments = ", ".join(f"{var} = {val}" for var, val in sol_dict.items())
            parts.append(assignments)
        return "\n".join(parts)
