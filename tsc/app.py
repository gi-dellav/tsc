"""REPL application — the main event loop."""

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings

from tsc.completer import create_completer
from tsc.keybindings import create_keybindings
from tsc.lexer import create_lexer
from tsc.style import create_style
from tsc.validator import create_validator

from tsc.interpreter import Interpreter

class TSCApp:
    """Textual Symbolic Calculator REPL."""

    def __init__(self, history_filename: str | None = None) -> None:
        self._session = PromptSession(
            history=self._make_history(history_filename),
            lexer=create_lexer(),
            completer=create_completer(),
            validator=create_validator(),
            key_bindings=create_keybindings(),
            style=create_style(),
            validate_while_typing=False,
        )
        self.interpreter = Interpreter()

    @staticmethod
    def _make_history(filename: str | None) -> FileHistory | None:
        if filename is None:
            return None
        return FileHistory(filename)

    def run(self) -> None:
        """Run the REPL until the user exits."""
        while True:
            try:
                text = self._session.prompt("tsc> ")
            except KeyboardInterrupt:
                continue
            except EOFError:
                break

            if not text.strip():
                continue

            self._evaluate(text)

        print("\nGoodbye!")

    def _evaluate(self, text: str) -> None:
        """Evaluate a line of input. Override this to add real logic."""
        print(self.interpreter.exec_str(text))
