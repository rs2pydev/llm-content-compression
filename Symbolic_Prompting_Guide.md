# Symbolic Prompting Guide

A comprehensive guide for writing token-efficient prompts using symbolic notation. This technique reduces input token count by 30-50% while maintaining full semantic clarity for LLMs.

## Why Symbolic Prompting?

LLM tokenizers break text into subword tokens. Natural language is verbose - filler words, connectives, and redundant phrasing inflate token counts without adding meaning. Symbolic prompting replaces multi-token phrases with single-token or low-token equivalents that LLMs interpret identically.

**Token cost comparison:**

| Natural Language | Tokens | Symbolic | Tokens | Savings |
|-----------------|--------|----------|--------|---------|
| "Please make sure that all variables are properly annotated with their types" | ~14 | `ensure: type-annotate all vars` | ~7 | 50% |
| "If the test fails, then log the error and retry up to 3 times" | ~15 | `test fails -> log(err) + retry(max=3)` | ~10 | 33% |
| "For every file in the source directory, check that it has a docstring" | ~14 | `for f in src/: assert f.docstring exists` | ~9 | 36% |

## Core Principles

### 1. Eliminate Filler

Remove words that carry no semantic weight:

```
# Verbose (11 tokens)
"Please go ahead and run the test suite for me"

# Compressed (4 tokens)
"run test suite"
```

Filler words to eliminate: please, go ahead, just, simply, basically, actually, make sure to, be sure to, go ahead and, I would like you to, could you please.

### 2. Use Operators for Relationships

Replace verbal descriptions of relationships with symbolic operators:

```
# Verbose (12 tokens)
"After the build completes successfully, deploy to staging"

# Compressed (5 tokens)
"build ok -> deploy staging"
```

### 3. Structured Key-Value Over Prose

Replace descriptive paragraphs with structured data:

```
# Verbose (35 tokens)
"The project uses Python version 3.11 for the backend, React version 19 for
the frontend, and PostgreSQL version 16 for the database. Tests are run using
pytest with the async mode set to auto."

# Compressed (12 tokens)
"stack: py3.11 | react19 | pg16
test: pytest(asyncio=auto)"
```

### 4. Implicit Subjects

When context makes the subject obvious, omit it:

```
# Verbose
"The function should return a list of strings"

# Compressed (subject is the function being discussed)
"-> list[str]"
```

## Notation Categories

### Flow and Sequence

| Symbol | Meaning | Example |
|--------|---------|---------|
| `->` | leads to / then / results in | `parse -> validate -> store` |
| `=>` | implies / therefore / causes | `err => retry` |
| `>>` | pipe / pass output to | `fetch >> transform >> render` |
| `;` | sequential steps | `lint; test; build` |
| `\|` | parallel / or / alternative | `redis \| memcached` |

**Example - deployment pipeline:**

```
# Verbose (42 tokens)
"First run the linter to check for errors. If the linter passes, run the test
suite. If tests pass, build the Docker image. Finally, if the build succeeds,
push the image to the container registry and deploy to the staging environment."

# Compressed (12 tokens)
"lint ok; test ok; docker build; push registry -> deploy staging"
```

### Conditionals and Logic

| Symbol | Meaning | Example |
|--------|---------|---------|
| `?` | if / when / condition | `err? -> retry` |
| `!` | not / negate / prevent | `!mutate args` |
| `&&` | and (both required) | `valid && auth -> allow` |
| `\|\|` | or (either sufficient) | `cache \|\| fetch` |
| `?:` | if-else (ternary) | `prod? https : http` |

**Example - error handling logic:**

```
# Verbose (38 tokens)
"If the API call returns a 429 status code, wait for the duration specified
in the Retry-After header and then retry the request. If it returns a 500,
log the error and raise an exception. For any other error, return a default value."

# Compressed (15 tokens)
"429? -> wait(Retry-After) + retry
500? -> log(err) + raise
else? -> return default"
```

### Quantifiers and Scope

| Symbol | Meaning | Example |
|--------|---------|---------|
| `*` | all / every / each | `* fn: typed params` |
| `@` | at / in / within | `@ src/`: within src directory |
| `#N` | count / number | `retry #3` (retry 3 times) |
| `..` | range / through | `lines 10..50` |
| `~` | approximately / about | `~100ms latency` |

**Example - code audit scope:**

```
# Verbose (28 tokens)
"Check every Python file in the source directory. Each function must have
type annotations on all parameters and a return type. Each class must have
a docstring with an Attributes section."

# Compressed (11 tokens)
"@ src/*.py:
  * fn: typed params + -> ReturnType
  * cls: docstring w/ Attributes"
```

### Assignment and State

| Symbol | Meaning | Example |
|--------|---------|---------|
| `=` | is / equals / set to | `timeout = 30s` |
| `:=` | define as / configure as | `logger := getLogger(__name__)` |
| `+=` | add / append / include | `deps += pytest` |
| `-=` | remove / exclude | `deps -= unused` |
| `<-` | receives from / depends on | `config <- env vars` |

**Example - configuration:**

