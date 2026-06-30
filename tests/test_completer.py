from prompt_toolkit.document import Document

from tsc.completer import TSCCompleter

_COMPLETER = TSCCompleter()


def _completions(text: str) -> list[str]:
    doc = Document(text, len(text))
    return [c.text for c in _COMPLETER.get_completions(doc, None)]


class TestColonCompletions:
    def test_colon_only_shows_all(self):
        assert set(_completions(":")) == {
            "maxima", "mathematica", "from_latex", "integrate", "integral"
        }

    def test_partial_match(self):
        assert set(_completions(":m")) == {"maxima", "mathematica"}

    def test_exact_match(self):
        assert _completions(":maxima") == ["maxima"]

    def test_unique_partial(self):
        assert _completions(":f") == ["from_latex"]

    def test_no_match(self):
        assert _completions(":xyz") == []


class TestNoCompletions:
    def test_empty(self):
        assert _completions("") == []

    def test_no_colon(self):
        assert _completions("2 + 2") == []

    def test_colon_not_at_start(self):
        assert _completions("x :m") == []
