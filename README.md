# LLM Content Compression

Token-efficient symbolic notation system for compressing LLM prompts, context files, and instructions - reducing input token count by 30-50% without semantic loss.

## What This Is

A framework for rewriting natural language prompts into compressed symbolic form that LLMs interpret identically but at significantly lower token cost. Includes a complete notation system, transformation rules, and a Python tool that applies them programmatically.

This is particularly useful for:
- CLAUDE.md and project instruction files that are loaded into every session
- Skill/plugin instructions where every token counts against context
- System prompts and recurring context blocks
- Any text an LLM reads repeatedly but humans rarely re-read

## Contents

| File | Purpose |
|------|---------|
| `Symbolic_Prompting_Guide.md` | Comprehensive guide with examples showing how to write compressed prompts. Covers core principles, notation categories, advanced patterns, and best practices. |
| `Symbolic_Prompting_Rules.md` | Complete symbol-to-NLP rule mapping. 14 notation categories, 20 transformation rules (R01-R20), 30+ abbreviations, composition rules, and precedence table. The authoritative legend. |
| `compress_prompt.py` | Python CLI tool that applies the compression rules to any .md or .txt file. Supports dry-run, custom output paths, and compression statistics. |

## Quick Start

### Using the Python Tool

```bash
# Compress a file (writes to <filename>.compressed.md)
python compress_prompt.py ./CLAUDE.md

# Preview without writing (dry-run)
python compress_prompt.py ./skill-instructions.md --dry-run

# Compress to a specific output path
python compress_prompt.py ./context.md --output ./context.min.md

# Show compression statistics
python compress_prompt.py ./CLAUDE.md --stats
```

### Example Transformation

**Before (14 tokens):**
```
Please make sure that all variables are properly annotated with their types
```

**After (7 tokens):**
```
ensure: type-annotate all vars
```

**Before (42 tokens):**
```
First run the linter to check for errors. If the linter passes, run the test
suite. If tests pass, build the Docker image. Finally, if the build succeeds,
push the image to the container registry and deploy to the staging environment.
```

**After (12 tokens):**
```
lint ok; test ok; docker build; push registry -> deploy staging
```

## Notation Overview

The system defines operators across these categories:

| Category | Symbols | Example |
|----------|---------|---------|
| Flow/Sequence | `->` `;` `>>` `\|` `+` | `parse -> validate -> store` |
| Conditionals | `?` `!` `&&` `\|\|` `?:` | `err? -> retry` |
| Quantifiers | `*` `@` `#N` `..` `~` | `* fn @ src/: typed` |
| Assignment | `=` `:=` `+=` `-=` `<-` | `config <- env vars` |
| Validation | checkmark / x / `>=` / `<=` | `x bare except; coverage >= 80%` |
| Grouping | `()` `[]` `{}` `<>` `/` | `status: {ok, err, pending}` |

Full reference in `Symbolic_Prompting_Rules.md`.

## Compression Rules (Summary)

| NLP Pattern | Symbolic Form | Rule |
|-------------|--------------|------|
| "make sure that X" | `ensure: X` | R01 |
| "do not X" / "never X" | `x X` | R02 |
| "if X then Y" | `X? -> Y` | R03 |
| "for each X in Y, check Z" | `* X @ Y: Z` | R04 |
| "X at least N" | `X >= N` | R05 |
| "X at most N" | `X <= N` | R06 |
| "set X to Y" | `X = Y` | R07 |
| "X reads from Y" | `X <- Y` | R08 |
| "after X, do Y" | `X; Y` | R09 |
| "either X or Y" | `X \| Y` | R10 |
| "both X and Y" | `X + Y` | R11 |
| "X returns Y" | `X -> Y` | R14 |
| "optionally X" | `[X]` | R16 |
| "one of X, Y, Z" | `{X, Y, Z}` | R17 |

## Requirements

- Python 3.10+ (uses `from __future__ import annotations`, `dataclass`, `pathlib`)
- No external dependencies - stdlib only

## When NOT to Compress

- User-facing documentation (README files, code comments)
- Error messages shown to end users
- Git commit messages
- Content that other humans need to read and edit frequently
- Code itself (only compress the instructions around code)

## Related

This notation system powers the [`compress-context`](https://github.com/rs2pydev/claude-skills) Claude Code skill plugin, which applies these transformations interactively inside a Claude Code session.

## License

MIT