```
# Verbose (30 tokens)
"Set the database connection timeout to 30 seconds. The maximum pool size
should be 10 connections. Enable SSL mode and set the certificate path to
the value of the DB_CERT_PATH environment variable."

# Compressed (10 tokens)
"db.timeout = 30s
db.pool_max = 10
db.ssl = on, cert <- $DB_CERT_PATH"
```

### Validation and Assertions

| Symbol | Meaning | Example |
|--------|---------|---------|
| `checkmark` | required / must have / ensure | `checkmark typed, checkmark tested` |
| `x` | forbidden / must not | `x bare except` |
| `!=` | must not equal / differs from | `password != username` |
| `>=` | at least / minimum | `coverage >= 80%` |
| `<=` | at most / maximum | `fn LOC <= 30` |

**Example - code quality gates:**

```
# Verbose (45 tokens)
"All functions must have type annotations. No function should exceed 30 lines
of code. Test coverage must be at least 80 percent. There must be no bare
except clauses. Every module must have a docstring. No print statements
should exist in production code."

# Compressed (12 tokens)
"gates:
  checkmark type annotations (all fn)
  x fn LOC > 30
  checkmark coverage >= 80%
  x bare except
  checkmark module docstrings
  x print() in prod"
```

### Grouping and Structure

| Symbol | Meaning | Example |
|--------|---------|---------|
| `()` | group / scope | `(fetch + parse) -> store` |
| `[]` | optional / array / list | `fn(x, [y]) -> z` |
| `{}` | set / one-of / enum | `status: {ok, err, pending}` |
| `<>` | type / generic / template | `list<str>` |
| `/` | or / per / divide | `req/sec`, `pass/fail` |

**Example - API specification:**

```
# Verbose (50 tokens)
"The endpoint accepts POST requests at /api/cases. The request body must
contain a case_id field which is a string, a patient object which contains
name and date_of_birth fields, and an optional notes field which is a string.
The response returns either a success object with a case_id and status, or
an error object with a code and message."

# Compressed (14 tokens)
"POST /api/cases
body: {case_id: str, patient: {name, dob}, [notes]: str}
resp: {case_id, status} | err{code, msg}"
```

## Compression Patterns for Common Contexts

### CLAUDE.md Files

```
# Verbose CLAUDE.md section (60+ tokens)
"When working with this project, always run the linter before committing.
The backend uses Python 3.11 with FastAPI. Tests should be run using pytest
with verbose output. The frontend uses React 19 with TypeScript and Vite.
Never hardcode the client name - always read it from client_config.yaml."

# Compressed (18 tokens)
"## Rules
pre-commit: lint
backend: py3.11 + FastAPI
test: pytest -v
frontend: react19 + ts + vite
client name <- client_config.yaml (never hardcode)"
```

### Skill Instructions

```
# Verbose skill instruction (40 tokens)
"For each Python file in the given folder, check that it has a module-level
docstring. If a docstring is missing, add one that describes the module's
purpose, its key exports, and any important dependencies."

# Compressed (12 tokens)
"@ <folder>/*.py:
  missing docstring? -> add:
    - purpose
    - key exports
    - dependencies"
```

### Task Decomposition

```
# Verbose (55 tokens)
"I need you to do the following things in order. First, read the configuration
file to understand the current settings. Second, identify which settings need
to be changed based on the requirements I provided. Third, make the changes
to the configuration file. Fourth, validate that the configuration is still
valid after the changes. Finally, summarize what was changed."

# Compressed (10 tokens)
"steps:
  1. read config
  2. diff vs requirements
  3. apply changes
  4. validate
  5. summarize delta"
```

## Advanced Patterns

### Templated Compression

Define a pattern once, reuse with substitution:

```
# Pattern definition
"audit_phase(tool, target, metric) := run {tool} on {target} -> capture {metric}"

# Usage (each expands to a full instruction)
"audit_phase(ruff, src/, violations)
audit_phase(pyright --strict, src/, errors)
audit_phase(pytest, tests/, pass/fail)"
```

### Nested Scope

Use indentation to express containment:

```
"@ backend/:
  * fn:
    params: typed
    return: typed
    body: <= 30 LOC
  * cls:
    docstring: NumPy style
    methods: same rules as fn
  * module:
    top: docstring
    imports: sorted (isort)"
```

### Conditional Chains

```
"input -> validate
  valid? -> process -> store -> respond(200)
  invalid? -> log(warn) -> respond(400, errors)
  exception? -> log(err) -> respond(500) + alert"
```

## Best Practices

1. **Be consistent** - Pick one symbol for each concept and use it everywhere
2. **Preserve ambiguity boundaries** - If a compression could be misread, keep it verbose
3. **Group related rules** - Use sections and indentation, not scattered symbols
4. **Test comprehension** - If Claude misinterprets a compressed prompt, it's too compressed
5. **Keep a legend** - Maintain `Symbolic_Prompting_Rules.md` alongside compressed content
6. **Don't compress proper nouns** - File paths, function names, and identifiers stay literal
7. **Don't compress code examples** - Actual code snippets should remain uncompressed

## When NOT to Compress

- User-facing documentation (README, comments in code)
- Error messages shown to end users
- Git commit messages
- Content that other humans need to read and edit frequently
- Code itself (only compress the prompts/instructions around code)
