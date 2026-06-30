"""Autocompletion."""

from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document


_INSTRUCTIONS: list[str] = [
    "maxima",
    "mathematica",
    "from_latex",
    "integrate",
    "integral",
]


class TSCCompleter(Completer):
    """Completer for `:`-prefixed instructions."""

    def get_completions(self, document: Document, complete_event):
        text = document.text_before_cursor
        if not text.startswith(":"):
            return
        # ponytail: only `:`-instruction completion for now;
        # general sympy completion would need expression-aware matching.
        word = text[1:]
        for name in _INSTRUCTIONS:
            if name.startswith(word):
                yield Completion(
                    name,
                    start_position=-len(word),
                    display=name,
                )


def create_completer() -> Completer | None:
    """Return a Completer, or None to disable autocompletion."""
    return TSCCompleter()
