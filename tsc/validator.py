"""Input validators.

Uses `Validator.from_callable` for simple boolean functions.
"""

from prompt_toolkit.validation import Validator


def _is_acceptable(text: str) -> bool:
    """Return True if *text* is valid input."""
    # ponytail: stub — replace with real validation logic
    return True


def create_validator() -> Validator:
    """Return a Validator for the REPL prompt.

    Override `_is_acceptable` above to change the validation rule.
    """
    return Validator.from_callable(
        _is_acceptable,
        error_message="Invalid input",
        move_cursor_to_end=True,
    )
