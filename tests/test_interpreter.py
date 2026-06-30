from tsc.interpreter import Interpreter


def _interp() -> Interpreter:
    return Interpreter()


class TestSimpleExpressions:
    def test_integer_arithmetic(self):
        assert _interp().exec_str("2 + 2") == "4"
        assert _interp().exec_str("2**10") == "1024"
        assert _interp().exec_str("10 / 3") == "10/3"

    def test_trig(self):
        assert _interp().exec_str("sin(pi/2)") == "1"

    def test_symbolic(self):
        assert _interp().exec_str("x**2 + 3*x") == "x**2 + 3*x"

    def test_sqrt_simplification(self):
        assert _interp().exec_str("sqrt(8)") == "2*sqrt(2)"


class TestEquations:
    def test_linear_single_solution(self):
        assert _interp().exec_str("x + 2 = 5") == "x = 3"

    def test_quadratic_two_solutions(self):
        result = _interp().exec_str("x**2 = 4")
        assert "x = -2" in result
        assert "x = 2" in result

    def test_tautology_numeric(self):
        assert _interp().exec_str("2 + 2 = 4") == "True"

    def test_contradiction_numeric(self):
        assert _interp().exec_str("2 + 2 = 5") == "False"

    def test_contradiction_symbolic(self):
        assert _interp().exec_str("x = x + 1") == "False"

    def test_identity_symbolic(self):
        assert _interp().exec_str("x = x") == "True"

    def test_multi_variable(self):
        result = _interp().exec_str("y = x + 2")
        assert result == "x = y - 2"


class TestEdgeCases:
    def test_empty_string(self):
        assert _interp().exec_str("") == "Empty string."

    def test_invalid_syntax(self):
        result = _interp().exec_str("foo bar baz")
        assert result.startswith("Error:")
