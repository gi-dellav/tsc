# Architecture

## Directory Layout

```
tsc/
├── __init__.py          # Package marker, version 0.1.0
├── __main__.py           # Entry point: main() → TSCApp.run()
├── app.py                # TSCApp: prompt_toolkit REPL session + loop
├── completer.py          # Autocomplete stub (ponytail: not yet implemented)
├── keybindings.py        # Custom keybindings stub
├── lexer.py              # Syntax highlighting stub
├── style.py              # Colors/theme stub
├── validator.py          # Input validator (always returns True)
└── interpreter/
    ├── __init__.py       # Re-exports Interpreter from .core
    ├── core.py           # Interpreter: symbolic eval engine (dispatch, sympy, solve)
    ├── parsers.py        # Wraps SymPy parsers: :maxima, :mathematica, :from_latex
    └── integrals.py      # :integrate command → sympy.integrate()
tests/
└── test_interpreter.py   # pytest-style tests for Interpreter
```

## Key Types

### `TSCApp` (`app.py`)
Owns the REPL loop. Creates a `prompt_toolkit.PromptSession` with history, lexer, completer,
validator, keybindings, and style (all currently `None`/stubs). Holds an `Interpreter`
instance. `run()` loops on `session.prompt("tsc> ")` and calls `_evaluate()`.

### `Interpreter` (`interpreter/core.py`)
Central evaluation engine. One public method: `exec_str(expression: str) -> str`.
Routes by first character:

| Prefix  | Handler               | Description                          |
|---------|-----------------------|--------------------------------------|
| `/`     | no-op                 | Reserved for future commands         |
| `:`     | `_exec_instruction()` | Dispatches to parsers or integrals   |
| `$`     | no-op                 | Reserved for future memory/assignment|
| default | `_evaluate_sympy()`   | Normal symbolic math                 |

`_evaluate_sympy()` detects `=` in the expression → `_solve_equation()`, otherwise
`sympify(expr)`. `_solve_equation()` sympifies both sides, simplifies the difference;
if no free symbols → `"True"/"False"`, else → `solve(Eq(lhs, rhs))`.

### Factory stubs (`completer.py`, `keybindings.py`, `lexer.py`, `style.py`, `validator.py`)
Each exports a function returning a `prompt_toolkit` component or `None`. All marked
`# ponytail: stub` — not yet wired up.

## Control Flow

```
python -m tsc  (or `tsc` console script)
  └─ __main__.py:main()
      └─ TSCApp(history_filename=sys.argv[1])
          └─ .run()
              └─ loop:
                  1. session.prompt("tsc> ")   → user input
                  2. _evaluate(text)
                     └─ interpreter.exec_str(text)
                         ├─ prefix "/" → (reserved, empty string)
                         ├─ prefix ":" → _exec_instruction()
                         │   ├─ ":maxima <expr>"       → parse_maxima()
                         │   ├─ ":mathematica <expr>"  → parse_mathematica()
                         │   ├─ ":from_latex <expr>"   → parse_latex()
                         │   └─ ":integrate <expr>"    → sympy.integrate()
                         ├─ prefix "$" → (reserved, empty string)
                         └─ else → _evaluate_sympy()
                             ├─ "=" in expr → _solve_equation()
                             └─ else → str(sympify(expr))
                  3. print(result)
                  4. Ctrl+D (EOFError) → "Goodbye!", exit
```

## Data Flow

1. **Raw string** from prompt_toolkit session
2. **Prefix dispatch** in `exec_str()` — first character determines path
3. **Syntax conversion** (parsers path): foreign syntax string → SymPy internal
   representation via `parse_maxima`/`parse_mathematica`/`parse_latex` → SymPy expression
4. **Symbolic evaluation** (default path): string → `sympify()` → SymPy expression → `str()`
5. **Equation solving** (if `=` present): split on `=` → sympify both sides →
   `simplify(lhs - rhs)` → if no free symbols, return boolean string; otherwise
   `solve(Eq(...))` → formatted string
6. **Integration** (`:integrate`): expression string → `sympy.integrate()` → result string
7. **Output**: result string printed to terminal

## Design Decisions

- **SymPy as sole CAS engine**: no symbolic math is reimplemented — `sympify`, `solve`,
  `Eq`, `simplify`, `integrate`, and parsers are all delegated to SymPy.
- **prompt_toolkit for REPL**: provides cross-platform terminal UI (history, completion,
  syntax highlighting hooks) without a GUI dependency. Currently only history is wired;
  other hooks are stubs.
- **Prefix-based command routing**: `/` and `$` reserved for future commands and memory.
  `:` for metaprogramming (parsers, integrals). Simple single-char dispatch avoids parser
  complexity.
- **Equation detection by `=`**: heuristic split on `=` — simpler than a full parser.
  Works for `x + 2 = 5`-style input.
- **Stub everything until needed**: `completer`, `lexer`, `style`, `keybindings` all
  return `None` with `# ponytail:` comments naming the upgrade path. No scaffolding for
  future features.
- **Single interpreter class**: `Interpreter` is a flat class (~80 lines) with all logic
  in one file — no plugin system, no abstract evaluator. YAGNI at this scale.
- **Python >= 3.10**: match syntax, modern type hints available.

## Dependencies

| Dependency        | Usage                                                                                |
|-------------------|--------------------------------------------------------------------------------------|
| `sympy`           | `sympify()`, `solve()`, `Eq()`, `simplify()`, `integrate()`, `parse_maxima()`, `parse_mathematica()`, `parse_latex()` |
| `prompt-toolkit`  | `PromptSession`, `FileHistory` — terminal REPL with history persistence              |

Build: `setuptools >= 75`, no lockfile. Testing: `pytest` (implicit — no import, just
`assert`-based tests in `tests/test_interpreter.py`).

## Entry Points

1. **`tsc`** — console script defined in `pyproject.toml` → `tsc.__main__:main`
2. **`python -m tsc`** — `__main__.py` → `main()`
3. Both accept an optional history filename as `sys.argv[1]`
