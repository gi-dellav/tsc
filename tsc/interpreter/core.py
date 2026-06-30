from sympy import SympifyError, sympify, solve, Eq, simplify

class Interpreter:
    """Core TSC Interpreter"""

    def exec_str(self, expression: str) -> str:
        if len(expression) == 0:
            return "Empty string."

        first_char = expression[0]
        if first_char == "/":
            pass  # TODO Commands for the interactive interface
        elif first_char == ":":
            pass  # TODO Instructions for the interpreter
        elif first_char == "$":
            pass  # TODO Memory assignment
        else:
            return self._evaluate_sympy(expression)

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
